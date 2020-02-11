from typing import Any, Dict, List, Tuple
from unittest.mock import Mock, patch

import pytest

from qwikstart.exceptions import TaskParserError
from qwikstart.operations import find_tagged_line, insert_text
from qwikstart.parser import operations
from qwikstart.repository import OperationSpec


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
        input_mapping = {"line_number": "line"}
        op_def = {"name": "insert_text", "input_mapping": input_mapping}
        op = operations.parse_operation_from_step(op_def)
        assert op == insert_text.Operation(input_mapping=input_mapping)

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


class TestParseOperation:
    def test_string_definition(self) -> None:
        assert (
            operations.parse_operation("find_tagged_line")
            == find_tagged_line.Operation()
        )

    def test_dict_definition(self) -> None:
        input_mapping = {"line_number": "line"}
        op_def: OperationSpec = {"insert_text": {"input_mapping": input_mapping}}
        assert operations.parse_operation(op_def) == insert_text.Operation(
            input_mapping=input_mapping
        )

    def test_tuple_definition(self) -> None:
        op_def: OperationSpec = ("insert_text", {})
        assert operations.parse_operation(op_def) == insert_text.Operation()

    def test_operation_with_local_context(self) -> None:
        context = {"line": 42}
        op_def: OperationSpec = {"insert_text": {"local_context": context}}
        assert operations.parse_operation(op_def) == insert_text.Operation(
            local_context=context
        )

    def test_operation_with_context_defined_as_top_level_parameter(self) -> None:
        context = {"line": 42}
        op_def: OperationSpec = {"insert_text": context}
        assert operations.parse_operation(op_def) == insert_text.Operation(
            local_context=context
        )

    def test_unknown_operation(self) -> None:
        with pytest.raises(TaskParserError):
            operations.parse_operation("undefined_operation")


class TestNormalizeOpDefinition:
    def test_empty_dict_not_supported(self) -> None:
        error_msg = "Operation definition with dict should only have a single key"
        with pytest.raises(TaskParserError, match=error_msg):
            operations.normalize_op_definition({})

    def test_dict_with_multiple_keys_not_supported(self) -> None:
        op_def_with_too_many_keys: Dict[str, Any] = {"op1": {}, "op2": {}}
        error_msg = "Operation definition with dict should only have a single key"
        with pytest.raises(TaskParserError, match=error_msg):
            operations.normalize_op_definition(op_def_with_too_many_keys)

    def test_tuple_of_one_not_supported(self) -> None:
        op_def_with_only_a_name = tuple(["name-of-op"])
        error_msg = "Operation definition with sequence should only have two items"
        with pytest.raises(TaskParserError, match=error_msg):
            # Ignore typing since we're intentionally passing an incompatible tuple
            operations.normalize_op_definition(op_def_with_only_a_name)  # type: ignore

    def test_tuple_of_more_than_two_not_supported(self) -> None:
        op_def_with_bad_tuple: Tuple[str, Dict[str, Any], str] = (
            "name-of-op",
            {},
            "unsupported-third-argument",
        )
        error_msg = "Operation definition with sequence should only have two items"
        with pytest.raises(TaskParserError, match=error_msg):
            # Ignore typing since we're intentionally passing an incompatible tuple
            operations.normalize_op_definition(op_def_with_bad_tuple)  # type: ignore

    def test_invalid_op_def_type(self) -> None:
        invalid_op_def_type = True
        error_msg = "Could not parse operation definition: True"
        with pytest.raises(TaskParserError, match=error_msg):
            # Ignore typing since we're intentionally passing an incompatible tuple
            operations.normalize_op_definition(invalid_op_def_type)  # type: ignore
