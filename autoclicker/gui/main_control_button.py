# autoclicker/gui/main_control_button.py
import ttkbootstrap as ttkb
from ttkbootstrap.widgets import Frame, Label, Button


class MainControlButton:
    """
    Creates the main start button + status display.

    """

    @staticmethod
    def create(parent, on_toggle, manager, button_text_var=None, status_text_var=None):
        """
        Creates the UI for the main control area.

        Args:
            parent: The parent widget (usually a Tab or Frame)
            on_toggle: Callback function to execute on button click
            manager: GUIManager instance for translations
            button_text_var: StringVar for button text (MVC-REFACTOR, optional for compatibility)
            status_text_var: StringVar for status label (MVC-REFACTOR, optional for compatibility)
        """
        def _t(key: str) -> str:
            """Get translated text via manager's translation service"""
            return manager.t(key)

        control_frame = Frame(parent)
        control_frame.pack(pady=20)

        # MVC-REFACTOR: OLD CODE (static text)
        # start_button = Button(
        #     control_frame,
        #     text=f"▶️  {_t('start_clicking')}",
        #     command=on_toggle,
        #     bootstyle="success",
        #     width=30,
        #     style="custom.TButton"
        # )

        # MVC-REFACTOR: NEW CODE (uses textvariable if provided, falls back to static text)
        if button_text_var:
            start_button = Button(
                control_frame,
                textvariable=button_text_var,
                command=on_toggle,
                bootstyle="success",
                width=30,
                style="custom.TButton"
            )
        else:
            # Fallback for compatibility during migration
            start_button = Button(
                control_frame,
                text=f"▶️  {_t('start_clicking')}",
                command=on_toggle,
                bootstyle="success",
                width=30,
                style="custom.TButton"
            )
        start_button.pack(pady=10)

        # MVC-REFACTOR: OLD CODE (static text)
        # status_label = Label(
        #     control_frame,
        #     text=f"⚪ {_t('ready').upper()}",
        #     font=("Segoe UI", 12, "bold"),
        #     bootstyle="secondary"
        # )

        # MVC-REFACTOR: NEW CODE (uses textvariable if provided, falls back to static text)
        if status_text_var:
            status_label = Label(
                control_frame,
                textvariable=status_text_var,
                font=("Segoe UI", 12, "bold"),
                bootstyle="secondary"
            )
        else:
            # Fallback for compatibility during migration
            status_label = Label(
                control_frame,
                text=f"⚪ {_t('ready').upper()}",
                font=("Segoe UI", 12, "bold"),
                bootstyle="secondary"
            )
        status_label.pack(pady=5)

        return control_frame, start_button, status_label