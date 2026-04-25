from textual.app import App

from speedtype.ui.constants.screens import AppScreen
from speedtype.ui.screens.session_stats import TypingSessionStats
from speedtype.ui.screens.typing_screen import TypingScreen


class SpeedType(App):
    SCREENS = {
        AppScreen.TYPING_SCREEN: TypingScreen,
        AppScreen.TYPING_SESSION_STATS: TypingSessionStats,
    }

    def on_mount(self) -> None:
        self.push_screen(AppScreen.TYPING_SCREEN)
        self.push_screen(AppScreen.TYPING_SESSION_STATS)
