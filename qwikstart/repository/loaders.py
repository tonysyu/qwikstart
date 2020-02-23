import abc
from pathlib import Path
from typing import Any, Dict

import yaml

from ..exceptions import RepoLoaderError
from ..utils import io
from . import git
from .core import QWIKSTART_TASK_SPEC_FILE


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


class LocalRepoLoader(BaseRepoLoader):
    """Loader for qwikstart task repos stored on the local filesystem."""

    def __init__(self, path: str):
        self._spec_path = Path(path).resolve()
        if self._spec_path.is_dir():
            self._spec_path = self._spec_path / QWIKSTART_TASK_SPEC_FILE

    @property
    def task_spec(self) -> Dict[str, Any]:
        try:
            return io.load_yaml_file(self._spec_path)
        except yaml.YAMLError as error:
            raise RepoLoaderError(f"Cannot load {self._spec_path!r}") from error

    @property
    def repo_path(self) -> Path:
        """Return local path to qwikstart repo."""
        return self._spec_path.parent


class GitRepoLoader(BaseRepoLoader):
    """Loader for qwikstart task repos stored in git repos."""

    def __init__(self, git_url: str, path: str = ""):
        local_path = git.sync_git_repo_locally(git_url) / path
        self._local_loader = LocalRepoLoader(str(local_path))

    @property
    def task_spec(self) -> Dict[str, Any]:
        return self._local_loader.task_spec

    @property
    def repo_path(self) -> Path:
        """Return local path to qwikstart repo."""
        return self._local_loader.repo_path
