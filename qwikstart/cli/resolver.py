from typing import Optional, cast

from ..exceptions import RepoLoaderError, UserFacingError
from ..parser import TaskDefinition, parse_task
from ..repository import BaseRepoLoader, GitRepoLoader, LocalRepoLoader
from ..tasks import Task
from ..utils import full_class_name


def resolve_task(task_path: str, repo_url: Optional[str] = None) -> Task:
    try:
        loader = get_repo_loader(task_path, repo_url)
    except RepoLoaderError as error:
        raise UserFacingError(str(error)) from error

    if not loader.can_load_spec():
        msg = f"{full_class_name(loader)}: Cannot load {loader.spec_path}"
        raise UserFacingError(msg)

    task_spec = loader.load_raw_task_spec()
    # FIXME: We should check whether the data has the required keys.
    task_definition = cast(TaskDefinition, task_spec)
    return parse_task(task_definition, loader.spec_path)


def get_repo_loader(task_path: str, repo_url: Optional[str] = None) -> BaseRepoLoader:
    if repo_url is not None:
        return GitRepoLoader(repo_url, task_path)
    return LocalRepoLoader(task_path)
