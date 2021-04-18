from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Iterator
from unittest.mock import Mock, patch

import pytest

from qwikstart.cli import resolver
from qwikstart.exceptions import RepoLoaderError, UserFacingError

FAKE_PATH_STR = "/path/to/fake.yml"
FAKE_PATH = Path(FAKE_PATH_STR)


class TestResolveTask:
    def test_resolve_file(self) -> None:
        data = {"name": "fake_task"}
        mock_loader = create_mock_repo_loader(data)
        with patch_resolve_task_dependencies(mock_loader) as mock_parse_task:
            resolver.resolve_task(FAKE_PATH_STR)
        mock_parse_task.assert_called_once_with(
            data, execution_config={"source_dir": FAKE_PATH.parent}
        )

    def test_resolve_directory(self) -> None:
        data = {"name": "fake_task"}
        mock_loader = create_mock_repo_loader(data)
        with patch_resolve_task_dependencies(mock_loader) as mock_parse_task:
            resolver.resolve_task(FAKE_PATH_STR)
        mock_parse_task.assert_called_once_with(
            data, execution_config={"source_dir": FAKE_PATH.parent}
        )

    def test_loader_error(self) -> None:
        error = RepoLoaderError("fake error")
        with patch.object(resolver.repository, "get_repo_loader", side_effect=error):
            with pytest.raises(UserFacingError):
                resolver.resolve_task(FAKE_PATH_STR)


@contextmanager
def patch_resolve_task_dependencies(mock_loader: Mock) -> Iterator[Mock]:
    with patch.object(resolver.repository, "get_repo_loader", return_value=mock_loader):
        with patch.object(resolver, "parse_task") as mock_parse_task:
            yield mock_parse_task


def create_mock_repo_loader(
    data: Dict[str, Any], task_path: str = FAKE_PATH_STR
) -> Any:
    spec_path = Path(task_path)
    return Mock(spec_path=spec_path, repo_path=spec_path.parent, task_spec=data)
