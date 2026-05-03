from textual import on
from textual.app import ComposeResult
from textual.message import Message

from speedtype.ui.widgets.menu_island.button import ButtonStyle, MenuIslandButton
from speedtype.ui.widgets.menu_island.island import MenuIsland


class CloseButton(MenuIsland):
    class Closed(Message):
        pass

    def compose(self) -> ComposeResult:
        yield MenuIslandButton(
            label="CLOSE",
            value=None,
            persist_click=False,
            button_style=ButtonStyle.ABORT,
        )

    @on(MenuIslandButton.Pressed)
    def _stop_button_pressed(self) -> None:
        self.post_message(self.Closed())
