# status_bar.py
import ttkbootstrap as ttkb
from ttkbootstrap.widgets import Frame, Label, Separator


class StatusBar:
    """Bottom status bar component"""

    def __init__(self, manager, parent):
        self.manager = manager
        self.parent = parent
        self.status_text_label = None
        self.connected_label = None
        self.version_label = None
        self._build()

    def _t(self, key: str) -> str:
        """Get translated text via manager's translation service"""
        return self.manager.t(key)

    def _build(self):
        """Builds content"""

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

    def update_text(self, message: str):
        """Update status bar text"""
        if self.status_text_label:
            self.status_text_label.config(text=message)

    def refresh_translations(self):
        """Refresh all translatable UI elements when language changes"""
        if hasattr(self, 'connected_label') and self.connected_label:
            self.connected_label.config(text=f"🟢 {self._t('connected')}")

        if hasattr(self, 'version_label') and self.version_label:
            self.version_label.config(text=self._t('version'))

        # Update status text only if it's still showing "Ready"
        if hasattr(self, 'status_text_label') and self.status_text_label:
            current = self.status_text_label.cget('text')
            if 'ready' in current.lower() or 'bereit' in current.lower():
                self.status_text_label.config(text=self._t('ready'))