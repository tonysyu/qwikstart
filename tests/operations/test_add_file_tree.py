from pathlib import Path
from typing import Any, Dict
from unittest.mock import ANY, Mock, patch

from qwikstart.operations import add_file_tree

from .. import helpers


class TestAddFileTree:
    def test_generator_initialized_and_called(self) -> None:
        template_dir = Path("/path/to/template/dir")
        target_dir = Path("/path/to/target/dir")

        context = {
            "execution_context": helpers.get_execution_context(target_dir=target_dir),
            "template_dir": template_dir,
            "target_dir": target_dir,
            "ignore": [],
        }

        mock_file_generator = self.execute_operation(context)

        # FileTreeGenerator should be initialized:
        mock_file_generator.assert_called_once_with(
            template_dir, target_dir, ANY, ignore_patterns=[]
        )
        # The FileTreeGenerator instance's copy method should be called:
        mock_file_generator.return_value.copy.assert_called_once()

    def test_dry_run(self) -> None:
        target_dir = Path("/path/to/target/dir")
        context = {
            "execution_context": helpers.get_execution_context(
                target_dir=target_dir, dry_run=True
            ),
            "template_dir": Path("/path/to/template/dir"),
            "target_dir": target_dir,
            "ignore": [],
        }

        mock_file_generator = self.execute_operation(context)
        mock_file_generator.assert_not_called()

    def test_help(self) -> None:
        assert (
            add_file_tree.Context.help("ignore") == add_file_tree.CONTEXT_HELP["ignore"]
        )

    def execute_operation(self, context: Dict[str, Any]) -> Mock:
        add_file_tree_op = add_file_tree.Operation()
        with patch.object(add_file_tree, "FileTreeGenerator") as mock_file_generator:
            add_file_tree_op.execute(context)
        return mock_file_generator
