from dataclasses import dataclass
from typing import Any, Optional

import click
import click.types

from qwikstart.exceptions import UserFacingError


@dataclass
class Prompt:
    name: str
    default_value: Optional[Any] = None


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
    """
    # Please see https://click.palletsprojects.com/en/7.x/api/#click.prompt
    return click.prompt(
        click.style(prompt.name, fg="green"), default=prompt.default_value
    )
