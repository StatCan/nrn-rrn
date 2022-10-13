*****************
Feature Catalogue
*****************

.. include:: <isonum.txt>
.. include:: <isopub.txt>

.. admonition:: Note

    The description of features and attributes provided in this catalogue is largely based on the standard *ISO 14825 —
    Intelligent transport systems — Geographic Data Files (GDF) — Overall data specification* resulting from technical
    committee ISO/TC 204.

    This catalogue was adapted from the international standard *ISO 19110 — Geographic information — Methodology for
    feature cataloguing* prepared by technical committee ISO/TC 211.

.. contents:: Contents:
   :depth: 3

Data Types
==========

Data types for all attributes for all feature classes are described in :doc:`product_distribution_formats`.

Missing Data
============

This section applies to all attributes for all feature classes.

``-1`` (numeric) / ``Unknown`` (character) is used when a value is unknown, missing, or invalid (not within the domain
of the attribute).

.. _Object Metadata en:

Object Metadata
===============

The attributes described in this section apply to all feature classes (except for Alternate Name Link where only
Creation Date, Dataset Name, and Standard Version apply).

Acquisition Technique
---------------------

The type of data source or technique used to populate (create or revise) the dataset.

.. csv-table::
   :header: "Code", "Label", "Definition"
   :widths: auto
   :align: left

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

.. csv-table::
   :header: "Code", "Label", "Definition"
   :widths: auto
   :align: left

   1, "Complete", "Metadata applies on the entire geometry or attribute event."
   2, "Partial", "Metadata applies on a portion of the geometry or attribute event."

Creation Date
-------------

The date of data creation.

:Domain: A date in the format YYYYMMDD. If the month or the day is unknown, corresponding characters are left blank.

         | Examples: 20060630, 200606, 2006.

.. _Dataset Name Domain en:

Dataset Name
------------

Province or Territory covered by the dataset.

.. csv-table::
   :header: "Code", "Label"
   :widths: auto
   :align: left

   1, "Newfoundland and Labrador"
   2, "Nova Scotia"
   3, "Prince Edward Island"
   4, "New Brunswick"
   5, "Quebec"
   6, "Ontario"
   7, "Manitoba"
   8, "Saskatchewan"
   9, "Alberta"
   10, "British Columbia"
   11, "Yukon Territory"
   12, "Northwest Territories"
   13, "Nunavut"

Planimetric Accuracy
--------------------

The planimetric accuracy expressed in meters as the circular map accuracy standard (CMAS).

:Domain: [-1,1..n]

Provider
--------

The affiliation of the organization that generated (created or revised) the object.

.. csv-table::
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
         The value "0" is used when no value applies.

         | Examples: 20060630, 200606, 2006.

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

:Domain: A UUID or ``None`` when no value applies.

         | Example: 69822b23d217494896014e57a2edb8ac

.. _Digitizing Direction Flag Domain en:

Digitizing Direction Flag (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Indicates if the attribute event follows the same direction as the digitizing of the Road Element. A specific value is
defined for the left and right sides of the Road Element.

.. csv-table::
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

:Domain: A non-integer value or ``None`` when no value applies.

.. _House Number Type Domain en:

First House Number Type (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Method used to populate the address range. A specific value is defined for the left and right sides of the Road Element.

.. csv-table::
   :header: "Code", "Label", "Definition"
   :widths: auto
   :align: left

   0, "None", "Absence of a house along the Road Element."
   1, "Actual Located", "Qualifier indicating that the house number is located at its ""real world"" position along a
   Road Element."
   2, "Actual Unlocated", "Qualifier indicating that the house number is located at one end of the Road Element. This
   may be or may not be its ""real world"" position."
   3, "Projected", "Qualifier indicating that the house number is planned, figured or estimated for the future and is
   located (at one end) at the beginning or the end of the Road Element."
   4, "Interpolated", "Qualifier indicating that the house number is calculated from two known house numbers which are
   located on either side. By convention, the house is positioned at one end of the Road Element."

House Number Structure (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The type of house numbering (or address numbering) method applied to one side of a particular Road Element. A specific
value is defined for the left and right sides of the Road Element.

.. csv-table::
   :header: "Code", "Label", "Definition"
   :widths: auto
   :align: left

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

:Domain: A non-integer value or ``None`` when no value applies.

Last House Number Type (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Method used to populate the address range. A specific value is defined for the left and right sides of the Road Element.

:Domain: Identical to :ref:`House Number Type Domain en`.

NID
^^^

A national unique identifier.

:Domain: A UUID.

         | Example: 69822b23d217494896014e57a2edb8ac

Official Street Name NID (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The identifier used to link an address range to its recognized official street name. A specific value is defined for
the left and right sides of the Road Element.

:Domain: A UUID or ``None`` when no value applies.

         | Example: 69822b23d217494896014e57a2edb8ac

Reference System Indicator (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

An indication of whether the physical address of all or a portion of a Road Element is based on a particular addressing
system. A specific value is defined for the left and right sides of the Road Element.

.. csv-table::
   :header: "Code", "Label", "Definition"
   :widths: auto
   :align: left

   0, "None", "No reference system indicator."
   1, "Civic", ""
   2, "Lot and Concession", ""
   3, "911 Measured", ""
   4, "911 Civic", ""
   5, "DLS Townships", "Dominion Land Survey, survey method dominant in the Prairie provinces."

Object Metadata
^^^^^^^^^^^^^^^

Refer to the attributes described in :ref:`Object Metadata en`.

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

         | Example: 69822b23d217494896014e57a2edb8ac

Street Name NID
^^^^^^^^^^^^^^^

The NID of the non official street and place name.

:Domain: A UUID.

         | Example: 69822b23d217494896014e57a2edb8ac

Object Metadata
^^^^^^^^^^^^^^^

Refer to the attributes described in :ref:`Object Metadata en`.

Blocked Passage
===============

Indication of a physical barrier on a Road Element built to prevent or control further access.

Attribute Section
-----------------

Blocked Passage Type
^^^^^^^^^^^^^^^^^^^^

The type of blocked passage as an indication of the fact whether it is removable.

.. csv-table::
   :header: "Code", "Label", "Definition"
   :widths: auto
   :align: left

   1, "Permanently Fixed", "The barrier cannot be removed without destroying it. Heavy equipment needed in order to
   allow further access. Examples of permanently fixed blocked passage are concrete blocks or a mound of earth."
   2, "Removable", "The barrier is designed to free the entrance to the (other side of the) Road Element that it is
   blocking. Further access easily allowed when so desired."

NID
^^^

A national unique identifier.

:Domain: A UUID.

         | Example: 69822b23d217494896014e57a2edb8ac

Road Element NID
^^^^^^^^^^^^^^^^

The NID of the Road Element on which the point geometry is located.

:Domain: A UUID.

         | Example: 69822b23d217494896014e57a2edb8ac

Object Metadata
^^^^^^^^^^^^^^^

Refer to the attributes described in :ref:`Object Metadata en`.

Ferry Connection Segment
========================

The average route a ferryboat takes when transporting vehicles between two fixed locations on the road network.

Attribute Section
-----------------

.. _Closing Period Domain en:

Closing Period
^^^^^^^^^^^^^^

The period in which the road or ferry connection is not available to the public.

.. csv-table::
   :header: "Code", "Label", "Definition"
   :widths: auto
   :align: left

   0, "None", "There is no closing period. The road or ferry connection is open year round."
   1, "Summer", "Period of the year for which the absence of ice and snow prevent the access to the road or ferry
   connection."
   2, "Winter", "Period of the year for which ice and snow prevent the access to the road or ferry connection."

Ferry Segment ID
^^^^^^^^^^^^^^^^

A unique identifier within a dataset assigned to each Ferry Connection Segment.

:Domain: [1..n]

.. _Functional Road Class Domain en:

Functional Road Class
^^^^^^^^^^^^^^^^^^^^^

A classification based on the importance of the role that the Road Element or Ferry Connection performs in the
connectivity of the total road network.

.. csv-table::
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

         | Example: 69822b23d217494896014e57a2edb8ac

Route Name English (1, 2, 3, 4)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The English version of a name of a particular route in a given road network as attributed by a national or subnational
agency. A particular Road Segment or Ferry Connection Segment can belong to more than one named route. In such cases,
it has multiple route name attributes.

:Domain: A complete English route name value such as ``Trans-Canada Highway`` or ``None`` when no value applies.

Route Name French (1, 2, 3, 4)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The French version of a name of a particular route in a given road network as attributed by a national or subnational
agency. A particular Road Segment or Ferry Connection Segment can belong to more than one named route. In such cases,
it has multiple route name attributes.

:Domain: A complete French route name value such as ``Autoroute transcanadienne`` or ``None`` when no value applies.

Route Number (1, 2, 3, 4, 5)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ID number of a particular route in a given road network as attributed by a national or subnational agency. A
particular Road Segment or Ferry Connection Segment can belong to more than one numbered route. In such cases, it has
multiple route number attributes.

:Domain: A route number including possible associated non-integer characters such as ``A`` or ``None`` when no value
         applies.

         | Examples: 1, 1A, 230-A, 430-28.

Object Metadata
^^^^^^^^^^^^^^^

Refer to the attributes described in :ref:`Object Metadata en`.

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

:Domain: An ID number including possible associated non-integer characters such as ``A`` or ``None`` when no value
         applies.

         | Examples: 11, 11A, 11-A, 80-EST, 80-E, 80E.

Junction Type
^^^^^^^^^^^^^

The classification of a junction.

.. csv-table::
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

         | Example: 69822b23d217494896014e57a2edb8ac

Object Metadata
^^^^^^^^^^^^^^^

Refer to the attributes described in :ref:`Object Metadata en`.

Road Segment
============

A road is a linear section of the earth designed for or the result of vehicular movement. A Road Segment is the
specific representation of a portion of a road with uniform characteristics.

Attribute Section
-----------------

Address Range Digitizing Direction Flag (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Indicates if the attribute event follows the same direction as the digitizing of the Road Element. A specific value is
defined for the left and right sides of the Road Element.

:Domain: Identical to :ref:`Digitizing Direction Flag Domain en`.

Address Range NID
^^^^^^^^^^^^^^^^^

A UUID assigned to each particular block face address ranges.

:Domain: A UUID or ``None`` when no value applies.

         | Example: 69822b23d217494896014e57a2edb8ac

Closing Period
^^^^^^^^^^^^^^

The period in which the road or ferry connection is not available to the public.

:Domain: Identical to :ref:`Closing Period Domain en`.

Exit Number
^^^^^^^^^^^

The ID number of an exit on a controlled access thoroughfare that has been assigned by an administrating body.

:Domain: An ID number including possible associated non-integer characters such as ``A`` or ``None`` when no value
         applies.

         | Examples: 11, 11A, 11-A, 80-EST, 80-E, 80E.

First House Number (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The first house number address value along a particular side (left or right) of a Road Element. A specific value is
defined for the left and right sides of the Road Element.

:Domain: [-1..n] The value ``0`` is used when no value applies.

Functional Road Class
^^^^^^^^^^^^^^^^^^^^^

A classification based on the importance of the role that the Road Element or Ferry Connection performs in the
connectivity of the total road network.

:Domain: Identical to :ref:`Functional Road Class Domain en`.

Last House Number (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The last house number address value along a particular side (left or right) of a Road Element. A specific value is
defined for the left and right sides of the Road Element.

:Domain: [-1..n] The value ``0`` is used when no value applies.

NID
^^^

A national unique identifier.

:Domain: A UUID.

         | Example: 69822b23d217494896014e57a2edb8ac

Number of Lanes
^^^^^^^^^^^^^^^

The number of lanes existing on a Road Element.

:Domain: [1..8]

Official Place Name (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Official name of an administrative area, district or other named area which is required for uniqueness of the street
name.

:Domain: Derived from the Street and place names table. A specific value is defined for the left and right sides of the
         Road Element. ``None`` when no value applies.

Official Street Name Concatenated (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A concatenation of the officially recognized Directional prefix, Street type prefix, Street name article, Street name
body, Street type suffix, Directional suffix and Muni quadrant values.

:Domain: Derived from the Street and place names table. A specific value is defined for the left and right sides of the
         Road Element. ``None`` when no value applies.

Paved Road Surface Type
^^^^^^^^^^^^^^^^^^^^^^^

The type of surface a paved Road Element has.

.. csv-table::
   :header: "Code", "Label", "Definition"
   :widths: auto
   :align: left

   0, "None", "No value applies."
   1, "Rigid", "A paved road with a rigid surface such as concrete or steel decks."
   2, "Flexible", "A paved road with a flexible surface such as asphalt or tar gravel."
   3, "Blocks", "A paved road with a surface made of blocks such as cobblestones."

Pavement Status
^^^^^^^^^^^^^^^

An indication of improvement applied to a Road surface.

.. csv-table::
   :header: "Code", "Label", "Definition"
   :widths: auto
   :align: left

   1, "Paved", "A road with a surface made of hardened material such as concrete, asphalt, tar gravel, or steel decks."
   2, "Unpaved", "A road with a surface made of loose material such as gravel or dirt."

Road Jurisdiction
^^^^^^^^^^^^^^^^^

The agency with the responsibility/authority to ensure maintenance occurs but is not necessarily the one who undertakes
the maintenance directly.

:Domain: The Agency name or ``None`` when no value applies.

Road Segment ID
^^^^^^^^^^^^^^^

A unique identifier within a dataset assigned to each Road Segment.

:Domain: [1..n]

Route Name English (1, 2, 3, 4)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The English version of a name of a particular route in a given road network as attributed by a national or subnational
agency. A particular Road Segment or Ferry Connection Segment can belong to more than one named route. In such cases,
it has multiple route name attributes.

:Domain: A complete English route name value such as ``Trans-Canada Highway`` or ``None`` when no value applies.

Route Name French (1, 2, 3, 4)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The French version of a name of a particular route in a given road network as attributed by a national or subnational
agency. A particular Road Segment or Ferry Connection Segment can belong to more than one named route. In such cases,
it has multiple route name attributes.

:Domain: A complete French route name value such as ``Autoroute transcanadienne`` or ``None`` when no value applies.

Route Number (1, 2, 3, 4, 5)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ID number of a particular route in a given road network as attributed by a national or subnational agency. A
particular Road Segment or Ferry Connection Segment can belong to more than one numbered route. In such cases, it has
multiple route number attributes.

:Domain: A route number including possible associated non-integer characters such as ``A`` or ``None`` when no value
         applies.

         | Examples: 1, 1A, 230-A, 430-28.

Speed Restriction
^^^^^^^^^^^^^^^^^

The maximum speed allowed on the road. The value is expressed in kilometers per hour.

:Domain: A multiple of 5, less than or equal to 120.

Structure ID
^^^^^^^^^^^^

A national unique identifier assigned to the Road Segment or the set of adjoining Road Segments forming a structure.
This identifier allows for the reconstitution of a structure that is fragmented by Junctions.

:Domain: A UUID or ``None`` when no value applies.

         | Example: 69822b23d217494896014e57a2edb8ac

Structure Name English
^^^^^^^^^^^^^^^^^^^^^^

The English version of the name of a road structure as assigned by a national or subnational agency.

:Domain: A complete structure name or ``None`` when no value applies.

Structure Name French
^^^^^^^^^^^^^^^^^^^^^

The French version of the name of a road structure as assigned by a national or subnational agency.

:Domain: A complete structure name or ``None`` when no value applies.

Structure Type
^^^^^^^^^^^^^^

The classification of a structure.

.. csv-table::
   :header: "Code", "Label", "Definition"
   :widths: auto
   :align: left

   0, "None", "No value applies."
   1, "Bridge", "A manmade construction that supports a road on a raised structure and spans an obstacle, river,
   another road, or railway."
   2, "Bridge covered", "A manmade construction that supports a road on a covered raised structure and spans an
   obstacle, river, another road, or railway."
   3, "Bridge moveable", "A manmade construction that supports a road on a moveable raised structure and spans an
   obstacle, river, another road, or railway."
   4, "Bridge unknown", "A bridge for which it is currently impossible to determine whether its structure is covered,
   moveable or other."
   5, "Tunnel", "An enclosed manmade construction built to carry a road through or below a natural feature or other
   obstructions."
   6, "Snowshed", "A manmade roofed structure built over a road in mountainous areas to prevent snow slides from
   blocking the road."
   7, "Dam", "A manmade linear structure built across a waterway or floodway to control the flow of water and
   supporting a road for motor vehicles."

Traffic Direction
^^^^^^^^^^^^^^^^^

The direction(s) of traffic flow allowed on the road.

.. csv-table::
   :header: "Code", "Label", "Definition"
   :widths: auto
   :align: left

   1, "Both directions", "Traffic flow is allowed in both directions."
   2, "Same direction", "The direction of one way traffic flow is the same as the digitizing direction of the Road
   Segment."
   3, "Opposite direction", "The direction of one way traffic flow is opposite to the digitizing direction of the Road
   Segment."

Unpaved Road Surface Type
^^^^^^^^^^^^^^^^^^^^^^^^^

The type of surface an unpaved Road Element has.

.. csv-table::
   :header: "Code", "Label", "Definition"
   :widths: auto
   :align: left

   0, "None", "No value applies."
   1, "Gravel", "A dirt road whose surface has been improved by grading with gravel."
   2, "Dirt", "Roads whose surface is formed by the removal of vegetation and/or by the transportation movements over
   that road which inhibit further growth of any vegetation."

Object Metadata
^^^^^^^^^^^^^^^

Refer to the attributes described in :ref:`Object Metadata en`.

Street and Place Names
======================

A street name recognized by the municipality or naming authority and a name of an administrative area, district or
other named area which is required for uniqueness of the street name.

Attribute Section
-----------------

.. _Street Direction Domain en:

Directional Prefix
^^^^^^^^^^^^^^^^^^

A geographic direction that is part of the street name and precedes the street name body or, if appropriate, the street 
type prefix.

.. csv-table::
   :header: "Code", "Label", "Definition"
   :widths: auto
   :align: left

   0, "None", "No value applies."
   1, "North", ""
   2, "Nord", ""
   3, "South", ""
   4, "Sud", ""
   5, "East", ""
   6, "Est", ""
   7, "West", ""
   8, "Ouest", ""
   9, "Northwest", ""
   10, "Nord-ouest", ""
   11, "Northeast", ""
   12, "Nord-est", ""
   13, "Southwest", ""
   14, "Sud-ouest", ""
   15, "Southeast", ""
   16, "Sud-est", ""
   17, "Central", ""
   18, "Centre", ""

Directional Suffix
^^^^^^^^^^^^^^^^^^

A geographic direction that is part of the street name and succeeds the street name body or, if appropriate, the street
type suffix.

:Domain: Identical to :ref:`Street Direction Domain en`.

Muni Quadrant
^^^^^^^^^^^^^

The attribute Muni quadrant is used in some addresses much like the directional attributes where the town is divided
into sections based on major east-west and north-south divisions. The effect is as if multiple directional were used.

.. csv-table::
   :header: "Code", "Label", "Definition"
   :widths: auto
   :align: left

   0, "None", "No value applies."
   1, "South-West", ""
   2, "South-East", ""
   3, "North-East", ""
   4, "North-West", ""

NID
^^^

A national unique identifier.

:Domain: A UUID.

         | Example: 69822b23d217494896014e57a2edb8ac

Place Name
^^^^^^^^^^

Name of an administrative area, district or other named area which is required for uniqueness of the street name.

:Domain: The complete name of the place.

         | Examples: Arnold's Cove, Saint-Jean-Baptiste-de-l'Îsle-Verte, Sault Ste. Marie, Grand-Sault, Grand Falls.

Place Type
^^^^^^^^^^

Expression specifying the type of place.

:Domain: Conforms to Census Subdivision (CSD) types and is periodically updated to reflect changes in those values.

         | Examples: C (City / Cité), IRI (Indian reserve / Réserve indienne), M (Municipality / Municipalité).

Province
^^^^^^^^

Province or Territory where the place is located.

:Domain: Identical to :ref:`Dataset Name Domain en`.

Street Name Article
^^^^^^^^^^^^^^^^^^^

Article(s) that is/are part of the street name and located at the beginning.

.. csv-table::
   :header: "Label", "Definition"
   :widths: auto
   :align: left

   "None", ""
   "à", ""
   "à l'", ""
   "à la", ""
   "au", ""
   "aux", ""
   "by the", ""
   "chez", ""
   "d'", ""
   "de", ""
   "de l'", ""
   "de la", ""
   "des", ""
   "du", ""
   "l'", ""
   "la", ""
   "le", ""
   "les", ""
   "of the", ""
   "the", ""

Street Name Body
^^^^^^^^^^^^^^^^

The portion of the street name (either official or alternate) that has the most identifying power excluding street type
and directional prefixes or suffixes and street name articles.

:Domain: The complete street name body or ``None`` when no value applies.

         | Examples: Capitale, Trésor, Golf, Abbott, Abbott's, Main, Church, Park, Bread and Cheese.

.. _Street Type Domain en:

Street Type Prefix
^^^^^^^^^^^^^^^^^^

A part of the street name of a Road Element identifying the street type. A prefix precedes the street name body of a 
Road Element.

.. admonition:: Note

    New values are periodically added.

.. csv-table::
   :header: "Code", "Label", "Definition"
   :widths: auto
   :align: left
   :class: longtable

   0, "None", "No value applies."
   1, "Abbey", ""
   2, "Access", ""
   3, "Acres", ""
   4, "Aire", ""
   5, "Allée", ""
   6, "Alley", ""
   7, "Autoroute", ""
   8, "Avenue", ""
   9, "Barrage", ""
   10, "Bay", ""
   11, "Beach", ""
   12, "Bend", ""
   13, "Bloc", ""
   14, "Block", ""
   15, "Boulevard", ""
   16, "Bourg", ""
   17, "Brook", ""
   18, "By-pass", ""
   19, "Byway", ""
   20, "Campus", ""
   21, "Cape", ""
   22, "Carre", ""
   23, "Carrefour", ""
   24, "Centre", ""
   25, "Cercle", ""
   26, "Chase", ""
   27, "Chemin", ""
   28, "Circle", ""
   29, "Circuit", ""
   30, "Close", ""
   31, "Common", ""
   32, "Concession", ""
   33, "Corners", ""
   34, "Côte", ""
   35, "Cour", ""
   36, "Court", ""
   37, "Cove", ""
   38, "Crescent", ""
   39, "Croft", ""
   40, "Croissant", ""
   41, "Crossing", ""
   42, "Crossroads", ""
   43, "Cul-de-sac", ""
   44, "Dale", ""
   45, "Dell", ""
   46, "Desserte", ""
   47, "Diversion", ""
   48, "Downs", ""
   49, "Drive", ""
   50, "Droit de passage", ""
   51, "Échangeur", ""
   52, "End", ""
   53, "Esplanade", ""
   54, "Estates", ""
   55, "Expressway", ""
   56, "Extension", ""
   57, "Farm", ""
   58, "Field", ""
   59, "Forest", ""
   60, "Freeway", ""
   61, "Front", ""
   62, "Gardens", ""
   63, "Gate", ""
   64, "Glade", ""
   65, "Glen", ""
   66, "Green", ""
   67, "Grounds", ""
   68, "Grove", ""
   69, "Harbour", ""
   70, "Haven", ""
   71, "Heath", ""
   72, "Heights", ""
   73, "Highlands", ""
   74, "Highway", ""
   75, "Hill", ""
   76, "Hollow", ""
   77, "Île", ""
   78, "Impasse", ""
   79, "Island", ""
   80, "Key", ""
   81, "Knoll", ""
   82, "Landing", ""
   83, "Lane", ""
   84, "Laneway", ""
   85, "Limits", ""
   86, "Line", ""
   87, "Link", ""
   88, "Lookout", ""
   89, "Loop", ""
   90, "Mall", ""
   91, "Manor", ""
   92, "Maze", ""
   93, "Meadow", ""
   94, "Mews", ""
   95, "Montée", ""
   96, "Moor", ""
   97, "Mount", ""
   98, "Mountain", ""
   99, "Orchard", ""
   100, "Parade", ""
   101, "Parc", ""
   102, "Park", ""
   103, "Parkway", ""
   104, "Passage", ""
   105, "Path", ""
   106, "Pathway", ""
   107, "Peak", ""
   108, "Pines", ""
   109, "Place", ""
   110, "Place", ""
   111, "Plateau", ""
   112, "Plaza", ""
   113, "Point", ""
   114, "Port", ""
   115, "Private", ""
   116, "Promenade", ""
   117, "Quay", ""
   118, "Rang", ""
   119, "Range", ""
   120, "Reach", ""
   121, "Ridge", ""
   122, "Right of Way", ""
   123, "Rise", ""
   124, "Road", ""
   125, "Rond Point", ""
   126, "Route", ""
   127, "Row", ""
   128, "Rue", ""
   129, "Ruelle", ""
   130, "Ruisseau", ""
   131, "Run", ""
   132, "Section", ""
   133, "Sentier", ""
   134, "Sideroad", ""
   135, "Square", ""
   136, "Street", ""
   137, "Stroll", ""
   138, "Subdivision", ""
   139, "Terrace", ""
   140, "Terrasse", ""
   141, "Thicket", ""
   142, "Towers", ""
   143, "Townline", ""
   144, "Trace", ""
   145, "Trail", ""
   146, "Trunk", ""
   147, "Turnabout", ""
   148, "Vale", ""
   149, "Via", ""
   150, "View", ""
   151, "Village", ""
   152, "Vista", ""
   153, "Voie", ""
   154, "Walk", ""
   155, "Way", ""
   156, "Wharf", ""
   157, "Wood", ""
   158, "Woods", ""
   159, "Wynd", ""
   160, "Driveway", ""
   161, "Height", ""
   162, "Roadway", ""
   163, "Strip", ""
   164, "Concession Road", ""
   165, "Corner", ""
   166, "County Road", ""
   167, "Crossroad", ""
   168, "Fire Route", ""
   169, "Garden", ""
   170, "Hills", ""
   171, "Isle", ""
   172, "Lanes", ""
   173, "Pointe", ""
   174, "Regional Road", ""
   175, "Autoroute à péage", ""
   176, "Baie", ""
   177, "Bluff", ""
   178, "Bocage", ""
   179, "Bois", ""
   180, "Boucle", ""
   181, "Bretelle", ""
   182, "Cap", ""
   183, "Causeway", ""
   184, "Chaussée", ""
   185, "Contournement", ""
   186, "Couloir", ""
   187, "Crête", ""
   188, "Croix", ""
   189, "Cross", ""
   190, "Dead End", ""
   191, "Débarquement", ""
   192, "Entrance", ""
   193, "Entrée", ""
   194, "Evergreen", ""
   195, "Exit", ""
   196, "Étang", ""
   197, "Falaise", ""
   198, "Jardin", ""
   199, "Lawn", ""
   200, "Lien", ""
   201, "Ligne", ""
   202, "Manoir", ""
   203, "Pass", ""
   204, "Pente", ""
   205, "Pond", ""
   206, "Quai", ""
   207, "Ramp", ""
   208, "Rampe", ""
   209, "Rangée", ""
   210, "Roundabout", ""
   211, "Route de plaisance", ""
   212, "Route sur élevée", ""
   213, "Side", ""
   214, "Sortie", ""
   215, "Throughway", ""
   216, "Took", ""
   217, "Turn", ""
   218, "Turnpike", ""
   219, "Vallée", ""
   220, "Villas", ""
   221, "Virage", ""
   222, "Voie oust", ""
   223, "Voie rapide", ""
   224, "Vue", ""
   225, "Westway", ""
   226, "Arm", ""
   227, "Baseline", ""
   228, "Bourne", ""
   229, "Branch", ""
   230, "Bridge", ""
   231, "Burn", ""
   232, "Bypass", ""
   233, "Camp", ""
   234, "Chart", ""
   235, "Club", ""
   236, "Copse", ""
   237, "Creek", ""
   238, "Crest", ""
   239, "Cul De Sac", ""
   240, "Curve", ""
   241, "Cut", ""
   242, "Fairway", ""
   243, "Gateway", ""
   244, "Greenway", ""
   245, "Inamo", ""
   246, "Inlet", ""
   247, "Junction", ""
   248, "Keep", ""
   249, "Lake", ""
   250, "Lakes", ""
   251, "Lakeway", ""
   252, "Market", ""
   253, "Millway", ""
   254, "Outlook", ""
   255, "Oval", ""
   256, "Overpass", ""
   257, "Pier", ""
   258, "River", ""
   259, "Service", ""
   260, "Shore", ""
   261, "Shores", ""
   262, "Sideline", ""
   263, "Spur", ""
   264, "Surf", ""
   265, "Track", ""
   266, "Valley", ""
   267, "Walkway", ""
   268, "Wold", ""
   269, "Tili", ""
   270, "Nook", ""
   271, "Drung", ""
   272, "Awti", ""
   273, "Awti'j", ""
   274, "Rest", ""
   275, "Rotary", ""

Street Type Suffix
^^^^^^^^^^^^^^^^^^

A part of the street name of a Road Element identifying the street type. A suffix follows the street name body of a
Road Element.

:Domain: Identical to :ref:`Street Type Domain en`.

Object Metadata
^^^^^^^^^^^^^^^

Refer to the attributes described in :ref:`Object Metadata en`.

Toll Point
==========

Place where a right-of-way is charged to gain access to a motorway, a bridge, etc.

Attribute Section
-----------------

NID
^^^

A national unique identifier.

:Domain: A UUID.

         | Example: 69822b23d217494896014e57a2edb8ac

Road Element NID
^^^^^^^^^^^^^^^^

The NID of the Road Element on which the point geometry is located.

:Domain: A UUID.

         | Example: 69822b23d217494896014e57a2edb8ac

Toll Point Type
^^^^^^^^^^^^^^^

The type of toll point.

.. csv-table::
   :header: "Code", "Label", "Definition"
   :widths: auto
   :align: left

   1, "Physical Toll Booth", "A toll booth is a construction along or across the road where toll can be paid to
   employees of the organization in charge of collecting the toll, to machines capable of automatically recognizing
   coins or bills or to machines involving electronic methods of payment like credit cards or bank cards."
   2, "Virtual Toll Booth", "At a virtual point of toll payment, toll will be charged via automatic registration of the
   passing vehicle by subscription or invoice."
   3, "Hybrid", "Hybrid signifies a toll booth which is both physical and virtual."

Object Metadata
^^^^^^^^^^^^^^^

Refer to the attributes described in :ref:`Object Metadata en`.
