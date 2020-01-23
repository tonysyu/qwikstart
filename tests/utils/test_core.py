from dataclasses import dataclass

import pytest

from qwikstart.utils import core


@dataclass
class Person:
    """Example dataclass for testing."""

    name: str


class TestGetDataclassKeys:
    def test_keys_match(self) -> None:
        assert list(core.get_dataclass_keys(Person)) == ["name"]

    def test_non_dataclass_raises_type_error(self) -> None:
        with pytest.raises(TypeError):
            core.get_dataclass_keys(object)


class TestGetDataclassValues:
    def test_values_match(self) -> None:
        assert [field.name for field in core.get_dataclass_values(Person)] == ["name"]

    def test_non_dataclass_raises_type_error(self) -> None:
        with pytest.raises(TypeError):
            core.get_dataclass_values(object)
