from collections.abc import Sequence

from textual.app import ComposeResult
from textual.reactive import var
from textual.widgets import Sparkline

from speedtype.ui.types.wpm_plot import PlotData
from speedtype.ui.widgets.base import BaseWidget


class Plot(BaseWidget):
    DEFAULT_CSS = """
    Plot {
        Sparkline {
            height: 100%;
        }
    }
    """
    plot_data: var[PlotData] = var(None, init=False)

    def compose(self) -> ComposeResult:
        yield Sparkline(summary_function=self._summary_function)

    def watch_plot_data(self) -> None:
        sparkline = self.query_one(Sparkline)
        sparkline.data = list(range(self.plot_data.input_time - 1)) + [self.plot_data.top_wpm_border]

    def _summary_function(self, value: Sequence[float]) -> float:
        value_idx = value[0]
        if value_idx == self.plot_data.top_wpm_border:
            return self.plot_data.wpm_approx[-1]
        return self.plot_data.wpm_approx[value_idx]
