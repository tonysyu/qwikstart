from qwikstart.utils import core

from typing_extensions import TypedDict


class MergeTypedDicts:
    def test_one_type(self):
        A = TypedDict("A", {"a": int})
        A_merged = core.merge_typed_dicts(A)
        assert A_merged == A
        assert A_merged.__name__ == "MergedTypedDict"

    def test_two_types(self):
        A = TypedDict("A", {"a": int})
        B = TypedDict("B", {"b": int})
        AB = core.merge_typed_dicts(A, B)
        assert AB.__annotations__ == {"a": int, "b": int}

    def test_three_types(self):
        A = TypedDict("A", {"a": int})
        B = TypedDict("B", {"b": int})
        C = TypedDict("C", {"c": int})
        ABC = core.merge_typed_dicts(A, B, C)
        assert ABC.__annotations__ == {"a": int, "b": int, "c": int}

    def test_duplicate_named_types_are_not_equal(self):
        A = core.merge_typed_dicts(TypedDict("A", {"a": int}))
        B = core.merge_typed_dicts(TypedDict("B", {"b": int}))
        assert A.__name__ == B.__name__
        assert A != B

    def test_rename_result(self):
        A = core.merge_typed_dicts(TypedDict("A", {"a": int}), name="A_name")
        assert A.__name__ == "A_name"
