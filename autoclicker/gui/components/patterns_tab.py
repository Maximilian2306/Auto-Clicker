# autoclicker/gui/patterns_tab.py
"""
Patterns & Macros Tab - UI for click patterns and macro recording

"""

import ttkbootstrap as ttkb
from ttkbootstrap.widgets import (Frame, Label, Button, Radiobutton, Scale, Checkbutton)
from ttkbootstrap.scrolled import ScrolledFrame
from tkinter import StringVar, IntVar, BooleanVar
from typing import Callable

from .base_tab import BaseTab
from .card import Card


class PatternsTab(BaseTab):
    """Tab for click patterns and macro recording"""

    def __init__(
        self,
        parent,
        manager,
        on_record_macro: Callable[[], None],
        on_stop_macro: Callable[[], None],
        on_play_macro: Callable[[], None],
    ):
        """
        Initialize PatternsTab with pattern controls and macro recording

        Args:
            parent: Parent Tkinter widget
            manager: GUIManager instance for accessing shared state
            on_record_macro: Callback function to start macro recording
            on_stop_macro: Callback function to stop macro recording
            on_play_macro: Callback function to playback recorded macro
        """
        self.on_record_macro = on_record_macro
        self.on_stop_macro = on_stop_macro
        self.on_play_macro = on_play_macro

        # === UI Variables ===
        self.pattern_var = StringVar(value="none")
        self.pattern_size_var = IntVar(value=100)
        self.click_while_pattern_var = BooleanVar(value=False)
        self.interrupt_on_move_var = BooleanVar(value=False)

        # === Dynamic UI State Variables (only for elements that change during runtime) ===
        self.pattern_size_label_var = StringVar(value=f"100 {manager.t('pattern_size_px')}")
        self.macro_status_var = StringVar(value=manager.t('no_macro_recorded'))

        self.size_label = None
        self.macro_status = None
        self.record_button = None
        self.stop_button = None
        self.play_button = None

        # Store pattern radio buttons and description labels for translation updates
        self.pattern_radios = []  # List of (radio_button, pattern_key, desc_label)
        self.behavior_radios = []  # List of (radio_button, mode_key, desc_label)

        super().__init__(parent, manager)

        # === MVC-REFACTOR: Auto-update pattern size label when size changes ===
        self.pattern_size_var.trace_add("write", self._on_pattern_size_changed)

    def _build_content(self) -> None:
        """
        Build the patterns tab UI content with pattern selection and macro controls

        Creates pattern options, behavior settings, pattern size controls, and macro buttons
        """
        scroll_frame = ScrolledFrame(self, autohide=True)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # === Pattern Layout (Grid) ===
        patterns_section = Frame(scroll_frame)
        patterns_section.pack(fill="x", pady=10)

        # === Grid-configuration ===
        patterns_section.columnconfigure(0, weight=1, uniform="col")
        patterns_section.columnconfigure(1, weight=1, uniform="col")
        patterns_section.rowconfigure(0, weight=1)

        # === Left column (Pattern Selection) ===
        self.pattern_card = Card.create(patterns_section, f"  {self._t('click_patterns')}  ", "danger", geometry="grid", row=0, column=0, sticky="nsew", padx=(0, 10))
        pattern_card = self.pattern_card

        # Pattern definitions: (translation_key_prefix, value)
        patterns = [
            ("pattern_none", "none"),
            ("pattern_circle", "circle"),
            ("pattern_figure8", "eight"),
            ("pattern_square", "square"),
            ("pattern_star", "star"),
            ("pattern_zigzag", "zigzag"),
            ("pattern_random", "random"),
            ("pattern_spiral", "spiral"),
            ("pattern_line", "line"),
        ]

        for pattern_key, value in patterns:
            pattern_frame = Frame(pattern_card)
            pattern_frame.pack(fill="x", pady=2)

            rb = Radiobutton(
                pattern_frame,
                text=self._t(pattern_key),
                variable=self.pattern_var,
                value=value,
                bootstyle="danger-outline-toolbutton",
            )
            rb.pack(side="left", padx=5)

            desc_label = Label(
                pattern_frame,
                text=f"- {self._t(pattern_key + '_desc')}",
                font=("Segoe UI", 9),
                foreground="gray",
            )
            desc_label.pack(side="left", padx=10)

            # Store for translation updates
            self.pattern_radios.append((rb, pattern_key, desc_label))

        # === Right column (Behavior & Settings) ===
        right_column = Frame(patterns_section)
        right_column.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        # === Pattern Behavior ===
        self.behavior_card = Card.create(right_column, f"  {self._t('pattern_behavior')}  ", "info", geometry="pack", fill="x", pady=(0, 10))
        click_pattern_card = self.behavior_card

        self.pattern_interaction_label = Label(
            click_pattern_card,
            text=self._t('pattern_interaction'),
            font=("Segoe UI", 9),
            foreground="gray",
        )
        self.pattern_interaction_label.pack(anchor="w", pady=5)

        behavior_frame = Frame(click_pattern_card)
        behavior_frame.pack(fill="x", pady=5)

        # Pattern mode definitions: (translation_key_prefix, value)
        pattern_modes = [
            ("only_move", False),
            ("click_and_move", True),
        ]

        for mode_key, value in pattern_modes:
            mode_frame = Frame(behavior_frame)
            mode_frame.pack(fill="x", pady=5, padx=10)

            rb = Radiobutton(
                mode_frame,
                text=self._t(mode_key),
                variable=self.click_while_pattern_var,
                value=value,
                bootstyle="info-outline-toolbutton",
            )
            rb.pack(side="left", padx=5)

            desc_label = Label(
                mode_frame,
                text=f"({self._t(mode_key + '_desc')})",
                font=("Segoe UI", 8),
                foreground="gray",
            )
            desc_label.pack(side="left", padx=10)

            # Store for translation updates
            self.behavior_radios.append((rb, mode_key, desc_label))

        # === Pattern Settings ===
        self.settings_card = Card.create(right_column, f"  {self._t('pattern_settings')}  ", "secondary", geometry="pack", fill="x", pady=(0, 10))
        settings_card = self.settings_card

        self.pattern_size_label = Label(settings_card, text=f"📏 {self._t('pattern_size')}:")
        self.pattern_size_label.pack(anchor="w", pady=5)
        size_frame = Frame(settings_card)
        size_frame.pack(fill="x", pady=5)

        size_slider = Scale(
            size_frame,
            from_=10,
            to=500,
            variable=self.pattern_size_var,
            bootstyle="secondary",
            orient="horizontal",
            length=300,
        )
        size_slider.pack(side="left", padx=5)

        self.size_label = Label(size_frame, textvariable=self.pattern_size_label_var)
        self.size_label.pack(side="left", padx=10)

        self.pause_on_move_check = Checkbutton(
            settings_card,
            text=f"⏸ {self._t('pause_on_move')}",
            variable=self.interrupt_on_move_var,
            bootstyle="warning-round-toggle"
        )
        self.pause_on_move_check.pack(side="left", padx=5, pady=(35, 15))

        # === Macro Recording ===
        self.macro_card = Card.create(scroll_frame, f"  {self._t('macro_recording')}  ", "primary", geometry="pack", fill="x", pady=0)
        macro_card = self.macro_card

        macro_buttons = Frame(macro_card)
        macro_buttons.pack(pady=10)

        self.record_button = Button(
            macro_buttons,
            text=f"⏺️ {self._t('macro_record')}",
            command=self.on_record_macro,
            bootstyle="danger",
            width=16,
        )
        self.record_button.pack(side="left", padx=5)

        self.stop_button = Button(
            macro_buttons,
            text=f"⏸️ {self._t('macro_stop')}",
            command=self.on_stop_macro,
            bootstyle="warning",
            width=16,
        )
        self.stop_button.pack(side="left", padx=5)

        self.play_button = Button(
            macro_buttons,
            text=f"▶️ {self._t('macro_play')}",
            command=self.on_play_macro,
            bootstyle="success",
            width=16,
        )
        self.play_button.pack(side="left", padx=5)

        self.macro_status = Label(
            macro_card,
            textvariable=self.macro_status_var,
            font=("Segoe UI", 9),
            foreground="gray",
        )
        self.macro_status.pack(pady=5)

    def _on_pattern_size_changed(self, *args):
        """
        Internal callback when pattern_size_var changes (MVC-REFACTOR)

        Updates pattern size label automatically via StringVar.
        Called by trace_add() registered in __init__.

        Args:
            *args: Tkinter trace callback arguments (unused)
        """
        try:
            self.pattern_size_label_var.set(f"{self.pattern_size_var.get()} {self._t('pattern_size_px')}")
        except Exception:
            pass

    def update_macro_status(self, text: str) -> None:
        """
        Update the macro status label with current recording/playback state

        Args:
            text: Status message to display
        """
        self.macro_status_var.set(text)

    def update_hotkey_labels(self, record_key: str = "F3", stop_key: str = "F4", play_key: str = "F5") -> None:
        """
        Update macro button labels with hotkey bindings

        Args:
            record_key: Hotkey for record button (default: F3)
            stop_key: Hotkey for stop button (default: F4)
            play_key: Hotkey for play button (default: F5)
        """
        try:
            self.record_button.config(text=f"⏺️ {self._t('macro_record')} ({record_key.upper()})")
            self.stop_button.config(text=f"⏸️ {self._t('macro_stop')} ({stop_key.upper()})")
            self.play_button.config(text=f"▶️ {self._t('macro_play')} ({play_key.upper()})")
        except Exception:
            pass

    def refresh_translations(self):
        """Refresh all translatable UI elements when language changes"""
        # Update card titles
        if hasattr(self, 'pattern_card'):
            self.pattern_card.config(text=f"  {self._t('click_patterns')}  ")

        if hasattr(self, 'behavior_card'):
            self.behavior_card.config(text=f"  {self._t('pattern_behavior')}  ")

        if hasattr(self, 'settings_card'):
            self.settings_card.config(text=f"  {self._t('pattern_settings')}  ")

        if hasattr(self, 'macro_card'):
            self.macro_card.config(text=f"  {self._t('macro_recording')}  ")

        # Update pattern radio buttons and descriptions
        if hasattr(self, 'pattern_radios'):
            for rb, pattern_key, desc_label in self.pattern_radios:
                rb.config(text=self._t(pattern_key))
                desc_label.config(text=f"- {self._t(pattern_key + '_desc')}")

        # Update behavior radio buttons and descriptions
        if hasattr(self, 'behavior_radios'):
            for rb, mode_key, desc_label in self.behavior_radios:
                rb.config(text=self._t(mode_key))
                desc_label.config(text=f"({self._t(mode_key + '_desc')})")

        # Update pattern interaction label
        if hasattr(self, 'pattern_interaction_label'):
            self.pattern_interaction_label.config(text=self._t('pattern_interaction'))

        # Update pattern size label
        if hasattr(self, 'pattern_size_label'):
            self.pattern_size_label.config(text=f"📏 {self._t('pattern_size')}:")

        # MVC-REFACTOR: OLD CODE (direct widget manipulation)
        # if hasattr(self, 'size_label'):
        #     self.size_label.config(text=f"{self.pattern_size_var.get()} {self._t('pattern_size_px')}")

        # MVC-REFACTOR: NEW CODE (uses StringVar)
        # Update size label with current value via StringVar
        if hasattr(self, 'pattern_size_label_var'):
            self.pattern_size_label_var.set(f"{self.pattern_size_var.get()} {self._t('pattern_size_px')}")

        # Update pause on move checkbutton
        if hasattr(self, 'pause_on_move_check'):
            self.pause_on_move_check.config(text=f"⏸ {self._t('pause_on_move')}")

        # Update macro buttons with hotkeys
        self.update_hotkey_labels()

        # Update macro status - only if showing "no macro" state
        if hasattr(self, 'macro_status_var'):
            current = self.macro_status_var.get()
            if 'no macro' in current.lower() or 'kein makro' in current.lower():
                self.macro_status_var.set(self._t('no_macro_recorded'))