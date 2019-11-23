import os
from pathlib import Path
from typing import Any, Dict, List, Type, Union

import jinja2
from typing_extensions import TypedDict

from ..base_context import BaseContext
from ..utils import ensure_path
from .base import BaseOperation

__all__ = ["Operation"]


class RequiredContext(BaseContext):
    target_path: Union[Path, str]
    template_path: str


class Context(RequiredContext, total=False):
    template_variables: Dict[str, Any]


class Operation(BaseOperation):
    """Operation to add a file to a project."""

    name: str = "add_file"

    def run(self, context: Context) -> None:
        execution_context = context.get("execution_context")
        template_loader = execution_context.get_template_loader()
        env = jinja2.Environment(loader=template_loader)
        template = env.get_template(context["template_path"])

        template_variables = context.get("template_variables", {})

        with ensure_path(context["target_path"]).open("w") as f:
            f.write(template.render(**template_variables))
