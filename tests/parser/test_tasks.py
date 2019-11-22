from unittest import mock

# Ignore pytest typing: see https://github.com/pytest-dev/pytest/issues/3342
import pytest  # type: ignore

from qwikstart import parser
from qwikstart.operations import find_tagged_line, insert_text
from qwikstart.tasks import Task


class TestParseTask:
    def test_two_operations(self):
        task_definition = {"operations": ["find_tagged_line", "insert_text"]}
        assert parser.parse_task(task_definition) == Task(
            context={"execution_context": mock.ANY},
            operations=[find_tagged_line.Operation(), insert_text.Operation()],
        )

    def test_operation_dict_definition(self):
        mapping = {"line_number": "line"}
        task_definition = {
            "operations": [{"insert_text": {"mapping": mapping}}]
        }
        assert parser.parse_task(task_definition) == Task(
            context={"execution_context": mock.ANY},
            operations=[insert_text.Operation(mapping=mapping)],
        )

    def test_operation_with_local_context(self):
        context = {"line": 42}
        task_definition = {
            "operations": [{"insert_text": {"local_context": context}}]
        }
        assert parser.parse_task(task_definition) == Task(
            context={"execution_context": mock.ANY},
            operations=[insert_text.Operation(local_context=context)],
        )

    def test_operation_tuple_definition(self):
        mapping = {"line_number": "line"}
        task_definition = {
            "operations": [("insert_text", {"mapping": mapping})]
        }
        assert parser.parse_task(task_definition) == Task(
            context={"execution_context": mock.ANY},
            operations=[insert_text.Operation(mapping=mapping)],
        )

    def test_unknown_operation(self):
        task_definition = {"operations": ["undefined_operation"]}
        with pytest.raises(parser.ParserError):
            parser.parse_task(task_definition)
