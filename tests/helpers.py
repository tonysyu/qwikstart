import io
import os
from contextlib import contextmanager
from pathlib import Path
from textwrap import dedent
from unittest.mock import Mock

from qwikstart.base_context import ExecutionContext

HERE = os.path.abspath(os.path.dirname(__file__))
TEMPLATES_DIR = os.path.join(HERE, "templates")
DEFAULT_EXECUTION_CONTEXT = ExecutionContext(
    source_dir=Path(HERE), target_dir=Path(HERE)
)


def create_mock_file_path(string_data: str):
    """Return mock `pathlib.Path` to file-like buffer containing `string_data`.
    """
    string_buffer = io.StringIO(dedent(string_data))

    @contextmanager
    def open_buffer(*args, **kwargs):
        string_buffer.seek(0)
        yield string_buffer

    mock_file_path = Mock(spec=Path)
    mock_file_path.open.side_effect = open_buffer
    return mock_file_path


def read_file_path(file_path: Path):
    """Return text read from `file_path`."""
    with file_path.open() as f:
        return f.read()
