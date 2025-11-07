# autoclicker/utils/theme.py
"""
Theme Management Utility
Handles theme cycling and application

"""

from typing import Callable, List

class ThemeManager:
    """Handles theme cycling and application"""

    def __init__(self):
        self.current_theme_index = 0
        self.available_themes = []

    def set_available_themes(self, themes: List[str]):
        self.available_themes = themes

    def cycle_theme(self, style_object, on_theme_applied: Callable[[str], None],) -> str:
        """Cycle through available themes"""
        if not self.available_themes:
            return None

        self.current_theme_index = (self.current_theme_index + 1) % len(self.available_themes)
        theme_name = self.available_themes[self.current_theme_index]

        self.apply_theme(style_object, theme_name, on_theme_applied)
        return theme_name

    def apply_theme(self, style_object, theme_name: str, on_theme_applied: Callable[[str], None],) -> bool:
        """Apply a specific theme"""
        try:
            style_object.theme_use(theme_name)
            if on_theme_applied:
                on_theme_applied(theme_name)
            return True
        except Exception as e:
            if on_theme_applied:
                on_theme_applied(f"❗ Error applying theme: {e}")
            return False


    # Wird derzeit nich verwendet vielleicht findet sich noch eine Anwendungsmöglichkeit
    def get_current_theme(self) -> str:
        """Get currently active theme"""
        if self.available_themes and self.current_theme_index < len(self.available_themes):
            return self.available_themes[self.current_theme_index]
        return None