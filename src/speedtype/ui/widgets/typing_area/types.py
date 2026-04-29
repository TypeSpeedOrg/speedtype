from contextlib import suppress
from dataclasses import dataclass, field

from funcy import memoize


@dataclass(kw_only=True, slots=True)
class TextLine:
    words: tuple[str]
    length: int
    text: str = field(init=False)
    input_words: list[InputWord] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.text = "".join(self.words)

    @memoize(key_func=lambda *args, **kwargs: (id(args[0]), kwargs["char_idx"]))
    def get_word_at_char_idx(self, *, char_idx: int, ) -> InputWord:
        word_indexes = {char_idx}

        start_idx = char_idx
        with suppress(IndexError):
            while self.text[start_idx] != " ":
                word_indexes.add(start_idx)
                start_idx -= 1

        end_idx = char_idx
        with suppress(IndexError):
            while True:
                word_indexes.add(end_idx)
                end_idx += 1

                if self.text[end_idx] == " ":
                    break

        input_word = InputWord(correct_chars=0, total_chars=len(word_indexes))

        self.input_words.append(input_word)
        self.get_word_at_char_idx.memory.update({(id(self), char_idx): input_word for char_idx in word_indexes})

        return input_word

    def __del__(self) -> None:
        self.get_word_at_char_idx.invalidate_all()


@dataclass(kw_only=True, slots=True)
class InputWord:
    correct_chars: int
    total_chars: int
    invalid_chars: list[str] = field(default_factory=list)

    def inc_correct_chars(self) -> None:
        self.correct_chars += 1

    def dec_correct_chars(self) -> None:
        self.correct_chars -= 1

    def add_invalid_char(self, *, char: str, ) -> None:
        self.invalid_chars.append(char)

    @property
    def plain(self) -> tuple[int, int, list[str]]:
        return self.correct_chars, self.total_chars, self.invalid_chars
