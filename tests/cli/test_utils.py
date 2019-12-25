from dataclasses import dataclass, field
from typing import List
from unittest.mock import patch

from qwikstart.cli import utils
from qwikstart.utils import first

FAKE_OP_NAME = "fake_operation"


def mock_get_operation_help(context_class):
    """Mock `utils.get_operation_help` return help for fake operation"""

    class FakeOperation:
        """Docstring for fake operation"""

        @classmethod
        def get_context_class(cls):
            return context_class

    op_mapping = {FAKE_OP_NAME: FakeOperation}
    with patch.object(
        utils, "get_operations_mapping", return_value=op_mapping
    ):
        return utils.get_operation_help(FAKE_OP_NAME)


class TestGetOperationHelp:
    def test_basic_context(self):
        @dataclass
        class FakeContext:
            required_parameter: str
            optional_parameter: str = "default value"

        op_help = mock_get_operation_help(FakeContext)

        assert op_help.name == FAKE_OP_NAME
        assert op_help.docstring == "Docstring for fake operation"

        var_names = [var.name for var in op_help.required_context]
        assert var_names == ["required_parameter"]
        var_names = [var.name for var in op_help.optional_context]
        assert var_names == ["optional_parameter"]

    def test_context_with_no_required_params(self):
        @dataclass
        class FakeContext:
            optional_parameter: str = "default value"

        op_help = mock_get_operation_help(FakeContext)

        assert op_help.required_context == []
        var_names = [var.name for var in op_help.optional_context]
        assert var_names == ["optional_parameter"]

    def test_context_with_no_optional_params(self):
        @dataclass
        class FakeContext:
            required_parameter: str

        op_help = mock_get_operation_help(FakeContext)

        assert op_help.optional_context == []
        var_names = [var.name for var in op_help.required_context]
        assert var_names == ["required_parameter"]

    def test_execution_context_excluded(self):
        @dataclass
        class FakeContext:
            execution_context: str

        op_help = mock_get_operation_help(FakeContext)

        assert op_help.required_context == []
        assert op_help.optional_context == []

    def test_default_value(self):
        @dataclass
        class FakeContext:
            default_string: str = "default"

        op_help = mock_get_operation_help(FakeContext)

        context_var = first(op_help.optional_context)
        assert context_var.default == "default"

    def test_default_factory(self):
        @dataclass
        class FakeContext:
            default_factory: List[int] = field(default_factory=list)

        op_help = mock_get_operation_help(FakeContext)

        context_var = first(op_help.optional_context)
        assert context_var.default == list
