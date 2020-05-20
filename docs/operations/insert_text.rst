===========
insert_text
===========

.. include:: aliases.rst

Operation inserting text on a given line

Example
=======

The following example inserts `text` into a file named `settings.py`:

.. literalinclude:: ../../examples/operations/insert_text.yml
   :language: yaml
   :emphasize-lines: 7-9
   :caption: `examples/operations/insert_text.yml`

To set up this example, we first use the :doc:`find_tagged_line` operation to find the
`line` number and `column` number where the tag `"# qwikstart: middleware"`. These
values are added to the global context and match variables expected by `insert_text`.
The `insert_text` operation will then insert text below the tagged line:

.. code-block:: python
    :emphasize-lines: 4-5

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        # qwikstart: middleware
        "django.contrib.auth.middleware.AuthenticationMiddleware",
    ]

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
    default: `'\\n'`

    Text appended to the end of inserted text.

`match_indent`
    default: `True`

See also
========
- :doc:`append_text`
- :doc:`find_tag_and_insert_text`
- :doc:`find_tagged_line`
- :doc:`search_and_replace`
