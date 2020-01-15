import logging
import textwrap
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..base_context import BaseContext
from ..utils.prompt import Prompt, read_user_variable
from ..utils.templates import DEFAULT_TEMPLATE_VARIABLE_PREFIX, TemplateRenderer
from .base import BaseOperation

__all__ = ["Operation"]

logger = logging.getLogger(__name__)

DEFAULT_INTRO = "Please enter the following information:"

CONTEXT_HELP = {
    "prompts": textwrap.dedent(
        """
            List of dictionaries describing prompts for user inputs.
            Dictionary have the following keys:
                - name: The name of the variable being defined.
                - default_value: Optional default value of variable. Note that this
                  can be defined as a template string, with variables defined in
                  previous prompts or from template variables in the context; e.g.:

                    - name: "name"
                      default_value: "World"
                    - name: "message"
                      default_value: "Hello {{ name }}!"
        """
    )
}


# Output will be dict with single key, `Context.output_dict_name`, and dict
# value w/ keys defined by `Context.prompts` mapping to user responses.
Output = Dict[str, Dict[str, Any]]


@dataclass(frozen=True)
class Context(BaseContext):
    prompts: List[Dict[str, Any]]
    output_dict_name: str = "template_variables"
    introduction: str = DEFAULT_INTRO
    template_variables: Dict[str, Any] = field(default_factory=dict)
    template_variable_prefix: str = DEFAULT_TEMPLATE_VARIABLE_PREFIX

    @classmethod
    def help(cls, field_name: str) -> Optional[str]:
        return CONTEXT_HELP.get(field_name)


class Operation(BaseOperation[Context, Output]):
    """Operation to prompt user for inputs."""

    name: str = "prompt_user"

    def run(self, context: Context) -> Output:

        introduction = context.introduction
        logger.info(introduction)

        renderer = TemplateRenderer.from_context(context)
        user_responses = {}
        for prompt_dict in context.prompts:
            prompt = Prompt(**prompt_dict)
            if isinstance(prompt.default_value, str):
                prompt.default_value = renderer.render_string(prompt.default_value)

            response = read_user_variable(prompt)
            user_responses[prompt.name] = response
            # Ensure that templates used for defaults can use the new variable.
            renderer.add_template_variable(prompt.name, response)

        output_name = context.output_dict_name
        logger.debug(f"Responses recorded to {output_name}:")
        logger.debug(
            "\t"
            + "\n\t".join(f"{key}: {value!r}" for key, value in user_responses.items())
        )

        return {output_name: user_responses}
