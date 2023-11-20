********
Validate
********

.. include:: <isonum.txt>
.. include:: <isopub.txt>

.. contents:: Contents:
   :depth: 3

Overview
========

The ``validate`` process enforces a set of validations and restrictions on NRN dataset geometry and attribution. The
intention of the ``validate`` process is to flag actual and potential data errors before continuing with the remainder
of the NRN pipeline.

The only output of ``validate`` is a GeoPackage which will contain a subset of features for each validation and dataset
which was flagged by that validation. This GeoPackage will be exported to: ``nrn-rrn/data/interim/validations.gpkg``.
The intended process is for the user to repair the original source data based on the subset datasets in the output
GeoPackage. Once completed, the entire pipeline should be rerun from the beginning.

Validation Errors
=================

Error Structure
---------------

All validations have been assigned a unique error code with the following structure::

    <major code (1-2 digits)><minor code (2 digits)>

Major and minor error codes are used to provide a more simplified and efficient classification of validations based on
the general type of issue that the validation is attempting to address.

Error Codes
-----------

Some of the validations are warnings intended to catch potential data issues and may not actually have to be resolved
depending on the circumstance. To distinguish between warnings and true errors, each of the following error codes are
tagged as either "hard" or "soft":

:hard: The error must be resolved.
:soft: The error should be reviewed and resolved only if actually an issue. If it is not an issue, it can be ignored.

100 - Construction
^^^^^^^^^^^^^^^^^^^

:101 [soft]: Arcs must be >= 1 meter in length, except structures (e.g. Bridges).
:102 [hard]: Arcs must not have zero length.
:103 [hard]: Arcs must be simple (i.e. must not self-overlap, self-cross, nor touch their interior).

200 - Duplication
^^^^^^^^^^^^^^^^^^

:201 [hard]: Features within the same dataset must not be duplicated.
:202 [hard]: Arcs within the same dataset must not overlap (i.e. contain duplicated adjacent vertices).

300 - Connectivity
^^^^^^^^^^^^^^^^^^^

:301 [soft]: Arcs must be >= 5 meters from each other, excluding connected arcs (i.e. no dangles).

400 - Dates
^^^^^^^^^^^^

:401 [hard]: Attributes "credate" and "revdate" must have lengths of 4, 6, or 8. Therefore, using zero-padded digits,
             dates can represent in the formats: YYYY, YYYYMM, or YYYYMMDD.
:402 [hard]: Attributes "credate" and "revdate" must have a valid YYYYMMDD combination.
:403 [hard]: Attributes "credate" and "revdate" must be between 19600101 and the current date, inclusively.

500 - Identifiers
^^^^^^^^^^^^^^^^^^

:501 [hard]: NID linkages must be valid.

600 - Exit Numbers
^^^^^^^^^^^^^^^^^^^

:601 [hard]: Attribute "exitnbr" must be identical, excluding the default value or "None", for all arcs sharing an NID.
:602 [soft]: When attribute "exitnbr" is not equal to the default value or "None", attribute "roadclass" must equal one
             of the following: "Expressway / Highway", "Freeway", "Ramp", "Rapid Transit", "Service Lane".

700 - Ferry Integration
^^^^^^^^^^^^^^^^^^^^^^^^

:701 [soft]: Ferry arcs must be connected to a road arc at at least one of their nodes.

800 - Number of Lanes
^^^^^^^^^^^^^^^^^^^^^^

:801 [soft]: Attribute "nbrlanes" must be between 1 and 8, inclusively.

900 - Speed
^^^^^^^^^^^^

:901 [soft]: Attribute "speed" must be between 5 and 120, inclusively.

1000 - Encoding
^^^^^^^^^^^^^^^^

:1001 [soft]: Attribute contains one or more question mark ("?"), which may be the result of invalid character encoding.
