from dataclasses import dataclass
from pathlib import Path

import jinja2
from typing_extensions import TypedDict


@dataclass(frozen=True)
class BaseExecutionContext:

    #: Source directory defining qwikstart task.
    #: Templates and other data files are relative to this location.
    source_dir: Path

    #: Target directory for qwikstart modifications.
    #: In practice, this will be set to the working directory by the CLI.
    target_dir: Path


@dataclass(frozen=True)
class ExecutionContext(BaseExecutionContext):

    #: Source directory defining qwikstart task.
    #: Templates and other data files are relative to this location.
    source_dir: Path

    #: Target directory for qwikstart modifications.
    #: In practice, this will be set to the working directory by the CLI.
    target_dir: Path

    #: Template loader used to resolve file templates.
    template_loader: jinja2.BaseLoader


@dataclass(frozen=True)
class DefaultExecutionContext(BaseExecutionContext):
    @property
    def template_loader(self) -> jinja2.BaseLoader:
        return jinja2.FileSystemLoader(self.source_dir)


class BaseContext(TypedDict):
    execution_context: ExecutionContext
