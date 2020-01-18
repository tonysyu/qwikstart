from typing import Any, Dict, Optional
from unittest.mock import Mock, patch

from termcolor import colored

from qwikstart.operations import echo

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

    def echo(
        self, message: str, template_variables: Optional[Dict[str, Any]] = None
    ) -> Mock:
        """Return mocked `print` function called by `echo.Operation`."""
        template_variables = template_variables or {}

        context = echo.Context(
            execution_context=helpers.get_execution_context(),
            message=message,
            template_variables=template_variables,
        )

        echo_op = echo.Operation()
        with patch.object(echo, "print") as mock_print:
            echo_op.run(context)
        return mock_print
