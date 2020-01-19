from typing import Any, Dict, Optional
from unittest.mock import patch

import pytest

from qwikstart.exceptions import OperationError
from qwikstart.operations import prompt_user
from qwikstart.utils.prompt import Prompt

from .. import helpers


class TestPromptUser:
    def test_no_default(self) -> None:
        context = {
            "execution_context": helpers.get_execution_context(),
            "prompts": [{"name": "name"}],
        }
        output_context = execute_prompt_user(context, responses={"name": "Tony"})
        assert output_context["template_variables"]["name"] == "Tony"

    def test_use_default(self) -> None:
        context = {
            "execution_context": helpers.get_execution_context(),
            "prompts": [{"name": "name", "default_value": "World"}],
        }
        output_context = execute_prompt_user(context)
        assert output_context["template_variables"]["name"] == "World"

    def test_template_string_for_default_value(self) -> None:
        context = {
            "execution_context": helpers.get_execution_context(),
            "prompts": [
                {"name": "name"},
                {"name": "message", "default_value": "Hello {{ qwikstart.name }}!"},
            ],
        }
        output_context = execute_prompt_user(context, responses={"name": "World"})
        assert output_context["template_variables"]["message"] == "Hello World!"


class TestCreatePrompt:
    def test_name_only(self) -> None:
        prompt = prompt_user.create_prompt(name="test")
        assert prompt.name == "test"
        assert prompt.default_value is None

    def test_name_and_default(self) -> None:
        prompt = prompt_user.create_prompt(name="test", default_value="hello")
        assert prompt.name == "test"
        assert prompt.default_value == "hello"

    def test_name_missing_raises(self) -> None:
        with pytest.raises(OperationError, match="Prompt definition has no 'name'"):
            prompt_user.create_prompt()

    def test_unknown_attribute_raises(self) -> None:
        msg = "Prompt definition for 'test' has unknown keys:"
        with pytest.raises(OperationError, match=msg):
            prompt_user.create_prompt(name="test", unknown="value")


def execute_prompt_user(
    context: Dict[str, Any], responses: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    mock_read_user_variable = MockReadUserVariable(responses=responses)
    prompt_op = prompt_user.Operation()
    with patch.object(prompt_user, "read_user_variable", new=mock_read_user_variable):
        return prompt_op.execute(context)


class MockReadUserVariable:
    def __init__(self, responses: Optional[Dict[str, Any]]):
        self.responses = responses or {}

    def __call__(self, prompt: Prompt) -> Any:
        if prompt.name in self.responses:
            return self.responses[prompt.name]
        if prompt.default_value is None:
            raise RuntimeError(f"No response or default for {prompt.name}")
        return prompt.default_value
