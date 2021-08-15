
Table Meta
^^^^^^^^^^

It's a universal class that created to be a middleware, universal mapping for data from different parsers - simple-ddl-parser and py-models-parser.

Based on this middleware 2 libraries are worked - omymodels & fakeme. 

It's allow create 1 adapter for different inputs and produce output only on one standard - easy to maintain ad add different output variants.

All classes - Pydantic classes, so you can do with them anything that you can with Pydantic classes.

Library contains 2 different classes - TableMeta - main class to convert input relative to models or tables. Second - Type, for Enum types data.

How it use
^^^^^^^^^^

Install
-------

.. code-block:: bash


       pip install table-meta

Usage
-----

.. code-block:: python


   from table_meta import TableMeta

   data = {your_table_definition}

   table_data = TableMeta(**data)

Convert simple-ddl-parser input to TableMeta
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Simple-ddl-parser: https://github.com/xnuinside/simple-ddl-parser

Pay attention that TableMeta expected data from simple-ddl-parser , that created with flag 'group_by_type=True'
Example: result = DDLParser(ddl).run(group_by_type=True, output_mode="bigquery")

To convert simple-ddl-parser output to TableMeta - use method: ddl_to_meta()

Usage example:

.. code-block:: python


       from simple_ddl_parser import DDLParser
       from table_meta import ddl_to_meta

       ddl = "your ddl"
       parser_result = DDLParser(ddl).run(group_by_type=True, output_mode="bigquery")
       data = ddl_to_meta(parser_result)

       # ddl_to_meta returns Dict with 2 keys {"tables": [], "types": []} inside lists you will have Table Meta a models

       print(data)

Convert py-model-parser input to TableMeta
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Py-models-parser: https://github.com/xnuinside/py-models-parser

Usage example:

.. code-block:: python


       from py_models_parser import parse
       from table_meta import models_to_meta

       model_from = "your python models, supported by parser"
       result = parse(model_from)
       data = models_to_meta(result)

       # models_to_meta returns Dict with 2 keys {"tables": [], "types": []} inside lists you will have a Table Meta models

       print(data)

Changelog
---------

**v0.1.0**


#. Table Meta moved from O!MyModels to separate library. To make it re-usebale in fakeme library.
