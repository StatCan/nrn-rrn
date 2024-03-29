*******************
Reference Materials
*******************

.. include:: <isonum.txt>
.. include:: <isopub.txt>

.. contents:: Contents:
   :depth: 2

Acronyms and Abbreviations
==========================

.. glossary::
    CCOG
        Canadian Council on Geomatics

    CMAS
        Circular Map Accuracy Standard

    CRSID
        Coordinate Reference System Identifier

    DEM
        Digital Elevation Model

    GDF
        Geographic Data File

    GPKG
        Open Geospatial Consortium Geopackage

    GPS
        Global Positioning System

    GUID
        Globally Unique Identifier

    IACG
        Inter-Agency Committee on Geomatics

    ID
        Identifier

    IEEE
        Institute of Electrical and Electronics Engineers - USA

    ISO
        International Organization for Standardization

    NAD83CSRS
        North American Datum 1983 (Canadian Spatial Reference System)

    NatProvTer
        National, Provincial, or Territorial

    NHN
        National Hydrographic Network

    NID
        National Identifier

    NRCan
        Natural Resources Canada

    NRN
        National Road Network

    NSDI
        National Spatial Data Infrastructure

    NVD
        National Vector Data

    OGC
        Open Geospatial Consortium

    SHP
        ESRI Shapefile

    StatsCan
        Statistics Canada

    TC
        Technical Committee

    UUID
        Universally Unique Identifier

    XML
        Extensible Markup Language

Terms and Definitions
=====================

Attribute
    Characteristic of a feature. For example, number of lanes or pavement status.

Class
    Description of a set of objects that share the same attributes, operations, methods, relationships, and semantics.
    A class does not always have an associated geometry (e.g. address range class).

Dataset
    Data collection identifiable for a Canadian province or territory.

Entity
    Digital representation of a real world phenomenon. For example, the digital representation of King Street is an
    entity.

Ferry Connection
    The average route a ferryboat takes when transporting vehicles between two fixed locations on the Road Network. Two
    Junctions always bound a Ferry Connection.

National Vector Data
    Several layers of vector data, referred to as National Vector Data (NVD), will share the same specification. The
    National Road Network (NRN) and National Hydrographic Network (NHN) are examples of NVD.

Network Linear Element
    Abstract class of a Road Element and Ferry Connection.

Object
    An object is an instance of a class.

Road Element
    A road is a linear section of the earth designed for or the result of vehicular movement. A Road Element is the
    representation of a road between Junctions. A Road Element is always bounded by two Junctions. A Road Element is
    composed of one or more than one contiguous Road Segments.

Segment
    Portion of a Network Linear Element that has a common set of defined characteristics (attributes).

Universal Unique Identifier
    The definition and method used for the generation of a Universal Unique Identifier (UUID) is defined in the
    document :doc:`identification_rules`.
