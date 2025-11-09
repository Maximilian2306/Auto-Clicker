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
        self.profile_combo = None

        self._build()

    def _build(self):
        """Builds content"""

        top_bar = Frame(self.parent, padding=15)
        top_bar.pack(fill="x")

        # === App title === 
        Label(top_bar, text="ClickMAX", font=("Segoe UI", 18, "bold"), bootstyle="primary").pack(side="left", padx=10)

        # === Profile selector ===
        profile_frame = Frame(top_bar)
        profile_frame.pack(side="right", padx=10)

        self.profile_combo = Combobox(
            profile_frame,
            textvariable=self.manager.state["current_profile"],
            values=self.manager.model.get_profile_list(),
            state="readonly",
            width=12,
            bootstyle="primary"
        )
        self.profile_combo.pack(side="left", padx=5)
        self.profile_combo.bind("<<ComboboxSelected>>", self._on_profile_selected)

        # === Quick theme toggle ===
        Button(
            top_bar,
            text="🎨",
            command=self.on_cycle_theme,
            bootstyle="primary-outline",
            width=3
        ).pack(side="right", padx=5)

    def refresh_profile_list(self):
        """Update the Combobox list of profiles"""
        if self.profile_combo:
            profiles = self.manager.model.get_profile_list()
            self.profile_combo.configure(values=profiles)

    def _on_profile_selected(self, event):
        selected = self.profile_combo.get()
        if hasattr(self.manager, "_on_load_profile"):
            self.manager._on_load_profile(selected)