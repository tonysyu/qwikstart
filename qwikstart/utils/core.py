import textwrap
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, TypeVar, Union, cast

__all__ = ["ensure_path", "first", "full_class_name", "indent", "remap_dict"]

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


def remap_dict(
    original_dict: Mapping[str, Any], key_mapping: Mapping[str, str]
) -> Dict[str, Any]:
    """Return dict with any keys in `key_mapping` renamed.

    Args:
        original_dict: Dictionary with keys to be renamed.
        key_mapping: Dictionary mapping keys in `original_dict` to new keys.
            Any keys not in `key_mapping` are returned unchanged.
    """
    return {key_mapping.get(key, key): value for key, value in original_dict.items()}


def indent(text: str, space_count: int) -> str:
    """Return `text` indented by `space_count` spaces."""
    return textwrap.indent(text, " " * space_count)
