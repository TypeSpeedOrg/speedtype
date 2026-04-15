from typing import NamedTuple

from rich.repr import Result
from textual import on
from textual.app import ComposeResult
from textual.events import Mount
from textual.message import Message

from ui.constants.classes import CSSClass
from ui.widgets.base import BaseWidget
from ui.widgets.menu_island import MenuIslandButton


type SectionOptions = tuple[SectionOption, ...]


class SectionOption(NamedTuple):
    label: str
    value: str | None = None
    css_class: str | None = None


class SectionConfiguration(NamedTuple):
    options: tuple[SectionOption, ...]
    name: str | None = None
    is_multiple_options: bool = False


class SectionMenuIsland(BaseWidget):
    DEFAULT_CSS = """
    SectionMenuIsland {
        height: auto;
        max-height: 20;
        width: auto;
    }
    """

    class OptionSelected(Message):

        def __init__(self, value: str, section_name: str) -> None:
            self.value = value
            self.section_name = section_name
            super().__init__()

        def __rich_repr__(self) -> Result:
            yield "value", self.value
            yield "section_name", self.section_name

    class OptionRemoved(Message):

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
        is_multiple_options: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self._options = options
        self._persistent = persistent
        self._name = name
        self._is_vertical = is_vertical
        self._multiple_options = is_multiple_options
        self.styles.layout = 'vertical' if is_vertical else 'horizontal'

        self._selected_options = [option.value for option in self._options if CSSClass.SELECTED == option.css_class]

    def compose(self) -> ComposeResult:
        max_width = max(map(lambda opt: len(opt.label), self._options))

        for option in self._options:
            button = MenuIslandButton(
                label=option.label,
                classes=option.css_class,
                persist_click=self._persistent,
                value=option.value,
            )

            # TODO: refactor, looks awful
            if self._is_vertical:
                button.styles.width = max_width + 6

            yield button

    @on(MenuIslandButton.Pressed)
    def button_pressed(self, event: MenuIslandButton.Pressed) -> None:
        if not self._persistent:
            return

        option = event.value

        if self._multiple_options and option not in self._selected_options:
            self._selected_options.append(option)
            self.post_message(
                self.OptionSelected(
                    value=option,
                    section_name=self._name,
                )
            )

        elif self._multiple_options and option in self._selected_options:
            self._selected_options.remove(option)
            self.post_message(
                self.OptionRemoved(
                    value=option,
                    section_name=self._name,
                )
            )

            for selected_button in self.query_children(MenuIslandButton).filter(f".{CSSClass.SELECTED}"):
                if selected_button.value == option:
                    selected_button.remove_class(CSSClass.SELECTED)

        elif not self._multiple_options and option not in self._selected_options:
            if self._selected_options:
                self.post_message(
                    self.OptionRemoved(
                        value=self._selected_options[0],
                        section_name=self._name,
                    )
                )

            self._selected_options = [option]
            self.post_message(
                self.OptionSelected(
                    value=option,
                    section_name=self._name,
                )
            )

            for selected_button in self.query_children(MenuIslandButton).filter(f".{CSSClass.SELECTED}"):
                if selected_button.value != option:
                    selected_button.remove_class(CSSClass.SELECTED)

        event.stop()

    def on_mount(self, event: Mount) -> None:
        for option in self._selected_options:
            self.post_message(
                self.OptionSelected(
                    value=option,
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
        section_configs: tuple[SectionConfiguration, ...],
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._section_configs = section_configs

    def compose(self) -> ComposeResult:
        for config in self._section_configs:
            yield SectionMenuIsland(
                options=config.options,
                persistent=True,
                is_vertical=True,
                name=config.name,
                is_multiple_options=config.is_multiple_options,
            )
