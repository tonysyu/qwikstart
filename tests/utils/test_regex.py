import re

from qwikstart.utils import regex


class TestCreateRegexFlags:
    def test_empty_list(self) -> None:
        assert regex.create_regex_flags([]) == re.RegexFlag(0)

    def test_unknown_flag(self) -> None:
        assert regex.create_regex_flags(["NOT-A-FLAG"]) == re.RegexFlag(0)

    def test_single_flag(self) -> None:
        assert regex.create_regex_flags(["MULTILINE"]) == re.MULTILINE

    def test_two_flags(self) -> None:
        flags = ["MULTILINE", "IGNORECASE"]
        assert regex.create_regex_flags(flags) == (re.MULTILINE | re.IGNORECASE)
