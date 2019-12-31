from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from typing_extensions import TypedDict

from .. import base_context
from ..tasks import Task
from .core import get_operations_mapping
from .operations import UnparsedOperation, parse_operation

OperationsList = Union[List[UnparsedOperation], Dict[str, UnparsedOperation]]


class TaskDefinition(TypedDict, total=False):
    context: Dict[str, Any]
    operations: OperationsList


def parse_task(
    task_definition: TaskDefinition, source_path: Optional[Path] = None
) -> Task:
    """Return task parsed from a task definition dictionary."""
    normalize_context(task_definition, source_path)

    known_operations = get_operations_mapping()

    operations = [
        parse_operation(op_def, known_operations)
        for op_def in normalize_operations_list(task_definition["operations"])
    ]

    return Task(context=task_definition["context"], operations=operations)


def normalize_operations_list(operations_list: OperationsList) -> List[Dict[str, Any]]:
    """"""
    if isinstance(operations_list, list):
        return operations_list  # type: ignore
    return [{op_name: op_config} for op_name, op_config in operations_list.items()]


def normalize_context(
    task_definition: TaskDefinition, source_path: Optional[Path] = None
) -> None:
    task_definition.setdefault("context", {})
    source_dir = source_path.parent if source_path else Path(".")
    task_definition["context"].setdefault(
        "execution_context",
        base_context.ExecutionContext(source_dir=source_dir, target_dir=Path(".")),
    )
