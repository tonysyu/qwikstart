import abc
import logging
from dataclasses import dataclass
from typing import Any, Dict, Generic, List, Mapping, Optional, TypeVar, Union, cast

from .. import utils
from ..base_context import BaseContext, DictContext

__all__ = ["BaseOperation", "GenericOperation", "OperationConfig"]

logger = logging.getLogger(__name__)

ContextData = Optional[Mapping[str, Any]]
ContextMapping = Mapping[str, str]
TContext = TypeVar("TContext", bound=BaseContext)
TOutput = TypeVar("TOutput", bound=Optional[DictContext])

SUCCESS_MARK = "\N{HEAVY CHECK MARK}"
FAILURE_MARK = "\N{HEAVY BALLOT X}"


class _NOT_SPECIFIED_TYPE:
    pass


NOT_SPECIFIED = _NOT_SPECIFIED_TYPE()


@dataclass
class OperationConfig:
    input_mapping: Union[ContextMapping, _NOT_SPECIFIED_TYPE] = NOT_SPECIFIED
    output_mapping: Union[ContextMapping, _NOT_SPECIFIED_TYPE] = NOT_SPECIFIED
    input_namespace: Union[str, None, _NOT_SPECIFIED_TYPE] = NOT_SPECIFIED
    output_namespace: Union[str, None, _NOT_SPECIFIED_TYPE] = NOT_SPECIFIED
    display_description: Union[bool, _NOT_SPECIFIED_TYPE] = NOT_SPECIFIED

    def update_unspecified_fields(self, **kwargs: Any) -> None:
        """Update any fields having value `NOT_SPECIFIED` with values in `kwargs`.

        Any fields with values other than `NOT_SPECIFIED` will not be altered. This
        method is used to support multiple layers of defaults and customization.
        """
        # Use `self.__dict__` instead of `dataclasses.asdict`, which copies objects,
        # so that `NOT_SPECIFIED` will no longer be identical.
        for name, value in self.__dict__.items():
            if value is NOT_SPECIFIED:
                new_value = kwargs.get(name, DEFAULT_OPERATION_CONFIG[name])
                setattr(self, name, new_value)


DEFAULT_OPERATION_CONFIG: Dict[str, Any] = dict(
    input_mapping={},
    output_mapping={},
    input_namespace=None,
    output_namespace=None,
    display_description=True,
)


class BaseOperation(Generic[TContext, TOutput], metaclass=abc.ABCMeta):
    """An operation within a qwikstart `Task`"""

    name: str
    aliases: Optional[List[str]] = None
    default_opconfig: Dict[str, Any] = {}

    def __init__(
        self,
        local_context: ContextData = None,
        opconfig: Optional[OperationConfig] = None,
        description: str = "",
    ):
        self.local_context = local_context or {}
        self.description = description
        self.opconfig = opconfig or OperationConfig()
        self.opconfig.update_unspecified_fields(**self.default_opconfig)

    @abc.abstractmethod
    def run(self, context: TContext) -> TOutput:
        """Override with action"""

    def pre_run(self, context_dict: DictContext) -> TContext:
        context_class = self.get_context_class()
        context_dict = utils.remap_dict(context_dict, self.opconfig.input_mapping)
        context_dict = (
            context_dict
            if self.opconfig.input_namespace is None
            else context_dict[self.opconfig.input_namespace]
        )
        merged_dict = utils.merge_nested_dicts(context_dict, self.local_context)
        return context_class.from_dict(merged_dict)

    def post_run(self, output: TOutput) -> DictContext:
        if not output:
            return {}

        output = (
            output
            if self.opconfig.output_namespace is None
            else {self.opconfig.output_namespace: output}
        )
        # If output is not `None`, then it should be a dict; tell mypy.
        return utils.remap_dict(cast(DictContext, output), self.opconfig.output_mapping)

    def execute(self, original_context: DictContext) -> Dict[str, Any]:
        context = self.pre_run(original_context)
        try:
            output = self.run(context)
        except Exception:
            if self.description:
                logger.error(f"{self.description}: {FAILURE_MARK}")
            raise
        else:
            if self.description and self.opconfig.display_description:
                logger.info(f"{self.description}: {SUCCESS_MARK}")
        output_dict = self.post_run(output)
        return utils.merge_nested_dicts(original_context, output_dict, inplace=True)

    def __repr__(self) -> str:
        return (
            utils.full_class_name(self) + f"(local_context={self.local_context}, "
            f"opconfig={self.opconfig}, description={self.description})"
        )

    def __eq__(self, other: Any) -> bool:
        return (
            other.__class__ is self.__class__
            and other.local_context == self.local_context
            and other.opconfig == self.opconfig
            and other.description == self.description
        )

    @classmethod
    def get_context_class(cls) -> TContext:
        return cast(TContext, cls.run.__annotations__["context"])

    @classmethod
    def get_output_class(cls) -> TOutput:
        return cast(TOutput, cls.run.__annotations__["return"])


GenericOperation = BaseOperation[BaseContext, Optional[DictContext]]
