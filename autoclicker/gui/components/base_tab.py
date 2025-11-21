# autoclicker/gui/components/base_tab.py
"""
Base classes for GUI components

Provides standardized base classes for tabs and other UI components
to ensure consistent structure, parameter order, and method naming.
"""

import ttkbootstrap as ttkb
from ttkbootstrap.widgets import Frame


class BaseComponent:
    """Base class for non-tab UI components (TopBar, StatusBar, etc.)"""

    def __init__(self, parent, manager):
        """Initialize base component with parent widget and manager"""
        self.parent = parent
        self.manager = manager
        self._build_content()

    def _build_content(self):
        """Build the component's UI content - must be overridden by subclasses"""
        raise NotImplementedError("Subclasses must implement _build_content()")

    def _t(self, key: str) -> str:
        """Get translated text for key"""
        return self.manager.t(key)

    def refresh_translations(self):
        """Refresh all translatable UI elements when language changes"""
        pass


class BaseTab(ttkb.Frame):
    """Base class for all tabs - provides access to GUIManager"""

    def __init__(self, parent, manager):
        """Initialize base tab with parent widget and manager"""
        super().__init__(parent)
        self.manager = manager
        self._build_content()

    def _build_content(self):
        """Builds content"""
        raise NotImplementedError("Subclasses must implement _build_content()")

    def _t(self, key: str) -> str:
        """Get translated text for key"""
        return self.manager.t(key)