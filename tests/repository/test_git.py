from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterator, Optional
from unittest.mock import MagicMock, Mock, patch

import pytest

from qwikstart.config import get_user_config
from qwikstart.exceptions import RepoLoaderError
from qwikstart.repository import git

CACHE_DIR = get_user_config().qwikstart_cache_path
TEST_URL = "https://github.com/user/repo"


class TestGitRepoLoader:
    def test_download_not_required(self) -> None:
        with patch_git_repo_loader_dependencies() as mocks:
            git.GitRepoLoader(TEST_URL)
        mocks.download_git_repo.assert_not_called()
        mocks.update_git_repo.assert_called_once_with(mocks.local_path)

    def test_download_required(self) -> None:
        with patch_git_repo_loader_dependencies(local_path_exists=False) as mocks:
            git.GitRepoLoader(TEST_URL)
        mocks.download_git_repo.assert_called_once_with(TEST_URL, mocks.local_path)
        mocks.update_git_repo.assert_not_called()

    def test_spec_path(self) -> None:
        with patch_git_repo_loader_dependencies(local_path="/my/path/to/qwikstart.yml"):
            loader = git.GitRepoLoader(TEST_URL)
        assert loader.spec_path == "/my/path/to/qwikstart.yml"

    def test_can_load_spec(self) -> None:
        with patch_git_repo_loader_dependencies(can_load_spec=False):
            loader = git.GitRepoLoader(TEST_URL)
        assert loader.can_load_spec() is False

    def test_load_raw_task_spec(self) -> None:
        with patch_git_repo_loader_dependencies(data={"greeting": "Hello"}):
            loader = git.GitRepoLoader(TEST_URL)
        assert loader.load_raw_task_spec() == {"greeting": "Hello"}


class TestResolveGitUrl:
    def test_echo_full_url(self) -> None:
        url = "https://github.com/user/repo"
        assert git.resolve_git_url(url) == url

    def test_github_abbreviation_resolved(self) -> None:
        assert git.resolve_git_url("gh:user/repo") == "https://github.com/user/repo"

    def test_gitlab_abbreviation_resolved(self) -> None:
        assert git.resolve_git_url("gl:user/repo") == "https://gitlab.com/user/repo"

    def test_bitbucket_abbreviation_resolved(self) -> None:
        assert git.resolve_git_url("bb:user/repo") == "https://bitbucket.org/user/repo"


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


class TestUpdateGitRepo:
    @patch.object(git._git, "Repo")
    def test_repo_initialized_with_string(self, repo_class: Mock) -> None:
        git.update_git_repo(Path("/path/to/local/repo"))
        repo_class.assert_called_once_with("/path/to/local/repo")


@dataclass(frozen=True)
class MockGitRepoLoaderDependencies:
    local_path: Path
    local_loader: Mock
    download_git_repo: Mock
    update_git_repo: Mock


@contextmanager
def patch_git_repo_loader_dependencies(
    local_path: str = "/path/to/qwikstart.yml",
    local_path_exists: bool = True,
    can_load_spec: bool = True,
    data: Optional[Dict[str, Any]] = None,
) -> Iterator[MockGitRepoLoaderDependencies]:
    mock_path = MagicMock(
        spec=Path,
        __str__=Mock(return_value=local_path),
        exists=Mock(return_value=local_path_exists),
    )

    mock_loader = Mock(
        spec_path=local_path,
        can_load_spec=Mock(return_value=can_load_spec),
        load_raw_task_spec=Mock(return_value=data or {}),
    )
    with patch.object(git.local, "LocalRepoLoader", return_value=mock_loader):
        with patch.object(git, "get_local_repo_path", return_value=mock_path):
            with patch.object(git, "download_git_repo") as mock_download:
                with patch.object(git, "update_git_repo") as mock_update_repo:
                    yield MockGitRepoLoaderDependencies(
                        local_path=mock_path,
                        local_loader=mock_loader,
                        download_git_repo=mock_download,
                        update_git_repo=mock_update_repo,
                    )
