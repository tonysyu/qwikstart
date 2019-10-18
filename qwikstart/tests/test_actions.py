import io
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent
from typing import Type

from qwikstart import actions


def create_mock_file_wrapper(file_text):

    string_buffer = io.StringIO(file_text)

    @dataclass
    class MockFileWrapper(actions.BaseFileWrapper):

        file_path: Path = ""

        @contextmanager
        def open_for_read(self):
            string_buffer.seek(0)
            yield string_buffer

        @contextmanager
        def open_for_write(self):
            string_buffer.seek(0)
            yield string_buffer

        @staticmethod
        def read():
            string_buffer.seek(0)
            return string_buffer.read()

    return MockFileWrapper


class MockContext:

    working_dir: Path = Path(".")


class TestableTextInjectAction(actions.TextInjectAction):
    file_path = Path("path/that/is/ignored")

    def __init__(
        self,
        inject_text: str,
        mock_file_class: Type[actions.BaseFileWrapper],
        line: int,
    ):
        self.inject_text = inject_text
        self.file_wrapper_class = mock_file_class
        self.line = line


class TestTextInjectAction:
    def test_inject_line(self):
        mock_file_class = create_mock_file_wrapper(
            dedent(
                """
                    A
                    B
                    C
                """
            )
        )
        inject_action = TestableTextInjectAction(
            inject_text="New Line\n", mock_file_class=mock_file_class, line=2
        )
        inject_action.do(MockContext())
        assert mock_file_class.read() == dedent(
            """
                A
                New Line
                B
                C
            """
        )
