# autoclicker/gui/base_tab.py
import ttkbootstrap as ttkb
from ttkbootstrap.widgets import Frame


class BaseTab(ttkb.Frame):
    """
    Base class for all tabs - provides access to GUIManager.
    Each tab inherits from this class and overrides _build_content().
    
    """

    def __init__(self, parent, manager):
        """
        Args:
            parent: The high-level widget (usually the Notebook)
            manager: Reference to GUIManager for access to global state
        """
        super().__init__(parent)
        self.manager = manager
        self._build_content()

    def _build_content(self):
        """Builds content"""
        raise NotImplementedError("Subclasses must implement _build_content()")

    def _t(self, key: str) -> str:
        """
        Shorthand for getting translated text via manager's translation service

        MVC-compliant: View → Controller (Manager) → Model
        This maintains clean separation of concerns.

        Args:
            key: Translation key

        Returns:
            Translated text
        """
        return self.manager.t(key)