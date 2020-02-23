import abc
from pathlib import Path
from typing import Any, Dict

from ..exceptions import RepoLoaderError
from ..utils import io
from .core import QWIKSTART_TASK_SPEC_FILE


class BaseRepoLoader(abc.ABC):
    """Base class for loader for qwikstart task repos."""

    @property
    @abc.abstractmethod
    def task_spec(self) -> Dict[str, Any]:
        """Return raw task specification loaded from qwikstart repo."""

    @property
    @abc.abstractmethod
    def repo_path(self) -> Path:
        """Return local path to qwikstart repo."""


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
        self._spec_path = Path(path).resolve()
        if self._spec_path.is_dir():
            self._spec_path = self._spec_path / QWIKSTART_TASK_SPEC_FILE

    @property
    def task_spec(self) -> Dict[str, Any]:
        if not self._can_load_spec():
            raise RepoLoaderError(f"Cannot load {self._spec_path!r}")
        return self.file_loader.load(self._spec_path)

    @property
    def repo_path(self) -> Path:
        """Return local path to qwikstart repo."""
        return self._spec_path.parent

    def _can_load_spec(self) -> bool:
        return self._spec_path.is_file() and self._can_load_spec_file()

    def _can_load_spec_file(self) -> bool:
        return self.file_loader.can_load(self._spec_path)
