from textual import events, on
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Footer

from speedtype.ui.constants.screens import AppScreen
from speedtype.ui.screens.base import BaseScreen
from speedtype.ui.screens.session_stats import TypingSessionStats
from speedtype.ui.types.session_stats import InputStats
from speedtype.ui.widgets.navigation_section import NavigationSection
from speedtype.ui.widgets.reload_text import ReloadTextButton
from speedtype.ui.widgets.stop_button import StopTypeButton
from speedtype.ui.widgets.text_configuration import TextConfiguration
from speedtype.ui.widgets.typing_area.area import TypingArea
from speedtype.ui.widgets.typing_area.text_input import TextInput


class TypingScreen(BaseScreen):
    DEFAULT_CSS = """
    TypingScreen {
        layout: vertical;
        overflow: hidden auto;

        .top {
            min-height: 0;
            max-height: 12;
        }

        .middle {
            height: 25;
        }

        .bottom {
            min-height: 7;
            layout: horizontal;
            width: 100%;
            align: center top;
            padding: 1 0 0 0;
        }
    }
    """

    def compose(self) -> ComposeResult:
        yield Container(classes="top")

        with Container(classes="middle"):
            yield TypingArea()

        with Container(classes="bottom"):
            yield ReloadTextButton()
            yield NavigationSection()
            yield TextConfiguration()
            yield StopTypeButton()

        yield Footer()

    @on(events.Mount)
    def _hide_stop_button(self) -> None:
        self.query_one(StopTypeButton).hide()

    @on(ReloadTextButton.Pressed)
    def _reload_button_pressed(self) -> None:
        self.query_one(TypingArea).regenerate_text()

    @on(StopTypeButton.Stopped)
    def _stop_button_pressed(self) -> None:
        self.query_one(TypingArea).stop()
        self.query_one(StopTypeButton).hide()
        self.query_one(ReloadTextButton).show()
        self.query_one(NavigationSection).show()
        self.query_one(TextConfiguration).show()

    @on(TextInput.TypingStarted)
    def _typing_started(self) -> None:
        self.query_one(StopTypeButton).show()
        self.query_one(ReloadTextButton).hide()
        self.query_one(NavigationSection).hide()
        self.query_one(TextConfiguration).hide()

    @on(TextInput.TypingFinished)
    def _typing_finished(
        self,
        event: TextInput.TypingFinished,
    ) -> None:
        self.query_one(StopTypeButton).hide()
        self.query_one(ReloadTextButton).show()
        self.query_one(NavigationSection).show()
        self.query_one(TextConfiguration).show()

        stats_screen: TypingSessionStats = self.app.get_screen(AppScreen.TYPING_SESSION_STATS)
        stats_screen.input_stats = InputStats(
            input_time=event.input_time,
            words=event.typed_words,
            typed_chars_per_second=event.typed_chars_per_second,
        )

        self.app.switch_screen(AppScreen.TYPING_SESSION_STATS)

    @on(TextConfiguration.ConfigUpdated)
    def _text_configuration_updated(
        self,
        event: TextConfiguration.ConfigUpdated,
    ) -> None:
        typing_area = self.query_one(TypingArea)
        typing_area.text_config = event.text_config
        typing_area.mutate_reactive(TypingArea.text_config)
