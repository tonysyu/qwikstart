=====
shell
=====

.. include:: aliases.rst

Operation to run an arbitrary shell command.

Required context
================

`cmd`
    Command or list of command arguments to run.

Optional context
================

`echo_output`
    default: `True`

    Toggle display of output to terminal.

`ignore_error_code`
    default: `False`

    Toggle check for error code returned by shell operation.

`output_processor`
    default: `'strip'`

    Processor to run on output `dict_keys(['noop', 'strip'])`

`output_var`
    default: `None`

    Variable name in which output is stored.

`template_variables`
    |template_variables description|

`template_variable_prefix`
    default: `'qwikstart'`

    |template_variable_prefix description|

Output
======

This operation can define arbitrary output in a variable defined by `output_var`.
