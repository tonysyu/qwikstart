from typing import Any, Dict, Optional
from unittest.mock import Mock, patch

from pygments.formatters import TerminalFormatter
from pygments.lexers import PythonLexer
from termcolor import colored

from qwikstart.operations import OperationConfig, echo

from .. import helpers


class TestEchoOperation:
    def test_string(self) -> None:
        mock_print = self.echo("Hello")
        mock_print.assert_called_once_with("Hello")

    def test_template_string(self) -> None:
        mock_print = self.echo(
            "Hello, {{ qwikstart.name }}!", template_variables={"name": "World"}
        )
        mock_print.assert_called_once_with("Hello, World!")

    def test_template_string_with_colored_filter(self) -> None:
        mock_print = self.echo("{{ 'Hello' | colored('green') }}")
        mock_print.assert_called_once_with(colored("Hello", color="green"))

    @patch.object(echo, "highlight")
    def test_highlight_python(self, mock_highlight: Mock) -> None:
        input_code = "print('hi'))"
        mock_print = self.echo(input_code, highlight="python")
        mock_print.assert_called_once_with(mock_highlight.return_value)
        code, lexer, formatter = mock_highlight.call_args[0]
        assert code == input_code
        assert isinstance(lexer, PythonLexer)
        assert isinstance(formatter, TerminalFormatter)

    @patch.object(echo, "logger")
    @patch.object(echo, "highlight")
    def test_highlight_with_unknown_language(
        self, mock_highlight: Mock, mock_logger: Mock
    ) -> None:
        code = "print('hi'))"
        mock_print = self.echo(code, highlight="unknown-language")
        mock_print.assert_called_once_with(code)
        mock_highlight.assert_not_called()
        mock_logger.warning.assert_called_once_with(
            "No highlighter found for 'unknown-language'"
        )

    def test_description_not_displayed_by_default(self) -> None:
        echo_op = echo.Operation()
        assert echo_op.config.display_step_description is False

    def test_configure_display_step_description(self) -> None:
        config = OperationConfig(display_step_description=True)
        echo_op = echo.Operation(config=config)
        assert echo_op.config.display_step_description is True

    def echo(
        self,
        message: str,
        highlight: str = "",
        template_variables: Optional[Dict[str, Any]] = None,
    ) -> Mock:
        """Return mocked `print` function called by `echo.Operation`."""
        template_variables = template_variables or {}

        context = echo.Context(
            execution_context=helpers.get_execution_context(),
            message=message,
            highlight=highlight,
            template_variables=template_variables,
        )

        echo_op = echo.Operation()
        with patch.object(echo, "print") as mock_print:
            echo_op.run(context)
        return mock_print
