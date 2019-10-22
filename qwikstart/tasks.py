from dataclasses import dataclass
from typing import Any, List

from .operations import Operation


__all__ = ["Task"]


@dataclass
class Task:
    """A series of operations to complete an qwikstart task."""

    name: str
    operations: List[Operation]
    variables: List[Any] = []
