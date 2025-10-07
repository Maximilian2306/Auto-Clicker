# top_bar.py
from ttkbootstrap import Frame, Label, Button, Combobox


class TopBar(Frame):
    def __init__(self, manager, parent):
        super().__init__(parent, padding=15)
        self.manager = manager
        self.pack(fill="x")
        self._build_ui()

    def _build_ui(self):
        # Titel
        Label(
            self,
            text="Modern Auto-Clicker Pro",
            font=("Segoe UI", 18, "bold"),
            bootstyle="primary",
        ).pack(side="left", padx=10)

        # Profilauswahl
        profile_frame = Frame(self)
        profile_frame.pack(side="right", padx=10)

        Label(profile_frame, text="Profile:").pack(side="left", padx=5)
        self.profile_combo = Combobox(
            profile_frame,
            textvariable=self.manager.state["current_profile"],
            values=["Default", "Gamer", "Custom1"],  # später dynamisch laden
            width=15,
            bootstyle="primary",
        )
        self.profile_combo.pack(side="left")

        # Theme-Toggle
        Button(
            self,
            text="🎨",
            command=self._cycle_theme,
            bootstyle="secondary-outline",
            width=3,
        ).pack(side="right", padx=5)

    def _cycle_theme(self):
        themes = ["cyborg", "flatly", "superhero", "darkly"]
        self.manager.current_theme_index = (
            self.manager.current_theme_index + 1
        ) % len(themes)
        new_theme = themes[self.manager.current_theme_index]
        self.manager.style.theme_use(new_theme)
        self.manager.update_status(f"Theme changed to {new_theme}")
