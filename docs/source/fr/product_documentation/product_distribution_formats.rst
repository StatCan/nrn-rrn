**********************************
Formats de distribution du produit
**********************************

.. include:: <isonum.txt>
.. include:: <isopub.txt>

.. contents:: Matières :
   :depth: 3

Aperçu
======

Les entités du Réseau routier national (RRN) vue segmentée sont les suivantes : *Intervalle d'adresse*, *Jonction*,
*Lien nom non officiel*, *Noms de rue et de lieu*, *Passage obstrué*, *Poste de péage*, *Segment de liaison par
transbordeur* et *Segment routier*.

Les formats de fichiers de sortie disponibles pour le produit sont : SHP (*ESRI*\ |trade| *Shapefile*) et GPKG (*OGC
Geopackage*).

Identification du produit
=========================

:Nom: Réseau routier national
:Version: 2.1
:Date: 2012-03-31
:Normes: :doc:`data_product_specifications`
:Catalogue d'entités: :doc:`feature_catalogue`

Identification des formats de distribution
==========================================

SHP – ESRI\ |trade| Shapefile
-----------------------------

:Nom: Shapefile
:Version: 01
:Date: Juillet 1998
:Spécifications: `ESRI Shapefile Technical Description, an ESRI White Paper, July 1998
                 <http://www.esri.com/library/whitepapers/pdfs/shapefile.pdf>`_

GPKG – OGC Geopackage
---------------------

:Nom: GeoPackage
:Version: 1.0.1
:Date: Janvier 2019
:Spécifications: https://www.geopackage.org/spec101/index.html

Identification des fichiers de distribution
===========================================

Nomenclature des fichiers SHP
-----------------------------

Les entités du produit dans le format SHP sont divisées selon leur représentation géométrique. Le nom des fichiers SHP
suit la structure suivante : ::

    RRN_<IDENTIFIANT>_<édition>_<version>_<ENTITÉ>[_<MODIFICATION>].shp

.. csv-table::
   :header: "Propriété", "Description"
   :widths: auto
   :align: left

   "RRN", "Titre abrégé du produit."
   "<IDENTIFIANT>", "Code de province ou de territoire anglais correspondant à la localisation du jeu de données. Les
   codes possibles sont : AB, BC, MB, NB, NL, NS, NT, NU, ON, PE, QC, SK, YT."
   "<édition>", "Édition du jeu de données."
   "<version>", "Version du jeu de données."
   "<ENTITÉ>", "Nom abrégé de l'entité tel que défini à :ref:`Datasets`."
   "[<MODIFICATION>]", "[] = Optionnel. Type de modification apportée aux entités et attributs du jeu de données par
   rapport à l'édition précédente. Les valeurs possibles sont identifiées à :ref:`Change Management Files`."
   ".shp", "Extension du nom de fichier principal de géométrie."

Dans le format SHP, il y a également cinq autres types de fichiers associés au fichier de géométrie de l'entité :

* un fichier d'attributs (.dbf pour dBASE® file);
* un fichier projection (.prj) contenant l'information sur le système de référence utilisé et les paramètres de la
  projection cartographique;
* un fichier d'index (.shx) contenant la position relative (offset) de chacun des enregistrements (records) du fichier
  principal de géométrie;
* deux fichiers d'index spatial pour les données géométriques (.sbn, .sbx).

**Exemples :**

.. csv-table::
   :header: "Nom de fichier", "Description"
   :widths: auto
   :align: left

   "RRN_AB_4_0_SEGMROUT.shp", "Entité *Segment routier* du jeu de données de l'Alberta, édition 4, version 0."
   "RRN_AB_4_0_SEGMROUT_AJOUT.shp", "Entités géométriques et/ou attributs de base du *Segment routier* ajoutés au jeu
   de données de l'Alberta, édition 4, version 0."

Nomenclature des fichiers GPKG
------------------------------

