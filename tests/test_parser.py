from typing import List
from unittest.mock import ANY, Mock, patch

import pytest

from qwikstart import parser
from qwikstart.exceptions import ObsoleteError, TaskParserError
from qwikstart.operations import insert_text
from qwikstart.tasks import Task

from . import helpers


class TestParseTask:
    def test_parse_returns_task_instance(self) -> None:
        task_spec = {"steps": {"Step 1": {"name": "insert_text"}}}
        expected_operation = insert_text.Operation(description="Step 1")
        assert parser.parse_task(task_spec) == Task(
            context={"execution_context": ANY}, operations=[expected_operation]
        )

    def test_operations_key_raises_obsolete_error(self) -> None:
        with pytest.raises(ObsoleteError):
            parser.parse_task({"operations": {"insert_text": {}}})

    def test_both_steps_and_operations_defined_raises_error(self) -> None:
        task_spec = {
            "steps": {"Step 1": {"name": "insert_text"}},
            "operations": {"completely_ignored": {}},
        }
        with pytest.raises(ObsoleteError):
            parser.parse_task(task_spec)

    def test_steps_not_defined_raises_error(self) -> None:
        with pytest.raises(TaskParserError):
            parser.parse_task({})


# Ignore type: Mypy doesn't seem to like objects imported into a module.
@patch.object(parser.BaseOperation, "__subclasses__")  # type: ignore
class TestGetOperationsMapping:
    def test_no_operations(self, mock_get_subclasses: Mock) -> None:
        mock_get_subclasses.return_value = []
        assert parser.get_operations_mapping() == {}

    def test_one_operation(self, mock_get_subclasses: Mock) -> None:
        class MockOperation:
            name = "fake_op"
            aliases: List[str] = []

        mock_get_subclasses.return_value = [MockOperation]
        assert parser.get_operations_mapping() == {"fake_op": MockOperation}

    def test_operation_with_no_name_skipped(self, mock_get_subclasses: Mock) -> None:
        class MockOperation:
            name = "fake_op"
            aliases: List[str] = []

        mock_get_subclasses.return_value = [MockOperation]
        assert parser.get_operations_mapping() == {"fake_op": MockOperation}

    def test_operation_with_alias(self, mock_get_subclasses: Mock) -> None:
        class MockOperation:
            name = "fake_op"
            aliases = ["fake_alias"]

        mock_get_subclasses.return_value = [MockOperation]
        assert parser.get_operations_mapping() == {
            "fake_op": MockOperation,
            "fake_alias": MockOperation,
        }


class TestParseOperationFromStep:
    def test_success(self) -> None:
        op_def = {"name": "insert_text", "description": "Test operation"}
        op = parser.parse_operation_from_step(op_def)
        assert op == insert_text.Operation(description="Test operation")

    def test_custom_operation_mapping(self) -> None:
        mock_operation = Mock()
        op_def = {"name": "custom"}
        known_ops = {"custom": Mock(return_value=mock_operation)}
        op = parser.parse_operation_from_step(op_def, known_ops)
        assert op == mock_operation

    def test_unknown_operation(self) -> None:
        with pytest.raises(TaskParserError):
            parser.parse_operation_from_step({"name": "undefined_operation"})

    def test_operation_with_no_name(self) -> None:
        with pytest.raises(TaskParserError):
            parser.parse_operation_from_step({})

    @patch.object(parser, "logger")
    def test_config_input_mapping_does_not_log(self, logger: Mock) -> None:
        config_dict = {"input_mapping": {"name": "template_variables.name"}}
        op_def = {"name": "fake_op", "description": "Test", "opconfig": config_dict}
        op = parser.parse_operation_from_step(op_def)

        opconfig = dict(input_mapping={"name": "template_variables.name"})
        assert op == helpers.FakeOperation(description="Test", opconfig=opconfig)
        logger.info.assert_not_called()

    @patch.object(parser, "logger")
    def test_config_output_mapping_does_not_log(self, logger: Mock) -> None:
        config_dict = {"output_mapping": {"template_variables.name": "name"}}
        op_def = {"name": "fake_op", "description": "Test", "opconfig": config_dict}
        op = parser.parse_operation_from_step(op_def)

        opconfig = dict(output_mapping={"template_variables.name": "name"})
        assert op == helpers.FakeOperation(description="Test", opconfig=opconfig)
        logger.info.assert_not_called()

    def test_old_input_mapping_raises_error(self) -> None:
        op_def = {"name": "fake_op", "description": "Test", "input_mapping": {}}
        with pytest.raises(ObsoleteError):
            parser.parse_operation_from_step(op_def)

    def test_old_output_mapping_raises_error(self) -> None:
        op_def = {"name": "fake_op", "description": "Test", "output_mapping": {}}
        with pytest.raises(ObsoleteError):
            parser.parse_operation_from_step(op_def)
