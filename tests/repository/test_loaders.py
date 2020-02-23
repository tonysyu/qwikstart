from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterator, Optional
from unittest.mock import Mock, patch

import pytest
from pyfakefs.fake_filesystem_unittest import TestCase

from qwikstart.exceptions import RepoLoaderError
from qwikstart.repository import loaders

TEST_URL = "https://github.com/user/repo"


class TestLocalRepoLoader(TestCase):
    def setUp(self) -> None:
        self.setUpPyfakefs()

    def test_resolve_file(self) -> None:
        self.fs.create_file("/path/to/file.yml", contents='{"a": 1}')
        loader = loaders.LocalRepoLoader("/path/to/file.yml")
        assert loader.task_spec == {"a": 1}

    def test_resolve_directory(self) -> None:
        self.fs.create_file("/path/containing/qwikstart.yml", contents='{"a": 1}')
        loader = loaders.LocalRepoLoader("/path/containing/")
        assert loader.task_spec == {"a": 1}

    def test_unknown_file_type(self) -> None:
        self.fs.create_file("/path/to/file.txt", contents="this: is: invalid")
        loader = loaders.LocalRepoLoader("/path/to/file.txt")
        with pytest.raises(RepoLoaderError):
            loader.task_spec

    def test_repo_path_defaults_to_spec_path_parent(self) -> None:
        self.fs.create_file("/path/to/file.txt")
        loader = loaders.LocalRepoLoader("/path/to/file.txt")
        assert loader.repo_path == Path("/path/to")


class TestGitRepoLoader:
    def test_task_spec(self) -> None:
        with patch_git_repo_loader_dependencies(data={"greeting": "Hello"}):
            loader = loaders.GitRepoLoader(TEST_URL)
        assert loader.task_spec == {"greeting": "Hello"}

    def test_repo_path(self) -> None:
        with patch_git_repo_loader_dependencies() as mocks:
            loader = loaders.GitRepoLoader(TEST_URL)
        assert loader.repo_path == mocks.repo_path


@dataclass(frozen=True)
class MockGitRepoLoaderDependencies:
    repo_path: Path
    local_loader: Mock
    sync_git_repo: Mock


@contextmanager
def patch_git_repo_loader_dependencies(
    repo_path: Path = Path("/path/to/repo"),
    local_path_exists: bool = True,
    data: Optional[Dict[str, Any]] = None,
) -> Iterator[MockGitRepoLoaderDependencies]:
    mock_loader = Mock(repo_path=repo_path, task_spec=data)

    mock_sync = Mock(return_value=repo_path)
    with patch.object(loaders, "LocalRepoLoader", return_value=mock_loader):
        with patch.object(loaders.git, "sync_git_repo_locally", new=mock_sync):
            yield MockGitRepoLoaderDependencies(
                repo_path=repo_path, local_loader=mock_loader, sync_git_repo=mock_sync
            )
