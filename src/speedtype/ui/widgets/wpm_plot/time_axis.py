from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Label

from speedtype.ui.widgets.base import BaseWidget


class TimeAxis(BaseWidget):
    DEFAULT_CSS = """
    TimeAxis {
        padding: 1 0 0 0;
        .wpm-time {
            layout: grid;
            grid-size: 6;

            .last-time-cell {
                layout: grid;
                grid-size: 2;

                .end-time-value {
                    width: 100%;
                    text-align: right;
                }
            }
        }
    }
    """

    def compose(self) -> ComposeResult:
        with Container(classes="wpm-time"):
            with Container():
                yield Label("0")
            with Container():
                yield Label("5")
            with Container():
                yield Label("10")
            with Container():
                yield Label("15")
            with Container():
                yield Label("20")
            with Container(classes="last-time-cell"):
                yield Label("25")
                yield Label("30", classes="end-time-value")
