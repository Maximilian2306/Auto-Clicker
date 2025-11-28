# autoclicker/gui/gui_manager.py
"""GUIManager - Main GUI Coordinator (MVC View Layer)"""

from typing import Optional
import sys
from pathlib import Path
import ttkbootstrap as ttkb
from ttkbootstrap import Window, Style
from tkinter import filedialog

from .components import (TopBar, StatusBar, MainTab, PatternsTab, StatsTab, SettingsTab)
from .handlers.status_handler import StatusHandler
from .handlers.profile_handler import ProfileHandler
from ..model import ApplicationModel
from ..utils.toast_notification import ToastManager
from ..utils.window_sizing import calculate_optimal_window_size, get_centered_geometry
from ..utils.validators import validate_delay, validate_duration, validate_repeat, validate_coordinates
from .. import events


# Type alias for optional string return
OptionalStr = Optional[str]


class GUIManager:
    """Main GUI coordinator implementing MVC View pattern"""

    def __init__(self, model: ApplicationModel):
        self.model = model

        # === Window Setup ===
        self.root = Window(themename="cyborg")
        self.root.title("ClickMAX")

        # === Calculate window size ===
        initial_width, initial_height = calculate_optimal_window_size(self.root, "English")
        initial_geometry = get_centered_geometry(self.root, initial_width, initial_height)
        self.root.geometry(initial_geometry)
        self.root.resizable(True, True)

        # === Set Window Icon ===
        if getattr(sys, 'frozen', False):
            icon_path = Path(sys._MEIPASS) / "icon.ico" # Running as EXE
        else:
            icon_path = Path(__file__).parent.parent.parent / "icon.ico" # Running from source

        if icon_path.exists():
            self.root.iconbitmap(str(icon_path))

        # === Theme & Style ===
        self.style: Style = Style("cyborg")
        self.current_theme_index = 0

        # === Toast Notification Manager ===
        self.toast = ToastManager(self.root)

        # === Initialize Handlers ===
        self.status_handler = StatusHandler(self)
        self.profile_handler = ProfileHandler(self)

        # === Register Callbacks ===
        self.model.set_status_callback(self.update_status)
        self.model.set_notify_callback(self._show_notification)

        # === Initialize Model Variables (MUST be after Window creation) ===
        self.model.initialize_variables(self.root)
        self.model.on_language_update = self.refresh_translations

        # === UI Components Registry ===
        self._ui_components = []

        # === Initialize Themes ===
        try:
            self.model.theme_manager.set_available_themes(self.style.theme_names())
        except Exception as e:
            print(f"[WARN] Failed to initialize themes: {e}")

        # === Register Callbacks in Model ===
        self.model.set_coordinates_callback(self._on_coordinates_received)
        # === Build UI ===
        self._build_ui()
        # === Setup Hotkeys ===
        self._setup_hotkeys()

        # === Load Last Used Profile ===
        last = self.model.profiles.load_last_profile()
        if last and last in self.model.get_profile_list():
            self._on_load_profile(last)
        else:
            self._on_load_profile("Default")

        # === Initialize Hotkey Labels on All Buttons ===
        self.update_all_hotkey_labels()
        # === Handle Window Close Event ===
        self.root.protocol("WM_DELETE_WINDOW", self._on_window_close)

    def t(self, key: str) -> str:
        """Get translated text for key"""
        return self.model.translation_manager.get_text(key)

    def _adjust_window_size_for_language(self):
        """Adjust window size based on current language and screen dimensions"""
        try:
            if not hasattr(self.model, 'language') or self.model.language is None:
                return

            current_lang = self.model.language.get()
            optimal_width, optimal_height = calculate_optimal_window_size(self.root, current_lang)

            # Try to preserve current window position
            current_geometry = self.root.geometry()
            if '+' in current_geometry:
                parts = current_geometry.split('+')
                if len(parts) >= 3:
                    try:
                        x_pos, y_pos = int(parts[1]), int(parts[2])
                        new_geometry = f"{optimal_width}x{optimal_height}+{x_pos}+{y_pos}"
                    except (ValueError, IndexError):
                        new_geometry = get_centered_geometry(self.root, optimal_width, optimal_height)
                else:
                    new_geometry = get_centered_geometry(self.root, optimal_width, optimal_height)
            else:
                new_geometry = get_centered_geometry(self.root, optimal_width, optimal_height)

            self.root.geometry(new_geometry)

        except Exception as e:
            print(f"[WARN] Failed to adjust window size: {e}")

    @property
    def state(self):
        """Access current application state variables"""
        return {
            "language": self.model.language,
            "current_profile": self.model.current_profile,
            "total_clicks": self.model.total_clicks,
            "session_time": self.model.session_time,
            "click_rate": self.model.click_rate,
        }

    # ============================================
    # === UI CONSTRUCTION ===
    # ============================================

    def _build_ui(self):
        """Build complete UI structure (called once during initialization)"""
        main_container = ttkb.Frame(self.root, padding=0)
        main_container.pack(fill="both", expand=True)

        # === Top Bar ===
        self.top_bar = TopBar(
            parent=main_container,
            manager=self,
            on_cycle_theme=self._on_cycle_theme,
            on_load_profile=self._on_load_profile,
        )

        # === Notebook (Tabs Container) ===
        self.notebook = ttkb.Notebook(main_container, bootstyle="dark")
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)

        # === Main Controls Tab ===
        self.main_tab = MainTab(
            parent=self.notebook,
            manager=self,
            on_toggle_clicker=self._on_toggle_clicker,
            on_capture_coordinates=self._on_capture_coordinates,
        )
        self.notebook.add(self.main_tab, text="🎯 Main Controls")

        # === Patterns & Macros Tab ===
        self.patterns_tab = PatternsTab(
            parent=self.notebook,
            manager=self,
            on_record_macro=self._on_record_macro,
            on_stop_macro=self._on_stop_macro,
            on_play_macro=self._on_play_macro,
        )
        self.notebook.add(self.patterns_tab, text="🎨 Patterns")
        self.model.on_macro_status_update = self.patterns_tab.update_macro_status

        # === Statistics Tab ===
        self.stats_tab = StatsTab(
            parent=self.notebook,
            manager=self,
            on_export_stats=self._on_export_stats,
            on_reset_stats=self._on_reset_stats,
        )
        self.notebook.add(self.stats_tab, text="📊 Statistics")
        self.model.on_progress_changed = self.stats_tab.update_progress

        # === Settings Tab ===
        available_themes = (
            self.model.theme_manager.available_themes
            if self.model.theme_manager.available_themes
            else self.style.theme_names()
        )

        self.settings_tab = SettingsTab(
            parent=self.notebook,
            manager=self,
            on_save_profile=self._on_save_profile,
            on_load_profile=self._on_load_profile,
            on_delete_profile=self._on_delete_profile,
            on_apply_theme=self._on_apply_theme,
            available_themes=available_themes,
            on_set_hotkey=self._on_set_hotkey,
            on_ask_string=self._ask_string,
            on_get_profile_list=self.model.get_profile_list,
        )
        self.notebook.add(self.settings_tab, text="🔧 Settings")

        # === Status Bar ===
        self.status_bar = StatusBar(main_container, self)

        # === Register UI Components for Translation Refresh ===
        self._ui_components = [
            self.top_bar,
            self.main_tab,
            self.patterns_tab,
            self.stats_tab,
            self.settings_tab,
            self.status_bar,
        ]

    def _setup_hotkeys(self):
        """Setup global hotkeys and register callback references"""
        self.model.register_hotkey_callbacks(
            toggle_clicker=self._on_toggle_clicker,
            capture_coordinates=self._on_capture_coordinates,
            exit_program=self._on_window_close,
            start_macro_recording=self._on_record_macro,
            stop_macro_recording=self._on_stop_macro,
            play_macro_recording=self._on_play_macro,
        )

        self.model.setup_default_hotkeys(
            on_toggle=self._on_toggle_clicker,
            on_capture=self._on_capture_coordinates,
            on_exit=self._on_window_close,
            on_record=self._on_record_macro,
            on_stop=self._on_stop_macro,
            on_play=self._on_play_macro,
        )

    # ============================================
    # === HOTKEY CALLBACKS ===
    # ============================================

    def _on_set_hotkey(self, name: str, key: str):
        """Handle hotkey change from SettingsTab"""
        success = self.model.update_hotkey(name, key)
        if success:
            self.update_status(events.HOTKEY_REGISTERED, key=key.upper())
            # Update all button labels to show new hotkeys
            self.update_all_hotkey_labels()
        else:
            self.update_status(events.HOTKEY_REGISTER_ERROR)

    def update_all_hotkey_labels(self):
        """Update all button labels to show current hotkey bindings"""
        try:
            hotkeys = self.model.hotkeys.get_all_hotkeys()

            if hasattr(self, 'main_tab'):
                capture_key = hotkeys.get("capture_coordinates", "F7")
                toggle_key = hotkeys.get("toggle_clicker", "F6")
                self.main_tab.update_hotkey_labels(
                    capture_key=capture_key,
                    toggle_key=toggle_key
                )

            if hasattr(self, 'patterns_tab'):
                record_key = hotkeys.get("start_macro_recording", "F3")
                stop_key = hotkeys.get("stop_macro_recording", "F4")
                play_key = hotkeys.get("play_macro_recording", "F5")
                self.patterns_tab.update_hotkey_labels(
                    record_key=record_key,
                    stop_key=stop_key,
                    play_key=play_key
                )
        except Exception as e:
            print(f"Error updating hotkey labels: {e}")

    # ============================================
    # === CLICKER CALLBACKS ===
    # ============================================

    def _show_notification(self, _event_code: str):
        """Show notification on GUI thread (thread-safe)"""
        t = self.model.translation_manager.get_text
        message = t('clicker_completed')

        def show():
            self.model.notification_manager.show_success(
                message,
                title=t('app_title')
            )

        self.root.after(0, show)

    def _ask_string(self, title: str = "Input", prompt: str = "Enter value:", info_text: str = None, initial_value: str = "") -> Optional[str]:
        """Show input dialog and return user input"""
        return self.model.notification_manager.ask_string(title, prompt, info_text, initial_value)

    def _on_toggle_clicker(self):
        """Handle start/stop button click from MainTab"""
        # Get raw string values to avoid TclError on invalid input
        # Use tk.getvar() to get the raw string value before type conversion
        try:
            delay_str = str(self.main_tab.delay_var.get())
        except Exception:
            delay_str = self.root.tk.getvar(self.main_tab.delay_var._name)

        try:
            duration_str = str(self.main_tab.duration_var.get())
        except Exception:
            duration_str = self.root.tk.getvar(self.main_tab.duration_var._name)

        try:
            repeat_str = str(self.main_tab.repeat_var.get())
        except Exception:
            repeat_str = self.root.tk.getvar(self.main_tab.repeat_var._name)

        # Validate delay
        is_valid, error, delay = validate_delay(delay_str)
        if not is_valid:
            self.toast.show(error, "warning")
            return

        # Validate duration
        is_valid, error, duration = validate_duration(duration_str)
        if not is_valid:
            self.toast.show(error, "warning")
            return

        # Validate repeat
        is_valid, error, repeat = validate_repeat(repeat_str)
        if not is_valid:
            self.toast.show(error, "warning")
            return

        notify_when_done = self.main_tab.notify_var.get()

        # Validate coordinates if provided
        x_str = self.main_tab.x_entry.get().strip()
        y_str = self.main_tab.y_entry.get().strip()

        if x_str and y_str:
            is_valid, error, (fixed_x, fixed_y) = validate_coordinates(x_str, y_str)
            if not is_valid:
                self.toast.show(error, "warning")
                return
        else:
            fixed_x, fixed_y = None, None

        click_type = self.main_tab.click_type_var.get()
        pattern = self.patterns_tab.pattern_var.get()
        pattern_size = self.patterns_tab.pattern_size_var.get()
        random_delay = self.main_tab.random_delay_var.get()

        click_while_pattern = self.patterns_tab.click_while_pattern_var.get()
        interrupt_on_move = self.patterns_tab.interrupt_on_move_var.get()

        btn = self.main_tab.start_button
        button_x = btn.winfo_rootx()
        button_y = btn.winfo_rooty()
        button_width = btn.winfo_width()
        button_height = btn.winfo_height()
        button_bounds = (button_x, button_y, button_x + button_width, button_y + button_height)

        if not self.model.is_clicker_running():
            self.model.start_session()

        self.model.toggle_clicker(
            delay=delay,
            duration=duration,
            fixed_x=fixed_x,
            fixed_y=fixed_y,
            click_type=click_type,
            pattern=pattern,
            pattern_size=pattern_size,
            repeat=repeat,
            random_delay=random_delay,
            click_while_pattern=click_while_pattern,
            notify_when_done=notify_when_done,
            interrupt_on_move=interrupt_on_move,
            button_bounds=button_bounds
        )

    # ============================================
    # === CAPTURE CALLBACKS ===
    # ============================================

    def _on_capture_coordinates(self):
        """Handle capture coordinates button click"""
        self.model.capture_mouse_coordinates()

    def _on_coordinates_received(self, x: int, y: int):
        """Callback when coordinates are captured"""
        self.main_tab.x_entry.delete(0, "end")
        self.main_tab.x_entry.insert(0, str(x))
        self.main_tab.y_entry.delete(0, "end")
        self.main_tab.y_entry.insert(0, str(y))

    # ============================================
    # === STATISTICS CALLBACKS ===
    # ============================================

    def _on_export_stats(self):
        """Handle export statistics button click"""
        from ..logic.stats import ExportResult

        self.model.stop_stats_updater()

        filename = filedialog.asksaveasfilename(
            title="Export Statistics",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")]
        )
        if not filename:
            self.model.start_stats_updater()
            return

        try:
            result, message = self.model.export_statistics(filename)

            if result == ExportResult.SUCCESS:
                self.update_status(events.STATS_EXPORTED, filename=message)
            else:
                print(f"Export failed: {result.value} - {message}")
                self.update_status(events.STATS_EXPORT_ERROR)

        finally:
            self.model.start_stats_updater()

    def _on_reset_stats(self):
        """Handle reset statistics button click"""
        self.model.reset_statistics()
        self.update_status(events.STATS_RESET)

    # ============================================
    # === PROFILE CALLBACKS ===
    # ============================================

    def _on_save_profile(self, profile_name: str):
        """Handle save profile button click"""
        self.profile_handler.save(profile_name)

    def _on_load_profile(self, profile_name: str):
        """Handle load profile selection"""
        self.profile_handler.load(profile_name)

    def _on_delete_profile(self, profile_name: str):
        """Handle delete profile button click"""
        self.profile_handler.delete(profile_name)

    # ============================================
    # === MACRO CALLBACKS ===
    # ============================================

    def _on_record_macro(self):
        """Handle record macro button click (thread-safe)"""
        self.root.after(0, self._record_macro_safe)

    def _record_macro_safe(self):
        """Internal thread-safe macro recording start"""
        self.model.start_macro_recording()

    def _on_stop_macro(self):
        """Handle stop macro recording button click (thread-safe)"""
        self.root.after(0, self._stop_macro_safe)

    def _stop_macro_safe(self):
        """Internal thread-safe macro recording stop"""
        self.model.stop_macro_recording()

    def _on_play_macro(self):
        """Handle play macro button click (thread-safe)"""
        self.root.after(0, self._play_macro_safe)

    def _play_macro_safe(self):
        """Internal thread-safe macro playback"""
        self.model.play_macro_recording()

    # ============================================
    # === STATUS & UI UPDATE METHODS ===
    # ============================================

    def update_status(self, event_code: str, **kwargs):
        """Update status bar and button states (thread-safe)"""
        self.status_handler.handle(event_code, **kwargs)

    # ============================================
    # === THEME CALLBACKS ===
    # ============================================

    def _on_cycle_theme(self):
        """Handle theme cycle button click"""
        try:
            theme_name = self.model.cycle_theme(self.style)
            self.update_status(events.THEME_APPLIED, theme_name=theme_name)
        except Exception as e:
            print(f"[ERROR] Failed to cycle theme: {e}")
            self.update_status(events.THEME_APPLY_ERROR)

    def _on_apply_theme(self, theme_name: str):
        """Handle theme selection from SettingsTab"""
        try:
            success = self.model.apply_theme(self.style, theme_name)
            if success:
                self.update_status(events.THEME_APPLIED, theme_name=theme_name)
            else:
                self.update_status(events.THEME_APPLY_ERROR, theme_name=theme_name)
        except Exception as e:
            print(f"[ERROR] Failed to apply theme '{theme_name}': {e}")
            self.update_status(events.THEME_APPLY_ERROR)

    # ============================================
    # === TRANSLATION/LANGUAGE METHODS ===
    # ============================================

    def refresh_translations(self, lang_code=None):
        """Refresh all UI text elements when language changes"""
        t = self.model.translation_manager.get_text

        try:
            # === Adjust Window Size for Language ===
            self._adjust_window_size_for_language()
            # === Window Title ===
            self.root.title(t("app_title"))

            # === Tab Names ===
            try:
                self.notebook.tab(0, text=f"🎯 {t('main_controls')}")
                self.notebook.tab(1, text=f"🎨 {t('patterns')}")
                self.notebook.tab(2, text=f"📊 {t('statistics')}")
                self.notebook.tab(3, text=f"🔧 {t('settings')}")
            except Exception as e:
                print(f"[WARN] Failed to update tab names: {e}")

            # === Refresh all registered UI components ===
            for component in self._ui_components:
                try:
                    if hasattr(component, 'refresh_translations'):
                        component.refresh_translations()
                except Exception as e:
                    component_name = component.__class__.__name__
                    print(f"[ERROR] Refreshing {component_name} translations: {e}")

        except Exception as e:
            try:
                self.update_status(events.ERROR)
            except Exception as inner_e:
                print(f"[ERROR] Translation refresh failed: {e}")
                print(f"[ERROR] Status update also failed: {inner_e}")

    # ============================================
    # === CLEANUP & MAINLOOP ===
    # ============================================

    def _on_window_close(self):
        """Handle window close and cleanup"""
        try:
            self.model.stop_stats_updater()
        except Exception as e:
            print(f"Error stopping stats updater: {e}")

        try:
            self.model.cleanup_hotkeys()
        except Exception as e:
            print(f"Error cleaning hotkeys: {e}")

        try:
            self.model.stop_clicker()
        except Exception as e:
            print(f"Error stopping clicker: {e}")

        self.root.quit()

    def run(self):
        """Start Tkinter main event loop"""
        self.root.mainloop()
