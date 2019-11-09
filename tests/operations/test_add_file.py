from typing import Any, Dict, Optional
import jinja2

from qwikstart.operations import add_file
from ..helpers import create_mock_file_path, read_file_path


class TestAddFile:
    def test_file_with_no_variables(self):
        rendered_string = render_template("Fake template content")
        assert rendered_string == "Fake template content"

    def test_file_with_variables(self):
        rendered_string = render_template(
            """Hello, {{name}}!""", template_variables={"name": "World"}
        )
        assert rendered_string == "Hello, World!"


def render_template(
    template_string: str, template_variables: Optional[Dict[str, Any]] = None
):
    """Return rendered string given a template and optional variables."""
    template_variables = template_variables or {}

    output_file = create_mock_file_path("")
    template_name = "test.txt"
    context: add_file.Context = {
        "target_path": output_file,
        "template_name": template_name,
        "template_loader": jinja2.DictLoader,
        "template_loader_args": [{template_name: template_string}],
        "template_variables": template_variables,
    }

    add_file_op = add_file.Operation()
    add_file_op.execute(context)

    return read_file_path(output_file)