Les entités du produit dans le format GPKG sont divisées selon leur représentation géométrique. Le nom des fichiers
GPKG suit la structure suivante : ::

    RRN_<IDENTIFIANT>_<édition>_<version>_fr.gpkg

.. csv-table::
   :header: "Propriété", "Description"
   :widths: auto
   :align: left

   "RRN", "Titre abrégé du produit."
   "<IDENTIFIANT>", "Code de province ou de territoire anglais correspondant à la localisation du jeu de données. Les
   codes possibles sont : AB, BC, MB, NB, NL, NS, NT, NU, ON, PE, QC, SK, YT."
   "<édition>", "Édition du jeu de données."
   "<version>", "Version du jeu de données."
   "fr", "Code ISO de la langue de distribution du jeu de données."
   ".gpkg", "Extension du nom de fichier."

**Examples:**

.. csv-table::
   :header: "Nom de fichier", "Description"
   :widths: auto
   :align: left

   "RRN_AB_4_0_fr.gpkg", "Toutes les entités du jeu de données de l'Alberta, édition 4, version 0."

Fichier de métadonnées
----------------------

Quatre fichiers de métadonnées sont distribués avec chaque jeu de données du produit RRN. Deux fichiers sont livrés
dans le format FGDC/XML (en français et en anglais) et deux autres selon le format FGDC/HTML. La nomenclature du
fichier de métadonnées est : ::

    nrn_rrn_<identifiant>_<édition>_<version>_fgdc_fr.<format>

.. csv-table::
   :header: "Propriété", "Description"
   :widths: auto
   :align: left

   "nrn_rrn", "Titre abrégé anglais et français du produit."
   "<identifiant>", "Code de province ou de territoire anglais correspondant à la localisation du jeu de données. Les
   codes possibles sont : AB, BC, MB, NB, NL, NS, NT, NU, ON, PE, QC, SK, YT."
   "<édition>", "Édition du jeu de données."
   "<version>", "Version du jeu de données."
   "fgdc", "Format du fichier de métadonnées selon la norme CSDGM du Federal Geographic Data Committee."
   "fr", "Code ISO de la langue de distribution du jeu de données."
   "<format>", "Extension du nom de fichier (xml ou html)."

**Exemples :**

.. csv-table::
   :header: "Nom de fichier", "Description"
   :widths: auto
   :align: left

   "nrn_rrn_ab_4_0_fgdc_en.xml", "Fichier de métadonnées du jeu de données de l'Alberta, édition 4, version 0 selon le
   format FGDC/XML."
   "nrn_rrn_ab_4_0_fgdc_en.html", "Fichier de métadonnées du jeu de données de l'Alberta, édition 4, version 0 selon le
   format FGDC/HTML."

Liste des noms de fichiers de distribution
------------------------------------------

Le produit RRN comporte deux types de jeux de données : des fichiers contenant les données actualisées (i.e. qui ont
été mises à jour) et des fichiers contenant les modifications (différences) appliquées à l'édition précédente du jeu de
données.

.. _Datasets:

Jeux de données
^^^^^^^^^^^^^^^

L'extension du nom de fichier dépend directement du format de distribution.

.. csv-table::
   :header: "Catalogue d'entités Nom d'entité", "Nom du fichier", "Type"
   :widths: auto
   :align: left

   "Intervalle d'adresse", "INTERVADR", "Table\ :sup:`*`\ "
   "Jonction", "JONCTION", "Point"
   "Lien nom non officiel", "LIENNOFF", "Table\ :sup:`*`\ "
   "Noms de rue et de lieu", "NOMRUELIEU", "Table\ :sup:`*`\ "
   "Passage obstrué", "PASSAGEOBS", "Point"
   "Poste de péage", "POSTEPEAGE", "Point"
   "Segment de liaison par transbordeur", "SLIAISONTR", "Ligne"
   "Segment routier", "SEGMROUT", "Ligne"

| :sup:`*` Fichier d'attributs (.dbf) dans le format SHP.

