# autoclicker/gui/main_control_button.py
import ttkbootstrap as ttkb
from ttkbootstrap.widgets import Frame, Label, Button


class MainControlButton:
    """
    Creates the main start button + status display.

    """

    @staticmethod
    def create(parent, on_toggle):
        """
        Creates the UI for the main control area.

        Args:
            parent: The parent widget (usually a Tab or Frame)
            on_toggle: Callback function to execute on button click
        """
        control_frame = Frame(parent)
        control_frame.pack(pady=20)

        start_button = Button(
            control_frame,
            text="▶️  START CLICKING",
            command=on_toggle,
            bootstyle="success",
            width=30,
            style="custom.TButton"
        )
        start_button.pack(pady=10)

        # === State label ===
        status_label = Label(
            control_frame,
            text="⚪ READY",
            font=("Segoe UI", 12, "bold"),
            bootstyle="secondary"
        )
        status_label.pack(pady=5)

        return control_frame, start_button, status_label