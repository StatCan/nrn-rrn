*******************
Catalogue d'entités
*******************

.. include:: <isonum.txt>
.. include:: <isopub.txt>

.. note::
    La description des entités et attributs de ce catalogue est en grande partie extraite de la norme internationale
    *ISO 14825 — Systèmes de transport intelligents — Fichiers de données géographiques — Spécification des données
    globales* du comité technique ISO/TC 204.

    Ce catalogue a été adapté à partir de la norme internationale *ISO 19110 — Information géographique — Méthodologie
    de catalogage des entités* préparée par le comité technique ISO/TC 211.

.. contents::
   :depth: 4

Types de données
================

Les types de données pour tous les attributs de toutes les entités sont décrits dans le
:doc:`product_distribution_formats`.

Données manquantes
==================

Cette section s'applique à tous les attributs de toutes les entités.

« -1 » (nombre) / « Inconnu » (caractère) est utilisé lorsqu'une valeur est inconnue, manquante ou invalide (pas dans
le domaine de l'attribut).

.. _Object Metadata:

Métadonnées d'objet
===================

Les attributs décrits dans la section métadonnées d'objet s'appliquent à toutes les entités (sauf pour Lien nom non
officiel où seulement Date création, Nom jeu de données et Version normes s'appliquent).

Acquisition Technique
---------------------

The type of data source or technique used to populate (create or revise) the dataset.

.. csv-table:: Domaine :
   :header: "Code", "Étiquette", "Définition"
   :widths: auto
   :align: left

   0, "Aucun", "Aucune valeur disponible à l'égard de la source."
   1, "Autre", "Toutes valeurs possibles non mentionnées explicitement dans le domaine."
   2, "GPS", "Données captée en utilisant le GPS."
   3, "Ortho-image", "Image satellite orthorectifiée."
   4, "Ortho-photo", "Photographie aérienne orthorectifiée."
   5, "Données vectorielles", "Données vectorielles numériques."
   6, "Carte papier", "Sources d'information conventionnelles comme des cartes ou des plans."
   7, "Complètement terrain", "Information obtenue de gens directement sur le terrain."
   8, "Données matricielles", "Données provenant d'un processus de balayage."
   9, "Modèle numérique d'élévation", "Données provenant d'un modèle numérique d'élévation (MNE)."
   10, "Photographie aérienne", "Photographie aérienne non orthorectifiée."
   11, "Image satellite brute", "Image satellite non orthorectifiée."
   12, "Calculé", "Informations géométriques calculées (non captées)."

Coverage
--------

This value indicates if this set of metadata covers the full length of the Network Linear Element or only a portion of
it.

.. csv-table:: Domaine :
   :header: "Code", "Étiquette", "Définition"
   :widths: auto
   :align: left

   1, "Complet", "Les métadonnées s'appliquent à la totalité de la géométrie ou de l'événement."
   2, "Partiel", "Les métadonnées s'appliquent à une portion de la géométrie ou de l'événement."

Creation Date
-------------

The date of data creation.

:Domaine: A date in the format YYYYMMDD. If the month or the day is unknown, corresponding characters are left blank.

    Examples: 20060630, 200606, 2006.

Dataset Name
------------

Province or Territory covered by the dataset.

.. _Dataset Name Domain:

.. csv-table:: Domaine :
   :header: "Code", "Étiquette", "Définition"
   :widths: auto
   :align: left

   1, "Terre-Neuve et Labrador", ""
   2, "Nouvelle-Écosse", ""
   3, "Île-du-Prince-Édouard", ""
   4, "Nouveau-Brunswick", ""
   5, "Québec", ""
   6, "Ontario", ""
   7, "Manitoba", ""
   8, "Saskatchewan, ""
   9, "Alberta", ""
   10, "Colombie-Britannique", ""
   11, "Territoire du Yukon", ""
   12, "Territoires du Nord-Ouest", ""
   13, "Nunavut", ""

Planimetric Accuracy
--------------------

The planimetric accuracy expressed in meters as the circular map accuracy standard (CMAS).

:Domaine: [-1,1..n]

Provider
--------

The affiliation of the organization that generated (created or revised) the object.

.. csv-table:: Domaine :
   :header: "Code", "Étiquette", "Définition"
   :widths: auto
   :align: left

   1, "Autre", "Valeur autre."
   2, "Fédéral", "Département ou agence fédéral."
   3, "Provincial / Territorial", "Département ou agence provincial / territorial."
   4, "Municipal", "Département ou agence municipal."

Revision Date
-------------

The date of data revision.

:Domaine: A date in the format YYYYMMDD. If the month or the day is unknown, corresponding characters are left blank.

    Examples: 20060630, 200606, 2006.

Standard Version
----------------

The version number of the GeoBase Product specifications.

:Domaine: [2.0]

Address Range
=============

A set of attributes representing the address of the first and last building located along a side of the entire Road
Element or a portion of it.

Attribute Section
-----------------

Alternate Street Name NID (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The identifier used to link an address range to its alternate street name. A specific value is defined for the left and
right sides of the Road Element.

:Domaine: A UUID or "None" when no value applies.

    Example: 69822b23d217494896014e57a2edb8ac

Digitizing Direction Flag (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Indicates if the attribute event follows the same direction as the digitizing of the Road Element. A specific value is
defined for the left and right sides of the Road Element.

.. _Digitizing Direction Flag Domain:

.. csv-table:: Domaine :
   :header: "Code", "Étiquette", "Définition"
   :widths: auto
   :align: left

   1, "Même sens", "Le sens de l'événement attributif et celui de la numérisation de l'Élément routier sont les mêmes."
   2, "Sens opposé", "Le sens de l'événement attributif et celui de la numérisation de l'Élément routier sont opposés."
   3, "Sans objet", "Le sens de numération de l'Élément routier est inutile pour l'événement attributif."

First House Number (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The first house number address value along a particular side (left or right) of a Road Element. A specific value is
defined for the left and right sides of the Road Element.

:Domaine: [-1..n] The value "0" is used when no value applies.

First House Number Suffix (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A non-integer value, such as a fraction (e.g. 1⁄4) or a character (e.g. A) that sometimes follows the house number
address value. A specific value is defined for the left and right sides of the Road Element.

:Domaine: A non-integer value or "None" when no value applies.

.. _House Number Type Domain:

First House Number Type (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Method used to populate the address range. A specific value is defined for the left and right sides of the Road Element.

.. csv-table:: Domaine :
   :header: "Code", "Étiquette", "Définition"
   :widths: auto
   :align: left

   0, "Aucun", "Il n'y a aucun bâtiment le long d'un côté de l'Élément routier."
   1, "Localisation réelle", "Qualificatif qui indique que le premier ou le dernier bâtiment, qui porte une adresse,
   sur l'Élément routier est à sa position réelle."
   2, "Localisation présumée", "Qualificatif qui indique que le premier ou le dernier bâtiment, qui porte une adresse,
   sur l'Élément routier est à une position qu'on ne peut qualifier de réelle et qu'on présume être au début (premier
   bâtiment) ou à la fin (dernier bâtiment) de l'Élément routier."
   3, "Projeté", "Valeur qui indique que le premier ou le dernier bâtiment, qui porte une adresse, sur l'Élément
   routier n'existe pas mais est plutôt projeté/planifié."
   4, "Interpolé", "Qualificatif qui indique que l'adresse civique (numéro de maison) est calculé à partir des numéros
   existants. La position du pseudo-bâtiment est au début ou à la fin de l'Élément routier."

House Number Structure (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The type of house numbering (or address numbering) method applied to one side of a particular Road Element. A specific
value is defined for the left and right sides of the Road Element.

.. csv-table:: Domaine :
   :header: "Code", "Étiquette", "Définition"
   :widths: auto
   :align: left

   0, "Aucun", "Aucune structure de numérotation. Il n'y a pas de bâtiment, avec adresse, le long d'un côté particulier
   d'un Élément routier."
   1, "Numéros pairs", "Les numéros de maisons s'affichent comme des numéros pairs d'une façon séquentielle ordonnée
   (ascendant ou descendant) quand on se déplace d'un bout à l'autre de l'Élément routier. L'intégrité numérique de la
   série n'est pas une exigence. Une série de numéros pairs de maisons qui a des numéros absents mais qui est ordonnée
   de manière séquentielle est considérée comme paire. Exemple : (2, 4, 8, 18, 22)."
   2, "Numéros impairs", "Les numéros de maisons s'affichent comme des numéros impairs d'une façon séquentielle
   ordonnée (ascendant ou descendant) quand on se déplace d'un bout à l'autre de l'Élément routier. L'intégrité
   numérique de la série n'est pas une exigence. Une série de numéros impairs de maisons qui a des numéros absents mais
   qui est ordonnée de manière séquentielle est considérée comme impaire. Exemples : (35, 39, 43, 69, 71, 73, 85)."
   3, "Numéros mixtes", "Les numéros de maisons sont impairs et pairs du même côté d'un Élément routier de façon
   ordonnée (ascendant ou descendant) quand on se déplace d'un bout à l'autre de l'Élément routier. L'intégrité
   numérique de la série n'est pas une exigence. Une série de numéros impairs ou pairs de maisons qui a des numéros
   absents mais qui est ordonnée de manière séquentielle est considérée comme mixte. Exemples : (5, 6, 7, 9, 10, 13) et
   (24, 27, 30, 33, 34, 36)."
   4, "Numéros irréguliers", "Les numéros de maisons ne se présentent pas dans un ordre ordonné."

Last House Number (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The last house number address value along a particular side (left or right) of a Road Element. A specific value is
defined for the left and right sides of the Road Element.

:Domaine: [-1..n] The value "0" is used when no value applies.

Last House Number Suffix (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A non-integer value, such as a fraction (e.g. 1⁄4) or a character (e.g. A) that sometimes follows the house number
address value. A specific value is defined for the left and right sides of the Road Element.

:Domaine: A non-integer value or "None" when no value applies.

Last House Number Type (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Method used to populate the address range. A specific value is defined for the left and right sides of the Road Element.

:Domaine: Identical to :ref:`House Number Type Domain`.

NID
^^^

A national unique identifier.

:Domaine: A UUID.

    Example: 69822b23d217494896014e57a2edb8ac

Official Street Name NID (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The identifier used to link an address range to its recognized official street name. A specific value is defined for
the left and right sides of the Road Element.

:Domaine: A UUID or "None" when no value applies.

    Example: 69822b23d217494896014e57a2edb8ac

Reference System Indicator (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

An indication of whether the physical address of all or a portion of a Road Element is based on a particular addressing
system. A specific value is defined for the left and right sides of the Road Element.

.. csv-table:: Domaine :
   :header: "Code", "Étiquette", "Définition"
   :widths: auto
   :align: left

   0, "Aucun", "Aucun indicateur du système de référence."
   1, "Civique", ""
   2, "Lot et concession", ""
   3, "Mesuré 911", ""
   4, "Civique 911", ""
   5, "DLS", "Dominion Land Survey, système de découpage des provinces des prairies."

Métadonnées d'objet
^^^^^^^^^^^^^^^^^^^

Référer aux attributs décrits dans la :ref:`Object Metadata`.

Alternate Name Link
===================

A linkup table establishing one or many relations between address ranges and their non-official street and place names
used or known by the general public.

Attribute Section
-----------------

NID
^^^

A national unique identifier.

:Domaine: A UUID.

    Example: 69822b23d217494896014e57a2edb8ac

Street Name NID
^^^^^^^^^^^^^^^

The NID of the non official street and place name.

:Domaine: A UUID.

    Example: 69822b23d217494896014e57a2edb8ac

Métadonnées d'objet
^^^^^^^^^^^^^^^^^^^

Référer aux attributs décrits dans la :ref:`Object Metadata`.

Blocked Passage
===============

Indication of a physical barrier on a Road Element built to prevent or control further access.

Attribute Section
-----------------

Blocked Passage Type
^^^^^^^^^^^^^^^^^^^^

The type of blocked passage as an indication of the fact whether it is removable.

.. csv-table:: Domaine :
   :header: "Code", "Étiquette", "Définition"
   :widths: auto
   :align: left

   1, "Permanente", "La barrière ou l’obstacle doit être détruit ou enlevé au moyen de machinerie lourde pour permettre
   l'accès. Les blocs de béton et les remblais de terre constituent des exemples d'obstructions considérées
   permanentes."
   2, "Amovible", "La barrière est conçue pour permettre l’accès à (l’autre côté de) l’Élément routier qu'elle bloque.
   Lorsque voulu, l’accès peut facilement être permis."

NID
^^^

A national unique identifier.

:Domaine: A UUID.

    Example: 69822b23d217494896014e57a2edb8ac

Road Element NID
^^^^^^^^^^^^^^^^

The NID of the Road Element on which the point geometry is located.

:Domaine: A UUID.

    Example: 69822b23d217494896014e57a2edb8ac

Métadonnées d'objet
^^^^^^^^^^^^^^^^^^^

Référer aux attributs décrits dans la :ref:`Object Metadata`.

Ferry Connection Segment
========================

The average route a ferryboat takes when transporting vehicles between two fixed locations on the road network.

Attribute Section
-----------------

Closing Period
^^^^^^^^^^^^^^

The period in which the road or ferry connection is not available to the public.

.. _Closing Period Domain:

.. csv-table:: Domaine :
   :header: "Code", "Étiquette", "Définition"
   :widths: auto
   :align: left

   0, "Aucun", "Il n'y a pas de période de fermeture. La route ou la liaison par transbordeur est accessible toute
   l'année."
   1, "Été", "Période au cours de laquelle l'absence de glace et de neige empêche l'accès à la route ou à la liaison
   par transbordeur."
   2, "Hiver", "Période au cours de laquelle la présence de glace et de neige empêche l'accès à la route ou à la
   liaison par transbordeur."

Ferry Segment ID
^^^^^^^^^^^^^^^^

A unique identifier within a dataset assigned to each Ferry Connection Segment.

:Domaine: [1..n]

Functional Road Class
^^^^^^^^^^^^^^^^^^^^^

A classification based on the importance of the role that the Road Element or Ferry Connection performs in the
connectivity of the total road network.

.. _Functional Road Class Domain:

.. csv-table:: Domaine :
   :header: "Code", "Étiquette", "Définition"
   :widths: auto
   :align: left

   1, "Autoroute", "Voie de circulation à accès contrôlé, exclusivement réservée à la circulation rapide, ne comportant
   habituellement aucun croisement de même niveau ni aucun accès à des propriétés et accessible seulement par des
   bretelles aménagées à cet effet. Les piétons y sont interdits."
   2, "Route express", "Voie de circulation à accès contrôlé, aménagée pour la circulation rapide et comportant des
   croisements de même niveau à certains carrefours."
   3, "Artère", "Voie de circulation majeure ayant une moyenne à grande capacité de trafic routier."
   4, "Route collectrice", "Voie de circulation mineure utilisée principalement pour accéder à des propriétés et pour
   canaliser le trafic routier vers des routes plus importantes."
   5, "Local / Rue", "Voie de circulation lente procurant un plein accès au devant des propriétés riveraines."
   6, "Local / Semi-privé", "Voie de circulation lente procurant un accès à des propriétés ayant une restriction
   publique potentielle telle que les parcs de maisons mobiles, Premières Nations, domaines privés, résidence
   saisonnière."
   7, "Local / Inconnu", "Voie de circulation lente procurant un accès au devant des propriétés mais dont les règles
   d'accès sont inconnues."
   8, "Ruelle / Voie", "Voie de circulation lente procurant un accès à l'arrière des propriétés."
   9, "Bretelle", "Système de voies inter-reliées permettant le transfert du trafic routier entre deux ou plusieurs
   voies de circulation."
   10, "Passage étroit dont la fonction première est de donner accès pour l'extraction de ressources et qui peut
   également servir à laisser le public accéder à l'arrière-pays."
   11, "Réservée transport commun", "Voie de circulation réservée exclusivement aux autobus de transport en commun."
   12, "Service", "Tronçon de route permettant aux véhicules de s'arrêter le long d'une autoroute ou d'une route
   express. Poste de pesage, voie de service, voie d'urgence, belvédère et halte routière."
   13, "Hiver", "Route carrossable seulement en hiver lorsque les conditions permettent le passage sur lacs, rivières
   et terres humides gelés."

NID
^^^

A national unique identifier.

:Domaine: A UUID.

    Example: 69822b23d217494896014e57a2edb8ac

Route Name English (1, 2, 3, 4)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The English version of a name of a particular route in a given road network as attributed by a national or subnational
agency. A particular Road Segment or Ferry Connection Segment can belong to more than one named route. In such cases,
it has multiple route name attributes.

:Domaine: A complete English route name value such as "Trans-Canada Highway" or "None" when no value applies.

Route Name French (1, 2, 3, 4)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The French version of a name of a particular route in a given road network as attributed by a national or subnational
agency. A particular Road Segment or Ferry Connection Segment can belong to more than one named route. In such cases,
it has multiple route name attributes.

:Domaine: A complete French route name value such as "Autoroute transcanadienne" or "None" when no value applies.

Route Number (1, 2, 3, 4, 5)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ID number of a particular route in a given road network as attributed by a national or subnational agency. A
particular Road Segment or Ferry Connection Segment can belong to more than one numbered route. In such cases, it has
multiple route number attributes.

:Domaine: A route number including possible associated non-integer characters such as "A" or "None" when no value
    applies.

    Examples: 1, 1A, 230-A, 430-28.

Métadonnées d'objet
^^^^^^^^^^^^^^^^^^^

Référer aux attributs décrits dans la :ref:`Object Metadata`.

Junction
========

A feature that bounds a Road Element or a Ferry Connection. A Road Element or Ferry Connection always forms a
connection between two Junctions and, a Road Element or Ferry Connection is always bounded by exactly two Junctions. A
Junction Feature represents the physical connection between its adjoining Road Elements or Ferry Connections. A
Junction is defined at the intersection of three or more roads, at the junction of a road and a ferry, at the end of a
dead end road and at the junction of a road or ferry with a National, Provincial or Territorial Boundary.

Attribute Section
-----------------

Exit Number
^^^^^^^^^^^

The ID number of an exit on a controlled access thoroughfare that has been assigned by an administrating body.

:Domaine: An ID number including possible associated non-integer characters such as "A" or "None" when no value applies.

    Examples: 11, 11A, 11-A, 80-EST, 80-E, 80E.

Junction Type
^^^^^^^^^^^^^

The classification of a junction.

.. csv-table:: Domaine :
   :header: "Code", "Étiquette", "Définition"
   :widths: auto
   :align: left

   1, "Intersection", "Intersection entre trois Éléments routiers ou plus se rencontrant au même niveau du sol."
   2, "Cul-de-sac", "Jonction spécifique qui indique qu'un Élément routier prend fin et n'est pas relié à aucun autre
   Élément routier ou Liaison par transbordeur."
   3, "Transbordement", "Jonction spécifique qui indique qu'un Élément routier se poursuit comme Liaison par
   transbordeur."
   4, "NatProvTer", "Jonction spécifique à la limite d'un jeu de données qui indique qu'un Élément routier ou une
   Liaison par transbordeur se poursuit dans la province, territoire ou pays voisin."

NID
^^^

A national unique identifier.

:Domaine: A UUID.

    Example: 69822b23d217494896014e57a2edb8ac

Métadonnées d'objet
^^^^^^^^^^^^^^^^^^^

Référer aux attributs décrits dans la :ref:`Object Metadata`.

Road Segment
============

A road is a linear section of the earth designed for or the result of vehicular movement. A Road Segment is the
specific representation of a portion of a road with uniform characteristics.

Attribute Section
-----------------

Address Range Digitizing Direction Flag (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Indicates if the attribute event follows the same direction as the digitizing of the Road Element. A specific value is
defined for the left and right sides of the Road Element.

:Domaine: Identical to :ref:`Digitizing Direction Flag Domain`.

Address Range NID
^^^^^^^^^^^^^^^^^

A UUID assigned to each particular block face address ranges.

:Domaine: A UUID or "None" when no value applies.

    Example: 69822b23d217494896014e57a2edb8ac

Closing Period
^^^^^^^^^^^^^^

The period in which the road or ferry connection is not available to the public.

:Domaine: Identical to :ref:`Closing Period Domain`.

Exit Number
^^^^^^^^^^^

The ID number of an exit on a controlled access thoroughfare that has been assigned by an administrating body.

:Domaine: An ID number including possible associated non-integer characters such as "A" or "None" when no value applies.

    Examples: 11, 11A, 11-A, 80-EST, 80-E, 80E.

First House Number (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The first house number address value along a particular side (left or right) of a Road Element. A specific value is
defined for the left and right sides of the Road Element.

:Domaine: [-1..n] The value "0" is used when no value applies.

Functional Road Class
^^^^^^^^^^^^^^^^^^^^^

A classification based on the importance of the role that the Road Element or Ferry Connection performs in the
connectivity of the total road network.

:Domaine: Identical to :ref:`Functional Road Class Domain`.

Last House Number (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The last house number address value along a particular side (left or right) of a Road Element. A specific value is
defined for the left and right sides of the Road Element.

:Domaine: [-1..n] The value "0" is used when no value applies.

NID
^^^

A national unique identifier.

:Domaine: A UUID.

    Example: 69822b23d217494896014e57a2edb8ac

Number of Lanes
^^^^^^^^^^^^^^^

The number of lanes existing on a Road Element.

:Domaine: [1..8]

Official Place Name (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Official name of an administrative area, district or other named area which is required for uniqueness of the street
name.

:Domaine: Derived from the Street and place names table. A specific value is defined for the left and right sides of
    the Road Element. "None" when no value applies.

Official Street Name Concatenated (left, right)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A concatenation of the officially recognized Directional prefix, Street type prefix, Street name article, Street name
body, Street type suffix, Directional suffix and Muni quadrant values.

:Domaine: Derived from the Street and place names table. A specific value is defined for the left and right sides of
    the Road Element. "None" when no value applies.

Paved Road Surface Type
^^^^^^^^^^^^^^^^^^^^^^^

The type of surface a paved Road Element has.

.. csv-table:: Domaine :
   :header: "Code", "Étiquette", "Définition"
   :widths: auto
   :align: left

   0, "Aucun", "Aucune valeur ne s'applique."
   1, "Rigide", "Route revêtue ayant une surface rigide, tel le béton."
   2, "Souple", "Route revêtue ayant une surface souple, tel l'asphalte."
   3, "Pavés", "Route revêtue ayant une surface constituée de blocs, tels que les pavés en cailloutis."

Pavement Status
^^^^^^^^^^^^^^^

An indication of improvement applied to a Road surface.

.. csv-table:: Domaine :
   :header: "Code", "Étiquette", "Définition"
   :widths: auto
   :align: left

   1, "Revêtue", "Route dont la surface comporte un matériau durci, tel le béton, l'asphalte, l'empierrement goudronné
   ou le platelage d'acier."
   2, "Non revêtue", "Route dont la surface comporte un matériau meuble, tel le gravier ou la terre."

Road Jurisdiction
^^^^^^^^^^^^^^^^^

The agency with the responsibility/authority to ensure maintenance occurs but is not necessarily the one who undertakes
the maintenance directly.

:Domaine: The Agency name or "None" when no value applies.

Road Segment ID
^^^^^^^^^^^^^^^

A unique identifier within a dataset assigned to each Road Segment.

:Domaine: [1..n]

Route Name English (1, 2, 3, 4)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The English version of a name of a particular route in a given road network as attributed by a national or subnational
agency. A particular Road Segment or Ferry Connection Segment can belong to more than one named route. In such cases,
it has multiple route name attributes.

:Domaine: A complete English route name value such as "Trans-Canada Highway" or "None" when no value applies.

Route Name French (1, 2, 3, 4)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The French version of a name of a particular route in a given road network as attributed by a national or subnational
agency. A particular Road Segment or Ferry Connection Segment can belong to more than one named route. In such cases,
it has multiple route name attributes.

:Domaine: A complete French route name value such as "Autoroute transcanadienne" or "None" when no value applies.

Route Number (1, 2, 3, 4, 5)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ID number of a particular route in a given road network as attributed by a national or subnational agency. A
particular Road Segment or Ferry Connection Segment can belong to more than one numbered route. In such cases, it has
multiple route number attributes.

:Domaine: A route number including possible associated non-integer characters such as "A" or "None" when no value
    applies.

    Examples: 1, 1A, 230-A, 430-28.

Speed Restriction
^^^^^^^^^^^^^^^^^

The maximum speed allowed on the road. The value is expressed in kilometers per hour.

:Domaine: A multiple of 5, less than or equal to 120.

Structure ID
^^^^^^^^^^^^

A national unique identifier assigned to the Road Segment or the set of adjoining Road Segments forming a structure.
This identifier allows for the reconstitution of a structure that is fragmented by Junctions.

:Domaine: A UUID or "None" when no value applies.

    Example: 69822b23d217494896014e57a2edb8ac

Structure Name English
^^^^^^^^^^^^^^^^^^^^^^

The English version of the name of a road structure as assigned by a national or subnational agency.

:Domaine: A complete structure name or "None" when no value applies.

Structure Name French
^^^^^^^^^^^^^^^^^^^^^

The French version of the name of a road structure as assigned by a national or subnational agency.

:Domaine: A complete structure name or "None" when no value applies.

Structure Type
^^^^^^^^^^^^^^

The classification of a structure.

.. csv-table:: Domaine :
   :header: "Code", "Étiquette", "Définition"
   :widths: auto
   :align: left

   0, "Aucun", "Aucune valeur applicable."
   1, "Pont", "Construction anthropique supportant une route sur une structure surélevée et servant à enjamber un
   obstacle, une rivière, une autre route ou un chemin de fer."
   2, "Pont couvert", "Construction anthropique supportant une route sur une structure surélevée et couverte, servant à
   enjamber un obstacle, une rivière, une autre route ou un chemin de fer."
   3, "Pont mobile", "Construction anthropique supportant une route sur une structure surélevée et mobile, servant à
   enjamber un obstacle, une autre route ou un chemin de fer."
   4, "Pont inconnu", "Pont pour lequel il est actuellement impossible de déterminer si sa structure est couverte,
   mobile ou autre."
   5, "Tunnel", "Construction fermée anthropique servant à renfermer une route à travers ou sous un élément naturel ou
   autres obstructions."
   6, "Paraneige", "Structure anthropique couverte et érigée au-dessus d'une route en région montagneuse pour empêcher
   les glissements de neige d'obstruer la route."
   7, "Barrage", "Structure anthropique érigée au-dessus d'un cours d'eau ou d'une voie sujette aux inondations pour
   contrôler le débit d'eau, sur laquelle une route a été construite pour supporter la circulation de véhicules
   motorisés."

Traffic Direction
^^^^^^^^^^^^^^^^^

The direction(s) of traffic flow allowed on the road.

.. csv-table:: Domaine :
   :header: "Code", "Étiquette", "Définition"
   :widths: auto
   :align: left

   1, "Bi-directionel", "La circulation est permise dans les deux directions."
   2, "Même direction", "La circulation à sens unique est dans la même direction que le sens de numérisation du Segment
   routier."
   3, "Direction contraire", "La circulation à sens unique est en direction opposée au sens de numérisation du Segment
   routier."

Unpaved Road Surface Type
^^^^^^^^^^^^^^^^^^^^^^^^^

The type of surface an unpaved Road Element has.

.. csv-table:: Domaine :
   :header: "Code", "Étiquette", "Définition"
   :widths: auto
   :align: left

   0, "Aucun", "Aucune valeur ne s'applique."
   1, "Gravier", "Chemin de terre dont la surface a été améliorée par nivellement avec du gravier."
   2, "Terre", "Des routes dont la surface est formée par l’enlèvement de la végétation et/ou par le va-et-vient des
   véhicules sur cette route, ce qui nuit à la croissance de toute végétation."

Métadonnées d'objet
^^^^^^^^^^^^^^^^^^^

Référer aux attributs décrits dans la :ref:`Object Metadata`.

Street and Place Names
======================

A street name recognized by the municipality or naming authority and a name of an administrative area, district or
other named area which is required for uniqueness of the street name.

Attribute Section
-----------------

Directional Prefix
^^^^^^^^^^^^^^^^^^

A geographic direction that is part of the street name and precedes the street name body or, if appropriate, the street
type prefix.

.. _Street Direction Domain:

.. csv-table:: Domaine :
   :header: "Code", "Étiquette", "Définition"
   :widths: auto
   :align: left

   0, "Aucun", "Aucune valeur ne s'applique."
   1, "North", ""
   2, "Nord", ""
   3, "South", ""
   4, "Sud", ""
   5, "East", ""
   6, "Est", ""
   7, "West", ""
   8, "Ouest", ""
   9, "Northwest", ""
   10, "Nord-ouest", ""
   11, "Northeast", ""
   12, "Nord-est", ""
   13, "Southwest", ""
   14, "Sud-ouest", ""
   15, "Southeast", ""
   16, "Sud-est", ""
   17, "Central", ""
   18, "Centre", ""

Directional Suffix
^^^^^^^^^^^^^^^^^^

A geographic direction that is part of the street name and succeeds the street name body or, if appropriate, the street
type suffix.

:Domaine: Identical to :ref:`Street Direction Domain`.

Muni Quadrant
^^^^^^^^^^^^^

The attribute Muni quadrant is used in some addresses much like the directional attributes where the town is divided
into sections based on major east-west and north-south divisions. The effect is as if multiple directional were used.

.. csv-table:: Domaine :
   :header: "Code", "Étiquette", "Définition"
   :widths: auto
   :align: left

   0, "Aucun", "Aucune valeur ne s'applique."
   1, "Sud-ouest", ""
   2, "Sud-est", ""
   3, "Nord-est", ""
   4, "Nord-ouest", ""

NID
^^^

A national unique identifier.

:Domaine: A UUID.

    Example: 69822b23d217494896014e57a2edb8ac

Place Name
^^^^^^^^^^

Name of an administrative area, district or other named area which is required for uniqueness of the street name.

:Domaine: The complete name of the place.

    Examples: Arnold's Cove, Saint-Jean-Baptiste-de-l'Îsle-Verte, Sault Ste. Marie, Grand-Sault, Grand Falls.

Place Type
^^^^^^^^^^

Expression specifying the type of place.

:Domaine: Conforms to Census Subdivision (CSD) types and is periodically updated to reflect changes in those values.

    Examples: C (City / Cité), IRI (Indian reserve / Réserve indienne), M (Municipality / Municipalité).

Province
^^^^^^^^

Province or Territory where the place is located.

:Domaine: Identical to :ref:`Dataset Name Domain`.

Street Name Article
^^^^^^^^^^^^^^^^^^^

Article(s) that is/are part of the street name and located at the beginning.

.. csv-table:: Domaine :
   :header: "Étiquette", "Définition"
   :widths: auto
   :align: left

   "Aucun", ""
   "à", ""
   "à l'", ""
   "à la", ""
   "au", ""
   "aux", ""
   "by the", ""
   "chez", ""
   "d'", ""
   "de", ""
   "de l'", ""
   "de la", ""
   "des", ""
   "du", ""
   "l'", ""
   "la", ""
   "le", ""
   "les", ""
   "of the", ""
   "the", ""

Street Name Body
^^^^^^^^^^^^^^^^

The portion of the street name (either official or alternate) that has the most identifying power excluding street type
and directional prefixes or suffixes and street name articles.

:Domaine: The complete street name body or "None" when no value applies.

    Examples: Capitale, Trésor, Golf, Abbott, Abbott's, Main, Church, Park, Bread and Cheese.

Street Type Prefix
^^^^^^^^^^^^^^^^^^

A part of the street name of a Road Element identifying the street type. A prefix precedes the street name body of a
Road Element.

.. _Street Type Domain:

.. csv-table:: Domaine (de nouvelles valeurs sont ajoutées périodiquement) :
   :header: "Code", "Étiquette", "Définition"
   :widths: auto
   :align: left
   :class: longtable

   0, "Aucun", "Aucune valeur ne s'applique."
   1, "Abbey", ""
   2, "Access", ""
   3, "Acres", ""
   4, "Aire", ""
   5, "Allée", ""
   6, "Alley", ""
   7, "Autoroute", ""
   8, "Avenue", ""
   9, "Barrage", ""
   10, "Bay", ""
   11, "Beach", ""
   12, "Bend", ""
   13, "Bloc", ""
   14, "Block", ""
   15, "Boulevard", ""
   16, "Bourg", ""
   17, "Brook", ""
   18, "By-pass", ""
   19, "Byway", ""
   20, "Campus", ""
   21, "Cape", ""
   22, "Carre", ""
   23, "Carrefour", ""
   24, "Centre", ""
   25, "Cercle", ""
   26, "Chase", ""
   27, "Chemin", ""
   28, "Circle", ""
   29, "Circuit", ""
   30, "Close", ""
   31, "Common", ""
   32, "Concession", ""
   33, "Corners", ""
   34, "Côte", ""
   35, "Cour", ""
   36, "Court", ""
   37, "Cove", ""
   38, "Crescent", ""
   39, "Croft", ""
   40, "Croissant", ""
   41, "Crossing", ""
   42, "Crossroads", ""
   43, "Cul-de-sac", ""
   44, "Dale", ""
   45, "Dell", ""
   46, "Desserte", ""
   47, "Diversion", ""
   48, "Downs", ""
   49, "Drive", ""
   50, "Droit de passage", ""
   51, "Échangeur", ""
   52, "End", ""
   53, "Esplanade", ""
   54, "Estates", ""
   55, "Expressway", ""
   56, "Extension", ""
   57, "Farm", ""
   58, "Field", ""
   59, "Forest", ""
   60, "Freeway", ""
   61, "Front", ""
   62, "Gardens", ""
   63, "Gate", ""
   64, "Glade", ""
   65, "Glen", ""
   66, "Green", ""
   67, "Grounds", ""
   68, "Grove", ""
   69, "Harbour", ""
   70, "Haven", ""
   71, "Heath", ""
   72, "Heights", ""
   73, "Highlands", ""
   74, "Highway", ""
   75, "Hill", ""
   76, "Hollow", ""
   77, "Île", ""
   78, "Impasse", ""
   79, "Island", ""
   80, "Key", ""
   81, "Knoll", ""
   82, "Landing", ""
   83, "Lane", ""
   84, "Laneway", ""
   85, "Limits", ""
   86, "Line", ""
   87, "Link", ""
   88, "Lookout", ""
   89, "Loop", ""
   90, "Mall", ""
   91, "Manor", ""
   92, "Maze", ""
   93, "Meadow", ""
   94, "Mews", ""
   95, "Montée", ""
   96, "Moor", ""
   97, "Mount", ""
   98, "Mountain", ""
   99, "Orchard", ""
   100, "Parade", ""
   101, "Parc", ""
   102, "Park", ""
   103, "Parkway", ""
   104, "Passage", ""
   105, "Path", ""
   106, "Pathway", ""
   107, "Peak", ""
   108, "Pines", ""
   109, "Place", ""
   110, "Place", ""
   111, "Plateau", ""
   112, "Plaza", ""
   113, "Point", ""
   114, "Port", ""
   115, "Private", ""
   116, "Promenade", ""
   117, "Quay", ""
   118, "Rang", ""
   119, "Range", ""
   120, "Reach", ""
   121, "Ridge", ""
   122, "Right of Way", ""
   123, "Rise", ""
   124, "Road", ""
   125, "Rond Point", ""
   126, "Route", ""
   127, "Row", ""
   128, "Rue", ""
   129, "Ruelle", ""
   130, "Ruisseau", ""
   131, "Run", ""
   132, "Section", ""
   133, "Sentier", ""
   134, "Sideroad", ""
   135, "Square", ""
   136, "Street", ""
   137, "Stroll", ""
   138, "Subdivision", ""
   139, "Terrace", ""
   140, "Terrasse", ""
   141, "Thicket", ""
   142, "Towers", ""
   143, "Townline", ""
   144, "Trace", ""
   145, "Trail", ""
   146, "Trunk", ""
   147, "Turnabout", ""
   148, "Vale", ""
   149, "Via", ""
   150, "View", ""
   151, "Village", ""
   152, "Vista", ""
   153, "Voie", ""
   154, "Walk", ""
   155, "Way", ""
   156, "Wharf", ""
   157, "Wood", ""
   158, "Woods", ""
   159, "Wynd", ""
   160, "Driveway", ""
   161, "Height", ""
   162, "Roadway", ""
   163, "Strip", ""
   164, "Concession Road", ""
   165, "Corner", ""
   166, "County Road", ""
   167, "Crossroad", ""
   168, "Fire Route", ""
   169, "Garden", ""
   170, "Hills", ""
   171, "Isle", ""
   172, "Lanes", ""
   173, "Pointe", ""
   174, "Regional Road", ""
   175, "Autoroute à péage", ""
   176, "Baie", ""
   177, "Bluff", ""
   178, "Bocage", ""
   179, "Bois", ""
   180, "Boucle", ""
   181, "Bretelle", ""
   182, "Cap", ""
   183, "Causeway", ""
   184, "Chaussée", ""
   185, "Contournement", ""
   186, "Couloir", ""
   187, "Crête", ""
   188, "Croix", ""
   189, "Cross", ""
   190, "Dead End", ""
   191, "Débarquement", ""
   192, "Entrance", ""
   193, "Entrée", ""
   194, "Evergreen", ""
   195, "Exit", ""
   196, "Étang", ""
   197, "Falaise", ""
   198, "Jardin", ""
   199, "Lawn", ""
   200, "Lien", ""
   201, "Ligne", ""
   202, "Manoir", ""
   203, "Pass", ""
   204, "Pente", ""
   205, "Pond", ""
   206, "Quai", ""
   207, "Ramp", ""
   208, "Rampe", ""
   209, "Rangée", ""
   210, "Roundabout", ""
   211, "Route de plaisance", ""
   212, "Route sur élevée", ""
   213, "Side", ""
   214, "Sortie", ""
   215, "Throughway", ""
   216, "Took", ""
   217, "Turn", ""
   218, "Turnpike", ""
   219, "Vallée", ""
   220, "Villas", ""
   221, "Virage", ""
   222, "Voie oust", ""
   223, "Voie rapide", ""
   224, "Vue", ""
   225, "Westway", ""
   226, "Arm", ""
   227, "Baseline", ""
   228, "Bourne", ""
   229, "Branch", ""
   230, "Bridge", ""
   231, "Burn", ""
   232, "Bypass", ""
   233, "Camp", ""
   234, "Chart", ""
   235, "Club", ""
   236, "Copse", ""
   237, "Creek", ""
   238, "Crest", ""
   239, "Cul De Sac", ""
   240, "Curve", ""
   241, "Cut", ""
   242, "Fairway", ""
   243, "Gateway", ""
   244, "Greenway", ""
   245, "Inamo", ""
   246, "Inlet", ""
   247, "Junction", ""
   248, "Keep", ""
   249, "Lake", ""
   250, "Lakes", ""
   251, "Lakeway", ""
   252, "Market", ""
   253, "Millway", ""
   254, "Outlook", ""
   255, "Oval", ""
   256, "Overpass", ""
   257, "Pier", ""
   258, "River", ""
   259, "Service", ""
   260, "Shore", ""
   261, "Shores", ""
   262, "Sideline", ""
   263, "Spur", ""
   264, "Surf", ""
   265, "Track", ""
   266, "Valley", ""
   267, "Walkway", ""
   268, "Wold", ""
   269, "Tili", ""
   270, "Nook", ""
   271, "Drung", ""

Street Type Suffix
^^^^^^^^^^^^^^^^^^

A part of the street name of a Road Element identifying the street type. A suffix follows the street name body of a
Road Element.

:Domaine: Identical to :ref:`Street Type Domain`.

Métadonnées d'objet
^^^^^^^^^^^^^^^^^^^

Référer aux attributs décrits dans la :ref:`Object Metadata`.

Toll Point
==========

Place where a right-of-way is charged to gain access to a motorway, a bridge, etc.

Attribute Section
-----------------

NID
^^^

A national unique identifier.

:Domaine: A UUID.

    Example: 69822b23d217494896014e57a2edb8ac

Road Element NID
^^^^^^^^^^^^^^^^

The NID of the Road Element on which the point geometry is located.

:Domaine: A UUID.

    Example: 69822b23d217494896014e57a2edb8ac

Toll Point Type
^^^^^^^^^^^^^^^

The type of toll point.

.. csv-table:: Domaine :
   :header: "Code", "Étiquette", "Définition"
   :widths: auto
   :align: left

   1, "Poste de péage", "Un poste de péage est une structure en bordure d'une route ou en travers de celle-ci où des
   péages sont perçus par des employés d'un organisme responsable de la collecte, par des appareils capable de
   reconnaître la monnaie métallique et papier ou par paiement électronique (carte de crédit ou carte bancaire)."
   2, "Poste de péage virtuel", "À un poste de péage virtuel, le péage est imputé par enregistrement automatique du
   véhicule passant, au moyen d'un abonnement ou de facturation."
   3, "Hybride", "Poste de péage conventionnel et virtuel à la fois."

Métadonnées d'objet
^^^^^^^^^^^^^^^^^^^

Référer aux attributs décrits dans la :ref:`Object Metadata`.
