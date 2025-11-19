# autoclicker/logic/stats.py
"""
Statistics Logic - Session tracking und reporting

"""

import threading
import time
from typing import Callable, Optional
from datetime import datetime
from pathlib import Path


class Stats:
    """Manages session statistics and reporting"""

    def __init__(self):
        self.session_start = None
        self.total_clicks = 0
        self.stats_thread = None
        self.stop_stats_thread = False

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

        self.stop_stats_thread = False

        def update_loop():
            while not self.stop_stats_thread:
                if self.session_start:
                    current_clicks = total_clicks_getter()
                    self.update_stats(current_clicks, on_stats_changed)
                time.sleep(1)

        self.stats_thread = threading.Thread(target=update_loop, daemon=True)
        self.stats_thread.start()

    def stop_background_updater(self):
        """Stop background stats updater"""
        self.stop_stats_thread = True

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
    ) -> bool:
        """Export statistics to file"""

        try:
            with open(filename, "w") as f:
                f.write("Auto-Clicker Statistics\n")
                f.write("=" * 40 + "\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Clicks: {total_clicks}\n")
                f.write(f"Session Time: {session_time_str}\n")
                f.write(f"Click Rate: {click_rate_str}\n")
                f.write(f"Profile Used: {profile_name}\n")
            return True
        except Exception as e:
            print(f"Error exporting stats: {e}")
            return False

