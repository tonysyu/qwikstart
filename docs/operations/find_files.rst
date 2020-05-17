==========
find_files
==========

.. include:: aliases.rst

Operation to search for text within files and return match file paths. Matching files
are stored in a list of `matching_files`, but the name can be specified using
`output_name`.

Example
=======

The following example searches for qwikstart examples that use the :doc:`shell`
operation:

.. literalinclude:: ../../examples/operations/find_files.yml
   :language: yaml
   :emphasize-lines: 3-7
   :caption: `examples/operations/find_files.yml`

In addition to searching, this example takes the output of the search and passes it to
the :doc:`prompt` operation. Using the `prompt` input's `choices_from` option allows the
user to select one of the `matching_files` found by `find_files`.

In order to use the `matching_files` output from the `find_files` operation, it's saved
to the `template_variables` namespace by defining
`output_namespace = "template_variables"`. See :doc:`../understanding_operations` and
the docs for the :doc:`prompt` operation for more info.

To complete the example, the :doc:`shell` operation is used to print the contents of the
file to the terminal.

Optional context
================

`regex`
    default: `''`

    Regex to search for in files

`directory`
    default: `'.'`

    Root directory for search (defaults to working directory).

`output_name`
    default: `'matching_files'`

    Variable name where list of matching files is stored.

`path_filter`
    default: `None`

    File filter string passed to `fnmatch` before searching. This can be used
    to speed up searching for large repositories.

    For example, you can limit text search to json files using `"*.json"`.

`regex_flags`
    |regex_flags description|


Output
======

This operation returns a list of file paths in a variable defined by `output_name`.


See also
========
- :doc:`find_tag_and_insert_text`
- :doc:`find_tagged_line`
- :doc:`prompt`
- :doc:`search_and_replace`
- :doc:`shell`
