from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Optional, cast
from unittest import TestCase

import pytest

from qwikstart.base_context import BaseContext, DictContext
from qwikstart.exceptions import OperationDefinitionError
from qwikstart.operations.base import BaseOperation

from .. import helpers


@dataclass(frozen=True)
class ContextWithDict(BaseContext):
    template_variables: Dict[str, Any] = field(default_factory=dict)


class FakeOperation(BaseOperation[ContextWithDict, DictContext]):
    name: str = "fake-operation"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.run_context: Optional[ContextWithDict] = None

    def run(self, context: ContextWithDict) -> DictContext:
        self.run_context = context
        return asdict(context)


class TestOperationHavingContextWithDict(TestCase):
    def setUp(self) -> None:
        self.execution_context = helpers.get_execution_context()

    def test_default_template_variables(self) -> None:
        operation = FakeOperation()
        output = operation.execute({"execution_context": self.execution_context})
        assert isinstance(operation.run_context, ContextWithDict)
        assert operation.run_context.template_variables == {}
        assert output["template_variables"] == {}

    def test_template_variables_from_run_context(self) -> None:
        operation = FakeOperation()
        template_variables = {"some": "value"}
        output = operation.execute(
            {
                "execution_context": self.execution_context,
                "template_variables": template_variables,
            }
        )
        assert isinstance(operation.run_context, ContextWithDict)
        assert operation.run_context.template_variables == template_variables
        assert output["template_variables"] == template_variables

    def test_mapping_temporarily_remaps_key_during_execution(self) -> None:
        operation = FakeOperation(mapping={"vars": "template_variables"})
        template_variables = {"some": "value"}
        output = operation.execute(
            {"execution_context": self.execution_context, "vars": template_variables}
        )
        # FIXME: Remove cast: mypy appears to think `operation.run_context` is `None`.
        run_context = cast(ContextWithDict, operation.run_context)
        # During exection, `vars` is remapped to `template_variables`:
        assert run_context.template_variables == template_variables
        # On return, `template_variables` is remapped back to `vars`:
        assert output["vars"] == template_variables

    def test_input_mapping(self) -> None:
        operation = FakeOperation(input_mapping={"vars": "template_variables"})
        output = operation.execute(
            {"execution_context": self.execution_context, "vars": {"some": "value"}}
        )
        assert output["template_variables"] == {"some": "value"}

    def test_output_mapping(self) -> None:
        operation = FakeOperation(output_mapping={"template_variables": "output_vars"})
        output = operation.execute(
            {
                "execution_context": self.execution_context,
                "template_variables": {"some": "value"},
            }
        )
        assert output["output_vars"] == {"some": "value"}

    def test_mapping_and_input_mapping_cannot_both_be_defined(self) -> None:
        mapping = {"vars": "template_variables"}
        with pytest.raises(OperationDefinitionError):
            FakeOperation(mapping=mapping, input_mapping=mapping)

    def test_mapping_and_output_mapping_cannot_both_be_defined(self) -> None:
        mapping = {"vars": "template_variables"}
        with pytest.raises(OperationDefinitionError):
            FakeOperation(mapping=mapping, output_mapping=mapping)

    def test_local_context_takes_precedence(self) -> None:
        operation = FakeOperation(
            local_context={"template_variables": {"same-key": "local-context"}}
        )
        output = operation.execute(
            {
                "execution_context": self.execution_context,
                "template_variables": {"same-key": "run-context"},
            }
        )
        assert output["template_variables"] == {"same-key": "local-context"}

    def test_nested_dictionary_merged_from_local_context(self) -> None:
        operation = FakeOperation(local_context={"template_variables": {"b": 2}})
        output = operation.execute(
            {
                "execution_context": self.execution_context,
                "template_variables": {"a": 1},
            }
        )
        assert output["template_variables"] == {"a": 1, "b": 2}
