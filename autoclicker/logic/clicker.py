# autoclicker/logic/clicker.py
"""Clicker Logic - Auto-clicking and mouse pattern movements"""

import pyautogui
import time
import threading
import math
import random
from threading import Event
from typing import Optional, Callable

from ..events import (CLICKER_STARTED, CLICKER_STOPPED, CLICKER_COMPLETED, CLICKER_PAUSED, CLICKER_RESUMED, CLICKER_WAITING)

pyautogui.FAILSAFE = True  # Failsafe activated (upper-left corner)
pyautogui.PAUSE = 0  # No delays between actions


class Clicker:
    """Manages auto-clicking functionality with thread-safe operations"""

    def __init__(self):
        self.stop_event = Event()
        self.stop_event.set()
        self.session_start = None
        self.clicking_thread = None
        self.total_clicks = 0
        self._clicks_lock = threading.Lock()
        self._notify_callback: Optional[Callable[[str], None]] = None  

    def toggle_clicker(
        self,
        delay: float,
        duration: int,
        fixed_x: Optional[int],
        fixed_y: Optional[int],
        click_type: str,
        pattern: str,
        pattern_size: int,
        repeat: int,
        random_delay: bool,
        click_while_pattern: bool = False,
        on_status_changed: Callable[[str], None] = None,
        on_stats_updated: Callable[[int, float], None] = None,
        notify_when_done: bool = False,
        notify_callback: Optional[Callable[[str], None]] = None,
        interrupt_on_move: bool = False,
        button_bounds: Optional[tuple[int,int,int,int]] = None
    ) -> None:
        """Toggle auto-clicker on/off with the given configuration"""
        self._notify_callback = notify_callback  

        if self.stop_event.is_set():
            self.stop_event.clear()
            self.session_start = time.time() # Start clicking
            with self._clicks_lock:
                self.total_clicks = 0
            on_status_changed(CLICKER_STARTED)

            self.clicking_thread = threading.Thread(
                target=self._click_loop,
                args=(
                    delay,
                    duration,
                    fixed_x,
                    fixed_y,
                    click_type,
                    pattern,
                    pattern_size,
                    repeat,
                    random_delay,
                    click_while_pattern,
                    on_status_changed,
                    on_stats_updated,
                    notify_when_done,  
                    interrupt_on_move,
                    button_bounds,
                ),
                daemon=True,
            )
            self.clicking_thread.start()
        else:
            self.stop_event.set() # Stop clicking
            on_status_changed(CLICKER_STOPPED)
            self.session_start = None

    def _click_loop(
        self,
        delay: float,
        duration: int,
        fixed_x: Optional[int],
        fixed_y: Optional[int],
        click_type: str,
        pattern: str,
        pattern_size: int,
        repeat: int,
        random_delay: bool,
        click_while_pattern: bool,
        on_status_changed: Callable[[str], None],
        on_stats_updated: Callable[[int, float], None],
        notify_when_done: bool = False,
        interrupt_on_move: bool = False,
        button_bounds: Optional[tuple[int,int,int,int]] = None
    ) -> None:
        """Main clicking loop running in separate thread"""
        # Wait for mouse to leave button area if needed
        if not self._wait_for_button_clear(button_bounds, on_status_changed):
            return

        start_time = time.time()
        last_stats_update = start_time

        # Initialize mouse tracking state
        mouse_state = {
            'last_user_pos': pyautogui.position(),
            'last_auto_pos': pyautogui.position(),
            'last_manual_move': 0,
            'is_paused': False,
            'last_status': None
        }

        while not self.stop_event.is_set():
            # Check for mouse interrupt in pattern mode
            pattern_mode = (pattern != "none") and interrupt_on_move
            if pattern_mode:
                should_continue, mouse_state = self._handle_mouse_interrupt(
                    mouse_state, on_status_changed
                )
                if not should_continue:
                    continue

            # Execute clicks based on mode
            if pattern != "none" and not click_while_pattern:
                # Pattern-only mode (no clicking)
                mouse_state['last_auto_pos'] = self._handle_pattern_only_mode(
                    pattern, pattern_size, repeat
                )
            else:
                # Normal clicking (with or without pattern)
                mouse_state['last_auto_pos'] = self._handle_clicking_mode(
                    pattern, pattern_size, repeat, click_while_pattern,
                    fixed_x, fixed_y, click_type
                )

                # Apply delay between click cycles
                if delay > 0:
                    actual_delay = delay * random.uniform(0.8, 1.2) if random_delay else delay
                    time.sleep(actual_delay)

                # Update stats periodically
                last_stats_update = self._update_stats_if_needed(
                    last_stats_update, on_stats_updated
                )

                # Check if duration limit reached
                if self._check_duration_complete(
                    duration, start_time, on_status_changed,
                    on_stats_updated, notify_when_done
                ):
                    break

    def _wait_for_button_clear(
        self,
        button_bounds: Optional[tuple[int, int, int, int]],
        on_status_changed: Callable[[str], None]
    ) -> bool:
        """Wait for mouse to leave button area. Returns False if stopped."""
        if not button_bounds:
            return True

        x1, y1, x2, y2 = button_bounds
        last_status = None

        while True:
            x, y = pyautogui.position()
            if not (x1 <= x <= x2 and y1 <= y <= y2):
                on_status_changed(CLICKER_RESUMED)
                return True
            if self.stop_event.is_set():
                return False
            if last_status != "waiting":
                on_status_changed(CLICKER_WAITING)
                last_status = "waiting"
            time.sleep(0.05)

    def _handle_mouse_interrupt(
        self,
        mouse_state: dict,
        on_status_changed: Callable[[str], None]
    ) -> tuple[bool, dict]:
        """Check for manual mouse movement, handle pause/resume. Returns (should_continue, state)."""
        current_pos = pyautogui.position()

        # Check if mouse moved manually (not by automation)
        if current_pos != mouse_state['last_user_pos']:
            if current_pos != mouse_state['last_auto_pos']:
                mouse_state['last_manual_move'] = time.time()
                mouse_state['is_paused'] = True

        # Auto-resume after 3 seconds of no manual movement
        if mouse_state['is_paused'] and (time.time() - mouse_state['last_manual_move'] > 3):
            mouse_state['is_paused'] = False

        mouse_state['last_user_pos'] = current_pos

        # Handle paused state
        if mouse_state['is_paused']:
            if mouse_state['last_status'] != "paused":
                on_status_changed(CLICKER_PAUSED)
                mouse_state['last_status'] = "paused"
            time.sleep(0.1)
            return False, mouse_state
        else:
            if mouse_state['last_status'] != "running":
                on_status_changed(CLICKER_RESUMED)
                mouse_state['last_status'] = "running"

        return True, mouse_state

    def _handle_pattern_only_mode(
        self,
        pattern: str,
        pattern_size: int,
        repeat: int
    ) -> tuple[int, int]:
        """Execute pattern movement without clicking. Returns last position."""
        last_pos = (0, 0)
        for _ in range(repeat):
            if self.stop_event.is_set():
                break
            last_pos = self._apply_pattern(pattern, pattern_size)
        return last_pos

    def _handle_clicking_mode(
        self,
        pattern: str,
        pattern_size: int,
        repeat: int,
        click_while_pattern: bool,
        fixed_x: Optional[int],
        fixed_y: Optional[int],
        click_type: str
    ) -> tuple[int, int]:
        """Execute clicking with optional pattern. Returns last position."""
        last_pos = pyautogui.position()

        for _ in range(repeat):
            if self.stop_event.is_set():
                break

            # Apply pattern if enabled
            if pattern != "none" and click_while_pattern:
                last_pos = self._apply_pattern(pattern, pattern_size)

            # Move to fixed position if specified
            if fixed_x is not None and fixed_y is not None:
                pyautogui.moveTo(fixed_x, fixed_y)

            # Perform click
            if click_type == "double":
                pyautogui.doubleClick()
            else:
                pyautogui.click(button=click_type)

            # Update click counter
            with self._clicks_lock:
                self.total_clicks += 1

        return last_pos

    def _update_stats_if_needed(
        self,
        last_stats_update: float,
        on_stats_updated: Callable[[int, float], None]
    ) -> float:
        """Update stats if 0.5s passed. Returns updated timestamp."""
        current_time = time.time()
        if current_time - last_stats_update >= 0.5:
            with self._clicks_lock:
                clicks_copy = self.total_clicks
            on_stats_updated(clicks_copy, self._calculate_click_rate())
            return current_time
        return last_stats_update

    def _check_duration_complete(
        self,
        duration: int,
        start_time: float,
        on_status_changed: Callable[[str], None],
        on_stats_updated: Callable[[int, float], None],
        notify_when_done: bool
    ) -> bool:
        """Check if duration reached. Returns True if should stop."""
        if duration > 0 and (time.time() - start_time) >= duration:
            self.stop_event.set()
            with self._clicks_lock:
                clicks_copy = self.total_clicks
            on_stats_updated(clicks_copy, self._calculate_click_rate())
            on_status_changed(CLICKER_COMPLETED)
            if notify_when_done and self._notify_callback:
                self._notify_callback(CLICKER_COMPLETED)
            return True
        return False


    def _apply_pattern(self, pattern: str, size: int) -> tuple[int, int]:
        """Apply movement pattern and return new position (x, y)"""
        screen_width, screen_height = pyautogui.size()
        center_x, center_y = screen_width // 2, screen_height // 2

        radius = size
        t = time.time()
        x, y = center_x, center_y

        # === Circle pattern ===
        if pattern == "circle":
            angle = t * 3.5  # Speed
            x = center_x + int(radius * math.cos(angle))
            y = center_y + int(radius * math.sin(angle))

        # === Eight pattern (figure eight) ===
        elif pattern == "eight":
            angle = t * 3
            a = radius
            denom = 1 + math.sin(angle) ** 2
            x = center_x + int(a * math.cos(angle) / denom)
            y = center_y + int(a * math.sin(angle) * math.cos(angle) / denom)

        # === Square pattern ===
        elif pattern == "square":
            side = radius
            perimeter = 4 * side
            progress = (t * 100) % perimeter

            if progress < side:  
                x = center_x - side//2 + int(progress)
                y = center_y - side//2
            elif progress < 2 * side:  
                x = center_x + side//2
                y = center_y - side//2 + int(progress - side)
            elif progress < 3 * side:  
                x = center_x + side//2 - int(progress - 2 * side)
                y = center_y + side//2
            else: 
                x = center_x - side//2
                y = center_y + side//2 - int(progress - 3 * side)

        # === Random pattern ===
        elif pattern == "random":
            x = center_x + random.randint(-radius, radius)
            y = center_y + random.randint(-radius, radius)

        # === Spiral pattern ===
        elif pattern == "spiral":
            angle = t * 3.5
            r = (radius * ((t * 0.2) % 2.2))  
            x = center_x + int(r * math.cos(angle))
            y = center_y + int(r * math.sin(angle))

        # === Line pattern ===
        elif pattern == "line":
            x = center_x + int(radius * math.sin(t * 2))
            y = center_y

        # === Zick-Zack ===
        elif pattern == "zigzag":
            x = center_x + int(radius * math.sin(t * 2))
            y = center_y + int(radius * 0.5 * math.cos(t * 3))

        # === Star pattern ===
        elif pattern == "star":
            x = center_x + int(radius * math.sin(t) * math.cos(t * 2.5))
            y = center_y + int(radius * math.cos(t) * math.sin(t * 2.5))

        # === Check screen sizes ===
        x = max(0, min(x, screen_width - 1))
        y = max(0, min(y, screen_height - 1))

        pyautogui.moveTo(x, y, duration=0)
        return (x, y)


    def _calculate_click_rate(self) -> float:
        """Calculate clicks per second (thread-safe)"""
        with self._clicks_lock:
            if not self.session_start:
                return 0.0
            elapsed = time.time() - self.session_start
            if elapsed > 0:
                return self.total_clicks / elapsed
        return 0.0

    def stop(self) -> None:
        """Stop the clicking thread"""
        self.stop_event.set()