from dataclasses import dataclass
from typing import Any, List

from .actions import Action


__all__ = ["Step", "Task"]


@dataclass
class Step:
    """A step within an qwikstart `Task`"""

    name: str
    actions: List[Action]
    pre_conditions: List[Any] = []
    post_conditions: List[Any] = []


@dataclass
class Task:
    """A series of steps to complete an qwikstart task."""

    name: str
    steps: List[Step]
    variables: List[Any] = []
