import pytest
from pyfakefs.fake_filesystem_unittest import TestCase

from qwikstart.exceptions import TaskLoaderError
from qwikstart.repository import local


class TestLocalPathResolver(TestCase):
    def setUp(self) -> None:
        self.setUpPyfakefs()

    def test_resolve_file(self) -> None:
        self.fs.create_file("/path/to/file.yml", contents='{"a": 1}')
        res = local.LocalRepoLoader("/path/to/file.yml")
        assert res.exists()
        assert res.parsed_data() == {"a": 1}

    def test_resolve_directory(self) -> None:
        self.fs.create_file("/path/containing/qwikstart.yml", contents='{"a": 1}')
        res = local.LocalRepoLoader("/path/containing/")
        assert res.exists()
        assert res.parsed_data() == {"a": 1}

    def test_unknown_file_type(self) -> None:
        self.fs.create_file("/path/to/file.txt", contents='{"a": 1}')
        res = local.LocalRepoLoader("/path/to/file.txt")
        assert res.exists()
        with pytest.raises(TaskLoaderError):
            res.parsed_data()
