from typing import Any, Dict, Optional

import jinja2

from ..base_context import BaseContext

DEFAULT_TEMPLATE_VARIABLE_PREFIX = "qwikstart"


class TemplateRenderer:
    def __init__(
        self,
        template_loader: jinja2.BaseLoader,
        template_variables: Optional[Dict[str, Any]] = None,
        template_variable_prefix: Optional[str] = None,
    ):
        self._env = jinja2.Environment(
            loader=template_loader, undefined=jinja2.StrictUndefined
        )
        self.template_variables = template_variables or {}
        self.template_variable_prefix = (
            template_variable_prefix or DEFAULT_TEMPLATE_VARIABLE_PREFIX
        )

    def get_template(self, path: str):
        return self._env.get_template(path)

    def render(self, template_path: str):
        template = self.get_template(template_path)
        return template.render(
            {self.template_variable_prefix: self.template_variables}
        )

    @classmethod
    def from_context(cls, context: BaseContext):
        execution_context = context["execution_context"]
        return cls(
            template_loader=execution_context.get_template_loader(),
            template_variables=context.get("template_variables"),
            template_variable_prefix=context.get("template_variable_prefix"),
        )
