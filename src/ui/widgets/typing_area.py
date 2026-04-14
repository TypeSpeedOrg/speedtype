import asyncio
import random
import string

from textual import work
from textual.app import ComposeResult
from textual.containers import Container
from textual.events import Key
from textual.reactive import reactive
from textual.widgets import Label, Static
from textual.worker import Worker

from ui.constants.colors import MENU_ISLAND_BACKGROUD, MENU_ISLAND_COLOR, SELECTED_TEXT_COLOR
from ui.widgets.base import BaseWidget
from ui.widgets.text_configuration import TextConfig, TextConfiguration


class TypingArea(BaseWidget, can_focus=True):
    DEFAULT_CSS = f"""
    TypingArea {{
        width: 100%;
        padding: 0 16;
        align: center middle;
        height: 100%;
        color: {MENU_ISLAND_COLOR};
        
        .text {{
            border: hkey {MENU_ISLAND_BACKGROUD};
            padding: 1 0;
            width: 200;
            
            border-title-align: left;
            border-title-color: {SELECTED_TEXT_COLOR};
            border-title-style: bold;
            border-title-background: {MENU_ISLAND_BACKGROUD};
            
            border-subtitle-align: right;
            border-subtitle-color: {SELECTED_TEXT_COLOR};
            border-subtitle-style: bold;
            border-subtitle-background: {MENU_ISLAND_BACKGROUD};
        }}
        
        Label {{
            text-align: justify;
            width: 100%;
            height: auto;
            text-wrap: wrap;
            text-overflow: fold;
            opacity: 100%;
        }}
    }}
    """
    text_config: reactive[TextConfig] = reactive(dict)
    input_text: reactive[list[str]] = reactive(list)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._input_animation: Worker[None] | None = None

        self._current_char_index = 0

    def compose(self) -> ComposeResult:
        with Container(classes="text"):
            yield Label("")

    def watch_text_config(self) -> None:
        config_string = []
        select_time = ""
        for config_name, values in self.text_config.items():
            if config_name == TextConfiguration.Configuration.TIME:
                select_time = f"{values[0]} SEC"
            else:
                config_string.extend(values)

        self.mount()

        container = self.query_one(Container)
        container.border_title = f" {select_time} "
        container.border_subtitle = f" {", ".join(config_string)} "

    def watch_input_text(self) -> None:
        self.query_one(Label).update(" ".join(self.input_text))

    def on_focus(self) -> None:
        self._input_animation = self._waiting_to_input_animation()

    def on_mount(self) -> None:
        self._update_input_text()

    def on_key(self, event: Key) -> None:
        print(event.character, event.key, flush=True)

    async def _load_input_text(self) -> list[str]:
        return [
            ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(5, 10)))
            for _ in range(1000)
        ]

    @work(name="update_input_text", exclusive=True)
    async def _update_input_text(self) -> None:
        self.input_text = await self._load_input_text()
        self.mutate_reactive(TypingArea.input_text)

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
