import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from ..base_context import BaseContext
from ..utils import ensure_path, merge_nested_dicts, pformat_json
from .base import BaseOperation
from .utils import FILE_PATH_HELP

__all__ = ["Operation"]

logger = logging.getLogger(__name__)

CONTEXT_HELP = {
    "file_path": FILE_PATH_HELP,
    "merge_data": "Data that will be merged into existing data in json file.",
}


@dataclass(frozen=True)
class Context(BaseContext):
    file_path: Path
    merge_data: Dict[str, Any]
    indent: int = 4

    @classmethod
    def help(cls, field_name: str) -> Optional[str]:
        return CONTEXT_HELP.get(field_name)


class Operation(BaseOperation[Context, None]):
    """Operation to edit json by merging data into existing json data.

    See https://qwikstart.readthedocs.io/en/latest/operations/edit_json.html
    """

    name: str = "edit_json"

    def run(self, context: Context) -> None:
        file_path = ensure_path(context.file_path)
        with file_path.open() as f:
            data = json.load(f)

        data = merge_nested_dicts(data, context.merge_data)

        if context.execution_context.dry_run:
            self.on_dry_run(file_path, context.merge_data)
        else:
            with file_path.open("w") as f:
                json.dump(data, f, indent=context.indent)

    @staticmethod
    def on_dry_run(file_path: Path, merge_data: Dict[str, Any]) -> None:
        logger.info(
            f"Skipping the following edits to {file_path} due to `--dry-run` option:\n"
            + pformat_json(merge_data)
        )
