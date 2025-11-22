# autoclicker/gui/components/top_bar.py
"""
TopBar Component - Application header with title, profile selector, and theme toggle
"""

import ttkbootstrap as ttkb
from ttkbootstrap.widgets import Frame, Label, Button, Combobox
from typing import Callable

from .base_tab import BaseComponent


class TopBar(BaseComponent):
    """Top bar component with title, profile selector, and theme toggle."""

    def __init__(
        self,
        parent,
        manager,
        on_cycle_theme: Callable[[], None],
        on_load_profile: Callable[[str], None],
    ):
        """Initialize TopBar with theme toggle and profile selector"""
        self.on_cycle_theme = on_cycle_theme
        self.on_load_profile = on_load_profile
        self.profile_combo = None

        super().__init__(parent, manager)

    def _build_content(self):
        """Build the top bar UI content"""
        top_bar = Frame(self.parent, padding=15)
        top_bar.pack(fill="x")

        # === App title ===
        Label(
            top_bar,
            text="ClickMAX",
            font=("Segoe UI", 18, "bold"),
            bootstyle="primary"
        ).pack(side="left", padx=10)

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
        """Handle profile selection from combobox"""
        selected = self.profile_combo.get()
        self.on_load_profile(selected)

    def refresh_translations(self):
        """Refresh all translatable UI elements when language changes"""
        pass
