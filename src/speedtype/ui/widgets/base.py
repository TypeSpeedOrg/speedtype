from textual.widget import Widget


class BaseWidget(Widget):
    def hide(self) -> None:
        self.styles.display = "none"

    def show(self) -> None:
        self.styles.display = "block"
