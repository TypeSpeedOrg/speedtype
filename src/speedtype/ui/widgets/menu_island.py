import asyncio
from enum import StrEnum, auto

from rich.repr import Result
from textual.app import ComposeResult
from textual.message import Message
from textual.widgets import Label

from speedtype.ui.constants.classes import CSSClass
from speedtype.ui.constants.colors import (
    ABORT_BLOCK_BG,
    ABORT_BLOCK_COLOR,
    ABORT_HOVER_BG,
    ABORT_HOVER_COLOR,
    BLOCK_BG,
    BLOCK_COLOR,
    BLOCK_HOVER_BG,
    BLOCK_HOVER_COLOR,
)
from speedtype.ui.widgets.base import BaseWidget


class ButtonStyle(StrEnum):
    REGULAR = auto()
    ABORT = auto()


class MenuIsland(BaseWidget):
    DEFAULT_CSS = """
    MenuIsland {
        width: auto;
        height: auto;
        margin: 1;
        layout: horizontal;
    }
    """


class MenuIslandText(BaseWidget):
    DEFAULT_CSS = f"""
    MenuIslandText {{
        color: {BLOCK_COLOR};
        height: auto;
        width: auto;
        padding: 1 3;
        background: {BLOCK_BG};
    }}
    """

    def __init__(
        self,
        *args,
        label: str,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._label = label

    def compose(self) -> ComposeResult:
        yield Label(self._label)


class MenuIslandButton(BaseWidget):
    DEFAULT_CSS = f"""
    MenuIslandButton {{
        height: auto;
        width: auto;
        padding: 1 3;

        &.{ButtonStyle.REGULAR} {{
            background: {BLOCK_BG};
            color: {BLOCK_COLOR};
        }}

        &.{ButtonStyle.ABORT} {{
            background: {ABORT_BLOCK_BG};
            color: {ABORT_BLOCK_COLOR};
        }}

        &.hover-{ButtonStyle.REGULAR} {{
            text-style: underline;
            background: {BLOCK_HOVER_BG};
            color: {BLOCK_HOVER_COLOR};
        }}

        &.hover-{ButtonStyle.ABORT} {{
            text-style: underline;
            background: {ABORT_HOVER_BG};
            color: {ABORT_HOVER_COLOR};
        }}
    }}
    """

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

    def on_enter(self) -> None:
        self.add_class(f"hover-{self._button_style}")

    def on_leave(self) -> None:
        self.remove_class(f"hover-{self._button_style}")

    async def on_click(self) -> None:
        self.add_class(CSSClass.SELECTED)

        if not self._persist_click:
            await asyncio.sleep(0.1)
            self.remove_class(CSSClass.SELECTED)

        self.post_message(self.Pressed(value=self._value))

    @property
    def value(self) -> str:
        return self._value
