===========
insert_text
===========

.. include:: aliases.rst

Operation inserting text on a given line

Required context
================

`file_path`
    |file_path description|

`text`
    Text that will be inserted.

`line`
    Line number where text will be inserted.

`column`
    Column where the text will be inserted.

Optional context
================

`line_ending`
    default: `'\n'`

    Text appended to the end of inserted text.

`match_indent`
    default: `True`
