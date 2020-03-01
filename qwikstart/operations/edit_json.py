import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from ..base_context import BaseContext
from ..utils import ensure_path, merge_nested_dicts
from .base import BaseOperation
from .utils import FILE_PATH_HELP

__all__ = ["Operation"]

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
    """Operation edit json by merging data into existing json data."""

    name: str = "edit_json"

    def run(self, context: Context) -> None:
        file_path = ensure_path(context.file_path)
        with file_path.open() as f:
            data = json.load(f)

        data = merge_nested_dicts(data, context.merge_data)

        with file_path.open("w") as f:
            json.dump(data, f, indent=context.indent)
