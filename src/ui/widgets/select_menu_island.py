from textual.app import ComposeResult
from textual.events import Click
from textual.widget import Widget

from ui.css.classes import CSSClass
from ui.widgets.menu_island import MenuIslandButton


class SectionMenuIsland(Widget):
    DEFAULT_CSS = """
    SectionMenuIsland {
        layout: horizontal;
        width: auto;
        height: auto;
    }
    """

    def __init__(
        self,
        *args,
        options: tuple[str | tuple[str, str], ...],
        persistent: bool,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._labels = tuple(option if isinstance(option, tuple) else (option, None) for option in options)
        self._persistent = persistent

    def compose(self) -> ComposeResult:
        for (option, css_classes) in self._labels:
            yield MenuIslandButton(
                label=option,
                classes=css_classes,
                persist_click=self._persistent,
            )

    def on_click(self, event: Click) -> None:
        if not self._persistent:
            return

        clicked_button = next(
            widget for widget in event.control.ancestors_with_self
            if isinstance(widget, MenuIslandButton)
        )

        for previous_selected_button in self.query_children(f"MenuIslandButton.{CSSClass.SELECTED}"):
            if previous_selected_button != clicked_button:
                previous_selected_button.remove_class(CSSClass.SELECTED)
