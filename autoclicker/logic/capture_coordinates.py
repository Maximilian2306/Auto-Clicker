# autoclicker/logic/capture_coordinates.py
"""
Coordinate Capture Logic - Capture mouse coordinates on click

This module handles coordinate capturing functionality.
It uses event codes to communicate state changes to the Model layer,
keeping the logic layer independent of UI concerns.
"""

import threading
from typing import Callable, Optional

try:
    import mouse
except ImportError:
    mouse = None

from ..events import (CAPTURE_READY, CAPTURE_LISTENING, CAPTURE_SUCCESS, CAPTURE_ERROR)


class CaptureCoordinates:
    """Manages coordinates"""

    def __init__(self):
        self.listening = False

    def capture_mouse_position(
        self,
        on_captured: Callable[[int, int], None],
        on_status: Callable[[str], None],
    ):
        """Listen for next mouse click and capture coordinates"""

        if not mouse:
            on_status(CAPTURE_ERROR)
            return

        if self.listening:
            on_status(CAPTURE_READY)
            return

        self.listening = True
        on_status(CAPTURE_LISTENING)

        def wait_for_click():
            """Run in separate thread"""

            def on_click(event):
                if isinstance(event, mouse.ButtonEvent) and event.event_type == "down":  # Only on mouse down
                    x, y = mouse.get_position()
                    on_captured(x, y)
                    # on_status(CAPTURE_SUCCESS)
                    mouse.unhook(on_click)
                    self.listening = False

            mouse.hook(on_click)

        thread = threading.Thread(target=wait_for_click, daemon=True)
        thread.start()

    def get_current_position(self) -> tuple[int, int]:
        """Get current mouse position"""
        try:
            import pyautogui
            return pyautogui.position()
        except Exception as e:
            print(f"Error getting mouse position: {e}")