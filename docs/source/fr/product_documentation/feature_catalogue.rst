*******************
Catalogue d'entités
*******************

.. include:: <isonum.txt>
.. include:: <isopub.txt>

.. admonition:: Notez

    La description des entités et attributs de ce catalogue est en grande partie extraite de la norme internationale
    *ISO 14825 — Systèmes de transport intelligents — Fichiers de données géographiques — Spécification des données
    globales* du comité technique ISO/TC 204.

    Ce catalogue a été adapté à partir de la norme internationale *ISO 19110 — Information géographique — Méthodologie
    de catalogage des entités* préparée par le comité technique ISO/TC 211.

.. contents:: Matières :
   :depth: 3

Types de données
================

Les types de données pour tous les attributs de toutes les entités sont décrits dans le
:doc:`product_distribution_formats`.

Données manquantes
==================

Cette section s'applique à tous les attributs de toutes les entités.

``-1`` (nombre) / ``Inconnu`` (caractère) est utilisé lorsqu'une valeur est inconnue, manquante ou invalide (pas dans
le domaine de l'attribut).

.. _Object Metadata fr:

Métadonnées d'objet
===================

Les attributs décrits dans la section métadonnées d'objet s'appliquent à toutes les entités (sauf pour Lien nom non
officiel où seulement Date création, Nom jeu de données et Version normes s'appliquent).

Couverture
----------

Cette valeur indique si les métadonnées s'appliquent à tout l'Élément linéaire du réseau ou à une portion de celui-ci.

.. csv-table::
   :header: "Code", "Étiquette", "Définition"
   :widths: auto
   :align: left

   1, "Complet", "Les métadonnées s'appliquent à la totalité de la géométrie ou de l'événement."
   2, "Partiel", "Les métadonnées s'appliquent à une portion de la géométrie ou de l'événement."

Date création
-------------

La date de création des données.

:Domaine: Une date selon le format AAAAMMJJ. Si le mois ou le jour est inconnu, les caractères correspondants sont
          laissés vides.

          | Exemples : 20060630, 200606, 2006.

Date révision
-------------

La date de révision des données.

:Domaine: Une date selon le format AAAAMMJJ. Si le mois ou le jour est inconnu, les caractères correspondants sont
          laissés vides. La valeur ``0`` indique qu'aucune valeur ne s'applique.

          | Exemples : 20060630, 200606, 2006.

Fournisseur
-----------

L'affiliation de l'organisme qui a généré (acquis ou révisé) l'objet.

.. csv-table::
   :header: "Code", "Étiquette", "Définition"
   :widths: auto
   :align: left

   1, "Autre", "Valeur autre."
   2, "Fédéral", "Département ou agence fédéral."
   3, "Provincial / Territorial", "Département ou agence provincial / territorial."
   4, "Municipal", "Département ou agence municipal."

.. _Dataset Name Domain fr:

Nom jeu de données
------------------

Province ou territoire couvert par le jeu de données.

.. csv-table::
   :header: "Code", "Étiquette"
   :widths: auto
   :align: left

   1, "Terre-Neuve et Labrador"
   2, "Nouvelle-Écosse"
   3, "Île-du-Prince-Édouard"
   4, "Nouveau-Brunswick"
   5, "Québec"
   6, "Ontario"
   7, "Manitoba"
   8, "Saskatchewan"
   9, "Alberta"
   10, "Colombie-Britannique"
   11, "Yukon"
   12, "Territoires du Nord-Ouest"
   13, "Nunavut"

Précision planimétrique
-----------------------

Précision planimétrique exprimée en mètres selon la précision cartographique circulaire normalisée (PCCN).

:Domaine: [-1,1..n]

Technique acquisition
---------------------

Le type de source ou la technique utilisé pour acquérir (création ou révision) les données.

.. csv-table::
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

Version normes
--------------

Le numéro de version des spécifications du produit GéoBase.

:Domaine: [2.0]

Intervalles d'adresse
=====================

Ensemble d'attributs qui représente l'adresse du premier et du dernier édifice situés de chaque côté d'un Élément
routier.

Section attribut
----------------

IDN
^^^

Un identifiant national unique.

:Domaine: Un IDUU.

          | Exemple : 69822b23d217494896014e57a2edb8ac

IDN nom de rue non officiel (gauche, droite)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

L'identifiant utilisé pour lier l'intervalle d'adresse à son ou ses noms de rue non reconnu(s) officiellement. Une
valeur spécifique est définie pour les côtés gauche et droit de l'Élément routier.

:Domaine: Un IDUU ou ``Aucun`` quand aucune valeur ne s'applique.

          | Exemple : 69822b23d217494896014e57a2edb8ac

IDN nom de rue officiel (gauche, droite)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

L'identifiant utilisé pour lier l'intervalle d'adresse à son nom de rue reconnu officiellement. Une valeur spécifique
est définie pour les côtés gauche et droit de l'Élément routier.

:Domaine: Un IDUU ou ``Aucun`` quand aucune valeur ne s'applique.

          | Exemple : 69822b23d217494896014e57a2edb8ac

.. _Digitizing Direction Flag Domain fr:

Indicateur sens numérisation (gauche, droite)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Indique si l'événement attributif est dans le même sens que celui de la numérisation de l'Élément routier. Une valeur
spécifique est définie pour les côtés gauche et droit de l'Élément routier.

.. csv-table::
   :header: "Code", "Étiquette", "Définition"
   :widths: auto
   :align: left

   1, "Même sens", "Le sens de l'événement attributif et celui de la numérisation de l'Élément routier sont les mêmes."
   2, "Sens opposé", "Le sens de l'événement attributif et celui de la numérisation de l'Élément routier sont opposés."
   3, "Sans objet", "Le sens de numération de l'Élément routier est inutile pour l'événement attributif."

Indicateur système référence (gauche, droite)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Indicateur qui précise si l'adresse physique de tout Élément routier ou d'une partie de celui-ci est basé sur un
système particulier d'adressage. Une valeur spécifique est définie pour les côtés gauche et droit de l'Élément routier.

.. csv-table::
   :header: "Code", "Étiquette", "Définition"
   :widths: auto
   :align: left

   0, "Aucun", "Aucun indicateur du système de référence."
   1, "Civique", ""
   2, "Lot et concession", ""
   3, "Mesuré 911", ""
   4, "Civique 911", ""
   5, "DLS", "Dominion Land Survey, système de découpage des provinces des prairies."

Numéro dernière maison (gauche, droite)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Adresse du dernier bâtiment situé le long d'un côté particulier (gauche ou droit) d'un Élément routier. Une valeur
spécifique est définie pour les côtés gauche et droit de l'Élément routier.

:Domaine: [-1..n] La valeur ``0`` indique qu'aucune valeur ne s'applique.

Numéro première maison (gauche, droite)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Adresse du premier bâtiment situé le long d'un côté particulier (gauche ou droit) d'un Élément routier. Une valeur
spécifique est définie pour les côtés gauche et droit de l'Élément routier.

:Domaine: [-1..n] La valeur ``0`` indique qu'aucune valeur ne s'applique.

Structure numéro maison (gauche, droite)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Type de numérotation de maisons (ou numéro d'adresse) appliqué à un côté d'un Élément routier particulier. Une valeur
spécifique est définie pour les côtés gauche et droit de l'Élément routier.

.. csv-table::
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

Suffixe numéro dernière maison (gauche, droite)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Valeur non-entière telle une fraction (exemple : 1⁄4) ou un caractère alphabétique (exemple : A) qui suit à l'occasion
le numéro civique d'une maison. Une valeur spécifique est définie pour les côtés gauche et droit de l'Élément routier.

:Domaine: Une valeur non entière ou ``Aucun`` quand aucune valeur ne s'applique.

Suffixe numéro première maison (gauche, droite)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Valeur non-entière telle une fraction (exemple : 1⁄4) ou un caractère alphabétique (exemple : A) qui suit à l'occasion
le numéro civique d'une maison. Une valeur spécifique est définie pour les côtés gauche et droit de l'Élément routier.

:Domaine: Une valeur non entière ou ``Aucun`` quand aucune valeur ne s'applique.

.. _House Number Type Domain fr:

Type numérotation dernière maison (gauche, droite)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Méthode utilisée pour acquérir l'intervalle d'adresse. Une valeur spécifique est définie pour les côtés gauche et droit
de l'Élément routier.

.. csv-table::
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

Type numérotation première maison (gauche, droite)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Méthode utilisée pour acquérir l'intervalle d'adresse. Une valeur spécifique est définie pour les côtés gauche et droit
de l'Élément routier.

:Domaine: Identique à :ref:`House Number Type Domain fr`.

Métadonnées d'objet
^^^^^^^^^^^^^^^^^^^

Référer aux attributs décrits dans la :ref:`Object Metadata fr`.

Jonction
========

Une entité positionnée à chaque extrémité d'un Élément routier ou d'une Liaison par transbordeur (fournir la définition
ou indiquer Segment de liaison par transbordeur). Un Élément routier ou une Liaison par transbordeur forme toujours une
liaison entre deux Jonctions et, un Élément routier ou une Liaison par transbordeur est toujours délimitée par
exactement deux Jonctions. Une entité Jonction représente la connexion physique existant entre les Éléments routiers et
Liaisons par transbordeur attenants. Une Jonction se situe à l'intersection de trois Éléments routiers ou plus, à
l'intersection d'un Élément routier et d'une Liaison par transbordeur, à la fin d'un cul-de-sac ou à l'intersection
d'un Élément routier ou d'une Liaison par transbordeur avec une frontière internationale, provinciale ou territoriale.

Section attribut
----------------

IDN
^^^

Un identifiant national unique.

:Domaine: Un IDUU.

          | Exemple : 69822b23d217494896014e57a2edb8ac

Numéro de sortie
^^^^^^^^^^^^^^^^

Le numéro d'identifiant d'une sortie sur une voie de circulation à accès contrôlé qui a été attribué par une autorité
administrative.

:Domaine: Un numéro d'identifiant y compris les caractères non entiers tels que ``A`` qui y sont parfois associés ou
          ``Aucun`` quand aucune valeur ne s'applique.

          | Exemples : 11, 11A, 11-A, 80-EST, 80-E, 80E.

Type jonction
^^^^^^^^^^^^^

La classification du type de jonction.

.. csv-table::
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

Métadonnées d'objet
^^^^^^^^^^^^^^^^^^^

Référer aux attributs décrits dans la :ref:`Object Metadata fr`.

Lien nom non officiel
=====================

Une table de correspondance qui définit une ou plusieurs relations entre les intervalles d'adresses et ses noms de rue
et de lieu non officiels utilisés ou connus par le public en général.

Section attribut
----------------

IDN
^^^

Un identifiant national unique.

:Domaine: Un IDUU.

          | Exemple : 69822b23d217494896014e57a2edb8ac

IDN nom de rue
^^^^^^^^^^^^^^

L'IDN du nom rue et de lieu non officiel.

:Domaine: Un IDUU.

          | Exemple : 69822b23d217494896014e57a2edb8ac

Métadonnées d'objet
^^^^^^^^^^^^^^^^^^^

Référer aux attributs décrits dans la :ref:`Object Metadata fr`.

Noms de rue et de lieu
======================

Un nom de rue reconnu par la municipalité ou autre autorité compétente et un nom de municipalité, district ou autre
territoire administratif nommé requis pour assurer l'unicité du nom de rue.

Section attribut
----------------

Article nom rue
^^^^^^^^^^^^^^^

Article(s) qui fait (font) partie du nom d'une rue et qui précède immédiatement le Corps nom rue.

.. csv-table::
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

Corps nom rue
^^^^^^^^^^^^^

La portion, la plus significative, d'un nom de rue (officiel ou non) excluant les préfixes ou suffixes de types de rue
et de direction ainsi que les articles de nom de rue.

:Domaine: La valeur complète du Corps nom rue ou ``Aucun`` quand aucune valeur ne s'applique.

          | Exemples : Capitale, Trésor, Golf, Abbott, Abbott's, Main, Church, Park, Bread and Cheese.

IDN
^^^

Un identifiant national unique.

:Domaine: Un IDUU.

          | Exemple : 69822b23d217494896014e57a2edb8ac

Muni quadrant
^^^^^^^^^^^^^

L'attribut Muni quadrant est utilisé dans certains noms de rue comme un attribut de direction dans les municipalités
qui sont divisées en sections selon des axes est-ouest et nord-sud. Il en résulte l'impression que le nom de rue
contient plusieurs attributs directionnels.

.. csv-table::
   :header: "Code", "Étiquette", "Définition"
   :widths: auto
   :align: left

   0, "Aucun", "Aucune valeur ne s'applique."
   1, "Sud-ouest", ""
   2, "Sud-est", ""
   3, "Nord-est", ""
   4, "Nord-ouest", ""

Nom de lieu
^^^^^^^^^^^

Nom d'une municipalité, d'un district ou d'un autre territoire administratif nommé requis pour assurer l'unicité du nom
de rue.

:Domaine: Le nom complet d'un lieu.

          | Exemples : Arnold's Cove, Saint-Jean-Baptiste-de-l'Îsle-Verte, Sault Ste. Marie, Grand-Sault, Grand Falls.

.. _Street Direction Domain fr:

Préfixe direction
^^^^^^^^^^^^^^^^^

Direction géographique qui fait partie du nom d'une rue et qui précède le corps nom rue ou, s'il y a lieu, le préfixe
type rue.

.. csv-table::
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

.. _Street Type Domain fr:

Préfixe type rue
^^^^^^^^^^^^^^^^

Partie du nom d'une rue qui identifie le type de rue d'un Élément routier, y compris les articles et prépositions
possibles. Un préfixe précède le corps nom rue d'un Élément routier.

.. admonition:: Notez

    De nouvelles valeurs sont ajoutées périodiquement.

.. csv-table::
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
   239, "Curve", ""
   240, "Cut", ""
   241, "Fairway", ""
   242, "Gateway", ""
   243, "Greenway", ""
   244, "Inamo", ""
   245, "Inlet", ""
   246, "Junction", ""
   247, "Keep", ""
   248, "Lake", ""
   249, "Lakes", ""
   250, "Lakeway", ""
   251, "Market", ""
   252, "Millway", ""
   253, "Outlook", ""
   254, "Oval", ""
   255, "Overpass", ""
   256, "Pier", ""
   257, "River", ""
   258, "Service", ""
   259, "Shore", ""
   260, "Shores", ""
   261, "Sideline", ""
   262, "Spur", ""
   263, "Surf", ""
   264, "Track", ""
   265, "Valley", ""
   266, "Walkway", ""
   267, "Wold", ""
   268, "Tili", ""
   269, "Nook", ""
   270, "Drung", ""
   271, "Awti", ""
   272, "Awti'j", ""
   273, "Rest", ""
   274, "Rotary", ""
   275, "Connection", ""
   276, "Estate", ""
   277, "Crossover", ""
   278, "Hideaway", ""
   279, "Linkway", ""

Province
^^^^^^^^

Nom de la province ou du territoire dans lequel se situe le lieu.

:Domaine: Identique à :ref:`Dataset Name Domain fr`.

Suffixe direction
^^^^^^^^^^^^^^^^^

Direction géographique qui fait partie du nom d'une rue et qui suit le corps nom rue ou, s'il y a lieu, le suffixe type
rue.

:Domaine: Identique à :ref:`Street Direction Domain fr`.

Suffixe type rue
^^^^^^^^^^^^^^^^

Partie du nom d'une rue qui identifie le type de rue d'un Élément routier, y compris les articles et prépositions
possibles. Un suffixe suit le corps nom de rue d'un Élément routier.

:Domaine: Identique à :ref:`Street Type Domain fr`.

Type de lieu
^^^^^^^^^^^^

Expression spécifiant le type de lieu.

:Domaine: Conforme aux types de subdivisions de recensement (SDR) et est périodiquement mis à jour pour refléter les
          changements dans ces valeurs.

          | Exemples : C (City / Cité), IRI (Indian reserve / Réserve indienne), M (Municipality / Municipalité).

Métadonnées d'objet
^^^^^^^^^^^^^^^^^^^

Référer aux attributs décrits dans la :ref:`Object Metadata fr`.

Passage obstrué
===============

Indication de la présence d'un obstacle sur un Élément routier pour empêcher ou contrôler l'accès.

Section attribut
----------------

IDN
^^^

Un identifiant national unique.

:Domaine: Un IDUU.

          | Exemple : 69822b23d217494896014e57a2edb8ac

IDN élément routier
^^^^^^^^^^^^^^^^^^^

L'IDN de l'Élément routier sur lequel la géométrie ponctuelle est positionnée.

:Domaine: Un IDUU.

          | Exemple : 69822b23d217494896014e57a2edb8ac

Type passage obstrué
^^^^^^^^^^^^^^^^^^^^

Le type de passage obstrué qui indique si celui-ci est amovible.

.. csv-table::
   :header: "Code", "Étiquette", "Définition"
   :widths: auto
   :align: left

   1, "Permanente", "La barrière ou l'obstacle doit être détruit ou enlevé au moyen de machinerie lourde pour permettre
   l'accès. Les blocs de béton et les remblais de terre constituent des exemples d'obstructions considérées
   permanentes."
   2, "Amovible", "La barrière est conçue pour permettre l'accès à (l'autre côté de) l'Élément routier qu'elle bloque.
   Lorsque voulu, l'accès peut facilement être permis."

Métadonnées d'objet
^^^^^^^^^^^^^^^^^^^

Référer aux attributs décrits dans la :ref:`Object Metadata fr`.

Poste de péage
==============

Emplacement où un droit de passage est prélevé pour avoir accès à une autoroute, un pont, etc.

Section attribut
----------------

IDN
^^^

Un identifiant national unique.

:Domaine: Un IDUU.

          | Exemple : 69822b23d217494896014e57a2edb8ac

IDN élément routier
^^^^^^^^^^^^^^^^^^^

L'IDN de l'Élément routier sur lequel la géométrie ponctuelle est positionnée.

:Domaine: Un IDUU.

          | Exemple : 69822b23d217494896014e57a2edb8ac

Type poste de péage
^^^^^^^^^^^^^^^^^^^

Le type de poste de péage.

.. csv-table::
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

Référer aux attributs décrits dans la :ref:`Object Metadata fr`.

Segment de liaison par transbordeur
===================================

Route approximative suivie par un navire transbordeur qui transporte des véhicules entre deux emplacements sur le
réseau routier.

Section attribut
----------------

.. _Functional Road Class Domain fr:

Classification routière fonctionnelle
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Une classification basée sur l'importance du rôle de l'Élément routier ou de la Liaison par transbordeur dans la
connectivité du réseau routier.

.. csv-table::
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

IDN
^^^

Un identifiant national unique.

:Domaine: Un IDUU.

          | Exemple : 69822b23d217494896014e57a2edb8ac

ID segment liaison par transbordeur
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Un identifiant unique à l'intérieur d'un jeu de données associé à chaque instance de Segment de liaison par
transbordeur.

:Domaine: [1..n]

Nom de route anglais (1, 2, 3, 4)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

La version anglaise du nom d'une route dans un réseau routier donné tel qu'attribué par un organisme national ou
infranational. Il se peut qu'un Élément routier ou Liaison par transbordeur porte plus d'un nom. Ainsi, un Élément
routier ou Liaison par transbordeur peut avoir plusieurs attributs nom de route.

:Domaine: Un nom de route anglais complet tel que ``Trans-Canada Highway`` ou ``Aucun`` quand aucune valeur ne
          s'applique.

Nom de route français (1, 2, 3, 4)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

La version française du nom d'une route dans un réseau routier donné tel qu'attribué par un organisme national ou
infranational. Il se peut qu'un Élément routier ou Liaison par transbordeur porte plus d'un nom. Ainsi, un Élément
routier ou Liaison par transbordeur peut avoir plusieurs attributs nom de route.

:Domaine: Un nom de route français complet tel que ``Autoroute transcanadienne`` ou ``Aucun`` quand aucune valeur ne
          s'applique.

Numéro de route (1, 2, 3, 4, 5)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Numéro d'identifiant d'une route dans un réseau routier tel qu'attribué par un organisme national ou infranational. Il
se peut qu'un Élément routier ou Liaison par transbordeur porte plus d'un numéro. Ainsi, un Élément routier ou Liaison
par transbordeur peut avoir plusieurs attributs numéro de route.

:Domaine: Un numéro de route y compris les caractères non entiers qui y sont parfois associés ou ``Aucun`` quand aucune
          valeur ne s'applique.

          | Exemples : 1, 1A, 230-A, 430-28.

.. _Closing Period Domain fr:

Période de fermeture
^^^^^^^^^^^^^^^^^^^^

Période au cours de laquelle la route ou la liaison par transbordeur n'est pas accessible au public.

.. csv-table::
   :header: "Code", "Étiquette", "Définition"
   :widths: auto
   :align: left

   0, "Aucun", "Il n'y a pas de période de fermeture. La route ou la liaison par transbordeur est accessible toute
   l'année."
   1, "Été", "Période au cours de laquelle l'absence de glace et de neige empêche l'accès à la route ou à la liaison
   par transbordeur."
   2, "Hiver", "Période au cours de laquelle la présence de glace et de neige empêche l'accès à la route ou à la
   liaison par transbordeur."

Métadonnées d'objet
^^^^^^^^^^^^^^^^^^^

Référer aux attributs décrits dans la :ref:`Object Metadata fr`.

Segment routier
===============

Une route est une section linéaire à la surface de la Terre qui a été conçue pour la circulation de véhicules ou qui en
est le résultat. Un Segment routier est la représentation spécifique d'une portion de route dont les caractéristiques
sont uniformes.

Section attribut
----------------

Autorité route
^^^^^^^^^^^^^^

Organisation qui a la responsabilité d'assurer la maintenance ou de voir au maintien de la route sans nécessairement
être celle qui fait la maintenance directement.

:Domaine: Un nom d'organisation ou ``Aucun`` quand aucune valeur ne s'applique.

Classification routière fonctionnelle
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Une classification basée sur l'importance du rôle de l'Élément routier ou de la Liaison par transbordeur dans la
connectivité du réseau routier.

:Domaine: Identique à :ref:`Functional Road Class Domain fr`.

État revêtement
^^^^^^^^^^^^^^^

Indication de la consolidation apportée à une chaussée.

.. csv-table::
   :header: "Code", "Étiquette", "Définition"
   :widths: auto
   :align: left

   1, "Revêtue", "Route dont la surface comporte un matériau durci, tel le béton, l'asphalte, l'empierrement goudronné
   ou le platelage d'acier."
   2, "Non revêtue", "Route dont la surface comporte un matériau meuble, tel le gravier ou la terre."

IDN
^^^

Un identifiant national unique.

:Domaine: Un IDUU.

          | Exemple : 69822b23d217494896014e57a2edb8ac

IDN intervalle d'adresse
^^^^^^^^^^^^^^^^^^^^^^^^

Un IDUU associé à chaque intervalle d'adresse.

:Domaine: Un IDUU ou ``Aucun`` quand aucune valeur ne s'applique.

          | Exemple : 69822b23d217494896014e57a2edb8ac

ID structure
^^^^^^^^^^^^

Un identifiant unique attribué au segment routier ou à l'ensemble de segments routiers formant une structure. Cet
identifiant permet la reconstitution d'une structure fragmentée par des jonctions.

:Domaine: Un IDUU ou ``Aucun`` quand aucune valeur ne s'applique.

          | Exemple : 69822b23d217494896014e57a2edb8ac

ID segment routier
^^^^^^^^^^^^^^^^^^

Un identifiant unique à l'intérieur d'un jeu de données associé à chaque instance de Segment routier.

:Domaine: [1..n]

Indicateur sens numérisation adresse (gauche, droite)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Indique si un événement attributif est dans le même sens que celui de la numérisation de l'Élément routier. Une valeur
spécifique est définie pour les côtés gauche et droit de l'Élément routier.

:Domaine: Identique à :ref:`Digitizing Direction Flag Domain fr`.

Limite de vitesse
^^^^^^^^^^^^^^^^^

Vitesse maximale permise sur la route. La valeur est exprimé en kilomètres heure.

:Domaine: Un multiple de 5 inférieur ou égal à 120.

Nombre de voies
^^^^^^^^^^^^^^^

Nombre de voies existant sur un Élément routier.

:Domaine: [1..8]

Nom de lieu officiel (gauche, droite)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Nom d'une municipalité, d'un district ou d'un autre territoire administratif nommé requis pour assurer l'unicité du nom
de rue.

:Domaine: Dérivé de la table Noms de rue et de lieu. Une valeur spécifique est définie pour les côtés gauche et droit
          de l'Élément routier. ``Aucun`` quand aucune valeur ne s'applique.

Nom de route anglais (1, 2, 3, 4)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

La version anglaise du nom d'une route dans un réseau routier donné tel qu'attribué par un organisme national ou
infranational. Il se peut qu'un Élément routier ou Liaison par transbordeur porte plus d'un nom. Ainsi, un Élément
routier ou Liaison par transbordeur peut avoir plusieurs attributs nom de route.

:Domaine: Un nom de route anglais complet tel que ``Trans-Canada Highway`` ou ``Aucun`` quand aucune valeur ne
          s'applique.

Nom de route français (1, 2, 3, 4)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

La version française du nom d'une route dans un réseau routier donné tel qu'attribué par un organisme national ou
infranational. Il se peut qu'un Élément routier ou Liaison par transbordeur porte plus d'un nom. Ainsi, un Élément
routier ou Liaison par transbordeur peut avoir plusieurs attributs nom de route.

:Domaine: Un nom de route français complet tel que ``Autoroute transcanadienne`` ou ``Aucun`` quand aucune valeur ne
          s'applique.

Nom de rue officiel concaténé (gauche, droite)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Une concaténation des attributs Préfixe direction, Préfixe type rue, Article nom rue, Corps nom rue, Suffixe type rue,
Suffixe direction et Muni quadrant du nom de rue officiel.

:Domaine: Dérivé de la table Noms de rue et de lieu. Une valeur spécifique est définie pour les côtés gauche et droit
          de l'Élément routier. ``Aucun`` quand aucune valeur ne s'applique.

Nom de structure anglais
^^^^^^^^^^^^^^^^^^^^^^^^

La version anglaise du nom d'un ouvrage routier tel qu'attribué par un organisme national ou infranational.

:Domaine: Un nom de structure complet ou ``Aucun`` quand aucune valeur ne s'applique.

Nom de structure français
^^^^^^^^^^^^^^^^^^^^^^^^^

La version française du nom d'un ouvrage routier tel qu'attribué par un organisme national ou infranational.

:Domaine: Un nom de structure complet ou ``Aucun`` quand aucune valeur ne s'applique.

Numéro dernière maison (gauche, droite)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Adresse du dernier bâtiment situé le long d'un côté particulier (gauche ou droit) d'un Élément routier. Une valeur
spécifique est définie pour les côtés gauche et droit de l'Élément routier.

:Domaine: [-1..n] La valeur ``0`` indique qu'aucune valeur ne s'applique.

Numéro de route (1, 2, 3, 4, 5)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Numéro d'identifiant d'une route dans un réseau routier tel qu'attribué par un organisme national ou infranational. Il
se peut qu'un Élément routier ou Liaison par transbordeur porte plus d'un numéro. Ainsi, un Élément routier ou Liaison
par transbordeur peut avoir plusieurs attributs numéro de route.

:Domaine: Un numéro de route y compris les caractères non entiers qui y sont parfois associés ou ``Aucun`` quand aucune
          valeur ne s'applique.

          | Exemples : 1, 1A, 230-A, 430-28.

Numéro de sortie
^^^^^^^^^^^^^^^^

Le numéro d'identifiant d'une sortie sur une voie de circulation à accès contrôlé qui a été attribué par une autorité
administrative.

:Domaine: Un numéro d'identifiant y compris les caractères non entiers tels que ``A`` qui y sont parfois associés ou
          ``Aucun`` quand aucune valeur ne s'applique.

          | Exemples : 11, 11A, 11-A, 80-EST, 80-E, 80E.

Numéro première maison (gauche, droite)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Adresse du premier bâtiment situé le long d'un côté particulier (gauche ou droit) d'un Élément routier. Une valeur
spécifique est définie pour les côtés gauche et droit de l'Élément routier.

:Domaine: [-1..n] La valeur ``0`` indique qu'aucune valeur ne s'applique.

Période de fermeture
^^^^^^^^^^^^^^^^^^^^

Période au cours de laquelle la route ou la liaison par transbordeur n'est pas accessible au public.

:Domaine: Identique à :ref:`Closing Period Domain fr`.

Sens de circulation
^^^^^^^^^^^^^^^^^^^

Le ou les sens de circulation permis sur la route.

.. csv-table::
   :header: "Code", "Étiquette", "Définition"
   :widths: auto
   :align: left

   1, "Bi-directionel", "La circulation est permise dans les deux directions."
   2, "Même direction", "La circulation à sens unique est dans la même direction que le sens de numérisation du Segment
   routier."
   3, "Direction contraire", "La circulation à sens unique est en direction opposée au sens de numérisation du Segment
   routier."

Type de chaussée non revêtue
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Le type de chaussée d'un Élément routier non revêtue.

.. csv-table::
   :header: "Code", "Étiquette", "Définition"
   :widths: auto
   :align: left

   0, "Aucun", "Aucune valeur ne s'applique."
   1, "Gravier", "Chemin de terre dont la surface a été améliorée par nivellement avec du gravier."
   2, "Terre", "Des routes dont la surface est formée par l'enlèvement de la végétation et/ou par le va-et-vient des
   véhicules sur cette route, ce qui nuit à la croissance de toute végétation."

Type de chaussée revêtue
^^^^^^^^^^^^^^^^^^^^^^^^

Le type de chaussée d'un Élément routier revêtue.

.. csv-table::
   :header: "Code", "Étiquette", "Définition"
   :widths: auto
   :align: left

   0, "Aucun", "Aucune valeur ne s'applique."
   1, "Rigide", "Route revêtue ayant une surface rigide, tel le béton."
   2, "Souple", "Route revêtue ayant une surface souple, tel l'asphalte."
   3, "Pavés", "Route revêtue ayant une surface constituée de blocs, tels que les pavés en cailloutis."

Type de structure
^^^^^^^^^^^^^^^^^

La classification de la structure.

.. csv-table::
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

Métadonnées d'objet
^^^^^^^^^^^^^^^^^^^

Référer aux attributs décrits dans la :ref:`Object Metadata fr`.
