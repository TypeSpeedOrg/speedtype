from enum import StrEnum

from textual.app import ComposeResult

from ui.widgets.menu_island import MenuIsland
from ui.widgets.section_menu_island import SectionMenuIsland, SectionOption


class NavigationSection(MenuIsland):

    class Section(StrEnum):
        PROFILE = "PROFILE"
        STATS = "STATS"
        RATING = "RATING"

    def compose(self) -> ComposeResult:
        yield SectionMenuIsland(
            options=(
                SectionOption(
                    label=self.Section.PROFILE,
                    value=None,
                ),
                SectionOption(
                    label=self.Section.STATS,
                    value=None,
                ),
                SectionOption(
                    label=self.Section.RATING,
                    value=None,
                ),
            ),
            persistent=False,
            is_vertical=False,
        )
