*********************
NRN Validation Errors
*********************

.. contents::
   :depth: 3

Abbreviations
=============

.. glossary::
    NID
        National Unique Identifier

    NRCan
        Natural Resources Canada

    NRN
        National Road Network

    StatCan
        Statistics Canada

    UUID
        Universal Unique Identifier

Overview
========

The NRN implements several validations against the attributes and geometry of constituent datasets. Most of the
currently implemented validations were adopted from the NRCan NRN process while a few are StatCan additions. Some
validations may be removed or modified after consultation with GeoBase partners as required. It is important to note
that not all validation failures are truly errors, but rather flags against potential errors which is up to the data
provider to review. Reference to such validations and the associated data records as errors is only for consistency and
simplicity of references.

Error Code Structure
====================

All validations have been assigned a unique error code with the following composition:

    :Structure: E (Fixed Letter) || Major Error Code || Minor Error Code
    :Format: E ### ##
    :Example: E00103

Errors
======

E001
----

:Validation: Construction.

E00101
^^^^^^

:Description: Arcs must be >= 3 meters in length.

E00102
^^^^^^

:Description: Arcs must be simple (i.e. must not self-overlap, self-cross, nor touch their interior).

E00103
^^^^^^

:Description: Arcs must have >= 0.01 meters distance between adjacent vertices (cluster tolerance).

E002
----

:Validation: Duplication.

E00201
^^^^^^

:Description: Features within the same dataset must not be duplicated.

E00202
^^^^^^

:Description: Arcs within the same dataset must not overlap (i.e. contain duplicated adjacent vertices).

E003
----

:Validation: Connectivity.

E00301
^^^^^^

:Description: Arcs must only connect at endpoints (nodes).

E00302
^^^^^^

:Description: Arcs must be >= 5 meters from each other, excluding connected arcs (i.e. no dangles).

E004
----

:Validation: Dates.

E00401
^^^^^^

:Description: Attributes "credate" and "revdate" must have lengths of 4, 6, or 8. Therefore, using zero-padded digits,
    dates can represent in the formats: YYYY, YYYYMM, or YYYYMMDD.

E00402
^^^^^^

:Description: Attributes "credate" and "revdate" must have a year (first 4 digits) between 1960 and the current year,
    inclusively.

E00403
^^^^^^

:Description: Attributes "credate" and "revdate" must have a month (digits 5 and 6) between 01 and 12, inclusively.

E00404
^^^^^^

:Description: Attributes "credate" and "revdate" must have a day (digits 7 and 8) between 01 and the monthly maximum,
    inclusively.

E00405
^^^^^^

:Description: Attributes "credate" and "revdate" must be <= today.

E00406
^^^^^^

:Description: Attribute "credate" must be <= attribute "revdate".

E005
----

:Validation: Identifiers.

E00501
^^^^^^

:Description: IDs must be 32 digit hexadecimal strings.

E00502
^^^^^^

:Description: Primary - foreign key linkages must be valid.

E00601
------

:Validation: Conflicting exit numbers.
:Description: Attribute "exitnbr" must be identical, excluding the default value or "None", for all arcs sharing an nid.

E00701
------

:Validation: Exit number - road class relationship.
:Description: When attribute "exitnbr" is not equal to the default value or "None", attribute "roadclass" must equal
    one of the following: "Expressway / Highway", "Freeway", "Ramp", "Rapid Transit", "Service Lane".

E00801
------

:Validation: Ferry - road connectivity.
:Description: Ferry arcs must be connected to a road arc at at least one of their nodes.


E00901
------

:Validation: Number of lanes.
:Description: Attribute "nbrlanes" must be between 1 and 8, inclusively.

E01001
------

:Validation: Speed.
:Description: Attribute "speed" must be between 5 and 120, inclusively.

E01101
------

:Validation: Encoding.
:Description: Attribute contains one or more question mark ("?"), which may be the result of invalid character encoding.

E01201
------

:Validation: Out-of-scope.
:Description: Geometry is non-completely within the source region.
