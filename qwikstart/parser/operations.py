import collections
from typing import Any, Dict, NamedTuple, Optional, Tuple, Type, Union

from .. import utils
from ..exceptions import TaskParserError
from ..operations import GenericOperation
from .core import OperationMapping, get_operations_mapping

__all__ = ["OperationDefinition", "parse_operation"]


UnparsedOperation = Union[str, Dict[str, Dict[str, Any]], Tuple[str, Dict[str, Any]]]


class OperationDefinition(NamedTuple):
    name: str
    config: Dict[str, Any]


def parse_operation(
    op_def: UnparsedOperation,
    known_operations: Optional[Dict[str, Type[GenericOperation]]] = None,
) -> GenericOperation:
    if known_operations is None:
        known_operations = get_operations_mapping()

    op_def = normalize_op_definition(op_def)

    if op_def.name not in known_operations:
        raise TaskParserError(f"Could not find operation named '{op_def.name}'")

    operation_class = known_operations[op_def.name]
    return operation_class(**op_def.config)


def normalize_op_definition(
    op_def: UnparsedOperation, op_mapping: Optional[OperationMapping] = None
) -> OperationDefinition:
    if op_mapping is None:
        op_mapping = get_operations_mapping()

    if isinstance(op_def, str):
        return OperationDefinition(name=op_def, config={})
    elif isinstance(op_def, collections.abc.Mapping):
        if len(op_def) != 1:
            raise TaskParserError(
                "Operation definition with dict should only have a single key"
                f", but given {op_def}"
            )
        op_name = utils.first(op_def.keys())
        return OperationDefinition(name=op_name, config=op_def[op_name])
    elif isinstance(op_def, collections.abc.Sequence):
        if len(op_def) != 2:
            raise TaskParserError(
                "Operation definition with sequence should only have two items"
                f", but given {op_def}"
            )
        return OperationDefinition(*op_def)
    else:
        raise TaskParserError(f"Could not parse operation definition: {op_def}")
