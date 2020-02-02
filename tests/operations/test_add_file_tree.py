from pathlib import Path
from unittest.mock import ANY, patch

from qwikstart.operations import add_file_tree

from .. import helpers


class TestAddFileTree:
    def test_generator_initialized_and_called(self) -> None:
        add_file_tree_op = add_file_tree.Operation()
        template_dir = Path("/path/to/template/dir")
        target_dir = Path("/path/to/target/dir")

        context = {
            "execution_context": helpers.get_execution_context(target_dir=target_dir),
            "template_dir": template_dir,
            "target_dir": target_dir,
            "ignore": [],
        }

        with patch.object(add_file_tree, "FileTreeGenerator") as mock_gen:
            add_file_tree_op.execute(context)

        # FileTreeGenerator should be initialized:
        mock_gen.assert_called_once_with(
            template_dir, target_dir, ANY, ignore_patterns=[]
        )
        # The FileTreeGenerator instance's copy method should be called:
        mock_gen.return_value.copy.assert_called_once()

    def test_help(self) -> None:
        assert (
            add_file_tree.Context.help("ignore") == add_file_tree.CONTEXT_HELP["ignore"]
        )
