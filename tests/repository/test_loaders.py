from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterator, Optional, Union
from unittest.mock import Mock, patch

import pytest
from pyfakefs.fake_filesystem_unittest import TestCase

from qwikstart.exceptions import RepoLoaderError
from qwikstart.repository import loaders

TEST_URL = "https://github.com/user/repo"
DETACHED_TASK_SPEC = {"source": {"url": TEST_URL}}
TASK_SPEC_PATH = "/fake/local/path/qwikstart.yml"


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
        with patch_git_repo_loader_dependencies(task_spec={"greeting": "Hello"}):
            loader = loaders.GitRepoLoader(TEST_URL)
        assert loader.task_spec == {"greeting": "Hello"}

    def test_repo_path(self) -> None:
        with patch_git_repo_loader_dependencies() as mocks:
            loader = loaders.GitRepoLoader(TEST_URL)
        assert loader.repo_path == mocks.repo_path


class TestDetachedRepoLoader:
    def test_task_spec_from_local_path(self) -> None:
        with patch_detached_repo_loader_deps(DETACHED_TASK_SPEC) as mocks:
            loader = loaders.DetachedRepoLoader(TASK_SPEC_PATH)

        assert loader.task_spec == DETACHED_TASK_SPEC
        mocks.read_from_url.assert_not_called()
        mocks.load_yaml_file.assert_called_once_with(Path(TASK_SPEC_PATH))
        mocks.sync_git_repo.assert_called_once_with(TEST_URL)

    def test_task_spec_from_url(self) -> None:
        task_spec_url = "https://example.com/qwikstart.yml"
        with patch_detached_repo_loader_deps(DETACHED_TASK_SPEC) as mocks:
            loader = loaders.DetachedRepoLoader(task_spec_url)

        assert loader.task_spec == DETACHED_TASK_SPEC
        mocks.read_from_url.assert_called_once_with(task_spec_url)
        mocks.load_yaml_file.assert_not_called()
        mocks.sync_git_repo.assert_called_once_with(TEST_URL)

    def test_remote_task_spec_without_source_url(self) -> None:
        task_spec_url = "https://example.com/qwikstart.yml"
        with patch_detached_repo_loader_deps({}) as mocks:
            with pytest.raises(RepoLoaderError):
                loaders.DetachedRepoLoader(task_spec_url)
        mocks.sync_git_repo.assert_not_called()

    def test_repo_path(self) -> None:
        repo_path = Path("/path/to/repo")
        with patch_detached_repo_loader_deps(DETACHED_TASK_SPEC, repo_path=repo_path):
            loader = loaders.DetachedRepoLoader(TASK_SPEC_PATH)
        assert loader.repo_path == repo_path


@dataclass(frozen=True)
class MockGitRepoLoaderDependencies:
    repo_path: Path
    local_loader: Mock
    sync_git_repo: Mock


@contextmanager
def patch_git_repo_loader_dependencies(
    repo_path: Path = Path("/path/to/repo"), task_spec: Optional[Dict[str, Any]] = None
) -> Iterator[MockGitRepoLoaderDependencies]:
    mock_loader = Mock(repo_path=repo_path, task_spec=task_spec)

    mock_sync = Mock(return_value=repo_path)
    with patch.object(loaders, "LocalRepoLoader", return_value=mock_loader):
        with patch.object(loaders.git, "sync_git_repo_locally", new=mock_sync):
            yield MockGitRepoLoaderDependencies(
                repo_path=repo_path, local_loader=mock_loader, sync_git_repo=mock_sync
            )


@dataclass(frozen=True)
class MockDetachedRepoLoaderDependencies:
    repo_path: Path
    local_loader: Mock
    load_yaml_file: Mock
    load_yaml_string: Mock
    read_from_url: Mock
    sync_git_repo: Mock


@contextmanager
def patch_detached_repo_loader_deps(
    task_spec: Union[str, Dict[str, Any]], repo_path: Path = Path("/path/to/repo")
) -> Iterator[MockDetachedRepoLoaderDependencies]:
    loader = Mock(repo_path=repo_path, task_spec=task_spec)
    sync = Mock(return_value=repo_path)
    load_yaml_file = Mock(return_value=task_spec)
    load_yaml_string = Mock(return_value=task_spec)
    read_url = Mock(return_value=task_spec)
    with patch.object(loaders.io, "load_yaml_string", new=load_yaml_string):
        with patch.object(loaders.io, "load_yaml_file", new=load_yaml_file):
            with patch.object(loaders, "LocalRepoLoader", return_value=loader):
                with patch.object(loaders.git, "sync_git_repo_locally", new=sync):
                    with patch.object(loaders.http, "read_from_url", new=read_url):
                        yield MockDetachedRepoLoaderDependencies(
                            repo_path=repo_path,
                            local_loader=loader,
                            load_yaml_file=load_yaml_file,
                            load_yaml_string=load_yaml_string,
                            read_from_url=read_url,
                            sync_git_repo=sync,
                        )
