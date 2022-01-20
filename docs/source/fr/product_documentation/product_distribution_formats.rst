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

Les formats de fichiers de sortie disponibles pour le produit sont : GML (*Geography Markup Language*), KML (*Keyhole
Markup Language*), SHP (*ESRI*\ |trade| *Shapefile*) et GPKG (*OGC Geopackage*).

.. admonition:: Notez

    Les fichiers de données dans le format KML contiennent uniquement l'entité Segment routier et un sous-ensemble de
    ses attributs.

Identification du produit
=========================

:Nom: Réseau routier national
:Version: 2.1
:Date: 2012-03-31
:Normes: :doc:`data_product_specifications`
:Catalogue d'entités: :doc:`feature_catalogue`

Identification des formats de distribution
==========================================

GML – Geography Markup Language
-------------------------------

:Nom: GML – Geography Markup Language
:Version: 2.1.2
:Date: 2002-09-17
:Spécifications: `Geography Markup Language – GML – 2.1.2, OpenGIS Implementation Specifications, OGC Document Number
                 02-069 <http://portal.opengeospatial.org/files/?artifact_id=11339>`_

KML – Keyhole Markup Language
-----------------------------

:Nom: KML – Keyhole Markup Language
:Version: 2.2
:Date: 2008-04-14
:Spécifications: `Open Geospatial Consortium Inc., OGC KML, Version 2.2.0, 2008-04-14, Reference number of this OGC
                 project document: OGC 07-147r2 <http://portal.opengeospatial.org/files/?artifact_id=27810>`_

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

Nomenclature des fichiers GML
-----------------------------

Les entités du produit distribuées dans le format GML sont regroupées par jeu de données à l'intérieur de différents
fichiers. Un fichier contenant les entités géométriques et leurs attributs de base (GEOM), un fichier regroupant les
tables d'attributs d'adressage (ADDR), et jusqu'à quatre fichiers de gestion des modifications pour chaque type de
contenu du jeu de données (GEOM et ADDR). Le nom des fichiers GML prend la forme suivante : ::

    RRN_<IDENTIFIANT>_<édition>_<version>_<CONTENU>[_<MODIFICATION>].gml

.. csv-table::
   :header: "Propriété", "Description"
   :widths: auto
   :align: left

   "RRN", "Titre abrégé du produit."
   "<IDENTIFIANT>", "Code de province ou de territoire anglais correspondant à la localisation du jeu de données. Les
   codes possibles sont : AB, BC, MB, NB, NL, NS, NT, NU, ON, PE, QC, SK, YT."
   "<édition>", "Édition du jeu de données."
   "<version>", "Version du jeu de données."
   "<CONTENU>", "Indicateur du contenu du jeu de données. Les valeurs possibles sont : GEOM (entités géométriques et
   attributs de base), ADDR (tables d'attributs d'adressage)."
   "[<MODIFICATION>]", "[] = Optionnel. Type de modification apportée aux entités et attributs du jeu de données par
   rapport à l'édition précédente. Les valeurs possibles sont identifiées à :ref:`Change Management Files`."
   ".gml", "Extension du nom de fichier."

**Exemples :**

.. csv-table::
   :header: "Nom de fichier", "Description"
   :widths: auto
   :align: left

   "RRN_AB_4_0_GEOM.gml", "Entités géométriques et attributs de base du jeu de données de l'Alberta, édition 4, version
   0."
   "RRN_AB_4_0_ADDR.gml", "Tables d'attributs d'adressage du jeu de données de l'Alberta, édition 4, version 0."
   "RRN_AB_4_0_GEOM_AJOUT.gml", "Entités géométriques et/ou attributs de base ajoutés au jeu de données de l'Alberta,
   édition 4, version 0."
   "RRN_AB_4_0_ADDR_AJOUT.gml", "Tables des attributs d'adressage ajoutés au jeu de données de l'Alberta, édition 4,
   version 0."

Un schéma XML (fichier XSD) est également livré pour chaque fichier GML. Ce fichier définit de façon structurée le type
de contenu, la syntaxe et la sémantique des documents GML. Le nom de ce fichier est
``RRN_<IDENTIFIANT>_<édition>_<version>_<CONTENU>[_<MODIFICATION>].xsd`` et est cité en référence dans le fichier GML.

Nomenclature du fichier KML
---------------------------

