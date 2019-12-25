from click.testing import CliRunner

from qwikstart.cli import main
from qwikstart.operations import add_file
from qwikstart.parser import get_operations_mapping


def test_list_operations():
    runner = CliRunner()
    result = runner.invoke(main.list_operations)
    assert result.exit_code == 0

    for op_name in get_operations_mapping():
        assert op_name in result.output


def test_help():
    runner = CliRunner()
    result = runner.invoke(main.help, [add_file.Operation.name])
    assert result.exit_code == 0
