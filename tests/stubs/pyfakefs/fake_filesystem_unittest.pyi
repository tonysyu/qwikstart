from typing import Any, List, Optional

from . import fake_filesystem


class TestCase:
    fs: fake_filesystem.FakeFilesystem

    def setUpPyfakefs(self, modules_to_reload: Optional[List[Any]] = None) -> None: ...
