from tkinter import ttk


def update_status(label: ttk.Label, text: str, color: str) -> None:
    label.config(text=f"Status: {text}", foreground=color)