.. _Change Management Files:

Fichiers de gestion des modifications
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

La gestion des modifications consiste principalement à identifier l'ajout, la confirmation, l'élimination ou la
modification des objets (géométrie et/ou attribut) entre deux éditions successives d'un jeu de données. Un fichier de
données est généré pour chaque type d'effet. L'extension du nom de fichier dépend directement du format de distribution.

.. csv-table::
   :header: "Gestion des modifications Nom de l'effet", "Nom du fichier SHP"
   :widths: auto
   :align: left

   "Ajout", "<Nom du fichier SHP>_AJOUT"
   "Confirmation", "<Nom du fichier SHP>_CONFIRME"
   "Modification", "<Nom du fichier SHP>_MODIFIE"
   "Élimination", "<Nom du fichier SHP>_ELIMINE"

La méthode utilisée pour le *suivi des modifications géométriques* est indiquée dans un fichier texte nommé :
``LISEZMOI_<IDENTIFIANT>.txt`` qui est joint au jeu de données.

Identification des attributs
============================

Les attributs communs à l'ensemble des entités du produit RRN sont identifiés dans le premier tableau. Les attributs
spécifiques à chaque entité sont présentés dans la sous-section suivante.

Le type de données de tous les formats de distribution est soit : ``C(c)`` pour caractères ou ``N(n,d)`` pour nombre
(``c`` = nombre de caractères, ``n`` = nombre total de chiffres, ``d`` = nombre de chiffres en décimales).

Attributs communs pour toutes les entités (sauf Lien nom non officiel)
----------------------------------------------------------------------

.. csv-table::
   :header: "Catalogue d'entités Nom d'attribut", "Nom d'attribut", "Type de données"
   :widths: auto
   :align: left

   "Couverture", "COUVERMETA", "C(8)"
   "Date création", "DATECRE", "N(8,0)"
   "Date révision", "DATEREV", "N(8,0)"
   "Fournisseur", "FOURNISSR", "C(24)"
   "Nom jeu de données", "NOMJEUDONN", "C(25)"
   "Précision planimétrique", "PRECISION", "N(4,0)"
   "Technique acquisition", "TECHACQ", "C(28)"
   "Version normes", "VERSNORMES", "N(4,0)"

Attributs spécifiques aux entités
---------------------------------

Intervalle d'adresse
^^^^^^^^^^^^^^^^^^^^

.. csv-table::
   :header: "Catalogue d'entités Nom d'attribut", "Nom d'attribut", "Type de données"
   :widths: auto
   :align: left

   "IDN", "IDN", "C(32)"
   "IDN nom de rue non officiel à gauche", "IDNOMNOF_G", "C(32)"
   "IDN nom de rue non officiel à droite", "IDNOMNOF_D", "C(32)"
   "IDN nom de rue officiel à gauche", "IDNOMOFF_G", "C(32)"
   "IDN nom de rue officiel à droite", "IDNOMOFF_D", "C(32)"
   "Indicateur sens numérisation à gauche", "SENSNUM_G", "C(18)"
   "Indicateur sens numérisation à droite", "SENSNUM_D", "C(18)"
   "Indicateur système référence à gauche", "SYSREF_G", "C(18)"
   "Indicateur système référence à droite", "SYSREF_D", "C(18)"
   "Numéro dernière maison à gauche", "NUMD_G", "N(9,0)"
   "Numéro dernière maison à droite", "NUMD_D", "N(9,0)"
   "Numéro première maison à gauche", "NUMP_G", "N(9,0)"
   "Numéro première maison à droite", "NUMP_D", "N(9,0)"
   "Structure numéro maison à gauche", "STRUNUM_G", "C(19)"
   "Structure numéro maison à droite", "STRUNUM_D", "C(19)"
   "Suffixe numéro dernière maison à gauche", "SUFNUMD_G", "C(10)"
   "Suffixe numéro dernière maison à droite", "SUFNUMD_D", "C(10)"
   "Suffixe numéro première maison à gauche", "SUFNUMP_G", "C(10)"
   "Suffixe numéro première maison à droite", "SUFNUMP_D", "C(10)"
   "Type numérotation dernière maison à gauche", "TYPENUMD_G", "C(21)"
   "Type numérotation dernière maison à droite", "TYPENUMD_D", "C(21)"
   "Type numérotation première maison à gauche", "TYPENUMP_G", "C(21)"
   "Type numérotation première maison à droite", "TYPENUMP_D", "C(21)"

