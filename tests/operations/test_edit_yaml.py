import textwrap
from pathlib import Path
from typing import Any, Dict

from pyfakefs.fake_filesystem_unittest import TestCase

from qwikstart.operations import edit_yaml
from qwikstart.utils.io import dump_yaml_string, load_yaml_string

from .. import helpers


class TestEditYamlFS(TestCase):
    def setUp(self) -> None:
        self.setUpPyfakefs()
        self.file_path = Path("/path/to/data.yaml")

    def initialize_yaml(self, data: Dict[str, Any]) -> None:
        self.fs.create_file(self.file_path, contents=dump_yaml_string(data))

    def edit_yaml_and_return_parsed(
        self, merge_data: Dict[str, Any], **override_context: Any,
    ) -> Dict[str, Any]:
        context = {
            "execution_context": helpers.get_execution_context(),
            "file_path": self.file_path,
            "merge_data": merge_data,
            **override_context,
        }
        edit_action = edit_yaml.Operation()
        edit_action.execute(context)
        return load_yaml_string(helpers.read_file_path(self.file_path))

    def test_add_sibling(self) -> None:
        self.initialize_yaml({"one": 1})
        assert self.edit_yaml_and_return_parsed({"two": 2}) == {"one": 1, "two": 2}

    def test_add_child(self) -> None:
        self.initialize_yaml({"parent": {"daughter": "Emily"}})
        assert self.edit_yaml_and_return_parsed({"parent": {"son": "Austin"}}) == {
            "parent": {"daughter": "Emily", "son": "Austin"}
        }

    def test_dry_run(self) -> None:
        self.initialize_yaml({"unchanged": True})
        output_yaml = self.edit_yaml_and_return_parsed(
            {"unchanged": False},
            execution_context=helpers.get_execution_context(dry_run=True),
        )
        assert output_yaml == {"unchanged": True}

    def test_overwrite(self) -> None:
        self.initialize_yaml({"mutable": 1})
        assert self.edit_yaml_and_return_parsed({"mutable": 2}) == {"mutable": 2}

    def test_pretty_printing(self) -> None:
        self.initialize_yaml({"one": 1})
        self.edit_yaml_and_return_parsed({"two": 2})

        assert helpers.read_file_path(self.file_path) == textwrap.dedent(
            """\
            one: 1
            two: 2
            """
        )

    def test_comments_preserved(self) -> None:
        data = load_yaml_string(
            textwrap.dedent(
                """
                parent:
                    # First child
                    child1: Emily
                """
            )
        )
        self.initialize_yaml(data)
        self.edit_yaml_and_return_parsed({"parent": {"child2": "Austin"}})
        assert helpers.read_file_path(self.file_path) == textwrap.dedent(
            """\
            parent:
                # First child
                child1: Emily
                child2: Austin
            """
        )
