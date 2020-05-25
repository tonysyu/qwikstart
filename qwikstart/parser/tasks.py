import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from .. import base_context
from ..exceptions import TaskParserError
from ..operations import BaseOperation
from ..repository import OperationsList
from ..tasks import Task
from .operations import (
    get_operations_mapping,
    parse_operation,
    parse_operation_from_step,
)

logger = logging.getLogger(__name__)

EXAMPLE_TASK_DEFINITION = """
steps:
    "Display message":
        name: echo
        message: "Hello, World!"
"""
OPERATIONS_DEPRECATION_WARNING = (
    "Note that `operations` in task specification is deprecated and will be "
    "removed in v0.8. Use `steps` instead."
)


def parse_task(
    task_spec: Dict[str, Any], execution_config: Optional[Dict[str, Any]] = None,
) -> Task:
    """Return task parsed from a task specification dictionary."""
    context = _initialize_context(task_spec, execution_config=execution_config)
    operations = parse_task_steps(task_spec)
    return Task(context=context, operations=operations)


def parse_task_steps(task_spec: Dict[str, Any]) -> Sequence[BaseOperation[Any, Any]]:
    known_operations = get_operations_mapping()

    if task_spec.get("steps"):
        if task_spec.get("operations"):
            logger.warning(
                "Found both `steps` and `operations` in task specification. "
                "Only `steps` will be read."
            )
        return [
            parse_operation_from_step(
                {"description": op_desc, **op_def}, known_operations
            )
            for op_desc, op_def in task_spec["steps"].items()
        ]
    elif task_spec.get("operations"):
        # FIXME: Raise error in v0.8
        logger.info(OPERATIONS_DEPRECATION_WARNING)
        return [
            parse_operation(op_def, known_operations)
            for op_def in normalize_operations_list(task_spec["operations"])
        ]

    raise TaskParserError(
        "Task specification file should define `steps` dictionary, e.g.:\n"
        + EXAMPLE_TASK_DEFINITION
    )


def normalize_operations_list(operations_list: OperationsList) -> List[Dict[str, Any]]:
    """"""
    if isinstance(operations_list, list):
        return operations_list  # type: ignore
    return [{op_name: op_config} for op_name, op_config in operations_list.items()]


def _initialize_context(
    task_spec: Dict[str, Any], execution_config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    execution_config = execution_config or {}
    execution_config.setdefault("source_dir", Path("."))
    execution_config.setdefault("target_dir", Path("."))

    return {
        "execution_context": base_context.ExecutionContext(**execution_config),
        **task_spec.get("context", {}),
    }
