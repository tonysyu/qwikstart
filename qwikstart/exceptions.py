"""
qwikstart.exceptions
-----------------------

All exceptions used in the qwikstart code base are defined here.
"""


class QwikstartException(Exception):
    """Base exception class. All qwikstart-specific exceptions should subclass this."""


class TaskLoaderError(QwikstartException):
    """Exception raised when loading task definition fails."""


class TaskParserError(QwikstartException):
    """Exception raised when parsing task definition fails."""


class OperationError(QwikstartException):
    """Exception raised during execution of operation."""


class OperationDefinitionError(QwikstartException):
    """Exception raised when an operation is improperly defined."""
