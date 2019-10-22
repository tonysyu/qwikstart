import io
from contextlib import contextmanager
from pathlib import Path
from textwrap import dedent
from unittest.mock import Mock

from qwikstart import operations


class MockContext:
    pass


def create_mock_file_path(string_data):
    string_buffer = io.StringIO(string_data)

    @contextmanager
    def open_buffer(*args, **kwargs):
        string_buffer.seek(0)
        yield string_buffer

    mock_file_path = Mock(spec=Path)
    mock_file_path.open.side_effect = open_buffer
    return mock_file_path


class TestTextInject:
    def test_inject_line(self):
        task_data = {
            "file_path": create_mock_file_path(
                dedent(
                    """
                        A
                        B
                        C
                    """
                )
            )
        }
        inject_action = operations.InjectText(text="New Line\n", line=2)
        inject_action.do(MockContext(), task_data)
        with task_data["file_path"].open() as f:
            assert f.read() == dedent(
                """
                    A
                    New Line
                    B
                    C
                """
            )
