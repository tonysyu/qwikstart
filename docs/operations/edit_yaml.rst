=========
edit_yaml
=========

.. include:: aliases.rst

Operation to edit yaml by merging data into existing yaml data.

Example
=======

The following example adds the `redis` service to a `docker-compose.yml` file:

.. literalinclude:: ../../examples/operations/edit_yaml.yml
   :language: yaml
   :emphasize-lines: 3-8
   :caption: `examples/operations/edit_yaml.yml`

Note that `merge_data` can specify arbitrarily nested data. This data will be merged
with existing data, so other `services` defined in the file will be preserved.

Required context
================

`file_path`
    |file_path description|

`merge_data`
    Data that will be merged into existing data in yaml file.

See also
========
- :doc:`edit_json`
- :doc:`find_files`
