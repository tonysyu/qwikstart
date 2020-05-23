from typing import Iterable

from .config import YamlLintConfig


class LintProblem:
    level: str

def run(input: str, conf: YamlLintConfig) -> Iterable[LintProblem]: ...
