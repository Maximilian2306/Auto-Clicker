# autoclicker/utils/toast_notification.py
"""Toast notifications with fade animations and auto-dismiss"""

import tkinter as tk
from typing import Literal
import ctypes
import sys


def set_rounded_corners(hwnd):
    """Set rounded corners for Windows 11+ toasts"""
    if sys.platform != "win32":
        return False

    try:
        dwmapi = ctypes.windll.dwmapi
        corner_preference = ctypes.c_int(2) 
        result = dwmapi.DwmSetWindowAttribute(
            hwnd, 33, ctypes.byref(corner_preference), ctypes.sizeof(corner_preference)
        )
        return result == 0
    except Exception:
        return False


NotificationType = Literal["success", "error", "warning", "info"]


class ToastNotification:
    """Non-blocking toast notification with fade animation and auto-dismiss"""

    TYPE_CONFIG = {
        "success": ("✓", "#28a745", "#ffffff", "#1e7e34"),
        "error": ("✕", "#dc3545", "#ffffff", "#bd2130"),
        "warning": ("⚠", "#ffc107", "#212529", "#e0a800"),
        "info": ("ℹ", "#17a2b8", "#ffffff", "#138496"),
    }

    def __init__(self, parent: tk.Tk, message: str, notification_type: NotificationType = "info",
                 duration: int = 1500, fade_duration: int = 150):
        """Initialize toast notification with message, type and timing settings"""
        self.parent = parent
        self.duration = duration
        self.fade_duration = fade_duration
        self.alpha = 0.0
        self.is_closing = False

        # Get type configuration
        icon, bg_color, fg_color, _ = self.TYPE_CONFIG.get(notification_type, self.TYPE_CONFIG["info"])

        # Create toplevel window
        self.window = tk.Toplevel(parent)
        self.window.overrideredirect(True)  # Remove window decorations
        self.window.attributes("-topmost", True)
        self.window.attributes("-alpha", 0.0)  # Start invisible
        self.window.configure(bg=bg_color)

        # Apply rounded corners on Windows 11+
        self.window.update_idletasks()
        has_rounded_corners = False
        if sys.platform == "win32":
            try:
                hwnd = ctypes.windll.user32.GetParent(self.window.winfo_id())
                has_rounded_corners = set_rounded_corners(hwnd)
            except Exception:
                pass

        # Add extra padding if rounded corners not available
        extra_pad = 0 if has_rounded_corners else 2
        main_frame = tk.Frame(self.window, bg=bg_color, padx=10 + extra_pad, pady=6 + extra_pad)
        main_frame.pack(padx=1, pady=1)

        icon_label = tk.Label(
            main_frame, text=icon, font=("Segoe UI", 10, "bold"), bg=bg_color, fg=fg_color
        )
        icon_label.pack(side="left", padx=(0, 6))

        message_label = tk.Label(
            main_frame, text=message, font=("Segoe UI", 9),
            bg=bg_color, fg=fg_color, wraplength=250
        )
        message_label.pack(side="left")

        self.window.update_idletasks()
        self._position_window()
        # Bind to parent resize/move to update position
        parent.bind("<Configure>", self._on_parent_configure, add="+")

    def _position_window(self):
        """Position notification centered at bottom of parent window"""
        try:
            parent_x = self.parent.winfo_x()
            parent_y = self.parent.winfo_y()
            parent_width = self.parent.winfo_width()
            parent_height = self.parent.winfo_height()

            notif_width = self.window.winfo_reqwidth()
            notif_height = self.window.winfo_reqheight()

            x = parent_x + (parent_width - notif_width) // 2
            y = parent_y + parent_height - notif_height - 15

            self.window.geometry(f"+{x}+{y}")
        except Exception:
            pass

    def _on_parent_configure(self, _):
        """Update position when parent window moves or resizes"""
        if not self.is_closing:
            self._position_window()

    def show(self):
        """Show the notification with fade-in animation"""
        self._fade_in()

    def _fade_in(self):
        """Animate fade-in effect"""
        if self.alpha < 0.95:
            self.alpha += 0.1
            try:
                self.window.attributes("-alpha", self.alpha)
                self.window.after(self.fade_duration // 10, self._fade_in)
            except Exception:
                pass
        else:
            self.alpha = 0.95
            try:
                self.window.attributes("-alpha", self.alpha)
                # Schedule auto-dismiss
                self.window.after(self.duration, self.close)
            except Exception:
                pass

    def close(self):
        """Close the notification with fade-out animation"""
        if not self.is_closing:
            self.is_closing = True
            self._fade_out()

    def _fade_out(self):
        """Animate fade-out effect"""
        if self.alpha > 0.05:
            self.alpha -= 0.1
            try:
                self.window.attributes("-alpha", self.alpha)
                self.window.after(self.fade_duration // 10, self._fade_out)
            except Exception:
                self._destroy()
        else:
            self._destroy()

    def _destroy(self):
        """Destroy the notification window"""
        try:
            self.parent.unbind("<Configure>")
            self.window.destroy()
        except Exception:
            pass


class ToastManager:
    """Manager for showing toast notifications of different types"""

    def __init__(self, parent: tk.Tk):
        """Initialize toast manager with parent window"""
        self.parent = parent
        self._active_toasts: list[ToastNotification] = []

    def show(self, message: str, notification_type: NotificationType = "info", duration: int = 1500):
        """Show a toast notification with message, type and duration"""
        toast = ToastNotification(self.parent, message, notification_type, duration)
        self._active_toasts.append(toast)
        toast.show()

    def success(self, message: str, duration: int = 1500):
        """Show success notification"""
        self.show(message, "success", duration)

    def error(self, message: str, duration: int = 2000):
        """Show error notification"""
        self.show(message, "error", duration)

    def warning(self, message: str, duration: int = 1500):
        """Show warning notification"""
        self.show(message, "warning", duration)

    def info(self, message: str, duration: int = 1500):
        """Show info notification"""
        self.show(message, "info", duration)
