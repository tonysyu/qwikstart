import logging
from typing import Any, Dict, NamedTuple, Optional, Type, cast

from ..exceptions import ObsoleteError, TaskParserError
from ..operations import BaseOperation, GenericOperation
from ..utils.io import dump_yaml_string

__all__ = ["OperationDefinition"]

logger = logging.getLogger(__name__)
OperationMapping = Dict[str, Type[GenericOperation]]
RESERVED_WORDS_OPERATION_CONFIG = {
    "opconfig",
    "description",
    "input_mapping",
    "local_context",
    "output_mapping",
}


MAPPING_OBSOLETE_ERROR = (
    "Support for `{0}` as a top-level config in task definitions was removed in v0.8. "
    "Use `opconfig.{0}` instead."
)


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
        description = self.config.get("description", "")
        opconfig = self.config.get("opconfig", {})

        if "input_mapping" in self.config:
            raise ObsoleteError(MAPPING_OBSOLETE_ERROR.format("input_mapping"))
        if "output_mapping" in self.config:
            raise ObsoleteError(MAPPING_OBSOLETE_ERROR.format("output_mapping"))

        local_context = self.config.get("local_context", {})
        local_context.update(
            {
                key: value
                for key, value in self.config.items()
                if key not in RESERVED_WORDS_OPERATION_CONFIG
            }
        )
        return {
            "local_context": local_context,
            "opconfig": opconfig,
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
        op_spec_string = dump_yaml_string(op_spec)
        raise TaskParserError(f"Operation definition has no name: \n\n{op_spec_string}")
    elif op_name not in known_operations:
        raise TaskParserError(f"Could not find operation named '{op_name}'")

    op_def = OperationDefinition(name=op_name, config=op_spec)
    operation_class = known_operations[op_name]
    return operation_class(**op_def.parsed_config)
