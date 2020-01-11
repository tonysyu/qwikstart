import abc
from pathlib import Path
from typing import Any, Dict


class BaseRepoLoader(abc.ABC):
    """Base class for loader for qwikstart task repos."""

    @abc.abstractmethod
    def can_load(self) -> bool:
        """Return true if this loader can load the qwikstart task data."""

    @abc.abstractmethod
    def load_task_data(self) -> Dict[str, Any]:
        """Return task definition dictionary loaded from qwikstart repo."""

    @property
    @abc.abstractmethod
    def resolved_path(self) -> Path:
        """Return local path to qwikstart repo."""
