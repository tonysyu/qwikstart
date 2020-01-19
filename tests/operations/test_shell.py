from typing import Any, Dict
from unittest.mock import Mock, call, patch

from qwikstart.operations import shell

from .. import helpers


class TestShellOperation:
    @patch.object(shell, "logger")
    def test_string_command(self, mock_logger: Mock) -> None:
        self.shell({"cmd": "echo hello"})
        mock_logger.info.assert_has_calls(
            [call("Running command: echo hello"), call("hello\n")]
        )

    @patch.object(shell, "logger")
    def test_list_command(self, mock_logger: Mock) -> None:
        self.shell({"cmd": ["echo", "hello"]})
        mock_logger.info.assert_has_calls(
            [call("Running command: ['echo', 'hello']"), call("hello\n")]
        )

    @patch.object(shell, "logger")
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

    def shell(self, context_defs: Dict[str, Any]) -> None:
        context = shell.Context(
            execution_context=helpers.get_execution_context(), **context_defs
        )
        shell_op = shell.Operation()
        shell_op.run(context)