Uniquement l'entité *Segment routier* (et un sous-ensemble d'attributs) du produit est distribuée dans le format KML.
Le nom du fichier KML prend la forme suivante : ::

    nrn_rrn_<identifiant>_kml_fr.kmz

.. csv-table::
   :header: "Propriété", "Description"
   :widths: auto
   :align: left

   "nrn_rrn", "Titre abrégé anglais et français du produit."
   "<identifiant>", "Code de province ou de territoire anglais correspondant à la localisation du jeu de données. Les
   codes possibles sont : ab, bc, mb, nb, nl, ns, nt, nu, on, pe, qc, sk, yt."
   "kml", "Format de distribution du jeu de données."
   "fr", "Code ISO de la langue de distribution du jeu de données."
   ".kmz", "Extension du nom de fichier."

**Exemple :**

.. csv-table::
   :header: "Nom de fichier", "Description"
   :widths: auto
   :align: left

   "nrn_rrn_ab_kml_fr.kmz", "*Segment routier* du jeu de données de l'Alberta, édition 4, version 0."

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
   :header: "Catalogue d'entités Nom d'entité", "GML/KML\ :sup:`*`\  Nom d'entité", "GPKG/SHP Nom du fichier", "Type"
   :widths: auto
   :align: left

   "Intervalle d'adresse", "IntervalleAdresse", "INTERVADR", "Table\ :sup:`**`\ "
   "Jonction", "Jonction", "JONCTION", "Point"
   "Lien nom non officiel", "LienNomNonOfficiel", "LIENNOFF", "Table\ :sup:`**`\ "
   "Noms de rue et de lieu", "NomRueLieu", "NOMRUELIEU", "Table\ :sup:`**`\ "
   "Passage obstrué", "PassageObstrue", "PASSAGEOBS", "Point"
   "Poste de péage", "PostePeage", "POSTEPEAGE", "Point"
   "Segment de liaison par transbordeur", "SegmentLiaisonTransbordeur", "SLIAISONTR", "Ligne"
   "Segment routier", "SegmentRoutier\ :sup:`*`\ ", "SEGMROUT", "Ligne"

| :sup:`*` Contenu KML (version simplifiée du jeu de données).
| :sup:`*` Fichier d'attributs (.dbf) dans le format SHP et entités sans géométrie dans le format GML.

.. _Change Management Files:

Fichiers de gestion des modifications
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

La gestion des modifications consiste principalement à identifier l'ajout, la confirmation, l'élimination ou la
modification des objets (géométrie et/ou attribut) entre deux éditions successives d'un jeu de données. Un fichier de
données est généré pour chaque type d'effet. L'extension du nom de fichier dépend directement du format de distribution.

.. csv-table::
   :header: "Gestion des modifications Nom de l'effet", "GML/SHP Nom du fichier"
   :widths: auto
   :align: left

   "Ajout", "<Nom du fichier GML/SHP>_AJOUT"
   "Confirmation", "<Nom du fichier GML/SHP>_CONFIRME"
   "Modification", "<Nom du fichier GML/SHP>_MODIFIE"
   "Élimination", "<Nom du fichier GML/SHP>_ELIMINE"

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
   :header: "Catalogue d'entités Nom d'attribut", "GML Nom d'attribut", "GPKG/SHP Nom d'attribut", "Type de données"
   :widths: auto
   :align: left

   "Couverture", "couvertureMetadonnees", "COUVERMETA", "C(8)"
   "Date création", "dateCreation", "DATECRE", "N(8,0)"
   "Date révision", "dateRevision", "DATEREV", "N(8,0)"
   "Fournisseur", "fournisseur", "FOURNISSR", "C(24)"
   "Nom jeu de données", "nomJeuDonnees", "NOMJEUDONN", "C(25)"
   "Précision planimétrique", "precisionPlanimetrique", "PRECISION", "N(4,0)"
   "Technique acquisition", "techniqueAcquisition", "TECHACQ", "C(28)"
   "Version normes", "versionNormes", "VERSNORMES", "N(4,0)"

Attributs spécifiques aux entités
---------------------------------

Intervalle d'adresse
^^^^^^^^^^^^^^^^^^^^

