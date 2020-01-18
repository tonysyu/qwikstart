from pathlib import Path
from typing import Any, Callable, Dict, Optional, Type, TypeVar

import jinja2
from typing_extensions import Protocol

from ..base_context import ExecutionContext
from .core import ensure_path, resolve_path

DEFAULT_TEMPLATE_VARIABLE_PREFIX = "qwikstart"
TEMPLATE_VARIABLE_META_PREFIX = "_meta_"
TRenderer = TypeVar("TRenderer", bound="TemplateRenderer")


class TemplateContext(Protocol):
    @property
    def execution_context(self) -> ExecutionContext:
        pass

    @property
    def template_variables(self) -> Dict[str, Any]:
        pass

    @property
    def template_variable_prefix(self) -> str:
        pass


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

    def get_template(self, path_str: str) -> jinja2.Template:
        path = Path(path_str)
        if not path.is_absolute():
            path = self.source_dir / path
        return self._env.get_template(str(path.resolve()))

    def render(self, template_path: str) -> str:
        template = self.get_template(template_path)
        return template.render(self._template_context)

    def render_string(self, string: str) -> str:
        template = self._env.from_string(string)
        return template.render(self._template_context)

    def add_template_variable(self, key: str, value: Any) -> None:
        self.template_variables[key] = value

    def update_template_variables(self, kwargs: Any) -> None:
        self.template_variables.update(kwargs)

    def add_template_filters(self, **kwargs: Callable[..., str]) -> None:
        for name, filter_function in kwargs.items():
            self._env.filters[name] = filter_function

    @classmethod
    def from_context(cls: Type[TRenderer], context: TemplateContext) -> TRenderer:
        execution_context = context.execution_context
        meta_variables = {
            TEMPLATE_VARIABLE_META_PREFIX: {
                "source_dir": resolve_path(execution_context.source_dir),
                "target_dir": resolve_path(execution_context.target_dir),
            }
        }
        return cls(
            template_loader=execution_context.get_template_loader(),
            template_variables={**meta_variables, **context.template_variables},
            template_variable_prefix=context.template_variable_prefix,
            source_dir=execution_context.source_dir,
        )
