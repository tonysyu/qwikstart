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
        self._spec_path = _resolve_task_spec_path(path)

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
            self._repo_path = None
            self._task_spec = io.load_yaml_string(url_contents)
        else:
            local_path = _resolve_task_spec_path(url_or_path)
            # This repo path may get overwritten if task spec defines `source.url`
            self._repo_path = local_path.parent
            self._task_spec = io.load_yaml_file(local_path)

        source = self._task_spec.get("source", {})
        git_url = source.get("url")
        if git_url:
            local_git_repo = git.sync_git_repo_locally(git_url)
            self._repo_path = local_git_repo / source.get("path", "")

        if self._repo_path is None:
            raise RepoLoaderError(
                "Qwikstart repository not valid. This can happen when:\n"
                "- Given a url to a qwikstart file that does not define `source.url`\n"
            )

    @property
    def task_spec(self) -> Dict[str, Any]:
        return self._task_spec

    @property
    def repo_path(self) -> Path:
        """Return local path to qwikstart repo."""
        return self._repo_path


def _resolve_task_spec_path(path_string: str) -> Path:
    """Return Path to task spec from string path.

    Note that the input path can be either the yaml file containing the task spec data
    or a directory that contains a file with the name `qwikstart.yml`.
    """
    spec_path = Path(path_string).resolve()
    return spec_path / QWIKSTART_TASK_SPEC_FILE if spec_path.is_dir() else spec_path
