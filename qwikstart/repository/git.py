from pathlib import Path
from typing import Any, Dict
from urllib.parse import urlparse

import git as _git

from ..config import get_user_config
from ..exceptions import RepoLoaderError
from . import base, local

# Separator between git repo url and paths within the git repo.
PATH_SEPARATOR = "::"


class GitRepoLoader(base.BaseRepoLoader):
    """Loader for qwikstart task repos stored in git repos."""

    def __init__(self, path: str):
        local_path = get_local_repo_path(path)
        if not local_path.exists():
            download_git_repo(path, local_path)
        self._local_loader = local.LocalRepoLoader(str(local_path))

    @property
    def resolved_path(self) -> Path:
        return self._local_loader.resolved_path

    def can_load(self) -> bool:
        return self._local_loader.can_load()

    def load_task_data(self) -> Dict[str, Any]:
        return self._local_loader.load_task_data()


def get_local_repo_path(url: str) -> Path:
    config = get_user_config()
    parsed_url = urlparse(url)
    if parsed_url.hostname is None:
        raise RepoLoaderError(f"Cannot load from repo with no hostname: {url!r}")
    local_repo_path = parsed_url.hostname + str(parsed_url.path)
    return config.qwikstart_cache / local_repo_path


def download_git_repo(repo_url: str, local_path: Path) -> None:
    try:
        _git.Repo.clone_from(repo_url, str(local_path))
    except (_git.NoSuchPathError, _git.GitCommandError):
        raise RepoLoaderError(f"Could not load git repo: {repo_url}")
