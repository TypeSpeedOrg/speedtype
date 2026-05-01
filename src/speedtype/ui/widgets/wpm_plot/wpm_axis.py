from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import var
from textual.widgets import Label

from speedtype.ui.types.typing_area import WordStats
from speedtype.ui.widgets.base import BaseWidget


class WPMAxis(BaseWidget):
    DEFAULT_CSS = """
    WPMAxis {
        padding: 0 3 0 0;

        .wpm-speed-axis {
            layout: grid;
            grid-size: 1 3;
            grid-rows: 1fr 1 1fr;

            .max-wpm {
                align: right top;
            }

            .mean-wpm {
                align: right bottom;
            }

            .min-wpm {
                align: right bottom;
            }
        }
    }
    """
    stats: var[list[WordStats]] = var(list, init=False)
    time_range: var[list[int]] = var(list, init=False)

    def compose(self) -> ComposeResult:
        with Container(classes="wpm-speed-axis"):
            with Container(classes="max-wpm"):
                yield Label("90")
            with Container(classes="mean-wpm"):
                yield Label("45")
            with Container(classes="min-wpm"):
                yield Label("0")

    def set_time_range(self, time_range: list[int]) -> None:
        self.time_range = time_range
        self.mutate_reactive(WPMAxis.time_range)
