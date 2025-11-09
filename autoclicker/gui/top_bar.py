# autoclicker/gui/top_bar.py
import ttkbootstrap as ttkb
from ttkbootstrap.widgets import Frame, Label, Button, Combobox
from typing import Callable


class TopBar:
    """Top bar component with title, profile selector, and theme toggle."""

    def __init__(self, manager, parent, on_cycle_theme):
        self.manager = manager
        self.parent = parent
        self.on_cycle_theme = on_cycle_theme

        self._build()

    def _build(self):
        """Builds content"""

        top_bar = Frame(self.parent, padding=15)
        top_bar.pack(fill="x")

        # === App title === 
        title_label = Label(
            top_bar,
            text="ClickMAX",
            font=("Segoe UI", 18, "bold"),
            bootstyle="primary"
        )
        title_label.pack(side="left", padx=10)

        # === Profile selector ===
        profile_frame = Frame(top_bar)
        profile_frame.pack(side="right", padx=10)

        profile_name_label = self.manager.state["current_profile"]

        Label(profile_frame, text="Profile: ").pack(side="left", padx=5)
        Combobox(
            profile_frame,
            textvariable=profile_name_label,
            # values=self.manager.get_profile_names(),
            state="readonly",
            width=10,
            bootstyle="primary"
        ).pack(side="left", padx=5)

        # === Quick theme toggle ===
        Button(
            top_bar,
            text="🎨",
            command=self.on_cycle_theme,
            bootstyle="primary-outline",
            width=3
        ).pack(side="right", padx=5)