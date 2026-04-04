from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Label, Static


class TypingArea(Widget):
    DEFAULT_CLASSES = "text_area"

    def compose(self) -> ComposeResult:
        yield Label("fasfa vfadaf asa wqwq xczxa" * 200, classes="multiline gray")
