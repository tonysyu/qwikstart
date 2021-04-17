"""
Thin wrapper around `yamllint` library to provide helpful error info for yaml files.
"""
import logging
import textwrap
from typing import List

from yamllint import cli, linter
from yamllint.config import YamlLintConfig

from ..exceptions import TaskParserError

logger = logging.getLogger(__name__)

# Use very relaxed linting configuration, since we only want real errors reported:
YAMLLINT_CONFIG = YamlLintConfig(
    content=textwrap.dedent(
        """
        extends: relaxed
        rules:
            new-line-at-end-of-file: disable
        """
    )
)


def linter_errors(text: str) -> List[linter.LintProblem]:
    problems = linter.run(text, YAMLLINT_CONFIG)
    return [p for p in problems if p.level == "error"]


def assert_no_errors(text: str, display_warnings: bool = True) -> None:
    problems = linter_errors(text)
    if not problems:
        return
    logger.warning("Detected issues with in yaml file")
    cli.show_problems(problems, "stdin", args_format="colored", no_warn=False)
    raise TaskParserError("Failed to read yaml file")
