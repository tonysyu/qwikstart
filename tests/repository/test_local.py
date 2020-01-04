import pytest
from pyfakefs.fake_filesystem_unittest import TestCase

from qwikstart.exceptions import TaskLoaderError
from qwikstart.repository import local


class TestLocalPathResolver(TestCase):
    def setUp(self) -> None:
        self.setUpPyfakefs()

    def test_resolve_file(self) -> None:
        self.fs.create_file("/path/to/file.yml", contents='{"a": 1}')
        loader = local.LocalRepoLoader("/path/to/file.yml")
        assert loader.can_load()
        assert loader.load_task_data() == {"a": 1}

    def test_resolve_directory(self) -> None:
        self.fs.create_file("/path/containing/qwikstart.yml", contents='{"a": 1}')
        loader = local.LocalRepoLoader("/path/containing/")
        assert loader.can_load()
        assert loader.load_task_data() == {"a": 1}

    def test_unknown_file_type(self) -> None:
        self.fs.create_file("/path/to/file.txt", contents='{"a": 1}')
        loader = local.LocalRepoLoader("/path/to/file.txt")
        assert not loader.can_load()
        with pytest.raises(TaskLoaderError):
            loader.load_task_data()
