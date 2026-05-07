from textual import on
from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import var
from textual.widgets import Footer

from speedtype.ui.constants.screens import AppScreen
from speedtype.ui.screens.base import BaseScreen
from speedtype.ui.types.session_stats import InputStats
from speedtype.ui.widgets.close_button import CloseButton
from speedtype.ui.widgets.invalid_chars_stats.invalid_symbols import InvalidCharsStats
from speedtype.ui.widgets.typing_value_stats.typing_stats import TypingValueStats
from speedtype.ui.widgets.wpm_plot.wpm_plot import WPMPlot


class TypingSessionStats(BaseScreen):
    DEFAULT_CSS = """
    TypingSessionStats {
        layout: vertical;

        .top {
            min-height: 0;
            max-height: 12;
        }

        .middle {
            align: center middle;
            width: 100%;
            height: auto;

            .stats {
                height: 25;
                max-width: 140;
                layout: grid;
                grid-size: 2;
                grid-columns: 30% 70%;
                grid-rows: 13 12;
                grid-gutter: 1 2;

                WPMPlot {
                    column-span: 2;
                }
            }
        }

        .bottom {
            min-height: 7;
            layout: horizontal;
            width: 100%;
            align: center top;
            padding: 1 0 0 0;
        }
    }
    """
    input_stats: var[InputStats] = var(None, init=False)

    def compose(self) -> ComposeResult:
        yield Container(classes="top")

        with (
            Container(classes="middle"),
            Container(classes="stats"),
        ):
            yield WPMPlot().data_bind(TypingSessionStats.input_stats)
            yield TypingValueStats().data_bind(TypingSessionStats.input_stats)
            yield InvalidCharsStats().data_bind(TypingSessionStats.input_stats)

        with Container(classes="bottom"):
            yield CloseButton()

        yield Footer()

    @on(CloseButton.Closed)
    def _close_stats(self) -> None:
        self.app.switch_screen(AppScreen.TYPING_SCREEN)
