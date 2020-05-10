==============
define_context
==============

.. include:: aliases.rst

Operation to context variables to the operation context.

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
