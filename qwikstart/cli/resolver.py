from pathlib import Path
from typing import Any, Dict, Optional, cast

import yaml

from ..exceptions import TaskLoaderError
from ..parser import TaskDefinition, parse_task
from ..tasks import Task

QWIKSTART_TASK_DEFINITION_FILE = "qwikstart.yml"


class YamlLoader:
    known_extensions = {".yaml", ".yml"}

    def can_load(self, file_path: Path) -> bool:
        return file_path.suffix in self.known_extensions

    def load(self, file_path: Path) -> Dict[str, Any]:
        with open(file_path) as f:
            return yaml.safe_load(f)


class LocalPathResolver:

    loader = YamlLoader()

    def __init__(self, path: str, root: Optional[Path] = None):
        root = root or Path(".")
        self.resolved_path = root.joinpath(path).resolve()
        if self.resolved_path.is_dir():
            self.resolved_path = self.resolved_path / QWIKSTART_TASK_DEFINITION_FILE

    def exists(self) -> bool:
        return self.resolved_path.is_file()

    def parsed_data(self) -> Dict[str, Any]:
        if self.loader.can_load(self.resolved_path):
            return self.loader.load(self.resolved_path)
        else:
            raise TaskLoaderError(f"Cannot load {self.resolved_path!r}")


task_resolver_list = [LocalPathResolver]


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