Jonction
^^^^^^^^

.. csv-table::
   :header: "Catalogue d'entités Nom d'attribut", "Nom d'attribut", "Type de données"
   :widths: auto
   :align: left

   "IDN", "IDN", "C(32)"
   "Numéro de sortie", "NUMSORTIE", "C(10)"
   "Type jonction", "TYPEJONC", "C(14)"

Lien nom non officiel
^^^^^^^^^^^^^^^^^^^^^

.. csv-table::
   :header: "Catalogue d'entités Nom d'attribut", "Nom d'attribut", "Type de données"
   :widths: auto
   :align: left

   "Date création", "DATECRE", "N(8,0)"
   "Date révision", "DATEREV", "N(8,0)"
   "IDN", "IDN", "C(32)"
   "IDN nom de rue", "IDNOMRUE", "C(32)"
   "Nom jeu de données", "NOMJEUDONN", "C(25)"
   "Version normes", "VERSNORMES", "N(4,0)"

Noms de rue et de lieu
^^^^^^^^^^^^^^^^^^^^^^

.. csv-table::
   :header: "Catalogue d'entités Nom d'attribut", "Nom d'attribut", "Type de données"
   :widths: auto
   :align: left

   "Article nom rue", "ARTNOMRUE", "C(7)"
   "Corps nom rue", "CORPSNOM", "C(50)"
   "IDN", "IDN", "C(32)"
   "Muni quadrant", "MUNIQUAD", "C(10)"
   "Nom de lieu", "NOMLIEU", "C(100)"
   "Préfixe direction", "PREDIR", "C(10)"
   "Préfixe type rue", "PRETYPRUE", "C(18)"
   "Province", "PROVINCE", "C(25)"
   "Suffixe direction", "SUFDIR", "C(10)"
   "Suffixe type rue", "SUFTYPRUE", "C(18)"
   "Type de lieu", "TYPELIEU", "C(68)"

Passage obstrué
^^^^^^^^^^^^^^^

.. csv-table::
   :header: "Catalogue d'entités Nom d'attribut", "Nom d'attribut", "Type de données"
   :widths: auto
   :align: left

   "IDN", "IDN", "C(32)"
   "IDN élément routier", "IDNELEMRTE", "C(32)"
   "Type passage obstrué", "TYPEOBSTRU", "C(17)"

Poste de péage
^^^^^^^^^^^^^^

.. csv-table::
   :header: "Catalogue d'entités Nom d'attribut", "Nom d'attribut", "Type de données"
   :widths: auto
   :align: left

   "IDN", "IDN", "C(32)"
   "IDN élément routier", "IDNELEMRTE", "C(32)"
   "Type poste péage", "TYPEPTEPEA", "C(22)"

