==================
context_from_regex
==================

.. include:: aliases.rst

Operation to extract context data from a file using a regex.

Required context
================

`regex`
    Regex to search for in `file_path`. Note that this is expected to contain named
    capture groups. Names of capture groups define new context variable names.

    See https://docs.python.org/3/howto/regex.html#non-capturing-and-named-groups

`file_path`
    Path to file relative to the current working directory.

Optional context
================

`regex_flags`
    default: `["MULTILINE"]`

    |regex_flags description|

Output
======

This operation can define arbitrary output values based on named capture groups in
`regex`.
