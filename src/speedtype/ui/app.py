from textual.app import App

from speedtype.ui.constants.screens import Screen
from speedtype.ui.screens.typing_area import TypingScreen


class SpeedType(App):
    SCREENS = {
        Screen.TYPING_SCREEN: TypingScreen,
    }

    def on_mount(self) -> None:
        self.push_screen(Screen.TYPING_SCREEN)
