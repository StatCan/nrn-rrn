*****************
Feature Catalogue
*****************

.. include:: <isonum.txt>
.. include:: <isopub.txt>

.. note::
    The description of features and attributes provided in this catalogue is largely based on the standard *ISO 14825 —
    Intelligent transport systems — Geographic Data Files (GDF) — Overall data specification* resulting from technical
    committee ISO/TC 204.

    This catalogue was adapted from the international standard *ISO 19110 — Geographic information — Methodology for
    feature cataloguing* prepared by technical committee ISO/TC 211.

.. contents::
   :depth: 4

Data Types
==========

Data types for all attributes for all feature classes are specified in :doc:`product_distribution_formats`.

Missing Data
============

This section applies to all attributes for all feature classes.

"-1" (integer) / "Unknown" (character) is used when a value is unknown, missing, or invalid (not within the domain of
the attribute).

.. _Object Metadata:

Object Metadata
===============

The attributes described in this section apply to all feature classes (except for Alternate Name Link where only
Creation Date, Dataset Name, and Standard Version apply).

Acquisition Technique
---------------------

The type of data source or technique used to populate (create or revise) the dataset.

.. csv-table:: Domain:
   :header: "Code", "Label", "Definition"
   :widths: auto
   :align: left

   -1, "Unknown", "Impossible to determine.",
   0, "None", "No value applies."
   1, "Other", "Other value."
   2, "GPS", "Data collected using a GPS device."
   3, "Orthoimage", "Satellite imagery orthorectified."
   4, "Orthophoto", "Aerial photo orthorectified."
   5, "Vector Data", "Vector digital data."
   6, "Paper Map", "Conventional sources of information like maps or plans."
   7, "Field Completion", "Information gathered from people directly on the field."
   8, "Raster Data", "Data resulting from a scanning process."
   9, "Digital Elevation Model", "Data coming from a Digital Elevation Model (DEM)."
   10, "Aerial Photo", "Aerial photography not orthorectified."
   11, "Raw Imagery Data", "Satellite imagery not orthorectified."
   12, "Computed", "Geometric information that has been computed (not captured)."

Coverage
--------

This value indicates if this set of metadata covers the full length of the Network Linear Element or only a portion of
it.

.. csv-table:: Domain:
   :header: "Code", "Label", "Definition"
   :widths: auto
   :align: left

   -1, "Unknown", "Impossible to determine."
   1, "Complete", "Metadata applies on the entire geometry or attribute event."
   2, "Partial", "Metadata applies on a portion of the geometry or attribute event."

Creation Date
-------------

The date of data creation.

:Domain: A date in the format YYYYMMDD. If the month or the day is unknown, corresponding characters are left blank.

    Examples: 20060630, 200606, 2006.

Dataset Name
------------

Province or Territory covered by the dataset.

.. csv-table:: Domain:
   :header: "Code", "Label", "Definition"
   :widths: auto
   :align: left

   1, "Newfoundland and Labrador", ""
   2, "Nova Scotia", ""
   3, "Prince Edward Island", ""
   4, "New Brunswick", ""
   5, "Quebec", ""
   6, "Ontario", ""
   7, "Manitoba", ""
   8, "Saskatchewan, ""
   9, "Alberta", ""
   10, "British Columbia", ""
   11, "Yukon Territory", ""
   12, "Northwest Territories", ""
   13, "Nunavut", ""

Planimetric Accuracy
--------------------

The planimetric accuracy expressed in meters as the circular map accuracy standard (CMAS).

:Domain: [-1,1..n]

Provider
--------

The affiliation of the organization that generated (created or revised) the object.

.. csv-table:: Domain:
   :header: "Code", "Label", "Definition"
   :widths: auto
   :align: left

   1, "Other", "Other value."
   2, "Federal", "Federal departments or agencies."
   3, "Provincial / Territorial", "Provincial / territorial departments or agencies."
   4, "Municipal", "Municipal departments or agencies."

Revision Date
-------------

The date of data revision.

:Domain: A date in the format YYYYMMDD. If the month or the day is unknown, corresponding characters are left blank.

    Examples: 20060630, 200606, 2006.

Standard Version
----------------

The version number of the GeoBase Product specifications.

:Domain: [2.0]

Address Range
=============

