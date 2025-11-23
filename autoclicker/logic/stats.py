# autoclicker/logic/stats.py
"""Statistics Logic - Session tracking and reporting"""

import threading
import time
from typing import Callable, Optional, Tuple
from datetime import datetime
from pathlib import Path
from enum import Enum


class ExportResult(Enum):
    """Result codes for stats export operation"""
    SUCCESS = "success"
    INVALID_PATH = "invalid_path"
    PERMISSION_DENIED = "permission_denied"
    WRITE_ERROR = "write_error"


class Stats:
    """Manages session statistics and reporting"""

    def __init__(self):
        self._lock = threading.Lock()
        self._session_start = None
        self._total_clicks = 0
        self.stats_thread = None
        self._stop_stats_thread = False
        self._stop_lock = threading.Lock()

    @property
    def session_start(self):
        with self._lock:
            return self._session_start

    @session_start.setter
    def session_start(self, value):
        with self._lock:
            self._session_start = value

    @property
    def total_clicks(self):
        with self._lock:
            return self._total_clicks

    @total_clicks.setter
    def total_clicks(self, value):
        with self._lock:
            self._total_clicks = value

    def start_session(self):
        """Start a new session"""
        self.session_start = time.time()
        self.total_clicks = 0

    def update_stats(
        self,
        total_clicks: int,
        on_stats_changed: Callable[[str, str, str], None],
    ):
        """Update statistics display"""

        if not self.session_start:
            return

        elapsed = time.time() - self.session_start
        hours, remainder = divmod(int(elapsed), 3600)
        minutes, seconds = divmod(remainder, 60)
        session_time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        click_rate = total_clicks / elapsed if elapsed > 0 else 0
        click_rate_str = f"{click_rate:.1f} clicks/s"

        on_stats_changed(session_time_str, click_rate_str, f"{total_clicks} clicks")

    def start_background_updater(
        self,
        total_clicks_getter: Callable[[], int],
        on_stats_changed: Callable[[str, str, str], None],
    ):
        """Start background thread for continuous stats updates"""

        with self._stop_lock:
            self._stop_stats_thread = False

        def update_loop():
            while True:
                with self._stop_lock:
                    if self._stop_stats_thread:
                        break
                if self.session_start:
                    current_clicks = total_clicks_getter()
                    self.update_stats(current_clicks, on_stats_changed)
                time.sleep(1)

        self.stats_thread = threading.Thread(target=update_loop, daemon=True)
        self.stats_thread.start()

    def stop_background_updater(self):
        """Stop background stats updater"""
        with self._stop_lock:
            self._stop_stats_thread = True

    def reset_stats(self):
        """Reset all statistics"""
        self.session_start = None
        self.total_clicks = 0

    def export_stats(
        self,
        filename: str,
        total_clicks: int,
        session_time_str: str,
        click_rate_str: str,
        profile_name: str,
    ) -> Tuple[ExportResult, str]:
        """Export statistics to file. Returns (ExportResult, message)."""
        path = Path(filename)

        # === Validate path ===
        if not path.parent.exists():
            return ExportResult.INVALID_PATH, f"Verzeichnis existiert nicht: {path.parent}"

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("ClickMAX Statistics\n")
                f.write("=" * 40 + "\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Clicks: {total_clicks}\n")
                f.write(f"Session Time: {session_time_str}\n")
                f.write(f"Click Rate: {click_rate_str}\n")
                f.write(f"Profile Used: {profile_name}\n")
            return ExportResult.SUCCESS, str(path)

        except PermissionError:
            return ExportResult.PERMISSION_DENIED, f"Keine Schreibberechtigung: {path}"
        except Exception as e:
            return ExportResult.WRITE_ERROR, str(e)

