from typing import Any, Dict, Optional

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

    execution_config = execution_config or {}
    execution_config.setdefault("source_dir", loader.repo_path)
    return parse_task(loader.task_spec, execution_config=execution_config)
