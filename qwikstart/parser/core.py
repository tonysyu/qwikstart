from typing import Dict

from ..operations import BaseOperation

__all__ = ["ParserError", "get_operations_mapping"]


class ParserError(RuntimeError):
    pass


def get_operations_mapping() -> Dict[str, BaseOperation]:
    """Return mapping of known operation names to their respective"""
    return {op.name: op for op in BaseOperation.__subclasses__()}
