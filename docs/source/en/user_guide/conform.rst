*******
Conform
*******

.. include:: <isonum.txt>
.. include:: <isopub.txt>

.. contents:: Contents:
   :depth: 3

Overview
========

The `conform` process uses one or more ``YAML`` (.yaml) configuration file(s) to define the mapping of source data to
the NRN schema.

The NRN schema is defined in :doc:`feature_catalogue`.

Ideally, source data would adhere to the NRN schema and have direct (1:1) field mapping. Unfortunately, this does not
reflect reality. Therefore, to accommodate the integration of as many data sources as possible, a number of functions
have been developed to manipulate source data for integration into the NRN data model.

:Field Mapping: The process of source data integration into the NRN data model.
:Key: Individual attribute of a YAML file.
:YAML: Data serialization language commonly used for configuration files.

Configuration Overview
======================

Directories
-----------

Root Directory
^^^^^^^^^^^^^^

The ``root`` directory for all configuration files is: ``nrn-rrn/src/conform/sources``.

Subdirectories
^^^^^^^^^^^^^^

Each configuration file must reside within a subdirectory of ``root``, where the subdirectory name is the provincial /
territorial abbreviation of the data source. Accepted source abbreviations are as follows:

.. csv-table::
   :header: "Abbreviation", "Source (Province / Territory)"
   :widths: auto
   :align: left

   "ab", "Alberta"
   "bc", "British Columbia"
   "mb", "Manitoba"
   "nb", "New Brunswick"
   "nl", "Newfoundland and Labrador"
   "ns", "Nova Scotia"
   "nt", "Northwest Territories"
   "nu", "Nunavut"
   "on", "Ontario"
   "pe", "Prince Edward Island"
   "qc", "Quebec"
   "sk", "Saskatchewan"
   "yt", "Yukon"

Files
-----

File Names
^^^^^^^^^^

Individual configuration file names do not matter, so long as they have the required ``.yaml`` extension.

File Integrity
^^^^^^^^^^^^^^

Each source dataset (file or layer) must be defined within its own configuration file. Similarly, each NRN dataset must
only be defined in a single configuration file per source subdirectory, otherwise the results will be overwritten by
subsequent configuration files which map to the same NRN dataset.

Structure
---------

Generic structure::

    src
    ├── conform
    │   ├── sources
    │   │   ├── <source abbreviation>
    │   │   │   ├── <configuration file name>.yaml
    │   │   │   ├── <configuration file name>.yaml
    │   │   │   ...

Specific structure (source: `GeoNB`)::

    src
    ├── conform
    │   ├── sources
    │   │   ├── nb
    │   │   │   ├── geonb_nbrn-rrnb_ferry-traversier.yaml
    │   │   │   └── geonb_nbrn-rrnb_road-route.yaml

Configuration Content
=====================

Configuration files consist of 3 main components (sections):

:Metadata: Source metadata.
:Data: Source file and layer properties.
:Conform: Field mapping definitions.

Metadata
--------

The metadata components define all relevant details about the source data. No metadata keys are mandatory but it is
strongly encouraged to populate as many metadata keys as possible as it is the primary reference used to contextualize
and refer back to the data source, if ever required.

Structure
^^^^^^^^^

Generic structure:

.. code:: yaml

    coverage:
      country:
      province:
      ISO3166:
        alpha2:
        country:
        subdivision:
      website:
      update_frequency:
    license:
      url:
      text:
    language:

Specific structure (source: `GeoNB`):

.. code:: yaml

    coverage:
      country: ca
      province: nb
      ISO3166:
        alpha2: CA-NB
        country: Canada
        subdivision: New Brunswick
      website: https://geonb-t.snb.ca/downloads/nbrn/geonb_nbrn-rrnb_orig.zip
      update_frequency: weekly
    license:
      url: http://geonb.snb.ca/documents/license/geonb-odl_en.pdf
      text: GeoNB Open Data License
    language: en

Data
----

The data components define the properties of the source file and layer relevant to constructing an NRN dataset.

