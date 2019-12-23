import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from typing_extensions import TypedDict

from ..base_context import BaseContext
from ..utils import indent
from ..utils.prompt import Prompt, read_user_variable
from .base import BaseOperation

__all__ = ["Operation"]

logger = logging.getLogger(__name__)

DEFAULT_INTRO = "Please enter the following information:"


class RequiredContext(BaseContext):
    prompts: List[Dict[str, Any]]


class Context(RequiredContext, total=False):
    output_dict_name: str
    introduction: str


class Operation(BaseOperation):
    """Operation to prompt user for inputs."""

    name: str = "prompt_user"

    def run(self, context: Context) -> None:
        output_name = context.get("output_dict_name", "template_variables")
        prompt_list = [Prompt(**pdict) for pdict in context["prompts"]]

        introduction = context.get("introduction", DEFAULT_INTRO)
        logger.info(introduction)

        user_responses = {}
        for prompt in prompt_list:
            user_responses[prompt.name] = read_user_variable(prompt)

        logger.debug(f"Responses recorded to {output_name}:")
        logger.debug(
            "\t"
            + "\n\t".join(
                f"{key}: {value!r}" for key, value in user_responses.items()
            )
        )

        return {output_name: user_responses}