Segment de liaison par transbordeur
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table::
   :header: "Catalogue d'entités Nom d'attribut", "Nom d'attribut", "Type de données"
   :widths: auto
   :align: left

   "Classification routière fonctionnelle", "CLASSROUTE", "C(41)"
   "ID segment liaison par transbordeur", "IDSEGMLTR", "N(9,0)"
   "IDN", "IDN", "C(32)"
   "Nom de route anglais 1", "NOMRTE1AN", "C(100)"
   "Nom de route anglais 2", "NOMRTE2AN", "C(100)"
   "Nom de route anglais 3", "NOMRTE3AN", "C(100)"
   "Nom de route anglais 4", "NOMRTE4AN", "C(100)"
   "Nom de route français 1", "NOMRTE1FR", "C(100)"
   "Nom de route français 2", "NOMRTE2FR", "C(100)"
   "Nom de route français 3", "NOMRTE3FR", "C(100)"
   "Nom de route français 4", "NOMRTE4FR", "C(100)"
   "Numéro de route 1", "NUMROUTE1", "C(10)"
   "Numéro de route 2", "NUMROUTE2", "C(10)"
   "Numéro de route 3", "NUMROUTE3", "C(10)"
   "Numéro de route 4", "NUMROUTE4", "C(10)"
   "Numéro de route 5", "NUMROUTE5", "C(10)"
   "Période de fermeture", "FERMETURE", "C(7)"

Segment routier
^^^^^^^^^^^^^^^

.. csv-table::
   :header: "Catalogue d'entités Nom d'attribut", "Nom d'attribut", "Type de données"
   :widths: auto
   :align: left

   "Autorité route", "AUTORITE", "C(100)"
   "Classification routière fonctionnelle", "CLASSROUTE", "C(41)"
   "État revêtement", "ETATREV", "C(11)"
   "ID segment routier", "IDSEGMRTE", "N(9,0)"
   "IDN", "IDN", "C(32)"
   "IDN intervalle d'adresse", "IDINTERVAD", "C(32)"
   "ID structure", "IDSTRUCT", "C(32)"
   "Indicateur sens numérisation adresse à gauche", "ADRSENS_G", "C(18)"
   "Indicateur sens numérisation adresse à droite", "ADRSENS_D", "C(18)"
   "Limites de vitesse", "VITESSE", "N(4,0)"
   "Nom de lieu officiel à gauche", "NOMLIEU_G", "C(100)"
   "Nom de lieu officiel à droite", "NOMLIEU_D", "C(100)"
   "Nom de route anglais 1", "NOMRTE1AN", "C(100)"
   "Nom de route anglais 2", "NOMRTE2AN", "C(100)"
   "Nom de route anglais 3", "NOMRTE3AN", "C(100)"
   "Nom de route anglais 4", "NOMRTE4AN", "C(100)"
   "Nom de route français 1", "NOMRTE1FR", "C(100)"
   "Nom de route français 2", "NOMRTE2FR", "C(100)"
   "Nom de route français 3", "NOMRTE3FR", "C(100)"
   "Nom de route français 4", "NOMRTE4FR", "C(100)"
   "Nom de rue officiel concaténé à gauche", "NOMRUE_C_G", "C(100)"
   "Nom de rue officiel concaténé à droite", "NOMRUE_C_D", "C(100)"
   "Nom de structure anglais", "NOMSTRUCAN", "C(100)"
   "Nom de structure français", "NOMSTRUCFR", "C(100)"
   "Nombre de voies", "NBRVOIES", "N(4,0)"
   "Numéro de route 1", "NUMROUTE1", "C(10)"
   "Numéro de route 2", "NUMROUTE2", "C(10)"
   "Numéro de route 3", "NUMROUTE3", "C(10)"
   "Numéro de route 4", "NUMROUTE4", "C(10)"
   "Numéro de route 5", "NUMROUTE5", "C(10)"
   "Numéro de sortie", "NUMSORTIE", "C(10)"
   "Numéro dernière maison à gauche", "NUMD_G", "N(9,0)"
   "Numéro dernière maison à droite", "NUMD_D", "N(9,0)"
   "Numéro première maison à gauche", "NUMP_G", "N(9,0)"
   "Numéro première maison à droite", "NUMP_D", "N(9,0)"
   "Période de fermeture", "FERMETURE", "C(7)"
   "Sens de circulation", "SENSCIRCUL", "C(19)"
   "Type de chaussée non revêtue", "TYPENONREV", "C(7)"
   "Type de chaussée revêtue", "TYPEREV", "C(8)"
   "Type de structure", "TYPESTRUCT", "C(15)"
