from unittest.mock import Mock, patch

from qwikstart.utils import http

# Ignore type: Mypy doesn't like referencing objects imported into a module.
REQUESTS_MODULE = http.requests  # type: ignore


class TestIsUrl:
    def test_http_url(self) -> None:
        assert http.is_url("http://example.com") is True

    def test_https_url(self) -> None:
        assert http.is_url("https://example.com") is True

    def test_non_url(self) -> None:
        assert http.is_url("not-a-url") is False


@patch.object(REQUESTS_MODULE, "get", return_value=Mock(text="http-response-text"))
def test_read_from_url(mock_get: Mock) -> None:
    assert http.read_from_url("fake.url") == "http-response-text"
    mock_get.assert_called_once_with("fake.url")
