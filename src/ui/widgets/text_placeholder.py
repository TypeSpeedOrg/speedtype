import asyncio

from textual import work
from textual.app import ComposeResult
from textual.containers import Container
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
                text-align: justify;
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

    def compose(self) -> ComposeResult:
        with Container(classes="placeholder"):
            yield Label("")

    def watch_text(self) -> None:
        self.query_one(Label).update(self.text)

    def on_focus(self) -> None:
        self._waiting_to_input_animation()

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
