===========
append_text
===========

.. include:: aliases.rst

Operation for appending text to a given file.

Example
=======

The following example appends text to a file named `README.rst`:

.. literalinclude:: ../../examples/operations/append_text.yml
   :language: yaml
   :caption: `examples/operations/append_text.yml`

Note that the pipe character (`|`) used above is an example of
`yaml's multi-line string syntax`_. This task assumes that there's a file named
`README.rst` in the working directory and will fail if that file doesn't exist.

.. _yaml's multi-line string syntax: https://yaml-multiline.info/

Required context
================

`file_path`
    |file_path description|

`text`
    Text that will be appended to `file_path`

Optional context
================

`prefix`
    default: `'\n'`

    Text added before appended `text`

`suffix`
    default: `''`

    Text added after appended `text`

See also
========
- :doc:`find_files`
- :doc:`find_tag_and_insert_text`
- :doc:`find_tagged_line`
- :doc:`insert_text`
- :doc:`search_and_replace`
