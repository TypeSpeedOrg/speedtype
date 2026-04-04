from textual.app import ComposeResult

from ui.widgets.menu_island import MenuIsland, MenuIslandButton


class ReloadText(MenuIsland):

    def compose(self) -> ComposeResult:
        yield MenuIslandButton(
            label="RELOAD",
            persist_click=False,
        )
