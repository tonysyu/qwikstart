from unittest import mock

from qwikstart import parser
from qwikstart.operations import insert_text
from qwikstart.tasks import Task


class TestParseTask:
    def test_operation_list(self) -> None:
        input_mapping = {"line_number": "line"}
        task_definition: parser.TaskDefinition = {
            "operations": [{"insert_text": {"input_mapping": input_mapping}}]
        }
        assert parser.parse_task(task_definition) == Task(
            context={"execution_context": mock.ANY},
            operations=[insert_text.Operation(input_mapping=input_mapping)],
        )

    def test_operation_dict(self) -> None:
        input_mapping = {"line_number": "line"}
        task_definition: parser.TaskDefinition = {
            "operations": {"insert_text": {"input_mapping": input_mapping}}
        }
        assert parser.parse_task(task_definition) == Task(
            context={"execution_context": mock.ANY},
            operations=[insert_text.Operation(input_mapping=input_mapping)],
        )
