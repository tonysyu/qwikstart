import pytest

from qwikstart.exceptions import UserFacingError
from qwikstart.utils.prompt import create_prompt


class TestCreatePrompt:
    def test_name_only(self) -> None:
        prompt = create_prompt(name="test")
        assert prompt.name == "test"
        assert prompt.default_value is None

    def test_name_and_default(self) -> None:
        prompt = create_prompt(name="test", default_value="hello")
        assert prompt.name == "test"
        assert prompt.default_value == "hello"

    def test_name_missing_raises(self) -> None:
        with pytest.raises(UserFacingError, match="Prompt definition has no 'name'"):
            create_prompt()

    def test_unknown_attribute_raises(self) -> None:
        msg = "Prompt definition for 'test' has unknown keys:"
        with pytest.raises(UserFacingError, match=msg):
            create_prompt(name="test", unknown="value")
