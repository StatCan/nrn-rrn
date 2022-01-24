****************************
Product Distribution Formats
****************************

.. include:: <isonum.txt>
.. include:: <isopub.txt>

.. contents:: Contents:
   :depth: 3

Overview
========

The following entities are part of the National Road Network (NRN) Segmented view: *Address Range*,
*Alternate Name Link*, *Blocked Passage*, *Ferry Connection Segment*, *Junction*, *Road Segment*,
*Street and Place Names* and *Toll Point*.

The product is available in the following output file formats: GML (*Geography Markup Language*), KML (*Keyhole Markup
Language*), SHP (*ESRI*\ |trade| *Shapefile*), and GPKG (*OGC Geopackage*).

.. admonition:: Note

    Data files distributed in KML format only contain the entity *Road Segment* and a subset of attributes.

Product Identification
======================

:Name: National Road Network
:Version: 2.1
:Date: 2012-03-31
:Standard: :doc:`data_product_specifications`
:Feature catalogue: :doc:`feature_catalogue`

Distribution Formats Identification
===================================

GML – Geography Markup Language
-------------------------------

:Name: GML – Geography Markup Language
:Version: 2.1.2
:Date: 2002-09-17
:Specifications: `Geography Markup Language – GML – 2.1.2, OpenGIS Implementation Specifications, OGC Document Number
                 02-069 <http://portal.opengeospatial.org/files/?artifact_id=11339>`_

KML – Keyhole Markup Language
-----------------------------

:Name: KML – Keyhole Markup Language
:Version: 2.2
:Date: 2008-04-14
:Specifications: `Open Geospatial Consortium Inc., OGC KML, Version 2.2.0, 2008-04-14, Reference number of this OGC
                 project document: OGC 07-147r2 <http://portal.opengeospatial.org/files/?artifact_id=27810>`_

SHP – ESRI\ |trade| Shapefile
-----------------------------

:Name: Shapefile
:Version: 01
:Date: July 1998
:Specifications: `ESRI Shapefile Technical Description, an ESRI White Paper, July 1998
                 <http://www.esri.com/library/whitepapers/pdfs/shapefile.pdf>`_

GPKG – OGC Geopackage
---------------------

:Name: GeoPackage
:Version: 1.0.1
:Date: January 2019
:Specifications: https://www.geopackage.org/spec101/index.html

Distribution Files Identification
=================================

GML File Names
--------------

NRN entities distributed in GML format are grouped into separate dataset files. One file contains the geometrical
entities and associated basic attributes, another file contains the addressing attributes tables, and finally up to
four change management files (one for each type of content) are available. The name of a GML file is structured
accordingly::

    NRN_<IDENTIFIER>_<edition>_<version>_<CONTENT>[_<MODIFICATION>].gml

.. csv-table::
   :header: "Property", "Description"
   :widths: auto
   :align: left

   "NRN", "Abbreviated title of the product."
   "<IDENTIFIER>", "Code of a province or a territory corresponding to the dataset location. Possible codes are: AB,
   BC, MB, NB, NL, NS, NT, NU, ON, PE, QC, SK, YT."
   "<edition>", "Dataset edition number."
   "<version>", "Dataset version number."
   "<CONTENT>", "Dataset content identifier. Possible values are: GEOM (Geometrical entities and basic attributes),
   ADDR (Address attributes tables)."
   "[<MODIFICATION>]", "[] = Optional. Type of modification applied to the dataset entities and attributes in
   comparison to previous edition. Possible values are identified in :ref:`Change Management Files`."
   ".gml", "File name extension."

**Examples:**

.. csv-table::
   :header: "File Name", "Description"
   :widths: auto
   :align: left

   "NRN_AB_4_0_GEOM.gml", "Geometrical entities and basic attributes of the dataset of Alberta, edition 4, version 0."
   "NRN_AB_4_0_ADDR.gml", "Tables of addressing attributes of the dataset of Alberta, edition 4, version 0."
   "NRN_AB_4_0_GEOM_ADDED.gml", "Geometrical entities and/or basic attributes added in the dataset of Alberta, edition
   4, version 0."
   "NRN_AB_4_0_ADDR_ADDED.gml", "Tables of the addressing attributes added in the dataset of Alberta, edition 4,
   version 0."

