from enum import StrEnum

from textual.app import ComposeResult

from ui.widgets.menu_island import MenuIsland
from ui.widgets.select_menu_island import SectionMenuIsland


class NavigationSection(MenuIsland):

    class Section(StrEnum):
        PROFILE = "PROFILE"
        STATS = "STATS"
        RATING = "RATING"

    def compose(self) -> ComposeResult:
        yield SectionMenuIsland(
            options=(
                self.Section.PROFILE,
                self.Section.STATS,
                self.Section.RATING,
            ),
            persistent=False,
        )
