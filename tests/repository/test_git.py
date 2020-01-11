from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterator, Optional
from unittest.mock import MagicMock, Mock, patch

import pytest

from qwikstart.config import get_user_config
from qwikstart.exceptions import RepoLoaderError
from qwikstart.repository import git

CACHE_DIR = get_user_config().qwikstart_cache
TEST_URL = "https://github.com/tonysyu/qwikstart"


class TestGitRepoLoader:
    def test_download_not_required(self) -> None:
        with patch_git_repo_loader_dependencies() as mocks:
            git.GitRepoLoader(TEST_URL)
        mocks.download_git_repo.assert_not_called()

    def test_download_required(self) -> None:
        with patch_git_repo_loader_dependencies(local_path_exists=False) as mocks:
            git.GitRepoLoader(TEST_URL)
        mocks.download_git_repo.assert_called_once_with(TEST_URL, mocks.local_path)

    def test_resolved_path(self) -> None:
        with patch_git_repo_loader_dependencies(local_path="/my/path/to/qwikstart.yml"):
            loader = git.GitRepoLoader(TEST_URL)
        assert loader.resolved_path == "/my/path/to/qwikstart.yml"

    def test_can_load(self) -> None:
        with patch_git_repo_loader_dependencies(can_load=False):
            loader = git.GitRepoLoader(TEST_URL)
        assert loader.can_load() is False

    def test_load_task_data(self) -> None:
        with patch_git_repo_loader_dependencies(data={"greeting": "Hello"}):
            loader = git.GitRepoLoader(TEST_URL)
        assert loader.load_task_data() == {"greeting": "Hello"}


class TestGetLocalRepoPath:
    def test_repo_only(self) -> None:
        local_path = git.get_local_repo_path("https://github.com/tonysyu/qwikstart")
        assert local_path == CACHE_DIR.joinpath("github.com/tonysyu/qwikstart")

    def test_non_url_raises_error(self) -> None:
        with pytest.raises(RepoLoaderError):
            git.get_local_repo_path("/this/is/not/a/url")


class TestDownloadGitRepo:
    @pytest.mark.integration  # type:ignore
    def test_non_url_raises_error(self) -> None:
        with pytest.raises(RepoLoaderError):
            git.download_git_repo("/this/is/not/a/url", CACHE_DIR.joinpath("new"))


@dataclass(frozen=True)
class MockGitRepoLoaderDependencies:
    local_path: Path
    local_loader: Mock
    download_git_repo: Mock


@contextmanager
def patch_git_repo_loader_dependencies(
    local_path: str = "/path/to/qwikstart.yml",
    local_path_exists: bool = True,
    can_load: bool = True,
    data: Optional[Dict[str, Any]] = None,
) -> Iterator[MockGitRepoLoaderDependencies]:
    mock_path = MagicMock(
        spec=Path,
        __str__=Mock(return_value=local_path),
        exists=Mock(return_value=local_path_exists),
    )

    mock_loader = Mock(
        resolved_path=local_path,
        can_load=Mock(return_value=can_load),
        load_task_data=Mock(return_value=data or {}),
    )
    with patch.object(git.local, "LocalRepoLoader", return_value=mock_loader):
        with patch.object(git, "get_local_repo_path", return_value=mock_path):
            with patch.object(git, "download_git_repo") as mock_download:
                yield MockGitRepoLoaderDependencies(
                    local_path=mock_path,
                    local_loader=mock_loader,
                    download_git_repo=mock_download,
                )
