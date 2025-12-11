# autoclicker/logic/capture_coordinates.py
"""Coordinate Capture Logic - Capture mouse position on click"""

import threading
from typing import Callable, Optional

try:
    from pynput import mouse
    MOUSE_AVAILABLE = True
except ImportError:
    mouse = None
    MOUSE_AVAILABLE = False

from ..events import (CAPTURE_READY, CAPTURE_LISTENING, CAPTURE_SUCCESS, CAPTURE_ERROR)


class CaptureCoordinates:
    """Manages coordinates using pynput (cross-platform)"""

    def __init__(self):
        self.listening = False
        self._listener = None

    def capture_mouse_position(
        self,
        on_captured: Callable[[int, int], None],
        on_status: Callable[[str], None],
    ):
        """Listen for next click and capture coordinates"""
        if not MOUSE_AVAILABLE:
            on_status(CAPTURE_ERROR)
            return

        if self.listening:
            on_status(CAPTURE_READY)
            return

        self.listening = True
        on_status(CAPTURE_LISTENING)

        def on_click(x, y, button, pressed):
            if pressed:  # Only on mouse down
                on_captured(x, y)
                self.listening = False
                if self._listener:
                    self._listener.stop()
                return False  # Stop listener

        self._listener = mouse.Listener(on_click=on_click)
        self._listener.start()

    def get_current_position(self) -> tuple[int, int]:
        """Get current mouse position"""
        try:
            import pyautogui
            return pyautogui.position()
        except Exception as e:
            print(f"Error getting mouse position: {e}")
            return (0, 0)
