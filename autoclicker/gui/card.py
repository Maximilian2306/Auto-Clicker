# autoclicker/gui/card.py
import ttkbootstrap as ttkb
from ttkbootstrap.widgets import LabelFrame


class Card:
    """
    UI-component for creating modern card containers.
    """

    @staticmethod
    def create(parent, title: str, style: str = "default"):
        """Creates a 'card'-like section and returns the LabelFrame."""
        card = LabelFrame(
            parent,
            text=f"  {title}  ",
            padding=15,
            bootstyle=style,
            relief="flat"
        )
        card.pack(fill="x", pady=10, padx=5)
        return card
