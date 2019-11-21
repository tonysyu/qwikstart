import io
import os
from contextlib import contextmanager
from pathlib import Path
from textwrap import dedent
from unittest.mock import Mock

from qwikstart import base_context

HERE = os.path.abspath(os.path.dirname(__file__))
TEMPLATES_DIR = os.path.join(HERE, "templates")


def get_execution_context(template_loader=None):
    source_dir = Path(HERE)
    target_dir = Path(HERE)
    if template_loader:
        return base_context.ExecutionContext(
            source_dir=source_dir,
            target_dir=target_dir,
            template_loader=template_loader,
        )
    else:
        return base_context.DefaultExecutionContext(
            source_dir=source_dir, target_dir=target_dir
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
