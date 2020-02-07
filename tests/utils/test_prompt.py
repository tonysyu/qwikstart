from unittest.mock import ANY, Mock, patch

import pytest

from qwikstart import utils
from qwikstart.exceptions import UserFacingError
from qwikstart.utils import prompt as _prompt
from qwikstart.utils.input_types import BoolInput, StringInput

PROMPT_ATTRS = utils.get_dataclass_keys(_prompt.PromptSpec)


class TestCreatePromptSpec:
    def test_name_only(self) -> None:
        prompt_spec = _prompt.create_prompt_spec(name="test")
        assert prompt_spec.name == "test"
        assert prompt_spec.default is None
        assert prompt_spec.input_type == StringInput

    def test_name_and_default(self) -> None:
        prompt_spec = _prompt.create_prompt_spec(name="test", default="hello")
        assert prompt_spec.name == "test"
        assert prompt_spec.default == "hello"

    def test_deprecated_default_value_still_works(self) -> None:
        prompt_spec = _prompt.create_prompt_spec(name="test", default_value="hello")
        assert prompt_spec.name == "test"
        assert prompt_spec.default == "hello"

    def test_name_missing_raises(self) -> None:
        msg = "PromptSpec definition has no 'name'"
        with pytest.raises(UserFacingError, match=msg):
            _prompt.create_prompt_spec()

    def test_unknown_attribute_raises(self) -> None:
        msg = "PromptSpec definition for 'test' has unknown keys:"
        with pytest.raises(UserFacingError, match=msg):
            _prompt.create_prompt_spec(name="test", unknown="value")

    @patch.object(_prompt, "PromptSpec")
    @patch.object(_prompt.utils, "get_dataclass_keys", return_value=PROMPT_ATTRS)
    def test_prompt_reraises_unknown_type_error(
        self, get_dataclass_keys: Mock, prompt_class: Mock
    ) -> None:
        prompt_class.side_effect = TypeError("Fake error should be re-raised")
        with pytest.raises(TypeError, match="Fake error should be re-raised"):
            _prompt.create_prompt_spec(name="test")


class TestGetParamType:
    def test_unknown_type_returns_string_input(self) -> None:
        assert _prompt.get_param_type(name="any") is StringInput

    def test_bool_based_on_default(self) -> None:
        assert _prompt.get_param_type(name="fake", default=True) is BoolInput
        assert _prompt.get_param_type(name="fake", default=False) is BoolInput

    def test_explicit_bool(self) -> None:
        assert _prompt.get_param_type(name="fake", type="bool") is BoolInput

    def test_explicit_bool_uppercase(self) -> None:
        assert _prompt.get_param_type(name="fake", type="BOOL") is BoolInput

    def test_explicit_bool_type(self) -> None:
        assert _prompt.get_param_type(name="fake", type=bool) is BoolInput

    def test_unknown_type(self) -> None:
        with pytest.raises(UserFacingError, match="Unknown type 'bad' for prompt fake"):
            _prompt.get_param_type(name="fake", type="bad")


@patch.object(_prompt, "read_user_choice")
@patch.object(_prompt.input_types, "ptk_prompt")
class TestReadUserVariable:
    def test_call_ptk_prompt(self, ptk_prompt: Mock, read_choice: Mock) -> None:
        prompt_spec = _prompt.create_prompt_spec(name="test")
        _prompt.read_user_variable(prompt_spec)

        ptk_prompt.assert_called_once_with(
            "test: ", default=None, completer=None, validator=ANY
        )
        read_choice.assert_not_called()

    def test_call_read_choice(self, ptk_prompt: Mock, read_choice: Mock) -> None:
        prompt_spec = _prompt.create_prompt_spec(name="greet", choices=["Hi", "Hello"])
        _prompt.read_user_variable(prompt_spec)

        read_choice.assert_called_once_with(prompt_spec)
        ptk_prompt.assert_not_called()

    def test_infer_boolean_prompt(self, ptk_prompt: Mock, read_choice: Mock) -> None:
        prompt_spec = _prompt.create_prompt_spec(name="test", default=False)
        _prompt.read_user_variable(prompt_spec)

        ptk_prompt.assert_called_once_with(
            "test: ", default=False, completer=None, validator=ANY
        )
        read_choice.assert_not_called()

    def test_explicit_type(self, ptk_prompt: Mock, read_choice: Mock) -> None:
        prompt_spec = _prompt.create_prompt_spec(name="test", type="bool")
        prompt_spec.input_type is BoolInput


@patch.object(_prompt.input_types, "ptk_prompt")
class TestReadUserChoice:
    def test_select_choice(self, ptk_prompt: Mock) -> None:
        prompt_spec = _prompt.create_prompt_spec(name="greet", choices=["Hi", "Hello"])

        ptk_prompt.return_value = "1"
        assert _prompt.read_user_choice(prompt_spec) == "Hi"

        ptk_prompt.return_value = "2"
        assert _prompt.read_user_choice(prompt_spec) == "Hello"

    def test_string_choices_raises_type_error(self, ptk_prompt: Mock) -> None:
        prompt_spec = _prompt.create_prompt_spec(name="greeting", choices="Hi, Hello")
        with pytest.raises(UserFacingError, match="Choices for prompt must be list"):
            _prompt.read_user_choice(prompt_spec)

    def test_empty_choices_raises_value_error(self, ptk_prompt: Mock) -> None:
        prompt_spec = _prompt.create_prompt_spec(name="greeting", choices=[])
        with pytest.raises(UserFacingError, match="Choices for prompt cannot be empty"):
            _prompt.read_user_choice(prompt_spec)
