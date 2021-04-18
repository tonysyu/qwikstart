from typing import Callable, Type, TypeVar

TValidator = TypeVar("TValidator", bound="Validator")

class Validator:
    @classmethod
    def from_callable(
        cls: Type[TValidator], is_valid: Callable[[str], bool], error_message: str
    ) -> TValidator: ...
