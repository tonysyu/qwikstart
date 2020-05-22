==============
define_context
==============

.. include:: aliases.rst

Operation to context variables to the operation context.

Example
=======

The following example adds a dictionary named `template_variables` with a single
variable named `name` to the context:

.. literalinclude:: ../../examples/operations/define_context.yml
   :language: yaml
   :emphasize-lines: 3-6
   :caption: `examples/operations/define_context.yml`

To complete the example, the variable is used by the :doc:`./echo` operation to display
a simple hello-world greeting. Note that the `template_variables` dictionary, a.k.a.
namespace, is used by default when rendering templates by the `echo` operation, and
any other operations that render templates.

Required context
================

`context_defs`
    Definition of variables to add to the context. Values can be defined using
    template variables; e.g.::

        context_defs:
            greeting: "Hello {{ qwikstart.name }}!"

Optional context
================

`template_variables`
    |template_variables description|

`template_variable_prefix`
    default: `'qwikstart'`

    |template_variable_prefix description|

Output
======

This operation can define arbitrary output values based on `context_defs`.

Additional notes
================

Overrides default :ref:`opconfig <opconfig>` with:

- `display_description`: `False`

See also
========
- :doc:`context_from_regex`
- :doc:`echo`
- :doc:`prompt`