An XML schema (XSD file) is also provided along with a GML data file. This file defines, in a structured manner, the
type of content, the syntax and the semantic of GML documents. The name of this file is
``NRN_<IDENTIFIER>_<edition>_<version>_<CONTENT>[_<MODIFICATION>].xsd`` and a reference is recorded within the GML file.

KML File Name
-------------

The entity *Road Segment* (and a subset of attributes) is the only entity part of the product that is distributed in
KML format. The name of the KML file is structured accordingly::

    nrn_rrn_<identifier>_kml_en.kmz

.. csv-table::
   :header: "Property", "Description"
   :widths: auto
   :align: left

   "nrn_rrn", "Abbreviated English and French product title."
   "<identifier>", "Code of a province or a territory corresponding to the dataset location. Possible codes are: ab,
   bc, mb, nb, nl, ns, nt, nu, on, pe, qc, sk, yt."
   "kml", "Dataset distribution format."
   "en", "ISO code of the dataset distribution language."
   ".kmz", "File name extension."

**Example:**

.. csv-table::
   :header: "File Name", "Description"
   :widths: auto
   :align: left

   "nrn_rrn_ab_kml_en.kmz", "*Road Segment* for dataset of Alberta."

SHP File Names
--------------

The entities of the product distributed in SHP format are divided according to their geometrical representation. The
name of the SHP files is structured accordingly::

    NRN_<IDENTIFIER>_<edition>_<version>_<ENTITY>[_<MODIFICATION>].shp

.. csv-table::
   :header: "Property", "Description"
   :widths: auto
   :align: left

   "NRN", "Abbreviated title of the product."
   "<IDENTIFIER>", "Code of a province or a territory corresponding to the dataset location. Possible codes are: AB,
   BC, MB, NB, NL, NS, NT, NU, ON, PE, QC, SK, YT."
   "<edition>", "Dataset edition number."
   "<version>", "Dataset version number."
   "<ENTITY>", "Abbreviated entity name as defined in :ref:`Datasets`."
   "[<MODIFICATION>]", "[] = Optional. Type of modification applied to the dataset entities and attributes in
   comparison to previous edition. Possible values are identified in :ref:`Change Management Files`."
   ".shp", "Extension of the main geometry file name."

There are also five other files associated with the main geometry file of an entity in SHP format:

* an attribute file (.dbf for dBASE® file);
* a projection file (.prj) which includes information about the reference system and the parameters of the cartographic
  projection;
* an index file (.shx) containing the offset (relative position) for each record of the main geometry file;
* two spatial index files for the geometrical data (.sbn, .sbx).

**Examples:**

.. csv-table::
   :header: "File Name", "Description"
   :widths: auto
   :align: left

   "NRN_AB_4_0_ROADSEG.shp", "Entity *Road Segment* for dataset of Alberta, edition 4, version 0."
   "NRN_AB_4_0_ROADSEG_ADDED.shp", "Geometrical entities and/or basic attributes added to *Road Segment* in dataset of
   Alberta, edition 4, version 0."

GPKG File Names
---------------

The entities of the product distributed in GPKG format are distributed as a single file, with the entities divided into
layers according to their geometrical representation. The name of the GPKG file is structured accordingly::

    NRN_<IDENTIFIER>_<edition>_<version>_en.gpkg

.. csv-table::
   :header: "Property", "Description"
   :widths: auto
   :align: left

   "NRN", "Abbreviated title of the product."
   "<IDENTIFIER>", "Code of a province or a territory corresponding to the dataset location. Possible codes are: AB,
   BC, MB, NB, NL, NS, NT, NU, ON, PE, QC, SK, YT."
   "<edition>", "Dataset edition number."
   "<version>", "Dataset version number."
   "en", "ISO code of the dataset distribution language."
   ".gpkg", "File name extension."

**Examples:**

.. csv-table::
   :header: "File Name", "Description"
   :widths: auto
   :align: left

   "NRN_AB_4_0_en.gpkg", "All entities for dataset of Alberta, edition 4, version 0."

Metadata File
-------------

