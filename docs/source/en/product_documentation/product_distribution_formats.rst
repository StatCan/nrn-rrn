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

The product is available in the following output file formats: SHP (*ESRI*\ |trade| *Shapefile*) and GPKG (*OGC
Geopackage*).

Product Identification
======================

:Name: National Road Network
:Version: 2.1
:Date: 2012-03-31
:Standard: :doc:`data_product_specifications`
:Feature catalogue: :doc:`feature_catalogue`

Distribution Formats Identification
===================================

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
   comparison to previous edition."
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
   :header: "Feature catalogue Entity name", "Entity name", "Type"
   :widths: auto
   :align: left

   "Address Range", "ADDRANGE", "Table\ :sup:`*`\ "
   "Alternate Name Link", "ALTNAMLINK", "Table\ :sup:`*`\ "
   "Blocked Passage", "BLKPASSAGE", "Point"
   "Ferry Connection Segment", "FERRYSEG", "Line"
   "Junction", "JUNCTION", "Point"
   "Road Segment", "ROADSEG", "Line"
   "Street and Place Names", "STRPLANAME", "Table\ :sup:`*`\ "
   "Toll Point", "TOLLPOINT", "Point"

| :sup:`*` Attributes file (.dbf) in SHP format.

Attributes Identification
=========================

The attributes common to all entities of the NRN product are listed in the first table. The attributes specific to each
entity are presented in the following subsection.

The data type for all distribution formats is either: ``C(c)`` for character or ``N(n,d)`` for number (``c`` = number
of characters, ``n`` = total number of digits, ``d`` = number of digits in decimal).

Attributes Common to All Entities (Except Alternate Name Link)
--------------------------------------------------------------

.. csv-table::
   :header: "Feature catalogue Attribute name", "Attribute name", "Data Type"
   :widths: auto
   :align: left

   "Acquisition Technique", "ACQTECH", "C(28)"
   "Coverage", "METACOVER", "C(8)"
   "Creation Date", "CREDATE", "N(8,0)"
   "Dataset Name", "DATASETNAME", "C(25)"
   "Planimetric Accuracy", "ACCURACY", "N(4,0)"
   "Provider", "PROVIDER", "C(24)"
   "Revision Date", "REVDATE", "N(8,0)"
   "Standard Version", "SPECVERS", "N(4,0)"

Attributes Specific to Entities
-------------------------------

Address Range
^^^^^^^^^^^^^

.. csv-table::
   :header: "Feature catalogue Attribute name", "Attribute name", "Data Type"
   :widths: auto
   :align: left

   "Alternate Street Name NID Left", "L_ALTNANID", "C(32)"
   "Alternate Street Name NID Right", "R_ALTNANID", "C(32)"
   "Digitizing Direction Flag Left", "L_DIGDIRFG", "C(18)"
   "Digitizing Direction Flag Right", "R_DIGDIRFG", "C(18)"
   "First House Number Left", "L_HNUMF", "N(9,0)"
   "First House Number Right", "R_HNUMF", "N(9,0)"
   "First House Number Suffix Left", "L_HNUMSUFF", "C(10)"
   "First House Number Suffix Right", "R_HNUMSUFF", "C(10)"
   "First House Number Type Left", "L_HNUMTYPE", "C(21)"
   "First House Number Type Right", "R_HNUMTYPE", "C(21)"
   "House Number Structure Left", "L_HNUMSTR", "C(19)"
   "House Number Structure Right", "R_HNUMSTR", "C(19)"
   "Last House Number Left", "L_HNUML", "N(9,0)"
   "Last House Number Right", "R_HNUML", "N(9,0)"
   "Last House Number Suffix Left", "L_HNUMSUFL", "C(10)"
   "Last House Number Suffix Right", "R_HNUMSUFL", "C(10)"
   "Last House Number Type Left", "L_HNUMTYPL", "C(21)"
   "Last House Number Type Right", "R_HNUMTYPL", "C(21)"
   "NID", "NID", "C(32)"
   "Official Street Name NID Left", "L_HNUMTYPL", "C(32)"
   "Official Street Name NID Right", "R_HNUMTYPL", "C(32)"
   "Reference System Indicator Left", "L_HNUMTYPL", "C(18)"
   "Reference System Indicator Right", "R_HNUMTYPL", "C(18)"

Alternate Name Link
^^^^^^^^^^^^^^^^^^^

.. csv-table::
   :header: "Feature catalogue Attribute name", "Attribute name", "Data Type"
   :widths: auto
   :align: left

   "Creation Date", "CREDATE", "N(8,0)"
   "Dataset Name", "DATASETNAM", "C(25)"
   "NID", "NID", "C(32)"
   "Revision Date", "REVDATE", "N(8,0)"
   "Standard Version", "SPECVERS", "N(4,0)"
   "Street Name NID", "STRNAMENID", "C(32)"

Blocked Passage
^^^^^^^^^^^^^^^

.. csv-table::
   :header: "Feature catalogue Attribute name", "Attribute name", "Data Type"
   :widths: auto
   :align: left

   "Blocked Passage Type", "BLKPASSTY", "C(17)"
   "NID", "NID", "C(32)"
   "Road Element NID", "ROADNID", "C(32)"

