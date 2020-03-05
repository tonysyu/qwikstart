from typing import Optional, cast

from .. import repository
from ..exceptions import RepoLoaderError, UserFacingError
from ..parser import parse_task
from ..tasks import Task


def resolve_task(
    task_path: str, repo_url: Optional[str] = None, detached: bool = False
) -> Task:
    try:
        loader = get_repo_loader(task_path, repo_url, detached)
    except RepoLoaderError as error:
        raise UserFacingError(str(error)) from error

    # FIXME: We should check whether the data has the required keys.
    task_spec = cast(repository.TaskSpec, loader.task_spec)
    return parse_task(task_spec, loader.repo_path)


def get_repo_loader(
    task_path: str, repo_url: Optional[str] = None, detached: bool = False
) -> repository.BaseRepoLoader:
    if detached:
        if repo_url is not None:
            raise UserFacingError("Cannot used both `--detached` and `--repo` options")
        return repository.RepoLoader(task_path)
    if repo_url is not None:
        return repository.GitRepoLoader(repo_url, task_path)
    return repository.LocalRepoLoader(task_path)
