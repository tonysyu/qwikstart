=========
edit_json
=========

.. include:: aliases.rst

Operation to edit json by merging data into existing json data.

Example
=======

The following example adds/updates the `test` script in a `package.json` file:

.. literalinclude:: ../../examples/operations/edit_json.yml
   :language: yaml
   :emphasize-lines: 3-8
   :caption: `examples/operations/edit_json.yml`

Required context
================

`file_path`
    |file_path description|

`merge_data`
    Dictionary of data that will be merged into existing data in json file.

Optional context
================

`indent`
    default: 4

See also
========
- :doc:`edit_yaml`
