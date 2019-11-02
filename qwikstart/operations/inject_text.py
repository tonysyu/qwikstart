from pathlib import Path

from typing_extensions import TypedDict

from .base import BaseOperation


__all__ = ["InjectText"]


class Context(TypedDict):
    text: str
    line: int
    file_path: Path


class InjectText(BaseOperation):
    """Operation injecting text on a given line"""

    name: str = "inject"

    def run(self, context: Context) -> None:
        file_path = context["file_path"]

        with file_path.open() as f:
            contents = f.readlines()

        contents.insert(context["line"], context["text"])

        with file_path.open("w") as f:
            f.writelines(contents)
