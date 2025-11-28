# autoclicker/utils/notification.py
"""Custom Dialog System - Modern dialogs with animations"""

import tkinter as tk
from ttkbootstrap.widgets import Frame, Label, Button, Entry
from ttkbootstrap.dialogs import Messagebox
from typing import Callable, Optional
import ctypes
import sys


def set_rounded_corners(hwnd):
    """Set rounded corners for Windows 11+ dialogs"""
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


class MessageDialog(tk.Toplevel):
    """Modern message dialog with icon and styled button"""

    TYPE_CONFIG = {
        "info": ("ℹ", "#17a2b8", "#ffffff"),
        "success": ("✓", "#28a745", "#ffffff"),
        "warning": ("⚠", "#ffc107", "#212529"),
        "error": ("✕", "#dc3545", "#ffffff"),
    }

    def __init__(
        self,
        parent: tk.Tk,
        message: str,
        title: str = "Information",
        dialog_type: str = "info",
        ok_text: str = "OK",
    ):
        super().__init__(parent)
        self.parent = parent
        self.result = None
        self.alpha = 0.0
        self.ok_button = None

        icon, bg_color, fg_color = self.TYPE_CONFIG.get(dialog_type, self.TYPE_CONFIG["info"])

        self.title(title)
        self.transient(parent)
        self.resizable(False, False)
        self.withdraw()
        self.attributes("-alpha", 0.0)

        container = Frame(self, padding=12)
        container.pack(fill="both", expand=True)

        content_frame = Frame(container)
        content_frame.pack(fill="both", expand=True, pady=(0, 10))

        icon_frame = Frame(content_frame)
        icon_frame.pack(side="left", padx=(0, 10))

        icon_label = tk.Label(
            icon_frame, text=icon, font=("Segoe UI", 16),
            bg=bg_color, fg=fg_color, width=2, height=1
        )
        icon_label.pack(padx=2, pady=2)

        message_label = Label(
            content_frame, text=message, font=("Segoe UI", 9),
            wraplength=180, justify="left"
        )
        message_label.pack(side="left", fill="both", expand=True, anchor="w")

        button_frame = Frame(container)
        button_frame.pack(fill="x")

        self.ok_button = Button(
            button_frame, text=ok_text, command=self._on_ok,
            bootstyle="primary", width=6
        )
        self.ok_button.pack(side="right")

        self.bind("<Return>", lambda e: self._on_ok())
        self.bind("<Escape>", lambda e: self._on_ok())
        self.protocol("WM_DELETE_WINDOW", self._on_ok)

    def _center_on_parent(self):
        """Center dialog on parent window after it's fully rendered"""
        self.update_idletasks()

        width = max(250, self.winfo_reqwidth())
        height = max(100, self.winfo_reqheight())

        # Get parent geometry using geometry string parsing for reliability
        try:
            parent_geo = self.parent.geometry()
            parent_size, parent_pos = parent_geo.split('+', 1)
            parent_w, parent_h = map(int, parent_size.split('x'))
            pos_parts = parent_pos.split('+')
            parent_x, parent_y = int(pos_parts[0]), int(pos_parts[1])
        except Exception:
            # Fallback to winfo methods
            parent_x = self.parent.winfo_x()
            parent_y = self.parent.winfo_y()
            parent_w = self.parent.winfo_width()
            parent_h = self.parent.winfo_height()

        # Calculate centered position and ensure dialog is visible on screen
        x = max(0, min(parent_x + (parent_w - width) // 2, self.winfo_screenwidth() - width))
        y = max(0, min(parent_y + (parent_h - height) // 2, self.winfo_screenheight() - height))

        self.geometry(f"{width}x{height}+{x}+{y}")
        self.deiconify()

        # Apply rounded corners on Windows 11+
        if sys.platform == "win32":
            try:
                hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
                set_rounded_corners(hwnd)
            except Exception:
                pass

        # Make modal after positioning
        self.grab_set()
        self.focus_set()
        self.ok_button.focus_set()

    def _fade_in(self):
        """Smooth fade-in animation"""
        if self.alpha < 1.0:
            self.alpha = min(1.0, self.alpha + 0.15)
            try:
                self.attributes("-alpha", self.alpha)
                if self.alpha < 1.0:
                    self.after(10, self._fade_in)
            except Exception:
                pass

    def _on_ok(self):
        """Handle OK button click"""
        self.result = True
        self.destroy()

    def show(self):
        """Show dialog with fade-in and wait for result"""
        self._center_on_parent()
        self._fade_in()
        self.wait_window()
        return self.result


class InputDialog(tk.Toplevel):
    """Modern input dialog with styling and translation support"""

    def __init__(
        self,
        parent: tk.Tk,
        title: str = "Input",
        prompt: str = "Enter value:",
        info_text: Optional[str] = None,
        initial_value: str = "",
        ok_text: str = "OK",
        cancel_text: str = "Cancel",
    ):
        super().__init__(parent)
        self.parent = parent
        self.result = None
        self.alpha = 0.0

        self.title(title)
        self.transient(parent)
        self.resizable(False, False)
        self.withdraw()
        self.attributes("-alpha", 0.0)

        container = Frame(self, padding=20)
        container.pack(fill="both", expand=True)

        if info_text:
            info_label = Label(
                container, text=info_text, font=("Segoe UI", 10, "bold"),
                wraplength=280, justify="left", bootstyle="secondary"
            )
            info_label.pack(anchor="w", pady=(0, 8))

        prompt_label = Label(
            container, text=prompt, font=("Segoe UI", 10, "bold"),
            wraplength=280, justify="left"
        )
        prompt_label.pack(anchor="w", pady=(0, 8))

        self.entry = Entry(
            container, font=("Segoe UI", 10), width=35, bootstyle="primary"
        )
        self.entry.pack(fill="x", pady=(0, 15))
        self.entry.insert(0, initial_value)
        self.entry.select_range(0, tk.END)
        self.entry.focus_set()

        button_frame = Frame(container)
        button_frame.pack(fill="x")

        cancel_button = Button(
            button_frame, text=cancel_text, command=self._on_cancel,
            bootstyle="secondary-outline", width=10
        )
        cancel_button.pack(side="right", padx=(5, 0))

        ok_button = Button(
            button_frame, text=ok_text, command=self._on_ok,
            bootstyle="primary", width=10
        )
        ok_button.pack(side="right")

        self.bind("<Return>", lambda e: self._on_ok())
        self.bind("<Escape>", lambda e: self._on_cancel())
        self.protocol("WM_DELETE_WINDOW", self._on_cancel)

    def _center_on_parent(self):
        """Center dialog on parent window after it's fully rendered"""
        self.update_idletasks()

        width = max(350, self.winfo_reqwidth())
        height = max(150, self.winfo_reqheight())

        # Get parent geometry using geometry string parsing for reliability
        try:
            parent_geo = self.parent.geometry()
            parent_size, parent_pos = parent_geo.split('+', 1)
            parent_w, parent_h = map(int, parent_size.split('x'))
            pos_parts = parent_pos.split('+')
            parent_x, parent_y = int(pos_parts[0]), int(pos_parts[1])
        except Exception:
            # Fallback to winfo methods
            parent_x = self.parent.winfo_x()
            parent_y = self.parent.winfo_y()
            parent_w = self.parent.winfo_width()
            parent_h = self.parent.winfo_height()

        # Calculate centered position and ensure dialog is visible on screen
        x = max(0, min(parent_x + (parent_w - width) // 2, self.winfo_screenwidth() - width))
        y = max(0, min(parent_y + (parent_h - height) // 2, self.winfo_screenheight() - height))

        self.geometry(f"{width}x{height}+{x}+{y}")
        self.deiconify()

        # Apply rounded corners on Windows 11+
        if sys.platform == "win32":
            try:
                hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
                set_rounded_corners(hwnd)
            except Exception:
                pass

        # Make modal after positioning
        self.grab_set()
        self.focus_set()
        self.entry.focus_set()

    def _fade_in(self):
        """Smooth fade-in animation"""
        if self.alpha < 1.0:
            self.alpha = min(1.0, self.alpha + 0.15)
            try:
                self.attributes("-alpha", self.alpha)
                if self.alpha < 1.0:
                    self.after(10, self._fade_in)
            except Exception:
                pass

    def _on_ok(self):
        """Handle OK button click"""
        self.result = self.entry.get().strip()
        self.destroy()

    def _on_cancel(self):
        """Handle Cancel button click"""
        self.result = None
        self.destroy()

    def show(self):
        """Show dialog with fade-in and wait for result"""
        self._center_on_parent()
        self._fade_in()
        self.wait_window()
        return self.result


class NotificationManager:
    """Manager for showing dialogs with translation support"""

    def __init__(self, parent: tk.Tk, get_text: Optional[Callable[[str], str]] = None):
        self.parent = parent
        self._get_text = get_text

    def _t(self, key: str) -> str:
        if self._get_text:
            return self._get_text(key)
        return {"ok": "OK", "cancel": "Cancel"}.get(key, key)

    def _show_dialog(self, message: str, title: str, dialog_type: str, on_closed: Optional[Callable[[], None]] = None):
        try:
            dialog = MessageDialog(self.parent, message, title, dialog_type, ok_text=self._t("ok"))
            dialog.show()
            if on_closed:
                on_closed()
        except Exception as e:
            print(f"Error showing {dialog_type} notification: {e}")

    def show_info(self, message: str, title: str = "Information", on_closed: Optional[Callable[[], None]] = None):
        """Show info dialog"""
        self._show_dialog(message, title, "info", on_closed)

    def show_success(self, message: str, title: str = "Success", on_closed: Optional[Callable[[], None]] = None):
        """Show success dialog"""
        self._show_dialog(message, title, "success", on_closed)

    def show_warning(self, message: str, title: str = "Warning", on_closed: Optional[Callable[[], None]] = None):
        """Show warning dialog"""
        self._show_dialog(message, title, "warning", on_closed)

    def show_error(self, message: str, title: str = "Error", on_closed: Optional[Callable[[], None]] = None):
        """Show error dialog"""
        self._show_dialog(message, title, "error", on_closed)

    def ask_string(self, title: str = "Input", prompt: str = "Enter value:",
                   info_text: Optional[str] = None, initial_value: str = "") -> Optional[str]:
        """Show input dialog and return user input"""
        try:
            dialog = InputDialog(
                self.parent, title=title, prompt=prompt, info_text=info_text,
                initial_value=initial_value, ok_text=self._t("ok"), cancel_text=self._t("cancel")
            )
            return dialog.show() or None
        except Exception as e:
            print(f"Error showing input dialog: {e}")
            return None

    def confirm(self, message: str, title: str = "Confirm") -> bool:
        """Show confirmation dialog, returns True if Yes clicked"""
        try:
            return Messagebox.yesno(message, title, parent=self.parent) == "Yes"
        except Exception as e:
            print(f"Error showing confirmation: {e}")
            return False
