from dataclasses import Field, dataclass, field, make_dataclass
from typing import List, Tuple, Union
from unittest.mock import patch

from qwikstart.base_context import BaseContext
from qwikstart.cli import utils
from qwikstart.utils import first

FAKE_OP_NAME = "fake_operation"

_DataClassField = Union[str, Tuple[str, type], Tuple[str, type, Field]]


class TestGetOperationHelp:
    def test_basic_context(self):
        context_class = make_context(
            ("required_parameter", str), ("optional_parameter", str, "default value")
        )
        op_help = get_operation_from_context_class(context_class)

        assert op_help.name == FAKE_OP_NAME
        assert op_help.docstring == "Docstring for fake operation"

        var_names = [var.name for var in op_help.required_context]
        assert var_names == ["required_parameter"]
        var_names = [var.name for var in op_help.optional_context]
        assert var_names == ["optional_parameter"]

    def test_context_with_no_required_params(self):
        context_class = make_context(("optional_parameter", str, "default value"))
        op_help = get_operation_from_context_class(context_class)

        assert op_help.required_context == []
        var_names = [var.name for var in op_help.optional_context]
        assert var_names == ["optional_parameter"]

    def test_context_with_no_optional_params(self):
        context_class = make_context(("required_parameter", str))
        op_help = get_operation_from_context_class(context_class)

        assert op_help.optional_context == []
        var_names = [var.name for var in op_help.required_context]
        assert var_names == ["required_parameter"]

    def test_execution_context_excluded(self):
        # FIXME: Ignore mypy error when accessing __dataclass_fields__.
        # See https://github.com/python/mypy/issues/6568
        assert "execution_context" in BaseContext.__dataclass_fields__
        op_help = get_operation_from_context_class(BaseContext)

        assert op_help.required_context == []
        assert op_help.optional_context == []

    def test_default_value(self):
        context_class = make_context(("default_string", str, "default"))
        op_help = get_operation_from_context_class(context_class)

        context_var = first(op_help.optional_context)
        assert context_var.default == "default"

    def test_default_factory(self):
        context_class = make_context(
            ("default_factory", List[int], field(default_factory=list))
        )
        op_help = get_operation_from_context_class(context_class)

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
    with patch.object(utils, "get_operations_mapping", return_value=op_mapping):
        return utils.get_operation_help(FAKE_OP_NAME)


def make_context(*fields):
    resolved_fields = [_resolve_dataclass_field(f) for f in fields]
    bases = (BaseContext,)
    return make_dataclass("FakeContext", resolved_fields, bases=bases, frozen=True)


def _resolve_dataclass_field(field_list) -> _DataClassField:
    """Return field list expected by `make_dataclass` with casting for defaults

    The third value of each field passed to `make_dataclass` is expected to be
    a `Field` instance. Cast third value to field, assuming it defines default
    value of field.
    """
    if len(field_list) == 3 and not isinstance(field_list[2], Field):
        return field_list[:2] + (field(default=field_list[2]),)
    return field_list
