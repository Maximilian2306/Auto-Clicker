# autoclicker/gui/stats_tab.py
"""
Statistics Tab - UI for session stats and monitoring

"""

import ttkbootstrap as ttkb
from ttkbootstrap.widgets import (Frame, Label, Button, Progressbar)
from ttkbootstrap.scrolled import ScrolledFrame
from tkinter import IntVar, StringVar
from typing import Callable

from .base_tab import BaseTab
from .card import Card


class StatsTab(BaseTab):
    """Tab for displaying session statistics and progress"""

    def __init__(
        self,
        parent,
        manager,
        on_export_stats: Callable[[], None],
        on_reset_stats: Callable[[], None],
    ):
        self.on_export_stats = on_export_stats
        self.on_reset_stats = on_reset_stats

        # === UI Variables ===
        self.progress_var = IntVar(value=0)
        self.progress_bar = None
        self.progress_label = None

        super().__init__(parent, manager)

    def _build_content(self):
        """Builds content"""
        scroll_frame = ScrolledFrame(self, autohide=True)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # === Live Statistics ===
        live_card = Card.create(scroll_frame, "Live Statistics", "info", geometry="pack", fill="x", pady=10)

        stats_grid = Frame(live_card)
        stats_grid.pack(fill="x", pady=10)

        # === Stat displays ===
        stats = [
            ("Session Time", self.manager.state["session_time"], "⏱️"),
            ("Total Clicks", self.manager.state["total_clicks"], "🧮"),
            ("Click Rate", self.manager.state["click_rate"], "📈"),
        ]

        for i, (label, var, icon) in enumerate(stats):
            stat_frame = Frame(stats_grid)
            stat_frame.grid(row=i // 2, column=i % 2, padx=20, pady=10, sticky="w") 

            Label(stat_frame, text=icon, font=("Segoe UI", 24)).pack(side="left", padx=5 )

            text_frame = Frame(stat_frame)
            text_frame.pack(side="left", padx=10)

            Label(text_frame, text=label, font=("Segoe UI", 9), foreground="gray").pack(anchor="w")

            Label(text_frame, textvariable=var, font=("Segoe UI", 14, "bold")).pack(anchor="w")


        # === Progress Visualization ===
        progress_card = Card.create(scroll_frame, "Session Progress", "success", geometry="pack", fill="x", pady=0)

        self.progress_var = IntVar(value=0)
        self.progress_bar = Progressbar(
            progress_card,
            variable=self.progress_var,
            maximum=100,
            bootstyle="success-striped",
            length=400,
        )
        self.progress_bar.pack(pady=10)

        self.progress_label = Label(progress_card, text="Ready to start", font=("Segoe UI", 10))
        self.progress_label.pack(pady=5)

        # === History/Log ===
        history_card = Card.create(scroll_frame, "Session History", "warning", geometry="pack", fill="x", pady=10)

        Button(
            history_card,
            text="📊 Export Statistics",
            command=self.on_export_stats,
            bootstyle="warning-outline",
        ).pack(pady=5)

        Button(
            history_card,
            text="🔄 Reset Statistics",
            command=self.on_reset_stats,
            bootstyle="danger-outline",
        ).pack(pady=5)

    def update_progress(self, value: int, text: str):
        """Update progress bar"""
        self.progress_var.set(value)
        self.progress_label.config(text=text)

        # Dynamic Color 
        if value < 20:
            style = "danger-striped"
        elif value < 60:
            style = "warning-striped"
        else:
            style = "success-striped"

        self.progress_bar.configure(bootstyle=style)