========================
Understanding operations
========================

Qwikstart operations (a.k.a. the steps of a qwikstart task) comprise the core
functionality of qwikstart. Typically, a single operation does something quite simple,
but they are combined to perform more complex tasks.

While operations are mostly independent, an operation can affect other operations by:

1. Modifying the filesystem
2. Modifying the global context

The global context is really just a Python dictionary with variables passed from one
operation to the next. Operations can choose which variables they want to use from the
global context and add or update variables in the global context, as desired.

Operation execution sequence
============================

The basic execution sequence is outlined below:

- Inject global context
- Remap variables based on `opconfig.input_mapping`
- Isolate context based on `opconfig.input_namespace`
- Add variables based on local context
- Run operation
- Nest output under namepace in `opconfig.output_namespace`
- Remap output based on `opconfig.output_mapping`
- Merge output with global context

These steps are explained in depth below.

Inject global context
---------------------

The execution sequence starts with an operation's `execute` method, which is passed
the global context. This global context is just a dictionary containing output from
prior operations.

For example, the `find_tagged_line` operation adds `line` and `column` variables to the
global context. These variables then be used by the `insert_text` operation.

Remap variables based on `opconfig.input_mapping`
-------------------------------------------------

Next, variables in the global context can be remapped to new variable names. Operations
expect variables with specific names, so this can be used to combine operations that
weren't initially meant to be combined.

Isolate context based on `opconfig.input_namespace`
---------------------------------------------------

Here, a "namespace" is really just a dictionary nested within the global context
dictionary. If an `input_namespace` is specified, then only the data within the
sub-dictionary will continue on this journey. Otherwise, the entire global context is
passed along.

Add variables based on local context
------------------------------------

The final step before running the operation is to add in the "local" context, which is
just data defined as part of the operation. For example, the following defines the
`echo` operation, with a local context variable, `message`:

.. code-block:: yaml

    steps:
        "Display message":
            name: echo
            message: "Hello"

This local context gets combined with the global context (after remapping and
namespacing) to form the operation context.

Run operation
-------------

Finally, the actual work of the operation gets done. The operation context, which was
created by the steps described above, is used to do whatever the operation wants using
the operation's `run` method. As part of this, the operation can return any data that it
wants added to the global context.

After the operation is run, we basically rewind the steps from above.

Nest output under namepace in `opconfig.output_namespace`
---------------------------------------------------------

The output from the operation (if there is any), can optionally be nested under
a namespace. In other words, it can be placed in a subdictionary in the global context.

Remap output based on `opconfig.output_mapping`
-----------------------------------------------

The output data from an operation can be renamed using an `opconfig.output_mapping`,
just like inputs were renamed using `opconfig.input_mapping`.

Merge output with global context
--------------------------------

Finally, the output variables can be merged with the global context for subsequent
commands to use.
