import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Union

from ..base_context import BaseContext
from ..utils.filesystem import FileTreeGenerator
from ..utils.templates import DEFAULT_TEMPLATE_VARIABLE_PREFIX, TemplateRenderer
from .base import BaseOperation

__all__ = ["Operation"]

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Context(BaseContext):
    template_dir: str
    target_dir: Union[Path, str, None] = None
    template_variables: Dict[str, Any] = field(default_factory=dict)
    template_variable_prefix: str = DEFAULT_TEMPLATE_VARIABLE_PREFIX


class Operation(BaseOperation[Context, None]):
    """Operation to add a file tree (a.k.a. directory) to a project."""

    name: str = "add_file_tree"

    def run(self, context: Context) -> None:
        execution_context = context.execution_context
        renderer = TemplateRenderer.from_context(context)

        source = execution_context.source_dir.joinpath(context.template_dir)
        target = context.target_dir or execution_context.target_dir

        generator = FileTreeGenerator(Path(source), Path(target), renderer)
        generator.copy()

        logger.info(f"Add file tree at {target}")
