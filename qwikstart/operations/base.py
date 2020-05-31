import abc
import logging
from collections import ChainMap
from dataclasses import dataclass
from typing import (
    Any,
    Dict,
    Generic,
    List,
    Mapping,
    Optional,
    Type,
    TypeVar,
    Union,
    cast,
)

from .. import utils
from ..base_context import BaseContext, DictContext

__all__ = ["BaseOperation", "GenericOperation", "OperationConfig"]

logger = logging.getLogger(__name__)

ContextData = Optional[Mapping[str, Any]]
ContextMapping = Mapping[str, str]
TContext = TypeVar("TContext", bound=BaseContext)
TOutput = TypeVar("TOutput", bound=Optional[DictContext])
TOperationConfig = TypeVar("TOperationConfig", bound="OperationConfig")

SUCCESS_MARK = "\N{HEAVY CHECK MARK}"
FAILURE_MARK = "\N{HEAVY BALLOT X}"


DEFAULT_OPERATION_CONFIG: Dict[str, Any] = dict(
    input_mapping={},
    output_mapping={},
    input_namespace=None,
    output_namespace=None,
    display_description=True,
)


@dataclass
class OperationConfig:
    input_mapping: Union[ContextMapping]
    output_mapping: Union[ContextMapping]
    input_namespace: Union[str, None]
    output_namespace: Union[str, None]
    display_description: Union[bool]

    @classmethod
    def create(cls: Type[TOperationConfig], **kwargs: Any) -> TOperationConfig:
        return cls.from_config_dicts(kwargs)

    @classmethod
    def from_config_dicts(
        cls: Type[TOperationConfig], *opconfig_dicts: Dict[str, Any]
    ) -> TOperationConfig:
        """Return OperationConfig from multiple opconfig dictionaries.

        Note that values in the later dictionaries take precendence over earlier ones.
        """
        # Reverse the order so that later dictionary values take precedence. This
        # ordering matches the behavior of `qwikstart.utils.merge_nested_dicts`.
        ordered_dicts = list(reversed(opconfig_dicts))
        ordered_dicts.append(DEFAULT_OPERATION_CONFIG)

        return cls(**ChainMap(*ordered_dicts))


class BaseOperation(Generic[TContext, TOutput], metaclass=abc.ABCMeta):
    """An operation within a qwikstart `Task`"""

    name: str
    aliases: Optional[List[str]] = None
    default_opconfig: Dict[str, Any] = {}

    def __init__(
        self,
        local_context: ContextData = None,
        opconfig: Optional[Dict[str, Any]] = None,
        description: str = "",
    ):
        self.local_context = local_context or {}
        self.description = description
        self.opconfig = OperationConfig.from_config_dicts(
            self.default_opconfig, opconfig or {}
        )

    @abc.abstractmethod
    def run(self, context: TContext) -> TOutput:
        """Override with action"""

    def pre_run(self, context_dict: DictContext) -> TContext:
        context_class = self.get_context_class()
        context_dict = utils.remap_dict(context_dict, self.opconfig.input_mapping)

        if self.opconfig.input_namespace is not None:
            context_dict = {
                **context_dict[self.opconfig.input_namespace],
                "execution_context": context_dict["execution_context"],
            }

        merged_dict = utils.merge_nested_dicts(context_dict, self.local_context)
        return context_class.from_dict(merged_dict)

    def post_run(self, output: TOutput) -> DictContext:
        if not output:
            return {}

        if self.opconfig.output_namespace is not None:
            output = cast(TOutput, {self.opconfig.output_namespace: output})

        # If output is not `None`, then it should be a dict; tell mypy.
        return utils.remap_dict(cast(DictContext, output), self.opconfig.output_mapping)

    def execute(self, global_context: DictContext) -> Dict[str, Any]:
        context = self.pre_run(global_context)
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
        return utils.merge_nested_dicts(global_context, output_dict, inplace=True)

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
