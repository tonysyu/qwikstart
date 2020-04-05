import json
import textwrap
from pathlib import Path
from typing import Any, Dict, Optional, cast

from pyfakefs.fake_filesystem_unittest import TestCase

from qwikstart.operations import edit_json

from .. import helpers


class TestEditJsonFS(TestCase):
    def setUp(self) -> None:
        self.setUpPyfakefs()
        self.file_path = Path("/path/to/data.json")

    def initialize_json(self, data: Dict[str, Any]) -> None:
        self.fs.create_file(self.file_path, contents=json.dumps(data))

    def edit_json_and_return_parsed(
        self,
        merge_data: Dict[str, Any],
        override_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        override_context = override_context or {}
        context = {
            "execution_context": helpers.get_execution_context(),
            "file_path": self.file_path,
            "merge_data": merge_data,
            **override_context,
        }
        edit_action = edit_json.Operation()
        edit_action.execute(context)
        data = json.loads(helpers.read_file_path(self.file_path))
        return cast(Dict[str, Any], data)

    def test_add_sibling(self) -> None:
        self.initialize_json({"one": 1})
        assert self.edit_json_and_return_parsed({"two": 2}) == {"one": 1, "two": 2}

    def test_add_child(self) -> None:
        self.initialize_json({"parent": {"daughter": "Emily"}})
        assert self.edit_json_and_return_parsed({"parent": {"son": "Austin"}}) == {
            "parent": {"daughter": "Emily", "son": "Austin"}
        }

    def test_dry_run(self) -> None:
        self.initialize_json({"unchanged": True})
        output_json = self.edit_json_and_return_parsed(
            {"unchanged": False},
            override_context={
                "execution_context": helpers.get_execution_context(dry_run=True)
            },
        )
        assert output_json == {"unchanged": True}

    def test_overwrite(self) -> None:
        self.initialize_json({"mutable": 1})
        assert self.edit_json_and_return_parsed({"mutable": 2}) == {"mutable": 2}

    def test_pretty_printing(self) -> None:
        self.initialize_json({"one": 1})
        self.edit_json_and_return_parsed({"two": 2})

        assert helpers.read_file_path(self.file_path) == textwrap.dedent(
            """\
            {
                "one": 1,
                "two": 2
            }"""
        )
