import io
from contextlib import contextmanager
from pathlib import Path
from textwrap import dedent
from unittest.mock import Mock

from qwikstart.operations import inject_text


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
        context: inject_text.InjectTextContext = {
            "text": "New Line\n",
            "line": 2,
            "file_path": create_mock_file_path(
                dedent(
                    """
                        A
                        B
                        C
                    """
                )
            ),
        }
        inject_action = inject_text.InjectText()
        inject_action.execute(context)
        with context["file_path"].open() as f:
            assert f.read() == dedent(
                """
                    A
                    New Line
                    B
                    C
                """
            )

    def test_inject_line_with_mapped_data(self):
        context = {
            "text": "New Line\n",
            "line_number": 2,
            "file_path": create_mock_file_path(
                dedent(
                    """
                        A
                        B
                        C
                    """
                )
            ),
        }
        inject_action = inject_text.InjectText(mapping={"line_number": "line"})
        output_context = inject_action.execute(context)
        with context["file_path"].open() as f:
            assert f.read() == dedent(
                """
                    A
                    New Line
                    B
                    C
                """
            )
        assert output_context == context
