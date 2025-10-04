import threading
import keyboard
import mouse
import time
import ttkbootstrap as ttkb
from ttkbootstrap import Style
from ttkbootstrap import Window, StringVar, BooleanVar
from ttkbootstrap.widgets import Frame, Label, Entry, Button, Checkbutton, Radiobutton, LabelFrame
from ttkbootstrap.constants import *

from .themes import toggle_theme
from .utils import update_status

# from . import logic_pyautogui, logic_sendinput
from . import logic_pyautogui


class AutoClickerGUI:
    def __init__(self) -> None:
        self.root = Window(themename="flatly")
        self.root.title("Auto-Clicker")
        self.root.geometry("600x500")
        self.root.resizable(True, True)

        self.style: Style = Style("flatly") # light

        # Thread Stop-Event
        self.stop_event: threading.Event = threading.Event()

        # UI 
        self._build_ui()

        # Hotkeys global
        keyboard.add_hotkey("f6", self.toggle_clicker)
        keyboard.add_hotkey("esc", self.root.quit)

    def _build_ui(self) -> None:
        main_frame = Frame(self.root, padding=20)
        main_frame.pack(fill="both", expand=True)

        # ---------------- Einstellungen ----------------
        settings_frame = LabelFrame(main_frame, text=" Settings ", padding=10)
        settings_frame.pack(fill="x", pady=10)

        Label(settings_frame, text="Click-Delay (Seconds):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.delay_entry = Entry(settings_frame, width=10)
        self.delay_entry.insert(0, "0.1")
        self.delay_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(settings_frame, text="Loop (Seconds, 0 = infinite):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.duration_entry = Entry(settings_frame, width=10)
        self.duration_entry.insert(0, "0")
        self.duration_entry.grid(row=1, column=1, padx=5, pady=5)

        self.follow_8_var = BooleanVar() # tk.BooleanVar()
        Checkbutton(settings_frame, text="Mouse follows '8' loop", variable=self.follow_8_var).grid(
            row=2, column=0, columnspan=2, sticky="w", padx=5, pady=5
        )

        # Checkbox für SendInput
        # Checkbutton(settings_frame, text="Direkte SendInput-Clicks verwenden", variable=self.use_sendinput).grid(
        #     row=3, column=0, columnspan=2, sticky="w", padx=5, pady=5
        # )

        # ---------------- Klickoptionen ----------------
        click_frame = LabelFrame(main_frame, text=" Click Options ", padding=10)
        click_frame.pack(fill="x", pady=10)

        Label(click_frame, text="Fixed X coordinate:").grid(row=0, column=0, padx=5, pady=5)
        self.x_entry = Entry(click_frame, width=10)
        self.x_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(click_frame, text="Fixed Y coordinate:").grid(row=1, column=0, padx=5, pady=5)
        self.y_entry = Entry(click_frame, width=10)
        self.y_entry.grid(row=1, column=1, padx=5, pady=5)

        # Button to find coordinates
        Button(
            click_frame,
            text="Find Coordinates",
            bootstyle="info-outline",
            command=self.capture_coordinates
        ).grid(row=0, column=2, columnspan=2, pady=5)

        self.click_type_var = StringVar(value="left") # tk.StringVar(value="left")
        Radiobutton(click_frame, text="Leftclick", variable=self.click_type_var, value="left").grid(
            row=3, column=0, padx=5, pady=5, sticky="w"
        )
        Radiobutton(click_frame, text="Rightclick", variable=self.click_type_var, value="right").grid(
            row=3, column=1, padx=5, pady=5, sticky="w"
        )

        # ---------------- Steuerung ----------------
        control_frame = LabelFrame(main_frame, text=" Cockpit ", padding=10)
        control_frame.pack(fill="x", pady=10)

        self.start_button = Button(control_frame, text="Start / Stop", command=self.toggle_clicker, bootstyle="success-outline")
        self.start_button.pack(pady=5)

        self.status_label = Label(
            control_frame,
            text="Status: STOP",
            font=("Segoe UI", 12, "bold"),
            bootstyle="danger"  # foreground="red"
        )
        self.status_label.pack(pady=5)

        # ---------------- Hotkey-Infos ----------------
        hotkey_frame = LabelFrame(main_frame, text=" Hotkeys ", padding=10)
        hotkey_frame.pack(fill="x", pady=10)

        Label(hotkey_frame, text="F6  → Start/Stop").pack(anchor="w", padx=5)
        Label(hotkey_frame, text="ESC → End").pack(anchor="w", padx=5)

        # ---------------- Theme-Umschalter ----------------
        Button(
            main_frame,
            text="Dark/Light Mode Switch",
            command= lambda: toggle_theme(self.style), # toggle_theme(self.style),
            bootstyle="secondary-outline"
        ).pack(pady=15)


    def toggle_clicker(self) -> None:
        if self.stop_event.is_set():  # If already stopped, restart
            self.stop_event.clear()
        else:
            self.stop_event.set()  # stop
            update_status(self.status_label, "STOP", "red")
            return

        try:
            delay: float = float(self.delay_entry.get())
        except ValueError:
            delay = 0.1

        try:
            duration: float = float(self.duration_entry.get())
        except ValueError:
            duration = 0

        follow_8: bool = self.follow_8_var.get()

        try:
            fx = int(self.x_entry.get())
            fy = int(self.y_entry.get())
            fixed_x, fixed_y = fx, fy
        except ValueError:
            fixed_x, fixed_y = None, None

        click_type: str = self.click_type_var.get()

        # save button coordinates
        bx1 = self.start_button.winfo_rootx()
        by1 = self.start_button.winfo_rooty()
        bx2 = bx1 + self.start_button.winfo_width()
        by2 = by1 + self.start_button.winfo_height()
        # logic.button_area = (bx1, by1, bx2, by2)

        # logic_module = logic_sendinput if self.use_sendinput.get() else logic_pyautogui
        logic_pyautogui.button_area = (bx1, by1, bx2, by2)

        # start thread
        self.stop_event.clear()
        threading.Thread(
            target=logic_pyautogui.auto_clicker,
            args=(delay, duration, follow_8, fixed_x, fixed_y, click_type, lambda t, c: update_status(self.status_label, t, c), self.stop_event),
            daemon=True
        ).start()
        update_status(self.status_label, "RUNNING", "green")


    def capture_coordinates(self):
        """Waits for the next mouse click and captures the coordinates."""
        update_status(self.status_label, "Waiting on mouse movement...", "orange")

        def wait_for_click():
            time.sleep(0.3)

            def on_click(event):
                if isinstance(event, mouse.ButtonEvent) and event.event_type == "down":
                    # x, y = event.x, event.y
                    x, y = mouse.get_position()
                    self.x_entry.delete(0, "end")
                    self.x_entry.insert(0, str(x))
                    self.y_entry.delete(0, "end")
                    self.y_entry.insert(0, str(y))

                    update_status(self.status_label, f"Koordinaten erfasst: {x}, {y}", "green")

                    mouse.unhook(on_click)

            mouse.hook(on_click)

        threading.Thread(target=wait_for_click, daemon=True).start()


    def run(self) -> None:
        self.root.mainloop()


