from textual.app import ComposeResult

from speedtype.ui.widgets.base import BaseWidget
from speedtype.ui.widgets.typing_value_stats.stats_section import StatsSection


class TypingValueStats(BaseWidget):
    DEFAULT_CSS = """
    TypingValueStats {
        layout: grid;
        padding: 1 1 0 0;
        grid-gutter: 1 0;
        grid-size: 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield StatsSection(label="WPM")
        yield StatsSection(label="CORRECTLY SYMBOLS")
        yield StatsSection(label="INVALID SYMBOLS")
