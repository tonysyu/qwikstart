================
find_tagged_line
================

.. include:: aliases.rst

Operation for finding a line in a file containing a text "tag".

Example
=======

The following example inserts `text` to a file named `settings.py` by first searching
for a string matching the `tag` `"# qwikstart: middleware"`:

.. literalinclude:: ../../examples/operations/find_tagged_line.yml
   :language: yaml
   :emphasize-lines: 3-5
   :caption: `examples/operations/find_tagged_line.yml`

The `settings.py` file has the following text:

.. code-block:: python
    :emphasize-lines: 4

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        # qwikstart: middleware
    ]

The `find_tagged_line` operation adds the `line` number and `column` number to the
global context. The names of these values match inputs expected by the
:doc:`insert_text` operation, which will insert text below the tagged line.


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

See also
========
- :doc:`find_tag_and_insert_text`
- :doc:`insert_text`
- :doc:`search_and_replace`
