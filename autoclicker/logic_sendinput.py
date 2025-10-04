# import time
# import math
# import ctypes
# from collections.abc import Callable
# from threading import Event
# from typing import Optional
# import pyautogui 

# button_area: Optional[tuple[int, int, int, int]] = None  

# # WinAPI Konstanten
# INPUT_MOUSE = 0
# MOUSEEVENTF_MOVE = 0x0001
# MOUSEEVENTF_ABSOLUTE = 0x8000
# MOUSEEVENTF_LEFTDOWN = 0x0002
# MOUSEEVENTF_LEFTUP = 0x0004
# MOUSEEVENTF_RIGHTDOWN = 0x0008
# MOUSEEVENTF_RIGHTUP = 0x0010

# SendInput = ctypes.windll.user32.SendInput

# class MOUSEINPUT(ctypes.Structure):
#     _fields_ = [
#         ("dx", ctypes.c_long),
#         ("dy", ctypes.c_long),
#         ("mouseData", ctypes.c_ulong),
#         ("dwFlags", ctypes.c_ulong),
#         ("time", ctypes.c_ulong),
#         ("dwExtraInfo", ctypes.c_ulonglong)
#     ]

# class INPUT(ctypes.Structure):
#     class _INPUT(ctypes.Union):
#         _fields_ = [("mi", MOUSEINPUT)]
#     _anonymous_ = ("_input",)
#     _fields_ = [("type", ctypes.c_ulong), ("_input", _INPUT)]

# def click_mouse(button="left"):
#     """Direkter Klick mit WinAPI SendInput"""
#     inp = INPUT()
#     inp.type = INPUT_MOUSE
#     if button == "left":
#         inp.mi.dwFlags = MOUSEEVENTF_LEFTDOWN
#         SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))
#         inp.mi.dwFlags = MOUSEEVENTF_LEFTUP
#         SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))
#     else:
#         inp.mi.dwFlags = MOUSEEVENTF_RIGHTDOWN
#         SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))
#         inp.mi.dwFlags = MOUSEEVENTF_RIGHTUP
#         SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))

# def auto_clicker(
#     delay: float,
#     duration: float,
#     follow_8: bool,
#     fixed_x: Optional[int],
#     fixed_y: Optional[int],
#     click_type: str,
#     update_status_callback: Callable[[str, str], None],
#     stop_event: Event,
# ) -> None:
#     """Auto-Clicker mit direktem SendInput"""
#     global button_area
#     start_time = time.time()

#     if button_area:
#         update_status_callback("Warte auf Mausbewegung...", "orange")
#         while not stop_event.is_set():
#             x, y = pyautogui.position()
#             if not (button_area[0] <= x <= button_area[2] and button_area[1] <= y <= button_area[3]):
#                 break
#             time.sleep(0.05)

#     while not stop_event.is_set():
#         if fixed_x is not None and fixed_y is not None:
#             pyautogui.moveTo(fixed_x, fixed_y)

#         if follow_8:
#             move_mouse_in_8_pattern()

#         click_mouse(click_type)

#         if delay > 0:
#             time.sleep(delay)

#         if duration > 0 and (time.time() - start_time) >= duration:
#             stop_event.set()
#             update_status_callback("STOPP", "red")
#             break

# def move_mouse_in_8_pattern():
#     """Bewegt die Maus in einer 8-förmigen Schleife."""
#     center_x, center_y = pyautogui.size()
#     center_x //= 2
#     center_y //= 2
#     radius = 100
#     t = time.time()
#     x = center_x + int(radius * math.sin(t) / (1 + math.cos(t) ** 2))
#     y = center_y + int(radius * math.sin(t) * math.cos(t) / (1 + math.cos(t) ** 2))
#     pyautogui.moveTo(x, y)
