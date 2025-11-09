# autoclicker/logic/setup_hotkeys.py
"""
Hotkey Setup Logic - Global keyboard shortcuts

"""

from typing import Callable, Dict

try:
    import keyboard
except ImportError:
    keyboard = None


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
            on_status("❌ Keyboard library not available")
            return False
        
        key = key.strip().lower()
        
        # === Check if hotkey already in use ===
        if any(existing_key == key for n, existing_key in self.hotkeys.items() if n != name):
            on_status(f"⚠️  Hotkey [{key.upper()}] wird bereits verwendet!")
            return False

        try:
            if name in self.registered_hotkeys:
                self.unregister_hotkey(name)

            try:
                keyboard.remove_hotkey(key)
            except Exception:
                pass

            keyboard.add_hotkey(key, callback)
            self.registered_hotkeys[name] = callback
            self.hotkeys[name] = key


            return True

        except Exception as e:
            on_status(f"❌ Error setting hotkey: {e}")
            return False

    def unregister_hotkey(self, name: str) -> bool:
        """Unregister a hotkey"""

        if not keyboard:
            return False

        try:
            if name in self.registered_hotkeys:
                key = self.hotkeys.get(name)
                if key:
                    keyboard.remove_hotkey(key)
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