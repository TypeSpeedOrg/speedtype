from textual.app import ComposeResult
from textual.reactive import var

from speedtype.ui.types.session_stats import InputStats
from speedtype.ui.widgets.base import BaseWidget
from speedtype.ui.widgets.typing_value_stats.stats_section import StatsSection


class TypingValueStats(BaseWidget):
    DEFAULT_CSS = """
    TypingValueStats {
        layout: grid;
        grid-gutter: 1 0;
        grid-size: 1;
    }
    """
    input_stats: var[InputStats] = var(None, init=False)

    def compose(self) -> ComposeResult:
        yield StatsSection(label="WPM", classes="wpm-section")
        yield StatsSection(label="CORRECT SYMBOLS", classes="correct-chars-section")
        yield StatsSection(label="INVALID SYMBOLS", classes="invalid-chars-section")

    def watch_input_stats(self) -> None:
        self.query_one("StatsSection.wpm-section", StatsSection).value = self.input_stats.wpm
        self.query_one("StatsSection.correct-chars-section", StatsSection).value = self.input_stats.correct_chars_amount
        self.query_one("StatsSection.invalid-chars-section", StatsSection).value = self.input_stats.invalid_chars_amount
