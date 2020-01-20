from unittest.mock import Mock, patch

import pytest

from qwikstart.exceptions import UserFacingError
from qwikstart.utils import prompt as _prompt


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
    def test_prompt_raises_unknown_type_error(self, prompt_class: Mock) -> None:
        prompt_class.__dataclass_fields__ = {"name": str}
        prompt_class.side_effect = TypeError("Fake error should be re-raised")
        with pytest.raises(TypeError, match="Fake error should be re-raised"):
            _prompt.create_prompt(name="test")


@patch.object(_prompt, "read_user_choice")
@patch.object(_prompt.click, "prompt")  # type: ignore
class TestReadUserVariable:
    def test_call_click_prompt(self, click_prompt: Mock, read_choice: Mock) -> None:
        prompt = _prompt.create_prompt(name="test")
        _prompt.read_user_variable(prompt)

        click_prompt.assert_called_once_with(
            _prompt.default_style("test"), default=None
        )
        read_choice.assert_not_called()

    def test_call_read_choice(self, click_prompt: Mock, read_choice: Mock) -> None:
        prompt = _prompt.create_prompt(name="greeting", choices=["Hi", "Hello"])
        _prompt.read_user_variable(prompt)

        read_choice.assert_called_once_with(prompt)
        click_prompt.assert_not_called()


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
