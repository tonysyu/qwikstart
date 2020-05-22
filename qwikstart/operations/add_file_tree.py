import logging
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from ..base_context import BaseContext
from ..utils.filesystem import FileTreeGenerator
from ..utils.templates import DEFAULT_TEMPLATE_VARIABLE_PREFIX, TemplateRenderer
from .base import BaseOperation
from .utils import TEMPLATE_VARIABLE_PREFIX_HELP

__all__ = ["Operation"]

logger = logging.getLogger(__name__)

CONTEXT_HELP = {
    "template_dir": textwrap.dedent(
        """
            Path to directory containing template files. This path is relative to the
            qwikstart repo directory, which is typically the directory containing the
            `qwikstart.yml` file.
        """
    ),
    "target_dir": textwrap.dedent(
        """
            Directory where files from `template_dir` will be written. This is relative
            to the current working directory.
        """
    ),
    "template_variable_prefix": TEMPLATE_VARIABLE_PREFIX_HELP,
    "ignore": textwrap.dedent(
        """
            List of file patterns to ignore from source directory. Unix-shell-style
            wildcards are accepted. See https://docs.python.org/3/library/fnmatch.html
        """
    ),
}


@dataclass(frozen=True)
class Context(BaseContext):
    template_dir: str
    target_dir: Union[Path, str, None] = None
    template_variables: Dict[str, Any] = field(default_factory=dict)
    template_variable_prefix: str = DEFAULT_TEMPLATE_VARIABLE_PREFIX
    ignore: List[str] = field(default_factory=list)

    @classmethod
    def help(cls, field_name: str) -> Optional[str]:
        return CONTEXT_HELP.get(field_name)


class Operation(BaseOperation[Context, None]):
    """Operation to add a file tree (a.k.a. directory) to a project.


    See https://qwikstart.readthedocs.io/en/latest/operations/add_file_tree.html
    """

    name: str = "add_file_tree"

    def run(self, context: Context) -> None:
        execution_context = context.execution_context
        renderer = TemplateRenderer.from_context(context)

        source = execution_context.source_dir.joinpath(context.template_dir)
        target = context.target_dir or execution_context.target_dir

        if context.execution_context.dry_run:
            logger.info(
                f"Skipping copy of files from {source} to {target} "
                "due to `--dry-run` option"
            )
            return

        generator = FileTreeGenerator(
            Path(source), Path(target), renderer, ignore_patterns=context.ignore
        )
        generator.copy()

        logger.info(f"Add file tree at {target}")
