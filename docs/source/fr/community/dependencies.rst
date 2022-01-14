***********
Dépendances
***********

.. include:: <isonum.txt>
.. include:: <isopub.txt>

.. contents:: Matières :
   :depth: 2

Le projet RRN s'appuie sur les capacités de plusieurs outils et bibliothèques Python open source. Les détails de
dépendance spécifiques sont décrits dans le fichier d'environnement conda
:doc:`environment <../../../../../environment.yml>`. Ce document explique brièvement chacune des dépendances au sein de
l'écosystème de dépendances RRN.

`Click (click) <https://click.palletsprojects.com/>`_
=====================================================

``Click`` est un package Python permettant de créer de belles interfaces de ligne de commande de manière composable
avec aussi peu de code que nécessaire.

`Fiona (fiona) <https://fiona.readthedocs.io/>`_
================================================

``Fiona`` est l'API soignée et agile de ``OGR`` pour les programmeurs Python. ``Fiona`` lit et écrit des fichiers de
données géographiques dans le style Python IO standard et s'appuie sur des types et des protocoles Python familiers
tels que des fichiers, des dictionnaires, des mappages et des itérateurs au lieu de classes spécifiques à
l'implémentation de ``OGR``.

`GDAL (gdal) <https://gdal.org/>`_
==================================

``GDAL`` est une bibliothèque de traduction open source pour les formats de données géospatiales raster et
vectorielles. La bibliothèque ``GDAL`` consiste en fait en deux bibliothèques séparées pour les données raster
(``GDAL``) et les données vectorielles (``OGR``), collectivement appelées ``GDAL/OGR``.

`GeoAlchemy 2 (geoalchemy2) <http://geoalchemy-2.readthedocs.org/>`_
====================================================================

``GeoAlchemy 2`` est une bibliothèque de support pour ``SQLAlchemy`` qui ajoute le support des bases de données
spatiales.

`GeoPandas (geopandas) <http://geopandas.readthedocs.io/>`_
===========================================================

``GeoPandas`` étend les objets de données ``pandas`` pour ajouter la prise en charge des données géographiques. Les
objets ``GeoPandas`` peuvent agir sur des objets géométriques ``Shapely`` et effectuer des opérations géométriques.

`Jinja (jinja2) <https://jinja.palletsprojects.com/>`_
======================================================

``Jinja`` est un moteur de template rapide, expressif et extensible. Des espaces réservés spéciaux dans le modèle
permettent d'écrire du code similaire à la syntaxe Python. Ensuite, le modèle reçoit des données pour rendre le
document final.

`Matplotlib (matplotlib) <https://matplotlib.org/stable/>`_
===========================================================

``Matplotlib`` est une bibliothèque complète pour créer des visualisations statiques, animées et interactives en Python.

`NumPy (numpy) <https://numpy.org/>`_
=====================================

``NumPy`` est une bibliothèque de calcul scientifique en Python. ``NumPy`` ajoute la prise en charge des grands
tableaux et matrices multidimensionnels, ainsi qu'une grande collection de fonctions mathématiques de haut niveau pour
opérer sur ces tableaux.

`pandas <https://pandas.pydata.org/>`_
======================================

``pandas`` est une bibliothèque d'analyse/manipulation de données pour Python, fournissant des structures de données
rapides, flexibles et expressives similaires à
`R data.frame <https://www.rdocumentation.org/packages/base/versions/3.6.2/topics/data.frame>`_ objets.

`Psycopg (psycopg2) <https://www.psycopg.org/>`_
================================================

``Psycopg`` est un adaptateur de base de données PostgreSQL pour Python.

`PyData Sphinx Theme (pydata-sphinx-theme) <https://pydata-sphinx-theme.readthedocs.io/>`_
==========================================================================================

``PyData Sphinx Theme`` est un thème Sphinx simple basé sur Bootstrap.

`PyGEOS (pygeos) <https://pygeos.readthedocs.io/>`_
===================================================

``PyGEOS`` est une bibliothèque C/Python avec des fonctions de géométrie vectorisées. Les opérations de géométrie sont
effectuées dans la bibliothèque de géométrie ``GEOS``. ``PyGEOS`` enveloppe ces opérations dans des ufuncs ``NumPy``
offrant une amélioration des performances lors de l'utilisation de tableaux de géométries.

`Python (python) <https://www.python.org/>`_
============================================

L'installation réelle de Python.

`PyYAML (pyyaml) <https://github.com/yaml/pyyaml>`_
===================================================

``PyYAML`` est un framework de traitement YAML complet pour Python.

`Requests (requests) <https://requests.readthedocs.io/>`_
=========================================================

``Requests`` est une bibliothèque HTTP élégante et simple pour Python.

`Shapely (shapely) <https://shapely.readthedocs.io/>`_
======================================================

``Shapely`` est un package Python pour la manipulation et l'analyse d'objets géométriques plans. Il est basé sur les
bibliothèques largement déployées ``GEOS`` (le moteur de PostGIS) et ``JTS`` (dont ``GEOS`` est porté). ``Shapely``
n'est pas concerné par les formats de données ou les systèmes de coordonnées, mais peut être facilement intégré aux
packages qui le sont.

`Sphinx (sphinx) <https://www.sphinx-doc.org/>`_
================================================

``Sphinx`` est un outil qui permet de créer facilement une documentation intelligente et belle pour les projets Python.
``Sphinx`` utilise reStructuredText comme langage de balisage.

`SQLAlchemy (sqlalchemy) <https://www.sqlalchemy.org/>`_
========================================================

``SQLAlchemy`` est une boîte à outils SQL et un mappeur relationnel d'objet qui donne aux développeurs d'applications
toute la puissance et la flexibilité de SQL en Python.

`python-tabulate (tabulate) <https://pypi.org/project/tabulate/>`_
==================================================================

``python-tabulate`` est une bibliothèque et un utilitaire de ligne de commande pour imprimer des données tabulaires en
Python.

`tqdm <https://tqdm.github.io/>`_
=================================

``tqdm`` est un outil de barre de progression rapide et extensible pour Python.
