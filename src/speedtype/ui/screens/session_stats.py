from textual import on
from textual.app import ComposeResult
from textual.containers import Container

from speedtype.ui.constants.colors import APP_BG
from speedtype.ui.screens.base import BaseScreen
from speedtype.ui.widgets.close_button import CloseButton
from speedtype.ui.widgets.invalid_chars_stats.invalid_symbols import InvalidCharsStats
from speedtype.ui.widgets.typing_value_stats.typing_stats import TypingValueStats
from speedtype.ui.widgets.wpm_plot.plot import WPMPlot


class TypingSessionStats(BaseScreen):
    DEFAULT_CSS = f"""
    TypingSessionStats {{
        background: {APP_BG};
        layout: vertical;

        .top {{
            min-height: 0;
            max-height: 12;
        }}

        .middle {{
            align: center middle;
            width: 100%;
            height: auto;

            .stats {{
                height: 25;
                max-width: 140;
                layout: grid;
                grid-size: 2;
                grid-columns: 30% 70%;
                grid-rows: 13 12;
                grid-gutter: 1 2;

                WPMPlot {{
                    column-span: 2;
                }}
            }}
        }}

        .bottom {{
            min-height: 7;
            layout: horizontal;
            width: 100%;
            align: center top;
            padding: 1 0 0 0;
        }}
    }}
    """

    def compose(self) -> ComposeResult:
        yield Container(classes="top")

        with (
            Container(classes="middle"),
            Container(classes="stats"),
        ):
            yield WPMPlot()
            yield TypingValueStats()
            yield InvalidCharsStats()

        with Container(classes="bottom"):
            yield CloseButton()

    @on(CloseButton.Closed)
    def close_stats(self) -> None:
        self.app.pop_screen()
