# autoclicker/utils/constants.py
"""
Centralized Constants - Single source of truth for magic strings and mappings

This module provides centralized constants to avoid hardcoded values
scattered throughout the codebase.
"""

# ============================================
# === LANGUAGE MAPPINGS ===
# ============================================

LANGUAGE_CODES = {
    "English": "en",
    "Deutsch": "de",
    "Español": "es",
    "Français": "fr",
    "中文": "zh",
}

LANGUAGE_DISPLAY_NAMES = {v: k for k, v in LANGUAGE_CODES.items()}

# List of available languages for UI dropdowns
AVAILABLE_LANGUAGES = list(LANGUAGE_CODES.keys())

# ============================================
# === HOTKEY MAPPINGS ===
# ============================================

# Map display names to internal names
HOTKEY_DISPLAY_TO_INTERNAL = {
    "Start/Stop": "toggle_clicker",
    "Exit Program": "exit_program",
    "Capture Position": "capture_coordinates",
    "Record Macro": "start_macro_recording",
    "Stop Macro": "stop_macro_recording",
    "Play Macro": "play_macro_recording",
}

# Reverse mapping
HOTKEY_INTERNAL_TO_DISPLAY = {v: k for k, v in HOTKEY_DISPLAY_TO_INTERNAL.items()}

# Default hotkey bindings
DEFAULT_HOTKEYS = {
    "toggle_clicker": "f6",
    "capture_coordinates": "f7",
    "exit_program": "esc",
    "start_macro_recording": "f3",
    "stop_macro_recording": "f4",
    "play_macro_recording": "f5",
}

# ============================================
# === CLICK PATTERNS ===
# ============================================

PATTERN_NAMES = [
    "none",
    "circle",
    "square",
    "spiral",
    "zigzag",
    "star",
    "eight",
    "random",
    "line",
]

# ============================================
# === CLICK BUTTONS ===
# ============================================

CLICK_BUTTONS = ["left", "right", "middle", "double"]

# ============================================
# === VALIDATION CONSTANTS ===
# ============================================

MAX_PROFILE_NAME_LENGTH = 100
MAX_MACRO_NAME_LENGTH = 100
MAX_DELAY_SECONDS = 60
MAX_PATTERN_SIZE = 1000
MIN_PATTERN_SIZE = 10
MAX_REPEAT_COUNT = 100

# ============================================
# === FILE PATHS ===
# ============================================

from pathlib import Path

PROFILES_FILE = Path.home() / ".autoclicker_profiles.json"
LAST_PROFILE_FILE = Path.home() / ".autoclicker_last_profile.json"
MACROS_DIR = Path.home() / ".autoclicker_macros"

# ============================================
# === UI CONSTANTS ===
# ============================================

DEFAULT_THEME = "cyborg"
DEFAULT_LANGUAGE = "English"

# Stats update interval in seconds
STATS_UPDATE_INTERVAL = 1

# Window dimensions
WINDOW_WIDTH_DEFAULT = 950
WINDOW_HEIGHT = 785
WINDOW_WIDTH_BY_LANGUAGE = {
    "English": 950,
    "Deutsch": 1050,
    "Español": 1000,
    "Français": 1000,
    "中文": 950,
}

# Animation timings (milliseconds)
TOAST_DURATION_MS = 1500
TOAST_DURATION_ERROR_MS = 2000
FADE_DURATION_MS = 150