A set of attributes representing the address of the first and last building located along a side of the entire Road
Element or a portion of it.

Attribute Section
-----------------

Alternate Street Name NID (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The identifier used to link an address range to its alternate street name. A specific value is defined for the left and
right sides of the Road Element.

:Domain: A UUID or "None" when no value applies.

    Example: 69822b23d217494896014e57a2edb8ac

Digitizing Direction Flag (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Indicates if the attribute event follows the same direction as the digitizing of the Road Element. A specific value is
defined for the left and right sides of the Road Element.

.. csv-table:: Domain:
   :header: "Code", "Label", "Definition"
   :widths: auto
   :align: left

   1, "Same Direction", "Attribute event and Road Element geometry are in the same direction."
   2, "Opposite Direction", "Attribute event and Road Element geometry are in opposite directions."
   3, "Not Applicable", "Indication of the digitizing direction of the Road Element not needed for the attribute event."

First House Number (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The first house number address value along a particular side (left or right) of a Road Element. A specific value is
defined for the left and right sides of the Road Element.

:Domain: [-1..n] The value "0" is used when no value applies.

First House Number Suffix (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A non-integer value, such as a fraction (e.g. 1⁄4) or a character (e.g. A) that sometimes follows the house number
address value. A specific value is defined for the left and right sides of the Road Element.

:Domain: A non-integer value or "None" when no value applies.

First House Number Type (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Method used to populate the address range. A specific value is defined for the left and right sides of the Road Element.

.. csv-table:: Domain:
   :header: "Code", "Label", "Definition"
   :widths: auto
   :align: left

   -1, "Unknown", "Due to the source, the house number type is not known."
   0, "None", "Absence of a house along the Road Element."
   1, "Actual Located", "Qualifier indicating that the house number is located at its \"real world\" position along a
   Road Element."
   2, "Actual Unlocated", "Qualifier indicating that the house number is located at one end of the Road Element. This
   may be or may not be its \"real world\" position."
   3, "Projected", "Qualifier indicating that the house number is planned, figured or estimated for the future and is
   located (at one end) at the beginning or the end of the Road Element."
   4, "Interpolated", "Qualifier indicating that the house number is calculated from two known house numbers which are
   located on either side. By convention, the house is positioned at one end of the Road Element."

House Number Structure (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The type of house numbering (or address numbering) method applied to one side of a particular Road Element. A specific
value is defined for the left and right sides of the Road Element.

.. csv-table:: Domain:
   :header: "Code", "Label", "Definition"
   :widths: auto
   :align: left

   -1, "Unknown", "Impossible to determine."
   0, "None", "Absence of a house along the Road Element."
   1, "Even", "The house numbers appear as even numbers in a sequentially sorted order (ascending or descending) when
   moving from one end of the Road Element to the other. Numeric completeness of the series is not a requirement. An
   even house number series that has missing numbers but is sequentially sorted is considered Even. An example is the
   series (2, 4, 8, 18, 22)."
   2, "Odd", "The house numbers appear as odd numbers in a sequentially sorted order (ascending or descending) when
   moving from one end of the Road Element to the other. Numeric completeness of the series is not a requirement. An
   odd house number series that has missing numbers but is sequentially sorted is considered Odd. An example is the
   series (35, 39, 43, 69, 71, 73, 85)."
   3, "Mixed", "The house numbers are odd and even on the same side of a Road Element in a sequentially sorted order
   (ascending or descending) when moving from one end of the Road Element to the other. Numeric completeness of the
   series is not a requirement. An odd and even house number series that has missing numbers but is sequentially sorted
   is considered Mixed. Examples are the series (5, 6, 7, 9, 10, 13) and (24, 27, 30, 33, 34, 36)."
   4, "Irregular", "The house numbers do not occur in any sorted order."

Last House Number (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The last house number address value along a particular side (left or right) of a Road Element. A specific value is
defined for the left and right sides of the Road Element.

:Domain: [-1..n] The value "0" is used when no value applies.

Last House Number Suffix (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A non-integer value, such as a fraction (e.g. 1⁄4) or a character (e.g. A) that sometimes follows the house number
address value. A specific value is defined for the left and right sides of the Road Element.

:Domain: A non-integer value or "None" when no value applies.

Last House Number Type (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Method used to populate the address range. A specific value is defined for the left and right sides of the Road Element.

.. csv-table:: Domain:
   :header: "Code", "Label", "Definition"
   :widths: auto
   :align: left

   -1, "Unknown", "Due to the source, the house number type is not known."
   0, "None", "Absence of a house along the Road Element."
   1, "Actual Located", "Qualifier indicating that the house number is located at its \"real world\" position along a
   Road Element."
   2, "Actual Unlocated", "Qualifier indicating that the house number is located at one end of the Road Element. This
   may be or may not be its \"real world\" position."
   3, "Projected", "Qualifier indicating that the house number is planned, figured or estimated for the future and is
   located (at one end) at the beginning or the end of the Road Element."
   4, "Interpolated", "Qualifier indicating that the house number is calculated from two known house numbers which are
   located on either side. By convention, the house is positioned at one end of the Road Element."

NID
^^^

A national unique identifier.

:Domain: A UUID.

    Example: 69822b23d217494896014e57a2edb8ac

Official Street Name NID (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The identifier used to link an address range to its recognized official street name. A specific value is defined for
the left and right sides of the Road Element.

:Domain: A UUID or "None" when no value applies.

    Example: 69822b23d217494896014e57a2edb8ac

Reference System Indicator (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

An indication of whether the physical address of all or a portion of a Road Element is based on a particular addressing
system. A specific value is defined for the left and right sides of the Road Element.

.. csv-table:: Domain:
   :header: "Code", "Label", "Definition"
   :widths: auto
   :align: left

   -1, "Unknown", "Impossible to determine."
   0, "None", "No reference system indicator."
   1, "Civic", ""
   2, "Lot and Concession", ""
   3, "911 Measured", ""
   4, "911 Civic", ""
   5, "DLS Townships", "Dominion Land Survey, survey method dominant in the Prairie provinces."

Object Metadata
^^^^^^^^^^^^^^^

Refer to the attributes described in :ref:`Object Metadata`.

Alternate Name Link
===================

A linkup table establishing one or many relations between address ranges and their non-official street and place names
used or known by the general public.

Attribute Section
-----------------

NID
^^^

A national unique identifier.

:Domain: A UUID.

    Example: 69822b23d217494896014e57a2edb8ac

Street Name NID
^^^^^^^^^^^^^^^

The NID of the non official street and place name.

:Domain: A UUID.

    Example: 69822b23d217494896014e57a2edb8ac

Object Metadata
^^^^^^^^^^^^^^^

Refer to the attributes described in :ref:`Object Metadata`.

Blocked Passage
===============

Indication of a physical barrier on a Road Element built to prevent or control further access.

Attribute Section
-----------------

Blocked Passage Type
^^^^^^^^^^^^^^^^^^^^

The type of blocked passage as an indication of the fact whether it is removable.

.. csv-table:: Domain:
   :header: "Code", "Label", "Definition"
   :widths: auto
   :align: left

   -1, "Unknown", "A blocked passage for which the specific type is unknown."
   1, "Permanently Fixed", "The barrier cannot be removed without destroying it. Heavy equipment needed in order to
   allow further access. Examples of permanently fixed blocked passage are concrete blocks or a mound of earth."
   2, "Removable", "The barrier is designed to free the entrance to the (other side of the) Road Element that it is
   blocking. Further access easily allowed when so desired."

NID
^^^

A national unique identifier.

:Domain: A UUID.

    Example: 69822b23d217494896014e57a2edb8ac

Road Element NID
^^^^^^^^^^^^^^^^

The NID of the Road Element on which the point geometry is located.

:Domain: A UUID.

    Example: 69822b23d217494896014e57a2edb8ac

Object Metadata
^^^^^^^^^^^^^^^

Refer to the attributes described in :ref:`Object Metadata`.

Ferry Connection Segment
========================

The average route a ferryboat takes when transporting vehicles between two fixed locations on the road network.

Attribute Section
-----------------

Closing Period
^^^^^^^^^^^^^^

The period in which the road or ferry connection is not available to the public.

.. csv-table:: Domain:
   :header: "Code", "Label", "Definition"
   :widths: auto
   :align: left

   -1, "Unknown", "Impossible to determine."
   0, "None", "There is no closing period. The road or ferry connection is open year round."
   1, "Summer", "Period of the year for which the absence of ice and snow prevent the access to the road or ferry
   connection."
   2, "Winter", "Period of the year for which ice and snow prevent the access to the road or ferry connection."

Ferry Segment ID
^^^^^^^^^^^^^^^^

A unique identifier within a dataset assigned to each Ferry Connection Segment.

:Domain: [1..n]

Functional Road Class
^^^^^^^^^^^^^^^^^^^^^

A classification based on the importance of the role that the Road Element or Ferry Connection performs in the
connectivity of the total road network.

.. csv-table:: Domain:
   :header: "Code", "Label", "Definition"
   :widths: auto
   :align: left

   1, "Freeway", "An unimpeded, high-speed controlled access thoroughfare for through traffic with typically no at-
   grade intersections, usually with no property access or direct access, and which is accessed by a ramp. Pedestrians
   are prohibited."
   2, "Expressway / Highway", "A high-speed thoroughfare with a combination of controlled access intersections at any
   grade."
   3, "Arterial", "A major thoroughfare with medium to large traffic capacity."
   4, "Collector", "A minor thoroughfare mainly used to access properties and to feed traffic with right of way."
   5, "Local / Street", "A low-speed thoroughfare dedicated to provide full access to the front of properties."
   6, "Local / Strata", "A low-speed thoroughfare dedicated to provide access to properties with potential public
   restriction such as: trailer parks, First Nations, strata, private estates, seasonal residences."
   7, "Local / Unknown", "A low-speed thoroughfare dedicated to provide access to the front of properties but for which
   the access regulations are unknown."
   8, "Alleyway / Lane", "A low-speed thoroughfare dedicated to provide access to the rear of properties."
   9, "Ramp", "A system of interconnecting roadways providing for the controlled movement between two or more roadways."
   10, "Resource / Recreation", "A narrow passage whose primary function is to provide access for resource extraction
   and may also have serve in providing public access to the backcountry."
   11, "Rapid Transit", "A thoroughfare restricted to public transit buses."
   12, "Service Lane", "A stretch of road permitting vehicles to come to a stop along a freeway or highway. Scale,
   service lane, emergency lane, lookout, and rest area."
   13, "Winter", "A road that is only useable during the winter when conditions allow for passage over lakes, rivers,
   and wetlands."

NID
^^^

A national unique identifier.

:Domain: A UUID.

    Example: 69822b23d217494896014e57a2edb8ac

Route Name English (1, 2, 3, 4)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The English version of a name of a particular route in a given road network as attributed by a national or sub-national
agency. A particular Road Segment or Ferry Connection Segment can belong to more than one named route. In such cases,
it has multiple route name attributes.

:Domain: A complete English route name value such as "Trans-Canada Highway" or "None" when no value applies.

Route Name French (1, 2, 3, 4)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The French version of a name of a particular route in a given road network as attributed by a national or sub-national
agency. A particular Road Segment or Ferry Connection Segment can belong to more than one named route. In such cases,
it has multiple route name attributes.

:Domain: A complete French route name value such as "Autoroute transcanadienne" or "None" when no value applies.

Route Number (1, 2, 3, 4, 5)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ID number of a particular route in a given road network as attributed by a national or sub-national agency. A
particular Road Segment or Ferry Connection Segment can belong to more than one numbered route. In such cases, it has
multiple route number attributes.

:Domain: A route number including possible associated non-integer characters such as "A" or "None" when no value
    applies.

    Examples: 1, 1A, 230-A, 430-28.

Object Metadata
^^^^^^^^^^^^^^^

Refer to the attributes described in :ref:`Object Metadata`.

Junction
========

A feature that bounds a Road Element or a Ferry Connection. A Road Element or Ferry Connection always forms a
connection between two Junctions and, a Road Element or Ferry Connection is always bounded by exactly two Junctions. A
Junction Feature represents the physical connection between its adjoining Road Elements or Ferry Connections. A
Junction is defined at the intersection of three or more roads, at the junction of a road and a ferry, at the end of a
dead end road and at the junction of a road or ferry with a National, Provincial or Territorial Boundary.

Attribute Section
-----------------

Exit Number
^^^^^^^^^^^

The ID number of an exit on a controlled access thoroughfare that has been assigned by an administrating body.

:Domain: An ID number including possible associated non-integer characters such as "A" or "None" when no value applies.

    Examples: 11, 11A, 11-A, 80-EST, 80-E, 80E.

Junction Type
^^^^^^^^^^^^^

The classification of a junction.

.. csv-table:: Domain:
   :header: "Code", "Label", "Definition"
   :widths: auto
   :align: left

   1, "Intersection", "An intersection between three or more Road Elements intersecting at same grade level."
   2, "Dead End", "A specific Junction that indicates that a Road Element ends and is not connected to any other Road
   Element or Ferry Connection."
   3, "Ferry", "A specific Junction that indicates that a Road Element connects to a Ferry Connection."
   4, "NatProvTer", "A specific Junction at the limit of a dataset indicating that a Road element or Ferry connection
   continues into the adjacent province, territory or country."

NID
^^^

A national unique identifier.

:Domain: A UUID.

    Example: 69822b23d217494896014e57a2edb8ac

Object Metadata
^^^^^^^^^^^^^^^

Refer to the attributes described in :ref:`Object Metadata`.

Road Segment
============

A road is a linear section of the earth designed for or the result of vehicular movement. A Road Segment is the
specific representation of a portion of a road with uniform characteristics.

Attribute Section
-----------------

Address Range Digitizing Direction Flag (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

...

Address Range NID
^^^^^^^^^^^^^^^^^

...

Closing Period
^^^^^^^^^^^^^^

...

Exit Number
^^^^^^^^^^^

...

First House Number (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

...

Functional Road Class
^^^^^^^^^^^^^^^^^^^^^

...

Last House Number (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

...

NID
^^^

...

Number of Lanes
^^^^^^^^^^^^^^^

...

Official Place Name (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

...

Official Street Name Concatenated (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

...

Paved Road Surface Type
^^^^^^^^^^^^^^^^^^^^^^^

...

Pavement Status
^^^^^^^^^^^^^^^

...

Road Jurisdiction
^^^^^^^^^^^^^^^^^

...

Road Segment ID
^^^^^^^^^^^^^^^

...

Route Name English (1, 2, 3, 4)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

...

Route Name French (1, 2, 3, 4)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

...

Route Number (1, 2, 3, 4, 5)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

...

Speed Restriction
^^^^^^^^^^^^^^^^^

...

Structure ID
^^^^^^^^^^^^

...

Structure Name English
^^^^^^^^^^^^^^^^^^^^^^

...

Structure Name French
^^^^^^^^^^^^^^^^^^^^^

...

Structure Type
^^^^^^^^^^^^^^

...

Traffic Direction
^^^^^^^^^^^^^^^^^

...

Unpaved Road Surface Type
^^^^^^^^^^^^^^^^^^^^^^^^^

...

Object Metadata
^^^^^^^^^^^^^^^

Refer to the attributes described in :ref:`Object Metadata`.

Street and Place Names
======================

A street name recognized by the municipality or naming authority and a name of an administrative area, district or
other named area which is required for uniqueness of the street name.

Attribute Section
-----------------

Directional Prefix
^^^^^^^^^^^^^^^^^^

...

Directional Suffix
^^^^^^^^^^^^^^^^^^

...

Muni Quadrant
^^^^^^^^^^^^^

...

NID
^^^

...

Place Name
^^^^^^^^^^

...

Place Type
^^^^^^^^^^

...

Province
^^^^^^^^

...

Street Name Article
^^^^^^^^^^^^^^^^^^^

...

Street Name Body
^^^^^^^^^^^^^^^^

...

Street Type Prefix
^^^^^^^^^^^^^^^^^^

...

Street Type Suffix
^^^^^^^^^^^^^^^^^^

...

Object Metadata
^^^^^^^^^^^^^^^

Refer to the attributes described in :ref:`Object Metadata`.

Toll Point
==========

Place where a right-of-way is charged to gain access to a motorway, a bridge, etc.

Attribute Section
-----------------

NID
^^^

...

Road Element NID
^^^^^^^^^^^^^^^^

...

Toll Point Type
^^^^^^^^^^^^^^^

...

Object Metadata
^^^^^^^^^^^^^^^

Refer to the attributes described in :ref:`Object Metadata`.
