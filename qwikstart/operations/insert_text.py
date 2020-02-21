import os
from dataclasses import dataclass
from pathlib import Path

from ..base_context import BaseContext
from ..utils import ensure_path, indent
from .base import BaseOperation

__all__ = ["Operation"]


@dataclass(frozen=True)
class Context(BaseContext):
    text: str
    line: int
    column: int
    file_path: Path
    line_ending: str = os.linesep
    match_indent: bool = True


class Operation(BaseOperation[Context, None]):
    """Operation inserting text on a given line"""

    name: str = "insert_text"

    def run(self, context: Context) -> None:
        file_path = ensure_path(context.file_path)
        text = self.get_text(context)
        insert_text_in_file(file_path, context.line, text)

    def get_text(self, context: Context) -> str:
        text = context.text
        if context.match_indent:
            text = indent(text, context.column)

        text += context.line_ending
        return text


def insert_text_in_file(file_path: Path, line_number: int, text: str) -> None:
    with file_path.open() as f:
        contents = f.readlines()

    contents.insert(line_number, text)

    with file_path.open("w") as f:
        f.writelines(contents)
