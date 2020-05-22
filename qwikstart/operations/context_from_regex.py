import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from ..base_context import BaseContext
from ..exceptions import OperationError
from ..utils import clean_multiline, create_regex_flags, ensure_path, io
from .base import BaseOperation
from .utils import FILE_PATH_HELP, REGEX_FLAGS_HELP

__all__ = ["Context", "Operation"]

logger = logging.getLogger(__name__)

CONTEXT_HELP = {
    "file_path": FILE_PATH_HELP,
    "regex": clean_multiline(
        """
        Regex to search for in `file_path`. Note that this is expected to contain named
        capture groups. Names of capture groups define new context variable names.

        See https://docs.python.org/3/howto/regex.html#non-capturing-and-named-groups
        """
    ),
    "regex_flags": REGEX_FLAGS_HELP,
}


@dataclass(frozen=True)
class Context(BaseContext):
    regex: str
    file_path: Path
    regex_flags: List[str] = field(default_factory=lambda: ["MULTILINE"])

    @classmethod
    def help(cls, field_name: str) -> Optional[str]:
        return CONTEXT_HELP.get(field_name)


class Operation(BaseOperation[Context, Dict[str, str]]):
    """Operation to extract context data from a file using a regex.

    See https://qwikstart.readthedocs.io/en/latest/operations/context_from_regex.html
    """

    name: str = "context_from_regex"

    def run(self, context: Context) -> Dict[str, str]:
        regex_flags = create_regex_flags(context.regex_flags)
        regex = re.compile(context.regex, flags=regex_flags)
        expected_groups = set(regex.groupindex)
        if len(expected_groups) == 0:
            raise OperationError(
                f"At least one named capture group required in regex: {regex}"
            )

        text = io.read_file_contents(ensure_path(context.file_path))
        data = {}
        for match in regex.finditer(text):
            data.update(
                {
                    key: value
                    for key, value in match.groupdict().items()
                    if value is not None
                }
            )

        if data.keys() != expected_groups:
            missing_groups = ", ".join(expected_groups.difference(data))
            raise OperationError(
                f"Unable to find {missing_groups} using {regex} on {context.file_path}"
            )

        return data
