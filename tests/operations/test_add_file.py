from typing import Any, Dict, Optional

import jinja2

from qwikstart.operations import add_file

from .. import helpers


class TestAddFile:
    def test_no_variables(self):
        rendered_string = render_template("Fake template content")
        assert rendered_string == "Fake template content"

    def test_variables(self):
        rendered_string = render_template(
            """Hello, {{name}}!""", template_variables={"name": "World"}
        )
        assert rendered_string == "Hello, World!"

    def test_file_system_template(self):
        output_file = helpers.create_mock_file_path("")
        template_loader = jinja2.FileSystemLoader(helpers.TEMPLATES_DIR)
        execution_context = helpers.get_execution_context(template_loader)
        context: add_file.Context = {
            "execution_context": execution_context,
            "target_path": output_file,
            "template_path": "hello_world.txt",
            "template_variables": {"name": "World"},
        }

        add_file_op = add_file.Operation()
        add_file_op.execute(context)
        helpers.read_file_path(output_file) == "Hello, World!"


def render_template(
    template_string: str, template_variables: Optional[Dict[str, Any]] = None
):
    """Return rendered string given a template and optional variables."""
    template_variables = template_variables or {}

    output_file = helpers.create_mock_file_path("")
    template_path = "test.txt"
    template_loader = jinja2.DictLoader({template_path: template_string})
    context: add_file.Context = {
        "execution_context": helpers.get_execution_context(template_loader),
        "target_path": output_file,
        "template_path": template_path,
        "template_variables": template_variables,
    }

    add_file_op = add_file.Operation()
    add_file_op.execute(context)

    return helpers.read_file_path(output_file)
