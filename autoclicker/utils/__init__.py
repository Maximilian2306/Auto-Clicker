# autoclicker/utils/__init__.py
"""
Utils Package - Utilities not tied to GUI or Logic
"""

from .theme import ThemeManager
from .show_notification import NotificationManager
from .translation import TranslationManager
# UNUSED - Phase 4.4: AnimationManager not used anywhere (placeholder code only)
# from .apply_animations import AnimationManager

__all__ = [
    "ThemeManager",
    "NotificationManager",
    "TranslationManager",
    # "AnimationManager",  # UNUSED
]