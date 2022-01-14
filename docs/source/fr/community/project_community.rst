********************
Communauté du projet
********************

.. include:: <isonum.txt>
.. include:: <isopub.txt>

.. contents:: Matières :
   :depth: 1

Équipe
======

| **Jesse Stewart** | Développeur principal et chef de projet | `@jessestewart1 <https://github.com/jessestewart1>`_
| **David Craig** | Intégration et traitement des données | `@davidacraig <https://github.com/DavidACraig>`_

Contributeurs
=============

Les avatars GitHub suivants représentent les contributeurs RRN, classés par nombre de contributions, cliquez pour
obtenir des informations détaillées sur les contributions.

.. image:: https://contrib.rocks/image?repo=jessestewart1/nrn-rrn
   :target: https://github.com/jessestewart1/nrn-rrn/graphs/contributors
   :alt: Contributeurs au dépôt GitHub.

Affiliations de projet
======================

.. |logo_statscan| image:: ../../../_static/affiliations/statistics_canada_fr.png
   :alt: Logo de Statistique Canada.
   :target: https://www.statcan.gc.ca/
   :height: 25px
   :align: middle

.. |logo_geobase| image:: ../../../_static/affiliations/geobase_fr.png
   :alt: Logo de GéoBase.
   :target: http://geobase.ca/
   :height: 35px
   :align: middle

.. |logo_ccog| image:: ../../../_static/affiliations/ccog.png
   :alt: Logo de COCG.
   :target: https://www.ccog-cocg.ca/
   :height: 30px
   :align: middle

|logo_statscan| |logo_geobase| |logo_ccog|

Fournisseurs de données
=======================

Des fournisseurs de données sont continuellement ajoutés au projet RRN et leurs métadonnées peuvent être trouvées dans
des fichiers de configuration source individuels (voir :doc:`../../user_guide/conform`). La carte de couverture
suivante montre les juridictions fournissant actuellement des données (ou hébergeant une plateforme de données ouvertes
à partir de laquelle les données sont récupérées) pour le projet RRN :

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
