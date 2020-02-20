import os
import textwrap
from pathlib import Path

from pyfakefs.fake_filesystem_unittest import TestCase

from qwikstart.operations import search_and_replace

from .. import helpers


class TestSearchAndReplace(TestCase):
    def setUp(self) -> None:
        self.setUpPyfakefs()
        self.file_path = Path("/path/to/test.txt")

    def test_single_word(self) -> None:
        self.fs.create_file(self.file_path, contents="Hello World!")
        assert self.search_and_replace("Hello", "Howdy") == "Howdy World!"

    def test_multiline(self) -> None:
        self.fs.create_file(
            self.file_path,
            contents=textwrap.dedent(
                """
                Before
                replace
                these
                lines
                After
                """
            ),
        )
        output = self.search_and_replace("replace\nthese\nlines", "new\ntext")
        assert output == textwrap.dedent(
            """
            Before
            new
            text
            After
            """
        )

    def test_regex(self) -> None:
        self.fs.create_file(self.file_path, contents="My email is private@test.com")
        output = self.search_and_replace("[^ ]+@", "xxx@", use_regex=True)
        assert output == "My email is xxx@test.com"

    def test_file_permissions_not_changed(self) -> None:
        self.fs.create_file(self.file_path, contents="Hello World!")
        os.chmod(self.file_path, 0o777)
        assert self.search_and_replace("Hello", "Howdy") == "Howdy World!"
        assert helpers.filemode(self.file_path) == 0o777

    def search_and_replace(
        self, search: str, replace: str, use_regex: bool = False
    ) -> str:
        context = {
            "execution_context": helpers.get_execution_context(),
            "file_path": self.file_path,
            "search": search,
            "replace": replace,
            "use_regex": use_regex,
        }
        op = search_and_replace.Operation()
        op.execute(context)
        return helpers.read_file_path(self.file_path)
