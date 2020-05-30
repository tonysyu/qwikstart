"""
qwikstart.exceptions
-----------------------

All exceptions used in the qwikstart code base are defined here.
"""


class QwikstartException(Exception):
    """Base exception class. All qwikstart-specific exceptions should subclass this."""


class RepoLoaderError(QwikstartException):
    """Exception raised when loading task specification fails."""


# ----------------------
# User-facing exceptions
# ----------------------


class UserFacingError(QwikstartException):
    """Base exception for errors that are meant to be displayed to users."""


class ConfigurationError(UserFacingError):
    """User-facing exception raised during qwikstart configuration."""


class ObsoleteError(UserFacingError):
    """User-facing exception raised for obsolete functionality."""


class OperationError(UserFacingError):
    """User-facing exception raised during execution of operation."""


class OperationDefinitionError(UserFacingError):
    """Exception raised when an operation is improperly defined."""


class TaskParserError(UserFacingError):
    """User-facing exception raised when parsing task specification fails."""
