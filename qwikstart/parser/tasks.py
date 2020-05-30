import logging
from pathlib import Path
from typing import Any, Dict, Optional, Sequence

from .. import base_context
from ..exceptions import ObsoleteError, TaskParserError
from ..operations import BaseOperation
from ..tasks import Task
from .operations import get_operations_mapping, parse_operation_from_step

logger = logging.getLogger(__name__)

EXAMPLE_TASK_DEFINITION = """
steps:
    "Display message":
        name: echo
        message: "Hello, World!"
"""
OPERATIONS_OBSOLETE_ERROR = (
    "Support for `operations` in task definition was removed in v0.8. "
    "Use `steps` instead."
)


def parse_task(
    task_spec: Dict[str, Any], execution_config: Optional[Dict[str, Any]] = None,
) -> Task:
    """Return task parsed from a task specification dictionary."""
    context = _initialize_context(task_spec, execution_config=execution_config)
    operations = parse_task_steps(task_spec)
    return Task(context=context, operations=operations)


def parse_task_steps(task_spec: Dict[str, Any]) -> Sequence[BaseOperation[Any, Any]]:
    if "operations" in task_spec:
        raise ObsoleteError(OPERATIONS_OBSOLETE_ERROR)

    if "steps" not in task_spec:
        raise TaskParserError(
            "Task specification file should define `steps` dictionary, e.g.:\n"
            + EXAMPLE_TASK_DEFINITION
        )

    known_operations = get_operations_mapping()
    return [
        parse_operation_from_step({"description": op_desc, **op_def}, known_operations)
        for op_desc, op_def in task_spec["steps"].items()
    ]


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
