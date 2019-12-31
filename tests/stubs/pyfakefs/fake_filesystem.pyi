from pathlib import Path
from typing import Optional, Union

PathLike = Union[str, Path]


class FakeFilesystem:
    def add_real_directory(
        self,
        source_path: PathLike,
        read_only: bool = True,
        lazy_read: bool = True,
        target_path: Optional[PathLike] = None,
    ) -> None:
        ...

    def create_file(self, file_path, contents: str = "") -> None:
        ...
