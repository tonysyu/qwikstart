from urllib.parse import urlparse

import requests


def is_url(url: str) -> bool:
    return bool(urlparse(url).scheme)


def content_type_from_response(response: requests.Response) -> str:
    content_type, _ = response.headers["Content-Type"]
    return content_type


def read_from_url(url: str) -> str:
    response = requests.get(url)
    return response.text
