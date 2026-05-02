from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import var
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
    wpm_borders: var[tuple[int, int, int]] = var(None, init=False)

    def compose(self) -> ComposeResult:
        with Container(classes="wpm-speed-axis"):
            yield Container(classes="max-wpm")
            yield Container(classes="mean-wpm")
            yield Container(classes="min-wpm")

    def watch_wpm_borders(self) -> None:
        max_wpm_container = self.query_one("Container.max-wpm", Container)
        mean_wpm_container = self.query_one("Container.mean-wpm", Container)
        min_wpm_container = self.query_one("Container.min-wpm", Container)

        max_wpm_container.remove_children()
        mean_wpm_container.remove_children()
        min_wpm_container.remove_children()

        max_wpm_container.mount(Label(str(self.wpm_borders[2])))
        mean_wpm_container.mount(Label(str(self.wpm_borders[1])))
        min_wpm_container.mount(Label(str(self.wpm_borders[0])))
