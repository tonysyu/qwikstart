from typing import Any, Dict, Optional, cast

from .. import repository
from ..exceptions import RepoLoaderError, UserFacingError
from ..parser import parse_task
from ..tasks import Task


def resolve_task(
    task_path: str,
    repo_url: Optional[str] = None,
    execution_config: Optional[Dict[str, Any]] = None,
) -> Task:
    try:
        loader = repository.get_repo_loader(task_path, repo_url)
    except RepoLoaderError as error:
        raise UserFacingError(str(error)) from error

    # FIXME: We should check whether the data has the required keys.
    task_spec = cast(repository.TaskSpec, loader.task_spec)

    execution_config = execution_config or {}
    execution_config.setdefault("source_dir", loader.repo_path)
    return parse_task(task_spec, execution_config=execution_config)
