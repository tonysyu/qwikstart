import os
from pathlib import Path

from pyfakefs.fake_filesystem_unittest import TestCase

from qwikstart.operations import append_text

from .. import helpers


class TestAppendText(TestCase):
    def setUp(self) -> None:
        self.setUpPyfakefs()
        self.file_path = Path("/path/to/test.txt")

    def test_append_to_empty_file(self) -> None:
        self.fs.create_file(self.file_path)
        assert self.append("New line") == "\nNew line"

    def test_append_to_existing(self) -> None:
        self.fs.create_file(self.file_path, contents="First line")
        os.chmod(self.file_path, 0o777)
        assert self.append("New line") == "First line\nNew line"
        assert helpers.filemode(self.file_path) == 0o777

    def test_file_permissions_not_changed(self) -> None:
        self.fs.create_file(self.file_path)
        os.chmod(self.file_path, 0o777)
        assert self.append("New line") == "\nNew line"
        assert helpers.filemode(self.file_path) == 0o777

    def append(self, text: str) -> str:
        context = {
            "execution_context": helpers.get_execution_context(),
            "text": text,
            "file_path": self.file_path,
        }
        append_op = append_text.Operation()
        append_op.execute(context)
        return helpers.read_file_path(self.file_path)
