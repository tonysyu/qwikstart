from unittest.mock import patch

from click.testing import CliRunner

from qwikstart.cli import main
from qwikstart.operations import add_file
from qwikstart.parser import get_operations_mapping


def test_run() -> None:
    runner = CliRunner()
    with patch.object(main, "resolve_task") as mock_resolve_task:
        result = runner.invoke(main.run, "fake/path")
    assert result.exit_code == 0
    mock_resolve_task.assert_called_once_with("fake/path", git_url=None)


def test_list_operations() -> None:
    runner = CliRunner()
    result = runner.invoke(main.list_operations)
    assert result.exit_code == 0

    for op_name in get_operations_mapping():
        assert op_name in result.output


def test_help() -> None:
    runner = CliRunner()
    result = runner.invoke(main.help, [add_file.Operation.name])
    assert result.exit_code == 0
