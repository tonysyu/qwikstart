import abc
from typing import Any, Dict, Mapping, Optional

from .. import utils
from ..base_context import BaseContext

__all__ = ["BaseOperation", "OperationError"]


ContextMapping = Optional[Mapping[str, Any]]


class OperationError(RuntimeError):
    pass


class OperationDefinitionError(ValueError):
    pass


class BaseOperation(abc.ABC):
    """An operation within a qwikstart `Task`"""

    name: str

    def __init__(
        self,
        local_context: ContextMapping = None,
        mapping: ContextMapping = None,
        input_mapping: ContextMapping = None,
        output_mapping: ContextMapping = None,
    ):
        self.local_context = local_context or {}

        if mapping and (input_mapping or output_mapping):
            msg = "`mapping` cannot be specified with input or output mappings"
            raise OperationDefinitionError(msg)
        if mapping:
            input_mapping = mapping
            output_mapping = {value: key for key, value in mapping.items()}
        self.input_mapping = input_mapping or {}
        self.output_mapping = output_mapping or {}

    @abc.abstractmethod
    def run(self, context):
        """Override with action"""

    def pre_run(self, context):
        context_class = self.get_context_class()
        if not context_class:
            return BaseContext()

        context = utils.remap_dict(context, self.input_mapping)
        return context_class.from_dict(**context, **self.local_context)

    def post_run(self, context):
        if not context:
            return {}

        return utils.remap_dict(context, self.output_mapping)

    def execute(self, original_context) -> Dict[str, Any]:
        context = self.pre_run(original_context)
        context_dict = self.run(context)
        context_dict = self.post_run(context_dict)
        return {**original_context, **context_dict}

    def __repr__(self):
        return (
            utils.full_class_name(self)
            + f"(local_context={self.local_context}, "
            f"input_mapping={self.input_mapping}, "
            f"output_mapping={self.output_mapping})"
        )

    def __eq__(self, other):
        return (
            other.__class__ is self.__class__
            and other.local_context == self.local_context
            and other.input_mapping == self.input_mapping
            and other.output_mapping == self.output_mapping
        )

    @classmethod
    def get_context_class(cls):
        return cls.run.__annotations__["context"]
