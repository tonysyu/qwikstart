from typing import cast

from ..exceptions import TaskLoaderError
from ..parser import TaskDefinition, parse_task
from ..repository import LocalRepoLoader
from ..tasks import Task

repo_loader_list = [LocalRepoLoader]


def resolve_task(task_path: str) -> Task:
    attempted_paths = []
    for repo_loader in repo_loader_list:
        loader = repo_loader(task_path)
        if loader.can_load():
            task_data = loader.load_task_data()
            # FIXME: We should check whether the data has the required keys.
            task_definition = cast(TaskDefinition, task_data)
            return parse_task(task_definition, loader.resolved_path)
        else:
            attempted_paths.append(loader.resolved_path)
    else:
        attempts = "\n- ".join(str(path) for path in attempted_paths)
        raise TaskLoaderError(f"Could not resolve path. Attempted: {attempts}")
