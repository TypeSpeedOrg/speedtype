import asyncio
from collections.abc import Coroutine
from contextlib import suppress
from datetime import datetime, timedelta
from enum import StrEnum, auto

from textual import events, on, work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.css.query import NoMatches
from textual.events import Key
from textual.message import Message
from textual.reactive import var
from textual.widgets import Label
from textual.worker import Worker

from speedtype.ui.constants.classes import CSSClass
from speedtype.ui.types.typing_area import InputWord, TextLine, WordStats
from speedtype.ui.widgets.base import BaseWidget


TEXT_LINE_CONTAINER_CLS = "text_line_container"
PLACEHOLDER_CONTAINER_ID = "placeholder_container"
LINE_ARROW_ID = "text_line_arrow"

INPUT_ANIMATION_DURATION = 0.7
INPUT_TEXT_OPACITY_LIMIT = 0.5
OPACITY_SPEED = (1 - INPUT_TEXT_OPACITY_LIMIT) / INPUT_ANIMATION_DURATION


class TextMark(StrEnum):
    INVALID = auto()
    CORRECT = auto()


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
                    color: $invalid-text-color;
                    background: $invalid-text-background 20%;
                }}

                &.{TextMark.CORRECT} {{
                    color: $correct-text-color;
                    background: $correct-text-background 20%;
                }}
            }}
        }}
    }}
    """
    BINDINGS = [
        Binding(
            key="ctrl+s",
            action="stop",
            description="Stop typing",
        )
    ]
    text: var[str] = var("", init=False)
    input_time: var[int] = var(None, init=False)

    class TypingStarted(Message):
        pass

    class TypingStopped(Message):
        pass

    class TypingFinished(Message):
        def __init__(
            self,
            typed_words: list[WordStats],
            input_time: int,
            typed_chars_per_second: list[float],
        ) -> None:
            self.typed_words = typed_words
            self.input_time = input_time
            self.typed_chars_per_second = typed_chars_per_second
            super().__init__()

    def __init__(
        self,
        *args,
        line_length: int,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self._input_animation: Worker[Coroutine[None, None, None]] | None = None

        self._line_length_limit = line_length
        self._text_lines: list[TextLine] = []

        self._current_line_idx = 0
        self._current_char_idx = 0
        self._current_word_idx = 0
        self._correct_chars_collector = 0
        self._typed_chars_per_second = []

        self._pause_typing_until: datetime = datetime.now()
        self._is_typing = False

    def compose(self) -> ComposeResult:
        yield Label(">", id=LINE_ARROW_ID, classes=CSSClass.SELECTED)
        yield Container(id=PLACEHOLDER_CONTAINER_ID)

    def watch_text(self) -> None:
        if not self.text:
            return

        self._text_lines = []
        current_line_length = 0
        line_words = []

        for word in self.text.split():
            word_length = len(word) + 1

            if current_line_length + word_length < self._line_length_limit:
                line_words.extend((word, " "))
                current_line_length += word_length
            else:
                self._text_lines.append(TextLine.new(words=tuple(line_words)))
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

    def action_stop(self) -> None:
        self.stop(is_finished=False)

    def check_action(self, action: str, parameters: tuple[object, ...]) -> bool | None:  # noqa: ARG002
        return self._is_typing if action == "stop" else None

    def stop(self, *, is_finished: bool) -> None:
        self._is_typing = False

        if is_finished:
            self._pause_typing_until = datetime.now() + timedelta(seconds=0.5)
            self.post_message(
                self.TypingFinished(
                    typed_words=[
                        word.plain for line in self._text_lines for word in line.input_words if line.input_words
                    ],
                    input_time=self.input_time,
                    typed_chars_per_second=self._typed_chars_per_second,
                )
            )
        else:
            self.post_message(self.TypingStopped())

        self._typed_chars_per_second = []
        self._current_line_idx = 0
        self._current_char_idx = 0
        self._current_word_idx = 0
        self._correct_chars_collector = 0
        self._text_lines = []
        self._input_animation = self._waiting_to_input_animation()

        for text_line in self.query(Container).filter(f".{TEXT_LINE_CONTAINER_CLS}"):
            text_line.remove()

        self._move_arrow_to_line(line_idx=0)
        self.refresh_bindings()

    def _start(self) -> None:
        self._is_typing = True
        self._animate_input(
            value=1,
            easing="in_out_quad",
            duration=self._get_remaining_input_animation_duration(final_value=1),
        )
        self._start_timer()
        self.refresh_bindings()
        self.post_message(self.TypingStarted())

    def _remove_char(self) -> None:
        if self._current_char_idx == 0:
            return

        text_label = self._get_last_label()
        removed_char = text_label.content[-1]

        if len(text_label.content) == 1:
            text_label.remove()
        else:
            text_label.content = text_label.content[:-1]

        self._current_char_idx -= 1

        if self._current_char == removed_char:
            self._dec_correct_char()

    def _add_space(self) -> None:
        if self._current_char != " ":
            text_label = self._get_text_label(mark=TextMark.INVALID)

            while self._current_char != " ":
                text_label.content += self._current_char
                self._inc_current_char_idx()

            text_label.content += " "

        elif self._current_char_idx + 1 != self._current_text_line_length:
            self._get_text_label(mark=TextMark.CORRECT).content += " "
            self._inc_correct_char()

        self._inc_current_char_idx()

    def _add_char(
        self,
        *,
        char: str,
    ) -> None:
        is_correct_char = char == self._current_char

        if is_correct_char:
            self._inc_correct_char()
        else:
            self._current_input_word.add_invalid_char(char=char)

        text_label = self._get_text_label(
            mark=TextMark.CORRECT if is_correct_char else TextMark.INVALID,
        )
        text_label.content += char
        self._inc_current_char_idx()

    def _get_text_label(
        self,
        *,
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

    def _create_new_line(self) -> Container:
        text_line_container = Container(classes=TEXT_LINE_CONTAINER_CLS)
        text_line_container.styles.layer = f"layer_{self._current_line_idx}"
        text_line_container.styles.margin = (self._current_line_idx, 0, 0, 2)
        self.mount(text_line_container, after=-1)
        self._move_arrow_to_line(line_idx=self._current_line_idx)
        return text_line_container

    def _move_arrow_to_line(
        self,
        line_idx: int,
    ) -> None:
        self.get_widget_by_id(LINE_ARROW_ID, Label).styles.padding = (line_idx, 1, 0, 0)

    def _inc_current_char_idx(self) -> None:
        self._current_char_idx += 1

        if self._current_char_idx == self._current_text_line_length:
            self._current_line_idx += 1
            self._current_char_idx = 0
            self._create_new_line()

    def _inc_correct_char(self) -> None:
        self._current_input_word.inc_correct_chars()
        self._correct_chars_collector += 1

    def _dec_correct_char(self) -> None:
        self._current_input_word.dec_correct_chars()
        if self._correct_chars_collector:
            self._correct_chars_collector -= 1

    def _animate_input(self, value: float, easing: str, duration: float) -> None:
        self.get_widget_by_id(PLACEHOLDER_CONTAINER_ID, Container).styles.animate(
            "opacity",
            value=value,
            duration=duration,
            easing=easing,
        )

    @on(events.Focus)
    def _start_animation(self) -> None:
        if not self._is_typing:
            self._input_animation = self._waiting_to_input_animation()

        if self._is_typing:
            self._animate_input(
                value=1,
                easing="in_out_quad",
                duration=self._get_remaining_input_animation_duration(final_value=1),
            )

    @on(events.Blur)
    def _disable_animation(self) -> None:
        self._input_animation.cancel()

        self._animate_input(
            value=INPUT_TEXT_OPACITY_LIMIT,
            easing="in_out_quad",
            duration=self._get_remaining_input_animation_duration(final_value=INPUT_TEXT_OPACITY_LIMIT),
        )

    @on(events.Key)
    def _process_typed_symbol(
        self,
        event: Key,
    ) -> None:
        if datetime.now() < self._pause_typing_until:
            return

        if not event.is_printable and event.name != "backspace":
            return

        if not self._is_typing:
            self._start()

        match event.name, event.character:
            case "backspace", _:
                self._remove_char()
            case "space", _:
                self._add_space()
            case _, char:
                self._add_char(char=char)

    @work(exclusive=True)
    async def _waiting_to_input_animation(self) -> None:
        while True:
            self._animate_input(
                value=1,
                easing="in_out_quad",
                duration=INPUT_ANIMATION_DURATION,
            )
            await asyncio.sleep(INPUT_ANIMATION_DURATION)
            self._animate_input(
                value=INPUT_TEXT_OPACITY_LIMIT,
                easing="in_out_quad",
                duration=INPUT_ANIMATION_DURATION,
            )
            await asyncio.sleep(INPUT_ANIMATION_DURATION)

    @work(exclusive=True)
    async def _start_timer(self) -> None:
        remaining_seconds = self.input_time

        while remaining_seconds > 0:
            await asyncio.sleep(1)
            self._typed_chars_per_second.append(self._correct_chars_collector)
            self._correct_chars_collector = 0
            remaining_seconds -= 1

        self.stop(is_finished=True)

    @property
    def _current_text_line(self) -> TextLine:
        return self._text_lines[self._current_line_idx]

    @property
    def _current_input_word(self) -> InputWord:
        return self._current_text_line.get_word_at_char_idx(char_idx=self._current_char_idx)

    @property
    def _current_char(self) -> str:
        return self._current_text_line.text[self._current_char_idx]

    @property
    def _current_text_line_length(self) -> int:
        return self._current_text_line.length

    @property
    def _current_text_line_container(self) -> Container:
        try:
            return self.query(Container).filter(f".{TEXT_LINE_CONTAINER_CLS}").last()
        except NoMatches:
            return self._create_new_line()

    def _get_remaining_input_animation_duration(self, *, final_value: float) -> float:
        current_opacity = self.get_widget_by_id(PLACEHOLDER_CONTAINER_ID, Container).styles.opacity
        return abs(final_value - current_opacity) / OPACITY_SPEED
