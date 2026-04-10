from typing import NamedTuple

from funcy import first
from rich.repr import Result
from textual.app import ComposeResult
from textual.events import Mount
from textual.message import Message
from textual.reactive import reactive

from ui.constants.classes import CSSClass
from ui.widgets.base import BaseWidget
from ui.widgets.menu_island import MenuIslandButton


type SectionOptions = tuple[SectionOption, ...]


class SectionOption(NamedTuple):
    label: str
    value: str | None = None
    css_class: str | None = None


class SectionMenuIsland(BaseWidget):
    DEFAULT_CSS = """
    SectionMenuIsland {
        height: auto;
        max-height: 20;
        width: auto;
    }
    """
    selected_option: reactive[str | None] = reactive(None)

    class OptionSelected(Message):

        def __init__(self, value: str, section_name: str) -> None:
            self.value = value
            self.section_name = section_name
            super().__init__()

        def __rich_repr__(self) -> Result:
            yield "value", self.value
            yield "section_name", self.section_name

    def __init__(
        self,
        *args,
        options: SectionOptions,
        persistent: bool,
        is_vertical: bool,
        name: str | None = None,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self._options = options
        self._persistent = persistent
        self._name = name
        self.styles.layout = 'vertical' if is_vertical else 'horizontal'

        if option := first(filter(lambda opt: CSSClass.SELECTED == opt.css_class, self._options)):
            self.set_reactive(
                SectionMenuIsland.selected_option,
                option.value,
            )

    def compose(self) -> ComposeResult:
        for option in self._options:
            yield MenuIslandButton(
                label=option.label,
                classes=option.css_class,
                persist_click=self._persistent,
                value=option.value,
            )

    def on_menu_island_button_pressed(self, event: MenuIslandButton.Pressed) -> None:
        if not self._persistent:
            return

        self.selected_option = event.value
        event.stop()

    def on_mount(self, event: Mount) -> None:
        self._process_selected_option()

    def watch_selected_option(self) -> None:
        self._process_selected_option()

    def _process_selected_option(self):
        for selected_button in self.query_children(MenuIslandButton).filter(f".{CSSClass.SELECTED}"):
            if selected_button.value != self.selected_option:
                selected_button.remove_class(CSSClass.SELECTED)

        self.post_message(
            self.OptionSelected(
                value=self.selected_option,
                section_name=self._name,
            )
        )


class MultipleSectionMenuIsland(BaseWidget):
    DEFAULT_CSS = """
    MultipleSectionMenuIsland {
        height: auto;
        layout: horizontal;
        width: auto;
    }
    """

    def __init__(
        self,
        *args,
        sections: tuple[SectionOptions, ...],
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._sections = sections

    def compose(self) -> ComposeResult:
        for section_options in self._sections:
            yield SectionMenuIsland(
                options=section_options,
                persistent=True,
                is_vertical=True,
            )
