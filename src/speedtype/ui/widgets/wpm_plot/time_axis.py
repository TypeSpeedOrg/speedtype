from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import var
from textual.widgets import Label

from speedtype.ui.widgets.base import BaseWidget


class TimeAxis(BaseWidget):
    DEFAULT_CSS = """
    TimeAxis {
        padding: 1 0 0 0;

        .wpm-time {
            layout: grid;
            grid-size: 5;

            .last-time-step {
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
    input_time: var[int] = var(None, init=False)

    def compose(self) -> ComposeResult:
        yield Container(classes="wpm-time")

    def watch_input_time(self) -> None:
        steps_amount = 5
        time_delta = self.input_time // steps_amount

        time_container = self.query_one(Container)
        time_container.remove_children()

        for step in range(steps_amount - 1):
            label_container = Container()
            time_container.mount(label_container)
            label_container.mount(Label(str(time_delta * step)))

        last_step_container = Container(classes="last-time-step")
        time_container.mount(last_step_container)
        last_step_container.mount(Label(str(self.input_time - time_delta)))
        last_step_container.mount(Label(str(self.input_time), classes="end-time-value"))
