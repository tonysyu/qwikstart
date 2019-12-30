from typing import Dict, Type

from ..operations import BaseOperation

__all__ = ["OperationMapping", "ParserError", "get_operations_mapping"]


class ParserError(RuntimeError):
    pass


OperationMapping = Dict[str, Type[BaseOperation]]


def get_operations_mapping() -> OperationMapping:
    """Return mapping of known operation names to their respective"""
    # FIXME: Ignore mypy error due to use of Type with abstract baseclass
    # See https://github.com/python/mypy/issues/4717
    return {op.name: op for op in BaseOperation.__subclasses__()}  # type:ignore
