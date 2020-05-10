========================
find_tag_and_insert_text
========================

.. include:: aliases.rst

Operation to find a tag and insert text below that tag.

This is a simple combination of the `find_tagged_line` and `insert_text` operations.


Required context
================

`file_path`
    |file_path description|

`tag`
    Text used as a placeholder for detecting where to insert text. For example::

        # qwikstart: inject-line-below

`text`
    Text that will be inserted.

Optional context
================

`line_ending`
    default: `'\n'`

    Text appended to the end of inserted text.

`match_indent`
    default: `True`
