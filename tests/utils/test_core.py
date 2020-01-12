from qwikstart.utils import core


class TestMergeNestedDicts:
    def test_nested_dict_only_in_first_dict(self) -> None:
        nested_dict = {"template_variables": {"some": "value"}}
        assert core.merge_nested_dicts(nested_dict, {}) == nested_dict

    def test_nested_dict_only_in_second_dict(self) -> None:
        nested_dict = {"template_variables": {"some": "value"}}
        assert core.merge_nested_dicts({}, nested_dict) == nested_dict

    def test_second_dict_takes_precedence(self) -> None:
        merged_dict = core.merge_nested_dicts(
            {"template_variables": {"same-key": "first"}},
            {"template_variables": {"same-key": "second"}},
        )
        assert merged_dict == {"template_variables": {"same-key": "second"}}

    def test_non_overlapping_key_merged(self) -> None:
        merged_dict = core.merge_nested_dicts(
            {"template_variables": {"a": 1}}, {"template_variables": {"b": 2}}
        )
        assert merged_dict == {"template_variables": {"a": 1, "b": 2}}
