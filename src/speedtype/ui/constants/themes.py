from textual.theme import Theme


denim_theme = Theme(
    name="denim",
    primary=(primary := "#ffd43b"),
    foreground=(foreground := "#5f647a"),
    background=(background := "#1a1d36"),
    surface=(surface := "#101224"),
    accent="#6e081f",
    panel=background,
    variables={
        "footer-background": surface,
        "footer-foreground": foreground,
        "footer-key-foreground": primary,
        "scrollbar": primary,
        "scrollbar-hover": primary,
        "scrollbar-active": primary,
        "scrollbar-background": surface,
        "scrollbar-background-hover": surface,
        "scrollbar-background-active": surface,
    },
    dark=True,
)
