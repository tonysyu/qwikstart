import logging
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

from ..base_context import BaseContext
from .base import BaseOperation

__all__ = ["Context", "Operation"]

logger = logging.getLogger(__name__)

CONTEXT_HELP = {
    "regex": "Regex to search for in files",
    "directory": "Root directory for search (defaults to working directory).",
    "output_name": "Variable name where list of matching files is stored.",
}


@dataclass(frozen=True)
class Context(BaseContext):
    regex: str
    directory: Optional[Path] = None
    output_name: str = "matching_files"

    @classmethod
    def help(cls, field_name: str) -> Optional[str]:
        return CONTEXT_HELP.get(field_name)


class Operation(BaseOperation[Context, Dict[str, List[str]]]):
    """Operation for searching for text within files and returning file paths."""

    name: str = "find_files"

    def run(self, context: Context) -> Dict[str, List[str]]:
        regex = re.compile(context.regex)
        root_directory = context.directory or "."
        matching_files = []
        for root, dirs, files in os.walk(root_directory):
            for filename in files:
                filename = os.path.join(root, filename)
                try:
                    with open(filename) as f:
                        file_contents = f.read()
                except IOError:
                    logger.debug(f"Failed to read file {filename}")
                    continue

                if regex.search(file_contents):
                    matching_files.append(filename)

        return {context.output_name: matching_files}
