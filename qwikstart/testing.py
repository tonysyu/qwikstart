import io
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import Mock


def create_mock_file_path(string_data: str):
    """Return mock `pathlib.Path` to file-like buffer containing `string_data`.
    """
    string_buffer = io.StringIO(string_data)

    @contextmanager
    def open_buffer(*args, **kwargs):
        string_buffer.seek(0)
        yield string_buffer

    mock_file_path = Mock(spec=Path)
    mock_file_path.open.side_effect = open_buffer
    return mock_file_path
