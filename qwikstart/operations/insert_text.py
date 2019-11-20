import os
from pathlib import Path

from typing_extensions import TypedDict

from ..base_context import BaseContext
from ..utils import indent
from .base import BaseOperation

__all__ = ["Operation"]


class RequiredContext(BaseContext):
    text: str
    line: int
    column: int
    file_path: Path


class Context(RequiredContext, total=False):
    line_ending: str
    match_indent: bool


class Operation(BaseOperation):
    """Operation inserting text on a given line"""

    name: str = "insert_text"

    def run(self, context: Context) -> None:
        file_path = context["file_path"]

        with file_path.open() as f:
            contents = f.readlines()

        contents.insert(context["line"], self.get_text(context))

        with file_path.open("w") as f:
            f.writelines(contents)

    def get_text(self, context):
        text = context["text"]
        if context.get("match_indent", True):
            text = indent(text, context["column"])

        line_ending = context.get("line_ending", os.linesep)
        text += line_ending
        return text
