import logging
import os
import shutil
from pathlib import Path

from binaryornot.check import is_binary

from .core import ensure_path
from .templates import TemplateRenderer

logger = logging.getLogger(__name__)


class FileTreeGenerator:
    def __init__(
        self, source_dir: Path, target_dir: Path, renderer: TemplateRenderer
    ):
        if not target_dir.exists():
            target_dir.mkdir()

        self.target_dir = target_dir
        self.source_dir = source_dir.resolve()
        self.renderer = renderer

        # Keep a mapping between source directories and target directories.
        # This simplifies resolution of rendered directory names.
        self._directory_mapping = {str(source_dir): target_dir}

    def copy(self):
        for source_root, dirs, files in os.walk(self.source_dir):
            source_root = Path(source_root)
            target_root = self._directory_mapping[str(source_root)]

            for filename in files:
                self._copy_file(filename, source_root, target_root)

            for subdir in dirs:
                self._ensure_dir_exists(subdir, source_root, target_root)

    def _copy_file(self, source_filename, source_root, target_root):
        # Render source_filename since it may be a template:
        tgt_path = target_root / self.renderer.render_string(source_filename)

        src_path = Path(source_root, source_filename)
        if is_binary(str(src_path)):
            shutil.copy(src_path, tgt_path)
            logger.debug(f"Copied binary file from {src_path} to {tgt_path}")
        else:
            with tgt_path.open("w") as f:
                f.write(self.renderer.render(str(src_path)))
            logger.debug(f"Rendered template from {src_path} to {tgt_path}")

    def _ensure_dir_exists(self, source_subdir, source_root, target_root):
        """Create subdirectory in target directory ."""
        # Render source_subdir since it may be a template:
        tgt_path = target_root / self.renderer.render_string(source_subdir)

        # Whenever a new directory is traversed, add to directory mapping.
        src_path = source_root / source_subdir
        self._directory_mapping[str(src_path)] = tgt_path

        tgt_path.mkdir(exist_ok=True)
        logger.debug(f"Created directory {tgt_path}")
