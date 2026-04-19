from textual import on
from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen

from speedtype.ui.widgets.navigation_section import NavigationSection
from speedtype.ui.widgets.reload_text import ReloadTextButton
from speedtype.ui.widgets.stop_button import StopTypeButton
from speedtype.ui.widgets.text_configuration import TextConfiguration
from speedtype.ui.widgets.text_input import TextInput
from speedtype.ui.widgets.typing_area import TypingArea


class TypingScreen(Screen):
    DEFAULT_CSS = """
    TypingScreen {
        background: #1a1d36;
        layout: vertical;
        overflow: hidden auto;

        .top {
            min-height: 0;
            max-height: 12;
        }

        .middle {
            height: 25;
        }

        .bottom {
            min-height: 7;
            layout: horizontal;
            width: 100%;
            align: center top;
            padding: 1 0 0 0;
        }
    }
    """

    CSS_PATH = "speedtype.tcss"

    def compose(self) -> ComposeResult:
        yield Container(classes="top")

        with Container(classes="middle"):
            yield TypingArea()

        with Container(classes="bottom"):
            yield ReloadTextButton()
            yield NavigationSection()
            yield TextConfiguration()
            yield StopTypeButton()

    def on_mount(self) -> None:
        self.query_one(StopTypeButton).hide()

    @on(ReloadTextButton.Pressed)
    def reload_button_pressed(self) -> None:
        self.query_one(TypingArea).regenerate_text()

    @on(StopTypeButton.Stopped)
    def stop_button_pressed(self) -> None:
        self.query_one(TypingArea).is_typing = False

    @on(TextInput.TypingStarted)
    def typing_started(self) -> None:
        self.query_one(ReloadTextButton).hide()
        self.query_one(NavigationSection).hide()
        self.query_one(TextConfiguration).hide()
        self.query_one(StopTypeButton).show()

    @on(TypingArea.TypingStopped)
    def typing_stopped(self) -> None:
        self.query_one(StopTypeButton).hide()
        self.query_one(ReloadTextButton).show()
        self.query_one(NavigationSection).show()
        self.query_one(TextConfiguration).show()

    @on(TextConfiguration.ConfigUpdated)
    def text_configuration_updated(
        self,
        event: TextConfiguration.ConfigUpdated,
    ) -> None:
        typing_area = self.query_one(TypingArea)
        typing_area.text_config = event.text_config
        typing_area.mutate_reactive(TypingArea.text_config)
