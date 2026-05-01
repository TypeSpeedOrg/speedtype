from nodeenv import iteritems
from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import var
from textual.widgets import Label

from speedtype.ui.constants.colors import BLOCK_BG, BLOCK_COLOR, BLOCK_HOVER_COLOR
from speedtype.ui.types.session_stats import InputStats
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

        .no-mistakes {{
            display: none;
            width: 100%;
            height: 100%;
            align: center middle;

            Label {{
                color: {BLOCK_COLOR};
            }}
        }}
    }}
    """
    input_stats: var[InputStats] = var(None, init=False)

    def compose(self) -> ComposeResult:
        yield Label("INVALID SYMBOLS LIST", classes="title")

        yield Container(classes="invalid-bars")

        with Container(classes="no-mistakes"):
            yield Label("NO MISTAKES. BRAVO!", classes="no-mistakes-label")

    def watch_input_stats(self) -> None:
        label = self.query_one(Label)
        invalid_bars = self.query_one("Container.invalid-bars", Container)
        no_mistakes_message = self.query_one("Container.no-mistakes", Container)

        for bar in invalid_bars.query_children(InvalidSymbolBar):
            bar.remove()

        if not self.input_stats.invalid_chars:
            label.styles.display = "none"
            invalid_bars.styles.display = "none"
            no_mistakes_message.styles.display = "block"
            return

        label.styles.display = "block"
        invalid_bars.styles.display = "block"
        no_mistakes_message.styles.display = "none"

        for symbol, amount in sorted(iteritems(self.input_stats.invalid_chars), key=lambda x: x[1], reverse=True):
            invalid_bars.mount(InvalidSymbolBar(symbol=symbol, amount=amount))
