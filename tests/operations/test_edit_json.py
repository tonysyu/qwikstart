import json
from pathlib import Path
from typing import Any, Dict, cast

from pyfakefs.fake_filesystem_unittest import TestCase

from qwikstart.operations import edit_json

from .. import helpers


class TestEditJsonFS(TestCase):
    def setUp(self) -> None:
        self.setUpPyfakefs()
        self.file_path = Path("/path/to/data.json")

    def initialize_json(self, data: Dict[str, Any]) -> None:
        self.fs.create_file(self.file_path, contents=json.dumps(data))

    def edit_json_and_return_parsed(self, merge_data: Dict[str, Any]) -> Dict[str, Any]:
        context = {
            "execution_context": helpers.get_execution_context(),
            "file_path": self.file_path,
            "merge_data": merge_data,
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

    def test_overwrite(self) -> None:
        self.initialize_json({"mutable": 1})
        assert self.edit_json_and_return_parsed({"mutable": 2}) == {"mutable": 2}
