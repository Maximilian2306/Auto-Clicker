from ttkbootstrap import Style

LIGHT_THEME = "flatly"
DARK_THEME = "darkly"


def toggle_theme(style: Style) -> None:
    current_theme: str = style.theme.name

    if "dark" in current_theme:
        style.theme_use(LIGHT_THEME)  # hell
    else:
        style.theme_use(DARK_THEME)  # dunkel