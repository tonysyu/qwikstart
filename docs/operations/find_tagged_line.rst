================
find_tagged_line
================

.. include:: aliases.rst

Operation for finding a line in a file containing a text "tag".

Required context
================

`file_path`
    Path to file relative to the current working directory.

`tag`
    Text used as a placeholder for detecting where to insert text. For example::

        # qwikstart: inject-line-below

Output
======

`line`
    Line number where the text was found.

`column`
    Column where the start of the matching text was found.
