# autoclicker/utils/notification.py
"""Custom Dialog System - Modern dialogs with animations"""

import tkinter as tk
from ttkbootstrap.widgets import Frame, Label, Button, Entry
from ttkbootstrap.dialogs import Messagebox
from typing import Callable, Optional
import ctypes
import sys


def set_rounded_corners(hwnd):
    """Set rounded corners for a window on Windows 11+."""
    if sys.platform != "win32":
        return False

    try:
        DWMWA_WINDOW_CORNER_PREFERENCE = 33
        DWMWCP_ROUND = 2

        dwmapi = ctypes.windll.dwmapi
        corner_preference = ctypes.c_int(DWMWCP_ROUND)
        result = dwmapi.DwmSetWindowAttribute(
            hwnd,
            DWMWA_WINDOW_CORNER_PREFERENCE,
            ctypes.byref(corner_preference),
            ctypes.sizeof(corner_preference)
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

        # Window setup
        self.title(title)
        self.transient(parent)
        self.resizable(False, False)

        # Hide window initially, will show after centering
        self.withdraw()
        self.attributes("-alpha", 0.0)

        # Main container - compact padding
        container = Frame(self, padding=12)
        container.pack(fill="both", expand=True)

        # Content frame (icon + message)
        content_frame = Frame(container)
        content_frame.pack(fill="both", expand=True, pady=(0, 10))

        # Icon with color background - compact size
        icon_frame = Frame(content_frame)
        icon_frame.pack(side="left", padx=(0, 10))

        icon_label = tk.Label(
            icon_frame,
            text=icon,
            font=("Segoe UI", 16),  # Smaller icon
            bg=bg_color,
            fg=fg_color,
            width=2,
            height=1,
        )
        icon_label.pack(padx=2, pady=2)

        # Message - compact font and wraplength
        message_label = Label(
            content_frame,
            text=message,
            font=("Segoe UI", 9),  # Smaller font
            wraplength=180,  # Smaller wrap
            justify="left",
        )
        message_label.pack(side="left", fill="both", expand=True, anchor="w")

        # Button frame
        button_frame = Frame(container)
        button_frame.pack(fill="x")

        self.ok_button = Button(
            button_frame,
            text=ok_text,
            command=self._on_ok,
            bootstyle="primary",
            width=6,  # Smaller button
        )
        self.ok_button.pack(side="right")

        # Bind keys
        self.bind("<Return>", lambda e: self._on_ok())
        self.bind("<Escape>", lambda e: self._on_ok())

        # Handle close button
        self.protocol("WM_DELETE_WINDOW", self._on_ok)

    def _center_on_parent(self):
        """Center dialog on parent window after it's fully rendered."""
        # Force geometry calculation
        self.update_idletasks()

        width = max(250, self.winfo_reqwidth())  # Compact minimum width
        height = max(100, self.winfo_reqheight())  # Compact minimum height

        # Get parent geometry using geometry string parsing for reliability
        try:
            parent_geo = self.parent.geometry()
            parent_size, parent_pos = parent_geo.split('+', 1)
            parent_w, parent_h = map(int, parent_size.split('x'))
            pos_parts = parent_pos.split('+')
            parent_x = int(pos_parts[0])
            parent_y = int(pos_parts[1])
        except Exception:
            parent_x = self.parent.winfo_x()
            parent_y = self.parent.winfo_y()
            parent_w = self.parent.winfo_width()
            parent_h = self.parent.winfo_height()

        # Calculate centered position
        x = parent_x + (parent_w - width) // 2
        y = parent_y + (parent_h - height) // 2

        # Ensure dialog is visible on screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = max(0, min(x, screen_width - width))
        y = max(0, min(y, screen_height - height))

        self.geometry(f"{width}x{height}+{x}+{y}")

        # Show window after positioning
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
        """Smooth fade-in animation."""
        if self.alpha < 1.0:
            self.alpha += 0.15
            if self.alpha > 1.0:
                self.alpha = 1.0
            try:
                self.attributes("-alpha", self.alpha)
                if self.alpha < 1.0:
                    self.after(10, self._fade_in)
            except Exception:
                pass

    def _on_ok(self):
        """Handle OK button click."""
        self.result = True
        self.destroy()

    def show(self):
        """Show dialog with fade-in and wait for result."""
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

        # Window setup
        self.title(title)
        self.transient(parent)
        self.resizable(False, False)

        # Hide window initially, will show after centering
        self.withdraw()
        self.attributes("-alpha", 0.0)

        # Main container
        container = Frame(self, padding=20)
        container.pack(fill="both", expand=True)

        # Info text (if provided) - same styling as prompt for consistency
        if info_text:
            info_label = Label(
                container,
                text=info_text,
                font=("Segoe UI", 10, "bold"),
                wraplength=280,
                justify="left",
                bootstyle="secondary",
            )
            info_label.pack(anchor="w", pady=(0, 8))

        # Prompt label
        prompt_label = Label(
            container,
            text=prompt,
            font=("Segoe UI", 10, "bold"),
            wraplength=280,
            justify="left",
        )
        prompt_label.pack(anchor="w", pady=(0, 8))

        # Entry field
        self.entry = Entry(
            container,
            font=("Segoe UI", 10),
            width=35,
            bootstyle="primary",
        )
        self.entry.pack(fill="x", pady=(0, 15))
        self.entry.insert(0, initial_value)
        self.entry.select_range(0, tk.END)
        self.entry.focus_set()

        # Button frame
        button_frame = Frame(container)
        button_frame.pack(fill="x")

        cancel_button = Button(
            button_frame,
            text=cancel_text,
            command=self._on_cancel,
            bootstyle="secondary-outline",
            width=10,
        )
        cancel_button.pack(side="right", padx=(5, 0))

        ok_button = Button(
            button_frame,
            text=ok_text,
            command=self._on_ok,
            bootstyle="primary",
            width=10,
        )
        ok_button.pack(side="right")

        # Bind keys
        self.bind("<Return>", lambda e: self._on_ok())
        self.bind("<Escape>", lambda e: self._on_cancel())

        # Handle close button
        self.protocol("WM_DELETE_WINDOW", self._on_cancel)

    def _center_on_parent(self):
        """Center dialog on parent window after it's fully rendered."""
        # Force geometry calculation
        self.update_idletasks()

        width = max(350, self.winfo_reqwidth())
        height = max(150, self.winfo_reqheight())

        # Get parent geometry using geometry string parsing for reliability
        try:
            # Parse parent geometry string: "WIDTHxHEIGHT+X+Y"
            parent_geo = self.parent.geometry()
            parent_size, parent_pos = parent_geo.split('+', 1)
            parent_w, parent_h = map(int, parent_size.split('x'))
            pos_parts = parent_pos.split('+')
            parent_x = int(pos_parts[0])
            parent_y = int(pos_parts[1])
        except Exception:
            # Fallback to winfo methods
            parent_x = self.parent.winfo_x()
            parent_y = self.parent.winfo_y()
            parent_w = self.parent.winfo_width()
            parent_h = self.parent.winfo_height()

        # Calculate centered position
        x = parent_x + (parent_w - width) // 2
        y = parent_y + (parent_h - height) // 2

        # Ensure dialog is visible on screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = max(0, min(x, screen_width - width))
        y = max(0, min(y, screen_height - height))

        self.geometry(f"{width}x{height}+{x}+{y}")

        # Show window after positioning
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
        """Smooth fade-in animation."""
        if self.alpha < 1.0:
            self.alpha += 0.15
            if self.alpha > 1.0:
                self.alpha = 1.0
            try:
                self.attributes("-alpha", self.alpha)
                if self.alpha < 1.0:
                    self.after(10, self._fade_in)
            except Exception:
                pass

    def _on_ok(self):
        """Handle OK button click."""
        self.result = self.entry.get().strip()
        self.destroy()

    def _on_cancel(self):
        """Handle Cancel button click."""
        self.result = None
        self.destroy()

    def show(self):
        """Show dialog with fade-in and wait for result."""
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
        """Get translated text or return key if no translation function."""
        if self._get_text:
            return self._get_text(key)
        # Default English fallback
        defaults = {
            "ok": "OK",
            "cancel": "Cancel",
        }
        return defaults.get(key, key)

    def show_info(
        self,
        message: str,
        title: str = "Information",
        on_closed: Optional[Callable[[], None]] = None,
    ):
        """Show info dialog."""
        try:
            dialog = MessageDialog(
                self.parent, message, title, "info",
                ok_text=self._t("ok")
            )
            dialog.show()
            if on_closed:
                on_closed()
        except Exception as e:
            print(f"Error showing info notification: {e}")

    def show_success(
        self,
        message: str,
        title: str = "Success",
        on_closed: Optional[Callable[[], None]] = None,
    ):
        """Show success dialog."""
        try:
            dialog = MessageDialog(
                self.parent, message, title, "success",
                ok_text=self._t("ok")
            )
            dialog.show()
            if on_closed:
                on_closed()
        except Exception as e:
            print(f"Error showing success notification: {e}")

    def show_warning(
        self,
        message: str,
        title: str = "Warning",
        on_closed: Optional[Callable[[], None]] = None,
    ):
        """Show warning dialog."""
        try:
            dialog = MessageDialog(
                self.parent, message, title, "warning",
                ok_text=self._t("ok")
            )
            dialog.show()
            if on_closed:
                on_closed()
        except Exception as e:
            print(f"Error showing warning notification: {e}")

    def show_error(
        self,
        message: str,
        title: str = "Error",
        on_closed: Optional[Callable[[], None]] = None,
    ):
        """Show error dialog."""
        try:
            dialog = MessageDialog(
                self.parent, message, title, "error",
                ok_text=self._t("ok")
            )
            dialog.show()
            if on_closed:
                on_closed()
        except Exception as e:
            print(f"Error showing error notification: {e}")

    def ask_string(
        self,
        title: str = "Input",
        prompt: str = "Enter value:",
        info_text: Optional[str] = None,
        initial_value: str = "",
    ) -> Optional[str]:
        """Show input dialog and return user input"""
        try:
            dialog = InputDialog(
                self.parent,
                title=title,
                prompt=prompt,
                info_text=info_text,
                initial_value=initial_value,
                ok_text=self._t("ok"),
                cancel_text=self._t("cancel"),
            )
            result = dialog.show()
            return result if result else None
        except Exception as e:
            print(f"Error showing input dialog: {e}")
            return None

    def confirm(
        self,
        message: str,
        title: str = "Confirm",
    ) -> bool:
        """Show confirmation dialog. Returns True if Yes clicked."""
        try:
            result = Messagebox.yesno(message, title, parent=self.parent)
            return result == "Yes"
        except Exception as e:
            print(f"Error showing confirmation: {e}")
            return False
