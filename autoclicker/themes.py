from tkinter import ttk

def toggle_theme(style):
    if style.theme_use() == "clam":
        style.theme_use("alt")  # different mode
    else:
        style.theme_use("clam")  # different mode
