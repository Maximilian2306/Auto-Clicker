# autoclicker/gui/components/card.py
import ttkbootstrap as ttkb
from ttkbootstrap.widgets import LabelFrame


class Card:
    """
    UI Card Factory - creates styled LabelFrame cards for UI sections.

    """

    @staticmethod
    def create(
        parent,
        title: str,
        style: str = "default",
        geometry: str = "pack",
        **layout_options
    ):
        """
        Implements a Card and applies layout.

        Parameter:
        ----------
        parent : Widget => Parent-Widget
        title : str => Headertitle 
        style : str => ttkbootstrap style
        geometry : str => Layout mode (Pack or Grid)
        **layout_options : More layout options like padx, pady, row, column, etc.
        """
        card = LabelFrame(
            parent,
            text=f"  {title}  ",
            padding=15,
            bootstyle=style,
            relief="solid",
        )

        geometry = geometry.lower().strip()

        if geometry == "grid":
            card.grid(**layout_options)
        elif geometry == "pack":
            card.pack(**layout_options)
        else:
            raise ValueError(
                f"Invalid geometry '{geometry}'. Use 'pack' or 'grid'."
            )

        return card
