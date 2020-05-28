import logging
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Optional

from ..base_context import BaseContext
from ..exceptions import OperationError
from ..repository import get_repo_loader
from ..utils import ensure_path
from .base import BaseOperation
from .utils import FILE_PATH_HELP

if TYPE_CHECKING:
    from ..tasks import Task

__all__ = ["Operation"]

logger = logging.getLogger(__name__)

CONTEXT_HELP = {
    "file_path": FILE_PATH_HELP,
}

EXCLUDED_CONTEXT = {"execution_context"}


@dataclass(frozen=True)
class Context(BaseContext):
    file_path: Path
    repo_url: Optional[str] = None

    @classmethod
    def help(cls, field_name: str) -> Optional[str]:
        return CONTEXT_HELP.get(field_name)


class Operation(BaseOperation[Context, Dict[str, Any]]):
    """Operation for running subtask defined by file.

    See https://qwikstart.readthedocs.io/en/latest/operations/subtask.html
    """

    name: str = "subtask"

    def run(self, context: Context) -> Dict[str, Any]:
        file_path = ensure_path(context.file_path)
        file_path = context.execution_context.source_dir / file_path
        if not file_path.is_file():
            raise OperationError(f"File does not exist: {file_path}")

        task = load_task(str(file_path), context)
        output_context = task.execute()
        return {
            key: value
            for key, value in output_context.items()
            if key not in EXCLUDED_CONTEXT
        }


def load_task(file_path: str, context: Context) -> "Task":
    # Nested imports to avoid circular import:
    from ..parser import parse_task_steps
    from ..tasks import Task

    loader = get_repo_loader(file_path, context.repo_url)
    operations = parse_task_steps(loader.task_spec)
    # FIXME: Switch with context that can contain arbitrary data.
    return Task(
        context={"execution_context": context.execution_context}, operations=operations,
    )
