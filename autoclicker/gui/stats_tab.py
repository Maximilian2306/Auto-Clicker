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
        """
        Initialize StatsTab with statistics display and export controls

        Args:
            parent: Parent Tkinter widget
            manager: GUIManager instance for accessing shared state
            on_export_stats: Callback function to export statistics to file
            on_reset_stats: Callback function to reset all statistics
        """
        self.on_export_stats = on_export_stats
        self.on_reset_stats = on_reset_stats

        # === UI Variables ===
        self.progress_var = IntVar(value=0)
        self.progress_bar = None
        self.progress_label = None

        super().__init__(parent, manager)

    def _build_content(self) -> None:
        """
        Build the statistics tab UI content with live stats and progress visualization

        Creates live statistics display, progress bar, and export/reset buttons
        """
        scroll_frame = ScrolledFrame(self, autohide=True)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # === Live Statistics ===
        self.live_card = Card.create(scroll_frame, f"  {self._t('live_statistics')}  ", "info", geometry="pack", fill="x", pady=10)
        live_card = self.live_card

        stats_grid = Frame(live_card)
        stats_grid.pack(fill="x", pady=10)

        # === Stat displays ===
        stats = [
            (self._t("session_time"), self.manager.state["session_time"], "⏱️"),
            (self._t("total_clicks"), self.manager.state["total_clicks"], "🧮"),
            (self._t("click_rate"), self.manager.state["click_rate"], "📈"),
        ]

        self.stat_labels = []
        for i, (label, var, icon) in enumerate(stats):
            stat_frame = Frame(stats_grid)
            stat_frame.grid(row=i // 2, column=i % 2, padx=20, pady=10, sticky="w")

            Label(stat_frame, text=icon, font=("Segoe UI", 24)).pack(side="left", padx=5)

            text_frame = Frame(stat_frame)
            text_frame.pack(side="left", padx=10)

            stat_label = Label(text_frame, text=label, font=("Segoe UI", 9), foreground="gray")
            stat_label.pack(anchor="w")
            self.stat_labels.append(stat_label)

            Label(text_frame, textvariable=var, font=("Segoe UI", 14, "bold")).pack(anchor="w")


        # === Progress Visualization ===
        self.progress_card = Card.create(scroll_frame, f"  {self._t('session_progress')}  ", "success", geometry="pack", fill="x", pady=0)
        progress_card = self.progress_card

        self.progress_var = IntVar(value=0)
        self.progress_bar = Progressbar(
            progress_card,
            variable=self.progress_var,
            maximum=100,
            bootstyle="success-striped",
            length=400,
        )
        self.progress_bar.pack(pady=10)

        self.progress_label = Label(progress_card, text=self._t('ready_to_start'), font=("Segoe UI", 10))
        self.progress_label.pack(pady=5)

        # === History/Log ===
        self.history_card = Card.create(scroll_frame, f"  {self._t('session_history')}  ", "warning", geometry="pack", fill="x", pady=10)
        history_card = self.history_card

        self.export_button = Button(
            history_card,
            text=f"📊 {self._t('export_statistics')}",
            command=self.on_export_stats,
            bootstyle="warning-outline",
        )
        self.export_button.pack(pady=5)

        self.reset_button = Button(
            history_card,
            text=f"🔄 {self._t('reset_statistics')}",
            command=self.on_reset_stats,
            bootstyle="danger-outline",
        )
        self.reset_button.pack(pady=5)

    def update_progress(self, value: int, text: str) -> None:
        """
        Update the progress bar with dynamic styling based on completion percentage

        Args:
            value: Progress percentage (0-100)
            text: Status text to display below progress bar
        """
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

    def refresh_translations(self):
        """Refresh all translatable UI elements when language changes"""
        # Update card titles
        if hasattr(self, 'live_card'):
            self.live_card.config(text=f"  {self._t('live_statistics')}  ")

        if hasattr(self, 'progress_card'):
            self.progress_card.config(text=f"  {self._t('session_progress')}  ")

        if hasattr(self, 'history_card'):
            self.history_card.config(text=f"  {self._t('session_history')}  ")

        # Update stat labels (session_time, total_clicks, click_rate)
        if hasattr(self, 'stat_labels') and len(self.stat_labels) == 3:
            self.stat_labels[0].config(text=self._t('session_time'))
            self.stat_labels[1].config(text=self._t('total_clicks'))
            self.stat_labels[2].config(text=self._t('click_rate'))

        # Update progress label if it's showing "ready_to_start"
        if hasattr(self, 'progress_label'):
            current = self.progress_label.cget('text')
            if 'ready' in current.lower() or 'bereit' in current.lower():
                self.progress_label.config(text=self._t('ready_to_start'))

        # Update export button
        if hasattr(self, 'export_button'):
            self.export_button.config(text=f"📊 {self._t('export_statistics')}")

        # Update reset button
        if hasattr(self, 'reset_button'):
            self.reset_button.config(text=f"🔄 {self._t('reset_statistics')}")