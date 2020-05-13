====================
Qwikstart operations
====================

Qwikstart operations (a.k.a. the steps of a qwikstart task) comprise the core
functionality of qwikstart. Typically, a single operation does something quite simple,
but they are combined to perform more complex tasks. This section summarizes the core
operations available.

See the section on :doc:`./understanding_operations` for more background on how
operations work.

.. _available-operations:

Available operations
====================

For examples the in this guide, we'll be using example files from the
`qwikstart/examples/operations`_ directory in the qwikstart project repo, which looks
something like::

    qwikstart
    └── examples
        └── operations
            ├── templates
            │   ├── hello_world.txt
            │   └── ...
            ├── add_file.yml
            └── ...

.. toctree::
   :maxdepth: 1

   operations/add_file
   operations/add_file_tree
   operations/append_text
   operations/context_from_regex
   operations/define_context
   operations/echo
   operations/edit_json
   operations/edit_yaml
   operations/find_files
   operations/find_tag_and_insert_text
   operations/find_tagged_line
   operations/insert_text
   operations/prompt
   operations/search_and_replace
   operations/shell

.. _qwikstart/examples/operations:
   https://github.com/tonysyu/qwikstart/tree/master/examples/operations
