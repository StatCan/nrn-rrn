********************
Utilisation générale
********************

.. include:: <isonum.txt>
.. include:: <isopub.txt>

.. contents:: Matières :
   :depth: 2

Aperçu
======

Le pipeline RRN est séparé en 4 processus distincts destinés à être exécutés en séquence :

1. ``conform``: Standardisation et harmonisation des sources de données au format RRN.
2. ``confirm``: Génération et récupération d'identifiants nationaux uniques (IDN).
3. ``validate``: Application d'un ensemble de validations et de restrictions sur la géométrie et l'attribution des
   ensembles de données RRN.
4. ``export``: Configuration et exportation des formats de distribution de produits requis.

.. figure:: /source/_static/figures/nrn_process_diagram.png
    :alt: Diagramme de processus du RRN

    Figure 1 : Diagramme de processus du RRN.

Mise en œuvre
=============

Chaque processus RRN est implémenté en tant qu'outil d'Interface en ligne de commande (ILC) qui peut être appelé à
partir de n'importe quel shell. Les paramètres de chaque outil ILC sont en grande partie les mêmes, la ``source``
(abréviation de la source provinciale/territoriale) étant le seul paramètre universel et obligatoire pour tous les
outils ILC. Des informations de référence spécifiques, y compris les spécifications des paramètres, peuvent être
affichées en passant :code:`--help` à l'outil ILC.

.. admonition:: Notez

    Il est fortement recommandé d'utiliser le pipeline RRN dans l'environnement conda ``nrn-rrn``. Sinon, le résultat
    et le comportement attendus, tels que documentés, ne peuvent être garantis. Les environnements conda peuvent être
    activés via : :code:`conda activate nrn-rrn`.

Exemples
========

Exécution d'un processus RRN : ::

    python conform.py bc -r

Affichage des informations de référence pour un processus RRN : ::

    python conform.py --help

Tâches de post-traitement
=========================

Une fois le pipeline RRN complet terminé, les tâches manuelles suivantes doivent être effectuées :

1. Copiez les documents de sortie dans le référentiel RRN, en écrasant les fichiers existants :

  i. Depuis ``nrn-rrn/data/processed/<source>.zip/en/completion_rates.yaml`` à ``nrn-rrn/src/export/distribution_docs/completion_rates.yaml``.
  ii. Depuis ``nrn-rrn/data/processed/<source>.zip/en/release_notes.yaml`` à ``nrn-rrn/src/export/distribution_docs/release_notes.yaml``.
  iii. Depuis ``nrn-rrn/data/processed/<source>.zip/en/completion_rates.rst`` à ``nrn-rrn/docs/source/en/product_documentation/completion_rates.rst``.
  iv. Depuis ``nrn-rrn/data/processed/<source>.zip/en/release_notes.rst`` à ``nrn-rrn/docs/source/en/product_documentation/release_notes.rst``.
  v. Depuis ``nrn-rrn/data/processed/<source>.zip/fr/completion_rates.rst`` à ``nrn-rrn/docs/source/fr/product_documentation/completion_rates.rst``.
  vi. Depuis ``nrn-rrn/data/processed/<source>.zip/fr/release_notes.rst`` à ``nrn-rrn/docs/source/fr/product_documentation/release_notes.rst``.

2. Copiez les données traitées sur le serveur RRN concerné sous le sous-répertoire : ``5_Process``.
3. Décompressez les données WMS de sortie et copiez le GeoPackage (``NRN_<SOURCE>_WMS.gpkg``) sur le serveur RRN concerné sous le sous-répertoire : ``7_Disseminate/wms``.
4. Informer les personnes concernées de la nouvelle version du RRN par e-mail.