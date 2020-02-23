import abc
from pathlib import Path
from typing import Any, Dict


class BaseRepoLoader(abc.ABC):
    """Base class for loader for qwikstart task repos."""

    @property
    @abc.abstractmethod
    def task_spec(self) -> Dict[str, Any]:
        """Return raw task specification loaded from qwikstart repo."""

    @property
    @abc.abstractmethod
    def repo_path(self) -> Path:
        """Return local path to qwikstart repo."""
