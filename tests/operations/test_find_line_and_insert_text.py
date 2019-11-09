from textwrap import dedent

from qwikstart.operations import find_tagged_line, insert_text
from ..helpers import create_mock_file_path, read_file_path


class TestFindAndInsert:
    def test_insert_line_at_tag(self):
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

        context["text"] = '"my.app",'
        insert_action = insert_text.Operation()
        context = insert_action.execute(context)

        assert read_file_path(context["file_path"]) == dedent(
            """
                INSTALLED_APPS = [
                    "django.contrib.admin",
                    # qwikstart-INSTALLED_APPS
                    "my.app",
                ]
            """
        )
