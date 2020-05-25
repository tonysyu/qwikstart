from typing import Any, Dict, List, Tuple, Union

QWIKSTART_TASK_SPEC_FILE = "qwikstart.yml"

OperationSpec = Union[str, Dict[str, Any], Tuple[str, Any]]
OperationsList = Union[List[OperationSpec], Dict[str, OperationSpec]]
