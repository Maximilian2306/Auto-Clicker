# autoclicker/logic/setup_hotkeys.py
"""
Hotkey Setup Logic - Global keyboard shortcuts

This module handles global hotkey registration and management.
It uses event codes to communicate state changes to the Model layer,
keeping the logic layer independent of UI concerns.
"""

from typing import Callable, Dict

try:
    import keyboard
except ImportError:
    keyboard = None

from ..events import (HOTKEY_REGISTERED, HOTKEY_REGISTER_ERROR, HOTKEY_UNKNOWN, HOTKEY_NO_CALLBACK)


class SetupHotkeys:
    """Manages global hotkeys"""

    def __init__(self):
        self.hotkeys: Dict[str, str] = {
            "start_macro_recording": "f3",
            "stop_macro_recording": "f4",
            "play_macro_recording": "f5",
            "toggle_clicker": "f6",
            "capture_coordinates": "f7",
            "exit_program": "esc",
        }
        self.registered_hotkeys: Dict[str, Callable] = {}

    def register_hotkey(
        self,
        name: str,
        key: str,
        callback: Callable[[], None],
        on_status: Callable[[str], None],
    ) -> bool:
        """Register a hotkey"""

        if not keyboard:
            on_status(HOTKEY_REGISTER_ERROR)
            return False

        # key = key.strip().lower()
        original_key = key.strip()        # für UI-Anzeige
        normalized_key = original_key.lower()  # für keyboard

        # === Check if hotkey already in use ===
        if any(existing_key.lower() == normalized_key for n, existing_key in self.hotkeys.items() if n != name):
            on_status(HOTKEY_REGISTER_ERROR)
            return False

        try:
            if name in self.registered_hotkeys:
                self.unregister_hotkey(name)

            try:
                keyboard.remove_hotkey(normalized_key)
            except Exception:
                pass

            keyboard.add_hotkey(normalized_key, callback)
            self.registered_hotkeys[name] = callback
            self.hotkeys[name] = original_key


            return True

        except Exception as e:
            on_status(HOTKEY_REGISTER_ERROR)
            return False

    def unregister_hotkey(self, name: str) -> bool:
        """Unregister a hotkey"""

        if not keyboard:
            return False

        try:
            if name in self.registered_hotkeys:
                key = self.hotkeys.get(name)
                if key:
                    try:
                        keyboard.remove_hotkey(key.lower())  # 🔧 normalize before removing
                    except KeyError:
                        pass
            del self.registered_hotkeys[name]
            return True
        except Exception as e:
            print(f"Error unregistering hotkey: {e}")
            return False
        

    def setup_default_hotkeys(
        self,
        on_toggle_clicker: Callable[[], None],
        on_capture_coordinates: Callable[[], None],
        on_exit_program: Callable[[], None],
        on_record_macro: Callable[[], None],
        on_stop_macro: Callable[[], None],
        on_play_macro: Callable[[], None],
        on_status: Callable[[str], None],
    ) -> bool:
        """Setup all default hotkeys"""

        self.cleanup()

        results = []
        results.append(
            self.register_hotkey("toggle_clicker", self.hotkeys["toggle_clicker"], on_toggle_clicker, on_status)
        )

        results.append(
            self.register_hotkey("capture_coordinates",self.hotkeys["capture_coordinates"], on_capture_coordinates, on_status)
        )

        results.append(
            self.register_hotkey("exit_program", self.hotkeys["exit_program"], on_exit_program, on_status)
        )

        results.append(
            self.register_hotkey("start_macro_recording", self.hotkeys["start_macro_recording"], on_record_macro, on_status)
        )

        results.append(
            self.register_hotkey("stop_macro_recording", self.hotkeys["stop_macro_recording"], on_stop_macro, on_status)
        )

        results.append(
            self.register_hotkey("play_macro_recording", self.hotkeys["play_macro_recording"], on_play_macro, on_status)
        )
        return all(results)
    

    def get_hotkey(self, name: str) -> str:
        """Get hotkey for a specific action"""
        return self.hotkeys.get(name, "")

    def set_hotkey(self, name: str, key: str) -> None:
        """Update hotkey mapping (without registering)"""
        self.hotkeys[name] = key

    def get_all_hotkeys(self) -> Dict[str, str]:
        """Get all hotkey mappings"""
        return self.hotkeys.copy()
        # return {name: key.upper() for name, key in self.hotkeys.items()}

    def cleanup(self):
        """Clean up all registered hotkeys"""
        for name in list(self.registered_hotkeys.keys()):
            self.unregister_hotkey(name)