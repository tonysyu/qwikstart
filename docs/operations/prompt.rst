======
prompt
======

.. include:: aliases.rst

Operation to prompt user for input values.

The input values will be added to a dictionary in the context with a name matching
`output_dict_name`.


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
