import collections
from typing import Any, Dict, List, NamedTuple, Union

from .. import utils
from .core import ParserError

OPERATION_DEFINITION = Union[str, Dict[str, Dict[str, Any]]]


class OperationDefinition(NamedTuple):
    name: str
    config: Dict[str, Any]


def normalize_op_definition(
    op_def: OPERATION_DEFINITION
) -> OperationDefinition:
    if isinstance(op_def, str):
        return OperationDefinition(name=op_def, config={})
    elif isinstance(op_def, collections.Mapping):
        if len(op_def) != 1:
            raise ParserError(
                "Operation definition with dict should only have a single key"
                f", but given {op_def}"
            )
        op_name = utils.first(op_def.keys())
        return OperationDefinition(name=op_name, config=op_def[op_name])
    elif isinstance(op_def, collections.Sequence):
        if len(op_def) != 2:
            raise ParserError(
                "Operation definition with sequence should only have two items"
                f", but given {op_def}"
            )
        return OperationDefinition(*op_def)
    else:
        raise ParserError(f"Could not parse operation definition: {op_def}")
