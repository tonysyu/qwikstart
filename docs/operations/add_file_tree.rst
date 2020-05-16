=============
add_file_tree
=============

.. include:: aliases.rst

Operation to add a file tree (a.k.a. directory) to a project.

Example
=======

The following example uses the :doc:`prompt` operation to prompt the user for a name,
and then uses it to generate a greeting message in one of the rendered files
(`example-file.txt`):

.. literalinclude:: ../../examples/operations/add_file_tree.yml
   :emphasize-lines: 7-12
   :caption: `examples/operations/add_file_tree.yml`

This example references an `add-file-tree` directory, which looks like::

    qwikstart/examples/operations
    ├── add_file_tree.yml
    └── templates
       └── add-file-tree
          ├── subdirectory
          │  └── example-file.txt
          └── {{ qwikstart.dynamic_directory_name }}
             └── {{ qwikstart.dynamic_file_name }}.txt

The :doc:`prompt` operation, by default, adds variables to the `template_variables`
namespace. The operation definition above defines additional template variables, `dynamic_directory_name` and `dynamic_file_name`, which are combined with those in
the `template_variables` from the global context. Running the operation defined above
produces the following::

    ./add-file-tree
    ├── subdirectory
    │  └── example-file.txt
    └── my-dynamic-directory
       └── my-dynamic-file.txt

Required context
================

`template_dir`
    Path to directory containing template files. This path is relative to the
    qwikstart repo directory, which is typically the directory containing the
    `qwikstart.yml` file.

Optional context
================

`target_dir`
    default: Working directory

    Directory where files from `template_dir` will be written. This is relative
    to the current working directory.

`template_variables`
    |template_variables description|

`template_variable_prefix`
    default: `'qwikstart'`

    |template_variable_prefix description|

`ignore`
    List of file patterns to ignore from source directory. Unix-shell-style
    wildcards are accepted. See https://docs.python.org/3/library/fnmatch.html

See also
========
- :doc:`add_file`
- :doc:`prompt`
