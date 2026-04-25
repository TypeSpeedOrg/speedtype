from textual.app import ComposeResult
from textual.containers import Container

from speedtype.ui.widgets.base import BaseWidget


class InvalidCharsPlot(BaseWidget):
    def compose(self) -> ComposeResult:
        yield Container()
