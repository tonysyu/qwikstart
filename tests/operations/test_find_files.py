import os
import textwrap
from typing import Any
from unittest.mock import Mock, patch

from pyfakefs.fake_filesystem_unittest import TestCase

from qwikstart.operations import find_files

from .. import helpers


class TestFindFilesFS(TestCase):
    def setUp(self) -> None:
        self.setUpPyfakefs()

    def test_no_files(self) -> None:
        assert self.find_files("doesn't match anything") == []

    def test_single_no_match(self) -> None:
        self.fs.create_file("/path/to/match.txt")
        assert self.find_files("doesn't match anything") == []

    def test_single_file_match(self) -> None:
        self.fs.create_file("/path/to/match.txt", contents="match")
        assert self.find_files("match") == ["/path/to/match.txt"]

    def test_multiline_match(self) -> None:
        self.fs.create_file(
            "/path/to/match.txt",
            contents=textwrap.dedent(
                """
                x
                y
                match
                z
                """
            ),
        )
        assert self.find_files("match") == ["/path/to/match.txt"]

    def test_single_match_in_similarly_named_files(self) -> None:
        self.fs.create_file("/a/b/file.txt", contents="no-match")
        self.fs.create_file("/x/y/file.txt", contents="exact-match")
        assert self.find_files("exact-match") == ["/x/y/file.txt"]

    def test_multiple_file_matches(self) -> None:
        self.fs.create_file("/match1.txt", contents="hi")
        self.fs.create_file("/match2.txt", contents="hello")
        assert self.find_files("(hi|hello)") == ["/match1.txt", "/match2.txt"]

    @patch.object(find_files, "logger")
    def test_unreadable_file(self, logger: Mock) -> None:
        self.fs.create_file("/restricted_file.txt")
        os.chmod("/restricted_file.txt", 0o000)
        assert self.find_files("ignore this") == []
        logger.debug("Failed to read file /restricted_file.txt")

    def find_files(
        self, regex: str, directory: str = "/", output_name: str = "matching_files"
    ) -> Any:
        context = {
            "execution_context": helpers.get_execution_context(),
            "directory": directory,
            "regex": regex,
        }
        op = find_files.Operation()
        return op.execute(context)[output_name]
