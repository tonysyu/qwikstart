from typing import Any, Dict, Optional
from unittest.mock import patch

import pytest

from qwikstart.exceptions import OperationDefinitionError
from qwikstart.operations import prompt as prompt_user
from qwikstart.utils.prompt import PromptSpec

from .. import helpers


class TestPromptUser:
    def test_no_default(self) -> None:
        context = {"inputs": [{"name": "name"}]}
        output_context = execute_prompt_op(context, responses={"name": "Tony"})
        assert output_context["template_variables"]["name"] == "Tony"

    def test_deprecated_prompts_still_works(self) -> None:
        context = {"prompts": [{"name": "name"}]}
        output_context = execute_prompt_op(context, responses={"name": "Tony"})
        assert output_context["template_variables"]["name"] == "Tony"

    def test_use_default(self) -> None:
        context = {"inputs": [{"name": "name", "default": "World"}]}
        output_context = execute_prompt_op(context, responses={})
        assert output_context["template_variables"]["name"] == "World"

    def test_pre_existing_template_variable_in_output(self) -> None:
        context = {
            "inputs": [{"name": "name"}],
            "template_variables": {"pre-existing": "value"},
        }
        output_context = execute_prompt_op(context, responses={"name": "Tony"})
        assert output_context["template_variables"] == {
            "pre-existing": "value",
            "name": "Tony",
        }

    def test_output_to_global_namespace(self) -> None:
        context = {
            "inputs": [{"name": "name"}],
            "template_variables": {"pre-existing": "value"},
        }
        output_context = execute_prompt_op(context, responses={"name": "Tony"})
        assert output_context["template_variables"] == {
            "pre-existing": "value",
            "name": "Tony",
        }

    def test_old_output_dict_name_raises_error(self) -> None:
        with pytest.raises(OperationDefinitionError):
            # Error only raised if `output_dict_name` passed as `local_context`:
            execute_prompt_op(
                context={"inputs": [{"name": "name"}]},
                local_context={"output_dict_name": "variables"},
            )

    def test_help(self) -> None:
        assert prompt_user.Context.help("inputs") == prompt_user.CONTEXT_HELP["inputs"]

    def test_template_string_for_default(self) -> None:
        context = {
            "inputs": [
                {"name": "name"},
                {"name": "message", "default": "Hello {{ qwikstart.name }}!"},
            ]
        }
        output_context = execute_prompt_op(context, responses={"name": "World"})
        assert output_context["template_variables"]["message"] == "Hello World!"


def execute_prompt_op(
    context: Dict[str, Any],
    responses: Optional[Dict[str, Any]] = None,
    **operation_kwargs: Any,
) -> Dict[str, Any]:
    context.setdefault("execution_context", helpers.get_execution_context())
    mock_read_user_variable = MockReadUserVariable(responses=responses)
    prompt_op = prompt_user.Operation(**operation_kwargs)
    with patch.object(prompt_user, "read_user_variable", new=mock_read_user_variable):
        return prompt_op.execute(context)


class MockReadUserVariable:
    def __init__(self, responses: Optional[Dict[str, Any]]):
        self.responses = responses or {}

    def __call__(self, prompt: PromptSpec) -> Any:
        if prompt.name in self.responses:
            return self.responses[prompt.name]
        if prompt.default is None:
            raise RuntimeError(f"No response or default for {prompt.name}")
        return prompt.default
