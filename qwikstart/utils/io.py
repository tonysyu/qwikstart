from pathlib import Path
from typing import Any, Dict

import yaml


def load_yaml_file(file_path: Path) -> Dict[str, Any]:
    with file_path.open() as f:
        return yaml.safe_load(f)
