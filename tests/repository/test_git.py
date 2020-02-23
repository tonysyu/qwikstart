from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterator, Optional
from unittest.mock import MagicMock, Mock, patch

import pytest

from qwikstart.config import get_user_config
from qwikstart.exceptions import RepoLoaderError
from qwikstart.repository import git

CACHE_DIR = get_user_config().repo_cache_path
TEST_URL = "https://github.com/user/repo"


class TestParseGitUrl:
    def test_https_url(self) -> None:
        git_url = self.parse_git_url("https://github.com/tonysyu/qwikstart")
        assert git_url.prefix == "https"
        assert git_url.separator == "://"
        assert git_url.path == "github.com/tonysyu/qwikstart"

    def test_git_ssh(self) -> None:
        git_url = self.parse_git_url("git@github.com:tonysyu/qwikstart.git")
        assert git_url.prefix == "git"
        assert git_url.separator == "@"
        assert git_url.path == "github.com/tonysyu/qwikstart.git"

    def parse_git_url(self, url: str) -> git.GitUrl:
        # Ensure that we get a non-None value to avoid mypy errors about non-checking.
        git_url = git.parse_git_url(url)
        assert git_url is not None
        return git_url


class TestGitRepoLoader:
    def test_task_spec(self) -> None:
        with patch_git_repo_loader_dependencies(data={"greeting": "Hello"}):
            loader = git.GitRepoLoader(TEST_URL)
        assert loader.task_spec == {"greeting": "Hello"}

    def test_repo_path(self) -> None:
        with patch_git_repo_loader_dependencies() as mocks:
            loader = git.GitRepoLoader(TEST_URL)
        assert loader.repo_path == mocks.repo_path


class TestSyncGitRepoLocally:
    def test_download_not_required(self) -> None:
        with patch_sync_git_repo_dependencies() as mocks:
            git.sync_git_repo_locally(TEST_URL)
        mocks.download_git_repo.assert_not_called()
        mocks.update_git_repo.assert_called_once_with(mocks.local_path)

    def test_download_required(self) -> None:
        with patch_sync_git_repo_dependencies(local_path_exists=False) as mocks:
            git.sync_git_repo_locally(TEST_URL)
        mocks.download_git_repo.assert_called_once_with(TEST_URL, mocks.local_path)
        mocks.update_git_repo.assert_not_called()


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

    @patch.object(git.gitlib, "Repo")
    def test_success(self, repo_class: Mock) -> None:
        output_dir = CACHE_DIR.joinpath("new")
        git.download_git_repo("/fake/repo", output_dir)
        repo_class.clone_from("/fake/repo", str(output_dir))


class TestUpdateGitRepo:
    @patch.object(git.gitlib, "Repo")
    def test_repo_initialized_with_string(self, repo_class: Mock) -> None:
        git.update_git_repo(Path("/path/to/local/repo"))
        repo_class.assert_called_once_with("/path/to/local/repo")


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
    with patch.object(git.local, "LocalRepoLoader", return_value=mock_loader):
        with patch.object(git, "sync_git_repo_locally", new=mock_sync):
            yield MockGitRepoLoaderDependencies(
                repo_path=repo_path, local_loader=mock_loader, sync_git_repo=mock_sync
            )


@dataclass(frozen=True)
class MockSyncGitRepoDepdendencies:
    local_path: Path
    download_git_repo: Mock
    update_git_repo: Mock


@contextmanager
def patch_sync_git_repo_dependencies(
    local_path: str = "/path/to/qwikstart.yml",
    local_path_exists: bool = True,
    data: Optional[Dict[str, Any]] = None,
) -> Iterator[MockSyncGitRepoDepdendencies]:
    mock_path = MagicMock(
        spec=Path,
        __str__=Mock(return_value=local_path),
        exists=Mock(return_value=local_path_exists),
    )

    with patch.object(git, "get_local_repo_path", return_value=mock_path):
        with patch.object(git, "download_git_repo") as mock_download:
            with patch.object(git, "update_git_repo") as mock_update_repo:
                yield MockSyncGitRepoDepdendencies(
                    local_path=mock_path,
                    download_git_repo=mock_download,
                    update_git_repo=mock_update_repo,
                )
