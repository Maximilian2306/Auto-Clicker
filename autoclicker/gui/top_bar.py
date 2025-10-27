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

        top_bar = Frame(self.parent, padding=15)
        top_bar.pack(fill="x")
        
        # App title 
        title_label = Label(
            top_bar,
            text="ClickMax Pro",
            font=("Segoe UI", 18, "bold"),
            bootstyle="primary"
        )
        title_label.pack(side="left", padx=10)
        
        # Profile selector
        profile_frame = Frame(top_bar)
        profile_frame.pack(side="right", padx=10)
        
        Label(profile_frame, text="Profile:").pack(side="left", padx=5)
        # self.profile_combo.pack(side="left")
        # self.profile_combo.bind("<<ComboboxSelected>>", self.on_profile_selected)
        
        # Quick theme toggle
        Button(
            top_bar,
            text="🎨",
            command=self.on_cycle_theme,
            bootstyle="secondary-outline",
            width=3
        ).pack(side="right", padx=5)
