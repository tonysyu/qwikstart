==================
search_and_replace
==================

.. include:: aliases.rst

Operation for searching for text and replacing it with new text.

Required context
================

`file_path`
    Path to file relative to the current working directory.

`search`
    Text to search for in file.

`replace`
    Text used to replace text matching `search`.

Optional context
================

`use_regex`
    default: `False`

    Use `re.sub` instead of `str.replace`.