There are four metadata files that are distributed with each dataset of an NRN product. Two files are provided in
FGDC/XML format (in French and in English) and two others according to FGDC/HTML format. The name of the metadata file
is structured accordingly::

    nrn_rrn_<identifier>_<edition>_<version>_fgdc_en.<format>

.. csv-table::
   :header: "Property", "Description"
   :widths: auto
   :align: left

   "nrn_rrn", "Abbreviated English and French product title."
   "<identifier>", "Code of a province or a territory corresponding to the dataset location. Possible codes are: ab,
   bc, mb, nb, nl, ns, nt, nu, on, pe, qc, sk, yt."
   "<edition>", "Dataset edition number."
   "<version>", "Dataset version number."
   "fgdc", "Metadata file format according to CSDGM standard of the Federal Geographic Data Committee (FGDC)."
   "en", "ISO code of the dataset distribution language."
   "<format>", "File name extension (xml or html)."

**Examples:**

.. csv-table::
   :header: "File Name", "Description"
   :widths: auto
   :align: left

   "nrn_rrn_ab_4_0_fgdc_en.xml", "Metadata file for dataset of Alberta, edition 4, version 0 in FGDC/XML format."
   "nrn_rrn_ab_4_0_fgdc_en.html", "Metadata file for dataset of Alberta, edition 4, version 0 in FGDC/HTML format."

List of distribution file names
-------------------------------

The NRN product is comprised of two types of datasets: a file that contains up to date (actualized) data (e.g. that has
been updated) and a file containing the modifications (differences) applied to the previous edition of the dataset.

.. _Datasets:

Datasets
^^^^^^^^

The extension of the file name corresponds to the distribution format.

.. csv-table::
   :header: "Feature catalogue Entity name", "GML/KML\ :sup:`*`\  Entity name", "GPKG/SHP Entity name", "Type"
   :widths: auto
   :align: left

   "Address Range", "AddressRange", "ADDRANGE", "Table\ :sup:`**`\ "
   "Alternate Name Link", "AlternateNameLink", "ALTNAMLINK", "Table\ :sup:`**`\ "
   "Blocked Passage", "BlockedPassage", "BLKPASSAGE", "Point"
   "Ferry Connection Segment", "FerryConnectionSegment", "FERRYSEG", "Line"
   "Junction", "Junction", "JUNCTION", "Point"
   "Road Segment", "RoadSegment\ :sup:`*`\ ", "ROADSEG", "Line"
   "Street and Place Names", "StreetPlaceNames", "STRPLANAME", "Table\ :sup:`**`\ "
   "Toll Point", "TollPoint", "TOLLPOINT", "Point"

| :sup:`*` KML content (simplified version of the dataset).
| :sup:`*` Attributes file (.dbf) in SHP format and entities without geometry in GML format.

.. _Change Management Files:

Change Management Files
^^^^^^^^^^^^^^^^^^^^^^^

Change management consists in identifying the effects of an addition, confirmation, retirement and modification of the
objects (geometry and/or attribute) between two consecutive dataset editions. A data file is produced for each effect
type. The extension of the file name corresponds to the distribution format.

.. csv-table::
   :header: "Change management Effect name", "GML/SHP File name"
   :widths: auto
   :align: left

   "Added", "<GML/SHP File Name>_ADDED"
   "Confirmed", "<GML/SHP File Name>_CONFIRMED"
   "Modified", "<GML/SHP File Name>_MODIFIED"
   "Retired", "<GML/SHP File Name>_RETIRED"

A readme text file named: ``README_<IDENTIFIER>.txt`` that identifies the method used for the *follow-up of the
geometrical modifications* is provided with the dataset.

Attributes Identification
=========================

The attributes common to all entities of the NRN product are listed in the first table. The attributes specific to each
entity are presented in the following subsection.

The data type for all distribution formats is either: ``C(c)`` for character or ``N(n,d)`` for number (``c`` = number
of characters, ``n`` = total number of digits, ``d`` = number of digits in decimal).

Attributes Common to All Entities (Except Alternate Name Link)
--------------------------------------------------------------

