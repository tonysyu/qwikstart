from textwrap import dedent

from qwikstart.operations import inject_text
from ..helpers import create_mock_file_path, read_file_path


class TestTextInject:
    def test_inject_line(self):
        context: inject_text.Context = {
            "text": "New Line",
            "line": 2,
            "column": 0,
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
        assert read_file_path(context["file_path"]) == dedent(
            """
                A
                New Line
                B
                C
            """
        )

    def test_inject_line_with_mapped_data(self):
        context = {
            "text": "New Line",
            "line_number": 2,
            "column": 0,
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
        assert read_file_path(context["file_path"]) == dedent(
            """
                A
                New Line
                B
                C
            """
        )
        assert output_context == context

    def test_inject_line_with_matched_indent(self):
        context = {
            "text": "New Line",
            "line_number": 3,
            "column": 4,
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
        assert read_file_path(context["file_path"]) == dedent(
            """
                A
                    B
                    New Line
                    C
            """
        )
        assert output_context == context

    def test_inject_line_ignoring_indent(self):
        context = {
            "text": "New Line",
            "line_number": 3,
            "column": 4,
            "match_indent": False,
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
        assert read_file_path(context["file_path"]) == dedent(
            """
                A
                    B
                New Line
                    C
            """
        )
        assert output_context == context

    def test_inject_line_with_no_trailing_new_line(self):
        context = {
            "text": "New Line",
            "line_number": 2,
            "column": 0,
            "line_ending": "",
            "file_path": create_mock_file_path(
                dedent(
                    """
                        A
                        B
                    """
                )
            ),
        }
        inject_action = inject_text.Operation(mapping={"line_number": "line"})
        output_context = inject_action.execute(context)
        assert read_file_path(context["file_path"]) == dedent(
            """
                A
                New LineB
            """
        )
        assert output_context == context
