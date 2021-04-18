from typing import Any, Optional
from .completion import Completer
from .validation import Validator

def prompt(
    message: str,
    completer: Optional[Completer] = None,
    validator: Optional[Validator] = None,
    **kwargs: Any
) -> str: ...
