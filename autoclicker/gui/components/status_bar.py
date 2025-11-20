# autoclicker/gui/status_bar.py
"""
StatusBar Component - Bottom status bar with connection status, profile, and version
"""

from ttkbootstrap.widgets import Frame, Label, Separator

from .base_tab import BaseComponent


class StatusBar(BaseComponent):
    """Bottom status bar component"""

    def __init__(self, parent, manager):
        """
        Initialize StatusBar component

        Args:
            parent: Parent Tkinter widget
            manager: GUIManager instance for accessing shared state
        """
        self.status_text_label = None
        self.connected_label = None
        self.version_label = None
        self._is_ready_state = True  # Track if showing "ready" state

        super().__init__(parent, manager)

    def _build_content(self):
        """Build the status bar UI content"""
        status_bar = Frame(self.parent, padding=10)
        status_bar.pack(side="bottom", fill="x")

        Separator(status_bar, orient="horizontal").pack(fill="x", pady=5)

        status_frame = Frame(status_bar)
        status_frame.pack(fill="x")

        # === Connection status ===
        self.connected_label = Label(
            status_frame,
            text=f"🟢 {self._t('connected')}",
            font=("Segoe UI", 9),
            foreground="green"
        )
        self.connected_label.pack(side="left", padx=10)

        # === Current profile ===
        Label(
            status_frame,
            textvariable=self.manager.state["current_profile"],
            font=("Segoe UI", 9)
        ).pack(side="left", padx=20)

        # === Dynamic status text ===
        self.status_text_label = Label(
            status_frame,
            text=self._t('ready'),
            font=("Segoe UI", 9),
            foreground="gray"
        )
        self.status_text_label.pack(side="left", padx=20)

        # === App-Version ===
        self.version_label = Label(
            status_frame,
            text=self._t('version'),
            font=("Segoe UI", 9),
            foreground="gray"
        )
        self.version_label.pack(side="right", padx=10)

    def update_text(self, message: str, is_ready: bool = False):
        """
        Update status bar text

        Args:
            message: Status message to display
            is_ready: Whether this is the "ready" state (for translation refresh)
        """
        if self.status_text_label:
            self.status_text_label.config(text=message)
            self._is_ready_state = is_ready

    def refresh_translations(self):
        """Refresh all translatable UI elements when language changes"""
        # Update connected label
        if self.connected_label:
            self.connected_label.config(text=f"🟢 {self._t('connected')}")

        # Update version label
        if self.version_label:
            self.version_label.config(text=self._t('version'))

        # Update status text only if it's still showing "Ready" state
        if self.status_text_label and self._is_ready_state:
            self.status_text_label.config(text=self._t('ready'))
