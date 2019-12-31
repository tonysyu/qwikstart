from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterator
from unittest.mock import Mock, patch

import pytest

from qwikstart.cli import resolver


class TestResolveTask:
    def test_resolved(self) -> None:
        data = {"name": "fake_task"}
        mock_resolver = create_mock_task_resolver(data)
        with patch_resolve_task_dependencies(mock_resolver) as mocks:
            resolver.resolve_task("fake.yml")
        mocks.parse_task.assert_called_once_with(data, "fake.yml")

    def test_not_found(self) -> None:
        mock_resolver = create_mock_task_resolver(data={}, file_exists=False)
        with patch_resolve_task_dependencies(mock_resolver) as mocks:
            with pytest.raises(RuntimeError):
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
    with patch.object(resolver, "task_resolver_list", new=[mock_resolver]):
        yield


def create_mock_task_resolver(
    data: Dict[str, Any], file_exists: bool = True
) -> Callable[[str], None]:
    def mock_resolver_init(task_path: str) -> Mock:
        resolver = Mock(resolved_path=task_path)
        resolver.parsed_data.return_value = data
        resolver.exists.return_value = file_exists
        return resolver

    return mock_resolver_init
