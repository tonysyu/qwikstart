.. |file_path description| replace::
    Path to file relative to the current working directory.

.. |regex_flags description| replace::
    List of Python regex flags. Any combination of `'IGNORECASE'`, `'MULTILINE'`,
    `'DOTALL'`, `'UNICODE'`. See `docs for Python regex library`_.

.. |template_variable_prefix description| replace::
    Template variables will be nested in this namespace when rendering; e.g:
    `{{<template_variable_prefix>.your_template_variable}}`

.. |template_variables description| replace::
    Dictionary of variables available when rendering the file template.

.. _docs for Python regex library: https://docs.python.org/3/library/re.html
