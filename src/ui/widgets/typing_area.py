from textual.app import ComposeResult
from textual.widgets import Label

from ui.widgets.base import BaseWidget


class TypingArea(BaseWidget):
    DEFAULT_CLASSES = "text_area"

    def compose(self) -> ComposeResult:
        yield Label("fasfa vfadaf asa wqwq xczxa" * 200, classes="multiline gray")