.. csv-table::
   :header: "Feature catalogue Attribute name", "GML Attribute name", "GPKG/SHP Attribute name", "Data Type"
   :widths: auto
   :align: left

   "Acquisition Technique", "acquisitionTechnique", "ACQTECH", "C(28)"
   "Coverage", "metadataCoverage", "METACOVER", "C(8)"
   "Creation Date", "creationDate", "CREDATE", "N(8,0)"
   "Dataset Name", "datasetName", "DATASETNAME", "C(25)"
   "Planimetric Accuracy", "planimetricAccuracy", "ACCURACY", "N(4,0)"
   "Provider", "provider", "PROVIDER", "C(24)"
   "Revision Date", "revisionDate", "REVDATE", "N(8,0)"
   "Standard Version", "standardVersion", "SPECVERS", "N(4,0)"

Attributes Specific to Entities
-------------------------------

Address Range
^^^^^^^^^^^^^

.. csv-table::
   :header: "Feature catalogue Attribute name", "GML Attribute name", "GPKG/SHP Attribute name", "Data Type"
   :widths: auto
   :align: left

   "Alternate Street Name NID Left", "left_AlternateStreetNameNid", "L_ALTNANID", "C(32)"
   "Alternate Street Name NID Right", "right_AlternateStreetNameNid", "R_ALTNANID", "C(32)"
   "Digitizing Direction Flag Left", "left_DigitizingDirectionFlag", "L_DIGDIRFG", "C(18)"
   "Digitizing Direction Flag Right", "right_DigitizingDirectionFlag", "R_DIGDIRFG", "C(18)"
   "First House Number Left", "left_FirstHouseNumber", "L_HNUMF", "N(9,0)"
   "First House Number Right", "right_FirstHouseNumber", "R_HNUMF", "N(9,0)"
   "First House Number Suffix Left", "left_FirstHouseNumberSuffix", "L_HNUMSUFF", "C(10)"
   "First House Number Suffix Right", "right_FirstHouseNumberSuffix", "R_HNUMSUFF", "C(10)"
   "First House Number Type Left", "left_FirstHouseNumberType", "L_HNUMTYPE", "C(21)"
   "First House Number Type Right", "right_FirstHouseNumberType", "R_HNUMTYPE", "C(21)"
   "House Number Structure Left", "left_HouseNumberStructure", "L_HNUMSTR", "C(19)"
   "House Number Structure Right", "right_HouseNumberStructure", "R_HNUMSTR", "C(19)"
   "Last House Number Left", "left_LastHouseNumber", "L_HNUML", "N(9,0)"
   "Last House Number Right", "right_LastHouseNumber", "R_HNUML", "N(9,0)"
   "Last House Number Suffix Left", "left_LastHouseNumberSuffix", "L_HNUMSUFL", "C(10)"
   "Last House Number Suffix Right", "right_LastHouseNumberSuffix", "R_HNUMSUFL", "C(10)"
   "Last House Number Type Left", "left_LastHouseNumberType", "L_HNUMTYPL", "C(21)"
   "Last House Number Type Right", "right_LastHouseNumberType", "R_HNUMTYPL", "C(21)"
   "NID", "nid", "NID", "C(32)"
   "Official Street Name NID Left", "left_OfficialStreetNameNid", "L_HNUMTYPL", "C(32)"
   "Official Street Name NID Right", "right_OfficialStreetNameNid", "R_HNUMTYPL", "C(32)"
   "Reference System Indicator Left", "left_ReferenceSystemIndicator", "L_HNUMTYPL", "C(18)"
   "Reference System Indicator Right", "right_ReferenceSystemIndicator", "R_HNUMTYPL", "C(18)"

Alternate Name Link
^^^^^^^^^^^^^^^^^^^

.. csv-table::
   :header: "Feature catalogue Attribute name", "GML Attribute name", "GPKG/SHP Attribute name", "Data Type"
   :widths: auto
   :align: left

   "Creation Date", "creationDate", "CREDATE", "N(8,0)"
   "Dataset Name", "datasetName", "DATASETNAM", "C(25)"
   "NID", "nid", "NID", "C(32)"
   "Revision Date", "revisionDate", "REVDATE", "N(8,0)"
   "Standard Version", "standardVersion", "SPECVERS", "N(4,0)"
   "Street Name NID", "streetNameNid", "STRNAMENID", "C(32)"

Blocked Passage
^^^^^^^^^^^^^^^

