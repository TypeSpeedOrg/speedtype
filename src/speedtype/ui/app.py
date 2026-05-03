from textual import events, on
from textual.app import App
from textual.binding import Binding

from speedtype.ui.constants.colors import denim_theme
from speedtype.ui.constants.screens import AppScreen
from speedtype.ui.screens.session_stats import TypingSessionStats
from speedtype.ui.screens.typing_screen import TypingScreen


class SpeedType(App):
    SCREENS = {
        AppScreen.TYPING_SCREEN: TypingScreen,
        AppScreen.TYPING_SESSION_STATS: TypingSessionStats,
    }
    ENABLE_COMMAND_PALETTE = False
    BINDINGS = [
        Binding(
            "ctrl+q",
            "quit",
            "Quit",
            tooltip="Quit the app and return to the command prompt.",
            show=True,
            priority=True,
        ),
        Binding(
            "tab",
            "focus_next",
            "Focus Next",
            priority=True,
        ),
        Binding(
            "shift+tab",
            "focus_previous",
            "Focus Previous",
            priority=True,
        ),
        Binding(
            "enter",
            "noop",
            "Press Button",
            key_display="enter",
            priority=True,
        ),
    ]

    @on(events.Mount)
    def _show_typing_screen(self) -> None:
        self.register_theme(denim_theme)
        self.theme = "denim"

        self.push_screen(AppScreen.TYPING_SCREEN)

    def get_theme_variable_defaults(self) -> dict[str, str]:
        return {
            "hover-background": "#161730",
            "hover-foreground": "#6c718c",
            "accent-color": "#fc9fb4",
            "accent-hover-color": "#f5aebe",
            "accent-hover-background": "#820a26",
            "invalid-text-color": "#f56788",
            "invalid-text-background": "#9c1131",
            "correct-text-color": "#86e39d",
            "correct-text-background": "#119c34",
        }
