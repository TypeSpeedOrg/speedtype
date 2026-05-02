from collections import defaultdict
from dataclasses import dataclass
from math import ceil, floor
from statistics import mean

from funcy import cached_readonly

from speedtype.ui.types.typing_area import WordStats


@dataclass(frozen=True, kw_only=True)
class InputStats:
    input_time: int
    words: list[WordStats]
    typed_chars_per_second: list[float]

    @cached_readonly
    def invalid_chars(self) -> dict[str, int]:
        invalid_symbols = defaultdict(int)

        for word in self.words:
            for invalid_symbol in word.invalid_chars:
                invalid_symbols[invalid_symbol] += 1

        return invalid_symbols

    @cached_readonly
    def invalid_chars_amount(self) -> int:
        return sum(self.invalid_chars.values())

    @cached_readonly
    def correct_chars_amount(self) -> int:
        return sum(word.correct_chars for word in self.words)

    @cached_readonly
    def wpm(self) -> int:
        words_amount = 0

        for word in self.words:
            if word.correct_chars == word.total_chars:
                words_amount += 1
            else:
                words_amount += word.correct_chars / word.total_chars

        return ceil(words_amount * (60 / self.input_time))

    @cached_readonly
    def mean_words_size(self) -> float:
        return floor(mean(word.total_chars for word in self.words))
