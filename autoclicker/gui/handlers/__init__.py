# autoclicker/gui/handlers/__init__.py
"""
GUI Handlers - Event handlers and GUI logic

This package contains handlers that manage GUI events and coordinate
between UI components and the application model.
"""

from .profile_handler import ProfileHandler
from .status_handler import StatusHandler
from .utils import update_button_state

__all__ = [
    'ProfileHandler',
    'StatusHandler',
    'update_button_state',
]
