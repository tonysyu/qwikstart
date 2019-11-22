from pathlib import Path
from typing import Any, Dict, List, Union

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
        for op_def in normalize_operations_list(task_definition["operations"])
    ]

    return Task(context=task_definition["context"], operations=operations)


def normalize_operations_list(
    operations_list: Union[
        List[OPERATION_DEFINITION], Dict[str, OPERATION_DEFINITION]
    ],
) -> List[Dict]:
    """"""
    if isinstance(operations_list, list):
        return operations_list
    return [
        {op_name: op_config} for op_name, op_config in operations_list.items()
    ]


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