.. csv-table::
   :header: "Catalogue d'entités Nom d'attribut", "GML Nom d'attribut", "GPKG/SHP Nom d'attribut", "Type de données"
   :widths: auto
   :align: left

   "IDN", "idn", "IDN", "C(32)"
   "IDN nom de rue non officiel à gauche", "idnNomRueNonOfficiel_Gauche", "IDNOMNOF_G", "C(32)"
   "IDN nom de rue non officiel à droite", "idnNomRueNonOfficiel_Droite", "IDNOMNOF_D", "C(32)"
   "IDN nom de rue officiel à gauche", "idnNomRueOfficiel_Gauche", "IDNOMOFF_G", "C(32)"
   "IDN nom de rue officiel à droite", "idnNomRueOfficiel_Droite", "IDNOMOFF_D", "C(32)"
   "Indicateur sens numérisation à gauche", "sensNumerisation_Gauche", "SENSNUM_G", "C(18)"
   "Indicateur sens numérisation à droite", "sensNumerisation_Droite", "SENSNUM_D", "C(18)"
   "Indicateur système référence à gauche", "indicSystemeReference_Gauche", "SYSREF_G", "C(18)"
   "Indicateur système référence à droite", "indicSystemeReference_Droite", "SYSREF_D", "C(18)"
   "Numéro dernière maison à gauche", "numDerniereMaison_Gauche", "NUMD_G", "N(9,0)"
   "Numéro dernière maison à droite", "numDerniereMaison_Droite", "NUMD_D", "N(9,0)"
   "Numéro première maison à gauche", "numPremiereMaison_Gauche", "NUMP_G", "N(9,0)"
   "Numéro première maison à droite", "numPremiereMaison_Droite", "NUMP_D", "N(9,0)"
   "Structure numéro maison à gauche", "structureNumMaison_Gauche", "STRUNUM_G", "C(19)"
   "Structure numéro maison à droite", "structureNumMaison_Droite", "STRUNUM_D", "C(19)"
   "Suffixe numéro dernière maison à gauche", "suffixNumDerniereMaison_Gauche", "SUFNUMD_G", "C(10)"
   "Suffixe numéro dernière maison à droite", "suffixNumDerniereMaison_Droite", "SUFNUMD_D", "C(10)"
   "Suffixe numéro première maison à gauche", "suffixNumPremiereMaison_Gauche", "SUFNUMP_G", "C(10)"
   "Suffixe numéro première maison à droite", "suffixNumPremiereMaison_Droite", "SUFNUMP_D", "C(10)"
   "Type numérotation dernière maison à gauche", "typeNumDerniereMaison_Gauche", "TYPENUMD_G", "C(21)"
   "Type numérotation dernière maison à droite", "typeNumDerniereMaison_Droite", "TYPENUMD_D", "C(21)"
   "Type numérotation première maison à gauche", "typeNumPremiereMaison_Gauche", "TYPENUMP_G", "C(21)"
   "Type numérotation première maison à droite", "typeNumPremiereMaison_Droite", "TYPENUMP_D", "C(21)"

Jonction
^^^^^^^^

.. csv-table::
   :header: "Catalogue d'entités Nom d'attribut", "GML Nom d'attribut", "GPKG/SHP Nom d'attribut", "Type de données"
   :widths: auto
   :align: left

   "IDN", "idn", "IDN", "C(32)"
   "Numéro de sortie", "numeroSortie", "NUMSORTIE", "C(10)"
   "Type jonction", "typeJonction", "TYPEJONC", "C(14)"

Lien nom non officiel
^^^^^^^^^^^^^^^^^^^^^

.. csv-table::
   :header: "Catalogue d'entités Nom d'attribut", "GML Nom d'attribut", "GPKG/SHP Nom d'attribut", "Type de données"
   :widths: auto
   :align: left

   "Date création", "dateCreation", "DATECRE", "N(8,0)"
   "Date révision", "dateRevision", "DATEREV", "N(8,0)"
   "IDN", "idn", "IDN", "C(32)"
   "IDN nom de rue", "idnNomRue", "IDNOMRUE", "C(32)"
   "Nom jeu de données", "nomJeuDonnees", "NOMJEUDONN", "C(25)"
   "Version normes", "versionNormes", "VERSNORMES", "N(4,0)"

Noms de rue et de lieu
^^^^^^^^^^^^^^^^^^^^^^

