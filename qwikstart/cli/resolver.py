#!/usr/bin/env python3
from pathlib import Path
from typing import Any, Dict, cast

import yaml

from ..parser import TaskDefinition, parse_task


class YamlLoader:
    known_extensions = {".yaml", ".yml"}

    def can_handle(self, file_path: Path) -> bool:
        return file_path.suffix in self.known_extensions

    def load(self, file_path: Path) -> Dict[str, Any]:
        with open(file_path) as f:
            return yaml.safe_load(f)


loaders_list = [YamlLoader()]


class ResolveLocalPath:
    def __init__(self, path: str, root: Path = None):
        root = root or Path(".")
        self.resolved_path = root.joinpath(path).resolve()

    def exists(self) -> bool:
        return self.resolved_path.is_file()

    def parsed_data(self) -> Dict[str, Any]:
        for loader in loaders_list:
            if loader.can_handle(self.resolved_path):
                return loader.load(self.resolved_path)
        else:
            raise RuntimeError(f"No loader to handle {self.resolved_path!r}")


task_resolver_list = [ResolveLocalPath]


def resolve_task(task_path):
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
        raise RuntimeError(f"Could not resolve path. Attempted: {attempts}")
