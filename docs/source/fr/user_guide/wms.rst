***
WMS
***

.. include:: <isonum.txt>
.. include:: <isopub.txt>

.. contents:: Matières :
   :depth: 3

Aperçu
======

Un WMS n'est pas un format de distribution obligatoire pour le RRN, il n'y a donc aucune spécification pour sa
conception. La mise en œuvre actuelle du WMS a été développée sur la base de l'examen des données disponibles pour
chacun des produits provinciaux / territoriaux du RRN et de l'élaboration d'un système d'affichage et d'étiquetage
hiérarchique basé sur une structuration significative des données.

Le WMS est construit à l'aide d'un projet ArcGIS Pro : ``nrn-rrn/wms/nrn_rrn_wms.aprx``. Toute modification de ce
fichier doit être suivie d'une copie du fichier sur le serveur de données du RRN (puisque ce serveur n'est pas destiné
à contenir le référentiel).

Structure du WMS
================

.. code-block:: yaml

    50 000 000:
      Afficher : Route transcanadienne.
      Étiquettes : Aucun.
    4 000 000:
      Afficher : Réseau routier national.
      Étiquettes : Numéros de route pour la route transcanadienne.
    500 000:
      Afficher : Toutes les routes principales.
      Étiquettes : Numéros de route pour le réseau routier national.
    100 000:
      Afficher : Toutes les routes, sauf les ruelles.
      Étiquettes : Tous les numéros de route.
    50 000:
      Afficher : Aucun changement.
      Étiquettes : Noms de rues pour les routes principales.
    10 000:
      Afficher : Toutes les routes, passages obstrués et postes de péage.
      Étiquettes : Noms de rue pour toutes les routes.

Configuration
=============

Requêtes WMS
------------

Les données WMS sont définies par des requêtes contenues dans le fichier : ``nrn-rrn/src/export/wms_queries.yaml``.

Structure
^^^^^^^^^

**Structure générique :**: ::

    queries:
      <nom d'attribut>:
        <abréviation de la source>:
          <contenu de la requête>

**Exemple :**: ::

    queries:
      wms_50m:
        nb: "(rtnumber1 in ('2', '16') or rtnumber2 in ('2', '16'))"

**Exemple :**: ::

    queries:
      wms_500k:
        sk:
          - "(roadclass in ('Freeway', 'Expressway / Highway', 'Arterial'))"
          - "((l_placenam.str.lower() = 'regina' or r_placenam.str.lower() = 'regina') and (roadclass = 'Collector'))"

Contenu
^^^^^^^

:Nom d'attribut: Attribut souhaité à ajouter à l’ensemble de données provisoires du RRN segmrout. Les résultats de la
                 requête attribueront une valeur de ``1`` à l'attribut qui pourra ensuite être utilisé, si nécessaire,
                 dans le fichier de projet WMS.
:Abréviation de la source: Abréviation provinciale / territoriale. Utilisé pour indiquer à quelle source NRN les
                           requêtes sont destinées.
:Contenu de la requête: Requête unique, liste de requêtes ou mot-clé ``all`` (qui utilise tous les enregistrements de
                        l'ensemble de données). Les requêtes doivent utiliser la syntaxe de
                        :func:`pandas.DataFrame.query()`.

Données WMS
-----------

Les données WMS sont exportées avec d'autres formats de distribution et sont définies dans
``nrn-rrn/src/export/distribution_formats/en/wms.yaml``. Seule la définition de sortie en anglais est requise puisque
les données WMS sont bilingues et que les noms et attributs des ensembles de données ne sont pas mis à la disposition
des utilisateurs de WMS. La structure de ce fichier suit celle de l'autre format de distribution, par simple souci de
cohérence.

Ce fichier est utilisé pour définir le schéma de sortie souhaité des données WMS, qui est destiné à être utilisé dans
le fichier de projet WMS.