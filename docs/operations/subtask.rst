=======
subtask
=======

.. include:: aliases.rst

Operation for running subtask defined by qwikstart task definition file.

Example
=======

The following example uses the `subtask` operation ro runs the example task for the
:doc:`echo` operation:

.. literalinclude:: ../../examples/operations/subtask.yml
   :language: yaml
   :caption: `examples/operations/subtask.yml`

Required context
================

`file_path`
    |file_path description|

    This path should point to a qwikstart task definition file, which will be executed
    by the `subtask` operation.

Optional context
================

`subcontext`
    Dictionary of variables passed to subtask.

Output
======

This operation can define arbitrary output values based on the operations run by the
subtask.

See also
========
- :doc:`echo`
