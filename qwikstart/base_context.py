from dataclasses import dataclass
from pathlib import Path

import jinja2
from typing_extensions import TypedDict


@dataclass(frozen=True)
class ExecutionContext:

    #: Source directory defining qwikstart task.
    #: Templates and other data files are relative to this location.
    source_dir: Path

    #: Target directory for qwikstart modifications.
    #: In practice, this will be set to the working directory by the CLI.
    target_dir: Path

    def get_template_loader(self) -> jinja2.BaseLoader:
        return jinja2.FileSystemLoader("/")


class BaseContext(TypedDict):
    execution_context: ExecutionContext
