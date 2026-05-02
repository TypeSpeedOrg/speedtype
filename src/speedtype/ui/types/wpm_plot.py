from dataclasses import dataclass

from funcy import cached_readonly, lmap


@dataclass(kw_only=True, frozen=True)
class PlotData:
    typed_chars_per_second: list[float]
    mean_words_size: int
    input_time: int

    @cached_readonly
    def wpm_approx(self) -> list[float]:
        return lmap(lambda v: int(v / self.mean_words_size * 60), self.typed_chars_per_second)

    @cached_readonly
    def top_wpm_border(self) -> int:
        return ((wpm_tens := max(self.wpm_approx) // 10) + wpm_tens // 2) * 10
