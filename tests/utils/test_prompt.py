from unittest.mock import Mock, patch

import click.types
import pytest

from qwikstart import utils
from qwikstart.exceptions import UserFacingError
from qwikstart.utils import prompt as _prompt

PROMPT_ATTRS = utils.get_dataclass_keys(_prompt.Prompt)


class TestCreatePrompt:
    def test_name_only(self) -> None:
        prompt = _prompt.create_prompt(name="test")
        assert prompt.name == "test"
        assert prompt.default is None

    def test_name_and_default(self) -> None:
        prompt = _prompt.create_prompt(name="test", default="hello")
        assert prompt.name == "test"
        assert prompt.default == "hello"

    def test_deprecated_default_value_still_works(self) -> None:
        prompt = _prompt.create_prompt(name="test", default_value="hello")
        assert prompt.name == "test"
        assert prompt.default == "hello"

    def test_name_missing_raises(self) -> None:
        with pytest.raises(UserFacingError, match="Prompt definition has no 'name'"):
            _prompt.create_prompt()

    def test_unknown_attribute_raises(self) -> None:
        msg = "Prompt definition for 'test' has unknown keys:"
        with pytest.raises(UserFacingError, match=msg):
            _prompt.create_prompt(name="test", unknown="value")

    @patch.object(_prompt, "Prompt")
    @patch.object(_prompt.utils, "get_dataclass_keys", return_value=PROMPT_ATTRS)
    def test_prompt_reraises_unknown_type_error(
        self, get_dataclass_keys: Mock, prompt_class: Mock
    ) -> None:
        prompt_class.side_effect = TypeError("Fake error should be re-raised")
        with pytest.raises(TypeError, match="Fake error should be re-raised"):
            _prompt.create_prompt(name="test")


class TestGetParamType:
    def test_unknown_type_returns_none(self) -> None:
        assert _prompt.get_param_type(name="any") is None

    def test_bool_based_on_default(self) -> None:
        assert _prompt.get_param_type(name="fake", default=True) == click.types.BOOL
        assert _prompt.get_param_type(name="fake", default=False) == click.types.BOOL

    def test_explicit_bool(self) -> None:
        assert _prompt.get_param_type(name="fake", type="bool") == click.types.BOOL

    def test_explicit_bool_uppercase(self) -> None:
        assert _prompt.get_param_type(name="fake", type="BOOL") == click.types.BOOL

    def test_explicit_bool_type(self) -> None:
        assert _prompt.get_param_type(name="fake", type=bool) == click.types.BOOL

    def test_unknown_type(self) -> None:
        with pytest.raises(UserFacingError, match="Unknown type 'bad' for prompt fake"):
            _prompt.get_param_type(name="fake", type="bad")


@patch.object(_prompt, "read_user_choice")
@patch.object(_prompt.click, "prompt")  # type: ignore
class TestReadUserVariable:
    def test_call_click_prompt(self, click_prompt: Mock, read_choice: Mock) -> None:
        prompt = _prompt.create_prompt(name="test")
        _prompt.read_user_variable(prompt)

        click_prompt.assert_called_once_with(
            _prompt.default_style("test"), default=None, type=None
        )
        read_choice.assert_not_called()

    def test_call_read_choice(self, click_prompt: Mock, read_choice: Mock) -> None:
        prompt = _prompt.create_prompt(name="greeting", choices=["Hi", "Hello"])
        _prompt.read_user_variable(prompt)

        read_choice.assert_called_once_with(prompt)
        click_prompt.assert_not_called()

    def test_boolean_prompt(self, click_prompt: Mock, read_choice: Mock) -> None:
        prompt = _prompt.create_prompt(name="test", default=False)
        _prompt.read_user_variable(prompt)

        click_prompt.assert_called_once_with(
            _prompt.default_style("test"), default=False, type=click.types.BOOL
        )
        read_choice.assert_not_called()


@patch.object(_prompt.click, "prompt")  # type: ignore
class TestReadUserChoice:
    def test_select_choice(self, click_prompt: Mock) -> None:
        prompt = _prompt.create_prompt(name="greeting", choices=["Hi", "Hello"])

        click_prompt.return_value = "1"
        assert _prompt.read_user_choice(prompt) == "Hi"

        click_prompt.return_value = "2"
        assert _prompt.read_user_choice(prompt) == "Hello"

    def test_string_choices_raises_type_error(self, click_prompt: Mock) -> None:
        prompt = _prompt.create_prompt(name="greeting", choices="Hi, Hello")
        with pytest.raises(UserFacingError, match="Choices for prompt must be list"):
            _prompt.read_user_choice(prompt)

    def test_empty_choices_raises_value_error(self, click_prompt: Mock) -> None:
        prompt = _prompt.create_prompt(name="greeting", choices=[])
        with pytest.raises(UserFacingError, match="Choices for prompt cannot be empty"):
            _prompt.read_user_choice(prompt)
