from contextlib import contextmanager
from dataclasses import dataclass
from unittest.mock import Mock, patch

import pytest  # type:ignore
from click.testing import CliRunner

from qwikstart import cli
from qwikstart.parser import get_operations_mapping


def test_list_operations():
    runner = CliRunner()
    result = runner.invoke(cli.list_operations)
    assert result.exit_code == 0

    for op_name in get_operations_mapping():
        assert op_name in result.output


class TestResolveTask:
    def test_resolved(self):
        data = {"name": "fake_task"}
        mock_resolver = create_mock_task_resolver(data)
        with patch_resolve_task_dependencies(mock_resolver) as mocks:
            cli.resolve_task("fake.yml")
        mocks.parse_task.assert_called_once_with(data, "fake.yml")

    def test_not_found(self):
        mock_resolver = create_mock_task_resolver(data={}, file_exists=False)
        with patch_resolve_task_dependencies(mock_resolver) as mocks:
            with pytest.raises(RuntimeError):
                cli.resolve_task("fake.yml")
        mocks.parse_task.assert_not_called()


@contextmanager
def patch_resolve_task_dependencies(mock_resolver):
    with patch_task_resolver(mock_resolver):
        with patch.object(cli, "parse_task") as mock_parse_task:
            yield MockResolveTaskDependencies(parse_task=mock_parse_task)


@dataclass
class MockResolveTaskDependencies:
    parse_task: Mock


@contextmanager
def patch_task_resolver(mock_resolver):
    with patch.object(cli, "task_resolver_list", new=[mock_resolver]):
        yield


def create_mock_task_resolver(data, file_exists=True):
    def mock_resolver_init(task_path):
        resolver = Mock(resolved_path=task_path)
        resolver.parsed_data.return_value = data
        resolver.exists.return_value = file_exists
        return resolver

    return mock_resolver_init
