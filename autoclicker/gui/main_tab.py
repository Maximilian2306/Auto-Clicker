# autoclicker/gui/main_tab.py
"""
Main Controls Tab - UI for main clicker configuration and controls

"""

import ttkbootstrap as ttkb
from ttkbootstrap.widgets import (Frame, Label, Entry, Radiobutton, Checkbutton, LabelFrame, Scale, Spinbox, Button)
from ttkbootstrap.scrolled import ScrolledFrame
from tkinter import DoubleVar, IntVar, StringVar, BooleanVar
from typing import Callable, Optional

from .base_tab import BaseTab
from .main_control_button import MainControlButton
from .card import Card


class MainTab(BaseTab):
    """Tab for main clicker configuration and controls"""

    def __init__(
        self,
        parent,
        manager,
        on_toggle_clicker: Callable[[], None],
        on_capture_coordinates: Callable[[], None],
    ):
        """
        Initialize MainTab with clicker controls and configuration

        Args:
            parent: Parent Tkinter widget
            manager: GUIManager instance for accessing shared state
            on_toggle_clicker: Callback function to toggle clicker on/off
            on_capture_coordinates: Callback function to capture mouse coordinates
        """
        self.on_toggle_clicker = on_toggle_clicker
        self.on_capture_coordinates = on_capture_coordinates

        # === UI Variables ===
        self.delay_var = DoubleVar(value=0.01)
        self.duration_var = IntVar(value=0)
        self.click_type_var = StringVar(value="left")
        self.x_entry = None
        self.y_entry = None
        self.start_button = None
        self.status_label = None

        super().__init__(parent, manager)

    def _build_content(self) -> None:
        """
        Build the main tab UI content with all configuration controls

        Creates click settings, advanced options, position settings, and main control button
        """
        scroll_frame = ScrolledFrame(self, autohide=True)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # === Top Layout-Grid (Click & Advanced) ===
        top_frame = Frame(scroll_frame)
        top_frame.pack(fill="x", pady=10)

        top_frame.columnconfigure(0, weight=1)
        top_frame.columnconfigure(1, weight=1)

        # === Click Settings Card ===
        self.click_card = Card.create(top_frame, f"  {self._t('click_configuration')}  ", "primary", geometry="grid", row=0, column=0, sticky="nsew", padx=(10, 0))
        click_card = self.click_card

        input_frame = Frame(click_card)
        input_frame.pack(fill="x", pady=10)

        # === Delay Slider ===
        self.delay_label_text = Label(input_frame, text=f"⏱️ {self._t('click_delay')}:", font=("Segoe UI", 10))
        self.delay_label_text.grid(row=0, column=0, sticky="w", padx=5)

        delay_frame = Frame(input_frame)
        delay_frame.grid(row=0, column=1, columnspan=2, padx=5, sticky="ew")

        delay_slider = Scale(
            delay_frame,
            from_=0.0,
            to=5.0,
            variable=self.delay_var,
            bootstyle="primary",
            orient="horizontal",
            length=200,
        )
        delay_slider.pack(side="left", padx=5)

        self.delay_label = Label(delay_frame, text="0.01s")
        self.delay_label.pack(side="left", padx=5)
        delay_slider.configure(command=lambda v: self.delay_label.config(text=f"{float(v):.2f}s"))

        # === Duration Input ===
        self.duration_label_text = Label(input_frame, text=f"⏳ {self._t('duration')}:", font=("Segoe UI", 10))
        self.duration_label_text.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        duration_spin = Spinbox(
            input_frame,
            from_=0,
            to=3600,
            textvariable=self.duration_var,
            bootstyle="primary",
            width=10,
        )
        duration_spin.grid(row=1, column=1, padx=5, pady=5)
        self.seconds_infinite_label = Label(input_frame, text=self._t('seconds_zero_infinite'))
        self.seconds_infinite_label.grid(row=1, column=2, sticky="w")


        # === Advanced Click Options ===
        self.adv_card = Card.create(top_frame, f"  {self._t('advanced_click_options')}  ", "warning", geometry="grid", row=0, column=1, sticky="nsew", padx=(10, 0))
        adv_card = self.adv_card

        rep_frame = Frame(adv_card)
        rep_frame.pack(fill="x", pady=5)

        self.repeat_clicks_label = Label(rep_frame, text=f"🔁 {self._t('repeat_clicks')}:")
        self.repeat_clicks_label.pack(side="left", padx=5)
        self.repeat_var = IntVar(value=1)
        Spinbox(rep_frame,
                from_=0,
                to=1000,
                textvariable=self.repeat_var,
                width=10,
                bootstyle="warning"
        ).pack(side="left", padx=5)
        self.times_per_interval_label = Label(rep_frame, text=self._t('times_per_interval'))
        self.times_per_interval_label.pack(side="left")

        # === Random delay ===
        self.random_delay_var = BooleanVar(value=False)
        rand_frame = Frame(adv_card)
        rand_frame.pack(fill="x", pady=5)

        self.random_delay_check = Checkbutton(rand_frame,
                    text=f"🎲 {self._t('add_random_delay')}",
                    variable=self.random_delay_var,
                    bootstyle="warning-round-toggle"
        )
        self.random_delay_check.pack(side="left", padx=5)

        # === Notify click option ===
        self.notify_var = BooleanVar(value=False)
        notify_frame = Frame(adv_card)
        notify_frame.pack(fill="x", pady=5)

        self.notify_check = Checkbutton(
            notify_frame,
            text=f"🔔 {self._t('notify_when_done')}",
            variable=self.notify_var,
            bootstyle="warning-round-toggle"
        )
        self.notify_check.pack(side="left", padx=5)


        # === Click Type Selection ===
        self.click_type_frame = LabelFrame(
            scroll_frame, text=f" {self._t('click_type')} ", padding=10, bootstyle="primary"
        )
        self.click_type_frame.pack(fill="x", padx=10, pady=(10,10))

        click_types = [
            (f"🖱️ {self._t('left_click')}", "left"),
            (f"🖱️ {self._t('right_click')}", "right"),
            (f"🖱️ {self._t('middle_click')}", "middle"),
            (f"🖱️ {self._t('double_click')}", "double"),
        ]

        self.click_type_radios = []
        for i, (text, value) in enumerate(click_types):
            rb = Radiobutton(
                self.click_type_frame,
                text=text,
                variable=self.click_type_var,
                value=value,
                bootstyle="primary-outline-toolbutton",
            )
            rb.grid(row=0, column=i, padx=10, pady=5)
            self.click_type_radios.append((rb, value))

        # === Position Settings Card ===
        self.pos_card = Card.create(scroll_frame, f"  {self._t('position_settings')}  ", "info", geometry="pack", fill="x", pady=10, padx=10)
        pos_card = self.pos_card

        pos_frame = Frame(pos_card)
        pos_frame.pack(fill="x", pady=10)

        self.fixed_position_label = Label(pos_frame, text=f"📍 {self._t('fixed_position')}:")
        self.fixed_position_label.grid(row=0, column=0, sticky="w", padx=5)

        coord_frame = Frame(pos_frame)
        coord_frame.grid(row=0, column=1, columnspan=3, padx=5)

        self.x_coord_label = Label(coord_frame, text=self._t('x_label'))
        self.x_coord_label.pack(side="left", padx=2)
        self.x_entry = Entry(coord_frame, width=8, bootstyle="info")
        self.x_entry.pack(side="left", padx=2)

        self.y_coord_label = Label(coord_frame, text=self._t('y_label'))
        self.y_coord_label.pack(side="left", padx=5)
        self.y_entry = Entry(coord_frame, width=8, bootstyle="info")
        self.y_entry.pack(side="left", padx=2)

        self.capture_button = Button(
            coord_frame,
            text=f"🎯 {self._t('capture')}",
            command=self.on_capture_coordinates,
            bootstyle="info",
            width=10,
        )
        self.capture_button.pack(side="left", padx=10)

        # === Main Control Button ===
        _, self.start_button, self.status_label = MainControlButton.create(
            parent=scroll_frame,
            on_toggle=self.on_toggle_clicker,
            manager=self.manager,
        )

    def update_delay_label(self) -> None:
        """
        Update the delay label to reflect current delay value

        Called when loading a profile to sync the label with the slider value
        """
        try:
            self.delay_label.configure(text=f"{self.delay_var.get():.2f}s")
        except Exception:
            pass

    def refresh_translations(self):
        """Refresh all translatable UI elements when language changes"""
        # Update card titles
        if hasattr(self, 'click_card'):
            self.click_card.config(text=f"  {self._t('click_configuration')}  ")

        if hasattr(self, 'adv_card'):
            self.adv_card.config(text=f"  {self._t('advanced_click_options')}  ")

        if hasattr(self, 'pos_card'):
            self.pos_card.config(text=f"  {self._t('position_settings')}  ")

        # Update all labels with translations
        if hasattr(self, 'delay_label_text'):
            self.delay_label_text.config(text=f"⏱️ {self._t('click_delay')}:")

        if hasattr(self, 'duration_label_text'):
            self.duration_label_text.config(text=f"⏳ {self._t('duration')}:")

        if hasattr(self, 'seconds_infinite_label'):
            self.seconds_infinite_label.config(text=self._t('seconds_zero_infinite'))

        if hasattr(self, 'repeat_clicks_label'):
            self.repeat_clicks_label.config(text=f"🔁 {self._t('repeat_clicks')}:")

        if hasattr(self, 'times_per_interval_label'):
            self.times_per_interval_label.config(text=self._t('times_per_interval'))

        if hasattr(self, 'random_delay_check'):
            self.random_delay_check.config(text=f"🎲 {self._t('add_random_delay')}")

        if hasattr(self, 'notify_check'):
            self.notify_check.config(text=f"🔔 {self._t('notify_when_done')}")

        # Update click type LabelFrame
        if hasattr(self, 'click_type_frame'):
            self.click_type_frame.config(text=f" {self._t('click_type')} ")

        # Update radio buttons with emoji prefix
        if hasattr(self, 'click_type_radios'):
            click_types = ['left_click', 'right_click', 'middle_click', 'double_click']
            for i, (rb, value) in enumerate(self.click_type_radios):
                if i < len(click_types):
                    rb.config(text=f"🖱️ {self._t(click_types[i])}")

        if hasattr(self, 'fixed_position_label'):
            self.fixed_position_label.config(text=f"📍 {self._t('fixed_position')}:")

        if hasattr(self, 'x_coord_label'):
            self.x_coord_label.config(text=self._t('x_label'))

        if hasattr(self, 'y_coord_label'):
            self.y_coord_label.config(text=self._t('y_label'))

        if hasattr(self, 'capture_button'):
            self.capture_button.config(text=f"🎯 {self._t('capture')}")

        # Update main control button - check current state first
        if hasattr(self, 'start_button'):
            current_text = self.start_button.cget('text')
            if 'START' in current_text.upper() or 'STARTEN' in current_text.upper() or 'INICIAR' in current_text.upper() or 'DÉMARRER' in current_text.upper():
                self.start_button.config(text=f"▶️  {self._t('start_clicking')}")
            else:
                self.start_button.config(text=f"⏸️  {self._t('stop_clicking')}")

        # Update status label - only if showing READY state
        if hasattr(self, 'status_label'):
            current_status = self.status_label.cget('text')
            if 'READY' in current_status or 'BEREIT' in current_status or 'LISTO' in current_status or 'PRÊT' in current_status:
                self.status_label.config(text=f"⚪ {self._t('ready').upper()}")