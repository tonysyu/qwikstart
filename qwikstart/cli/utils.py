import inspect
from dataclasses import dataclass, field
from typing import Any, List

from ..parser import get_operations_mapping


@dataclass(frozen=True)
class ContextVar:
    name: str
    annotation: Any
    default: Any = inspect.Parameter.empty

    @classmethod
    def from_parameter(cls, parameter: inspect.Parameter):
        return cls(
            name=parameter.name,
            annotation=parameter.annotation,
            default=parameter.default,
        )


@dataclass(frozen=True)
class OperationHelp:
    name: str
    docstring: str
    required_context: List[ContextVar] = field(default_factory=list)
    optional_context: List[ContextVar] = field(default_factory=list)


def get_operation_help(op_name: str) -> OperationHelp:
    op_mapping = get_operations_mapping()
    operation = op_mapping[op_name]

    context_signature = inspect.signature(operation.get_context_class())
    required_context = []
    optional_context = []
    for parameter in context_signature.parameters.values():
        context = (
            required_context
            if parameter.default is inspect.Parameter.empty
            else optional_context
        )
        context.append(ContextVar.from_parameter(parameter))

    return OperationHelp(
        name=op_name,
        docstring=operation.__doc__,
        required_context=required_context,
        optional_context=optional_context,
    )
