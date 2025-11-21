# autoclicker/gui/components/main_control_button.py
from ttkbootstrap.widgets import Frame, Label, Button


class MainControlButton:
    """
    Creates the main start button + status display.

    """

    @staticmethod
    def create(parent, on_toggle, manager, button_text_var, status_text_var):
        """
        Creates the UI for the main control area.

        Args:
            parent: The parent widget
            on_toggle: Callback function to execute on button click
            manager: GUIManager instance for translations
            button_text_var: StringVar for button text (required)
            status_text_var: StringVar for status label (required)
        """
        control_frame = Frame(parent)
        control_frame.pack(pady=20)

        start_button = Button(
            control_frame,
            textvariable=button_text_var,
            command=on_toggle,
            bootstyle="success",
            width=30,
            style="custom.TButton"
        )
        start_button.pack(pady=10)

        status_label = Label(
            control_frame,
            textvariable=status_text_var,
            font=("Segoe UI", 12, "bold"),
            bootstyle="secondary"
        )
        status_label.pack(pady=5)

        return control_frame, start_button, status_label