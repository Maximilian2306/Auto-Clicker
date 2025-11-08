# status_bar.py
import ttkbootstrap as ttkb
from ttkbootstrap.widgets import Frame, Label, Separator


class StatusBar:
    """Bottom status bar component"""

    def __init__(self, manager, parent):
        self.manager = manager
        self.parent = parent
        self.status_text_label = None
        self._build()

    def _build(self):
        """Builds content"""
        
        status_bar = Frame(self.parent, padding=10)
        status_bar.pack(side="bottom", fill="x")
        
        Separator(status_bar, orient="horizontal").pack(fill="x", pady=5)
        
        status_frame = Frame(status_bar)
        status_frame.pack(fill="x")
        
        # === Connection status ===
        Label(
            status_frame,
            text="🟢 Connected",
            font=("Segoe UI", 9),
            foreground="green"
        ).pack(side="left", padx=10)
        
        # === Current profile ===
        Label(
            status_frame,
            textvariable=self.manager.state["current_profile"],
            font=("Segoe UI", 9)
        ).pack(side="left", padx=20)
        
        # === Dynamic status text ===
        self.status_text_label = Label(
            status_frame,
            text="Ready",
            font=("Segoe UI", 9),
            foreground="gray"
        )
        self.status_text_label.pack(side="left", padx=20)
        
        # === App-Version ===
        Label(
            status_frame,
            text="v1.0.0 Pro",
            font=("Segoe UI", 9),
            foreground="gray"
        ).pack(side="right", padx=10)

    def update_text(self, message: str):
        """Update status bar text"""
        if self.status_text_label:
            self.status_text_label.config(text=message)