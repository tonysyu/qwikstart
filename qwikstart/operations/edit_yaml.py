from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from ..base_context import BaseContext
from ..utils import ensure_path, io, merge_nested_dicts
from .base import BaseOperation
from .utils import FILE_PATH_HELP

__all__ = ["Operation"]

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
    """Operation edit yaml by merging data into existing yaml data."""

    name: str = "edit_yaml"

    def run(self, context: Context) -> None:
        file_path = ensure_path(context.file_path)

        data = io.load_yaml_file(file_path)
        data = merge_nested_dicts(data, context.merge_data, inplace=True)

        io.dump_yaml_file(data, file_path)
