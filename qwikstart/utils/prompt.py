from dataclasses import dataclass
from typing import Any, Optional

import click


@dataclass
class Prompt:
    name: str
    default_value: Optional[Any] = None


def read_user_variable(prompt):
    """Prompt user for variable and return the entered value or given default.

    Adapted from `cookiecutter.prompt`
    (see https://github.com/cookiecutter/cookiecutter).
    """
    # Please see https://click.palletsprojects.com/en/7.x/api/#click.prompt
    return click.prompt(
        click.style(prompt.name, fg="green"), default=prompt.default_value
    )
