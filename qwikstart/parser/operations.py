import collections
from typing import Any, Dict, List, NamedTuple, Optional, Union

from .. import utils
from ..operations import BaseOperation
from .core import ParserError, get_operations_mapping

__all__ = ["OPERATION_DEFINITION", "parse_operation"]


OPERATION_DEFINITION = Union[str, Dict[str, Dict[str, Any]]]


class OperationDefinition(NamedTuple):
    name: str
    config: Dict[str, Any]


def parse_operation(
    op_def: OPERATION_DEFINITION,
    known_operations: Optional[Dict[str, BaseOperation]] = None,
) -> OperationDefinition:
    if known_operations is None:
        known_operations = get_operations_mapping()

    op_def = normalize_op_definition(op_def)

    if op_def.name not in known_operations:
        raise ParserError(f"Could not find operation named '{op_def.name}'")

    operation_class = known_operations[op_def.name]
    return operation_class(**op_def.config)


def normalize_op_definition(
    op_def: OPERATION_DEFINITION,
    op_mapping: Optional[Dict[str, BaseOperation]] = None,
) -> OperationDefinition:
    if op_mapping is None:
        op_mapping = get_operations_mapping()

    if isinstance(op_def, str):
        return OperationDefinition(name=op_def, config={})
    elif isinstance(op_def, collections.abc.Mapping):
        if len(op_def) != 1:
            raise ParserError(
                "Operation definition with dict should only have a single key"
                f", but given {op_def}"
            )
        op_name = utils.first(op_def.keys())
        return OperationDefinition(name=op_name, config=op_def[op_name])
    elif isinstance(op_def, collections.abc.Sequence):
        if len(op_def) != 2:
            raise ParserError(
                "Operation definition with sequence should only have two items"
                f", but given {op_def}"
            )
        return OperationDefinition(*op_def)
    else:
        raise ParserError(f"Could not parse operation definition: {op_def}")
