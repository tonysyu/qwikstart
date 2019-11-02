from textwrap import dedent

from qwikstart.operations import inject_text
from qwikstart.testing import create_mock_file_path


class TestTextInject:
    def test_inject_line(self):
        context: inject_text.Context = {
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
        inject_action = inject_text.Operation()
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
        inject_action = inject_text.Operation(mapping={"line_number": "line"})
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
