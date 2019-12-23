import logging
from pathlib import Path
from typing import Any, Dict, Union

import jinja2

from ..base_context import BaseContext
from ..utils import ensure_path
from ..utils.filesystem import FileTreeGenerator
from ..utils.templates import TemplateRenderer
from .base import BaseOperation

__all__ = ["Operation"]

logger = logging.getLogger(__name__)


class RequiredContext(BaseContext):
    template_dir: str


class Context(RequiredContext, total=False):
    target_dir: Union[Path, str]
    template_variables: Dict[str, Any]
    template_variable_prefix: str


class Operation(BaseOperation):
    """Operation to add a file tree (a.k.a. directory) to a project."""

    name: str = "add_file_tree"

    def run(self, context: Context) -> None:
        execution_context = context["execution_context"]
        renderer = TemplateRenderer.from_context(context)

        source = execution_context.source_dir.joinpath(context["template_dir"])
        target = context.get("target_dir", execution_context.target_dir)

        generator = FileTreeGenerator(Path(source), Path(target), renderer)
        generator.copy()

        logger.info(f"Add file tree at {target}")
