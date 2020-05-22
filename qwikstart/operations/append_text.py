import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from ..base_context import BaseContext
from ..exceptions import OperationError
from ..utils import ensure_path
from .base import BaseOperation
from .utils import FILE_PATH_HELP

__all__ = ["Operation"]

logger = logging.getLogger(__name__)

CONTEXT_HELP = {
    "file_path": FILE_PATH_HELP,
    "text": "Text that will be appended to `file_path`",
    "prefix": "Text added before appended `text`",
    "suffix": "Text added after appended `text`",
}


@dataclass(frozen=True)
class Context(BaseContext):
    file_path: Path
    text: str
    prefix: str = os.linesep
    suffix: str = ""

    @classmethod
    def help(cls, field_name: str) -> Optional[str]:
        return CONTEXT_HELP.get(field_name)


class Operation(BaseOperation[Context, None]):
    """Operation for appending text to a given file.

    See https://qwikstart.readthedocs.io/en/latest/operations/append_text.html
    """

    name: str = "append_text"

    def run(self, context: Context) -> None:
        file_path = ensure_path(context.file_path)
        if not file_path.is_file():
            raise OperationError(f"File does not exist: {file_path}")

        if context.execution_context.dry_run:
            logger.info(
                f"Skipping append_text operation on {file_path} "
                "due to `--dry-run` option"
            )
            return

        with file_path.open("a") as f:
            f.write(self.get_text(context))

    def get_text(self, context: Context) -> str:
        return "".join([context.prefix, context.text, context.suffix])
