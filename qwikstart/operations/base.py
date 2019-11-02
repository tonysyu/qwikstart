import abc
from typing import Any, Mapping, Optional

__all__ = ["Operation", "OperationError"]


ContextMapping = Optional[Mapping[str, Any]]


class OperationError(RuntimeError):
    pass


class Operation(abc.ABC):
    """An operation within an qwikstart `Task`"""

    name: str

    def __init__(
        self,
        mapping: ContextMapping = None,
        input_mapping: ContextMapping = None,
        output_mapping: ContextMapping = None,
    ):
        if mapping and (input_mapping or output_mapping):
            msg = "`mapping` cannot be specified with input or output mappings"
            raise ValueError(msg)
        if mapping:
            input_mapping = mapping
            output_mapping = {value: key for key, value in mapping.items()}
        self.input_mapping = input_mapping or {}
        self.output_mapping = output_mapping or {}

    @abc.abstractmethod
    def run(self, context):
        """Override with action"""

    def pre_run(self, context):
        if not context:
            return {}
        return {
            self.input_mapping.get(key, key): value
            for key, value in context.items()
        }

    def post_run(self, context):
        if not context:
            return {}
        return {
            self.output_mapping.get(key, key): value
            for key, value in context.items()
        }

    def execute(self, original_context):
        context = self.pre_run(original_context)
        context = self.run(context)
        context = self.post_run(context)
        return {**original_context, **context}
