from click.testing import CliRunner

from qwikstart.cli import main
from qwikstart.parser import get_operations_mapping


def test_list_operations():
    runner = CliRunner()
    result = runner.invoke(main.list_operations)
    assert result.exit_code == 0

    for op_name in get_operations_mapping():
        assert op_name in result.output
