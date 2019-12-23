import logging
from pathlib import Path
from typing import Any, Dict, Union

from ..base_context import BaseContext
from ..utils import ensure_path
from ..utils.templates import TemplateRenderer
from .base import BaseOperation

__all__ = ["Operation"]

logger = logging.getLogger(__name__)


class RequiredContext(BaseContext):
    target_path: Union[Path, str]
    template_path: str


class Context(RequiredContext, total=False):
    template_variables: Dict[str, Any]
    template_variable_prefix: str


class Operation(BaseOperation):
    """Operation to add a file to a project."""

    name: str = "add_file"

    def run(self, context: Context) -> None:
        renderer = TemplateRenderer.from_context(context)
        with ensure_path(context["target_path"]).open("w") as f:
            f.write(renderer.render(context["template_path"]))
        logger.info(f"Wrote file to {context['target_path']}")