.. csv-table::
   :header: "Catalogue d'entités Nom d'attribut", "GML Nom d'attribut", "GPKG/SHP Nom d'attribut", "Type de données"
   :widths: auto
   :align: left

   "Article nom rue", "articleNomRue", "ARTNOMRUE", "C(7)"
   "Corps nom rue", "corpsNomRue", "CORPSNOM", "C(50)"
   "IDN", "idn", "IDN", "C(32)"
   "Muni quadrant", "muniQuadrant", "MUNIQUAD", "C(10)"
   "Nom de lieu", "nomLieu", "NOMLIEU", "C(100)"
   "Préfixe direction", "prefixeDirection", "PREDIR", "C(10)"
   "Préfixe type rue", "prefixeTypeRue", "PRETYPRUE", "C(18)"
   "Province", "province", "PROVINCE", "C(25)"
   "Suffixe direction", "suffixeDirection", "SUFDIR", "C(10)"
   "Suffixe type rue", "suffixeTypeRue", "SUFTYPRUE", "C(18)"
   "Type de lieu", "typeLieu", "TYPELIEU", "C(68)"

Passage obstrué
^^^^^^^^^^^^^^^

.. csv-table::
   :header: "Catalogue d'entités Nom d'attribut", "GML Nom d'attribut", "GPKG/SHP Nom d'attribut", "Type de données"
   :widths: auto
   :align: left

   "IDN", "idn", "IDN", "C(32)"
   "IDN élément routier", "idnElementRoutier", "IDNELEMRTE", "C(32)"
   "Type passage obstrué", "typePassageObstrue", "TYPEOBSTRU", "C(17)"

Poste de péage
^^^^^^^^^^^^^^

.. csv-table::
   :header: "Catalogue d'entités Nom d'attribut", "GML Nom d'attribut", "GPKG/SHP Nom d'attribut", "Type de données"
   :widths: auto
   :align: left

   "IDN", "idn", "IDN", "C(32)"
   "IDN élément routier", "idnElementRoutier", "IDNELEMRTE", "C(32)"
   "Type poste péage", "typePostePeage", "TYPEPTEPEA", "C(22)"

Segment de liaison par transbordeur
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table::
   :header: "Catalogue d'entités Nom d'attribut", "GML Nom d'attribut", "GPKG/SHP Nom d'attribut", "Type de données"
   :widths: auto
   :align: left

   "Classification routière fonctionnelle", "classRoutiereFonctionnelle", "CLASSROUTE", "C(41)"
   "ID segment liaison par transbordeur", "idSegmentLiaisonTransbordeur", "IDSEGMLTR", "N(9,0)"
   "IDN", "idn", "IDN", "C(32)"
   "Nom de route anglais 1", "nomRouteAnglais1", "NOMRTE1AN", "C(100)"
   "Nom de route anglais 2", "nomRouteAnglais2", "NOMRTE2AN", "C(100)"
   "Nom de route anglais 3", "nomRouteAnglais3", "NOMRTE3AN", "C(100)"
   "Nom de route anglais 4", "nomRouteAnglais4", "NOMRTE4AN", "C(100)"
   "Nom de route français 1", "nomRouteFrançais1", "NOMRTE1FR", "C(100)"
   "Nom de route français 2", "nomRouteFrançais2", "NOMRTE2FR", "C(100)"
   "Nom de route français 3", "nomRouteFrançais3", "NOMRTE3FR", "C(100)"
   "Nom de route français 4", "nomRouteFrançais4", "NOMRTE4FR", "C(100)"
   "Numéro de route 1", "numeroRoute1", "NUMROUTE1", "C(10)"
   "Numéro de route 2", "numeroRoute2", "NUMROUTE2", "C(10)"
   "Numéro de route 3", "numeroRoute3", "NUMROUTE3", "C(10)"
   "Numéro de route 4", "numeroRoute4", "NUMROUTE4", "C(10)"
   "Numéro de route 5", "numeroRoute5", "NUMROUTE5", "C(10)"
   "Période de fermeture", "periodeFermeture", "FERMETURE", "C(7)"

Segment routier
^^^^^^^^^^^^^^^

