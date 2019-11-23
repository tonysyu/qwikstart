import textwrap
from pathlib import Path
from typing import Any, Dict, Union

from typing_extensions import TypedDict

__all__ = [
    "ensure_path",
    "first",
    "full_class_name",
    "indent",
    "merge_typed_dicts",
    "remap_dict",
]


def ensure_path(path: Union[Path, str]) -> Path:
    """Return path object from `pathlib.Path` or string.

    While `Path` can be called on strings or `Path` and return a `Path`, it
    does not behave correctly for mock path instances. This helper function
    ensures we can support normal usage and mocked paths used for testing.
    """
    if hasattr(path, "open"):
        return path
    return Path(path)


def first(iterable):
    return next(iter(iterable))


def full_class_name(obj):
    return f"{obj.__class__.__module__}.{obj.__class__.__name__}"


def remap_dict(
    original_dict: Dict[str, Any], key_mapping: Dict[str, str]
) -> Dict[str, Any]:
    """Return dict with any keys in `key_mapping` renamed.

    Args:
        original_dict: Dictionary with keys to be renamed.
        key_mapping: Dictionary mapping keys in `original_dict` to new keys.
            Any keys not in `key_mapping` are returned unchanged.
    """
    return {
        key_mapping.get(key, key): value
        for key, value in original_dict.items()
    }


def merge_typed_dicts(*typed_dicts, name: str = "MergedTypeDict"):
    """Return `TypedDict` containing all keys in one or more `typed_dicts`."""
    key_types: Dict[str, Any] = {}
    for tdict in typed_dicts:
        key_types.update(tdict.__annotations__)
    return TypedDict(name, key_types)  # type: ignore


def indent(text, space_count, predicate=None):
    """Return `text` indented by `space_count` spaces."""
    return textwrap.indent(text, " " * space_count)
