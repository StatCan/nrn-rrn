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
