==================
context_from_regex
==================

.. include:: aliases.rst

Operation to extract context data from a file using a regex.

Example
=======

The following example uses a regex to extract the project name from a python project's
`pyproject.toml`:

.. literalinclude:: ../../examples/operations/context_from_regex.yml
   :emphasize-lines: 3-5
   :caption: `examples/operations/context_from_regex.yml`

Note that the regex must be defined as a `named capture group`_, where the name of the
capture group (the `project_name` part of `(?P<project_name>[^"]+)` in this case)
specifies the name where the value is stored.

In order to render the context variable using the `echo` operation, the `project_name`
is saved to the `template_variables` namespace by defining
`output_namespace = "template_variables"`. See :doc:`../understanding_operations` and
the docs for the :doc:`./echo` operation for more info.

Required context
================

`regex`
    Regex to search for in `file_path`. Note that this is expected to contain
    `named capture groups`_. Names of capture groups define new context variable names.

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

See also
========

- :doc:`define_context`
- :doc:`echo`

.. _named capture groups:
    https://docs.python.org/3/howto/regex.html#non-capturing-and-named-groups

.. _named capture group: `named capture groups`_
