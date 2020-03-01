import abc
from pathlib import Path
from typing import Any, Dict

from ruamel.yaml import YAMLError

from ..exceptions import RepoLoaderError
from ..utils import http, io
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
        except YAMLError as error:
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


class DetachedRepoLoader(BaseRepoLoader):
    """Loader for qwikstart task spec that is detached from the qwikstart repo.

    The task spec must specify a source url for the location of the qwikstart repo.
    """

    def __init__(self, url_or_path: str = ""):
        if http.is_url(url_or_path):
            url_contents = http.read_from_url(url_or_path)
            self._task_spec = io.load_yaml_string(url_contents)
        else:
            path = Path(url_or_path)
            self._task_spec = io.load_yaml_file(path)

        source = self._task_spec.get("source", {})
        git_url = source.get("url")
        if not git_url:
            raise RepoLoaderError(
                f"Task defined by {url_or_path} must define `source.url`"
            )

        local_path = git.sync_git_repo_locally(git_url) / source.get("path", "")
        self._local_loader = LocalRepoLoader(str(local_path))

    @property
    def task_spec(self) -> Dict[str, Any]:
        return self._task_spec

    @property
    def repo_path(self) -> Path:
        """Return local path to qwikstart repo."""
        return self._local_loader.repo_path
