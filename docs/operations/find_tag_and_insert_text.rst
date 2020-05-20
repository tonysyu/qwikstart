========================
find_tag_and_insert_text
========================

.. include:: aliases.rst

Operation to find a tag and insert text below that tag.

This is a simple combination of the :doc:`find_tagged_line` and :doc:`insert_text`
operations.

Example
=======

The following example inserts `text` to a file named `settings.py` by first searching
for a string matching the `tag` `"# qwikstart: middleware"`:

.. literalinclude:: ../../examples/operations/find_tag_and_insert_text.yml
   :language: yaml
   :caption: `examples/operations/find_tag_and_insert_text.yml`

Before this operation is run, `settings.py` would have the following code:

.. code-block:: python
    :emphasize-lines: 4

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        # qwikstart: middleware
    ]

After running the operation, the `text` is inserted below the tag:

.. code-block:: python
    :emphasize-lines: 5

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

`tag`
    Text used as a placeholder for detecting where to insert text. For example::

        # qwikstart: inject-line-below

`text`
    Text that will be inserted.

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
- :doc:`find_tagged_line`
- :doc:`insert_text`
- :doc:`search_and_replace`
