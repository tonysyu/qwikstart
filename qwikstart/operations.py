import abc
from pathlib import Path
from typing import Any, Dict

__all__ = ["InjectText", "Operation"]


class Operation:
    """A step within an qwikstart `Task`"""

    name: str
    required_data: Dict[str, Any] = {}
    supplied_data: Dict[str, Any] = {}

    @abc.abstractmethod
    def do(self, context, task_data) -> None:
        """Override with action"""


class InjectText(Operation):
    """Operation injecting text on a given line"""

    name: str = "inject"
    required_data: Dict[str, Any] = {"file_path": Path}

    def __init__(self, text: str, line: int):
        self.text = text
        self.line = line

    def do(self, context, task_data) -> None:
        file_path = task_data["file_path"]

        with file_path.open() as f:
            contents = f.readlines()

        contents.insert(self.line, self.text)

        with file_path.open("w") as f:
            f.writelines(contents)