.. csv-table::
   :header: "Feature catalogue Attribute name", "GML Attribute name", "GPKG/SHP Attribute name", "Data Type"
   :widths: auto
   :align: left

   "Blocked Passage Type", "blockedPassageType", "BLKPASSTY", "C(17)"
   "NID", "nid", "NID", "C(32)"
   "Road Element NID", "roadElementNid", "ROADNID", "C(32)"

Ferry Connection Segment
^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table::
   :header: "Feature catalogue Attribute name", "GML Attribute name", "GPKG/SHP Attribute name", "Data Type"
   :widths: auto
   :align: left

   "Closing Period", "closingPeriod", "CLOSING", "C(7)"
   "Ferry Segment ID", "ferrySegmentId", "FERRYSEGID", "N(9,0)"
   "Functional Road Class", "functionalRoadClass", "ROADCLASS", "C(41)"
   "NID", "nid", "NID", "C(32)"
   "Route Name English 1", "routeNameEnglish1", "RTENAME1EN", "C(100)"
   "Route Name English 2", "routeNameEnglish2", "RTENAME2EN", "C(100)"
   "Route Name English 3", "routeNameEnglish3", "RTENAME3EN", "C(100)"
   "Route Name English 4", "routeNameEnglish4", "RTENAME4EN", "C(100)"
   "Route Name French 1", "routeNameFrench1", "RTENAME1FR", "C(100)"
   "Route Name French 2", "routeNameFrench2", "RTENAME2FR", "C(100)"
   "Route Name French 3", "routeNameFrench3", "RTENAME3FR", "C(100)"
   "Route Name French 4", "routeNameFrench4", "RTENAME4FR", "C(100)"
   "Route Number 1", "routeNumber1", "RTNUMBER1", "C(10)"
   "Route Number 2", "routeNumber2", "RTNUMBER2", "C(10)"
   "Route Number 3", "routeNumber3", "RTNUMBER3", "C(10)"
   "Route Number 4", "routeNumber4", "RTNUMBER4", "C(10)"
   "Route Number 5", "routeNumber5", "RTNUMBER5", "C(10)"

Junction
^^^^^^^^

.. csv-table::
   :header: "Feature catalogue Attribute name", "GML Attribute name", "GPKG/SHP Attribute name", "Data Type"
   :widths: auto
   :align: left

   "Exit Number", "exitNumber", "EXITNBR", "C(10)"
   "Junction Type", "junctionType", "JUNCTYPE", "C(14)"
   "NID", "nid", "NID", "C(32)"

Road Segment
^^^^^^^^^^^^

