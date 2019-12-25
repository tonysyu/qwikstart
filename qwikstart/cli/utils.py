import dataclasses
import inspect
from typing import Any, List

from ..base_context import BaseContext
from ..parser import get_operations_mapping

__all__ = ["get_operation_help"]


@dataclasses.dataclass(frozen=True)
class ContextVar:
    name: str
    annotation: Any
    default: Any = dataclasses.MISSING
    description: str = ""

    @property
    def is_required(self):
        return self.default is dataclasses.MISSING


@dataclasses.dataclass(frozen=True)
class OperationHelp:
    name: str
    docstring: str
    required_context: List[ContextVar]
    optional_context: List[ContextVar]


def get_operation_help(op_name: str) -> OperationHelp:
    op_mapping = get_operations_mapping()
    operation = op_mapping[op_name]

    context_class = operation.get_context_class()
    context_signature = inspect.signature(context_class)
    required_context = []
    optional_context = []
    for field in context_class.__dataclass_fields__.values():
        if field.name != "execution_context":
            context_var = ContextVar(
                name=field.name,
                annotation=field.type,
                default=_get_default(field),
                description=context_class.help(field.name),
            )
            context = (
                required_context
                if context_var.is_required
                else optional_context
            )
            context.append(context_var)

    return OperationHelp(
        name=op_name,
        docstring=operation.__doc__,
        required_context=required_context,
        optional_context=optional_context,
    )


def _get_default(field: dataclasses.Field):
    return (
        field.default
        if field.default is not dataclasses.MISSING
        else field.default_factory
    )
