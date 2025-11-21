# autoclicker/gui/components/settings_tab.py
"""
Settings Tab - UI for application settings and profile management

"""

from ttkbootstrap.widgets import (Frame, Label, Button, Entry, Combobox)
from ttkbootstrap.scrolled import ScrolledFrame
from typing import Callable

from .base_tab import BaseTab
from .card import Card
from ...utils.constants import AVAILABLE_LANGUAGES


class SettingsTab(BaseTab):
    """Tab for application settings and profile management"""

    def __init__(
        self,
        parent,
        manager,
        on_save_profile: Callable[[str], None],
        on_load_profile: Callable[[str], None],
        on_delete_profile: Callable[[str], None],

        on_apply_theme: Callable[[str], None],
        available_themes: list[str],

        on_set_hotkey: Callable[[str, str], None],

        on_ask_string: Callable,
        on_get_profile_list: Callable[[], list[str]],
    ):
        """Initialize SettingsTab with language, theme, hotkey and profile settings"""
        self.on_save_profile = on_save_profile
        self.on_load_profile = on_load_profile
        self.on_delete_profile = on_delete_profile

        self.on_apply_theme = on_apply_theme
        self.available_themes = available_themes

        self.on_set_hotkey = on_set_hotkey

        self.on_ask_string = on_ask_string
        self.on_get_profile_list = on_get_profile_list

        # Widget references for refresh_translations
        self.profile_combo = None
        self.hotkey_entries = {}
        self.hotkey_labels = {}
        self.hotkey_set_buttons = {}

        super().__init__(parent, manager)

    def _build_content(self) -> None:
        """Build the settings tab UI with language, theme, hotkey and profile controls"""
        scroll_frame = ScrolledFrame(self, autohide=True)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # === Settings Layout (Grid) ===
        settings_section = Frame(scroll_frame)
        settings_section.pack(fill="x", pady=10)

        # === Grid-configuration (two) ===
        settings_section.columnconfigure(0, weight=1, uniform="col")
        settings_section.columnconfigure(1, weight=1, uniform="col")
        settings_section.rowconfigure(0, weight=1)
        settings_section.rowconfigure(1, weight=1)

        # === Left column stack (Language & Theme) ===
        left_column = Frame(settings_section)
        left_column.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # === Language Settings ===
        self.lang_card = Card.create(left_column, f"  {self._t('language_region')}  ", "primary", geometry="pack", fill="x", pady=(0, 10))
        lang_card = self.lang_card

        lang_frame = Frame(lang_card)
        lang_frame.pack(fill="x", pady=10)

        self.language_label = Label(lang_frame, text=f"🌍 {self._t('language')}:")
        self.language_label.pack(side="left", padx=5)
        lang_combo = Combobox(
            lang_frame,
            textvariable=self.manager.state["language"],
            values=AVAILABLE_LANGUAGES,
            width=15,
            bootstyle="primary",
        )
        lang_combo.pack(side="left", padx=5)

        # === Theme Settings ===
        self.theme_card = Card.create(left_column, f"  {self._t('appearance')}  ", "info", geometry="pack", fill="x", pady=(0, 10))
        theme_card = self.theme_card

        self.select_theme_label = Label(theme_card, text=f"🎨 {self._t('select_theme')}:")
        self.select_theme_label.pack(anchor="w", pady=5)

        theme_grid = Frame(theme_card)
        theme_grid.pack(fill="x", pady=10)

        for i, theme in enumerate(self.available_themes or []):
            btn = Button(
                theme_grid,
                text=theme.title(),
                command=lambda t=theme: self.on_apply_theme(t),
                bootstyle="info-outline",
                width=12,
            )
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)


        ###
        right_column = Frame(settings_section)
        right_column.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        ###

        # === Hotkey Settings ===
        self.hotkey_card = Card.create(right_column, f"  {self._t('hotkey_configuration')}  ", "warning", geometry="pack", fill="x", pady=(0, 10))
        hotkey_card = self.hotkey_card

        hotkeys = [
            ("Record Macro", "F3"),
            ("Stop Macro", "F4"),
            ("Play Macro", "F5"),
            ("Start/Stop", "F6"),
            ("Exit Program", "ESC"),
            ("Capture Position", "F7"),
        ]

        for name, default in hotkeys:
            hk_frame = Frame(hotkey_card)
            hk_frame.pack(fill="x", pady=5)

            label = Label(hk_frame, text=f"{name}:", width=15)
            label.pack(side="left", padx=5)
            self.hotkey_labels[name] = label

            entry = Entry(hk_frame, width=10, bootstyle="warning")
            entry.insert(0, default)
            entry.pack(side="left", padx=5)
            self.hotkey_entries[name] = entry

            set_button = Button(
                hk_frame,
                text=self._t('set_hotkey'),
                command=lambda e=entry, n=name: self.on_set_hotkey(n, e.get()),
                bootstyle="warning-outline",
                width=6,
            )
            set_button.pack(side="left", padx=5)
            self.hotkey_set_buttons[name] = set_button

        # === Profile Management ===
        self.profile_card = Card.create(right_column, f"  {self._t('profile_management')}  ", "success", geometry="pack", fill="x", pady=(0, 10))
        profile_card = self.profile_card

        profile_buttons = Frame(profile_card)
        profile_buttons.pack(pady=36.4)

        self.save_button = Button(
            profile_buttons,
            text=f"💾 {self._t('save')}",
            command=self._on_save_profile_dialog,
            bootstyle="success",
            width=12,
        )
        self.save_button.pack(side="left", padx=5)

        self.load_button = Button(
            profile_buttons,
            text=f"📁 {self._t('load')}",
            command=self._on_load_profile_dialog,
            bootstyle="primary",
            width=12,
        )
        self.load_button.pack(side="left", padx=5)

        self.delete_button = Button(
            profile_buttons,
            text=f"✕ {self._t('delete')}",
            command=self._on_delete_profile_dialog,
            bootstyle="danger",
            width=12,
        )
        self.delete_button.pack(side="left", padx=5)


    def update_hotkey_label(self) -> None:
        """Update hotkey entry fields to reflect currently configured hotkeys"""
        try:
            hotkeys = getattr(self.manager.model.hotkeys, "hotkeys", {})

            for name, entry in self.hotkey_entries.items():
                key_map = {
                    "Record Macro": "start_macro_recording",
                    "Stop Macro": "stop_macro_recording",
                    "Play Macro": "play_macro_recording",
                    "Start/Stop": "toggle_clicker",
                    "Exit Program": "exit_program",
                    "Capture Position": "capture_coordinates",
                }

                hotkey_name = key_map.get(name)
                if hotkey_name and hotkey_name in hotkeys:
                    entry.delete(0, "end")
                    entry.insert(0, hotkeys[hotkey_name])
        except Exception as e:
            print(f"[ERROR] update_hotkey_label failed: {e}")

    def _on_save_profile_dialog(self) -> None:
        """Show dialog to prompt user for profile name and save current settings"""
        profile_name = self.on_ask_string(
            title=self._t('save_profile_dialog_title'),
            prompt=self._t('save_profile_prompt'),
        )
        if profile_name:
            self.on_save_profile(profile_name)

    def _on_load_profile_dialog(self) -> None:
        """Show dialog to select and load a saved profile"""
        profiles = self.on_get_profile_list()
        if profiles:
            profile_name = self.on_ask_string(
                title=self._t('load_profile_dialog_title'),
                prompt=self._t('load_profile_prompt'),
                info_text=f"{self._t('available_profiles')} {', '.join(profiles)}",
            )
            if profile_name:
                self.on_load_profile(profile_name)
        else:
            self.on_load_profile(None)

    def _on_delete_profile_dialog(self) -> None:
        """Show dialog to select and delete a saved profile"""
        profiles = [p for p in self.on_get_profile_list() if p != "Default"]
        if profiles:
            profile_name = self.on_ask_string(
                title=self._t('delete_profile_dialog_title'),
                prompt=self._t('delete_profile_prompt'),
                info_text=f"{self._t('available_profiles')} {', '.join(profiles)}",
            )
            if profile_name:
                self.on_delete_profile(profile_name)
        else:
            self.on_delete_profile(None)

    def refresh_translations(self):
        """Refresh all translatable UI elements when language changes"""
        # Update card titles
        if hasattr(self, 'lang_card'):
            self.lang_card.config(text=f"  {self._t('language_region')}  ")

        if hasattr(self, 'theme_card'):
            self.theme_card.config(text=f"  {self._t('appearance')}  ")

        if hasattr(self, 'hotkey_card'):
            self.hotkey_card.config(text=f"  {self._t('hotkey_configuration')}  ")

        if hasattr(self, 'profile_card'):
            self.profile_card.config(text=f"  {self._t('profile_management')}  ")

        # Update language label
        if hasattr(self, 'language_label'):
            self.language_label.config(text=f"🌍 {self._t('language')}:")

        # Update theme label
        if hasattr(self, 'select_theme_label'):
            self.select_theme_label.config(text=f"🎨 {self._t('select_theme')}:")

        # Update hotkey labels
        hotkey_key_map = {
            "Record Macro": "hotkey_record_macro",
            "Stop Macro": "hotkey_stop_macro",
            "Play Macro": "hotkey_play_macro",
            "Start/Stop": "hotkey_start_stop",
            "Exit Program": "hotkey_exit_program",
            "Capture Position": "hotkey_capture_position",
        }
        for name, label in self.hotkey_labels.items():
            translation_key = hotkey_key_map.get(name)
            if translation_key:
                label.config(text=f"{self._t(translation_key)}:")

        # Update hotkey set buttons
        for button in self.hotkey_set_buttons.values():
            button.config(text=self._t('set_hotkey'))

        # Update profile management buttons
        if hasattr(self, 'save_button'):
            self.save_button.config(text=f"💾 {self._t('save')}")

        if hasattr(self, 'load_button'):
            self.load_button.config(text=f"📁 {self._t('load')}")

        if hasattr(self, 'delete_button'):
            self.delete_button.config(text=f"✕ {self._t('delete')}")
