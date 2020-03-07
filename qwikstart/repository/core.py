from typing import Any, Dict, List, Tuple, Union

from typing_extensions import TypedDict

QWIKSTART_TASK_SPEC_FILE = "qwikstart.yml"

OperationSpec = Union[str, Dict[str, Any], Tuple[str, Any]]
OperationsList = Union[List[OperationSpec], Dict[str, OperationSpec]]


class TaskSpec(TypedDict, total=False):
    context: Dict[str, Any]
    steps: Dict[str, Dict[str, Any]]
    # FIXME: `operations` should be deprecated in favor of `steps`
    operations: OperationsList
