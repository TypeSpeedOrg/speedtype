import asyncio

from textual import work
from textual.app import ComposeResult
from textual.containers import Container
from textual.events import Key
from textual.message import Message
from textual.reactive import reactive
from textual.widgets import Label

from ui.widgets.base import BaseWidget


class TextPlaceholder(BaseWidget, can_focus=True):
    DEFAULT_CSS = """
    TextPlaceholder {
        .placeholder {
            height: 100%;
            width: 100%;

            Label {
                width: 100%;
                height: auto;
                text-wrap: wrap;
                text-overflow: fold;
                opacity: 100%;
            }
        }
    }
    """
    text: reactive[str] = reactive("")

    class KeyPressed(Message):

        def __init__(self, name: str, char: str, is_printable: bool) -> None:
            self.name = name
            self.char = char
            self.is_printable = is_printable
            super().__init__()

    def compose(self) -> ComposeResult:
        with Container(classes="placeholder"):
            yield Label("")

    def watch_text(self) -> None:
        self.query_one(Label).update(self.text)

    def on_focus(self) -> None:
        self._waiting_to_input_animation()

    def on_blur(self):
        self._waiting_to_input_animation().cancel()

    def on_key(self, event: Key) -> None:
        self.post_message(
            self.KeyPressed(
                name=event.name,
                char=event.character,
                is_printable=event.is_printable,
            )
        )

    @work(name="waiting_to_input_animation", exclusive=True)
    async def _waiting_to_input_animation(self) -> None:
        duration = 0.8

        async def animate_input(value: float, easing: str) -> None:
            self.query_one(Label).styles.animate(
                "opacity",
                value=value,
                duration=duration,
                easing=easing,
            )
            await asyncio.sleep(duration)

        while True:
            await animate_input(0.5, "in_out_quad")
            await animate_input(1, "in_out_quad")
