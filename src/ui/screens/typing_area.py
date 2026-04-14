from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen

from ui.widgets.navigation_section import NavigationSection
from ui.widgets.reload_text import ReloadText
from ui.widgets.text_configuration import TextConfiguration
from ui.widgets.typing_area import TypingArea


class TypingScreen(Screen):
    """
    Initial screen that user sees when launch the speedtype.

    It contains input area where the person can start typing.
    Also, it has configurations to customize the text for the
    typing, and also additional buttons to open corresponding
    screens:
    * Profile
    * User's typing statistics
    * Global rating of other speedtypers
    """
    DEFAULT_CSS = """
    TypingScreen {
        background: #1a1d36;
        layout: vertical;
        overflow: hidden auto;
    
        .top {
            min-height: 0;
            max-height: 20;
        }

        .middle {
            height: 30;
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
            yield ReloadText()
            yield NavigationSection()
            yield TextConfiguration()

    def on_text_configuration_config_updated(self, event: TextConfiguration.ConfigUpdated) -> None:
        typing_area = self.query_one(TypingArea)
        typing_area.text_config = event.text_config
        typing_area.mutate_reactive(TypingArea.text_config)
