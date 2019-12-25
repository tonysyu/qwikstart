from dataclasses import dataclass, field
from typing import List
from unittest.mock import patch

from qwikstart.base_context import BaseContext
from qwikstart.cli import utils
from qwikstart.utils import first

FAKE_OP_NAME = "fake_operation"


class TestGetOperationHelp:
    def test_basic_context(self):
        @dataclass(frozen=True)
        class FakeContext(BaseContext):
            required_parameter: str
            optional_parameter: str = "default value"

        op_help = get_operation_from_context_class(FakeContext)

        assert op_help.name == FAKE_OP_NAME
        assert op_help.docstring == "Docstring for fake operation"

        var_names = [var.name for var in op_help.required_context]
        assert var_names == ["required_parameter"]
        var_names = [var.name for var in op_help.optional_context]
        assert var_names == ["optional_parameter"]

    def test_context_with_no_required_params(self):
        @dataclass(frozen=True)
        class FakeContext(BaseContext):
            optional_parameter: str = "default value"

        op_help = get_operation_from_context_class(FakeContext)

        assert op_help.required_context == []
        var_names = [var.name for var in op_help.optional_context]
        assert var_names == ["optional_parameter"]

    def test_context_with_no_optional_params(self):
        @dataclass(frozen=True)
        class FakeContext(BaseContext):
            required_parameter: str

        op_help = get_operation_from_context_class(FakeContext)

        assert op_help.optional_context == []
        var_names = [var.name for var in op_help.required_context]
        assert var_names == ["required_parameter"]

    def test_execution_context_excluded(self):
        assert "execution_context" in BaseContext.__dataclass_fields__
        op_help = get_operation_from_context_class(BaseContext)

        assert op_help.required_context == []
        assert op_help.optional_context == []

    def test_default_value(self):
        @dataclass(frozen=True)
        class FakeContext(BaseContext):
            default_string: str = "default"

        op_help = get_operation_from_context_class(FakeContext)

        context_var = first(op_help.optional_context)
        assert context_var.default == "default"

    def test_default_factory(self):
        @dataclass(frozen=True)
        class FakeContext(BaseContext):
            default_factory: List[int] = field(default_factory=list)

        op_help = get_operation_from_context_class(FakeContext)

        context_var = first(op_help.optional_context)
        assert context_var.default == list

    def test_field_with_help(self):
        @dataclass(frozen=True)
        class FakeContext(BaseContext):
            field_with_help: str

            @classmethod
            def help(cls, field_name):
                return "Additional info about field."

        class FakeOperation:
            @classmethod
            def get_context_class(cls):
                return FakeContext

        op_help = get_operation_from_context_class(FakeContext)

        context_var = first(op_help.required_context)
        assert context_var.description == "Additional info about field."


def get_operation_from_context_class(context_class):
    """Mock `utils.get_operation_help` return help for fake operation"""

    class FakeOperation:
        """Docstring for fake operation"""

        @classmethod
        def get_context_class(cls):
            return context_class

    return get_operation_from_fake_operation(FakeOperation)


def get_operation_from_fake_operation(fake_coperation_class):
    """Mock `utils.get_operation_help` return help for fake operation"""
    op_mapping = {FAKE_OP_NAME: fake_coperation_class}
    with patch.object(
        utils, "get_operations_mapping", return_value=op_mapping
    ):
        return utils.get_operation_help(FAKE_OP_NAME)
