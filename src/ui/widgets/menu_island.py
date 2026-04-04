import asyncio

from textual.app import ComposeResult
from textual.events import Click, Enter, Leave
from textual.widget import Widget
from textual.widgets import Static

from ui.css.classes import CSSClass


class MenuIsland(Widget):
    DEFAULT_CSS = """
    MenuIsland {
        background: #101224;
        width: auto;
        height: auto;
        margin: 1;
        layout: horizontal;
    }
    """


class MenuIslandText(Widget):
    DEFAULT_CSS = """
    MenuIslandText {
        color: #5f647a;
        height: auto;
        width: auto;
        padding: 1 3;
    }
    """

    def __init__(self, *args, label: str, **kwargs):
        super().__init__(*args, **kwargs)
        self._label = label

    def compose(self) -> ComposeResult:
        yield Static(self._label)

    def on_click(self, event: Click) -> None:
        event.stop()


class MenuIslandButton(Widget):
    DEFAULT_CSS = f"""
    MenuIslandButton {{
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

    def __init__(
        self,
        *args,
        label: str,
        persist_click: bool,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._label = label
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
