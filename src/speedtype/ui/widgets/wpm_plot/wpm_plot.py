from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import var
from textual.widgets import Label

from speedtype.ui.types.session_stats import InputStats
from speedtype.ui.types.wpm_plot import PlotData
from speedtype.ui.widgets.base import BaseWidget
from speedtype.ui.widgets.wpm_plot.plot import Plot
from speedtype.ui.widgets.wpm_plot.time_axis import TimeAxis
from speedtype.ui.widgets.wpm_plot.wpm_axis import WPMAxis


class WPMPlot(BaseWidget):
    DEFAULT_CSS = """
    WPMPlot {
        background: $surface;
        layout: vertical;
        padding: 1 5 1 2;

        .title {
            text-align: center;
            width: 100%;
        }

        .plot {
            padding: 1 0 0 0;
            layout: grid;
            grid-size: 2 2;
            grid-rows: 1fr 2;
            grid-columns: 6 1fr;
        }
    }
    """
    input_stats: var[InputStats] = var(None, init=False)

    def compose(self) -> ComposeResult:
        yield Label("WORDS PER MINUTE CHART", classes="title")
        with Container(classes="plot"):
            yield WPMAxis()
            yield Plot()
            yield Container()
            yield TimeAxis()

    def watch_input_stats(self) -> None:
        plot_data = PlotData(
            typed_chars_per_second=self.input_stats.typed_chars_per_second,
            mean_words_size=self.input_stats.mean_words_size,
            input_time=self.input_stats.input_time,
        )

        self.query_one(WPMAxis).wpm_borders = (0, plot_data.top_wpm_border // 2, plot_data.top_wpm_border)
        self.query_one(TimeAxis).input_time = self.input_stats.input_time
        self.query_one(Plot).plot_data = plot_data
