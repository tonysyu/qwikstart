import functools
import re
from typing import List


def create_regex_flags(flag_strings: List[str]) -> re.RegexFlag:
    default = re.RegexFlag(0)
    flags = (getattr(re, name, default) for name in flag_strings)
    # FIXME: This line complains about returning Any but still fails when casting.
    return functools.reduce(lambda x, y: x | y, flags, default)  # type: ignore
