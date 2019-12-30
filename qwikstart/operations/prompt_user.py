import logging
from dataclasses import dataclass
from typing import Any, Dict, List

from ..base_context import BaseContext
from ..utils.prompt import Prompt, read_user_variable
from .base import BaseOperation

__all__ = ["Operation"]

logger = logging.getLogger(__name__)

DEFAULT_INTRO = "Please enter the following information:"


@dataclass(frozen=True)
class Context(BaseContext):
    prompts: List[Dict[str, Any]]
    output_dict_name: str = "template_variables"
    introduction: str = DEFAULT_INTRO


class Operation(BaseOperation):
    """Operation to prompt user for inputs."""

    name: str = "prompt_user"

    def run(self, context: Context) -> Dict[str, Dict[str, Any]]:
        output_name = context.output_dict_name
        prompt_list = [Prompt(**pdict) for pdict in context.prompts]

        introduction = context.introduction
        logger.info(introduction)

        user_responses = {}
        for prompt in prompt_list:
            user_responses[prompt.name] = read_user_variable(prompt)

        logger.debug(f"Responses recorded to {output_name}:")
        logger.debug(
            "\t"
            + "\n\t".join(f"{key}: {value!r}" for key, value in user_responses.items())
        )

        return {output_name: user_responses}
