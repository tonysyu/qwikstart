from typing import Any, Dict
from unittest.mock import Mock, call, patch

from qwikstart.operations import shell

from .. import helpers


@patch.object(shell, "logger")
class TestShellOperation:
    def test_string_command(self, mock_logger: Mock) -> None:
        self.shell({"cmd": "echo hello"})
        mock_logger.info.assert_has_calls(
            [call("Running command: echo hello"), call("hello\n")]
        )

    def test_output_not_logged_with_echo_off(self, mock_logger: Mock) -> None:
        self.shell({"cmd": "echo hello", "echo_output": False})
        mock_logger.info.assert_called_once_with("Running command: echo hello")

    def test_output_saved_to_variable(self, mock_logger: Mock) -> None:
        output = self.shell({"cmd": "echo hello", "output_var": "greeting"})
        assert output == {"greeting": "hello\n"}

    def test_list_command(self, mock_logger: Mock) -> None:
        self.shell({"cmd": ["echo", "hello"]})
        mock_logger.info.assert_has_calls(
            [call("Running command: ['echo', 'hello']"), call("hello\n")]
        )

    def test_render_template(self, mock_logger: Mock) -> None:
        self.shell(
            {
                "cmd": "echo {{ qwikstart.greeting }}",
                "template_variables": {"greeting": "Howdy"},
            }
        )
        mock_logger.info.assert_has_calls(
            [call("Running command: echo Howdy"), call("Howdy\n")]
        )

    def shell(self, context_defs: Dict[str, Any]) -> Dict[str, Any]:
        context = shell.Context(
            execution_context=helpers.get_execution_context(), **context_defs
        )
        shell_op = shell.Operation()
        return shell_op.run(context)
