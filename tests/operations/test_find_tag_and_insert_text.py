from textwrap import dedent

from qwikstart.operations import find_tag_and_insert_text

from ..helpers import create_mock_file_path, get_execution_context, read_file_path


class TestFindTagAndInsertText:
    def test_success(self) -> None:
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
        operation = find_tag_and_insert_text.Operation()
        context = operation.execute(context)
        assert read_file_path(context["file_path"]) == dedent(
            """
                INSTALLED_APPS = [
                    "django.contrib.admin",
                    # qwikstart-INSTALLED_APPS
                    "my.app",
                ]
            """
        )

    def test_no_matched_indent(self) -> None:
        context = {
            "execution_context": get_execution_context(),
            "tag": "# qwikstart-tag",
            "file_path": create_mock_file_path(
                """
                    def greetings():
                        pass
                        # qwikstart-tag
                """
            ),
            "text": "print('Done')",
            "match_indent": False,
        }
        operation = find_tag_and_insert_text.Operation()
        context = operation.execute(context)
        assert read_file_path(context["file_path"]) == dedent(
            """
                    def greetings():
                        pass
                        # qwikstart-tag
                    print('Done')
            """
        )
