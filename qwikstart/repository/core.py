from typing import Any, Dict, List, Tuple, Union

from typing_extensions import TypedDict

OperationSpec = Union[str, Dict[str, Dict[str, Any]], Tuple[str, Dict[str, Any]]]
OperationsList = Union[List[OperationSpec], Dict[str, OperationSpec]]


class TaskSpec(TypedDict, total=False):
    context: Dict[str, Any]
    steps: Dict[str, Dict[str, Any]]
    # FIXME: `operations` should be deprecated in favor of `steps`
    operations: OperationsList
