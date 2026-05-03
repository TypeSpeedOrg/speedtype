from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import var
from textual.widgets import Label

from speedtype.ui.constants.classes import CSSClass
from speedtype.ui.widgets.base import BaseWidget


class StatsSection(BaseWidget):
    DEFAULT_CSS = """
    StatsSection {
        layout: grid;
        grid-size: 2;
        grid-columns: 30% 70%;
        background: $surface;
        align-vertical: middle;
        padding: 0 2;

        .value {
            width: 100%;
            height: auto;
        }

        .description {
            width: 100%;
            height: auto;

            Label {
                width: 100%;
                text-align: right;
            }
        }
    }
    """
    value: var[str] = var(None, init=False)

    def __init__(
        self,
        *args,
        label: str,
        **kwargs,
    ) -> None:
        self._label = label
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        with Container(classes="value"):
            yield Label(self.value, classes=CSSClass.SELECTED)
        with Container(classes="description"):
            yield Label(self._label)

    def watch_value(self) -> None:
        self.query_one("Container.value", Container).query_one(Label).update(self.value)
