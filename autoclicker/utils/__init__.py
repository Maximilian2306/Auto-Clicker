# autoclicker/utils/__init__.py
"""
Utils Package - Utilities not tied to GUI or Logic
"""

from .theme import ThemeManager
from .show_notification import NotificationManager
from .translation import TranslationManager
from .validators import validate_safe_filename, validate_profile_name, validate_macro_name
from .constants import (
    LANGUAGE_CODES,
    LANGUAGE_DISPLAY_NAMES,
    AVAILABLE_LANGUAGES,
    HOTKEY_DISPLAY_TO_INTERNAL,
    HOTKEY_INTERNAL_TO_DISPLAY,
    DEFAULT_HOTKEYS,
    PATTERN_NAMES,
    CLICK_BUTTONS,
    MAX_PROFILE_NAME_LENGTH,
    MAX_MACRO_NAME_LENGTH,
    PROFILES_FILE,
    LAST_PROFILE_FILE,
    MACROS_DIR,
    DEFAULT_THEME,
    DEFAULT_LANGUAGE,
)

__all__ = [
    "ThemeManager",
    "NotificationManager",
    "TranslationManager",
    # Validators
    "validate_safe_filename",
    "validate_profile_name",
    "validate_macro_name",
    # Constants
    "LANGUAGE_CODES",
    "LANGUAGE_DISPLAY_NAMES",
    "AVAILABLE_LANGUAGES",
    "HOTKEY_DISPLAY_TO_INTERNAL",
    "HOTKEY_INTERNAL_TO_DISPLAY",
    "DEFAULT_HOTKEYS",
    "PATTERN_NAMES",
    "CLICK_BUTTONS",
    "MAX_PROFILE_NAME_LENGTH",
    "MAX_MACRO_NAME_LENGTH",
    "PROFILES_FILE",
    "LAST_PROFILE_FILE",
    "MACROS_DIR",
    "DEFAULT_THEME",
    "DEFAULT_LANGUAGE",
]