# autoclicker/logic/macro_recording.py
"""Macro Recording Logic - Record and playback mouse/keyboard actions"""

import threading
import time
import json
from typing import Callable, Optional, List, Dict, Any
from pathlib import Path
from datetime import datetime

try:
    from pynput import mouse, keyboard
    MACRO_LIBS_AVAILABLE = True
except ImportError:
    mouse = None
    keyboard = None
    MACRO_LIBS_AVAILABLE = False

from ..events import (MACRO_RECORDING_STARTED, MACRO_RECORDING_STOPPED, MACRO_ALREADY_RECORDING, MACRO_NOT_RECORDING, MACRO_SAVED, MACRO_SAVE_ERROR, MACRO_LOADED, MACRO_LOAD_ERROR, MACRO_PLAYING, MACRO_PLAY_COMPLETED, MACRO_PLAY_ERROR, MACRO_DELETED, MACRO_DELETE_ERROR, MACRO_NO_EVENTS, MACRO_INVALID_NAME, MACRO_NOT_FOUND, MACRO_LIBS_UNAVAILABLE)
from ..utils.validators import validate_macro_name
from ..utils.constants import MACROS_DIR

class MacroRecording:
    """Manages macro recording and playback using pynput (cross-platform)"""

    def __init__(self, hotkeys: dict[str, str] = None):
        self.recording = False
        self._recording_lock = threading.Lock()
        self.macro_events: List[Dict[str, Any]] = []
        self._events_lock = threading.Lock()
        self.recording_start_time = None
        self.recorded_macro_name = None
        self.hotkeys = hotkeys or {
            "start_macro_recording": "f3",
            "stop_macro_recording": "f4",
            "play_macro_recording": "f5",
        }
        self._mouse_listener = None
        self._keyboard_listener = None

    def _validate_macro_name(self, name: str) -> bool:
        """Validate macro name to prevent path traversal"""
        return validate_macro_name(name)

    def update_hotkeys(self, hotkeys: dict[str, str]) -> None:
        """Update hotkey bindings (registration handled by SetupHotkeys)"""
        self.hotkeys.update(hotkeys)

    def start_recording(self, on_status: Callable[[str], None]) -> bool:
        """Start recording mouse and keyboard events"""
        if not MACRO_LIBS_AVAILABLE:
            on_status(MACRO_LIBS_UNAVAILABLE)
            return False

        with self._recording_lock:
            if self.recording:
                on_status(MACRO_ALREADY_RECORDING)
                return False
            self.recording = True

        with self._events_lock:
            self.macro_events = []

        self.recording_start_time = time.time()
        on_status(MACRO_RECORDING_STARTED)

        # Mouse event handlers
        def on_move(x, y):
            with self._recording_lock:
                if not self.recording:
                    return False
            with self._events_lock:
                self.macro_events.append({
                    "type": "mouse_move",
                    "x": x,
                    "y": y,
                    "timestamp": time.time() - self.recording_start_time,
                })

        def on_click(x, y, button, pressed):
            with self._recording_lock:
                if not self.recording:
                    return False
            with self._events_lock:
                self.macro_events.append({
                    "type": "mouse_click",
                    "button": button.name if hasattr(button, 'name') else str(button),
                    "action": "down" if pressed else "up",
                    "timestamp": time.time() - self.recording_start_time,
                })

        def on_scroll(x, y, dx, dy):
            with self._recording_lock:
                if not self.recording:
                    return False
            with self._events_lock:
                self.macro_events.append({
                    "type": "mouse_wheel",
                    "delta": dy,  # Vertical scroll
                    "timestamp": time.time() - self.recording_start_time,
                })

        # Keyboard event handlers
        def on_press(key):
            with self._recording_lock:
                if not self.recording:
                    return False
            try:
                key_name = key.char if hasattr(key, 'char') else key.name
            except AttributeError:
                key_name = str(key)

            with self._events_lock:
                self.macro_events.append({
                    "type": "key_event",
                    "key": key_name,
                    "action": "down",
                    "timestamp": time.time() - self.recording_start_time,
                })

        def on_release(key):
            with self._recording_lock:
                if not self.recording:
                    return False
            try:
                key_name = key.char if hasattr(key, 'char') else key.name
            except AttributeError:
                key_name = str(key)

            with self._events_lock:
                self.macro_events.append({
                    "type": "key_event",
                    "key": key_name,
                    "action": "up",
                    "timestamp": time.time() - self.recording_start_time,
                })

        # Start listeners
        self._mouse_listener = mouse.Listener(
            on_move=on_move,
            on_click=on_click,
            on_scroll=on_scroll
        )
        self._keyboard_listener = keyboard.Listener(
            on_press=on_press,
            on_release=on_release
        )

        self._mouse_listener.start()
        self._keyboard_listener.start()

        return True

    def stop_recording(self, on_status: Callable[[str], None]) -> bool:
        """Stop recording and finalize macro event list"""
        with self._recording_lock:
            if not self.recording:
                on_status(MACRO_NOT_RECORDING)
                return False
            self.recording = False

        # Stop listeners
        if self._mouse_listener:
            self._mouse_listener.stop()
            self._mouse_listener = None

        if self._keyboard_listener:
            self._keyboard_listener.stop()
            self._keyboard_listener = None

        on_status(MACRO_RECORDING_STOPPED, count=len(self.macro_events))
        return True

    def save_macro(self, name: str, on_status: Callable[[str], None]) -> bool:
        """Save recorded macro to JSON file"""
        if not self._validate_macro_name(name):
            on_status(MACRO_INVALID_NAME)
            return False

        if not self.macro_events:
            on_status(MACRO_NO_EVENTS)
            return False

        try:
            MACROS_DIR.mkdir(exist_ok=True)
            filename = MACROS_DIR / f"{name}.json"

            # SECURITY: Verify path is within MACROS_DIR (symlink-safe)
            try:
                filename_resolved = filename.resolve()
                macro_dir_resolved = MACROS_DIR.resolve()
                filename_resolved.relative_to(macro_dir_resolved)
            except (ValueError, OSError):
                on_status(MACRO_SAVE_ERROR)
                return False

            macro_data = {
                "name": name,
                "created": datetime.now().isoformat(),
                "events": self.macro_events,
                "event_count": len(self.macro_events),
            }

            with open(filename, "w") as f:
                json.dump(macro_data, f, indent=2)

            self.recorded_macro_name = name
            on_status(MACRO_SAVED, name=name)
            return True

        except Exception as e:
            print(f"[ERROR] Failed to save macro: {e}")
            on_status(MACRO_SAVE_ERROR)
            return False


    def load_macro(self, name: str, on_status: Callable[[str], None]) -> bool:
        """Load macro from JSON file"""
        if not self._validate_macro_name(name):
            on_status(MACRO_INVALID_NAME)
            return False

        try:
            filename = MACROS_DIR / f"{name}.json"

            # SECURITY: Verify path is within MACROS_DIR (symlink-safe)
            try:
                filename_resolved = filename.resolve()
                macro_dir_resolved = MACROS_DIR.resolve()
                filename_resolved.relative_to(macro_dir_resolved)
            except (ValueError, OSError):
                on_status(MACRO_LOAD_ERROR)
                return False

            if not filename.exists():
                on_status(MACRO_NOT_FOUND, name=name)
                return False

            with open(filename, "r") as f:
                macro_data = json.load(f)

            self.macro_events = macro_data.get("events", [])
            self.recorded_macro_name = name
            on_status(MACRO_LOADED, name=name, count=len(self.macro_events))
            return True

        except Exception:
            on_status(MACRO_LOAD_ERROR)
            return False

    def play_macro(self, on_status: Callable[[str], None]) -> bool:
        """Playback recorded macro with timing preservation"""
        if not self.macro_events:
            on_status(MACRO_NO_EVENTS)
            return False

        if not MACRO_LIBS_AVAILABLE:
            on_status(MACRO_LIBS_UNAVAILABLE)
            return False

        on_status(MACRO_PLAYING)

        def playback():
            mouse_controller = mouse.Controller()
            keyboard_controller = keyboard.Controller()

            for i, event in enumerate(self.macro_events):
                event_type = event.get("type")

                try:
                    if event_type == "mouse_move":
                        mouse_controller.position = (event["x"], event["y"])

                    elif event_type == "mouse_click":
                        button_name = event.get("button", "left")
                        # Convert button string to pynput Button
                        if button_name == "left":
                            button = mouse.Button.left
                        elif button_name == "right":
                            button = mouse.Button.right
                        elif button_name == "middle":
                            button = mouse.Button.middle
                        else:
                            button = mouse.Button.left

                        action = event.get("action", "down")
                        if action == "down":
                            mouse_controller.press(button)
                        elif action == "up":
                            mouse_controller.release(button)

                    elif event_type == "mouse_wheel":
                        delta = event.get("delta", 0)
                        mouse_controller.scroll(0, delta)

                    elif event_type == "key_event":
                        key_name = event.get("key")
                        action = event.get("action")

                        # Try to convert key name to pynput key
                        try:
                            # Check if it's a special key
                            if hasattr(keyboard.Key, key_name):
                                key = getattr(keyboard.Key, key_name)
                            else:
                                # Regular character
                                key = key_name
                        except:
                            key = key_name

                        if action == "down":
                            keyboard_controller.press(key)
                        elif action == "up":
                            keyboard_controller.release(key)

                except Exception as e:
                    print(f"Error playing event: {e}")
                    continue

                # Wait for next event
                if i < len(self.macro_events) - 1:
                    current_ts = event["timestamp"]
                    next_ts = self.macro_events[i + 1]["timestamp"]
                    delay = 1.1 * (next_ts - current_ts)
                    if delay > 0:
                        time.sleep(delay)

            on_status(MACRO_PLAY_COMPLETED)

        thread = threading.Thread(target=playback, daemon=True)
        thread.start()

        return True

    def delete_macro(self, name: str, on_status: Callable[[str], None]) -> bool:
        """Delete saved macro file"""
        if not self._validate_macro_name(name):
            on_status(MACRO_INVALID_NAME)
            return False

        try:
            filename = MACROS_DIR / f"{name}.json"

            # SECURITY: Verify path is within MACROS_DIR (symlink-safe)
            try:
                filename_resolved = filename.resolve()
                macro_dir_resolved = MACROS_DIR.resolve()
                filename_resolved.relative_to(macro_dir_resolved)
            except (ValueError, OSError):
                on_status(MACRO_DELETE_ERROR)
                return False

            if filename.exists():
                filename.unlink()
                if name == self.recorded_macro_name:
                    self.recorded_macro_name = None
                on_status(MACRO_DELETED, name=name)
                return True
            else:
                on_status(MACRO_NOT_FOUND, name=name)
                return False

        except Exception:
            on_status(MACRO_DELETE_ERROR)
            return False

    def get_saved_macros(self) -> List[str]:
        """Get list of all saved macro names"""
        try:
            if MACROS_DIR.exists():
                return [f.stem for f in MACROS_DIR.glob("*.json")]
            return []
        except Exception as e:
            print(f"Error getting macros: {e}")
            return []

    def get_macro_info(self, name: str) -> Optional[Dict[str, Any]]:
        """Get metadata about a saved macro"""
        try:
            filename = MACROS_DIR / f"{name}.json"
            if filename.exists():
                with open(filename, "r") as f:
                    return json.load(f)
            return None
        except Exception as e:
            print(f"Error getting macro info: {e}")
            return None
