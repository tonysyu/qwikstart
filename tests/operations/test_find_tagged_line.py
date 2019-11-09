# Ignore pytest typing: see https://github.com/pytest-dev/pytest/issues/3342
import pytest  # type: ignore

from qwikstart.operations import OperationError, find_tagged_line
from ..helpers import create_mock_file_path


class TestFindTaggedLine:
    def test_line_found(self):
        context: find_tagged_line.Context = {
            "tag": "# qwikstart-INSTALLED_APPS",
            "file_path": create_mock_file_path(
                """
                    INSTALLED_APPS = [
                        "django.contrib.admin",
                        # qwikstart-INSTALLED_APPS
                    ]
                """
            ),
        }
        find_tagged_line_action = find_tagged_line.Operation()
        context = find_tagged_line_action.execute(context)
        assert context["line"] == 4

    def test_line_not_found(self):
        context: find_tagged_line.Context = {
            "tag": "# qwikstart-INSTALLED_APPS",
            "file_path": create_mock_file_path("File without tag"),
        }
        find_tagged_line_action = find_tagged_line.Operation()
        with pytest.raises(OperationError):
            context = find_tagged_line_action.execute(context)
