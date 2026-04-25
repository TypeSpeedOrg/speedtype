from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Label

from speedtype.ui.constants.colors import BLOCK_BG, BLOCK_COLOR, BLOCK_HOVER_COLOR
from speedtype.ui.widgets.base import BaseWidget
from speedtype.ui.widgets.invalid_chars_stats.invalid_symbol_bar import InvalidSymbolBar


class InvalidCharsStats(BaseWidget):
    DEFAULT_CSS = f"""
    InvalidCharsStats {{
        padding: 1 3 1 1;
        layout: vertical;
        background: {BLOCK_BG};

        .title {{
            color: {BLOCK_COLOR};
            text-align: center;
            width: 100%;
        }}

        .invalid-bars {{
            layout: grid;
            grid-size: 6;
            grid-rows: 1;
            grid-gutter: 1 2;
            padding: 1 2;
            overflow: hidden auto;
            scrollbar-size-vertical: 1;
            scrollbar-background: {BLOCK_BG};
            scrollbar-background-hover: {BLOCK_BG};
            scrollbar-background-active: {BLOCK_BG};
            scrollbar-color: {BLOCK_COLOR};
            scrollbar-color-hover: {BLOCK_HOVER_COLOR};
            scrollbar-color-active: {BLOCK_HOVER_COLOR};
            scrollbar-gutter: auto;
        }}
    }}
    """

    def compose(self) -> ComposeResult:
        yield Label("INVALID SYMBOLS LIST", classes="title")

        with Container(classes="invalid-bars"):
            yield InvalidSymbolBar(symbol="j", amount=32)
            yield InvalidSymbolBar(symbol="l", amount=7)
            yield InvalidSymbolBar(symbol="k", amount=5)
            yield InvalidSymbolBar(symbol="s", amount=4)
            yield InvalidSymbolBar(symbol="g", amount=3)
            yield InvalidSymbolBar(symbol="h", amount=3)
