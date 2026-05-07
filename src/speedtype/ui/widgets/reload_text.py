from textual import on
from textual.app import ComposeResult
from textual.message import Message

from speedtype.ui.widgets.menu_island.button import MenuIslandButton
from speedtype.ui.widgets.menu_island.island import MenuIsland


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
    def _button_pressed(self) -> None:
        self.post_message(self.Pressed())
