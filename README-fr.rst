Réseau routier national (RRN)
=============================

.. image:: https://img.shields.io/badge/Repository-nrn--rrn-brightgreen.svg?style=flat-square&logo=github
   :target: https://github.com/StatCan/nrn-rrn
.. image:: https://img.shields.io/badge/License-BSD%203--Clause-blue.svg?style=flat-square
   :target: https://opensource.org/licenses/BSD-3-Clause
.. image:: https://readthedocs.org/projects/nrn-rrn-docs/badge/?style=flat-square
   :target: https://nrn-rrn-docs.readthedocs.io/en/latest/

.. include:: /source/_static/maps/process_overview.rst

Description
-----------

Le RRN a été adopté par les membres du Comité mixte des organismes intéressés à la géomatique (CMOIG) et du Conseil 
canadien de géomatique (COCG) pour fournir des données géospatiales et attributives de qualité (actuelles, précises, 
cohérentes), homogènes et normalisées de l'ensemble du réseau routier canadien. Le RRN fait partie de l'initiative 
GéoBase qui vise à fournir une infrastructure géospatiale commune qui est maintenue régulièrement par les organisations 
les *plus proches de la source*.

Le RRN est distribué sous forme de treize ensembles de données provinciaux/territoriaux constitués de deux entités 
linéaires (segments routiers et segments de liaison par transbordeur), de trois entités ponctuelles (jonctions, 
passages obstrués et points de péage) et de trois entités tabulaires (intervalles d'adresses, noms de rue et de lieu et 
liens de noms non officiels). Actuellement, le RRN est accessible au public sur le `portail de données Ouvertes du
gouvernement <https://open.canada.ca/fr>`_.

Le contenu du RRN est largement conforme à la norme `ISO 14825 <https://www.iso.org/standard/54610.html>`_.

Configuration
-------------

Le référentiel du projet NRN est désigné par son nom de référentiel réel : ``nrn-rrn``.

Dépendances logicielles
^^^^^^^^^^^^^^^^^^^^^^^

Le ``nrn-rrn`` n'a pas de dépendances logicielles obligatoires mais recommande fortement le logiciel spécifié dans
cette section. De plus, la documentation pour l'installation et l'utilisation de ``nrn-rrn`` utilisera ce logiciel car
il représente l'approche la plus simple et recommandée.

Anaconda / conda
""""""""""""""""

Le ``nrn-rrn`` est écrit en Python pur, mais a plusieurs dépendances écrites avec des bibliothèques C. Ces
bibliothèques C peuvent être difficiles à installer (surtout sous Windows) et, par conséquent, il est recommandé de
créer et d'utiliser l'environnement virtuel conda défini dans le ``nrn-rrn``. conda est un gestionnaire d'environnement
et de packages et est le choix préférable pour la gestion des dépendances car il fournit des binaires pré-construits
pour toutes les dépendances du ``nrn-rrn`` pour toutes les plates-formes (Windows, Mac, Linux).

| `Anaconda <https://docs.anaconda.com/anaconda/install/>`_ avec conda >= 4.9.
| `Miniconda <https://docs.conda.io/en/latest/miniconda.html>`_ suffira également (distribution minimale ne contenant
  que Python et conda).

Git
"""

| `Git <https://git-scm.com/downloads>`_ est recommandé pour une installation plus simple du référentiel et
l'intégration des mises à jour.

Installation
^^^^^^^^^^^^

Utilisez les étapes suivantes pour installer le référentiel ``nrn-rrn`` et l'environnement conda :

1. Installer le référentiel.

  a) Utilisation de Git : ::

      git clone https://github.com/StatCan/nrn-rrn.git

  b) Installation manuelle : Téléchargez et décompressez le `référentiel <https://github.com/StatCan/nrn-rrn>`_.

2. Créez l'environnement conda à partir du fichier ``environment.yml`` : ::

    conda env create -f nrn-rrn/environment.yml
