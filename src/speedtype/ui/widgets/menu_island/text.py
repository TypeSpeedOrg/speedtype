from textual.app import ComposeResult
from textual.widgets import Label

from speedtype.ui.widgets.base import BaseWidget


class MenuIslandText(BaseWidget):
    DEFAULT_CSS = """
    MenuIslandText {
        height: auto;
        width: auto;
        padding: 1 3;
        background: $surface;
    }
    """

    def __init__(
        self,
        *args,
        label: str,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._label = label

    def compose(self) -> ComposeResult:
        yield Label(self._label)