.. csv-table::
   :header: "Feature catalogue Attribute name", "GML/KML\ :sup:`*`\  Attribute name", "GPKG/SHP Attribute name", "Data
            Type"
   :widths: auto
   :align: left

   "Address Range Digitizing Direction Flag Left", "left_AddressDirectionFlag\ :sup:`**`\ ", "L_ADDDIRFG", "C(18)"
   "Address Range Digitizing Direction Flag Right", "right_AddressDirectionFlag\ :sup:`**`\ ", "R_ADDDIRFG", "C(18)"
   "Address Range NID", "addressRangeNid", "ADRANGENID", "C(32)"
   "Closing Period", "closingPeriod", "CLOSING", "C(7)"
   "Exit Number", "exitNumber", "EXITNBR", "C(10)"
   "First House Number Left", "left_FirstHouseNumber", "L_HNUMF", "N(9,0)"
   "First House Number Right", "right_FirstHouseNumber", "R_HNUMF", "N(9,0)"
   "Functional Road Class", "functionalRoadClass", "ROADCLASS", "C(41)"
   "Last House Number Left", "left_LastHouseNumber", "L_HNUML", "N(9,0)"
   "Last House Number Right", "right_LastHouseNumber", "R_HNUML", "N(9,0)"
   "NID", "nid\ :sup:`**`\ ", "NID", "C(32)"
   "Number of Lanes", "numberLanes", "NBRLANES", "N(4,0)"
   "Official Place Name Left", "left_OfficialPlaceName\ :sup:`**`\ ", "L_PLACENAM", "C(100)"
   "Official Place Name Right", "right_OfficialPlaceName\ :sup:`**`\ ", "R_PLACENAM", "C(100)"
   "Official Street Name Concatenated Left", "left_OfficialStreetNameConcat\ :sup:`**`\ ", "L_STNAME_C", "C(100)"
   "Official Street Name Concatenated Right", "right_OfficialStreetNameConcat\ :sup:`**`\ ", "R_STNAME_C", "C(100)"
   "Paved Road Surface Type", "pavedRoadSurfaceType", "PAVSURF", "C(8)"
   "Pavement Status", "pavementStatus", "PAVSTATUS", "C(11)"
   "Road Jurisdiction", "roadJurisdiction", "ROADJURIS", "C(100)"
   "Road Segment ID", "roadSegmentId", "ROADSEGID", "N(9,0)"
   "Route Name English 1", "routeNameEnglish1", "RTENAME1EN", "C(100)"
   "Route Name English 2", "routeNameEnglish2", "RTENAME2EN", "C(100)"
   "Route Name English 3", "routeNameEnglish3", "RTENAME3EN", "C(100)"
   "Route Name English 4", "routeNameEnglish4", "RTENAME4EN", "C(100)"
   "Route Name French 1", "routeNameFrench1", "RTENAME1FR", "C(100)"
   "Route Name French 2", "routeNameFrench2", "RTENAME2FR", "C(100)"
   "Route Name French 3", "routeNameFrench3", "RTENAME3FR", "C(100)"
   "Route Name French 4", "routeNameFrench4", "RTENAME4FR", "C(100)"
   "Route Number 1", "routeNumber1\ :sup:`**`\ ", "RTNUMBER1", "C(10)"
   "Route Number 2", "routeNumber2", "RTNUMBER2", "C(10)"
   "Route Number 3", "routeNumber3", "RTNUMBER3", "C(10)"
   "Route Number 4", "routeNumber4", "RTNUMBER4", "C(10)"
   "Route Number 5", "routeNumber5", "RTNUMBER5", "C(10)"
   "Speed Restrictions", "speedRestrictions", "SPEED", "N(4,0)"
   "Structure Name English", "structureNameEnglish", "STRUNAMEEN", "C(100)"
   "Structure Name French", "structureNameFrench", "STRUNAMEFR", "C(100)"
   "Structure ID", "structureId", "STRUCTID", "C(32)"
   "Structure Type", "structureType", "STRUCTTYPE", "C(15)"
   "Traffic Direction", "trafficDirection", "TRAFFICDIR", "C(19)"
   "Unpaved Road Surface Type", "unpavedRoadSurfaceType", "UNPAVSURF", "C(7)"

:sup:`*` KML content (simplified version of the dataset).

Street and Place Names
^^^^^^^^^^^^^^^^^^^^^^

.. csv-table::
   :header: "Feature catalogue Attribute name", "GML Attribute name", "GPKG/SHP Attribute name", "Data Type"
   :widths: auto
   :align: left

   "Directional Prefix", "directionalPrefix", "DIRPREFIX", "C(10)"
   "Directional Suffix", "directionalSuffix", "DIRSUFFIX", "C(10)"
   "Muni Quadrant", "muniQuadrant", "MUNIQUAD", "C(10)"
   "NID", "nid", "NID", "C(32)"
   "Place Name", "placeName", "PLACENAME", "C(100)"
   "Place Type", "placeType", "PLACETYPE", "C(68)"
   "Province", "province", "PROVINCE", "C(25)"
   "Street Name Article", "streetNameArticle", "STARTICLE", "C(7)"
   "Street Name Body", "streetNameBody", "NAMEBODY", "C(50)"
   "Street Type Prefix", "streetTypePrefix", "STRTYPRE", "C(18)"
   "Street Type Suffix", "streetTypeSuffix", "STRTYSUF", "C(18)"

Toll Point
^^^^^^^^^^

.. csv-table::
   :header: "Feature catalogue Attribute name", "GML Attribute name", "GPKG/SHP Attribute name", "Data Type"
   :widths: auto
   :align: left

   "NID", "nid", "NID", "C(32)"
   "Road Element NID", "roadElementNid", "ROADNID", "C(32)"
   "Toll Point Type", "tollPointType", "TOLLPTTYPE", "C(22)"
