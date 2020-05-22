import logging
import subprocess
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Union

from ..base_context import BaseContext
from ..utils import text_utils
from ..utils.templates import DEFAULT_TEMPLATE_VARIABLE_PREFIX, TemplateRenderer
from .base import BaseOperation
from .utils import TEMPLATE_VARIABLE_PREFIX_HELP

__all__ = ["Operation"]

logger = logging.getLogger(__name__)


OUTPUT_PROCESSORS: Dict[str, Callable[[str], str]] = {
    "noop": text_utils.noop,
    "strip": str.strip,
}

CONTEXT_HELP = {
    "cmd": "Command or list of command arguments to run.",
    "echo_output": "Toggle display of output to terminal.",
    "output_var": "Variable name in which output is stored.",
    "output_processor": f"Processor to run on output {OUTPUT_PROCESSORS.keys()}",
    "ignore_error_code": "Toggle check for error code returned by shell operation.",
    "template_variable_prefix": TEMPLATE_VARIABLE_PREFIX_HELP,
}


@dataclass(frozen=True)
class Context(BaseContext):
    cmd: Union[List[str], str]
    echo_output: bool = True
    ignore_error_code: bool = False
    output_processor: str = "strip"
    output_var: Optional[str] = None
    template_variables: Dict[str, Any] = field(default_factory=dict)
    template_variable_prefix: str = DEFAULT_TEMPLATE_VARIABLE_PREFIX

    @classmethod
    def help(cls, field_name: str) -> Optional[str]:
        return CONTEXT_HELP.get(field_name)


class Operation(BaseOperation[Context, Dict[str, Any]]):
    """Operation to run an arbitrary shell command.

    See https://qwikstart.readthedocs.io/en/latest/operations/shell.html
    """

    name: str = "shell"

    def run(self, context: Context) -> Dict[str, Any]:
        renderer = TemplateRenderer.from_context(context)
        if isinstance(context.cmd, list):
            cmd = [renderer.render_string(arg) for arg in context.cmd]
        else:
            # FIXME: Ignore mypy complaint caused by `cmd` assignment to list above.
            cmd = renderer.render_string(context.cmd)  # type: ignore

        logger.info(f"Running command: {cmd}")

        if context.execution_context.dry_run:
            logger.warning(
                "Running with `--dry-run` option, but shell operation will run "
                "regardless of whether operation modifies filesystem."
            )

        response = subprocess.run(
            cmd,
            shell=isinstance(cmd, str),
            # FIXME: Once Python 3.6 support is dropped use capture_output=True
            # instead of stdout/stderr and text instead of universal_newlines
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        if not context.ignore_error_code:
            response.check_returncode()

        process_output = OUTPUT_PROCESSORS[context.output_processor]
        output = process_output(response.stdout)

        if context.echo_output:
            logger.info(output)

        return {context.output_var: output} if context.output_var else {}
