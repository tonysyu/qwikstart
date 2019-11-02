from dataclasses import dataclass
from typing import Any, List

from .operations import BaseOperation


__all__ = ["Task"]


@dataclass
class Task:
    """A series of operations to complete an qwikstart task."""

    name: str
    operations: List[BaseOperation]
    variables: List[Any] = []
