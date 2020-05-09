from pathlib import Path
from typing import Any, Dict

import pytest
from pyfakefs.fake_filesystem_unittest import TestCase

from qwikstart.exceptions import OperationError
from qwikstart.operations import context_from_regex
from qwikstart.utils import clean_multiline

from .. import helpers


class TestDefineContext(TestCase):
    def setUp(self) -> None:
        self.setUpPyfakefs()

    def test_single_value(self) -> None:
        text = "PROJECT = 'myproject'"
        regex = r"^PROJECT = \'(?P<project>\w+)\'"
        assert self.context_from_regex(regex, text) == {"project": "myproject"}

    def test_default_to_multiline_regex(self) -> None:
        # Ensure MULTILINE flag by default caret only matches the start of the
        # entire text, not the start of a line.
        text = clean_multiline(
            """
            # Some header text
            PROJECT = 'myproject'
            """
        )
        regex = r"^PROJECT = \'(?P<project>\w+)\'"
        assert self.context_from_regex(regex, text) == {"project": "myproject"}

    def test_error_if_match_not_found(self) -> None:
        regex = r"^PROJECT = \'(?P<project>\w+)\'"
        with pytest.raises(OperationError):
            self.context_from_regex(regex, "does not match regex")

    def test_error_if_capture_group_not_named(self) -> None:
        text = "PROJECT = 'myproject'"
        regex = r"^PROJECT = \'(\w+)\'"
        with pytest.raises(OperationError):
            self.context_from_regex(regex, text)

    def test_multiple_matches(self) -> None:
        text = clean_multiline(
            """
            PROJECT = 'myproject'
            URL = 'https://myproject.io'
            """
        )
        regex = r"(^PROJECT = \'(?P<project>\w+)\'|^URL = \'(?P<url>[^']+)\')"
        assert self.context_from_regex(regex, text) == {
            "project": "myproject",
            "url": "https://myproject.io",
        }

    def context_from_regex(self, regex: str, text: str) -> Dict[str, Any]:
        """Return output context from `context_from_regex.Operation`."""
        file_path = Path("target_file.txt")
        self.fs.create_file(file_path, contents=text)
        context = context_from_regex.Context(
            execution_context=helpers.get_execution_context(),
            regex=regex,
            file_path=file_path,
        )

        op = context_from_regex.Operation()
        return op.run(context)
