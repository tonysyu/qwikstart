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


class TestStringInput:
    def test_empty_response_not_allowed_by_default(self) -> None:
        string_input = input_types.StringInput()
        assert string_input.is_valid("") is False

    @patch.object(input_types, "ptk_prompt", return_value="hi")
    def test_prompt_prefix(self, ptk_prompt: Mock) -> None:
        string_input = input_types.StringInput()
        assert string_input.prompt("Input", suffix="> ")
        ptk_prompt.assert_called_once_with("Input> ", completer=None, validator=ANY)

    def test_whitespace_treated_as_empty_response(self) -> None:
        string_input = input_types.StringInput()
        assert string_input.is_valid("\t") is False

    def test_empty_response_allowed(self) -> None:
        string_input = input_types.StringInput(allow_empty_response=True)
        assert string_input.is_valid("") is True


class TestBoolInput:
    def test_y_is_valid(self) -> None:
        bool_input = input_types.BoolInput()
        assert bool_input.is_valid("y") is True
        assert bool_input.is_valid("Y") is True

    def test_n_is_valid(self) -> None:
        bool_input = input_types.BoolInput()
        assert bool_input.is_valid("n") is True
        assert bool_input.is_valid("N") is True

    def test_empty_string_is_not_valid(self) -> None:
        bool_input = input_types.BoolInput()
        assert bool_input.is_valid("") is False

    @patch.object(input_types, "ptk_prompt", return_value="y")
    def test_y_maps_to_true(self, ptk_prompt: Mock) -> None:
        bool_input = input_types.BoolInput()
        assert bool_input.prompt("Confirm") is True

    @patch.object(input_types, "ptk_prompt", return_value="n")
    def test_n_maps_to_false(self, ptk_prompt: Mock) -> None:
        bool_input = input_types.BoolInput()
        assert bool_input.prompt("Confirm") is False
