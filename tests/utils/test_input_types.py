from unittest.mock import ANY, Mock, patch

from prompt_toolkit.validation import Validator

from qwikstart.utils import input_types


class TestNumberRange:
    def test_inclusive_range_is_valid(self) -> None:
        number_range = input_types.NumberRange(1, 5)
        assert number_range.is_valid("1") is True
        assert number_range.is_valid("5") is True

    def test_below_range_is_not_valid(self) -> None:
        assert input_types.NumberRange(1, 5).is_valid("0") is False

    def test_above_range_is_not_valid(self) -> None:
        assert input_types.NumberRange(1, 5).is_valid("6") is False

    def test_non_number_is_not_valid(self) -> None:
        assert input_types.NumberRange(1, 5).is_valid("bad") is False

    def test_cast(self) -> None:
        assert input_types.NumberRange(1, 5).cast("3") == 3

    def test_validator(self) -> None:
        assert isinstance(input_types.NumberRange(1, 5).validator, Validator)

    @patch.object(input_types, "ptk_prompt", return_value="3")
    def test_ptk_prompt_initialization(self, ptk_prompt: Mock) -> None:
        number_range = input_types.NumberRange(1, 5)
        assert number_range.raw_prompt("Enter number") == "3"
        ptk_prompt.assert_called_once_with(
            "Enter number: ", completer=None, validator=ANY
        )

    @patch.object(input_types, "ptk_prompt", return_value="3")
    def test_prompt_response_cast_to_int(self, ptk_prompt: Mock) -> None:
        number_range = input_types.NumberRange(1, 5)
        assert number_range.prompt("Enter number") == 3
