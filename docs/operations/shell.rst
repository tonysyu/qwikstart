=====
shell
=====

.. include:: aliases.rst

Operation to run an arbitrary shell command.

Example
=======

The following example uses the `shell` operation to perform two different operations:
First, it uses `grep` to find a file in the git repo starting with a `__version__`, then
it calls `echo` to display the result:

.. literalinclude:: ../../examples/operations/shell.yml
   :language: yaml
   :caption: `examples/operations/shell.yml`

Note that this uses two different signatures to define the shell `cmd`: The `grep`
operation defines the entire command as a string, while the `echo` command defines each
part of the command as an item in a list.

In order to render the context variable using the `echo` command, the `version_file`
is saved to the `template_variables` namespace by defining
`output_namespace = "template_variables"`. See :doc:`../understanding_operations` more
info.

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

See also
========
- :doc:`echo`
- :doc:`find_files`
