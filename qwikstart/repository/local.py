from pathlib import Path
from typing import Any, Dict, Optional

import yaml

from ..exceptions import RepoLoaderError
from .base import BaseRepoLoader

QWIKSTART_TASK_DEFINITION_FILE = "qwikstart.yml"


class YamlFileLoader:
    known_extensions = {".yaml", ".yml"}

    def can_load(self, file_path: Path) -> bool:
        return file_path.suffix in self.known_extensions

    def load(self, file_path: Path) -> Dict[str, Any]:
        with open(file_path) as f:
            return yaml.safe_load(f)


class LocalRepoLoader(BaseRepoLoader):
    """Loader for qwikstart task repos stored on the local filesystem."""

    file_loader = YamlFileLoader()

    def __init__(self, path: str, root: Optional[Path] = None):
        root = root or Path(".")
        self._local_path = root.joinpath(path).resolve()
        if self._local_path.is_dir():
            self._local_path = self.resolved_path / QWIKSTART_TASK_DEFINITION_FILE

    @property
    def resolved_path(self) -> Path:
        return self._local_path

    def can_load(self) -> bool:
        return self.resolved_path.is_file() and self._can_load_file()

    def _can_load_file(self) -> bool:
        return self.file_loader.can_load(self.resolved_path)

    def load_task_data(self) -> Dict[str, Any]:
        if not self.can_load():
            raise RepoLoaderError(f"Cannot load {self.resolved_path!r}")
        return self.file_loader.load(self.resolved_path)
