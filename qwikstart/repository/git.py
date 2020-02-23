import logging
import re
from pathlib import Path
from typing import NamedTuple, Optional

import git as gitlib

from ..config import get_user_config
from ..exceptions import RepoLoaderError

logger = logging.getLogger(__name__)

# Git url regex adapted from https://stackoverflow.com/a/22312124/260303
RX_GIT_URL_PREFIX = r"(?P<prefix>(git|ssh|http(s)?))"
RX_GIT_URL_SEPARATOR = r"(?P<separator>(:|@)(//)?)"
RX_GIT_URL_PATH = r"(?P<path>([\w\.@\:/\-~]+)(\.git)?(/)?)"
RX_GIT_URL = re.compile(RX_GIT_URL_PREFIX + RX_GIT_URL_SEPARATOR + RX_GIT_URL_PATH)


class GitUrl(NamedTuple):
    prefix: str
    separator: str
    raw_path: str

    @property
    def path(self) -> str:
        return self.raw_path.replace(":", "/")


def parse_git_url(url: str) -> Optional[GitUrl]:
    match = RX_GIT_URL.match(url)
    if not match:
        return None
    parts = match.groupdict()
    # Ignore typing: mypy can't detect keys in `groupdict`.
    return GitUrl(
        prefix=parts["prefix"], separator=parts["separator"], raw_path=parts["path"]
    )


def sync_git_repo_locally(git_url: str) -> Path:
    """Download or update local copy of git repo and return local path."""
    git_url = resolve_git_url(git_url)
    local_repo_path = get_local_repo_path(git_url)
    if not local_repo_path.exists():
        download_git_repo(git_url, local_repo_path)
    else:
        update_git_repo(local_repo_path)
    return local_repo_path


def resolve_git_url(url: str) -> str:
    prefix, _, repo_path = url.partition(":")
    config = get_user_config()
    if prefix in config.git_abbreviations:
        url = config.git_abbreviations[prefix].format(repo_path)
    return url


def get_local_repo_path(url: str) -> Path:
    git_url = parse_git_url(url)
    if git_url is None:
        raise RepoLoaderError(f"Cannot load from repo with no hostname: {url!r}")

    config = get_user_config()
    return config.repo_cache_path / git_url.path


def download_git_repo(repo_url: str, local_path: Path) -> None:
    logger.debug(f"Downloading qwikstart repo from {repo_url}")
    try:
        gitlib.Repo.clone_from(repo_url, str(local_path))
    except (gitlib.NoSuchPathError, gitlib.GitCommandError):
        raise RepoLoaderError(f"Could not load git repo: {repo_url}")
    logger.debug(f"Downloaded qwikstart repo from {repo_url} to {local_path}")


def update_git_repo(local_path: Path) -> None:
    logger.debug(f"Updating qwikstart repo at {local_path}")
    gitlib.Repo(str(local_path)).remote().pull()
