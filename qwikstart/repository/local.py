from pathlib import Path
from typing import Any, Dict, Optional

import yaml

from ..exceptions import TaskLoaderError

QWIKSTART_TASK_DEFINITION_FILE = "qwikstart.yml"


class YamlFileLoader:
    known_extensions = {".yaml", ".yml"}

    def can_load(self, file_path: Path) -> bool:
        return file_path.suffix in self.known_extensions

    def load(self, file_path: Path) -> Dict[str, Any]:
        with open(file_path) as f:
            return yaml.safe_load(f)


class LocalRepoLoader:

    loader = YamlFileLoader()

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
