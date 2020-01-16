from typing import Any, Dict, Optional

from qwikstart.operations import define_context

from .. import helpers


class TestDefineContext:
    def test_string_value_added_to_context(self) -> None:
        assert self.define_context({"key": "value"}) == {"key": "value"}

    def test_int_value_added_to_context(self) -> None:
        # Test int value to ensure it doesn't cause template rendering to fail.
        assert self.define_context({"key": 42}) == {"key": 42}

    def test_render_variable(self) -> None:
        context_defs = {"target_file": "{{ qwikstart.target_dir }}/file.txt"}
        template_variables = {"target_dir": "/path/to/parent"}
        assert self.define_context(context_defs, template_variables) == {
            "target_file": "/path/to/parent/file.txt"
        }

    def test_render_variable_using_non_rendered_variable_def(self) -> None:
        context_defs = {
            "magic_number": 3,
            "message": "{{ qwikstart.magic_number }} is the magic number",
        }
        assert self.define_context(context_defs) == {
            "magic_number": 3,
            "message": "3 is the magic number",
        }

    def test_render_variable_using_previous_rendered_variable(self) -> None:
        context_defs = {
            "greeting": "Hello {{ qwikstart.name }}!",
            "message": "{{ qwikstart.greeting }} Welcome to qwikstart!",
        }
        template_variables = {"name": "World"}
        assert self.define_context(context_defs, template_variables) == {
            "greeting": "Hello World!",
            "message": "Hello World! Welcome to qwikstart!",
        }

    def define_context(
        self,
        context_defs: Dict[str, Any],
        template_variables: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Return output context from `define_context.Operation`."""
        template_variables = template_variables or {}

        context = define_context.Context(
            execution_context=helpers.get_execution_context(),
            context_defs=context_defs,
            template_variables=template_variables,
        )

        define_context_op = define_context.Operation()
        return define_context_op.run(context)
