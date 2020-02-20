import re
from dataclasses import dataclass
from pathlib import Path

from ..base_context import BaseContext
from ..utils import ensure_path
from .base import BaseOperation

__all__ = ["Context", "Operation"]


@dataclass(frozen=True)
class Context(BaseContext):
    file_path: Path
    search: str
    replace: str
    use_regex: bool = False


class Operation(BaseOperation[Context, None]):
    """Operation for searching for text and replacing """

    name: str = "search_and_replace"

    def run(self, context: Context) -> None:
        file_path = ensure_path(context.file_path)

        with file_path.open() as f:
            content_before = f.read()

        replace = search_and_replace_rx if context.use_regex else search_and_replace
        content_after = replace(context.search, context.replace, content_before)

        with file_path.open("w") as f:
            f.write(content_after)


def search_and_replace(search_text: str, replace_text: str, content: str) -> str:
    return content.replace(search_text, replace_text)


def search_and_replace_rx(search_text: str, replace_text: str, content: str) -> str:
    return re.sub(search_text, replace_text, content)
