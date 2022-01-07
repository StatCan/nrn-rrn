*******************
Data Exchange Model
*******************

.. include:: <isonum.txt>
.. include:: <isopub.txt>

.. contents:: Contents:
   :depth: 3

Overview
========

This document describes recommendations and format used for data exchange between NRN data providers. It is important
to note that this physical data model does not constitute the final distribution model for the NRN data.

The document results from eight consultation meetings performed with Closest to Source data providers. The broad range
of the producer and user committee participants has allowed this process to identify and review many aspects of the
physical data exchange model.

We wish to thank the producer and user community both at the federal and provincial levels who have contributed to this
exercise an in doing so have ensured that the best possible exchange format for the NRN datasets will be implemented.

Data Exchange Model
===================

.. figure:: /_static/figures/data_exchange_model.png
    :alt: Data exchange model

    Figure 1: Data exchange model.

Recommendations
===============

Various items of discussion were raised during the consultations. The following resolutions or recommendations were
established by consensus. Some of the recommendations included hereafter were not discussed during the consultation but
are based on practices previously established.

Address Range Extent
--------------------

Address ranges must not overlap on more than one Road Element NID. A Road Element NID can however have more than one
adjoining address ranges. In the case where a House Number value is not known at segmentation, interpolated values can
be calculated or the address range of the adjoining Road Segment can be repeated. Segmentation can be introduced to
report known House Number value. At junctions where no House Number value is known, interpolated values can be
calculated or a value -1 (for unknown) can be assigned as a House Number.

Address Range Increment
-----------------------

A First House Number value of an address range can be smaller, equal or greater than its Last House Number value.
Having a First House Number value always smaller or equal than the Last House Number value is possible through the use
of the Digitizing Direction Flag.

A House Number value 0 can only be combined with another House Number value 0. It means that the Road Segment does not
have an address range.

Digitizing Direction
--------------------

The digitizing direction of all Road Segments with populated Address Ranges should follow the Address Range orientation
from the First to the Last House Number value. Orientation from the Lower Left coordinate of a vector is no longer
required but can still be used where there is no address range.

Street Type and Place Type
--------------------------

Street Type and Place Type values are completely spelled out without abbreviations in proper case (First letter of the
first word in uppercase and remaining characters in lowercase). Values not currently listed in the NRN attribute
domains can be added. When the lists are well established, the use of codes will be considered.

Special Characters
------------------

Special characters should remain if it is part of the official Place Name or Name Body. Unicode characters are used.

Route Names, Route Numbers and Street Names
-------------------------------------------

Unless officially recognized as street names, it is not recommended to insert Route Number and Route Name values in the
Street Name table.

Place Names
-----------

The Provincial or Territorial source provider information is deemed the provider of the valid Place Name value. Should
a Place Name geopolitical administrative polygon be available from another source that is not covered by the Provincial
or Territorial Source provider then this polygon will be deemed valid up to and until such time it is replaced by the
Province or Territory.

Road Elements Located in Non-Organized Territories
--------------------------------------------------

When the Closest to Source provider is unable to define or associate a geopolitical administrative name for remote
regions within its dataset than other sources should be considered and used up to populate the Place Name field until
such time that it can be replaced by a more authoritative source.

Metadata on Addressing Components
---------------------------------

During the consultation, it was established that only the Dates and Provider would be part of the object metadata
requirements to be populated in the addressing tables. Therefore, other Object Metadata attributes such as Planimetric
Accuracy, Acquisition Technique and Metadata Coverage can be set to Unknown (-1) value. Dataset Name and Standard
Version can and must always be populated.

Metadata on Junction
--------------------

As an option, Object Metadata attributes on Junctions can be populated by the data provider. Otherwise, they will be
automatically populated by the data publisher using the following default values and rules.

:Acquisition Technique: 12 (Computed)
:Provider: 2 (Federal)
:Coverage: 1 (Complete)
:Planimetric Accuracy: Highest planimetric accuracy value of connecting segments.
:Creation Date: Lowest creation date of connecting segments or current date for newly created junction.
:Revision Date: Highest revision date of connecting segments or default value for newly created junction.

NID and Object Metadata Management
----------------------------------

A NID can only have one set of Object Metadata information. In the case of linear feature, these metadata attributes
must be constant for the entire length of a NID. Effects on NID and Object metadata are based on updates applied to the
feature or table record. Update effects are described in :doc:`change_management`.

Segmentation
------------

Road segments are broken at any topological node (note a grade crossing is not considered a topological break). Road
segments are not broken due to a grade crossing. Where there are grade separated road crossings, the bisecting Road
Segments do not share a Junction. Grade Separated Crossings between Road Segments involve road Structure objects,
either Bridges or Tunnels. If a Junction is present at the location of the Grade separation, it is either connected to
the lower set of Road Segments or to the higher but never to both.

Road segments are broken due to any change in attribution.

NID Assignation
---------------

The same NID is assigned to each adjoining Road Segments or Ferry Connection Segments between Junctions.

Functional Road Class Integrity
-------------------------------

A Functional Road Class should not change on the length of a structure and the structure should have the same
Functional Road Class as one of the road segments to which it is connected.

Roads with Functional Road Class Freeway, Highway, Arterial, Ramp and Rapid Transit should not form a closed loop.

Ferry Connection Segments are assigned with the same Functional Road Class value of the two Road Segments that it joins
when they are the same. If the Functional Road Classes differ, the lowest value (i.e. most prominent class) prevails.

Route Names and Route Numbers Network Continuity
------------------------------------------------

Route Numbers, Route Names should not have gaps across their span, and the names should extend to associated service
lanes and ramps.

Ferry Connection Segment Valency
--------------------------------

In the real world, there is only one access to a ferry boat, therefore a Ferry Connection Segment end should only
connect with one Road Segment. A Ferry Connection is always bounded by two Junctions and composed of one or more Ferry
Connection Segment.

Ferry connections cross one another without creating segmentation.

Ferry Connection Segments can end as deadend.

Exit Number on Junctions
------------------------
When a Road Segment portrays a one-way ramp with an exit number, only the Junction marking its point of entrance (in
the real world) is assigned with the same Exit Number value.
