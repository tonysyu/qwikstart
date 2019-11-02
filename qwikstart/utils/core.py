from typing import Any, Dict


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
