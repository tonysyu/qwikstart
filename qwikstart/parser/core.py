from typing import Dict, Type

from ..operations import BaseOperation, GenericOperation

OperationMapping = Dict[str, Type[GenericOperation]]


def get_operations_mapping() -> OperationMapping:
    """Return mapping of known operation names to their respective"""
    # FIXME: Ignore mypy error due to use of Type with abstract baseclass
    # See https://github.com/python/mypy/issues/4717
    return {
        op.name: op  # type:ignore
        for op in BaseOperation.__subclasses__()
        # FIXME: Each subclass of BaseOperation generates two subclasses:
        # The actual subclass AND the `BaseOperation[TContext, TOutput]` used
        # as superclass. Ignore operations without names to avoid these classes.
        if hasattr(op, "name")
    }
