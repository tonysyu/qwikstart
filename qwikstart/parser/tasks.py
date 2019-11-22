from pathlib import Path
from typing import Any, Dict, List

from typing_extensions import TypedDict

from .. import base_context
from ..tasks import Task
from .core import ParserError, get_operations_mapping
from .operations import OPERATION_DEFINITION, parse_operation

__all__ = ["parse_task"]


class RequiredTaskDefinition(TypedDict):
    operations: List[OPERATION_DEFINITION]


class TaskDefinition(RequiredTaskDefinition):
    context: Dict[str, Any]


def parse_task(task_definition: TaskDefinition) -> Task:
    """Return task parsed from a task definition dictionary."""
    task_definition = normalize_task_definition(task_definition)

    known_operations = get_operations_mapping()

    operations = [
        parse_operation(op_def, known_operations)
        for op_def in task_definition["operations"]
    ]

    return Task(context=task_definition["context"], operations=operations)


def normalize_task_definition(
    task_definition: TaskDefinition
) -> TaskDefinition:
    context = {
        "execution_context": base_context.ExecutionContext(
            source_dir=Path("."), target_dir=Path(".")
        )
    }
    return {
        "context": task_definition.get("context", context),
        "operations": task_definition["operations"],
    }
