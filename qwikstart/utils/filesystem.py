import os
from pathlib import Path

from .core import ensure_path
from .templates import TemplateRenderer


def render_file_tree(
    source_dir: Path, target_dir: Path, renderer: TemplateRenderer
):
    for root, dirs, files in os.walk(source_dir.resolve()):
        for filename in files:
            source_path = Path(root, filename)

            target_filename = renderer.render_string(filename)
            with Path(target_dir, target_filename).open("w") as f:
                f.write(renderer.render(str(source_path)))

        for dirname in dirs:
            target_dirname = renderer.render_string(dirname)
            target_path = Path(target_dir, target_dirname)
            target_path.mkdir(exist_ok=True)
            render_file_tree(Path(source_dir, dirname), target_path, renderer)
