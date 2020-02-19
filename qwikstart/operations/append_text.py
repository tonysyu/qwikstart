import os
from dataclasses import dataclass
from pathlib import Path

from ..base_context import BaseContext
from ..utils import ensure_path
from .base import BaseOperation

__all__ = ["Operation"]


@dataclass(frozen=True)
class Context(BaseContext):
    text: str
    file_path: Path
    prefix: str = os.linesep
    suffix: str = ""


class Operation(BaseOperation[Context, None]):
    """Operation for appending text on a given file."""

    name: str = "append_text"

    def run(self, context: Context) -> None:
        file_path = ensure_path(context.file_path)

        with file_path.open("a") as f:
            f.write(self.get_text(context))

    def get_text(self, context: Context) -> str:
        return "".join([context.prefix, context.text, context.suffix])