.. csv-table::
   :header: "Catalogue d'entités Nom d'attribut", "GML/KML\ :sup:`*`\  Nom d'attribut", "GPKG/SHP Nom d'attribut",
            "Type de données"
   :widths: auto
   :align: left

   "Autorité route", "autoriteRoute", "AUTORITE", "C(100)"
   "Classification routière fonctionnelle", "classRoutiereFonctionnelle", "CLASSROUTE", "C(41)"
   "État revêtement", "etatRevetement", "ETATREV", "C(11)"
   "ID segment routier", "idSegmentRoutier", "IDSEGMRTE", "N(9,0)"
   "IDN", "idn\ :sup:`**`\ ", "IDN", "C(32)"
   "IDN intervalle d'adresse", "idnIntervalleAdresse", "IDINTERVAD", "C(32)"
   "ID structure", "idStructure", "IDSTRUCT", "C(32)"
   "Indicateur sens numérisation adresse à gauche", "sensNumerisationAdresse_Gauche\ :sup:`**`\ ", "ADRSENS_G", "C(18)"
   "Indicateur sens numérisation adresse à droite", "sensNumerisationAdresse_Droite\ :sup:`**`\ ", "ADRSENS_D", "C(18)"
   "Limites de vitesse", "limitesVitesse", "VITESSE", "N(4,0)"
   "Nom de lieu officiel à gauche", "nomLieuOfficiel_Gauche\ :sup:`**`\ ", "NOMLIEU_G", "C(100)"
   "Nom de lieu officiel à droite", "nomLieuOfficiel_Droite\ :sup:`**`\ ", "NOMLIEU_D", "C(100)"
   "Nom de route anglais 1", "nomRouteAnglais1", "NOMRTE1AN", "C(100)"
   "Nom de route anglais 2", "nomRouteAnglais2", "NOMRTE2AN", "C(100)"
   "Nom de route anglais 3", "nomRouteAnglais3", "NOMRTE3AN", "C(100)"
   "Nom de route anglais 4", "nomRouteAnglais4", "NOMRTE4AN", "C(100)"
   "Nom de route français 1", "nomRouteFrançais1", "NOMRTE1FR", "C(100)"
   "Nom de route français 2", "nomRouteFrançais2", "NOMRTE2FR", "C(100)"
   "Nom de route français 3", "nomRouteFrançais3", "NOMRTE3FR", "C(100)"
   "Nom de route français 4", "nomRouteFrançais4", "NOMRTE4FR", "C(100)"
   "Nom de rue officiel concaténé à gauche", "nomRueOfficielConcat_Gauche\ :sup:`**`\ ", "NOMRUE_C_G", "C(100)"
   "Nom de rue officiel concaténé à droite", "nomRueOfficielConcat_Droite\ :sup:`**`\ ", "NOMRUE_C_D", "C(100)"
   "Nom de structure anglais", "nomStructureAnglais", "NOMSTRUCAN", "C(100)"
   "Nom de structure français", "nomStructureFrançais", "NOMSTRUCFR", "C(100)"
   "Nombre de voies", "nombreVoies", "NBRVOIES", "N(4,0)"
   "Numéro de route 1", "numeroRoute1\ :sup:`**`\ ", "NUMROUTE1", "C(10)"
   "Numéro de route 2", "numeroRoute2", "NUMROUTE2", "C(10)"
   "Numéro de route 3", "numeroRoute3", "NUMROUTE3", "C(10)"
   "Numéro de route 4", "numeroRoute4", "NUMROUTE4", "C(10)"
   "Numéro de route 5", "numeroRoute5", "NUMROUTE5", "C(10)"
   "Numéro de sortie", "numeroSortie", "NUMSORTIE", "C(10)"
   "Numéro dernière maison à gauche", "numDerniereMaison_Gauche", "NUMD_G", "N(9,0)"
   "Numéro dernière maison à droite", "numDerniereMaison_Droite", "NUMD_D", "N(9,0)"
   "Numéro première maison à gauche", "numPremiereMaison_Gauche", "NUMP_G", "N(9,0)"
   "Numéro première maison à droite", "numPremiereMaison_Droite", "NUMP_D", "N(9,0)"
   "Période de fermeture", "periodeFermeture", "FERMETURE", "C(7)"
   "Sens de circulation", "sensCirculation", "SENSCIRCUL", "C(19)"
   "Type de chaussée non revêtue", "typeChausseeNonRevetue", "TYPENONREV", "C(7)"
   "Type de chaussée revêtue", "typeChausseeRevetue", "TYPEREV", "C(8)"
   "Type de structure", "typeStructure", "TYPESTRUCT", "C(15)"

:sup:`*` Contenu KML (version simplifiée du jeu de données)
