from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Label

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

    _time: reactive[list[int]] = reactive(list)

    def compose(self) -> ComposeResult:
        with Container(classes="wpm-speed-axis"):
            with Container(classes="max-wpm"):
                yield Label("90")
            with Container(classes="mean-wpm"):
                yield Label("45")
            with Container(classes="min-wpm"):
                yield Label("0")

    @property
    def time(self) -> list[int]:
        return self._time

    @time.setter
    def time(self, value: list[int]) -> None:
        self._time = value
        self.mutate_reactive(self._time)
