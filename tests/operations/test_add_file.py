import os
from pathlib import Path
from typing import Any, Dict, Optional

from pyfakefs.fake_filesystem_unittest import TestCase

from qwikstart.operations import add_file

from .. import helpers


class TestAddFile(TestCase):
    def setUp(self) -> None:
        self.setUpPyfakefs()

    def test_no_variables(self) -> None:
        template_path = self.create_template("Fake template content")
        output_path = self.render_template(template_path)
        assert helpers.read_file_path(output_path) == "Fake template content"

    def test_dry_run(self) -> None:
        template_path = self.create_template("Fake template content")
        output_path = self.render_template(
            template_path,
            execution_context=helpers.get_execution_context(dry_run=True),
        )
        assert not output_path.exists()

    def test_variables(self) -> None:
        template_path = self.create_template("""Hello, {{ qwikstart.name }}!""")
        output_path = self.render_template(
            template_path, template_variables={"name": "World"}
        )
        assert helpers.read_file_path(output_path) == "Hello, World!"

    def test_real_template_file(self) -> None:
        # Configure execution and pyfakefs to use real templates directory:
        execution_context = helpers.get_execution_context(
            source_dir=helpers.TEMPLATES_DIR
        )
        self.fs.add_real_directory(helpers.TEMPLATES_DIR)

        output_file = Path("output.txt")
        context = {
            "execution_context": execution_context,
            "target_path": output_file,
            "template_path": "hello_world.txt",
            "template_variables": {"name": "World"},
        }

        add_file_op = add_file.Operation()
        add_file_op.execute(context)
        assert helpers.read_file_path(output_file) == "Hello, World!\n"

    def test_copy_file_permissions(self) -> None:
        template_path = self.create_template("Hello")
        os.chmod(template_path, 0o777)
        output_path = self.render_template(template_path)
        assert helpers.filemode(output_path) == 0o777

    def create_template(self, template_string: str) -> Path:
        path = Path("/source/test.txt")
        self.fs.create_file(path, contents=template_string)
        return path

    def render_template(
        self,
        template_path: Path,
        template_variables: Optional[Dict[str, Any]] = None,
        **override_context: Any,
    ) -> Path:
        template_variables = template_variables or {}
        output_file = Path("output.txt")
        context = {
            "execution_context": helpers.get_execution_context(),
            "target_path": output_file,
            "template_path": str(template_path),
            "template_variables": template_variables,
            **override_context,
        }

        add_file_op = add_file.Operation()
        add_file_op.execute(context)

        return output_file
