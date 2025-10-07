import pyautogui
import time
import math
from collections.abc import Callable
from threading import Event
from typing import Optional

pyautogui.FAILSAFE = True  # Failsafe activated (left upper corner)
pyautogui.PAUSE = 0        # No pause between actions

button_area: Optional[tuple[int, int, int, int]] = None  


def auto_clicker(
    delay: float,
    duration: float,
    follow_8: bool,
    fixed_x: Optional[int],
    fixed_y: Optional[int],
    click_type: str,
    update_status_callback: Callable[[str, str], None],
    stop_event: Event,
) -> None:
    global button_area
    start_time = time.time()

    # if mouse is in button area, wait until it leaves
    if button_area:
        update_status_callback("Waiting on mouse movement...", "orange")
        while not stop_event.is_set():
            x, y = pyautogui.position()
            if not (button_area[0] <= x <= button_area[2] and button_area[1] <= y <= button_area[3]):
                break
            time.sleep(0.05)

    # Click Loop
    while not stop_event.is_set():
        if fixed_x is not None and fixed_y is not None:
            pyautogui.moveTo(fixed_x, fixed_y)

        if follow_8:
            move_mouse_in_8_pattern()

        pyautogui.click(button=click_type)

        if delay > 0:
            time.sleep(delay)

        if duration > 0 and (time.time() - start_time) >= duration:
            stop_event.set()
            update_status_callback("STOP", "red")
            break


def move_mouse_in_8_pattern():
    center_x, center_y = pyautogui.size()
    center_x //= 2
    center_y //= 2
    radius = 100
    t = time.time()
    x = center_x + int(radius * math.sin(t) / (1 + math.cos(t) ** 2))
    y = center_y + int(radius * math.sin(t) * math.cos(t) / (1 + math.cos(t) ** 2))
    pyautogui.moveTo(x, y)


