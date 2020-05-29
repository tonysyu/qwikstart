import abc
from pathlib import Path
from typing import Any, Dict, Optional, cast

from ..exceptions import RepoLoaderError
from ..utils import http, io
from . import git, yamllint
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


def get_repo_loader(task_path: str, repo_url: Optional[str] = None) -> BaseRepoLoader:
    if repo_url is not None:
        return GitRepoLoader(repo_url, task_path)
    return RepoLoader(task_path)


class GitRepoLoader(BaseRepoLoader):
    """Loader for qwikstart task repos stored in git repos."""

    def __init__(self, git_url: str, path: str = ""):
        local_path = git.sync_git_repo_locally(git_url) / path
        self._local_loader = RepoLoader(str(local_path))

    @property
    def task_spec(self) -> Dict[str, Any]:
        return self._local_loader.task_spec

    @property
    def repo_path(self) -> Path:
        """Return local path to qwikstart repo."""
        return self._local_loader.repo_path


class RepoLoader(BaseRepoLoader):
    """Loader for qwikstart task spec.

    The task spec must specify a source url for the location of the qwikstart repo.
    """

    def __init__(self, url_or_path: str = ""):
        if http.is_url(url_or_path):
            self._repo_path = None
            spec_contents = http.read_from_url(url_or_path)
        else:
            local_path = _resolve_task_spec_path(url_or_path)
            # This repo path may get overwritten if task spec defines `source.url`
            self._repo_path = local_path.parent
            spec_contents = io.read_file_contents(local_path)

        yamllint.assert_no_errors(spec_contents)
        self._task_spec = io.load_yaml_string(spec_contents)

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
        # Cast to avoid type error, even though `None` is excluded in __init__.
        return cast(Path, self._repo_path)


def _resolve_task_spec_path(path_string: str) -> Path:
    """Return Path to task spec from string path.

    Note that the input path can be either the yaml file containing the task spec data
    or a directory that contains a file with the name `qwikstart.yml`.
    """
    spec_path = Path(path_string).resolve()
    return spec_path / QWIKSTART_TASK_SPEC_FILE if spec_path.is_dir() else spec_path
