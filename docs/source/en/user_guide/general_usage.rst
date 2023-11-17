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

#. Copy output documents to NRN repository, overwriting existing files:

   i. From ``nrn-rrn/data/processed/<source>.zip/distribution_docs/en/release_notes.yaml`` to ``nrn-rrn/src/export/distribution_docs/data/release_notes.yaml``.
   ii. From ``nrn-rrn/data/processed/<source>.zip/distribution_docs/en/release_notes.rst`` to ``nrn-rrn/docs/source/en/product_documentation/release_notes.rst``.
   iii. From ``nrn-rrn/data/processed/<source>.zip/distribution_docs/fr/release_notes.rst`` to ``nrn-rrn/docs/source/fr/product_documentation/release_notes.rst``.


#. Use ``git`` to ``commit`` and ``push`` the updated documentation files to the repository.

#. Copy processed data to the relevant NRN server under subdirectory: ``5_Process``. Ignore aforementioned output documents.

#. Unzip output WMS data and copy GeoPackage (``NRN_<SOURCE>_WMS.gpkg``) to relevant NRN server under subdirectory: ``7_Disseminate/wms``.

#. Generate a new .sd file (for WMS):

   i. In the WMS project (.aprx), located in ``7_Disseminate/wms``, open the "Save As Offline Service Definition" tool
      as shown in Figure 2.

.. figure:: /source/_static/figures/wms_sd_tool_location.png
    :alt: "Save As Offline Service Definition" tool location

    Figure 2: "Save As Offline Service Definition" tool location.

   ii. Select / populate the required parameters in each tab shown in Figure 3. Service properties in Figure 3c are
       populated using the following data (excludes empty properties):

       * Name: WMS
       * Title: National Road Network / Réseau routier national
       * Abstract: NRN WMS service / service WMS du RRN
       * Keyword: canada, geographic infrastructure, infrastructure géographique, nrn, rrn, national road network, réseau routier national, transport, road transport, transport routier, infrastructure, road maps, carte routière, road networks, réseau routier
       * ContactOrganization: Statistics Canada / Statistique Canada
       * Address: 170 Tunney’s Pasture Driveway / 170, Promenade Tunney’s Pasture
       * AddressType: Civic / Civique
       * City: Ottawa
       * StateOrProvince: Ontario
       * PostCode: K1A 0T6
       * Country: Canada
       * ContactVoiceTelephone: 1-800-263-1136
       * ContactFacsimileTelephone: 1-514-283-9350
       * ContactElectronicMailAddress: infostats@statcan.gc.ca

   iii. "Analyze" and then "Save" the .sd file (see bottom of Figure 3c).

.. figure:: /source/_static/figures/wms_sd_tool_parameters.png
    :alt: "Save As Offline Service Definition" tool parameters

    Figure 3: "Save As Offline Service Definition" tool parameters.

#. Notify relevant individuals of new NRN release via email.
