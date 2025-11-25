# autoclicker/gui/handlers/profile_handler.py
"""
ProfileHandler - Profile management extracted from GUIManager

Handles saving, loading, and deleting profiles with proper MVC separation.
"""

from typing import TYPE_CHECKING
from ... import events

if TYPE_CHECKING:
    from ..gui_manager import GUIManager


class ProfileHandler:
    """Handles all profile-related operations (save, load, delete)"""

    def __init__(self, gui_manager: "GUIManager"):
        self.gm = gui_manager

    def save(self, profile_name: str):
        """Save current settings as a profile"""
        settings = {
            # MainTab settings
            "delay": self.gm.main_tab.delay_var.get(),
            "duration": self.gm.main_tab.duration_var.get(),
            "click_type": self.gm.main_tab.click_type_var.get(),
            "repeat": self.gm.main_tab.repeat_var.get(),
            "random_delay": self.gm.main_tab.random_delay_var.get(),
            "notify_when_done": self.gm.main_tab.notify_var.get(),

            # PatternsTab settings
            "pattern": self.gm.patterns_tab.pattern_var.get(),
            "pattern_size": self.gm.patterns_tab.pattern_size_var.get(),
            "click_while_pattern": self.gm.patterns_tab.click_while_pattern_var.get(),
            "interrupt_on_move": self.gm.patterns_tab.interrupt_on_move_var.get(),

            # Application settings
            "language": self.gm.model.language.get(),
            "theme": self.gm.style.theme.name,
            "hotkeys": self.gm.model.hotkeys.get_all_hotkeys(),
        }

        if self.gm.model.save_profile(profile_name, settings):
            self.gm.model.current_profile.set(profile_name)
            self.gm.update_status(events.PROFILE_SAVED, profile_name=profile_name)
            self.gm.top_bar.refresh_profile_list()
        else:
            self.gm.update_status(events.PROFILE_SAVE_ERROR)

    def load(self, profile_name: str):
        """Load profile and apply all settings"""
        if profile_name is None:
            self.gm.update_status(events.ERROR)
            return

        profile = self.gm.model.load_profile(profile_name)
        if not profile:
            self.gm.update_status(events.PROFILE_NOT_FOUND, profile_name=profile_name)
            return

        # Apply Main Tab Settings
        self.gm.main_tab.delay_var.set(profile.get("delay", 0.01))
        self.gm.main_tab.duration_var.set(profile.get("duration", 0))
        self.gm.main_tab.click_type_var.set(profile.get("click_type", "left"))
        self.gm.main_tab.repeat_var.set(profile.get("repeat", 1))
        self.gm.main_tab.random_delay_var.set(profile.get("random_delay", False))
        self.gm.main_tab.notify_var.set(profile.get("notify_when_done", False))

        # Apply Patterns Tab Settings
        self.gm.patterns_tab.pattern_var.set(profile.get("pattern", "none"))
        self.gm.patterns_tab.pattern_size_var.set(profile.get("pattern_size", 100))
        self.gm.patterns_tab.click_while_pattern_var.set(profile.get("click_while_pattern", False))
        self.gm.patterns_tab.interrupt_on_move_var.set(profile.get("interrupt_on_move", False))

        # Apply Language
        lang = profile.get("language")
        if lang and lang != self.gm.model.language.get():
            self.gm.model.language.set(lang)

        # Apply Theme
        theme = profile.get("theme")
        if theme and theme in self.gm.style.theme_names():
            self.gm._on_apply_theme(theme)

        # Register Hotkeys from profile
        self._register_hotkeys_from_profile(profile.get("hotkeys", {}))

        self.gm.settings_tab.update_hotkey_label()
        self.gm.update_all_hotkey_labels()
        self.gm.model.current_profile.set(profile_name)
        self.gm.update_status(events.PROFILE_LOADED, profile_name=profile_name)
        self.gm.top_bar.refresh_profile_list()

    def delete(self, profile_name: str):
        """Delete a profile"""
        if profile_name is None:
            self.gm.update_status(events.ERROR)
            return

        if self.gm.model.delete_profile(profile_name):
            self.gm.update_status(events.PROFILE_DELETED, profile_name=profile_name)
            self.gm.top_bar.refresh_profile_list()

            if self.gm.model.current_profile.get() == profile_name:
                self.gm.model.current_profile.set("Default")
                self.load("Default")
        else:
            self.gm.update_status(events.PROFILE_DELETE_ERROR)

    def _register_hotkeys_from_profile(self, hotkeys: dict):
        """Register hotkeys from profile settings using Model's callback registry"""
        if not hotkeys:
            return

        self.gm.model.hotkeys.cleanup()

        for name, key in hotkeys.items():
            # Use central callback registry from Model
            callback = self.gm.model.get_hotkey_callback(name)
            if callback:
                self.gm.model.hotkeys.register_hotkey(
                    name, key, callback, self.gm.model._on_hotkey_status
                )
