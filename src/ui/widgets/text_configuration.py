from enum import StrEnum

from rich.repr import Result
from textual.app import ComposeResult
from textual.message import Message

from ui.constants.classes import CSSClass
from ui.widgets.menu_island import MenuIsland, MenuIslandText
from ui.widgets.section_menu_island import (
    MultipleSectionMenuIsland, SectionConfiguration, SectionMenuIsland,
    SectionOption,
)


type TextConfig = dict[TextConfiguration.Configuration, list[str]]


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

    class Language(StrEnum):
        ENGLISH = "ENGLISH"
        RUSSIAN = "РУССКИЙ"
        UKRAINIAN = "УКРАЇНСЬКА"

    class WordsLength(StrEnum):
        SHORT_WORDS = "SHORT WORDS"
        REGULAR_WORDS = "REGULAR WORDS"
        LONG_WORDS = "LONG WORDS"

    class AdditionalSymbols(StrEnum):
        PUNCTUATION = "PUNCTUATION"
        SPECIAL_CHARACTERS = "SPECIAL CHARACTERS"

    class ConfigUpdated(Message):

        def __init__(self, text_config: TextConfig) -> None:
            self.text_config = text_config
            super().__init__()

        def __rich_repr__(self) -> Result:
            yield "text_config", self.text_config

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._text_config_sections = {
            self.Configuration.TIME: SectionMenuIsland(
                options=(
                    SectionOption(
                        label=self.TimeOption.SEC_30,
                        value=self.TimeOption.SEC_30,
                    ),
                    SectionOption(
                        label=self.TimeOption.SEC_60,
                        value=self.TimeOption.SEC_60,
                        css_class=CSSClass.SELECTED,
                    ),
                    SectionOption(
                        label=self.TimeOption.SEC_90,
                        value=self.TimeOption.SEC_90,
                    ),
                    SectionOption(
                        label=self.TimeOption.SEC_120,
                        value=self.TimeOption.SEC_120,
                    ),
                ),
                name=self.Configuration.TIME,
                persistent=True,
                is_vertical=False,
            ),
            self.Configuration.LANGUAGE: SectionMenuIsland(
                options=(
                    SectionOption(
                        label=self.Language.ENGLISH,
                        value=self.Language.ENGLISH,
                        css_class=CSSClass.SELECTED,
                    ),
                    SectionOption(
                        label=self.Language.RUSSIAN,
                        value=self.Language.RUSSIAN,
                    ),
                    SectionOption(
                        label=self.Language.UKRAINIAN,
                        value=self.Language.UKRAINIAN,
                    ),
                ),
                name=self.Configuration.LANGUAGE,
                persistent=True,
                is_vertical=True,
            ),
            self.Configuration.DIFFICULTY: MultipleSectionMenuIsland(
                section_configs=(
                    SectionConfiguration(
                        options=(
                            SectionOption(
                                label=self.WordsLength.SHORT_WORDS,
                                value=self.WordsLength.SHORT_WORDS,
                            ),
                            SectionOption(
                                label=self.WordsLength.REGULAR_WORDS,
                                value=self.WordsLength.REGULAR_WORDS,
                                css_class=CSSClass.SELECTED,
                            ),
                            SectionOption(
                                label=self.WordsLength.LONG_WORDS,
                                value=self.WordsLength.LONG_WORDS,
                            ),
                        ),
                        name="words_length",
                    ),
                    SectionConfiguration(
                        options=(
                            SectionOption(
                                label=self.AdditionalSymbols.PUNCTUATION,
                                value=self.AdditionalSymbols.PUNCTUATION,
                            ),
                            SectionOption(
                                label=self.AdditionalSymbols.SPECIAL_CHARACTERS,
                                value=self.AdditionalSymbols.SPECIAL_CHARACTERS,
                            ),
                        ),
                        name="additional_symbols",
                        is_multiple_options=True,
                    ),
                )
            ),
        }
        self._text_config: TextConfig = {}

        self._customization_sections_name = 'config_menu'
        self._customization_sections = SectionMenuIsland(
            options=(
                SectionOption(
                    label=self.Configuration.TIME,
                    value=self.Configuration.TIME,
                    css_class=CSSClass.SELECTED,
                ),
                SectionOption(
                    label=self.Configuration.LANGUAGE,
                    value=self.Configuration.LANGUAGE,
                ),
                SectionOption(
                    label=self.Configuration.DIFFICULTY,
                    value=self.Configuration.DIFFICULTY,
                ),
            ),
            name=self._customization_sections_name,
            persistent=True,
            is_vertical=False,
        )

    def compose(self) -> ComposeResult:
        yield self._customization_sections
        yield MenuIslandText(label="┃")

        for section in self._text_config_sections.values():
            yield section

    def on_section_menu_island_option_selected(self, event: SectionMenuIsland.OptionSelected) -> None:
        if event.section_name != self._customization_sections_name:
            self._text_config.setdefault(event.section_name, []).append(event.value)
            self.post_message(self.ConfigUpdated(text_config=self._text_config))
            return

        selected_section_name = event.value
        self._text_config_sections[selected_section_name].show()

        for section_name, section in self._text_config_sections.items():
            if selected_section_name == section_name:
                section.show()
            else:
                section.hide()

    def on_section_menu_island_option_removed(self, event: SectionMenuIsland.OptionRemoved) -> None:
        if event.section_name != self._customization_sections_name:
            self._text_config.setdefault(event.section_name, []).remove(event.value)
            self.post_message(self.ConfigUpdated(text_config=self._text_config))
            return
