======
prompt
======

.. include:: aliases.rst

Operation to prompt user for input values.

The input values will be added to a dictionary in the context with a name matching
`output_dict_name`.

Example
=======

The following example uses the `prompt` operation to get two inputs: First, it prompts
for a `name` to greet, and then prompts for a `greeting` message:

.. literalinclude:: ../../examples/operations/prompt.yml
   :language: yaml
   :emphasize-lines: 3-14
   :caption: `examples/operations/prompt.yml`

These inputs are then displayed in the terminal using the :doc:`echo` operation. The
prompt for `"name"` sets a default of `"World"` and provides a message to help the user
provide an input. Only the `name` field is required.

The `greeting` message defines a set of `choices` which limits the input to predefined
choices for the input. The selection of choices is presented as a numeric input::

    Select greeting:
    1 - Hello
    2 - Hola
    3 - Howdy
    Choose from 1, 2, 3:

By default, the output for `prompt` is added to the `template_variables` namespace, so
output variables can be used for rendering in the :doc:`echo` operation without
explicitly specifying `output_namespace` (see :ref:`opconfig`).

Required context
================

`inputs`
    List of dictionaries describing prompts for user inputs.
    Each dictionary can have the following keys:

    `name`
        The name of the variable being defined.
    `default`
        Optional default value of variable. Note that this can be defined as
        a template string, with variables defined in previous prompts or from
        template variables in the context. For example::

            - name: "name"
              default: "World"
            - name: "message"
              default: "Hello {{ qwikstart.name }}!"

    `help_text`
        Optional info presented to users when responding to prompts.
    `choices`
        A list of allowed choices.
    `choices_from`
        The name of a template variable in `template_variables` mapping to a list of
        allowed choices.

Optional context
================

`introduction`
    default: `'Please enter the following information:'`

    Message to user before prompting for inputs.

`template_variables`
    |template_variables description|

`template_variable_prefix`
    default: `'qwikstart'`

    |template_variable_prefix description|

Output
======

This operation can define arbitrary output values based on the values of `name` defined
in `inputs`.

See also
========
- :doc:`echo`
