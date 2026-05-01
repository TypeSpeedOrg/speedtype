import random
from itertools import repeat
from statistics import mean

from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import var
from textual.widgets import Label, Sparkline

from speedtype.ui.constants.colors import BLOCK_BG, BLOCK_COLOR, SELECTED_COLOR
from speedtype.ui.types.session_stats import InputStats
from speedtype.ui.widgets.base import BaseWidget
from speedtype.ui.widgets.wpm_plot.time_axis import TimeAxis
from speedtype.ui.widgets.wpm_plot.wpm_axis import WPMAxis


data = [i + random.randint(-5, 3) + 0.5 for i in repeat(50, 30)]


class WPMPlot(BaseWidget):
    DEFAULT_CSS = f"""
    WPMPlot {{
        background: {BLOCK_BG};
        color: {BLOCK_COLOR};
        layout: vertical;
        padding: 1 5 1 2;

        .title {{
            text-align: center;
            width: 100%;
        }}

        .plot {{
            padding: 1 0 0 0;
            layout: grid;
            grid-size: 2 2;
            grid-rows: 1fr 2;
            grid-columns: 6 1fr;

            Sparkline {{
                height: 100%;

                .sparkline--max-color {{
                    color: {SELECTED_COLOR};
                }}

                .sparkline--min-color {{
                    color: #f2a218;
                }}
            }}
        }}
    }}
    """
    input_stats: var[InputStats] = var(None, init=False)

    def compose(self) -> ComposeResult:
        yield Label("WORDS PER MINUTE CHART", classes="title")
        with Container(classes="plot"):
            yield WPMAxis()
            yield Sparkline(data, summary_function=mean)
            yield Container()
            yield TimeAxis()
