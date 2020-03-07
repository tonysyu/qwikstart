import functools
import logging
import os
import re
import textwrap
from dataclasses import dataclass, field
from fnmatch import fnmatch
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional, cast

from ..base_context import BaseContext
from .base import BaseOperation

__all__ = ["Context", "Operation"]

logger = logging.getLogger(__name__)

CONTEXT_HELP = {
    "regex": "Regex to search for in files",
    "directory": "Root directory for search (defaults to working directory).",
    "output_name": "Variable name where list of matching files is stored.",
    "path_filter": textwrap.dedent(
        """
        File filter string passed to `fnmatch` before searching. This can be used
        to speed up searching for large repositories.

        For example, you can limit text search to json files using "*.json".
        """
    ),
}


@dataclass(frozen=True)
class Context(BaseContext):
    regex: str = ""
    directory: str = None
    output_name: str = "matching_files"
    path_filter: Optional[str] = None
    regex_flags: List[str] = field(default_factory=list)

    @classmethod
    def help(cls, field_name: str) -> Optional[str]:
        return CONTEXT_HELP.get(field_name)


class Operation(BaseOperation[Context, Dict[str, List[str]]]):
    """Operation for searching for text within files and returning file paths."""

    name: str = "find_files"

    def run(self, context: Context) -> Dict[str, List[str]]:
        regex_flags = create_regex_flags(context.regex_flags)
        regex = re.compile(context.regex, flags=regex_flags) if context.regex else None
        root_directory = context.directory or "."

        matching_files = []
        for filename in iter_path(root_directory, context.path_filter):
            if regex:
                try:
                    with open(filename) as f:
                        file_contents = f.read()
                except (IOError, UnicodeDecodeError):
                    logger.debug(f"Failed to read file {filename}")
                    continue

                if not regex.search(file_contents):
                    continue

            matching_files.append(filename)

        return {context.output_name: matching_files}


def iter_path(root_directory: str, path_filter_string: Optional[str]) -> Iterable[str]:
    path_filter = create_path_filter(path_filter_string)
    for root, dirs, files in os.walk(root_directory):
        for filename in files:
            filename = os.path.join(root, filename)
            if path_filter(filename):
                yield filename


def create_path_filter(path_filter_string: Optional[str]) -> Callable[[str], bool]:
    if not path_filter_string:

        def path_filter(path: str) -> bool:
            return True

    else:

        def path_filter(path: str) -> bool:
            return fnmatch(path, cast(str, path_filter_string))

    return path_filter


def create_regex_flags(flag_strings: List[str]) -> re.RegexFlag:
    default = re.RegexFlag(0)
    flags = (getattr(re, name, default) for name in flag_strings)
    # FIXME: This line complains about returning Any but still fails when casting.
    return functools.reduce(lambda x, y: x | y, flags, default)  # type: ignore
