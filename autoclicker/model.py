# autoclicker/model.py
"""ApplicationModel - Central MVC Controller (Facade Pattern)"""

from typing import Callable, Optional
from tkinter import StringVar, IntVar, BooleanVar
from autoclicker.logic import (Clicker, CaptureCoordinates, Stats, Profiles, SetupHotkeys, MacroRecording)
from autoclicker.utils import (ThemeManager, NotificationManager, TranslationManager)
from autoclicker.utils.constants import (LANGUAGE_CODES, LANGUAGE_DISPLAY_NAMES, HOTKEY_DISPLAY_TO_INTERNAL)
from autoclicker.utils.validators import validate_hotkey


class ApplicationModel:
    """Central MVC Controller implementing Facade and Mediator patterns"""

    def __init__(self):
        # === Tkinter Variables (lazy init after Window creation) ===
        self.total_clicks = None
        self.session_time = None
        self.click_rate = None
        self.language = None
        self.current_profile = None

        # === GUI Callbacks ===
        self.on_status_changed = None
        self.on_progress_changed = None
        self.on_coordinates_captured = None
        self.on_language_update = None
        self.on_macro_status_update = None
        self._notify_callback = None

        # === Hotkey Callback Registry ===
        self._hotkey_callbacks: dict[str, Callable[[], None]] = {}

        # === Logic Components ===
        self.clicker = Clicker()
        self.capture = CaptureCoordinates()
        self.stats = Stats()
        self.profiles = Profiles()
        self.hotkeys = SetupHotkeys()
        self.macro = MacroRecording(hotkeys=self.hotkeys.get_all_hotkeys())

        # === Utility Components ===
        self.theme_manager = ThemeManager()
        self.notification_manager = None
        self.translation_manager = TranslationManager()


    def initialize_variables(self, root=None):
        """Initialize Tkinter variables after Window creation"""
        self.total_clicks = IntVar(value=0)
        self.session_time = StringVar(value="00:00:00")
        self.click_rate = StringVar(value="0 clicks/s")
        self.language = StringVar(value=self._lang_code_to_name(self.translation_manager.get_current_language()))
        self.language.trace_add("write", self._on_language_changed)
        self.current_profile = StringVar(value="Default")
        self.notify_when_done_var = BooleanVar(value=False)

        if root:
            self.notification_manager = NotificationManager(
                root,
                get_text=self.translation_manager.get_text
            )

    # ============================================
    # === TRANSLATION SERVICE ===
    # ============================================

    def t(self, key: str) -> str:
        """Get translated text for key"""
        return self.translation_manager.get_text(key)

    # ============================================
    # === HOTKEY METHODS ===
    # ============================================

    def register_hotkey_callbacks(
        self,
        toggle_clicker: Callable[[], None],
        capture_coordinates: Callable[[], None],
        exit_program: Callable[[], None],
        start_macro_recording: Callable[[], None],
        stop_macro_recording: Callable[[], None],
        play_macro_recording: Callable[[], None],
    ):
        """Register all hotkey callbacks in central registry"""
        self._hotkey_callbacks = {
            "toggle_clicker": toggle_clicker,
            "capture_coordinates": capture_coordinates,
            "exit_program": exit_program,
            "start_macro_recording": start_macro_recording,
            "stop_macro_recording": stop_macro_recording,
            "play_macro_recording": play_macro_recording,
        }

    def get_hotkey_callback(self, internal_name: str) -> Optional[Callable[[], None]]:
        """Get callback function for hotkey by internal name"""
        return self._hotkey_callbacks.get(internal_name)

    def setup_default_hotkeys(
        self,
        on_toggle: Callable[[], None],
        on_capture: Callable[[], None],
        on_exit: Callable[[], None],
        on_record: Callable[[], None],
        on_stop: Callable[[], None],
        on_play: Callable[[], None],
    ) -> bool:
        """Setup all default hotkeys"""
        self.hotkeys.cleanup()
        return self.hotkeys.setup_default_hotkeys(
            on_toggle_clicker=on_toggle,
            on_capture_coordinates=on_capture,
            on_exit_program=on_exit,
            on_record_macro=on_record,
            on_stop_macro=on_stop,
            on_play_macro=on_play,
            on_status=self._on_hotkey_status,
        )

    def register_hotkey(self, name: str, key: str, callback: Callable[[], None]) -> bool:
        """Register a custom hotkey"""
        return self.hotkeys.register_hotkey(
            name=name,
            key=key,
            callback=callback,
            on_status=self._on_hotkey_status,
        )

    def update_hotkey(self, display_name: str, key: str) -> bool:
        """Update hotkey by display name"""
        internal_name = HOTKEY_DISPLAY_TO_INTERNAL.get(display_name)
        if not internal_name:
            from .events import HOTKEY_UNKNOWN
            self._on_hotkey_status(HOTKEY_UNKNOWN, hotkey_name=display_name)
            return False

        original_key = key.strip()

        # Validate hotkey
        is_valid, error = validate_hotkey(original_key)
        if not is_valid:
            from .events import HOTKEY_REGISTER_ERROR
            self._on_hotkey_status(HOTKEY_REGISTER_ERROR, error=error)
            return False

        callback = self.get_hotkey_callback(internal_name)
        if callback is None:
            from .events import HOTKEY_NO_CALLBACK
            self._on_hotkey_status(HOTKEY_NO_CALLBACK, hotkey_name=display_name)
            return False

        return self.hotkeys.register_hotkey(
            internal_name,
            original_key,
            callback,
            self._on_hotkey_status,
        )

    def cleanup_hotkeys(self):
        """Cleanup and unregister all hotkeys (called on exit)"""
        self.hotkeys.cleanup()

    def _on_hotkey_status(self, status_text: str, **kwargs):
        """Internal callback handler for hotkey status updates"""
        if self.on_status_changed:
            self.on_status_changed(status_text, **kwargs)

    # ============================================
    # === CLICKER METHODS ===
    # ============================================

    def set_notify_callback(self, callback: Callable[[str], None]):
        """Register callback for showing notifications"""
        self._notify_callback = callback

    def toggle_clicker(
        self,
        delay: float,
        duration: int,
        fixed_x: int,
        fixed_y: int,
        click_type: str,
        pattern: str,
        pattern_size: int,
        repeat: int,
        random_delay: bool,
        click_while_pattern: bool = False,
        notify_when_done: bool = False,
        interrupt_on_move: bool = False,
        button_bounds: tuple[int,int,int,int] = None
    ):
        """Start or stop the auto-clicker"""
        self.clicker.toggle_clicker(
            delay=delay,
            duration=duration,
            fixed_x=fixed_x if fixed_x else None,
            fixed_y=fixed_y if fixed_y else None,
            click_type=click_type,
            pattern=pattern,
            pattern_size=pattern_size,
            repeat=repeat,
            random_delay=random_delay,
            on_status_changed=self._on_clicker_status,
            on_stats_updated=self._on_stats_updated,
            click_while_pattern=click_while_pattern,
            notify_when_done=notify_when_done,
            notify_callback=self._notify_callback,
            interrupt_on_move=interrupt_on_move,
            button_bounds=button_bounds,
        )

    def stop_clicker(self):
        """Stop the auto-clicker immediately"""
        self.clicker.stop()

    def is_clicker_running(self) -> bool:
        """Check if clicker is currently active"""
        return not self.clicker.stop_event.is_set()

    def _on_clicker_status(self, status_text: str, **kwargs):
        """Internal callback handler for clicker status updates"""
        if self.on_status_changed:
            self.on_status_changed(status_text, **kwargs)

    def _on_stats_updated(self, total_clicks: int, click_rate: float):
        """Internal callback handler for stats updates from clicker"""
        if self.total_clicks:
            self.total_clicks.set(total_clicks)
        if self.click_rate:
            self.click_rate.set(f"{click_rate:.1f} clicks/s")

    # ============================================
    # === COORDINATE CAPTURE METHODS ===
    # ============================================

    def capture_mouse_coordinates(self):
        """Start coordinate capture process"""
        self.capture.capture_mouse_position(
            on_captured=self._on_coordinates_captured,
            on_status=self._on_capture_status,
        )

    def set_coordinates_callback(self, callback):
        """Register callback for coordinate capture"""
        self.on_coordinates_captured = callback

    def _on_coordinates_captured(self, x: int, y: int):
        """Internal handler when coordinates are captured"""
        if self.on_coordinates_captured:
            self.on_coordinates_captured(x, y)
        from .events import CAPTURE_SUCCESS
        if self.on_status_changed:
            self.on_status_changed(CAPTURE_SUCCESS, x=x, y=y)

    def _on_capture_status(self, status_text: str, **kwargs):
        """Internal callback handler for capture status updates"""
        if self.on_status_changed:
            self.on_status_changed(status_text, **kwargs)

    # ============================================
    # === STATISTICS METHODS ===
    # ============================================

    def start_session(self):
        """Start a new statistics session and reset all counters"""
        self.stats.start_session()
        if self.total_clicks:
            self.total_clicks.set(0)
        if self.session_time:
            self.session_time.set("00:00:00")
        if self.click_rate:
            self.click_rate.set("0 clicks/s")

    def start_stats_updater(self):
        """Start background thread for continuous statistics updates"""
        self.stats.start_background_updater(
            total_clicks_getter=lambda: self.total_clicks.get() if self.total_clicks else 0,
            on_stats_changed=self._on_stats_display_changed,
        )

    def stop_stats_updater(self):
        """Stop background statistics updater thread"""
        self.stats.stop_background_updater()

    def reset_statistics(self):
        """Reset all statistics counters to zero"""
        self.stats.reset_stats()
        if self.total_clicks:
            self.total_clicks.set(0)
        if self.session_time:
            self.session_time.set("00:00:00")
        if self.click_rate:
            self.click_rate.set("0 clicks/s")

    def export_statistics(self, filename: str):
        """Export current statistics to file"""
        return self.stats.export_stats(
            filename=filename,
            total_clicks=self.total_clicks.get() if self.total_clicks else 0,
            session_time_str=self.session_time.get() if self.session_time else "00:00:00",
            click_rate_str=self.click_rate.get() if self.click_rate else "0 clicks/s",
            profile_name=self.current_profile.get() if self.current_profile else "Default",
        )

    def _on_stats_display_changed(
        self, session_time_str: str, click_rate_str: str, progress_str: str
    ):
        """Internal callback handler for statistics display updates"""
        if self.session_time:
            self.session_time.set(session_time_str)
        if self.click_rate:
            self.click_rate.set(click_rate_str)

        if hasattr(self, "on_progress_changed") and self.on_progress_changed:
            try:
                rate_value = float(click_rate_str.split()[0])
                progress_value = min(rate_value / 1000 * 100, 100)
                text = f"{rate_value:.1f} clicks/s"
            except Exception:
                progress_value = 0
                text = "0 clicks/s"

            self.on_progress_changed(progress_value, text)

    # ============================================
    # === PROFILE METHODS ===
    # ============================================

    def get_profile_list(self) -> list[str]:
        """Get list of all available profiles"""
        return self.profiles.get_all_profiles()

    def set_current_profile(self, name: str):
        """Update current profile name"""
        if self.current_profile:
            self.current_profile.set(name)

    def load_profile(self, name: str) -> dict:
        """Load profile and return its settings"""
        profile = self.profiles.load_profile(name) or self.profiles.get_default_profile()
        if profile:
            self.current_profile.set(name)
            self.profiles.save_last_profile(name)
            self.macro.update_hotkeys(self.hotkeys.get_all_hotkeys())
        return profile

    def save_profile(self, name: str, settings: dict) -> bool:
        """Save current settings as a profile"""
        success = self.profiles.create_profile(name, settings)
        if success:
            self.profiles.save_last_profile(name)
        return success

    def delete_profile(self, name: str) -> bool:
        """Delete a profile"""
        return self.profiles.delete_profile(name)

    def import_profiles(self, filename: str) -> bool:
        """Import profiles from file"""
        return self.profiles.import_profiles(filename)

    def export_profiles(self, filename: str) -> bool:
        """Export profiles to file"""
        return self.profiles.export_profiles(filename)

    # ============================================
    # === MACRO METHODS ===
    # ============================================

    def start_macro_recording(self) -> bool:
        """Start recording a macro"""
        return self.macro.start_recording(on_status=self._on_macro_status)

    def stop_macro_recording(self) -> bool:
        """Stop recording the current macro"""
        return self.macro.stop_recording(on_status=self._on_macro_status)

    def save_macro(self, name: str) -> bool:
        """Save recorded macro to file"""
        return self.macro.save_macro(name, on_status=self._on_macro_status)

    def load_macro(self, name: str) -> bool:
        """Load macro from file"""
        return self.macro.load_macro(name, on_status=self._on_macro_status)

    def play_macro_recording(self) -> bool:
        """Play the loaded macro"""
        return self.macro.play_macro(on_status=self._on_macro_status)

    def delete_macro(self, name: str) -> bool:
        """Delete saved macro file"""
        return self.macro.delete_macro(name, on_status=self._on_macro_status)

    def get_saved_macros(self) -> list[str]:
        """Get list of all saved macros"""
        return self.macro.get_saved_macros()

    def _on_macro_status(self, status_text: str, **kwargs):
        """Internal callback handler for macro status updates"""
        if self.on_status_changed:
            self.on_status_changed(status_text, **kwargs)

    # ============================================
    # === UTILITY METHODS ===
    # ============================================

    def set_status_callback(self, callback: Callable[[str], None]):
        """Register callback for status updates"""
        self.on_status_changed = callback

    def get_current_settings(self) -> dict:
        """Get current application settings snapshot"""
        return {
            "language": self.language.get() if self.language else "en",
            "current_profile": self.current_profile.get() if self.current_profile else "Default",
            "total_clicks": self.total_clicks.get() if self.total_clicks else 0,
        }

    # ============================================
    # === THEME METHODS ===
    # ============================================

    def cycle_theme(self, style_object):
        """Cycle to next theme"""
        theme_name = self.theme_manager.cycle_theme(
            style_object=style_object,
            on_theme_applied=self.on_theme_applied
        )
        return theme_name

    def apply_theme(self, style_object, theme_name: str) -> bool:
        """Apply specific theme by name"""
        return self.theme_manager.apply_theme(
            style_object,
            theme_name,
            on_theme_applied=self.on_theme_applied
        )

    def on_theme_applied(self, theme_name: str):
        """Internal handler when theme is applied"""
        if isinstance(theme_name, str) and theme_name.startswith("Error"):
            return

        self.current_theme = theme_name

    # ============================================
    # === TRANSLATION/LANGUAGE METHODS ===
    # ============================================

    def _on_language_changed(self, *args):
        """Internal handler when language changes"""
        lang_name = self.language.get()
        lang_code = self._lang_name_to_code(lang_name)
        if self.translation_manager.set_language(lang_code):
            try:
                print(f"[OK] Language changed to: {lang_name} ({lang_code})")
            except UnicodeEncodeError:
                print(f"[OK] Language changed to: {lang_name} ({lang_code})".encode('ascii', 'ignore').decode())
            if callable(self.on_language_update):
                try:
                    self.on_language_update(lang_code)
                except Exception as e:
                    print(f"[WARN] Language update callback failed: {e}")
        else:
            try:
                print(f"[WARN] Language {lang_name} not supported")
            except UnicodeEncodeError:
                print(f"[WARN] Language {lang_name} not supported".encode('ascii', 'ignore').decode())

    def _lang_name_to_code(self, name: str) -> str:
        """Convert display name to ISO code"""
        return LANGUAGE_CODES.get(name, "en")

    def _lang_code_to_name(self, code: str) -> str:
        """Convert ISO code to display name"""
        return LANGUAGE_DISPLAY_NAMES.get(code, "English")