Ferry Connection Segment
^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table::
   :header: "Feature catalogue Attribute name", "Attribute name", "Data Type"
   :widths: auto
   :align: left

   "Closing Period", "CLOSING", "C(7)"
   "Ferry Segment ID", "FERRYSEGID", "N(9,0)"
   "Functional Road Class", "ROADCLASS", "C(41)"
   "NID", "NID", "C(32)"
   "Route Name English 1", "RTENAME1EN", "C(100)"
   "Route Name English 2", "RTENAME2EN", "C(100)"
   "Route Name English 3", "RTENAME3EN", "C(100)"
   "Route Name English 4", "RTENAME4EN", "C(100)"
   "Route Name French 1", "RTENAME1FR", "C(100)"
   "Route Name French 2", "RTENAME2FR", "C(100)"
   "Route Name French 3", "RTENAME3FR", "C(100)"
   "Route Name French 4", "RTENAME4FR", "C(100)"
   "Route Number 1", "RTNUMBER1", "C(10)"
   "Route Number 2", "RTNUMBER2", "C(10)"
   "Route Number 3", "RTNUMBER3", "C(10)"
   "Route Number 4", "RTNUMBER4", "C(10)"
   "Route Number 5", "RTNUMBER5", "C(10)"

Junction
^^^^^^^^

.. csv-table::
   :header: "Feature catalogue Attribute name", "Attribute name", "Data Type"
   :widths: auto
   :align: left

   "Exit Number", "EXITNBR", "C(10)"
   "Junction Type", "JUNCTYPE", "C(14)"
   "NID", "NID", "C(32)"

Road Segment
^^^^^^^^^^^^

.. csv-table::
   :header: "Feature catalogue Attribute name", "Attribute name", "Data Type"
   :widths: auto
   :align: left

   "Address Range Digitizing Direction Flag Left", "L_ADDDIRFG", "C(18)"
   "Address Range Digitizing Direction Flag Right", "R_ADDDIRFG", "C(18)"
   "Address Range NID", "ADRANGENID", "C(32)"
   "Closing Period", "CLOSING", "C(7)"
   "Exit Number", "EXITNBR", "C(10)"
   "First House Number Left", "L_HNUMF", "N(9,0)"
   "First House Number Right", "R_HNUMF", "N(9,0)"
   "Functional Road Class", "ROADCLASS", "C(41)"
   "Last House Number Left", "L_HNUML", "N(9,0)"
   "Last House Number Right", "R_HNUML", "N(9,0)"
   "NID", "NID", "C(32)"
   "Number of Lanes", "NBRLANES", "N(4,0)"
   "Official Place Name Left", "L_PLACENAM", "C(100)"
   "Official Place Name Right", "R_PLACENAM", "C(100)"
   "Official Street Name Concatenated Left", "L_STNAME_C", "C(100)"
   "Official Street Name Concatenated Right", "R_STNAME_C", "C(100)"
   "Paved Road Surface Type", "PAVSURF", "C(8)"
   "Pavement Status", "PAVSTATUS", "C(11)"
   "Road Jurisdiction", "ROADJURIS", "C(100)"
   "Road Segment ID", "ROADSEGID", "N(9,0)"
   "Route Name English 1", "RTENAME1EN", "C(100)"
   "Route Name English 2", "RTENAME2EN", "C(100)"
   "Route Name English 3", "RTENAME3EN", "C(100)"
   "Route Name English 4", "RTENAME4EN", "C(100)"
   "Route Name French 1", "RTENAME1FR", "C(100)"
   "Route Name French 2", "RTENAME2FR", "C(100)"
   "Route Name French 3", "RTENAME3FR", "C(100)"
   "Route Name French 4", "RTENAME4FR", "C(100)"
   "Route Number 1", "RTNUMBER1", "C(10)"
   "Route Number 2", "RTNUMBER2", "C(10)"
   "Route Number 3", "RTNUMBER3", "C(10)"
   "Route Number 4", "RTNUMBER4", "C(10)"
   "Route Number 5", "RTNUMBER5", "C(10)"
   "Speed Restrictions", "SPEED", "N(4,0)"
   "Structure Name English", "STRUNAMEEN", "C(100)"
   "Structure Name French", "STRUNAMEFR", "C(100)"
   "Structure ID", "STRUCTID", "C(32)"
   "Structure Type", "STRUCTTYPE", "C(15)"
   "Traffic Direction", "TRAFFICDIR", "C(19)"
   "Unpaved Road Surface Type", "UNPAVSURF", "C(7)"

Street and Place Names
^^^^^^^^^^^^^^^^^^^^^^

.. csv-table::
   :header: "Feature catalogue Attribute name", "Attribute name", "Data Type"
   :widths: auto
   :align: left

   "Directional Prefix", "DIRPREFIX", "C(10)"
   "Directional Suffix", "DIRSUFFIX", "C(10)"
   "Muni Quadrant", "MUNIQUAD", "C(10)"
   "NID", "NID", "C(32)"
   "Place Name", "PLACENAME", "C(100)"
   "Place Type", "PLACETYPE", "C(68)"
   "Province", "PROVINCE", "C(25)"
   "Street Name Article", "STARTICLE", "C(7)"
   "Street Name Body", "NAMEBODY", "C(50)"
   "Street Type Prefix", "STRTYPRE", "C(18)"
   "Street Type Suffix", "STRTYSUF", "C(18)"

Toll Point
^^^^^^^^^^

.. csv-table::
   :header: "Feature catalogue Attribute name", "Attribute name", "Data Type"
   :widths: auto
   :align: left

   "NID", "NID", "C(32)"
   "Road Element NID", "ROADNID", "C(32)"
   "Toll Point Type", "TOLLPTTYPE", "C(22)"
