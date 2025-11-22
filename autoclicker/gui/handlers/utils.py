# autoclicker/gui/handlers/utils.py
"""
GUI Utilities - Helper functions for consistent UI updates

This module provides utility functions for GUI components to ensure
consistent behavior across the application.
"""

from tkinter import StringVar
from typing import Optional


def update_button_state(
    button,
    bootstyle: str,
    text_var: Optional[StringVar] = None,
    text: Optional[str] = None,
    width: Optional[int] = None,
    style: Optional[str] = None
) -> None:
    """Update button state consistently with bootstyle and optional text/width"""
    # Build config dict
    config = {"bootstyle": bootstyle}

    if width is not None:
        config["width"] = width

    if style is not None:
        config["style"] = style

    # Apply configuration
    button.configure(**config)

    # Update text via StringVar if provided
    if text_var is not None and text is not None:
        text_var.set(text)


def update_label_state(
    label,
    text_var: Optional[StringVar] = None,
    text: Optional[str] = None,
    bootstyle: Optional[str] = None
) -> None:
    """Update label state consistently with optional text and bootstyle"""
    if bootstyle is not None:
        label.configure(bootstyle=bootstyle)

    if text_var is not None and text is not None:
        text_var.set(text)
