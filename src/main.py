from textual.app import App

from ui.constants.screens import Screen
from ui.screens.typing_area import TypingScreen


class SpeedTypeApp(App):
    SCREENS = {
        Screen.TYPING_SCREEN: TypingScreen,
    }

    def on_mount(self) -> None:
        self.push_screen(Screen.TYPING_SCREEN)


if __name__ == "__main__":
    app = SpeedTypeApp()
    app.run()
