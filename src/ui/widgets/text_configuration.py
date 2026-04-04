from enum import StrEnum

from textual.app import ComposeResult

from ui.css.classes import CSSClass
from ui.css.ids import WidgetID
from ui.widgets.menu_island import MenuIsland, MenuIslandText
from ui.widgets.select_menu_island import SectionMenuIsland


class TextConfiguration(MenuIsland):

    class Configuration(StrEnum):
        TIME = "TIME"
        LANGUAGE = "LANGUAGE"
        DIFFICULTY = "DIFFICULTY"

    class TimeOption(StrEnum):
        SEC_30 = "30"
        SEC_60 = "60"
        SEC_90 = "90"
        SEC_120 = "120"

    def compose(self) -> ComposeResult:
        yield SectionMenuIsland(
            options=(
                (self.Configuration.TIME, CSSClass.SELECTED),
                self.Configuration.LANGUAGE,
                self.Configuration.DIFFICULTY,
            ),
            id=WidgetID.TEXT_CUSTOMIZATION_MENU,
            persistent=True,
        )

        yield MenuIslandText(label="┃")

        yield SectionMenuIsland(
            options=(
                self.TimeOption.SEC_30,
                (self.TimeOption.SEC_60, CSSClass.SELECTED),
                self.TimeOption.SEC_90,
                self.TimeOption.SEC_120,
            ),
            id=WidgetID.TIME_OPTIONS,
            persistent=True,
        )
