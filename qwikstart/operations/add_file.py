import os
from pathlib import Path
from typing import Any, Dict, List, Type

import jinja2
from typing_extensions import TypedDict

from ..base_context import BaseContext
from .base import BaseOperation

__all__ = ["Operation"]


class RequiredContext(BaseContext):
    target_path: Path
    template_path: str


class Context(RequiredContext, total=False):
    template_loader: Type[jinja2.BaseLoader]
    template_loader_args: List[Any]
    template_loader_kwargs: Dict[str, Any]
    template_variables: Dict[str, Any]


class Operation(BaseOperation):
    """Operation write file"""

    name: str = "write_file"

    def run(self, context: Context) -> None:
        loader_class = context.get("template_loader", jinja2.FileSystemLoader)
        loader_args = context.get("template_loader_args", ())
        loader_kwargs = context.get("template_loader_kwargs", {})
        env = jinja2.Environment(
            loader=loader_class(*loader_args, **loader_kwargs)
        )
        template = env.get_template(context["template_path"])

        template_variables = context.get("template_variables", {})
        with context["target_path"].open("w") as f:
            f.write(template.render(**template_variables))
