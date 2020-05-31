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

Tasks and operations
====================

A qwikstart task definition is simply a `yaml <https://en.wikipedia.org/wiki/YAML>`_
file that defines a series of "steps", a.k.a. "operations". Take the following
hello-world example:

.. code-block:: yaml

   steps:
       "Ask for name":     # 1. Description of operation
           name: prompt    # 2. Name of operation
           opconfig:       # 3. Common operation configuration
               output_namespace: "template_variables"
           inputs:         # 4. Context data specific to the `prompt` operation
               name: "name"
       "Display message":
           name: echo
           message: |
               Hello, {{ qwikstart.name }}!

This task composes two different operations: :doc:`operations/prompt` and
:doc:`operations/echo`. The `prompt` operation is used to prompt the user for a `name`,
and then the `echo` operation displays a greeting.

The :doc:`operations/prompt` operation adds all user inputs into a `template_variables`
dictionary, which is added to the global context. Note that the `output_namespace`
config isn't actually needed since that's the default for the `prompt` operation. It's
added here just for clarity.

The :doc:`operations/echo` operation expects a `template_variables` dictionary as input,
which is used to render the `message`. The :doc:`operations/echo` operation defaults to
`template_variable_prefix = "qwikstart"`, which is why the template variable is rendered
using `qwikstart.name` instead of just `name` as specified in the `inputs` definition.

Anatomy of an operation
-----------------------

As outlined in the inline comments in the example, there are four different parts to
a given operation:

1. The operation description. This is a descriptive string for the operation that is
   used for display purposes and must be unique.
2. `name`, which is the name of the operation being configured. This should be a name
   matching any of the :ref:`available-operations` for qwikstart tasks.
3. `opconfig`, which contains common configuration for qwikstart operations. This is
   described in more detail in the :ref:`opconfig` section.
4. Context data specific to each of the :ref:`available-operations`. For example, the
   `prompt` operation expects a list of `inputs` and the `echo` operation expects
   a `message` string. The docs for :doc:`operations/prompt` and :doc:`operations/echo`
   will have more detail about the optional variables for these operations.

Context data
------------

The context data specified in the operation definition above (comment 4), is just one
way to define context data. That definition is known as "local" context data, since
those definitions only affect the operation where they're defined. To make the concept
of local context clear, we can define `template_variables` for the
:doc:`operations/echo` operation as local context:

.. literalinclude:: ../examples/opconfig/echo_with_local_context.yml
   :language: yaml
   :caption: `examples/opconfig/echo_with_local_context.yml`

Operations can have outputs, which are added to the global context for use by subsequent
operations. The following example uses the :doc:`operations/define_context` operation to
define `template_variables`:

.. literalinclude:: ../examples/opconfig/define_and_echo.yml
   :language: yaml
   :caption: `examples/opconfig/define_and_echo.yml`

Using :doc:`operations/define_context` to add static values isn't that useful, but
operations such as :doc:`operations/context_from_regex`, :doc:`operations/find_files`,
and :doc:`operations/prompt` allow you to write tasks that define context based on the
execution environment and the user.

.. _opconfig:

Common operation configuration
------------------------------

The `opconfig` variable is a dictionary containing optional configuration common to all
qwikstart operations.

`input_mapping` (default: `{}`):
    Dictionary mapping new context variable names, which will be used by the operation,
    to variable names in the global context.
`output_mapping` (default: `{}`):
    Dictionary mapping new context variable names, which will be stored in the global
    context, to variable names returned by the operation.
`input_namespace` (default: `None`):
    String specifying a dictionary in the global context that will be used as input
    variables by the operation *instead of* the variables in the global context.
`output_namespace` (default: `None`):
    String specifying the name of the dictionary in the global context where output
    variables from the operation are stored. By default, this is `None`, which means
    output variables are added directly to the global context. Some operations, notably
    :doc:`operations/prompt`, specify the default of `"template_variables"`, which is
    a special namespace used by many operations when rendering templates.
`display_description` (default: `True`):
    Boolean value controlling whether to display the description of an operation on
    the command line during exection. This defaults to `True` but some operations
    override this default (though it's possible to override that by when configuring an
    operation).

Operation execution sequence
============================

The basic execution sequence is outlined below:

