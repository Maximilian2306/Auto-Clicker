# autoclicker/logic/setup_hotkeys.py
"""Hotkey Setup Logic - Global keyboard shortcuts"""

from typing import Callable, Dict, Union, Optional, TYPE_CHECKING
import sys

try:
    from pynput import keyboard
    HOTKEYS_AVAILABLE = True
except ImportError:
    keyboard = None
    HOTKEYS_AVAILABLE = False

if TYPE_CHECKING:
    from pynput.keyboard import Key, KeyCode

from ..events import (HOTKEY_REGISTERED, HOTKEY_REGISTER_ERROR, HOTKEY_UNKNOWN, HOTKEY_NO_CALLBACK)


class SetupHotkeys:
    """Manages global hotkeys using pynput (cross-platform)"""

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
        self._listener = None
        self._active_combinations = {}

    def _normalize_key(self, key_str: str) -> Optional[Union['Key', 'KeyCode']]:
        """Convert string key to pynput Key or KeyCode"""
        if not HOTKEYS_AVAILABLE:
            return None

        key_lower = key_str.lower().strip()

        # Special keys mapping
        special_keys = {
            'esc': keyboard.Key.esc,
            'escape': keyboard.Key.esc,
            'f1': keyboard.Key.f1,
            'f2': keyboard.Key.f2,
            'f3': keyboard.Key.f3,
            'f4': keyboard.Key.f4,
            'f5': keyboard.Key.f5,
            'f6': keyboard.Key.f6,
            'f7': keyboard.Key.f7,
            'f8': keyboard.Key.f8,
            'f9': keyboard.Key.f9,
            'f10': keyboard.Key.f10,
            'f11': keyboard.Key.f11,
            'f12': keyboard.Key.f12,
            'ctrl': keyboard.Key.ctrl,
            'shift': keyboard.Key.shift,
            'alt': keyboard.Key.alt,
            'cmd': keyboard.Key.cmd,
            'space': keyboard.Key.space,
            'enter': keyboard.Key.enter,
            'tab': keyboard.Key.tab,
        }

        if key_lower in special_keys:
            return special_keys[key_lower]

        # Regular character key
        if len(key_lower) == 1:
            return keyboard.KeyCode.from_char(key_lower)

        return None

    def register_hotkey(
        self,
        name: str,
        key: str,
        callback: Callable[[], None],
        on_status: Callable[[str], None],
    ) -> bool:
        """Register a hotkey"""

        if not HOTKEYS_AVAILABLE:
            on_status(HOTKEY_REGISTER_ERROR)
            return False

        original_key = key.strip()
        normalized_key = original_key.lower()

        # Check if hotkey already in use
        if any(existing_key.lower() == normalized_key for n, existing_key in self.hotkeys.items() if n != name):
            on_status(HOTKEY_REGISTER_ERROR)
            return False

        try:
            # Convert key string to pynput key
            pynput_key = self._normalize_key(normalized_key)
            if pynput_key is None:
                on_status(HOTKEY_REGISTER_ERROR)
                return False

            # Store the hotkey
            self.hotkeys[name] = original_key
            self.registered_hotkeys[name] = callback
            self._active_combinations[pynput_key] = callback

            # Restart listener with updated hotkeys
            self._restart_listener()

            return True

        except Exception as e:
            print(f"Error registering hotkey: {e}")
            on_status(HOTKEY_REGISTER_ERROR)
            return False

    def _restart_listener(self):
        """Restart the keyboard listener with current hotkey mappings"""
        if not HOTKEYS_AVAILABLE:
            return

        # Stop existing listener
        if self._listener is not None:
            self._listener.stop()

        # Create new listener with all registered hotkeys
        def on_press(key):
            # Check if this key has a registered callback
            if key in self._active_combinations:
                try:
                    self._active_combinations[key]()
                except Exception as e:
                    print(f"Error executing hotkey callback: {e}")

        self._listener = keyboard.Listener(on_press=on_press)
        self._listener.start()

    def unregister_hotkey(self, name: str) -> bool:
        """Unregister a hotkey"""

        if not HOTKEYS_AVAILABLE:
            return False

        try:
            if name in self.registered_hotkeys:
                key_str = self.hotkeys.get(name)
                if key_str:
                    pynput_key = self._normalize_key(key_str)
                    if pynput_key in self._active_combinations:
                        del self._active_combinations[pynput_key]

                del self.registered_hotkeys[name]

                # Restart listener
                self._restart_listener()

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

    def cleanup(self):
        """Clean up all registered hotkeys"""
        for name in list(self.registered_hotkeys.keys()):
            self.unregister_hotkey(name)

        # Stop listener
        if self._listener is not None:
            self._listener.stop()
            self._listener = None
