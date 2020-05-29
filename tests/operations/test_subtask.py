import textwrap
from pathlib import Path
from typing import Any, Dict

import pytest
from pyfakefs.fake_filesystem_unittest import TestCase

from qwikstart.exceptions import OperationError
from qwikstart.operations import subtask

from .. import helpers


class TestSubtask(TestCase):
    def setUp(self) -> None:
        self.setUpPyfakefs()
        self.task_dir = Path("/path/to/task")
        self.subtask_path = self.task_dir / "subdir" / "subtask.yml"

    def test_return_context_from_subtask(self) -> None:
        self.fs.create_file(
            self.subtask_path,
            contents=textwrap.dedent(
                """
                steps:
                    "Define subtask_var":
                        name: define_context
                        context_defs:
                            subtask_var: "Test"
                """
            ),
        )
        output_context = self.execute_subtask()
        assert output_context["subtask_var"] == "Test"

    def test_subcontext_used_to_render_in_subtask(self) -> None:
        self.fs.create_file(
            self.subtask_path,
            contents=textwrap.dedent(
                """
                steps:
                    "Define greeting":
                        name: define_context
                        context_defs:
                            greeting: "Hello, {{ qwikstart.name }}!"
                """
            ),
        )
        subcontext = {"template_variables": {"name": "World"}}
        output_context = self.execute_subtask(subcontext=subcontext)
        assert output_context["greeting"] == "Hello, World!"

    def test_paths_relative_to_subtask_directory(self) -> None:
        subdir = self.subtask_path.parent
        # Note that "greeting.txt" is relative to subtask not task:
        template_path = subdir / "greeting.txt"
        self.fs.create_file(template_path, contents="Hello, World!")
        self.fs.create_file(
            self.subtask_path,
            contents=textwrap.dedent(
                """
                steps:
                    "Copy file":
                        name: add_file
                        template_path: "./greeting.txt"
                """
            ),
        )
        target_path = Path("/path/to/target.txt")
        subcontext = {"template_path": template_path, "target_path": target_path}
        self.execute_subtask(subcontext=subcontext)
        assert helpers.read_file_path(target_path) == "Hello, World!"

    def test_unknown_file_raises(self) -> None:
        with pytest.raises(OperationError):
            self.execute_subtask()

    def execute_subtask(self, **override_context: Any) -> Dict[str, Any]:
        execution_context = helpers.get_execution_context(source_dir=self.task_dir)
        context = {
            "execution_context": execution_context,
            "file_path": self.subtask_path,
            **override_context,
        }
        append_op = subtask.Operation()
        return append_op.execute(context)
