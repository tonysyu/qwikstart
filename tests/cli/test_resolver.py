from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterator
from unittest.mock import Mock, patch

import pytest
from pyfakefs.fake_filesystem_unittest import TestCase

from qwikstart.cli import resolver
from qwikstart.exceptions import TaskLoaderError


class TestLocalPathResolver(TestCase):
    def setUp(self) -> None:
        self.setUpPyfakefs()

    def test_resolve_file(self) -> None:
        self.fs.create_file("/path/to/file.yml", contents='{"a": 1}')
        res = resolver.LocalPathResolver("/path/to/file.yml")
        assert res.exists()
        assert res.parsed_data() == {"a": 1}

    def test_resolve_directory(self) -> None:
        self.fs.create_file("/path/containing/qwikstart.yml", contents='{"a": 1}')
        res = resolver.LocalPathResolver("/path/containing/")
        assert res.exists()
        assert res.parsed_data() == {"a": 1}

    def test_unknown_file_type(self) -> None:
        self.fs.create_file("/path/to/file.txt", contents='{"a": 1}')
        res = resolver.LocalPathResolver("/path/to/file.txt")
        assert res.exists()
        with pytest.raises(TaskLoaderError):
            res.parsed_data()


class TestResolveTask:
    def test_resolve_file(self) -> None:
        data = {"name": "fake_task"}
        mock_resolver = create_mock_task_resolver(data)
        with patch_resolve_task_dependencies(mock_resolver) as mocks:
            resolver.resolve_task("fake.yml")
        mocks.parse_task.assert_called_once_with(data, "fake.yml")

    def test_resolve_directory(self) -> None:
        data = {"name": "fake_task"}
        mock_resolver = create_mock_task_resolver(data)
        with patch_resolve_task_dependencies(mock_resolver) as mocks:
            resolver.resolve_task("fake.yml")
        mocks.parse_task.assert_called_once_with(data, "fake.yml")

    def test_not_found(self) -> None:
        mock_resolver = create_mock_task_resolver(data={}, file_exists=False)
        with patch_resolve_task_dependencies(mock_resolver) as mocks:
            with pytest.raises(TaskLoaderError):
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
