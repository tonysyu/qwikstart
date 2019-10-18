import abc
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Type

__all__ = ["Action"]


class Action(abc.ABC):

    name: str

    @abc.abstractmethod
    def do(self, context) -> None:
        """Override with action"""


class BaseFileWrapper:

    file_path: Path

    def __init__(self, file_path):
        self.file_path = file_path

    @contextmanager
    def open_for_read(self):
        pass

    @contextmanager
    def open_for_write(self):
        pass


class FileWrapper(BaseFileWrapper):
    @contextmanager
    def open_for_read(self):
        with open(self.file_path, "r") as f:
            yield f

    @contextmanager
    def open_for_write(self):
        with open(self.file_path, "w") as f:
            yield f


@dataclass
class TextInjectAction(Action):
    """Action injecting text on a given line"""

    file_path: Path
    inject_text: str
    line: int
    name: str = "inject"
    file_wrapper_class: Type[BaseFileWrapper] = FileWrapper

    def do(self, context) -> None:
        file_wrapper = self.file_wrapper_class(
            file_path=context.working_dir.joinpath(self.file_path)
        )

        with file_wrapper.open_for_read() as f:
            contents = f.readlines()

        contents.insert(self.line, self.inject_text)

        with file_wrapper.open_for_write() as f:
            f.writelines(contents)
