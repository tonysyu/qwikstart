from pathlib import Path
from typing import Any, Dict, Optional

from pyfakefs.fake_filesystem_unittest import TestCase  # type: ignore

from qwikstart.operations import add_file

from .. import helpers


class TestAddFile(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_no_variables(self):
        rendered_string = self.render_template("Fake template content")
        assert rendered_string == "Fake template content"

    def test_variables(self):
        rendered_string = self.render_template(
            """Hello, {{ qwikstart.name }}!""",
            template_variables={"name": "World"},
        )
        assert rendered_string == "Hello, World!"

    def test_file_system_template(self):
        execution_context = helpers.get_execution_context(
            source_dir=helpers.TEMPLATES_DIR
        )
        self.fs.add_real_directory(helpers.TEMPLATES_DIR)

        output_file = Path("output.txt")
        context: add_file.Context = {
            "execution_context": execution_context,
            "target_path": output_file,
            "template_path": "hello_world.txt",
            "template_variables": {"name": "World"},
        }

        add_file_op = add_file.Operation()
        add_file_op.execute(context)
        assert helpers.read_file_path(output_file) == "Hello, World!"

    def render_template(
        self,
        template_string: str,
        template_variables: Optional[Dict[str, Any]] = None,
    ):
        """Return rendered string given a template and optional variables."""
        template_variables = template_variables or {}
        source_dir = Path("/source")

        template_path = "test.txt"
        self.fs.create_file(source_dir / "test.txt", contents=template_string)

        output_file = Path("output.txt")

        context = {
            "execution_context": helpers.get_execution_context(
                source_dir=source_dir
            ),
            "target_path": output_file,
            "template_path": template_path,
            "template_variables": template_variables,
        }

        add_file_op = add_file.Operation()
        add_file_op.execute(context)

        return helpers.read_file_path(output_file)
