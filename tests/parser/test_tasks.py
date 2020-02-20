from unittest.mock import ANY, Mock, patch

import pytest

from qwikstart.exceptions import TaskParserError
from qwikstart.operations import insert_text
from qwikstart.parser import tasks
from qwikstart.tasks import Task


class TestParseTask:
    def test_operation_list(self) -> None:
        input_mapping = {"line_number": "line"}
        task_spec: tasks.TaskSpec = {
            "operations": [{"insert_text": {"input_mapping": input_mapping}}]
        }
        assert tasks.parse_task(task_spec) == Task(
            context={"execution_context": ANY},
            operations=[insert_text.Operation(input_mapping=input_mapping)],
        )

    def test_operation_dict(self) -> None:
        input_mapping = {"line_number": "line"}
        task_spec: tasks.TaskSpec = {
            "operations": {"insert_text": {"input_mapping": input_mapping}}
        }
        assert tasks.parse_task(task_spec) == Task(
            context={"execution_context": ANY},
            operations=[insert_text.Operation(input_mapping=input_mapping)],
        )

    @patch.object(tasks, "logger")
    def test_deprecation_logged_for_operations(self, logger: Mock) -> None:
        tasks.parse_task({"operations": {"insert_text": {}}})
        logger.info.assert_called_once_with(
            "Note that `operations` in task specification is deprecated. "
            "Use `steps` instead."
        )

    def test_steps(self) -> None:
        input_mapping = {"line_number": "line"}
        task_spec: tasks.TaskSpec = {
            "steps": {"Step 1": {"name": "insert_text", "input_mapping": input_mapping}}
        }
        expected_operation = insert_text.Operation(
            description="Step 1", input_mapping=input_mapping
        )
        assert tasks.parse_task(task_spec) == Task(
            context={"execution_context": ANY}, operations=[expected_operation]
        )

    @patch.object(tasks, "logger")
    def test_both_steps_and_operations_defined(self, logger: Mock) -> None:
        task_spec: tasks.TaskSpec = {
            "steps": {"Step 1": {"name": "insert_text"}},
            "operations": {"completely_ignored": {}},
        }
        assert tasks.parse_task(task_spec) == Task(
            context={"execution_context": ANY},
            operations=[insert_text.Operation(description="Step 1")],
        )
        logger.warning.assert_called_once_with(
            "Found both `steps` and `operations` in task specification. "
            "Only `steps` will be read."
        )

    def test_exception_when_neither_steps_or_operations_defined(self) -> None:
        with pytest.raises(TaskParserError):
            tasks.parse_task({})
