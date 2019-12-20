import os
import shutil
from pathlib import Path

from binaryornot.check import is_binary

from .core import ensure_path
from .templates import TemplateRenderer


def render_file_tree(
    source_dir: Path, target_dir: Path, renderer: TemplateRenderer
):
    if not target_dir.exists():
        target_dir.mkdir()
    source_dir = source_dir.resolve()

    # Keep a mapping between source directories and target directories.
    # This simplifies resolution of rendered directory names.
    directory_mapping = {str(source_dir): target_dir}

    for source_root, dirs, files in os.walk(source_dir):
        source_root = Path(source_root)
        target_root = directory_mapping[str(source_root)]

        for filename in files:
            source_path = Path(source_root, filename)

            # Render filename since it may be a template:
            target_filename = renderer.render_string(filename)
            target_path = target_root / target_filename

            if is_binary(str(source_path)):
                shutil.copy(source_path, target_path)
            else:
                with target_path.open("w") as f:
                    f.write(renderer.render(str(source_path)))

        for source_subdir in dirs:
            target_subdir = renderer.render_string(source_subdir)
            target_path = target_root / target_subdir

            directory_mapping[str(source_root / source_subdir)] = target_path

            target_path.mkdir(exist_ok=True)
