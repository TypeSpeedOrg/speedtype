import asyncio
import random

from textual import on, work
from textual.app import ComposeResult
from textual.containers import Container
from textual.message import Message
from textual.reactive import reactive

from speedtype.ui.constants.colors import (
    BLOCK_BG_COLOR,
    BLOCK_COLOR,
    SELECTED_TEXT_COLOR,
)
from speedtype.ui.widgets.base import BaseWidget
from speedtype.ui.widgets.text_configuration import TextConfig, TextConfiguration
from speedtype.ui.widgets.text_input import TextInput


LINE_WIDTH = 140
TEXT_MOCK = """
alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi omicron pi rho sigma tau upsilon phi chi psi
omega apple banana cherry date elderberry fig grape honeydew kiwi lemon mango nectarine orange papaya quince
raspberry strawberry tangerine ugli watermelon apricot blackberry blueberry cantaloupe cranberry dragonfruit guava
jackfruit kumquat lime lychee mandarin mulberry passionfruit peach pear persimmon pineapple plum pomegranate
starfruit avocado broccoli cabbage carrot cauliflower celery cucumber eggplant garlic ginger kale lettuce mushroom
onion pepper potato pumpkin radish spinach squash tomato turnip zucchini almond cashew hazelnut peanut pecan
pistachio walnut bread butter cheese cream milk yogurt coffee tea water juice soda syrup sugar salt pepper basil
oregano thyme parsley rosemary dill cilantro mint vanilla cinnamon nutmeg clove gingerbread pancake waffle cereal
oatmeal rice pasta noodle pizza burger sandwich soup salad steak chicken turkey beef pork fish shrimp crab lobster
oyster salmon tuna cod sardine anchovy trout eagle falcon hawk sparrow pigeon crow raven owl parrot penguin flamingo
swan goose duck rooster hen lion tiger leopard cheetah panther jaguar elephant giraffe zebra rhinoceros hippopotamus
bear wolf fox coyote dog cat horse donkey camel goat sheep cow bull deer moose rabbit squirrel hamster guinea pig
mouse rat otter beaver dolphin whale shark octopus squid jellyfish coral algae moss fern tree flower grass bush vine
leaf root stem branch bark seed soil sand rock stone mountain valley river ocean lake pond island forest jungle
desert tundra glacier volcano canyon cliff hill plain plateau sky cloud rain snow hail storm wind breeze thunder
lightning rainbow sunrise sunset dawn dusk night day morning evening noon midnight spring summer autumn winter
january february march april may june july august september october november december monday tuesday wednesday
thursday friday saturday sunday time space matter energy force motion gravity friction velocity acceleration mass
weight density pressure temperature heat light sound color shape size length width height depth volume area circle
square triangle rectangle polygon sphere cube cylinder cone pyramid line point angle curve equation number digit
fraction decimal percent ratio algebra geometry calculus logic data code program function variable constant array
list stack queue graph tree network system process thread memory storage disk file folder path input output error
debug compile run build deploy test validate design model pattern structure architecture interface protocol package
module library framework engine kernel server client browser request response header body token session cookie cache
index query table row column key value hash map set filter sort search find replace insert update delete create drop
join merge split connect disconnect upload download sync async parallel sequential random ordered stable unstable
fast slow secure unsafe public private local global static dynamic simple complex basic advanced modern classic
digital analog virtual physical real abstract concrete linear nonlinear discrete continuous finite infinite open
closed start stop begin end first last next previous early late new old young ancient future past present current
temporary permanent optional required valid invalid true false yes no high low big small short long wide narrow thick
thin strong weak heavy light hard soft rough smooth bright dark clear blurry sharp dull noisy quiet calm active
passive happy sad angry joyful peaceful curious serious careful bold brave timid clever wise kind gentle honest loyal
fair equal free bound common rare unique normal strange simple tricky easy difficult possible impossible certain
uncertain known unknown visible hidden complete partial full empty ready busy safe risky clean dirty fresh stale rich
poor stronghold framework foundation baseline guide
"""


class TypingArea(BaseWidget):
    DEFAULT_CSS = f"""
    TypingArea {{
        width: 100%;
        height: 100%;
        color: {BLOCK_COLOR};
        align: center middle;

        .wrapper {{
            align: center middle;
            width: auto;
            padding: 1 0;

            border: hkey {BLOCK_BG_COLOR};
            border-title-align: left;
            border-title-color: {SELECTED_TEXT_COLOR};
            border-title-style: bold;
            border-title-background: {BLOCK_BG_COLOR};

            border-subtitle-align: right;
            border-subtitle-color: {SELECTED_TEXT_COLOR};
            border-subtitle-style: bold;
            border-subtitle-background: {BLOCK_BG_COLOR};

            .text {{
                width: {LINE_WIDTH};
                height: 100%;
            }}
        }}
    }}
    """
    text_config: reactive[TextConfig] = reactive(dict)
    text: reactive[str] = reactive("")
    is_typing: reactive[bool | None] = reactive(None)

    class TypingStopped(Message):
        pass

    def compose(self) -> ComposeResult:
        with (
            Container(classes="wrapper"),
            Container(classes="text"),
        ):
            yield TextInput(line_length=LINE_WIDTH).data_bind(
                TypingArea.text,
                TypingArea.is_typing,
            )

    def watch_text_config(self) -> None:
        config_values = []
        selected_time = ""

        for config_name, values in self.text_config.items():
            if config_name == TextConfiguration.Configuration.TIME:
                selected_time = values[0]
            else:
                config_values.extend(values)

        config_string = f" {', '.join(config_values)} "

        self._update_timer(selected_time)
        if self.query_one(Container).border_subtitle != config_string:
            self.query_one(Container).border_subtitle = f" {', '.join(config_values)} "
            self.regenerate_text()

    def watch_is_typing(
        self,
        is_typing: bool | None,
    ) -> None:
        if is_typing:
            self._start_timer()

        elif is_typing is False:
            self._start_timer().cancel()
            self._update_timer(
                self.text_config[TextConfiguration.Configuration.TIME][0],
            )
            self.regenerate_text()
            self.post_message(self.TypingStopped())
            self.query_one(TextInput).blur()

    def on_mount(self) -> None:
        self.regenerate_text()

    @on(TextInput.TypingStarted)
    def typing_started(self) -> None:
        self.is_typing = True

    def _update_timer(
        self,
        seconds: str | int,
    ) -> None:
        self.query_one(Container).border_title = f" {seconds} SEC "

    @staticmethod
    async def _load_input_text() -> str:
        # TODO: Mocking, in the future must do request to zeus
        words = TEXT_MOCK.split()
        random.shuffle(words)
        return " ".join(words)

    @work(exclusive=True)
    async def regenerate_text(self) -> None:
        self.text = await self._load_input_text()

    @work(exclusive=True)
    async def _start_timer(self) -> None:
        remaining_seconds = int(
            self.text_config[TextConfiguration.Configuration.TIME][0],
        )

        while remaining_seconds >= 0:
            self._update_timer(remaining_seconds)
            await asyncio.sleep(1)
            remaining_seconds -= 1

        self.is_typing = False
