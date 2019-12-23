import os
from pathlib import Path
from typing import Any, Dict, Optional

import jinja2

from ..base_context import BaseContext
from .core import ensure_path

DEFAULT_TEMPLATE_VARIABLE_PREFIX = "qwikstart"


class TemplateRenderer:
    def __init__(
        self,
        template_loader: jinja2.BaseLoader,
        template_variables: Optional[Dict[str, Any]] = None,
        template_variable_prefix: Optional[str] = None,
        source_dir: Optional[Path] = None,
    ):
        self._env = jinja2.Environment(
            loader=template_loader, undefined=jinja2.StrictUndefined
        )
        self.template_variables = template_variables or {}
        self.template_variable_prefix = (
            template_variable_prefix or DEFAULT_TEMPLATE_VARIABLE_PREFIX
        )
        self._template_context = {
            self.template_variable_prefix: self.template_variables
        }
        self.source_dir = ensure_path(source_dir or Path("."))

    def get_template(self, path: str) -> jinja2.Template:
        if not os.path.isabs(path):
            path = str(self.source_dir / path)
        return self._env.get_template(path)

    def render(self, template_path: str) -> str:
        template = self.get_template(template_path)
        return template.render(self._template_context)

    def render_string(self, string: str) -> str:
        template = self._env.from_string(string)
        return template.render(self._template_context)

    @classmethod
    def from_context(cls, context: BaseContext):
        execution_context = context["execution_context"]
        return cls(
            template_loader=execution_context.get_template_loader(),
            template_variables=context.get("template_variables"),
            template_variable_prefix=context.get("template_variable_prefix"),
            source_dir=execution_context.source_dir,
        )
