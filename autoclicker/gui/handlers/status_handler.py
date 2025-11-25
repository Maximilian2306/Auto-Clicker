# autoclicker/gui/handlers/status_handler.py
"""
StatusHandler - Centralized status message handling

Extracts the status update logic from GUIManager for better separation of concerns.
Handles event code translation, UI updates, and toast notifications.
"""

from typing import TYPE_CHECKING, Callable
from ... import events
from .utils import update_button_state

if TYPE_CHECKING:
    from ..gui_manager import GUIManager


class StatusHandler:
    """Handles all status-related updates, translations and UI state changes"""

    def __init__(self, gui_manager: "GUIManager"):
        self.gm = gui_manager

    def _t(self, key: str) -> str:
        """Get translated text via GUIManager's translation service"""
        return self.gm.t(key)

    def handle(self, event_code: str, **kwargs):
        """Handle status update for given event code with optional context kwargs"""
        message = self._get_message(event_code, kwargs)

        # Console output
        print(f"[STATUS] {message}")

        # Show toast notification
        self._show_toast(event_code)

        # Schedule UI update on main thread
        self.gm.root.after(0, lambda: self._update_ui(event_code, message, kwargs))

    def _get_message(self, event_code: str, kwargs: dict) -> str:
        """Get localized message for event code"""
        t = self._t

        def msg(base_key: str, **values):
            """Get translation and append dynamic values"""
            text = t(base_key)
            if values:
                value_str = " ".join(
                    f"'{v}'" if isinstance(v, str) and ' ' not in str(v) else str(v)
                    for v in values.values()
                )
                return f"{text}: {value_str}" if value_str else text
            return text

        messages = {
            # Clicker Events
            events.CLICKER_STARTED: f"[{t('running').upper()}] {t('clicker_started')}",
            events.CLICKER_STOPPED: f"[{t('stopped').upper()}] {t('clicker_stopped')}",
            events.CLICKER_COMPLETED: f"[{t('completed').upper()}] {t('clicker_completed')}",
            events.CLICKER_PAUSED: f"[{t('paused').upper()}] {t('clicker_paused')}",
            events.CLICKER_RESUMED: f"[{t('running').upper()}] {t('clicker_resumed')}",
            events.CLICKER_WAITING: f"[{t('waiting').upper()}] {t('clicker_waiting')}",

            # Capture Events
            events.CAPTURE_READY: f"[{t('ready').upper()}] {t('capture_ready')}",
            events.CAPTURE_LISTENING: f"[{t('listening').upper()}] {t('capture_listening')}",
            events.CAPTURE_SUCCESS: f"[OK] {t('capture_success')} ({kwargs.get('x', 0)}, {kwargs.get('y', 0)})",
            events.CAPTURE_ERROR: f"[ERROR] {t('capture_error')}",

            # Macro Events
            events.MACRO_RECORDING_STARTED: f"[{t('recording').upper()}] {t('macro_recording_started')}",
            events.MACRO_RECORDING_STOPPED: f"[OK] {msg('macro_recording_stopped', count=kwargs.get('count', ''))}",
            events.MACRO_ALREADY_RECORDING: f"[WARN] {t('macro_already_recording')}",
            events.MACRO_NOT_RECORDING: f"[WARN] {t('macro_not_recording')}",
            events.MACRO_SAVED: f"[OK] {msg('macro_saved', name=kwargs.get('name', ''))}",
            events.MACRO_SAVE_ERROR: f"[ERROR] {t('macro_save_error')}",
            events.MACRO_LOADED: f"[OK] {msg('macro_loaded', name=kwargs.get('name', ''), count=kwargs.get('count', ''))}",
            events.MACRO_LOAD_ERROR: f"[ERROR] {t('macro_load_error')}",
            events.MACRO_PLAYING: f"[{t('playing').upper()}] {t('macro_playing')}",
            events.MACRO_PLAY_COMPLETED: f"[OK] {t('macro_play_completed')}",
            events.MACRO_PLAY_ERROR: f"[ERROR] {t('macro_play_error')}",
            events.MACRO_DELETED: f"[OK] {msg('macro_deleted', name=kwargs.get('name', ''))}",
            events.MACRO_DELETE_ERROR: f"[ERROR] {t('macro_delete_error')}",
            events.MACRO_NO_EVENTS: f"[ERROR] {t('macro_no_events')}",
            events.MACRO_INVALID_NAME: f"[ERROR] {t('macro_invalid_name')}",
            events.MACRO_NOT_FOUND: f"[ERROR] {msg('macro_not_found', name=kwargs.get('name', ''))}",
            events.MACRO_LIBS_UNAVAILABLE: f"[ERROR] {t('macro_libs_unavailable')}",

            # Profile Events
            events.PROFILE_SAVED: f"[OK] {msg('profile_saved', profile_name=kwargs.get('profile_name', ''))}",
            events.PROFILE_SAVE_ERROR: f"[ERROR] {t('profile_save_error')}",
            events.PROFILE_LOADED: f"[OK] {msg('profile_loaded', profile_name=kwargs.get('profile_name', ''))}",
            events.PROFILE_LOAD_ERROR: f"[ERROR] {t('profile_load_error')}",
            events.PROFILE_DELETED: f"[OK] {msg('profile_deleted', profile_name=kwargs.get('profile_name', ''))}",
            events.PROFILE_DELETE_ERROR: f"[ERROR] {t('profile_delete_error')}",
            events.PROFILE_NOT_FOUND: f"[ERROR] {msg('profile_not_found', profile_name=kwargs.get('profile_name', ''))}",

            # Theme Events
            events.THEME_APPLIED: f"[OK] {msg('theme_applied', theme_name=kwargs.get('theme_name', ''))}",
            events.THEME_APPLY_ERROR: f"[ERROR] {t('theme_apply_error')}",

            # Hotkey Events
            events.HOTKEY_REGISTERED: f"[OK] {msg('hotkey_registered', key=kwargs.get('key', ''))}",
            events.HOTKEY_REGISTER_ERROR: f"[ERROR] {t('hotkey_register_error')}",
            events.HOTKEY_UNKNOWN: f"[ERROR] {msg('hotkey_unknown', hotkey_name=kwargs.get('hotkey_name', ''))}",
            events.HOTKEY_NO_CALLBACK: f"[ERROR] {msg('hotkey_no_callback', hotkey_name=kwargs.get('hotkey_name', ''))}",

            # Statistics Events
            events.STATS_EXPORTED: f"[OK] {msg('stats_exported', filename=kwargs.get('filename', ''))}",
            events.STATS_EXPORT_ERROR: f"[ERROR] {t('stats_export_error')}",
            events.STATS_RESET: f"[OK] {t('stats_reset')}",

            # General Events
            events.READY: f"[{t('ready').upper()}]",
            events.SUCCESS: f"[OK]",
            events.ERROR: f"[ERROR]",
        }

        return messages.get(event_code, f"[INFO] {event_code}")

    def _show_toast(self, event_code: str):
        """Show toast notification for event"""
        toast_config = {
            events.CLICKER_STARTED: ("toast_clicker_started", "success"),
            events.CLICKER_STOPPED: ("toast_clicker_stopped", "info"),
            events.CLICKER_COMPLETED: ("toast_clicker_completed", "success"),
            events.CLICKER_PAUSED: ("toast_clicker_paused", "warning"),
            events.PROFILE_SAVED: ("toast_profile_saved", "success"),
            events.PROFILE_LOADED: ("toast_profile_loaded", "success"),
            events.PROFILE_DELETED: ("toast_profile_deleted", "info"),
            events.THEME_APPLIED: ("toast_theme_applied", "success"),
            events.HOTKEY_REGISTERED: ("toast_hotkey_registered", "success"),
            events.STATS_EXPORTED: ("toast_stats_exported", "success"),
            events.STATS_RESET: ("toast_stats_reset", "info"),
            events.CAPTURE_SUCCESS: ("toast_capture_success", "success"),
            events.MACRO_RECORDING_STARTED: ("toast_macro_recording_started", "info"),
            events.MACRO_RECORDING_STOPPED: ("toast_macro_recording_stopped", "success"),
            events.MACRO_PLAYING: ("toast_macro_playing", "info"),
            events.MACRO_PLAY_COMPLETED: ("toast_macro_play_completed", "success"),
        }

        if event_code in toast_config:
            toast_key, toast_type = toast_config[event_code]
            toast_message = self._t(toast_key)
            self.gm.root.after(0, lambda msg=toast_message, ttype=toast_type: self.gm.toast.show(msg, ttype))

    def _update_ui(self, event_code: str, message: str, kwargs: dict):
        """Update UI elements based on event code"""
        t = self._t

        # Update status bar
        if hasattr(self.gm, 'status_bar'):
            is_ready = event_code in (events.READY, events.CAPTURE_READY)
            self.gm.status_bar.update_text(message, is_ready=is_ready)

        # Clicker state updates
        if event_code in (events.CLICKER_STARTED, events.CLICKER_RESUMED, events.CLICKER_WAITING):
            self._update_clicker_running(event_code)
        elif event_code == events.CLICKER_PAUSED:
            self._update_clicker_paused()
        elif event_code == events.CLICKER_STOPPED:
            self._update_clicker_stopped()
        elif event_code == events.CLICKER_COMPLETED:
            self._update_clicker_completed()

        # Macro status updates
        elif event_code == events.MACRO_RECORDING_STARTED:
            self.gm.patterns_tab.update_macro_status(message)
        elif event_code == events.MACRO_RECORDING_STOPPED:
            count = kwargs.get('count', 0)
            self.gm.patterns_tab.update_macro_status(f"[OK] {t('macro_recording_stopped')} {count}")
        elif event_code in (events.MACRO_NOT_RECORDING, events.MACRO_ALREADY_RECORDING,
                           events.MACRO_PLAYING, events.MACRO_NO_EVENTS, events.MACRO_PLAY_COMPLETED):
            self.gm.patterns_tab.update_macro_status(message)

    def _update_clicker_running(self, event_code: str):
        """Update UI for running/resumed/waiting state"""
        t = self._t
        update_button_state(
            self.gm.main_tab.start_button,
            bootstyle="danger",
            text_var=self.gm.main_tab.button_text_var,
            text=f"⏸️  {t('stop_clicking').upper()}",
            width=30
        )
        status_emoji = "🟢" if event_code != events.CLICKER_WAITING else "⏳"
        status_text = t('running').upper() if event_code != events.CLICKER_WAITING else t('waiting').upper()
        self.gm.main_tab.status_text_var.set(f"{status_emoji} {status_text}")

    def _update_clicker_paused(self):
        """Update UI for paused state"""
        t = self._t
        update_button_state(
            self.gm.main_tab.start_button,
            bootstyle="warning",
            text_var=self.gm.main_tab.button_text_var,
            text=f"⏸️  {t('stop_clicking').upper()}",
            width=30
        )
        self.gm.main_tab.status_text_var.set(f"⏸️ {t('paused').upper()}")

    def _update_clicker_stopped(self):
        """Update UI for stopped state"""
        t = self._t
        update_button_state(
            self.gm.main_tab.start_button,
            bootstyle="success",
            text_var=self.gm.main_tab.button_text_var,
            text=f"▶️  {t('start_clicking').upper()}",
            width=30,
            style="custom.TButton"
        )
        self.gm.main_tab.status_text_var.set(f"🔴 {t('stopped').upper()}")

    def _update_clicker_completed(self):
        """Update UI for completed state"""
        t = self._t
        update_button_state(
            self.gm.main_tab.start_button,
            bootstyle="success",
            text_var=self.gm.main_tab.button_text_var,
            text=f"▶️  {t('start_clicking').upper()}",
            width=30,
            style="custom.TButton"
        )
        self.gm.main_tab.status_text_var.set(f"✅ {t('completed').upper()}")
