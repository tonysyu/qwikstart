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


class RequiredContext(BaseContext):
    prompts: List[Dict[str, Any]]


class Context(RequiredContext, total=False):
    output_dict_name: str


class Operation(BaseOperation):
    """Operation to prompt user for inputs."""

    name: str = "prompt_user"

    def run(self, context: Context) -> None:
        output_name = context.get("output_dict_name", "template_variables")

        prompt_list = [Prompt(**pdict) for pdict in context["prompts"]]
        user_response = {}
        for prompt in prompt_list:
            user_response[prompt.name] = read_user_variable(prompt)

        return {output_name: user_response}
