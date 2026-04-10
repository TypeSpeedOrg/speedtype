import asyncio

from rich.repr import Result
from textual.app import ComposeResult
from textual.events import Click, Enter, Leave
from textual.message import Message
from textual.widgets import Static

from ui.constants.classes import CSSClass
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
    DEFAULT_CSS = """
    MenuIslandText {
        color: #5f647a;
        height: auto;
        width: auto;
        padding: 1 3;
        background: #101224;
    }
    """

    def __init__(self, *args, label: str, **kwargs):
        super().__init__(*args, **kwargs)
        self._label = label

    def compose(self) -> ComposeResult:
        yield Static(self._label)

    def on_click(self, event: Click) -> None:
        event.stop()


class MenuIslandButton(BaseWidget):
    DEFAULT_CSS = f"""
    MenuIslandButton {{
        background: #101224;
        color: #5f647a;
        height: auto;
        width: auto;
        padding: 1 3;
        
        &.{CSSClass.HOVER} {{
            text-style: underline;
            background: #161730;
            color: #787E9C;
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
        yield Static(self._label)

    def on_enter(self, event: Enter) -> None:
        self.add_class(CSSClass.HOVER)

    def on_leave(self, event: Leave) -> None:
        self.remove_class(CSSClass.HOVER)

    async def on_click(self, event: Click) -> None:
        self.add_class(CSSClass.SELECTED)

        if not self._persist_click:
            await asyncio.sleep(0.1)
            self.remove_class(CSSClass.SELECTED)

        event.stop()
        self.post_message(self.Pressed(value=self._value))

    @property
    def value(self) -> str:
        return self._value
