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

    NRN
        National Road Network

Overview
========

The NRN implements several validations against the attributes and geometry of constituent datasets. It is important to
note that not all validation "errors" are truly errors, but rather flags against potential issues. Reference to such
validations and the associated data records as "errors" is purely for consistency and simplicity of references.

Error Code Structure
====================

All validations have been assigned a unique error code with the following composition:

    :Structure: E (Fixed Letter) || Major Error Code (1-2 digits) || Minor Error Code (2 digits)
    :Example: E101

Errors
======

E100
----

:Validation: Construction.

E101
^^^^

:Description: Arcs must be >= 3 meters in length.

E102
^^^^

:Description: Arcs must be simple (i.e. must not self-overlap, self-cross, nor touch their interior).

E103
^^^^

:Description: Arcs must have >= 0.01 meters distance between adjacent vertices (cluster tolerance).

E200
----

:Validation: Duplication.

E201
^^^^

:Description: Features within the same dataset must not be duplicated.

E202
^^^^

:Description: Arcs within the same dataset must not overlap (i.e. contain duplicated adjacent vertices).

E300
----

:Validation: Connectivity.

E301
^^^^

:Description: Arcs must only connect at endpoints (nodes).

E302
^^^^

:Description: Arcs must be >= 5 meters from each other, excluding connected arcs (i.e. no dangles).

E400
----

:Validation: Dates.

E401
^^^^

:Description: Attributes "credate" and "revdate" must have lengths of 4, 6, or 8. Therefore, using zero-padded digits,
    dates can represent in the formats: YYYY, YYYYMM, or YYYYMMDD.

E402
^^^^

:Description: Attributes "credate" and "revdate" must have a year (first 4 digits) between 1960 and the current year,
    inclusively.

E403
^^^^

:Description: Attributes "credate" and "revdate" must have a month (digits 5 and 6) between 01 and 12, inclusively.

E404
^^^^

:Description: Attributes "credate" and "revdate" must have a day (digits 7 and 8) between 01 and the monthly maximum,
    inclusively.

E405
^^^^

:Description: Attributes "credate" and "revdate" must be <= today.

E406
^^^^

:Description: Attribute "credate" must be <= attribute "revdate".

E500
----

:Validation: Identifiers.

E501
^^^^

:Description: IDs must be 32 digit hexadecimal strings.

E502
^^^^

:Description: Primary - foreign key linkages must be valid.

E600
----

:Validation: Exit Numbers.

E601
^^^^

:Description: Attribute "exitnbr" must be identical, excluding the default value or "None", for all arcs sharing an nid.

E602
^^^^

:Description: When attribute "exitnbr" is not equal to the default value or "None", attribute "roadclass" must equal
    one of the following: "Expressway / Highway", "Freeway", "Ramp", "Rapid Transit", "Service Lane".

E701
----

:Validation: Ferry Integration.
:Description: Ferry arcs must be connected to a road arc at at least one of their nodes.


E801
----

:Validation: Number of Lanes.
:Description: Attribute "nbrlanes" must be between 1 and 8, inclusively.

E901
-----

:Validation: Speed.
:Description: Attribute "speed" must be between 5 and 120, inclusively.

E1001
-----

:Validation: Encoding.
:Description: Attribute contains one or more question mark ("?"), which may be the result of invalid character encoding.

E1101
-----

:Validation: Scope.
:Description: Geometry is not completely within the source region.
