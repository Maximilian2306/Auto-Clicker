# autoclicker/gui/card.py
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
        parent : Widget
            Elterncontainer
        title : str
            Überschrift der Card
        style : str
            ttkbootstrap-Stil (z. B. "primary", "info", "warning", ...)
        geometry : str
            Layout-Modus, "pack" oder "grid"
        **layout_options :
            Weitere Layout-Argumente, wie padx, pady, row, column, etc.

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
