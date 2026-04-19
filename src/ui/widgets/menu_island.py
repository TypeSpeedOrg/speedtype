import asyncio

from rich.repr import Result
from textual.app import ComposeResult
from textual.message import Message
from textual.widgets import Label

from ui.constants.classes import CSSClass
from ui.constants.colors import FOCUS_TEXT_COLOR, MENU_BACKGROUND_COLOR, REGULAR_TEXT_COLOR
from ui.widgets.base import BaseWidget


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
        color: {REGULAR_TEXT_COLOR};
        height: auto;
        width: auto;
        padding: 1 3;
        background: {MENU_BACKGROUND_COLOR};
    }}
    """

    def __init__(self, *args, label: str, **kwargs):
        super().__init__(*args, **kwargs)
        self._label = label

    def compose(self) -> ComposeResult:
        yield Label(self._label)


class MenuIslandButton(BaseWidget):
    DEFAULT_CSS = f"""
    MenuIslandButton {{
        background: {MENU_BACKGROUND_COLOR};
        color: {REGULAR_TEXT_COLOR};
        height: auto;
        width: auto;
        padding: 1 3;
        
        &.hover {{
            text-style: underline;
            background: #161730;
            color: {FOCUS_TEXT_COLOR};
        }}
    }}
    """

    class Pressed(Message):

        def __init__(self, value: str) -> None:
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
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._label = label
        self._value = value
        self._persist_click = persist_click

    def compose(self) -> ComposeResult:
        yield Label(self._label)

    def on_enter(self) -> None:
        self.add_class("hover")

    def on_leave(self) -> None:
        self.remove_class("hover")

    async def on_click(self) -> None:
        self.add_class(CSSClass.SELECTED)

        if not self._persist_click:
            await asyncio.sleep(0.1)
            self.remove_class(CSSClass.SELECTED)

        self.post_message(self.Pressed(value=self._value))

    @property
    def value(self) -> str:
        return self._value
