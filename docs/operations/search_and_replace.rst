==================
search_and_replace
==================

.. include:: aliases.rst

Operation for searching for text and replacing it with new text.

Example
=======

The following example uses the `search_and_replace` operation to replace the greeting
in the `basic-hello-world.yml` example:

.. literalinclude:: ../../examples/operations/search_and_replace.yml
   :language: yaml
   :caption: `examples/operations/search_and_replace.yml`

Running this operation replaces "Hello" with "Hola" within the file.

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

See also
========
- :doc:`append_text`
- :doc:`find_tag_and_insert_text`
- :doc:`find_tagged_line`
- :doc:`insert_text`
