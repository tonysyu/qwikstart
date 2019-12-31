from . import fake_filesystem

class TestCase:
    fs: fake_filesystem.FakeFilesystem

    def setUpPyfakefs(self) -> None: ...
