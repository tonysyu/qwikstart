import os
from dataclasses import dataclass
from typing import Any, List, Optional

import click
import click.types

from qwikstart.exceptions import UserFacingError


@dataclass
class Prompt:
    name: str
    default_value: Optional[Any] = None
    choices: Optional[List[Any]] = None


def create_prompt(**prompt_kwargs: Any) -> Prompt:
    """Return Prompt instance from attributes in dictionary.

    This raises a UserFacingError if the Prompt is incorrectly defined.
    """
    try:
        return Prompt(**prompt_kwargs)
    except TypeError as error:
        name = prompt_kwargs.get("name", None)
        if not name:
            msg = f"Prompt definition has no 'name': {prompt_kwargs}"
            raise UserFacingError(msg) from error

        # FIXME: Ignore mypy error when accessing __dataclass_fields__.
        # See https://github.com/python/mypy/issues/6568
        known_keys = Prompt.__dataclass_fields__.keys()  # type:ignore
        unknown_keys = set(prompt_kwargs.keys()).difference(known_keys)
        if unknown_keys:
            msg = f"Prompt definition for {name!r} has unknown keys: {unknown_keys}"
            raise UserFacingError(msg) from error
        raise


def read_user_variable(prompt: Prompt) -> Any:
    """Prompt user for variable and return the entered value or given default.

    Adapted from `cookiecutter.prompt`
    (see https://github.com/cookiecutter/cookiecutter).

    For more info, see https://click.palletsprojects.com/en/7.x/api/#click.prompt
    """
    if prompt.choices:
        return read_user_choice(prompt)
    return click.prompt(default_style(prompt.name), default=prompt.default_value)


def read_user_choice(prompt: Prompt) -> Any:
    """Prompt user to choose from several options for the given variable.

    The first item will be returned if no input provided.

    Adapted from `cookiecutter.prompt`
    (see https://github.com/cookiecutter/cookiecutter).
    """
    choices = prompt.choices
    if not isinstance(choices, list):
        msg = f"Choices for prompt must be list but given {type(choices)}: {choices!r}"
        raise UserFacingError(msg)

    if not choices:
        raise UserFacingError("Choices for prompt cannot be empty")

    choice_map = {"{}".format(i): value for i, value in enumerate(choices, 1)}
    numeric_choices = choice_map.keys()
    default = "1"

    choice_lines = ["{} - {}".format(*c) for c in choice_map.items()]
    display = os.linesep.join(
        (
            "Select {}:".format(prompt.name),
            os.linesep.join(choice_lines),
            "Choose from {}".format(", ".join(numeric_choices)),
        )
    )

    user_choice = click.prompt(
        display, type=click.Choice(numeric_choices), default=default, show_choices=False
    )
    return choice_map[user_choice]


def default_style(message: str) -> str:
    return click.style(message, fg="green")
