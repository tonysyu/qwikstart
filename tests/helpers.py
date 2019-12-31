import io
import os
from contextlib import contextmanager
from pathlib import Path
from textwrap import dedent
from typing import Any, Iterator
from unittest.mock import Mock

from qwikstart.base_context import ExecutionContext

HERE = os.path.abspath(os.path.dirname(__file__))
TEMPLATES_DIR = os.path.join(HERE, "templates")


def get_execution_context(**execution_context_kwargs: Any) -> ExecutionContext:
    execution_context_kwargs.setdefault("source_dir", Path(HERE))
    execution_context_kwargs.setdefault("target_dir", Path(HERE))
    return ExecutionContext(**execution_context_kwargs)


def create_mock_file_path(string_data: str) -> Mock:
    """Return mock `pathlib.Path` to file-like buffer containing `string_data`.
    """
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
