import io
from contextlib import contextmanager
from pathlib import Path
from textwrap import dedent
from unittest.mock import Mock

import pytest

from qwikstart.operations import OperationError, find_tagged_line


def create_mock_file_path(string_data):
    string_buffer = io.StringIO(string_data)

    @contextmanager
    def open_buffer(*args, **kwargs):
        string_buffer.seek(0)
        yield string_buffer

    mock_file_path = Mock(spec=Path)
    mock_file_path.open.side_effect = open_buffer
    return mock_file_path


class TestFindTaggedLine:
    def test_line_found(self):
        context: find_tagged_line.Context = {
            "tag": "# qwikstart-INSTALLED_APPS",
            "file_path": create_mock_file_path(
                dedent(
                    """
                        INSTALLED_APPS = [
                            "django.contrib.admin",
                            # qwikstart-INSTALLED_APPS
                        ]
                    """
                )
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
