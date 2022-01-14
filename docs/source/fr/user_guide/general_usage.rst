********************
Utilisation générale
********************

.. include:: <isonum.txt>
.. include:: <isopub.txt>

.. contents:: Matières :
   :depth: 1

Aperçu
======

Le pipeline NRN est séparé en 4 processus distincts destinés à être exécutés en séquence :

:1. ``conform``: Standardisation et harmonisation des sources de données au format RRN.
:2. ``validate``: Application d'un ensemble de validations et de restrictions sur la géométrie et l'attribution des
                  ensembles de données RRN.
:3. ``confirm``: Génération et récupération d'identifiants nationaux uniques (IDN).
:4. ``export``: Configuration et exportation des formats de distribution de produits requis.

Mise en œuvre
=============

Chaque processus RRN est implémenté en tant qu'outil d'Interface en ligne de commande (ILC) qui peut être appelé à
partir de n'importe quel shell. Les paramètres de chaque outil ILC sont en grande partie les mêmes, la ``source``
(abréviation de la source provinciale/territoriale) étant le seul paramètre universel et obligatoire pour tous les
outils ILC. Des informations de référence spécifiques, y compris les spécifications des paramètres, peuvent être
affichées en passant :code:`--help` à l'outil ILC.

.. admonition:: Notez

    Il est fortement recommandé d'utiliser le pipeline RRN dans l'environnement conda `nrn-rrn`. Sinon, le résultat et
    le comportement attendus, tels que documentés, ne peuvent être garantis. Les environnements conda peuvent être
    activés via : :code:`conda activate <env name>`.

Exemples
========

Exécution d'un processus RRN : ::

    python conform.py bc -r

Affichage des informations de référence pour un processus RRN : ::

    python conform.py --help
