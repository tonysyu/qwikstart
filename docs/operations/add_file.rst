========
add_file
========

.. include:: aliases.rst

Operation used to add files to a project. This copies a file located in the qwikstart
repository (`template_path`) to a path relative to the working directory
(`target_path`).

Example
=======

The following example uses the :doc:`prompt` operation to prompt the user for a name,
and then uses it to generate a greeting message:

.. literalinclude:: ../../examples/operations/add_file.yml
   :emphasize-lines: 7-9
   :caption: `examples/operations/add_file.yml`

This example uses the following template (path relative to qwikstart definition file):

.. literalinclude:: ../../examples/operations/templates/hello_world.txt
   :caption: examples/operations/templates/hello_world.txt

Note that template variables (in this case, `name`) default to using `qwikstart` as
a prefix, when rendered in templates. This can be controlled using the
`template_variable_prefix` option described below. By default, the :doc:`prompt`
operation adds variables to the `template_variables` namespace, which is used when
rendering the template.

Required context
================

`target_path`
    File path where rendered template will be saved. This will be relative to
    the current working directory.

`template_path`
    Path to template file relative qwikstart repo directory, which is typically
    the directory containing the `qwikstart.yml` file.

Optional context
================

`template_variables`
    |template_variables description|

`template_variable_prefix`
    default: `'qwikstart'`

    |template_variable_prefix description|

See also
========
- :doc:`add_file_tree`
- :doc:`prompt`
