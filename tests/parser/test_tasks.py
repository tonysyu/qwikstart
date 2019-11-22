from unittest import mock

from qwikstart import parser
from qwikstart.operations import insert_text
from qwikstart.tasks import Task


class TestParseTask:
    def test_basic_task_definition(self):
        mapping = {"line_number": "line"}
        task_definition = {
            "operations": [{"insert_text": {"mapping": mapping}}]
        }
        assert parser.parse_task(task_definition) == Task(
            context={"execution_context": mock.ANY},
            operations=[insert_text.Operation(mapping=mapping)],
        )
