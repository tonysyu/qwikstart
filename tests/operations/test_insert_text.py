from textwrap import dedent

from qwikstart.operations import insert_text

from ..helpers import create_mock_file_path, read_file_path


class TestTextInject:
    def test_insert_line(self):
        context: insert_text.Context = {
            "text": "New Line",
            "line": 2,
            "column": 0,
            "file_path": create_mock_file_path(
                """
                    A
                    B
                """
            ),
        }
        assert insert_text_and_return_file_text(context) == dedent(
            """
                A
                New Line
                B
            """
        )

    def test_return_context_unchanged(self):
        context: insert_text.Context = {
            "text": "New Line",
            "line": 1,
            "column": 0,
            "file_path": create_mock_file_path("A\nB"),
        }
        insert_action = insert_text.Operation()
        assert insert_action.execute(context) == context

    def test_insert_line_with_mapped_data(self):
        context = {
            "text": "New Line",
            "line_number": 2,
            "column": 0,
            "file_path": create_mock_file_path(
                """
                    A
                    B
                """
            ),
        }
        mapping = {"line_number": "line"}
        assert insert_text_and_return_file_text(
            context, mapping=mapping
        ) == dedent(
            """
                A
                New Line
                B
            """
        )

    def test_insert_line_with_matched_indent(self):
        context = {
            "text": "New Line",
            "line": 3,
            "column": 4,
            "file_path": create_mock_file_path(
                """
                    A
                        B
                        C
                """
            ),
        }
        assert insert_text_and_return_file_text(context) == dedent(
            """
                A
                    B
                    New Line
                    C
            """
        )

    def test_insert_multiline_indent(self):
        context = {
            "text": "One\nTwo",
            "line": 3,
            "column": 4,
            "file_path": create_mock_file_path(
                """
                    A
                        B
                        C
                """
            ),
        }
        assert insert_text_and_return_file_text(context) == dedent(
            """
                A
                    B
                    One
                    Two
                    C
            """
        )

    def test_insert_line_ignoring_indent(self):
        context = {
            "text": "New Line",
            "line": 3,
            "column": 4,
            "match_indent": False,
            "file_path": create_mock_file_path(
                """
                    A
                        B
                        C
                """
            ),
        }
        assert insert_text_and_return_file_text(context) == dedent(
            """
                A
                    B
                New Line
                    C
            """
        )

    def test_insert_line_with_no_trailing_new_line(self):
        context = {
            "text": "New Line",
            "line": 2,
            "column": 0,
            "line_ending": "",
            "file_path": create_mock_file_path(
                """
                    A
                    B
                """
            ),
        }
        assert insert_text_and_return_file_text(context) == dedent(
            """
                A
                New LineB
            """
        )


def insert_text_and_return_file_text(context: insert_text.Context, **kwargs):
    insert_action = insert_text.Operation(**kwargs)
    insert_action.execute(context)
    return read_file_path(context["file_path"])
