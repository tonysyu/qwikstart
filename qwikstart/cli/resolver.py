from typing import List, cast

from ..exceptions import RepoLoaderError, UserFacingError
from ..parser import TaskDefinition, parse_task
from ..repository import GitRepoLoader, LocalRepoLoader
from ..tasks import Task

repo_loader_list = [LocalRepoLoader, GitRepoLoader]


def resolve_task(task_path: str) -> Task:
    failed_attempts: List[str] = []
    for repo_loader in repo_loader_list:
        try:
            loader = repo_loader(task_path)
        except RepoLoaderError as error:
            failed_attempts.append(f"{repo_loader.__name__}: {error}")
            continue
        if loader.can_load():
            task_data = loader.load_task_data()
            # FIXME: We should check whether the data has the required keys.
            task_definition = cast(TaskDefinition, task_data)
            return parse_task(task_definition, loader.resolved_path)
        else:
            msg = f"{loader.__class__.__name__}: Cannot load {loader.resolved_path}"
            failed_attempts.append(msg)
    else:
        attempts = "\n- " + "\n- ".join(str(path) for path in failed_attempts)
        raise UserFacingError(f"Could not resolve path. Failed attempts: {attempts}")
