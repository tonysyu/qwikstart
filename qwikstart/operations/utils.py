from ..utils import clean_multiline

FILE_PATH_HELP = "Path to file relative to the current working directory."

REGEX_FLAGS_HELP = clean_multiline(
    """
        List of Python regex flags. Any combination of `'IGNORECASE'`, `'MULTILINE'`,
        `'DOTALL'`, `'UNICODE'`. See `docs for Python regex library`_
    """
)
TEMPLATE_VARIABLE_PREFIX_HELP = clean_multiline(
    """
        Template variables will be nested in this namespace when rendering; e.g:

        {{ <template_variable_prefix>.your_template_variable }}
    """
)
