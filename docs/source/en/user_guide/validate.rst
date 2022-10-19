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
intention of the ``validate`` process is to flag actual and potential data error before continuing with the remainder
of the NRN pipeline.

The only output of ``validate`` is a log (.log) file which will be exported to:
``nrn-rrn/data/interim/validations.log``. The intended process is for the user to repair the original source data based
on the specified errors in the output log. Once completed, the entire pipeline should be rerun from the initial process.

.. admonition:: Note

    While the unique identifiers logged by the validations exist only on the interim data, edits should only to be made
    to the raw data. Therefore, when editing, both the raw and interim data are required (interim data for locating the
    invalid features and raw data for editing). Furthermore, after completing the required edits, the pipeline must be
    re-run from the beginning.

Log Structure
=============

The output log will contain a series of standardized logs for each validation executed by the ``validate`` process.
Each logged validation will have the same content structure.

**Generic structure:** ::

    <timestamp> - WARNING: E<error code> - <NRN dataset> - <Error description>.

    Values:
    <uuid>
    ...

    Query: "uuid" in ('<uuid>', ...)

**Specific structure:** ::

    2022-01-04 16:00:51 - WARNING: E201 - roadseg - Features within the same dataset must not be duplicated.

    Values:
    76d283b46076400c900ed84c02ab605f
    c9ac2f60a0814eec9ff56bf95ad79804

    Query: "uuid" in ('76d283b46076400c900ed84c02ab605f', 'c9ac2f60a0814eec9ff56bf95ad79804')

**Components:**

:Values: A list containing the ``uuid`` value of each record flagged by the validation for the NRN dataset. ``uuid`` is
         a unique identifier assigned to each record of each NRN dataset for the purpose of tracking and identifying
         records throughout the NRN pipeline.
:Query: A QGIS expression to query all records flagged by the validation for the NRN dataset. This will contain the
        same values as ``Values``.

Validation Errors
=================

Error Structure
---------------

All validations have been assigned a unique error code with the following structure::

    E<major code (1-2 digits)><minor code (2 digits)>

Major and minor error codes are used to provide a more simplified and efficient classification of validations based on
the general type of issue that the validation is attempting to address.

Error Codes
-----------

E100 - Construction
^^^^^^^^^^^^^^^^^^^

:E101: Arcs must be >= 3 meters in length, except structures (e.g. Bridges).
:E102: Arcs must not have zero length.
:E103: Arcs must be simple (i.e. must not self-overlap, self-cross, nor touch their interior).

E200 - Duplication
^^^^^^^^^^^^^^^^^^

:E201: Features within the same dataset must not be duplicated.
:E202: Arcs within the same dataset must not overlap (i.e. contain duplicated adjacent vertices).

E300 - Connectivity
^^^^^^^^^^^^^^^^^^^

:E301: Arcs must be >= 5 meters from each other, excluding connected arcs (i.e. no dangles).

E400 - Dates
^^^^^^^^^^^^

:E401: Attributes "credate" and "revdate" must have lengths of 4, 6, or 8. Therefore, using zero-padded digits, dates
       can represent in the formats: YYYY, YYYYMM, or YYYYMMDD.
:E402: Attributes "credate" and "revdate" must have a valid YYYYMMDD combination.
:E403: Attributes "credate" and "revdate" must be between 19600101 and the current date, inclusively.

E500 - Identifiers
^^^^^^^^^^^^^^^^^^

:E501: NID linkages must be valid.
:E502: NIDs must not be isolated (i.e. have no linkages).

E600 - Exit Numbers
^^^^^^^^^^^^^^^^^^^

:E601: Attribute "exitnbr" must be identical, excluding the default value or "None", for all arcs sharing an NID.
:E602: When attribute "exitnbr" is not equal to the default value or "None", attribute "roadclass" must equal one of
       the following: "Expressway / Highway", "Freeway", "Ramp", "Rapid Transit", "Service Lane".

E700 - Ferry Integration
^^^^^^^^^^^^^^^^^^^^^^^^

:E701: Ferry arcs must be connected to a road arc at at least one of their nodes.


E800 - Number of Lanes
^^^^^^^^^^^^^^^^^^^^^^

:E801: Attribute "nbrlanes" must be between 1 and 8, inclusively.

E900 - Speed
^^^^^^^^^^^^

:E901: Attribute "speed" must be between 5 and 120, inclusively.

E1000 - Encoding
^^^^^^^^^^^^^^^^

:E1001: Attribute contains one or more question mark ("?"), which may be the result of invalid character encoding.

E1100 - Scope
^^^^^^^^^^^^^

:E1101: Geometry is not completely within the source region.
