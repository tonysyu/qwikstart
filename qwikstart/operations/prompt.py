import logging
import textwrap
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Type

from ..base_context import BaseContext, DictContext, TContext
from ..exceptions import OperationDefinitionError, OperationError
from ..utils.prompt import create_prompt_spec, read_user_variable
from ..utils.templates import DEFAULT_TEMPLATE_VARIABLE_PREFIX, TemplateRenderer
from .base import BaseOperation
from .utils import TEMPLATE_VARIABLE_PREFIX_HELP

__all__ = ["Operation"]

logger = logging.getLogger(__name__)

DEFAULT_INTRO = "Please enter the following information:"

CONTEXT_HELP = {
    "inputs": textwrap.dedent(
        """
            List of dictionaries describing prompts for user inputs.
            Dictionary have the following keys:
                - name: The name of the variable being defined.
                - default: Optional default value of variable. Note that this
                  can be defined as a template string, with variables defined in
                  previous prompts or from template variables in the context; e.g.:

                    - name: "name"
                      default: "World"
                    - name: "message"
                      default: "Hello {{ qwikstart.name }}!"
        """
    ),
    "introduction": "Message to user before prompting for inputs.",
    "template_variable_prefix": TEMPLATE_VARIABLE_PREFIX_HELP,
}

Output = Dict[str, Any]


@dataclass(frozen=True)
class Context(BaseContext):
    inputs: List[Dict[str, Any]]
    introduction: str = DEFAULT_INTRO
    template_variables: Dict[str, Any] = field(default_factory=dict)
    template_variable_prefix: str = DEFAULT_TEMPLATE_VARIABLE_PREFIX

    @classmethod
    def help(cls, field_name: str) -> Optional[str]:
        return CONTEXT_HELP.get(field_name)

    @classmethod
    def from_dict(cls: Type[TContext], field_dict: DictContext) -> TContext:
        # FIXME: Remove in v0.5; Support "prompts" for backwards compatibility
        if "prompts" in field_dict:
            field_dict = {
                "inputs": field_dict["prompts"],
                **{k: v for k, v in field_dict.items() if k != "prompts"},
            }
        return super().from_dict(field_dict)  # type: ignore


class Operation(BaseOperation[Context, Output]):
    """Operation to prompt user for input values.

    See https://qwikstart.readthedocs.io/en/latest/operations/prompt.html

    Overrides default `opconfig` with:

    - `display_description`: `False`
    - `output_namespace`: `"template_variables"`
    """

    name = "prompt"
    aliases = ["prompt_user"]
    default_opconfig = {
        "display_description": False,
        "output_namespace": "template_variables",
    }

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        if "output_dict_name" in self.local_context:
            raise OperationDefinitionError(
                "prompt operation no longer supports `output_dict_name`. "
                "Use `opconfig.output_namespace` instead."
            )

    def run(self, context: Context) -> Output:
        if not isinstance(context.inputs, list):
            raise OperationDefinitionError(
                f"Expected prompt inputs to be a list but given {context.inputs}"
            )

        introduction = context.introduction
        logger.info(introduction)

        renderer = TemplateRenderer.from_context(context)
        user_responses = {}

        for input_description in context.inputs:
            if "choices_from" in input_description:
                self._resolve_input_choices_from_template_variables(
                    input_description, context.template_variables
                )
            prompt_spec = create_prompt_spec(**input_description)

            if isinstance(prompt_spec.default, str):
                prompt_spec.default = renderer.render_string(prompt_spec.default)

            response = read_user_variable(prompt_spec)
            user_responses[prompt_spec.name] = response
            # Ensure that templates used for defaults can use the new variable.
            renderer.add_template_variable(prompt_spec.name, response)

        return user_responses

    def _resolve_input_choices_from_template_variables(
        self, input_description: Dict[str, Any], template_variables: Dict[str, Any]
    ) -> None:
        """Update `input_description` with `choices` resolved from `template_variables`.

        The `choices_from` value in `input_description` should be a variable name in
        `template_variables` mapping to a list of input choices.
        """
        variable_name = input_description.pop("choices_from")
        choices = template_variables.get(variable_name)
        if not choices:
            input_name = input_description["name"]
            raise OperationError(
                f"Input '{input_name}' defined with `choices_from='{variable_name}'` "
                f"not found in template variables: {template_variables}"
            )
        input_description["choices"] = choices
