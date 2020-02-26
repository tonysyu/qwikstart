from urllib.parse import urlparse

import requests


def is_url(url: str) -> bool:
    return bool(urlparse(url).scheme)


def read_from_url(url: str) -> str:
    response = requests.get(url)
    return response.text