Mandatory keys:

:filename: Name of the source file, including the extension.
:driver: OGR vector driver name (see: https://gdal.org/drivers/vector/index.html).
:crs: Coordinate Reference System authority string.
:spatial: Flag to indicate if the source is spatial.

Optional keys:

:layer: Layer name for files containing data layers.
:query: Query used to filter data source records.

Structure
^^^^^^^^^

Generic structure:

.. code:: yaml

    data:
      filename:
      layer:
      driver:
      crs:
      spatial:
      query:

Specific structure (source: `GeoNB`):

.. code:: yaml

    data:
      filename: geonb_nbrn-rrnb.gdb
      layer: Road_Segment_Entity
      driver: OpenFileGDB
      crs: "EPSG:2953"
      spatial: True
      query: "Functional_Road_Class != 425"

Conform
-------

The conform components define the field mapping between the source data and NRN schema. Field mapping can be either
direct (source attribute directly maps to an NRN data attribute) or make use of a series of functions.

Structure
^^^^^^^^^

Generic structure:

.. code:: yaml

    conform:
      <NRN dataset>:
        <NRN dataset attribute>: <field mapping>
        ...
      ...

No Field Mapping
^^^^^^^^^^^^^^^^

Keys for NRN datasets or attributes without any source field mapping can be excluded from the configuration file or
simply left empty.

Direct Field Mapping
^^^^^^^^^^^^^^^^^^^^

NRN attributes with a direct field mapping from the source can be populated with a literal value or attribute name. The
specified value is determined to be an attribute name if it exists in the set of attributes for the source file / layer.

Example:

.. code:: yaml

    accuracy: Element_Planimetric_Accuracy

Field Mapping Functions
^^^^^^^^^^^^^^^^^^^^^^^

To define a field mapping function, the following tags must be used:

:fields: An attribute name or list of attribute names of the source file / layer.
:functions: A list of function names and function-specific parameters. The first key in each listed function must be
            ``function`` followed by the function name.

When multiple field mapping functions are defined, the output of each function is the input to the next function.

Structure
"""""""""

Generic structure:

.. code:: yaml

    <NRN dataset attribute>:
      fields: <source attribute> or [<source attribute>, ...]
      functions:
        - function: <function name>
          <function parameter name>: <function parameter value>
          ...
        - ...

Function: ``apply_domain``
""""""""""""""""""""""""""

**Description:** Enforces the domain restrictions from a specified NRN dataset attribute.

**Accepts Multiple Source Attributes:** No.

**Parameters:**

.. csv-table::
   :header: "Parameter", "Value"
   :widths: auto
   :align: left

   "table", "NRN dataset name."
   "field", "NRN attribute name."
   "default", "Default value to be used if an error is encountered."

Function: ``concatenate``
"""""""""""""""""""""""""

**Description:** Concatenates values into a single string.

**Accepts Multiple Source Attributes:** Yes.

**Parameters:**

.. csv-table::
   :header: "Parameter", "Value"
   :widths: auto
   :align: left

   "columns", "List of source attribute names."
   "separator", "Delimiter string used to join the values."

Function: ``direct``
""""""""""""""""""""

**Description:** Directly maps the given value with optional type casting. This function is purely intended to provide
a function call for direct field mapping.

**Accepts Multiple Source Attributes:** No.

**Parameters:**

.. csv-table::
   :header: "Parameter", "Value"
   :widths: auto
   :align: left

   "cast_type", "String name of a Python type class to be casted to. Accepted values: ``float``, ``int``, ``str``."

Function: ``map_values``
""""""""""""""""""""""""

...

Function: ``query_assign``
""""""""""""""""""""""""""

...

Function: ``regex_find``
""""""""""""""""""""""""

...

Function: ``regex_sub``
"""""""""""""""""""""""

...

Field Mapping Functions - Special Keys
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Process Separately
""""""""""""""""""

...

Iterate Columns
"""""""""""""""

...

Field Domains
"""""""""""""

...

Address Segmentation
====================

...