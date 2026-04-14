import random
import string

from textual import work
from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import reactive

from ui.constants.colors import MENU_ISLAND_BACKGROUD, MENU_ISLAND_COLOR, SELECTED_TEXT_COLOR
from ui.widgets.base import BaseWidget
from ui.widgets.text_configuration import TextConfig, TextConfiguration
from ui.widgets.text_input import TextInput
from ui.widgets.text_placeholder import TextPlaceholder


LINE_WIDTH = 160


class TypingArea(BaseWidget):
    DEFAULT_CSS = f"""
    TypingArea {{
        width: 100%;
        padding: 0 16;
        height: 100%;
        color: {MENU_ISLAND_COLOR};
        align: center middle;

        .wrapper {{
            align: center middle;
            width: auto;
            padding: 1 0;

            border: hkey {MENU_ISLAND_BACKGROUD};
            border-title-align: left;
            border-title-color: {SELECTED_TEXT_COLOR};
            border-title-style: bold;
            border-title-background: {MENU_ISLAND_BACKGROUD};
            
            border-subtitle-align: right;
            border-subtitle-color: {SELECTED_TEXT_COLOR};
            border-subtitle-style: bold;
            border-subtitle-background: {MENU_ISLAND_BACKGROUD};

            .text {{
                width: {LINE_WIDTH};
                height: 100%;
                layers: placeholder input;

                TextPlaceholder {{
                    layer: placeholder;
                }}

                TextInput {{
                    layer: input;
                }}
            }}
        }}
    }}
    """
    text_config: reactive[TextConfig] = reactive(dict)
    text: reactive[str] = reactive("")

    def compose(self) -> ComposeResult:
        with Container(classes="wrapper"):
            with Container(classes="text"):
                yield TextPlaceholder().data_bind(TypingArea.text)
                yield TextInput(line_width=LINE_WIDTH).data_bind(TypingArea.text)

    def watch_text_config(self) -> None:
        config_string = []
        select_time = ""
        for config_name, values in self.text_config.items():
            if config_name == TextConfiguration.Configuration.TIME:
                select_time = f"{values[0]} SEC"
            else:
                config_string.extend(values)

        container = self.query_one(Container)
        container.border_title = f" {select_time} "
        container.border_subtitle = f" {", ".join(config_string)} "

    def on_mount(self) -> None:
        self._update_input_text()

    @staticmethod
    async def _load_input_text() -> str:
        # TODO: Mocking, in the future must do request to zeus
        return " ".join(
            "".join(random.choice(string.ascii_lowercase) for _ in range(random.randint(5, 10)))
            for _ in range(1000)
        )

    @work(name="update_input_text", exclusive=True)
    async def _update_input_text(self) -> None:
        self.text = await self._load_input_text()
