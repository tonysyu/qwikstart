import os
from pathlib import Path
from textwrap import dedent
from typing import Any

from pyfakefs.fake_filesystem_unittest import TestCase

from qwikstart.base_context import DictContext
from qwikstart.operations import OperationConfig, insert_text

from .. import helpers


class TestInsertTextFakeFS(TestCase):
    def setUp(self) -> None:
        self.setUpPyfakefs()
        self.file_path = Path("/path/to/test.txt")

    def test_insert(self) -> None:
        self.fs.create_file(self.file_path, contents="Hello")
        assert self.insert_on_first_line("New Line") == "New Line\nHello"

    def test_file_permissions_not_changed(self) -> None:
        self.fs.create_file(self.file_path, contents="Hello")
        os.chmod(self.file_path, 0o777)
        assert self.insert_on_first_line("New Line") == "New Line\nHello"
        assert helpers.filemode(self.file_path) == 0o777

    def insert_on_first_line(self, text: str) -> str:
        context = {
            "execution_context": helpers.get_execution_context(),
            "text": text,
            "line": 0,
            "column": 0,
            "file_path": self.file_path,
        }
        return insert_text_and_return_file_text(context)


class TestInsertText:
    def test_insert_line(self) -> None:
        context = {
            "execution_context": helpers.get_execution_context(),
            "text": "New Line",
            "line": 2,
            "column": 0,
            "file_path": helpers.create_mock_file_path(
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

    def test_return_context_unchanged(self) -> None:
        context = {
            "execution_context": helpers.get_execution_context(),
            "text": "New Line",
            "line": 1,
            "column": 0,
            "file_path": helpers.create_mock_file_path("A\nB"),
        }
        insert_action = insert_text.Operation()
        assert insert_action.execute(context) == context

    def test_insert_line_with_mapped_data(self) -> None:
        context = {
            "execution_context": helpers.get_execution_context(),
            "text": "New Line",
            "line_number": 2,
            "column": 0,
            "file_path": helpers.create_mock_file_path(
                """
                    A
                    B
                """
            ),
        }
        assert insert_text_and_return_file_text(
            context, config=OperationConfig(input_mapping={"line_number": "line"})
        ) == dedent(
            """
                A
                New Line
                B
            """
        )

    def test_insert_line_with_matched_indent(self) -> None:
        context = {
            "execution_context": helpers.get_execution_context(),
            "text": "New Line",
            "line": 3,
            "column": 4,
            "file_path": helpers.create_mock_file_path(
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

    def test_insert_multiline_indent(self) -> None:
        context = {
            "execution_context": helpers.get_execution_context(),
            "text": "One\nTwo",
            "line": 3,
            "column": 4,
            "file_path": helpers.create_mock_file_path(
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

    def test_insert_line_ignoring_indent(self) -> None:
        context = {
            "execution_context": helpers.get_execution_context(),
            "text": "New Line",
            "line": 3,
            "column": 4,
            "match_indent": False,
            "file_path": helpers.create_mock_file_path(
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

    def test_insert_line_with_no_trailing_new_line(self) -> None:
        context = {
            "execution_context": helpers.get_execution_context(),
            "text": "New Line",
            "line": 2,
            "column": 0,
            "line_ending": "",
            "file_path": helpers.create_mock_file_path(
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


def insert_text_and_return_file_text(context: DictContext, **kwargs: Any) -> str:
    insert_action = insert_text.Operation(**kwargs)
    insert_action.execute(context)
    return helpers.read_file_path(context["file_path"])
