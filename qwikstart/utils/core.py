import textwrap
from pathlib import Path
from typing import Any, Iterable, TypeVar, Union, cast

T = TypeVar("T")


def ensure_path(path: Union[Path, str]) -> Path:
    """Return path object from `pathlib.Path` or string.

    While `Path` can be called on strings or `Path` and return a `Path`, it
    does not behave correctly for mock path instances. This helper function
    ensures we can support normal usage and mocked paths used for testing.
    """
    if hasattr(path, "open"):
        return cast(Path, path)
    return Path(path)


def first(iterable: Iterable[T]) -> T:
    return next(iter(iterable))


def full_class_name(obj: Any) -> str:
    return f"{obj.__class__.__module__}.{obj.__class__.__name__}"


def indent(text: str, space_count: int) -> str:
    """Return `text` indented by `space_count` spaces."""
    return textwrap.indent(text, " " * space_count)
