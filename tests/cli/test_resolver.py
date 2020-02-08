from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict
from unittest.mock import Mock, patch

import pytest

from qwikstart.cli import resolver
from qwikstart.exceptions import RepoLoaderError, UserFacingError
from qwikstart.repository import LocalRepoLoader

FAKE_PATH_STR = "/path/to/fake.yml"
FAKE_PATH = Path(FAKE_PATH_STR)


class TestResolveTask:
    def test_resolve_file(self) -> None:
        data = {"name": "fake_task"}
        mock_loader = create_mock_repo_loader(data)
        with patch_resolve_task_dependencies(mock_loader) as mock_parse_task:
            resolver.resolve_task(FAKE_PATH_STR)
        mock_parse_task.assert_called_once_with(data, FAKE_PATH)

    def test_resolve_directory(self) -> None:
        data = {"name": "fake_task"}
        mock_loader = create_mock_repo_loader(data)
        with patch_resolve_task_dependencies(mock_loader) as mock_parse_task:
            resolver.resolve_task(FAKE_PATH_STR)
        mock_parse_task.assert_called_once_with(data, FAKE_PATH)

    def test_not_found(self) -> None:
        mock_loader = create_mock_repo_loader(data={}, can_load=False)
        with patch_resolve_task_dependencies(mock_loader) as mock_parse_task:
            with pytest.raises(UserFacingError):
                resolver.resolve_task(FAKE_PATH_STR)
        mock_parse_task.assert_not_called()

    def test_loader_error(self) -> None:
        error = RepoLoaderError("fake error")
        with patch.object(resolver, "get_repo_loader", side_effect=error):
            with pytest.raises(UserFacingError):
                resolver.resolve_task(FAKE_PATH_STR)


class TestGetRepoLoader:
    def test_local_loader(self) -> None:
        loader = resolver.get_repo_loader(FAKE_PATH_STR)
        assert isinstance(loader, LocalRepoLoader)

    def test_git_loader(self) -> None:
        repo_url = "http://example.com"
        with patch.object(resolver, "GitRepoLoader") as loader_class:
            loader = resolver.get_repo_loader(FAKE_PATH_STR, repo_url=repo_url)
        assert loader is loader_class.return_value
        loader_class.assert_called_once_with(repo_url, FAKE_PATH_STR)


@contextmanager
def patch_resolve_task_dependencies(mock_loader: Mock) -> Mock:
    with patch.object(resolver, "get_repo_loader", return_value=mock_loader):
        with patch.object(resolver, "parse_task") as mock_parse_task:
            yield mock_parse_task


def create_mock_repo_loader(
    data: Dict[str, Any], can_load: bool = True, task_path: str = FAKE_PATH_STR
) -> Any:
    return Mock(
        resolved_path=Path(task_path),
        load_raw_task_spec=Mock(return_value=data),
        can_load=Mock(return_value=can_load),
    )
