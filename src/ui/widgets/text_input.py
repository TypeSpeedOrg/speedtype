from textual.app import ComposeResult
from textual.containers import Container
from textual.events import Key
from textual.reactive import reactive
from textual.widgets import Label

from ui.widgets.base import BaseWidget


class TextInput(BaseWidget, can_focus=True):
    DEFAULT_CSS = """
    TextInput {
        width: auto;
        height: auto;

        .input {
            width: auto;
            height: auto;
            layout: vertical;

            .text_line {
                layout: horizontal;
                width: auto;
                height: auto;

                .invalid {
                    color: red;
                }

                .correct {
                    color: white;
                }

                Label {
                    width: auto;
                    height: auto;
                }
            }
        }
    }
    """
    text: reactive[str] = reactive("")

    def __init__(self, *args, line_width: int, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._line_size = line_width

    def compose(self) -> ComposeResult:
        with Container(classes="input"):
            with Container(classes="text_line"):
                yield Label("12")

    def on_key(self, event: Key):
        label = self.query_one(Label)
        label.update(label.content + event.character if event.character else "")
