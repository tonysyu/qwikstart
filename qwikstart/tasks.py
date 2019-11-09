from dataclasses import dataclass
from typing import Any, Dict, List

from .operations import BaseOperation

__all__ = ["Task"]


@dataclass
class Task:
    """A series of operations to complete an qwikstart task."""

    operations: List[BaseOperation]
    context: Dict[str, Any]

    def execute(self):
        context = self.context
        for operation in self.operations:
            context = operation.execute(context)
        return context
