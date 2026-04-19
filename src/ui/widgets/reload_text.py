from textual import on
from textual.app import ComposeResult
from textual.message import Message

from ui.widgets.menu_island import MenuIsland, MenuIslandButton


class ReloadTextButton(MenuIsland):
    class Pressed(Message):
        pass

    def compose(self) -> ComposeResult:
        yield MenuIslandButton(
            label="RELOAD",
            value=None,
            persist_click=False,
        )

    @on(MenuIslandButton.Pressed)
    def button_pressed(self) -> None:
        self.post_message(self.Pressed())
