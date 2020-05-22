import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from ..base_context import BaseContext
from ..utils import ensure_path, io, merge_nested_dicts, pformat_json
from .base import BaseOperation
from .utils import FILE_PATH_HELP

__all__ = ["Operation"]

logger = logging.getLogger(__name__)

CONTEXT_HELP = {
    "file_path": FILE_PATH_HELP,
    "merge_data": "Data that will be merged into existing data in yaml file.",
}


@dataclass(frozen=True)
class Context(BaseContext):
    file_path: Path
    merge_data: Dict[str, Any]

    @classmethod
    def help(cls, field_name: str) -> Optional[str]:
        return CONTEXT_HELP.get(field_name)


class Operation(BaseOperation[Context, None]):
    """Operation to edit yaml by merging data into existing yaml data.

    See https://qwikstart.readthedocs.io/en/latest/operations/edit_yaml.html
    """

    name: str = "edit_yaml"

    def run(self, context: Context) -> None:
        file_path = ensure_path(context.file_path)

        data = io.load_yaml_file(file_path)
        data = merge_nested_dicts(data, context.merge_data, inplace=True)

        if context.execution_context.dry_run:
            self.on_dry_run(file_path, context.merge_data)
        else:
            io.dump_yaml_file(data, file_path)

    @staticmethod
    def on_dry_run(file_path: Path, merge_data: Dict[str, Any]) -> None:
        logger.info(
            f"Skipping the following edits to {file_path} due to `--dry-run` option:\n"
            + pformat_json(merge_data)
        )
