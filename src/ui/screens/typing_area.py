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

    CSS_PATH = "speedtype.tcss"

    def compose(self) -> ComposeResult:
        yield Container()
        yield TypingArea()
        with Container(classes="bottom"):
            yield ReloadText()
            yield NavigationSection()
            yield TextConfiguration()
