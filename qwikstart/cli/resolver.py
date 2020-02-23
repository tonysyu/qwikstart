from typing import Optional, cast

from ..exceptions import RepoLoaderError, UserFacingError
from ..parser import parse_task
from ..repository import BaseRepoLoader, GitRepoLoader, LocalRepoLoader, TaskSpec
from ..tasks import Task


def resolve_task(task_path: str, repo_url: Optional[str] = None) -> Task:
    try:
        loader = get_repo_loader(task_path, repo_url)
    except RepoLoaderError as error:
        raise UserFacingError(str(error)) from error

    # FIXME: We should check whether the data has the required keys.
    task_spec = cast(TaskSpec, loader.task_spec)
    return parse_task(task_spec, loader.repo_path)


def get_repo_loader(task_path: str, repo_url: Optional[str] = None) -> BaseRepoLoader:
    if repo_url is not None:
        return GitRepoLoader(repo_url, task_path)
    return LocalRepoLoader(task_path)
