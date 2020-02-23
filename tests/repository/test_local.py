from pathlib import Path

import pytest
from pyfakefs.fake_filesystem_unittest import TestCase

from qwikstart.exceptions import RepoLoaderError
from qwikstart.repository import local


class TestLocalRepoLoader(TestCase):
    def setUp(self) -> None:
        self.setUpPyfakefs()

    def test_resolve_file(self) -> None:
        self.fs.create_file("/path/to/file.yml", contents='{"a": 1}')
        loader = local.LocalRepoLoader("/path/to/file.yml")
        assert loader.task_spec == {"a": 1}

    def test_resolve_directory(self) -> None:
        self.fs.create_file("/path/containing/qwikstart.yml", contents='{"a": 1}')
        loader = local.LocalRepoLoader("/path/containing/")
        assert loader.task_spec == {"a": 1}

    def test_unknown_file_type(self) -> None:
        self.fs.create_file("/path/to/file.txt", contents='{"a": 1}')
        loader = local.LocalRepoLoader("/path/to/file.txt")
        with pytest.raises(RepoLoaderError):
            loader.task_spec

    def test_repo_path_defaults_to_spec_path_parent(self) -> None:
        self.fs.create_file("/path/to/file.txt")
        loader = local.LocalRepoLoader("/path/to/file.txt")
        assert loader.repo_path == Path("/path/to")
