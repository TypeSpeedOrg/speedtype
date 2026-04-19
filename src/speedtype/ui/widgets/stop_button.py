from textual import on
from textual.app import ComposeResult
from textual.message import Message

from speedtype.ui.widgets.menu_island import MenuIsland, MenuIslandButton


class StopTypeButton(MenuIsland):
    class Stopped(Message):
        pass

    def compose(self) -> ComposeResult:
        yield MenuIslandButton(
            label="STOP",
            value=None,
            persist_click=False,
        )

    @on(MenuIslandButton.Pressed)
    def stop_button_pressed(self) -> None:
        self.post_message(self.Stopped())
