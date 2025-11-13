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
        click_card = Card.create(top_frame, "Click Configuration", "primary", geometry="grid", row=0, column=0, sticky="nsew", padx=(10, 0))

        input_frame = Frame(click_card)
        input_frame.pack(fill="x", pady=10)

        # === Delay Slider ===
        Label(input_frame, text="⏱️ Click Delay:", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", padx=5)

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
        Label(input_frame, text="⏳ Duration:", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        duration_spin = Spinbox(
            input_frame,
            from_=0,
            to=3600,
            textvariable=self.duration_var,
            bootstyle="primary",
            width=10,
        )
        duration_spin.grid(row=1, column=1, padx=5, pady=5)
        Label(input_frame, text="seconds (0 = ∞)").grid(row=1, column=2, sticky="w")


        # === Advanced Click Options ===
        adv_card = Card.create(top_frame, "Advanced Click Options", "warning", geometry="grid", row=0, column=1, sticky="nsew", padx=(10, 0))

        rep_frame = Frame(adv_card)
        rep_frame.pack(fill="x", pady=5)

        Label(rep_frame, text="🔁 Repeat clicks:").pack(side="left", padx=5)
        self.repeat_var = IntVar(value=1)
        Spinbox(rep_frame, 
                from_=0,
                to=1000, 
                textvariable=self.repeat_var,
                width=10, 
                bootstyle="warning"
        ).pack(side="left", padx=5)
        Label(rep_frame, text="times per interval").pack(side="left")

        # === Random delay ===
        self.random_delay_var = BooleanVar(value=False)
        rand_frame = Frame(adv_card)
        rand_frame.pack(fill="x", pady=5)

        Checkbutton(rand_frame, 
                    text="🎲 Add random delay (±20%)",
                    variable=self.random_delay_var,
                    bootstyle="warning-round-toggle"
        ).pack(side="left", padx=5)

        # === Notify click option ===
        self.notify_var = BooleanVar(value=False)
        notify_frame = Frame(adv_card)
        notify_frame.pack(fill="x", pady=5)

        Checkbutton(
            notify_frame,
            text="🔔 Notify when done",
            variable=self.notify_var,
            bootstyle="warning-round-toggle"
        ).pack(side="left", padx=5)


        # === Click Type Selection ===
        click_type_frame = LabelFrame(
            scroll_frame, text=" Click Type ", padding=10, bootstyle="primary"
        )
        click_type_frame.pack(fill="x", padx=10, pady=(10,10))

        click_types = [
            ("🖱️ Left Click", "left"),
            ("🖱️ Right Click", "right"),
            ("🖱️ Middle Click", "middle"),
            ("🖱️ Double Click", "double"),
        ]

        for i, (text, value) in enumerate(click_types):
            Radiobutton(
                click_type_frame,
                text=text,
                variable=self.click_type_var,
                value=value,
                bootstyle="primary-outline-toolbutton",
            ).grid(row=0, column=i, padx=10, pady=5)

        # === Position Settings Card ===
        pos_card = Card.create(scroll_frame, "Position Settings", "info", geometry="pack", fill="x", pady=10, padx=10)

        pos_frame = Frame(pos_card)
        pos_frame.pack(fill="x", pady=10)

        Label(pos_frame, text="📍 Fixed Position:").grid(
            row=0, column=0, sticky="w", padx=5
        )

        coord_frame = Frame(pos_frame)
        coord_frame.grid(row=0, column=1, columnspan=3, padx=5)

        Label(coord_frame, text="X:").pack(side="left", padx=2)
        self.x_entry = Entry(coord_frame, width=8, bootstyle="info")
        self.x_entry.pack(side="left", padx=2)

        Label(coord_frame, text="Y:").pack(side="left", padx=5)
        self.y_entry = Entry(coord_frame, width=8, bootstyle="info")
        self.y_entry.pack(side="left", padx=2)

        Button(
            coord_frame,
            text="🎯 Capture",
            command=self.on_capture_coordinates,
            bootstyle="info",
            width=10,
        ).pack(side="left", padx=10)

        # === Main Control Button ===
        _, self.start_button, self.status_label = MainControlButton.create(
            parent=scroll_frame,
            on_toggle=self.on_toggle_clicker,
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