import collections
from typing import Any, Dict, NamedTuple, Optional, Type, cast

from .. import utils
from ..exceptions import TaskParserError
from ..operations import BaseOperation, GenericOperation
from ..repository import OperationSpec

__all__ = ["OperationDefinition", "parse_operation"]

OperationMapping = Dict[str, Type[GenericOperation]]
RESERVED_WORDS_OPERATION_CONFIG = {
    "local_context",
    "input_mapping",
    "output_mapping",
    "description",
}


def get_operations_mapping() -> OperationMapping:
    """Return mapping of known operation names to their respective operation classes."""
    # FIXME: Each subclass of BaseOperation generates two subclasses: The actual
    # subclass AND the `BaseOperation[TContext, TOutput]` used as superclass. Ignore
    # operations without names to avoid these classes.
    operations = [op for op in BaseOperation.__subclasses__() if hasattr(op, "name")]
    op_mapping = {op.name: op for op in operations}

    # Add any operations that have aliases to our mapping:
    for op in operations:
        if op.aliases:
            for name in op.aliases:
                op_mapping.setdefault(name, op)

    # FIXME: Cast to avoid mypy error due to use of Type with abstract baseclass
    # See https://github.com/python/mypy/issues/4717
    return cast(OperationMapping, op_mapping)


class OperationDefinition(NamedTuple):
    name: str
    config: Dict[str, Any]

    @property
    def parsed_config(self) -> Dict[str, Any]:
        """Return operation configuration parsed from raw config input.

        Any configuration that is not a reserved word will be added to the
        `local_context` passed to the operation initializer.
        """
        local_context = self.config.get("local_context", {})
        input_mapping = self.config.get("input_mapping")
        output_mapping = self.config.get("output_mapping")
        description = self.config.get("description", "")
        local_context.update(
            {
                key: value
                for key, value in self.config.items()
                if key not in RESERVED_WORDS_OPERATION_CONFIG
            }
        )
        return {
            "local_context": local_context,
            "input_mapping": input_mapping,
            "output_mapping": output_mapping,
            "description": description,
        }


def parse_operation_from_step(
    op_spec: Dict[str, Any],
    known_operations: Optional[Dict[str, Type[GenericOperation]]] = None,
) -> GenericOperation:
    if known_operations is None:
        known_operations = get_operations_mapping()

    op_name = op_spec.pop("name", None)
    if not op_name:
        raise TaskParserError(f"Operation definition has no name: {op_spec}")
    elif op_name not in known_operations:
        raise TaskParserError(f"Could not find operation named '{op_name}'")

    op_def = OperationDefinition(name=op_name, config=op_spec)
    operation_class = known_operations[op_name]
    return operation_class(**op_def.parsed_config)


def parse_operation(
    op_spec: OperationSpec,
    known_operations: Optional[Dict[str, Type[GenericOperation]]] = None,
) -> GenericOperation:
    if known_operations is None:
        known_operations = get_operations_mapping()

    op_spec = normalize_op_definition(op_spec)

    if op_spec.name not in known_operations:
        raise TaskParserError(f"Could not find operation named '{op_spec.name}'")

    operation_class = known_operations[op_spec.name]
    return operation_class(**op_spec.parsed_config)


def normalize_op_definition(op_spec: OperationSpec) -> OperationDefinition:
    if isinstance(op_spec, str):
        return OperationDefinition(name=op_spec, config={})
    elif isinstance(op_spec, collections.abc.Mapping):
        if len(op_spec) != 1:
            raise TaskParserError(
                "Operation definition with dict should only have a single key"
                f", but given {op_spec}"
            )
        op_name = utils.first(op_spec.keys())
        return OperationDefinition(name=op_name, config=op_spec[op_name])
    elif isinstance(op_spec, collections.abc.Sequence):
        if len(op_spec) != 2:
            raise TaskParserError(
                "Operation definition with sequence should only have two items"
                f", but given {op_spec}"
            )
        return OperationDefinition(*op_spec)
    raise TaskParserError(f"Could not parse operation definition: {op_spec}")
