from typing import Any
from unittest import TestCase
from unittest.mock import Mock, patch

import pytest

from qwikstart.base_context import DictContext
from qwikstart.operations import base

from .. import helpers


class ErrorOperation(base.BaseOperation[helpers.ContextWithDict, DictContext]):
    name: str = "error-operation"

    def run(self, context: helpers.ContextWithDict) -> DictContext:
        raise Exception("Error raised for testing purposes")


class TestOperationConfig:
    # FIXME: Add mypy stub for pytest parametrize
    @pytest.mark.parametrize(  # type: ignore
        "attr_name,value", base.DEFAULT_OPERATION_CONFIG.items()
    )
    def test_update_all_defaults(self, attr_name: str, value: Any) -> None:
        opconfig = base.OperationConfig.create()
        assert getattr(opconfig, attr_name) == value

    def test_final_config_takes_precedence(self) -> None:
        opconfig = base.OperationConfig.from_config_dicts(
            {"display_description": False}, {"display_description": True}
        )
        assert opconfig.display_description is True

        opconfig = base.OperationConfig.from_config_dicts(
            {"display_description": True}, {"display_description": False}
        )
        assert opconfig.display_description is False


class TestBaseOperation(TestCase):
    def setUp(self) -> None:
        self.execution_context = helpers.get_execution_context()

    def test_default_template_variables(self) -> None:
        operation = helpers.FakeOperation()
        output = operation.execute({"execution_context": self.execution_context})
        assert isinstance(operation.run_context, helpers.ContextWithDict)
        assert operation.run_context.template_variables == {}
        assert output["template_variables"] == {}

    def test_template_variables_from_run_context(self) -> None:
        operation = helpers.FakeOperation()
        template_variables = {"some": "value"}
        output = operation.execute(
            {
                "execution_context": self.execution_context,
                "template_variables": template_variables,
            }
        )
        assert isinstance(operation.run_context, helpers.ContextWithDict)
        assert operation.run_context.template_variables == template_variables
        assert output["template_variables"] == template_variables

    def test_input_mapping(self) -> None:
        opconfig = dict(input_mapping={"vars": "template_variables"})
        operation = helpers.FakeOperation(opconfig=opconfig)
        output = operation.execute(
            {"execution_context": self.execution_context, "vars": {"some": "value"}}
        )
        assert output["template_variables"] == {"some": "value"}

    def test_output_mapping(self) -> None:
        opconfig = dict(output_mapping={"template_variables": "output_vars"})
        operation = helpers.FakeOperation(opconfig=opconfig)
        output = operation.execute(
            {
                "execution_context": self.execution_context,
                "template_variables": {"some": "value"},
            }
        )
        assert output["output_vars"] == {"some": "value"}

    def test_input_namespace(self) -> None:
        opconfig = dict(input_namespace="my-namespace")
        operation = helpers.FakeOperation(opconfig=opconfig)
        context = {
            "execution_context": self.execution_context,
            "my-namespace": {"template_variables": {"some": "value"}},
        }
        output = operation.execute(context)
        assert output["template_variables"] == {"some": "value"}

    def test_output_namespace(self) -> None:
        opconfig = dict(output_namespace="my-namespace")
        operation = helpers.FakeOperation(opconfig=opconfig)
        output = operation.execute(
            {
                "execution_context": self.execution_context,
                "template_variables": {"some": "value"},
            }
        )
        assert output["my-namespace"]["template_variables"] == {"some": "value"}

    def test_local_context_takes_precedence(self) -> None:
        operation = helpers.FakeOperation(
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
        operation = helpers.FakeOperation(
            local_context={"template_variables": {"b": 2}}
        )
        output = operation.execute(
            {
                "execution_context": self.execution_context,
                "template_variables": {"a": 1},
            }
        )
        assert output["template_variables"] == {"a": 1, "b": 2}

    def test_repr(self) -> None:
        operation = helpers.FakeOperation(description="Test Op")
        args = (
            "local_context={}, "
            f"opconfig={base.OperationConfig.create()}, "
            "description=Test Op"
        )
        assert repr(operation) == f"tests.helpers.FakeOperation({args})"

    @patch.object(base, "logger")
    def test_log_success_if_description_defined(self, logger: Mock) -> None:
        operation = helpers.FakeOperation(description="Step 1")
        operation.execute({"execution_context": self.execution_context})
        logger.info.assert_called_once_with(f"Step 1: {base.SUCCESS_MARK}")

    @patch.object(base, "logger")
    def test_log_error_if_description_defined(self, logger: Mock) -> None:
        operation = ErrorOperation(description="Step 1")
        with pytest.raises(Exception):
            operation.execute({"execution_context": self.execution_context})
        logger.error.assert_called_once_with(f"Step 1: {base.FAILURE_MARK}")

    @patch.object(base, "logger")
    def test_log_success_not_called_without_description(self, logger: Mock) -> None:
        helpers.FakeOperation().execute({"execution_context": self.execution_context})
        logger.info.assert_not_called()

    @patch.object(base, "logger")
    def test_log_error_not_called_without_description(self, logger: Mock) -> None:
        with pytest.raises(Exception):
            ErrorOperation().execute({"execution_context": self.execution_context})
        logger.error.assert_not_called()
