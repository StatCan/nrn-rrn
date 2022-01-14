*****************
Project Community
*****************

.. include:: <isonum.txt>
.. include:: <isopub.txt>

.. contents:: Contents:
   :depth: 1

Team
=====

| **Jesse Stewart** | Lead Developer and Project Manager | `@jessestewart1 <https://github.com/jessestewart1>`_
| **David Craig** | Data Integration and Processing | `@davidacraig <https://github.com/DavidACraig>`_

Contributors
============

The following GitHub avatars represent the NRN contributors, ordered by contribution count, click for detailed
contribution insights.

.. image:: https://contrib.rocks/image?repo=jessestewart1/nrn-rrn
   :target: https://github.com/jessestewart1/nrn-rrn/graphs/contributors
   :alt: GitHub repository contributors.

Project Affiliations
====================

.. |logo_statscan| image:: https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Statistics_Canada_logo.svg/800px-Statistics_Canada_logo.svg.png
   :alt: Statistics Canada logo.
   :target: https://www.statcan.gc.ca/
   :height: 25px
   :align: middle

.. |logo_geobase| image:: ../../../_static/affiliations/geobase_en.png
   :alt: GeoBase logo.
   :target: http://geobase.ca/
   :height: 35px
   :align: middle

.. |logo_ccog| image:: https://www.ccog-cocg.ca/wp-content/themes/wet-boew-child/images/ccog-ccdg.png
   :alt: CCOG logo.
   :target: https://www.ccog-cocg.ca/
   :height: 30px
   :align: middle

|logo_statscan| |logo_geobase| |logo_ccog|

Data Providers
==============

Data providers are continuously being added to the NRN project and their metadata can be found in individual source
configuration files (see :doc:`../../user_guide/conform`). The following coverage map shows the jurisdictions currently
providing data (or hosting an open data platform from which data is being retrieved) for the NRN project:

.. ipython:: python
   :suppress:

   import geopandas as gpd
   from pathlib import Path

   sources = gpd.read_file("../../../../src/boundaries.zip", layer="boundaries")
   config_dir = Path("../../../../src/conform/sources")
   config_sources = set(map(lambda p: p.stem, filter(Path.is_dir, config_dir.glob("*"))))
   sources = sources.loc[sources.source.isin(config_sources)]

.. ipython:: python

   sources.explore(color="green", tooltip="name")
