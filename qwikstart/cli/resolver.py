from typing import cast

from ..exceptions import TaskLoaderError
from ..parser import TaskDefinition, parse_task
from ..repository import LocalRepoLoader
from ..tasks import Task

task_resolver_list = [LocalRepoLoader]


def resolve_task(task_path: str) -> Task:
    attempted_paths = []
    for path_resolver in task_resolver_list:
        resolver = path_resolver(task_path)
        if resolver.exists():
            parsed_data = resolver.parsed_data()
            # FIXME: We should check whether the data has the required keys.
            task_definition = cast(TaskDefinition, parsed_data)
            return parse_task(task_definition, resolver.resolved_path)
        else:
            attempted_paths.append(resolver.resolved_path)
    else:
        attempts = "\n- ".join(str(path) for path in attempted_paths)
        raise TaskLoaderError(f"Could not resolve path. Attempted: {attempts}")
