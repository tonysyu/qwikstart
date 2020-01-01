# Ignore pytest typing: see https://github.com/pytest-dev/pytest/issues/3342
import pytest

from qwikstart.exceptions import OperationError
from qwikstart.operations import find_tagged_line

from .. import helpers


class TestFindTaggedLine:
    def test_line_found(self) -> None:
        context = {
            "execution_context": helpers.get_execution_context(),
            "tag": "# qwikstart-INSTALLED_APPS",
            "file_path": helpers.create_mock_file_path(
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

    def test_line_not_found(self) -> None:
        context = {
            "execution_context": helpers.get_execution_context(),
            "tag": "# qwikstart-INSTALLED_APPS",
            "file_path": helpers.create_mock_file_path("File without tag"),
        }
        find_tagged_line_action = find_tagged_line.Operation()
        with pytest.raises(OperationError):
            context = find_tagged_line_action.execute(context)
