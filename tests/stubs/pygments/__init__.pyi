from .formatters import Formatter
from .lexers import Lexer

def highlight(message: str, lexer: Lexer, formatter: Formatter) -> str: ...
