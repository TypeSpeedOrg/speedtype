import asyncio
from contextlib import suppress
from enum import StrEnum, auto
from typing import NamedTuple

from textual import work
from textual.app import ComposeResult
from textual.containers import Container
from textual.css.query import NoMatches
from textual.events import Key
from textual.message import Message
from textual.reactive import reactive
from textual.widgets import Label

from speedtype.ui.constants.classes import CSSClass
from speedtype.ui.constants.colors import (
    CORRECT_TEXT_BACKGROUND,
    CORRECT_TEXT_COLOR,
    INVALID_TEXT_BACKGROUND,
    INVALID_TEXT_COLOR,
)
from speedtype.ui.widgets.base import BaseWidget


TEXT_LINE_CONTAINER_CLS = "text_line_container"
PLACEHOLDER_CONTAINER_ID = "placeholder_container"
LINE_ARROW_ID = "text_line_arrow"


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
    DEFAULT_CSS = f"""
    TextInput {{
        width: 100%;
        height: 100%;
        layout: horizontal;

        #{LINE_ARROW_ID} {{
            width: auto;
            height: auto;
            padding: 0 1 0 0;
        }}

        #{PLACEHOLDER_CONTAINER_ID} {{
            height: 100%;
            width: 100%;
            layout: vertical;

            Label {{
                width: 100%;
                height: auto;
                text-wrap: wrap;
                text-overflow: fold;
                opacity: 100%;
            }}
        }}

        .{TEXT_LINE_CONTAINER_CLS} {{
            layout: horizontal;
            width: auto;
            height: auto;

            Label {{
                width: auto;
                height: auto;

                &.{TextMark.INVALID} {{
                    color: {INVALID_TEXT_COLOR};
                    background: {INVALID_TEXT_BACKGROUND} 20%;
                }}

                &.{TextMark.CORRECT} {{
                    color: {CORRECT_TEXT_COLOR};
                    background: {CORRECT_TEXT_BACKGROUND} 20%;
                }}
            }}
        }}
    }}
    """
    text: reactive[str] = reactive("")
    is_typing: reactive[bool | None] = reactive(None)

    class TypingStarted(Message):
        pass

    def __init__(
        self,
        *args,
        line_length: int,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self._line_length_limit = line_length
        self._text_lines: list[TextLine] = []

        self._current_line_idx = 0
        self._current_char_idx = 0
        self._current_word_idx = 0

    def compose(self) -> ComposeResult:
        yield Label(">", id=LINE_ARROW_ID, classes=CSSClass.SELECTED)
        yield Container(id=PLACEHOLDER_CONTAINER_ID)

    def on_key(
        self,
        event: Key,
    ) -> None:
        if not self.is_typing:
            self.post_message(self.TypingStarted())

        self.is_typing = True
        self.process_typed_char(
            name=event.name,
            char=event.character,
            is_printable=event.is_printable,
        )

    def on_focus(self) -> None:
        self._waiting_to_input_animation()

    def watch_is_typing(self, is_typing_started: bool) -> None:
        if is_typing_started:
            self._waiting_to_input_animation().cancel()

        else:
            self._reset()

    def watch_text(self) -> None:
        self._text_lines = []
        current_line_length = 0
        line_words = []

        for word in self.text.split():
            word_length = len(word) + 1

            if current_line_length + word_length < self._line_length_limit:
                line_words.extend((word, " "))
                current_line_length += word_length

            else:
                self._text_lines.append(
                    TextLine(
                        words=tuple(line_words),
                        length=current_line_length,
                    ),
                )
                line_words = []
                current_line_length = 0

        self.styles.layers = " ".join(f"line_{i}" for i in range(len(self._text_lines)))
        placeholder_container = self.get_widget_by_id(
            PLACEHOLDER_CONTAINER_ID,
            Container,
        )

        for placeholder_label in placeholder_container.query(Label):
            placeholder_label.remove()

        for text_line in self._text_lines:
            placeholder_container.mount(Label(text_line.text))

    def process_typed_char(
        self,
        name: str,
        char: str,
        is_printable: bool,
    ) -> None:
        match name, char, is_printable:
            case "backspace", _, _:
                self._remove_char()
            case "space", _, _:
                self._add_space()
            case _, _, True:
                self._add_char(char)

    def _reset(self) -> None:
        self._current_line_idx = 0
        self._current_char_idx = 0
        self._current_word_idx = 0
        self._move_arrow_to_line(0)

        for text_line in self.query(Container).filter(f".{TEXT_LINE_CONTAINER_CLS}"):
            text_line.remove()

    def _remove_char(self) -> None:
        if self._current_char_idx == 0:
            return

        text_label = self._get_last_label()

        if len(text_label.content) == 1:
            text_label.remove()
        else:
            text_label.content = text_label.content[:-1]

        self._current_char_idx -= 1

    def _add_space(self) -> None:
        if self._current_char != " ":
            text_label = self._get_text_label(mark=TextMark.INVALID)

            while self._current_char != " ":
                text_label.content += self._current_char
                self._inc_current_char_idx()

        if self._current_char_idx + 1 != self._current_text_line_length:
            self._get_text_label(mark=TextMark.CORRECT).content += " "

        self._inc_current_char_idx()

    def _add_char(
        self,
        character: str,
    ) -> None:
        is_char_valid = character == self._current_char
        text_label = self._get_text_label(
            mark=TextMark.CORRECT if is_char_valid else TextMark.INVALID,
        )
        text_label.content += character
        self._inc_current_char_idx()

    def _get_text_label(
        self,
        mark: TextMark,
    ) -> Label:
        last_label = self._get_last_label()

        if last_label and last_label.has_class(mark):
            return last_label

        label = Label(classes=mark)
        self._current_text_line_container.mount(label)
        return label

    def _get_last_label(self) -> Label | None:
        with suppress(NoMatches):
            return self._current_text_line_container.query(Label).last()

        return None

    def _inc_current_char_idx(self) -> None:
        self._current_char_idx += 1

        if self._current_char_idx == self._current_text_line_length:
            self._current_line_idx += 1
            self._current_char_idx = 0
            self._move_to_new_line()

    def _move_to_new_line(self) -> Container:
        text_line_container = Container(classes=TEXT_LINE_CONTAINER_CLS)
        text_line_container.styles.layer = f"layer_{self._current_line_idx}"
        text_line_container.styles.margin = (self._current_line_idx, 0, 0, 2)
        self.mount(text_line_container, after=-1)
        self._move_arrow_to_line(self._current_line_idx)
        return text_line_container

    def _move_arrow_to_line(
        self,
        line_idx: int,
    ) -> None:
        self.get_widget_by_id(LINE_ARROW_ID, Label).styles.padding = (line_idx, 1, 0, 0)

    @property
    def _current_char(self) -> str:
        return self._text_lines[self._current_line_idx].text[self._current_char_idx]

    @property
    def _current_text_line_length(self) -> int:
        return self._text_lines[self._current_line_idx].length

    @property
    def _current_text_line_container(self) -> Container:
        try:
            return self.query(Container).filter(f".{TEXT_LINE_CONTAINER_CLS}").last()
        except NoMatches:
            return self._move_to_new_line()

    @work(exclusive=True)
    async def _waiting_to_input_animation(self) -> None:
        duration = 0.8

        async def animate_input(value: float, easing: str) -> None:
            self.get_widget_by_id(PLACEHOLDER_CONTAINER_ID, Container).styles.animate(
                "opacity",
                value=value,
                duration=duration,
                easing=easing,
            )
            await asyncio.sleep(duration)

        while True:
            await animate_input(0.5, "in_out_quad")
            await animate_input(1, "in_out_quad")
