*************
General Usage
*************

.. include:: <isonum.txt>
.. include:: <isopub.txt>

.. contents:: Contents:
   :depth: 2

Overview
========

The NRN pipeline is separated into 4 distinct processes which are intended to be executed in sequence:

1. ``conform``: Standardization and harmonization of data source(s) into NRN format.
2. ``confirm``: Generation and recovery of National Unique Identifiers (NIDs).
3. ``validate``: Enforcement of a set of validations and restrictions on NRN dataset geometry and attribution.
4. ``export``: Configuration and export of required product distribution formats.

.. figure:: /source/_static/figures/nrn_process_diagram.png
    :alt: NRN process diagram

    Figure 1: NRN process diagram.

Implementation
==============

Each NRN process is implemented as a Command Line Interface (CLI) tool which can be called from any shell. The
parameters for each CLI tool are largely the same, with ``source`` (provincial / territorial source abbreviation) being
the only universal and required parameter for all CLI tools. Specific reference information, including parameter
specifications, can be displayed by passing :code:`--help` to the CLI tool.

.. admonition:: Note

    It is strongly recommended to use the NRN pipeline within the ``nrn-rrn`` conda environment. Otherwise, the
    expected output and behaviour, as documented, cannot be guaranteed. conda environments can be activated via:
    :code:`conda activate nrn-rrn`.

Examples
========

Execution of an NRN process::

    python conform.py bc -r

Displaying reference information for an NRN process::

    python conform.py --help

Post-Processing Tasks
=====================

After completion of the full NRN pipeline, the following manual tasks must be performed:

1. Copy output documents to NRN repository, overwriting existing files:

  i. From ``nrn-rrn/data/processed/<source>.zip/en/completion_rates.yaml`` to ``nrn-rrn/src/export/distribution_docs/completion_rates.yaml``.
  ii. From ``nrn-rrn/data/processed/<source>.zip/en/release_notes.yaml`` to ``nrn-rrn/src/export/distribution_docs/release_notes.yaml``.
  iii. From ``nrn-rrn/data/processed/<source>.zip/en/completion_rates.rst`` to ``nrn-rrn/docs/source/en/product_documentation/completion_rates.rst``.
  iv. From ``nrn-rrn/data/processed/<source>.zip/en/release_notes.rst`` to ``nrn-rrn/docs/source/en/product_documentation/release_notes.rst``.
  v. From ``nrn-rrn/data/processed/<source>.zip/fr/completion_rates.rst`` to ``nrn-rrn/docs/source/fr/product_documentation/completion_rates.rst``.
  vi. From ``nrn-rrn/data/processed/<source>.zip/fr/release_notes.rst`` to ``nrn-rrn/docs/source/fr/product_documentation/release_notes.rst``.

2. Copy processed data to the relevant NRN server under subdirectory: ``5_Process``.
3. Unzip output WMS data and copy GeoPackage (``NRN_<SOURCE>_WMS.gpkg``) to relevant NRN server under subdirectory: ``7_Disseminate/wms``.
4. Notify relevant individuals of new NRN release via email.