from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Label

from speedtype.ui.constants.classes import CSSClass
from speedtype.ui.widgets.base import BaseWidget


class InvalidSymbolBar(BaseWidget):
    DEFAULT_CSS = """
    InvalidSymbolBar {
        .invalid-symbol-bar {
            layout: grid;
            grid-size: 2;
            grid-columns: auto 1fr;
            grid-gutter: 0 1;

            .invalid-symbol {
                text-align: center;
                width: 100%;
                color: $invalid-text-color;
            }

            .invalid-symbol-amount {
                text-align: center;
                width: 100%;
                background: $invalid-text-background;
            }
        }
    }
    """

    def __init__(
        self,
        *args,
        symbol: str,
        amount: int,
        **kwargs,
    ) -> None:
        self._symbol = symbol
        self._amount = amount
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        with Container(classes="invalid-symbol-bar"):
            yield Label(self._symbol, classes="invalid-symbol")
            yield Label(str(self._amount), classes=f"invalid-symbol-amount {CSSClass.SELECTED}")
