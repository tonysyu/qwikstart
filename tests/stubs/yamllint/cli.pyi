from typing import Iterable

from .linter import LintProblem

def show_problems(
    problems: Iterable[LintProblem], file: str, args_format: str, no_warn: bool
) -> None: ...
