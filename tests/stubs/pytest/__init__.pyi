from contextlib import contextmanager
from typing import Iterator, Type
@contextmanager
def raises(exception: Type[Exception], match: str = "") -> Iterator[None]: ...
