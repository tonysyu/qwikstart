from qwikstart.utils import text_utils


class TestStripEmptyLines:
    def test_none_input_gives_empty_string(self) -> None:
        assert text_utils.strip_empty_lines(None) == ""

    def test_whitespace_gives_empty_string(self) -> None:
        assert text_utils.strip_empty_lines("   ") == ""

    def test_single_line(self) -> None:
        assert text_utils.strip_empty_lines("hello") == "hello"

    def test_leading_empty_line_stripped(self) -> None:
        assert text_utils.strip_empty_lines("\nhello") == "hello"

    def test_trailing_empty_line_stripped(self) -> None:
        assert text_utils.strip_empty_lines("hello\n") == "hello"

    def test_empty_line_between_text_preserved(self) -> None:
        assert text_utils.strip_empty_lines("hello\nworld") == "hello\nworld"

    def test_single_line_with_indentation_preserved(self) -> None:
        assert text_utils.strip_empty_lines("    hello") == "    hello"


class TestPformatJson:
    def test_single_key(self) -> None:
        assert text_utils.pformat_json({"key": "value"}) == text_utils.format_multiline(
            """
            {
                "key": "value"
            }
            """
        )
