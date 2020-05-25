from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterator, Optional
from unittest.mock import Mock, patch

import pytest
from pyfakefs.fake_filesystem_unittest import TestCase

from qwikstart.exceptions import RepoLoaderError, TaskParserError
from qwikstart.repository import loaders
from qwikstart.utils import io

FAKE_PATH_STR = "/path/to/fake.yml"
TEST_URL = "https://github.com/user/repo"
DETACHED_TASK_SPEC = {"source": {"url": TEST_URL}}
TASK_SPEC_PATH = "/fake/local/path/qwikstart.yml"


class TestGetRepoLoader:
    def test_loader_for_local_path(self) -> None:
        with patch.object(loaders, "RepoLoader") as loader_class:
            loaders.get_repo_loader(FAKE_PATH_STR)
        loader_class.assert_called_once_with(FAKE_PATH_STR)

    def test_git_loader(self) -> None:
        repo_url = "http://example.com"
        with patch.object(loaders, "GitRepoLoader") as loader_class:
            loader = loaders.get_repo_loader(FAKE_PATH_STR, repo_url=repo_url)
        assert loader is loader_class.return_value
        loader_class.assert_called_once_with(repo_url, FAKE_PATH_STR)


class TestRepoLoaderFS(TestCase):
    def setUp(self) -> None:
        self.setUpPyfakefs()

    def test_resolve_file(self) -> None:
        self.fs.create_file("/path/to/file.yml", contents='{"a": 1}')
        loader = loaders.RepoLoader("/path/to/file.yml")
        assert loader.task_spec == {"a": 1}

    def test_resolve_directory(self) -> None:
        self.fs.create_file("/path/containing/qwikstart.yml", contents='{"a": 1}')
        loader = loaders.RepoLoader("/path/containing/")
        assert loader.task_spec == {"a": 1}

    def test_unknown_file_type(self) -> None:
        self.fs.create_file("/path/to/file.txt", contents="this: is: invalid")
        with pytest.raises(TaskParserError):
            loaders.RepoLoader("/path/to/file.txt")

    def test_repo_path_defaults_to_spec_path_parent(self) -> None:
        self.fs.create_file("/path/to/file.txt", contents="{}")
        loader = loaders.RepoLoader("/path/to/file.txt")
        assert loader.repo_path == Path("/path/to")


class TestGitRepoLoader:
    def test_task_spec(self) -> None:
        with patch_git_repo_loader_dependencies(task_spec={"greeting": "Hello"}):
            loader = loaders.GitRepoLoader(TEST_URL)
        assert loader.task_spec == {"greeting": "Hello"}

    def test_repo_path(self) -> None:
        with patch_git_repo_loader_dependencies() as mocks:
            loader = loaders.GitRepoLoader(TEST_URL)
        assert loader.repo_path == mocks.repo_path


class TestRepoLoaderWithSourceUrl:
    def test_task_spec_from_local_path(self) -> None:
        with patch_repo_loader_deps(DETACHED_TASK_SPEC) as mocks:
            loader = loaders.RepoLoader(TASK_SPEC_PATH)

        assert loader.task_spec == DETACHED_TASK_SPEC
        mocks.read_from_url.assert_not_called()
        mocks.read_file.assert_called_once_with(Path(TASK_SPEC_PATH))
        mocks.sync_git_repo.assert_called_once_with(TEST_URL)

    def test_task_spec_from_url(self) -> None:
        task_spec_url = "https://example.com/qwikstart.yml"
        with patch_repo_loader_deps(DETACHED_TASK_SPEC) as mocks:
            loader = loaders.RepoLoader(task_spec_url)

        assert loader.task_spec == DETACHED_TASK_SPEC
        mocks.read_from_url.assert_called_once_with(task_spec_url)
        mocks.read_file.assert_not_called()
        mocks.sync_git_repo.assert_called_once_with(TEST_URL)

    def test_remote_task_spec_without_source_url(self) -> None:
        task_spec_url = "https://example.com/qwikstart.yml"
        with patch_repo_loader_deps({}) as mocks:
            with pytest.raises(RepoLoaderError):
                loaders.RepoLoader(task_spec_url)
        mocks.sync_git_repo.assert_not_called()

    def test_repo_path(self) -> None:
        repo_path = Path("/path/to/repo")
        with patch_repo_loader_deps(DETACHED_TASK_SPEC, repo_path=repo_path):
            loader = loaders.RepoLoader(TASK_SPEC_PATH)
        assert loader.repo_path == repo_path


@dataclass(frozen=True)
class MockGitRepoLoaderDependencies:
    repo_path: Path
    loader: Mock
    sync_git_repo: Mock


@contextmanager
def patch_git_repo_loader_dependencies(
    repo_path: Path = Path("/path/to/repo"), task_spec: Optional[Dict[str, Any]] = None
) -> Iterator[MockGitRepoLoaderDependencies]:
    mock_loader = Mock(repo_path=repo_path, task_spec=task_spec)

    mock_sync = Mock(return_value=repo_path)
    with patch.object(loaders, "RepoLoader", return_value=mock_loader):
        with patch.object(loaders.git, "sync_git_repo_locally", new=mock_sync):
            yield MockGitRepoLoaderDependencies(
                repo_path=repo_path, loader=mock_loader, sync_git_repo=mock_sync
            )


@dataclass(frozen=True)
class MockRepoLoaderDependencies:
    repo_path: Path
    read_file: Mock
    read_from_url: Mock
    sync_git_repo: Mock


@contextmanager
def patch_repo_loader_deps(
    task_spec: Dict[str, Any], repo_path: Path = Path("/path/to/repo")
) -> Iterator[MockRepoLoaderDependencies]:
    task_spec_yaml_string = io.dump_yaml_string(task_spec)
    sync = Mock(return_value=repo_path)
    read_url = Mock(return_value=task_spec_yaml_string)
    read_file = Mock(return_value=task_spec_yaml_string)
    with patch.object(loaders.io, "read_file_contents", new=read_file):
        with patch.object(loaders.http, "read_from_url", new=read_url):
            with patch.object(loaders.git, "sync_git_repo_locally", new=sync):
                yield MockRepoLoaderDependencies(
                    repo_path=repo_path,
                    read_file=read_file,
                    read_from_url=read_url,
                    sync_git_repo=sync,
                )
