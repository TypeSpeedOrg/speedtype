import asyncio
from enum import StrEnum, auto

from rich.repr import Result
from textual import events, on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.message import Message
from textual.widgets import Label

from speedtype.ui.constants.classes import CSSClass
from speedtype.ui.widgets.base import BaseWidget


class ButtonStyle(StrEnum):
    REGULAR = auto()
    ABORT = auto()


class MenuIslandButton(BaseWidget, can_focus=True):
    DEFAULT_CSS = f"""
    MenuIslandButton {{
        height: auto;
        width: auto;
        padding: 1 3;

        &.{ButtonStyle.REGULAR} {{
            background: $surface;
        }}

        &.{ButtonStyle.ABORT} {{
            background: $accent;
            color: $accent-color;
        }}

        &.hover-{ButtonStyle.REGULAR} {{
            text-style: underline;
            background: $hover-background;
            color: $hover-foreground;
        }}

        &.hover-{ButtonStyle.ABORT} {{
            text-style: underline;
            background: $accent-hover-background;
            color: $accent-hover-color;
        }}
    }}
    """
    BINDINGS = [
        Binding(
            key="enter",
            action="press_buton",
            description="Press Button",
            key_display="enter",
            priority=True,
        ),
    ]

    class Pressed(Message):
        def __init__(
            self,
            value: str,
        ) -> None:
            self.value = value
            super().__init__()

        def __rich_repr__(self) -> Result:
            yield "value", self.value

    def __init__(
        self,
        *args,
        label: str,
        value: str | None,
        persist_click: bool,
        button_style: ButtonStyle = ButtonStyle.REGULAR,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._label = label
        self._value = value
        self._persist_click = persist_click
        self._button_style = button_style

        self.add_class(self._button_style)

    def compose(self) -> ComposeResult:
        yield Label(self._label)

    @on(events.Click)
    async def action_press_buton(self) -> None:
        self.add_class(CSSClass.SELECTED)

        if not self._persist_click:
            await asyncio.sleep(0.1)
            self.remove_class(CSSClass.SELECTED)

        self.post_message(self.Pressed(value=self._value))

    @property
    def value(self) -> str:
        return self._value

    @on(events.Enter)
    @on(events.Focus)
    def _button_selected(self) -> None:
        self.add_class(f"hover-{self._button_style}")

    @on(events.Leave)
    @on(events.Blur)
    def _button_left(self, event: events.Blur | events.Leave) -> None:
        if not self.has_focus or isinstance(event, events.Blur):
            self.remove_class(f"hover-{self._button_style}")
