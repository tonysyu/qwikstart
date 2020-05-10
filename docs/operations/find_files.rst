==========
find_files
==========

.. include:: aliases.rst

Operation to search for text within files and return match file paths. Matching files
are stored in a list of `matching_files`, but the name can be specified using
`output_name`.

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
