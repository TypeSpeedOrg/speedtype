from contextlib import suppress
from enum import StrEnum, auto
from typing import NamedTuple

from textual.app import ComposeResult
from textual.containers import Container
from textual.css.query import NoMatches
from textual.events import Key
from textual.reactive import reactive
from textual.widgets import Label

from ui.widgets.base import BaseWidget


class TextMark(StrEnum):
    INVALID = auto()
    CORRECT = auto()


class TextLine(NamedTuple):
    words: tuple[str]
    length: int

    @property
    def text(self) -> str:
        return "".join(self.words)


class TextInput(BaseWidget, can_focus=True):
    DEFAULT_CSS = F"""
    TextInput {{
        width: auto;
        height: auto;

        .text_field {{
            width: auto;
            height: auto;
            layout: vertical;

            .text_line {{
                layout: horizontal;
                width: auto;
                height: auto;

                Label {{
                    width: auto;
                    height: auto;
                    
                    &.{TextMark.INVALID} {{
                        color: #f56788;
                        background: #9c1131 20%;
                    }}
                    
                    &.{TextMark.CORRECT} {{
                        color: #86e39d;
                        background: #119c34 20%;
                    }}
                }}
            }}
        }}
    }}
    """
    text: reactive[str] = reactive("")

    def __init__(self, *args, line_length: int, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._line_length_limit = line_length
        self._text_lines: list[TextLine] = []
        self._current_line_idx = 0
        self._current_char_idx = 0

        self._text_field = Container(classes="text_field")

    def compose(self) -> ComposeResult:
        yield self._text_field

    def on_key(self, event: Key):
        self.process_typed_char(name=event.name, char=event.character, is_printable=event.is_printable)

    def watch_text(self) -> None:
        self._text_lines = []

        current_line_length = 0
        line_words = []

        for word in self.text.split():
            word_length = len(word) + 1

            if current_line_length + word_length <= self._line_length_limit:
                line_words.extend((word, " "))
                current_line_length += word_length

            else:
                self._text_lines.append(
                    TextLine(
                        words=tuple(line_words),
                        length=current_line_length,
                    )
                )
                line_words = []
                current_line_length = 0

        self.styles.layers = " ".join(f"line_{i}" for i in range(len(self._text_lines)))

    def process_typed_char(self, name: str, char: str, is_printable: bool) -> None:
        match name, char, is_printable:
            case "backspace", _, _:
                pass
            case _, _, True:
                self._add_char(char)

    def _add_char(self, character: str) -> None:
        is_char_valid = character == self._current_char
        text_label = self._get_text_label(mark=TextMark.CORRECT if is_char_valid else TextMark.INVALID)
        text_label.content += character
        self._inc_current_char_idx()

    def _get_text_label(self, mark: TextMark) -> Label:
        text_line = self._current_text_line_container

        with suppress(NoMatches):
            label = text_line.query(Label).last()
            if label.has_class(mark):
                return label

        label = Label(classes=mark)
        text_line.mount(label)
        return label

    def _inc_current_char_idx(self) -> None:
        self._current_char_idx += 1

        if self._current_char_idx == self._current_text_line_length:
            self._current_line_idx += 1
            self._current_char_idx = 0
            self._add_new_text_line_container()

    def _add_new_text_line_container(self) -> Container:
        text_line = Container(classes="text_line")
        text_line.styles.layer = f"layer_{self._current_line_idx}"
        text_line.styles.margin = (self._current_line_idx, 0, 0, 0)
        self._text_field.mount(text_line, after=-1)
        return text_line

    @property
    def _current_char(self) -> str:
        return self._text_lines[self._current_line_idx].text[self._current_char_idx]

    @property
    def _current_text_line_length(self) -> int:
        return self._text_lines[self._current_line_idx].length

    @property
    def _current_text_line_container(self) -> Container:
        try:
            return self._text_field.query(Container).last()
        except NoMatches:
            return self._add_new_text_line_container()
