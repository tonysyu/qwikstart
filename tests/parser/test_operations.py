from typing import List
from unittest.mock import Mock, patch

import pytest

from qwikstart.exceptions import ObsoleteError, TaskParserError
from qwikstart.operations import insert_text
from qwikstart.parser import operations

from .. import helpers


# Ignore type: Mypy doesn't seem to like objects imported into a module.
@patch.object(operations.BaseOperation, "__subclasses__")  # type: ignore
class TestGetOperationsMapping:
    def test_no_operations(self, mock_get_subclasses: Mock) -> None:
        mock_get_subclasses.return_value = []
        assert operations.get_operations_mapping() == {}

    def test_one_operation(self, mock_get_subclasses: Mock) -> None:
        class MockOperation:
            name = "fake_op"
            aliases: List[str] = []

        mock_get_subclasses.return_value = [MockOperation]
        assert operations.get_operations_mapping() == {"fake_op": MockOperation}

    def test_operation_with_no_name_skipped(self, mock_get_subclasses: Mock) -> None:
        class MockOperation:
            name = "fake_op"
            aliases: List[str] = []

        mock_get_subclasses.return_value = [MockOperation]
        assert operations.get_operations_mapping() == {"fake_op": MockOperation}

    def test_operation_with_alias(self, mock_get_subclasses: Mock) -> None:
        class MockOperation:
            name = "fake_op"
            aliases = ["fake_alias"]

        mock_get_subclasses.return_value = [MockOperation]
        assert operations.get_operations_mapping() == {
            "fake_op": MockOperation,
            "fake_alias": MockOperation,
        }


class TestParseOperationFromStep:
    def test_success(self) -> None:
        op_def = {"name": "insert_text", "description": "Test operation"}
        op = operations.parse_operation_from_step(op_def)
        assert op == insert_text.Operation(description="Test operation")

    def test_custom_operation_mapping(self) -> None:
        mock_operation = Mock()
        op_def = {"name": "custom"}
        known_ops = {"custom": Mock(return_value=mock_operation)}
        op = operations.parse_operation_from_step(op_def, known_ops)
        assert op == mock_operation

    def test_unknown_operation(self) -> None:
        with pytest.raises(TaskParserError):
            operations.parse_operation_from_step({"name": "undefined_operation"})

    def test_operation_with_no_name(self) -> None:
        with pytest.raises(TaskParserError):
            operations.parse_operation_from_step({})

    @patch.object(operations, "logger")
    def test_config_input_mapping_does_not_log(self, logger: Mock) -> None:
        config_dict = {"input_mapping": {"name": "template_variables.name"}}
        op_def = {"name": "fake_op", "description": "Test", "opconfig": config_dict}
        op = operations.parse_operation_from_step(op_def)

        opconfig = dict(input_mapping={"name": "template_variables.name"})
        assert op == helpers.FakeOperation(description="Test", opconfig=opconfig)
        logger.info.assert_not_called()

    @patch.object(operations, "logger")
    def test_config_output_mapping_does_not_log(self, logger: Mock) -> None:
        config_dict = {"output_mapping": {"template_variables.name": "name"}}
        op_def = {"name": "fake_op", "description": "Test", "opconfig": config_dict}
        op = operations.parse_operation_from_step(op_def)

        opconfig = dict(output_mapping={"template_variables.name": "name"})
        assert op == helpers.FakeOperation(description="Test", opconfig=opconfig)
        logger.info.assert_not_called()

    def test_old_input_mapping_raises_error(self) -> None:
        op_def = {"name": "fake_op", "description": "Test", "input_mapping": {}}
        with pytest.raises(ObsoleteError):
            operations.parse_operation_from_step(op_def)

    def test_old_output_mapping_raises_error(self) -> None:
        op_def = {"name": "fake_op", "description": "Test", "output_mapping": {}}
        with pytest.raises(ObsoleteError):
            operations.parse_operation_from_step(op_def)
