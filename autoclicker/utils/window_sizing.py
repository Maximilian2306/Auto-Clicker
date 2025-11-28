# autoclicker/utils/window_sizing.py
"""Dynamic window sizing utilities for adaptive display support"""

from typing import Tuple
import tkinter as tk
from .constants import (
    WINDOW_WIDTH_MIN,
    WINDOW_HEIGHT_MIN,
    WINDOW_WIDTH_MULTIPLIER_BY_LANGUAGE,
)


def calculate_optimal_window_size(root: tk.Tk, language: str = "English") -> Tuple[int, int]:
    """
    Calculate optimal window size based on screen and language.
    Uses minimum required size, only reduces if screen is too small.
    """
    root.update_idletasks()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    lang_multiplier = WINDOW_WIDTH_MULTIPLIER_BY_LANGUAGE.get(language, 1.0)

    desired_width = int(WINDOW_WIDTH_MIN * lang_multiplier)
    desired_height = WINDOW_HEIGHT_MIN

    # Max 90% of screen to leave space for taskbar
    max_width = int(screen_width * 0.9)
    max_height = int(screen_height * 0.9)

    final_width = min(desired_width, max_width)
    final_height = min(desired_height, max_height)

    return final_width, final_height


def get_centered_geometry(root: tk.Tk, width: int, height: int) -> str:
    """Get geometry string for centering window on screen (format: "WIDTHxHEIGHT+X+Y")"""
    root.update_idletasks()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = max(0, (screen_width - width) // 2)
    y = max(0, (screen_height - height) // 2)

    return f"{width}x{height}+{x}+{y}"
