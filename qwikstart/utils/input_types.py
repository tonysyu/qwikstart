import abc
from typing import Any, Generic, Optional, TypeVar, cast

from prompt_toolkit import prompt as ptk_prompt
from prompt_toolkit.completion import Completer
from prompt_toolkit.validation import Validator

T = TypeVar("T", covariant=True)


class InputType(Generic[T]):

    error_msg: str = "Input does not pass validation"
    completer: Optional[Completer] = None

    @property
    def validator(self) -> Validator:
        return Validator.from_callable(self.is_valid, error_message=self.error_msg)

    @abc.abstractmethod
    def is_valid(self, text: str) -> bool:
        pass  # pragma: no cover

    def cast(self, input_text: str) -> T:
        return cast(T, input_text)

    def raw_prompt(self, message: str, suffix: str = ": ", **prompt_kwargs: Any) -> str:
        return ptk_prompt(  # type: ignore
            message + suffix,
            completer=self.completer,
            validator=self.validator,
            **prompt_kwargs,
        )

    def prompt(self, message: str, **prompt_kwargs: Any) -> T:
        value = self.raw_prompt(message, **prompt_kwargs)
        return self.cast(value)


class NumberRange(InputType[int]):
    def __init__(self, min_value: int, max_value: int):
        self.min = min_value
        self.max = max_value
        self.error_msg = f"This input must be number between {self.min} and {self.max}"

    def is_valid(self, text: str) -> bool:
        try:
            number = self.cast(text)
        except ValueError:
            return False
        return self.min <= number <= self.max

    def cast(self, input_text: str) -> int:
        return int(input_text)


class StringInput(InputType[str]):
    error_msg: str = "Input cannot be empty"

    def __init__(self, allow_empty_response: bool = False):
        self.allow_empty_response = allow_empty_response

    def is_valid(self, text: str) -> bool:
        return bool(text.strip() or self.allow_empty_response)


class BoolInput(InputType[bool]):
    error_msg: str = "Response must be 'y' or 'n'"

    def is_valid(self, text: str) -> bool:
        return text.lower() in ("y", "n")

    def cast(self, input_text: str) -> bool:
        return input_text.lower() == "y"
