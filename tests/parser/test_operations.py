import pytest

from qwikstart.exceptions import TaskParserError
from qwikstart.operations import find_tagged_line, insert_text
from qwikstart.parser import operations


class TestParseOperation:
    def test_string_definition(self) -> None:
        assert (
            operations.parse_operation("find_tagged_line")
            == find_tagged_line.Operation()
        )

    def test_dict_definition(self) -> None:
        input_mapping = {"line_number": "line"}
        op_def: operations.UnparsedOperation = {
            "insert_text": {"input_mapping": input_mapping}
        }
        assert operations.parse_operation(op_def) == insert_text.Operation(
            input_mapping=input_mapping
        )

    def test_tuple_definition(self) -> None:
        op_def: operations.UnparsedOperation = ("insert_text", {})
        assert operations.parse_operation(op_def) == insert_text.Operation()

    def test_operation_with_local_context(self) -> None:
        context = {"line": 42}
        op_def: operations.UnparsedOperation = {
            "insert_text": {"local_context": context}
        }
        assert operations.parse_operation(op_def) == insert_text.Operation(
            local_context=context
        )

    def test_operation_with_context_defined_as_top_level_parameter(self) -> None:
        context = {"line": 42}
        op_def: operations.UnparsedOperation = {"insert_text": context}
        assert operations.parse_operation(op_def) == insert_text.Operation(
            local_context=context
        )

    def test_unknown_operation(self) -> None:
        with pytest.raises(TaskParserError):
            operations.parse_operation("undefined_operation")
