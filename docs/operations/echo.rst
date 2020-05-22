====
echo
====

.. include:: aliases.rst

Operation to echo a message to the console.

Example
=======

The following example uses the `echo` operation to display a hello-world greeting to the
terminal:

.. literalinclude:: ../../examples/operations/echo.yml
   :language: yaml
   :emphasize-lines: 8-10
   :caption: `examples/operations/echo.yml`

In order to demonstrate how data is rendered by the `echo` operation, the example uses
the :doc:`./define_context` operation to add a `name` variable to the
`template_variables` dictionary in the context. When rendering, the `echo` operation
reads from the `template_variables` dictionary but uses a separate prefix, or namespace,
defined by `template_variable_prefix`, which defaults to `qwikstart`.

Required context
================

`message`
    Message displayed to user.

Optional context
================

`template_variables`
    |template_variables description|

`template_variable_prefix`
    default: `'qwikstart'`

    |template_variable_prefix description|

`highlight`
    default: `''`

    Name of language used for syntax highlighting using `pygments` library.
    See https://pygments.org/docs/lexers/

Additional notes
================

Overrides default :ref:`opconfig <opconfig>` with:

- `display_description`: `False`

See also
========
- :doc:`context_from_regex`
- :doc:`define_context`
- :doc:`prompt`
