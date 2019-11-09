from textwrap import dedent

from qwikstart.operations import find_tagged_line, inject_text
from ..helpers import create_mock_file_path, read_file_path


class TestFindAndInject:
    def test_inject_line_at_tag(self):
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

        context["text"] = '"my.app",'
        inject_action = inject_text.Operation()
        context = inject_action.execute(context)

        assert read_file_path(context["file_path"]) == dedent(
            """
                INSTALLED_APPS = [
                    "django.contrib.admin",
                    # qwikstart-INSTALLED_APPS
                    "my.app",
                ]
            """
        )
