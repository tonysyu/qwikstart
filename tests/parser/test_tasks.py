from unittest.mock import ANY

import pytest

from qwikstart.exceptions import ObsoleteError, TaskParserError
from qwikstart.operations import insert_text
from qwikstart.parser import tasks
from qwikstart.tasks import Task


class TestParseTask:
    def test_parse_returns_task_instance(self) -> None:
        task_spec = {"steps": {"Step 1": {"name": "insert_text"}}}
        expected_operation = insert_text.Operation(description="Step 1")
        assert tasks.parse_task(task_spec) == Task(
            context={"execution_context": ANY}, operations=[expected_operation]
        )

    def test_operations_key_raises_obsolete_error(self) -> None:
        with pytest.raises(ObsoleteError):
            tasks.parse_task({"operations": {"insert_text": {}}})

    def test_both_steps_and_operations_defined_raises_error(self) -> None:
        task_spec = {
            "steps": {"Step 1": {"name": "insert_text"}},
            "operations": {"completely_ignored": {}},
        }
        with pytest.raises(ObsoleteError):
            tasks.parse_task(task_spec)

    def test_steps_not_defined_raises_error(self) -> None:
        with pytest.raises(TaskParserError):
            tasks.parse_task({})
