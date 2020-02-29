from pathlib import Path
from typing import Any, Dict

import yaml


def load_yaml_file(file_path: Path) -> Dict[str, Any]:
    with file_path.open() as f:
        return yaml.safe_load(f)


def load_yaml_string(yaml_contents: str) -> Dict[str, Any]:
    # Ignore typing: safe_load can handle strings, but mypy doesn't recognize that.
    return yaml.safe_load(yaml_contents)  # type: ignore
