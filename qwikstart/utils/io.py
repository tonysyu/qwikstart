from io import StringIO
from pathlib import Path
from typing import Any, Dict, cast

from ruamel.yaml import YAML

_yaml = YAML()
# Use 4-space indent for mappings and list-bullet offsets and
# 6-space indent (from beginning) for list-item text.
# `sequence = offset + 2` to provide space for bullet and single space`.
# See https://yaml.readthedocs.io/en/latest/detail.html#indentation-of-block-sequences
_yaml.indent(mapping=4, sequence=6, offset=4)


def read_file_contents(file_path: Path) -> str:
    with file_path.open() as f:
        return f.read()


def load_yaml_file(file_path: Path) -> Dict[str, Any]:
    with file_path.open() as f:
        return cast(Dict[str, Any], _yaml.load(f))


def load_yaml_string(yaml_contents: str) -> Dict[str, Any]:
    # Ignore typing: load can handle strings, but mypy doesn't recognize that.
    return _yaml.load(yaml_contents)  # type: ignore


def dump_yaml_string(data: Dict[str, Any]) -> str:
    """Return yaml string representation of data."""
    string_buffer = StringIO()
    _yaml.dump(data, string_buffer)
    return string_buffer.getvalue()


def dump_yaml_file(data: Dict[str, Any], file_path: Path) -> None:
    with file_path.open("w") as f:
        _yaml.dump(data, f)
