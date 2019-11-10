import textwrap
from typing import Any, Dict

from typing_extensions import TypedDict

__all__ = ["first", "indent", "merge_typed_dicts", "remap_dict"]


def first(iterable):
    return next(iter(iterable))


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
