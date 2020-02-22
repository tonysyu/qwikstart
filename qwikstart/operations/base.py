import abc
import logging
from typing import Any, Dict, Generic, List, Mapping, Optional, TypeVar, cast

from .. import utils
from ..base_context import BaseContext, DictContext

__all__ = ["BaseOperation", "GenericOperation"]

logger = logging.getLogger(__name__)

ContextData = Optional[Mapping[str, Any]]
ContextMapping = Optional[Mapping[str, str]]
TContext = TypeVar("TContext", bound=BaseContext)
TOutput = TypeVar("TOutput", bound=Optional[DictContext])

SUCCESS_MARK = "\N{HEAVY CHECK MARK}"
FAILURE_MARK = "\N{HEAVY BALLOT X}"


class BaseOperation(Generic[TContext, TOutput], metaclass=abc.ABCMeta):
    """An operation within a qwikstart `Task`"""

    name: str
    aliases: Optional[List[str]] = None

    def __init__(
        self,
        local_context: ContextData = None,
        input_mapping: ContextMapping = None,
        output_mapping: ContextMapping = None,
        description: str = "",
    ):
        self.local_context = local_context or {}
        self.input_mapping = input_mapping or {}
        self.output_mapping = output_mapping or {}
        self.description = description

    @abc.abstractmethod
    def run(self, context: TContext) -> TOutput:
        """Override with action"""

    def pre_run(self, context_dict: DictContext) -> TContext:
        context_class = self.get_context_class()
        context_dict = utils.remap_dict(context_dict, self.input_mapping)
        merged_dict = utils.merge_nested_dicts(context_dict, self.local_context)
        return context_class.from_dict(merged_dict)

    def post_run(self, output: TOutput) -> DictContext:
        if not output:
            return {}

        # If output is not `None`, then it should be a dict; tell mypy.
        return utils.remap_dict(cast(DictContext, output), self.output_mapping)

    def execute(self, original_context: DictContext) -> Dict[str, Any]:
        context = self.pre_run(original_context)
        try:
            output = self.run(context)
        except Exception:
            if self.description:
                logger.error(f"{self.description}: {FAILURE_MARK}")
            raise
        else:
            if self.description and getattr(context, "display_step_description", True):
                logger.info(f"{self.description}: {SUCCESS_MARK}")
        output_dict = self.post_run(output)
        return {**original_context, **output_dict}

    def __repr__(self) -> str:
        return (
            utils.full_class_name(self) + f"(local_context={self.local_context}, "
            f"input_mapping={self.input_mapping}, "
            f"output_mapping={self.output_mapping})"
        )

    def __eq__(self, other: Any) -> bool:
        return (
            other.__class__ is self.__class__
            and other.local_context == self.local_context
            and other.input_mapping == self.input_mapping
            and other.output_mapping == self.output_mapping
        )

    @classmethod
    def get_context_class(cls) -> TContext:
        return cast(TContext, cls.run.__annotations__["context"])

    @classmethod
    def get_output_class(cls) -> TOutput:
        return cast(TOutput, cls.run.__annotations__["return"])


GenericOperation = BaseOperation[BaseContext, Optional[DictContext]]
