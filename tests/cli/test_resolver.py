from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterator
from unittest.mock import Mock, patch

import pytest

from qwikstart.cli import resolver
from qwikstart.exceptions import UserFacingError


class TestResolveTask:
    def test_resolve_file(self) -> None:
        data = {"name": "fake_task"}
        mock_resolver = create_mock_repo_loader(data)
        with patch_resolve_task_dependencies(mock_resolver) as mocks:
            resolver.resolve_task("fake.yml")
        mocks.parse_task.assert_called_once_with(data, "fake.yml")

    def test_resolve_directory(self) -> None:
        data = {"name": "fake_task"}
        mock_resolver = create_mock_repo_loader(data)
        with patch_resolve_task_dependencies(mock_resolver) as mocks:
            resolver.resolve_task("fake.yml")
        mocks.parse_task.assert_called_once_with(data, "fake.yml")

    def test_not_found(self) -> None:
        mock_resolver = create_mock_repo_loader(data={}, can_load=False)
        with patch_resolve_task_dependencies(mock_resolver) as mocks:
            with pytest.raises(UserFacingError):
                resolver.resolve_task("fake.yml")
        mocks.parse_task.assert_not_called()


@dataclass
class MockResolveTaskDependencies:
    parse_task: Mock


@contextmanager
def patch_resolve_task_dependencies(
    mock_resolver: Mock
) -> Iterator[MockResolveTaskDependencies]:
    with patch_task_resolver(mock_resolver):
        with patch.object(resolver, "parse_task") as mock_parse_task:
            yield MockResolveTaskDependencies(parse_task=mock_parse_task)


@contextmanager
def patch_task_resolver(mock_resolver: Mock) -> Iterator[None]:
    with patch.object(resolver, "repo_loader_list", new=[mock_resolver]):
        yield


def create_mock_repo_loader(
    data: Dict[str, Any], can_load: bool = True
) -> Callable[[str], None]:
    def mock_repo_loader_init(task_path: str) -> Mock:
        loader = Mock(resolved_path=task_path)
        loader.load_task_data.return_value = data
        loader.can_load.return_value = can_load
        return loader

    return mock_repo_loader_init
