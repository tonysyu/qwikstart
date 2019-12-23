from pathlib import Path
from unittest.mock import ANY, patch

from qwikstart.operations import add_file_tree

from .. import helpers


class TestAddFileTree:
    def test_generator_initialized_and_called(self):
        add_file_tree_op = add_file_tree.Operation()
        template_dir = Path("/path/to/template/dir")
        target_dir = Path("/path/to/target/dir")

        context: add_file_tree.Context = {
            "execution_context": helpers.get_execution_context(
                target_dir=target_dir
            ),
            "template_dir": template_dir,
            "target_dir": target_dir,
        }

        with patch.object(add_file_tree, "FileTreeGenerator") as mock_gen:
            add_file_tree_op.execute(context)

        # FileTreeGenerator should be initialized:
        mock_gen.assert_called_once_with(template_dir, target_dir, ANY)
        # The FileTreeGenerator instance's copy method should be called:
        mock_gen.return_value.copy.assert_called_once()