1. Inject global context
2. Remap variables based on `opconfig.input_mapping`
3. Isolate context based on `opconfig.input_namespace`
4. Add variables based on local context
5. Run operation
6. Nest output under namepace in `opconfig.output_namespace`
7. Remap output based on `opconfig.output_mapping`
8. Merge output with global context

Other than the run-operation step in step 5, all the other steps are to control either
of the following:
- The data (i.e. context data) passed to the operation (steps 1-4)
- The data saved to the global context (steps 6-8)

These steps are explained in depth below.

Inject global context
---------------------

The execution sequence starts with an operation's `execute` method, which is passed
the global context. This global context is just a dictionary containing output from
prior operations.

The following example uses the :doc:`operations/define_context` operation to add
a `template_variables` dictionary (containing `name`) to the global context. That
context is injected into the :doc:`operations/echo` operation, which expects
a `template_variables` dictionary used for rendering a `message`:

.. literalinclude:: ../examples/opconfig/define_and_echo.yml
   :language: yaml
   :emphasize-lines: 5-6,10
   :caption: `examples/opconfig/define_and_echo.yml`

Remap variables based on `opconfig.input_mapping`
-------------------------------------------------

Next, variables in the global context can be remapped to new variable names. Operations
expect variables with specific names, so this can be used to combine operations that
weren't initially meant to be combined.

Instead of defining a `template_variables` dictionary directly, the following example
just adds a `name` to the global context. Since the :doc:`operations/echo` operation
expects a `template_variables` dictionary, we can use the `input_mapping` to remap the
`name` to `template_variables.name`, below), for use when rendering the template:

.. literalinclude:: ../examples/opconfig/define_and_echo_with_input_mapping.yml
   :language: yaml
   :emphasize-lines: 5,9-10,12
   :caption: `examples/opconfig/define_and_echo_with_input_mapping.yml`

Note that the period in `template_variables.name` is a namespace separator.

Isolate context based on `opconfig.input_namespace`
---------------------------------------------------

Here, a "namespace" is really just a dictionary nested within the global context
dictionary. If an `input_namespace` is specified, then only the data within the
sub-dictionary will continue on this journey. Otherwise, the entire global context is
passed along.

The following example uses the :doc:`operations/define_context` operation to define
a dictionary with the key `context_for_echo` containing a `template_variables`
dictionary with the `name` that will be rendered by the :doc:`operations/echo`
operation. To use `template_variables` for rendering, the `echo` operation selects
the `context_for_echo` dictionary from the global context using `input_namespace`:

.. literalinclude:: ../examples/opconfig/define_and_echo_with_input_namespace.yml
   :language: yaml
   :emphasize-lines: 5-7,11,13
   :caption: `examples/opconfig/define_and_echo_with_input_namespace.yml`

Note that the mapping is defined using the source name as the key, and the target name
as the value.

Add variables based on local context
------------------------------------

The final step before running the operation is to add in the "local" context, which is
just data defined as part of the operation. For example, the following defines the
`echo` operation, with a local context variable, `message`:

.. code-block:: yaml
    :emphasize-lines: 4

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

The following example uses the :doc:`operations/define_context` operation to define
a `name`, which is then put in a `template_variables` dictionary using the
`output_namespace` operation config:

.. literalinclude:: ../examples/opconfig/define_and_echo_with_output_namespace.yml
   :language: yaml
   :emphasize-lines: 5,7,11
   :caption: `examples/opconfig/define_and_echo_with_output_namespace.yml`


Remap output based on `opconfig.output_mapping`
-----------------------------------------------

The output data from an operation can be renamed using an `opconfig.output_mapping`,
just like inputs were renamed using `opconfig.input_mapping`.

The following example uses the :doc:`operations/define_context` operation to define
a `name`, which is then put in a `template_variables` dictionary using the
`output_mapping` operation config:

.. literalinclude:: ../examples/opconfig/define_and_echo_with_output_mapping.yml
   :language: yaml
   :emphasize-lines: 5,7-8,12
   :caption: `examples/opconfig/define_and_echo_with_output_mapping.yml`

Note that the mapping is defined using the source name as the key, and the target name
as the value.

Merge output with global context
--------------------------------

Finally, the output variables can be merged with the global context for subsequent
commands to use.
