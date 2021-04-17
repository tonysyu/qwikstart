import io
import os
import stat
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from pathlib import Path
from textwrap import dedent
from typing import Any, Dict, Iterator, Optional
from unittest.mock import Mock

from qwikstart.base_context import BaseContext, DictContext, ExecutionContext
from qwikstart.operations import base

HERE = os.path.abspath(os.path.dirname(__file__))
TEMPLATES_DIR = os.path.join(HERE, "templates")


def get_execution_context(**execution_context_kwargs: Any) -> ExecutionContext:
    execution_context_kwargs.setdefault("source_dir", Path(HERE))
    execution_context_kwargs.setdefault("target_dir", Path(HERE))
    return ExecutionContext(**execution_context_kwargs)


def create_mock_file_path(string_data: str) -> Mock:
    """Return mock `pathlib.Path` to file-like buffer containing `string_data`."""
    string_buffer = io.StringIO(dedent(string_data))

    @contextmanager
    def open_buffer(*args: Any, **kwargs: Any) -> Iterator[io.StringIO]:
        string_buffer.seek(0)
        yield string_buffer

    mock_file_path = Mock(spec=Path)
    mock_file_path.open.side_effect = open_buffer
    return mock_file_path


def read_file_path(file_path: Path) -> str:
    """Return text read from `file_path`."""
    with file_path.open() as f:
        return f.read()


def filemode(filename: Path) -> int:
    """Return a file's mode as an octal that should match the input to `os.chmod`."""
    file_stat = os.stat(str(filename))
    return stat.S_IMODE(file_stat.st_mode)


@dataclass(frozen=True)
class ContextWithDict(BaseContext):
    template_variables: Dict[str, Any] = field(default_factory=dict)


class FakeOperation(base.BaseOperation[ContextWithDict, DictContext]):
    """Fake operation used for testing.

    This operation has a special `run_context` used for verifying the context
    data passed to the `run` method.
    """

    name: str = "fake_op"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.run_context: Optional[ContextWithDict] = None

    def run(self, context: ContextWithDict) -> DictContext:
        self.run_context = context
        return asdict(context)
