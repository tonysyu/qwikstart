from pathlib import Path
from typing import Any, Dict

from ..exceptions import RepoLoaderError
from ..utils import io
from .base import BaseRepoLoader

QWIKSTART_TASK_SPEC_FILE = "qwikstart.yml"


class YamlFileLoader:
    known_extensions = {".yaml", ".yml"}

    def can_load(self, file_path: Path) -> bool:
        return file_path.suffix in self.known_extensions

    def load(self, file_path: Path) -> Dict[str, Any]:
        return io.load_yaml_file(file_path)


class LocalRepoLoader(BaseRepoLoader):
    """Loader for qwikstart task repos stored on the local filesystem."""

    file_loader = YamlFileLoader()

    def __init__(self, path: str):
        self._local_path = Path(path).resolve()
        if self._local_path.is_dir():
            self._local_path = self.spec_path / QWIKSTART_TASK_SPEC_FILE

    @property
    def spec_path(self) -> Path:
        return self._local_path

    def _can_load_spec(self) -> bool:
        return self.spec_path.is_file() and self._can_load_spec_file()

    def _can_load_spec_file(self) -> bool:
        return self.file_loader.can_load(self.spec_path)

    @property
    def task_spec(self) -> Dict[str, Any]:
        if not self._can_load_spec():
            raise RepoLoaderError(f"Cannot load {self.spec_path!r}")
        return self.file_loader.load(self.spec_path)
