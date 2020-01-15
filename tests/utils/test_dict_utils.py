from typing import Any, Dict

import pytest

from qwikstart.utils import dict_utils


class TestGetNestedDictValue:
    def test_one_level(self) -> None:
        nested_dict = {"nested": {"key": "value"}}
        assert dict_utils.get_nested_dict_value(nested_dict, "nested.key") == "value"

    def test_nested_key_not_found_raises_key_error(self) -> None:
        nested_dict = {"key": "value"}
        with pytest.raises(KeyError, match="Nested key 'nested.key' not found"):
            dict_utils.get_nested_dict_value(nested_dict, "nested.key")

    def test_part_of_nested_key_not_dict_raises_value_error(self) -> None:
        nested_dict = {"a": "value"}
        with pytest.raises(ValueError, match="Expected key 'a' to contain dict"):
            dict_utils.get_nested_dict_value(nested_dict, "a.key")

    def test_missing_key_raises_key_error(self) -> None:
        nested_dict = {"key": "value"}
        with pytest.raises(KeyError, match="Nested key 'missing' not found"):
            dict_utils.get_nested_dict_value(nested_dict, "missing")


class TestSetNestedDictValue:
    def test_one_level(self) -> None:
        nested_dict: Dict[str, Any] = {"nested": {}}
        dict_utils.set_nested_dict_value(nested_dict, "nested.key", "value")
        assert nested_dict == {"nested": {"key": "value"}}

    def test_part_of_nested_key_not_dict_raises_value_error(self) -> None:
        nested_dict = {"a": "value"}
        with pytest.raises(ValueError, match="Expected key 'a' to contain dict"):
            dict_utils.set_nested_dict_value(nested_dict, "a.key", "value")


class TestMergeNestedDicts:
    def test_nested_dict_only_in_first_dict(self) -> None:
        nested_dict = {"nested_dict": {"some": "value"}}
        assert dict_utils.merge_nested_dicts(nested_dict, {}) == nested_dict

    def test_nested_dict_only_in_second_dict(self) -> None:
        nested_dict = {"nested_dict": {"some": "value"}}
        assert dict_utils.merge_nested_dicts({}, nested_dict) == nested_dict

    def test_second_dict_takes_precedence(self) -> None:
        merged_dict = dict_utils.merge_nested_dicts(
            {"nested_dict": {"same-key": "first"}},
            {"nested_dict": {"same-key": "second"}},
        )
        assert merged_dict == {"nested_dict": {"same-key": "second"}}

    def test_non_overlapping_key_merged(self) -> None:
        merged_dict = dict_utils.merge_nested_dicts(
            {"nested_dict": {"a": 1}}, {"nested_dict": {"b": 2}}
        )
        assert merged_dict == {"nested_dict": {"a": 1, "b": 2}}


class TestRemapDict:
    def test_remap_key(self) -> None:
        remapped_dict = dict_utils.remap_dict({"key": "value"}, {"key": "new-key"})
        assert remapped_dict == {"new-key": "value"}

    def test_no_op(self) -> None:
        remapped_dict = dict_utils.remap_dict({"key": "value"}, {"key": "key"})
        assert remapped_dict == {"key": "value"}

    def test_unknown_mappings_have_no_effect(self) -> None:
        remapped_dict = dict_utils.remap_dict({"key": "value"}, {"a": "b"})
        assert remapped_dict == {"key": "value"}

    def test_nested_dict_mapping_creates_nested_dict(self) -> None:
        remapped_dict = dict_utils.remap_dict({"key": "value"}, {"key": "nested.key"})
        assert remapped_dict == {"nested": {"key": "value"}}

    def test_nested_dict_mapping_removes_from_nested_dict(self) -> None:
        remapped_dict = dict_utils.remap_dict(
            {"nested": {"key": "value"}}, {"nested.key": "key"}
        )
        assert remapped_dict == {"key": "value", "nested": {}}

    def test_nested_key_in_mapping_is_not_subdict(self) -> None:
        with pytest.raises(ValueError, match="Expected key 'not-dict' to contain dict"):
            dict_utils.remap_dict({"not-dict": "value"}, {"not-dict.key": "key"})
