***
WMS
***

.. include:: <isonum.txt>
.. include:: <isopub.txt>

.. contents:: Contents:
   :depth: 3

Overview
========

A WMS is not a required distribution format for the NRN, therefore there are no specifications for its design. The
current WMS implementation was developed based on reviewing the available data for each of the provincial / territorial
NRN products and developing a hierarchical display and labelling scheme based on a meaningful structuring of the data.

The WMS is constructed using an ArcGIS Pro project: ``nrn-rrn/wms/nrn_rrn_wms.aprx``. Any modifications to this file
must be followed by copying the file to the NRN data server (since that server is not intended to hold the repository).

WMS Structure
=============

.. code-block:: yaml

    50,000,000:
      Display: Trans-Canada Highway.
      Labels: None.
    4,000,000:
      Display: National Highway System.
      Labels: Route numbers for Trans-Canada Highway.
    500,000:
      Display: All major roads.
      Labels: Route numbers for National Highway System.
    100,000:
      Display: All roads, except alleyways.
      Labels: All route numbers.
    50,000:
      Display: No changes.
      Labels: Street names for major roads.
    10,000:
      Display: All roads, blocked passages, and toll points.
      Labels: Street names for all roads.

Configuration
=============

WMS Queries
-----------

WMS data is defined by queries contained within the file: ``nrn-rrn/src/export/wms_queries.yaml``.

Structure
^^^^^^^^^

**Generic structure:**: ::

    queries:
      <attribute name>:
        <source abbreviation>:
          <query content>

**Example:**: ::

    queries:
      wms_50m:
        nb: "(rtnumber1 in ('2', '16') or rtnumber2 in ('2', '16'))"

**Example:**: ::

    queries:
      wms_500k:
        sk:
          - "(roadclass in ('Freeway', 'Expressway / Highway', 'Arterial'))"
          - "((l_placenam.str.lower() = 'regina' or r_placenam.str.lower() = 'regina') and (roadclass = 'Collector'))"

Content
^^^^^^^

:Attribute name: Desired attribute to be added to the interim NRN roadseg dataset. Query results will assign a value of
                 ``1`` to the attribute which can then be used, as needed, in the WMS project file.
:Source abbreviation: Provincial / territorial abbreviation. Used to indicate which NRN source the queries are intended
                      for.
:Query content: Single query, list of queries, or the keyword ``all`` (which uses all dataset records). Queries must
                use the syntax of :func:`pandas.DataFrame.query()`.

WMS Data
--------

WMS data is exported alongside other distribution formats and is defined in
``nrn-rrn/src/export/distribution_formats/en/wms.yaml``. Only the English output definition is required since the WMS
data is bilingual and dataset names and attributes are not made available to WMS users. The structure of this file
follows that of the other distribution format, purely for consistency.

This file is used to define the desired output schema of the WMS data, which is intended to be used in the WMS project
file.