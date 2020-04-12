from typing import Any, Dict, Optional
from unittest.mock import patch

import pytest

from qwikstart.exceptions import OperationDefinitionError, OperationError
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

    def test_choices_from_template_variables(self) -> None:
        with patch.object(prompt_user, "create_prompt_spec") as create_prompt_spec:
            execute_prompt_op(
                {
                    "inputs": [{"name": "name", "choices_from": "possible_names"}],
                    "template_variables": {"possible_names": ["Troy", "Abed"]},
                }
            )
        create_prompt_spec.assert_called_once_with(
            name="name", choices=["Troy", "Abed"],
        )

    def test_unknown_choices_from(self) -> None:
        with pytest.raises(OperationError):
            execute_prompt_op(
                {"inputs": [{"name": "name", "choices_from": "unknown_variable"}],}
            )

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
        # Double check that "name" wasn't also added to the global context.
        assert "name" not in output_context

    def test_output_to_global_namespace(self) -> None:
        context = {"inputs": [{"name": "name"}]}
        # Override default output_namespace (template_variables) to use global context.
        output_context = execute_prompt_op(
            context, responses={"name": "Tony"}, opconfig={"output_namespace": None}
        )
        assert output_context["name"] == "Tony"
        # Double check the default namespace, "template_variables", is not created.
        assert "template_variables" not in output_context

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
    prompt_op = prompt_user.Operation(**operation_kwargs)
    mock_read_user_variable = MockReadUserVariable(responses=responses)
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
