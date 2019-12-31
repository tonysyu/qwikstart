from textwrap import dedent

from qwikstart.operations import find_tagged_line, insert_text
from qwikstart.tasks import Task

from .helpers import create_mock_file_path, get_execution_context, read_file_path


class TestTask:
    def test_find_tagged_line_and_insert_text(self) -> None:
        context = {
            "execution_context": get_execution_context(),
            "tag": "# qwikstart-INSTALLED_APPS",
            "file_path": create_mock_file_path(
                """
                    INSTALLED_APPS = [
                        "django.contrib.admin",
                        # qwikstart-INSTALLED_APPS
                    ]
                """
            ),
            "text": '"my.app",',
        }
        task = Task(
            context=context,
            operations=[find_tagged_line.Operation(), insert_text.Operation()],
        )
        context = task.execute()
        assert read_file_path(context["file_path"]) == dedent(
            """
                INSTALLED_APPS = [
                    "django.contrib.admin",
                    # qwikstart-INSTALLED_APPS
                    "my.app",
                ]
            """
        )
