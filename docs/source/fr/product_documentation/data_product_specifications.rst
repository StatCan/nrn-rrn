*************************
Spécifications de produit
*************************

.. include:: <isonum.txt>
.. include:: <isopub.txt>

.. admonition:: Notez

    Ces spécifications ont été produites conformément à la *Norme internationale ISO/TC 211 19131 : 2007 Information
    géographique – Spécifications de contenu informationnel*, laquelle réfère notamment à la norme *ISO 19115 : 2003
    Information géographique – Métadonnées*.

.. contents:: Matières :
   :depth: 4

Aperçu
======

Titre
-----

Réseau routier national

Date de référence
-----------------

Date de création des spécifications de produit : 2007-05-31.

Responsable du produit
----------------------

| GéoBase
| Stastistique Canada
| Centre de géomatique statistique
| 170, Promenade Tunney's Pasture,
| Ottawa, Ontario, Canada
| K1A 0T6

| Téléphone : 1-800-263-1136
| Télécopieur : 1-514-283-9350
| Courriel : infostats@statcan.gc.ca
| Site internet : https://statcan.gc.ca
| Site internet : https://www.geobase.ca

Langue
------

Langues dans lesquelles les spécifications de produit sont disponibles conformément à la norme ISO 639-2 :

| en – anglais
| fr – français

Description informelle du produit
---------------------------------

Le produit Réseau routier national (RRN) contient des données géospatiales de qualité (actuelles, précises, cohérentes
et tenues à jour) des phénomènes routiers canadiens. Le produit est distribué sous forme de treize jeux de données
provinciaux ou territoriaux et est composé de deux entités linéaires (Segment routier et Segment de liaison par
transbordeur) et de trois entités ponctuelles (Jonction, Passage obstrué et Poste de péage) auxquelles est associée une
série d'attributs descriptifs dont, entre autres : Numéro première maison, Numéro dernière maison, Corps nom rue, Nom
de lieu, Classification routière fonctionnelle, État revêtement, Nombre de voies, Type de structure, Numéro de route,
Nom de route, Numéro de sortie.

La maintenance des données RRN est réalisée par l'entremise d'ententes de partenariat intergouvernemental (fédéral,
provincial, territorial et municipal) par les organismes gouvernementaux intéressés, identifiés être les plus près de
la source et capables d'offrir des représentations adéquates et actualisées des phénomènes routiers. La fréquence de
maintenance visée est d'au moins une mise à jour par an. Les données produites forment une vue homogène et standardisée
pour l'ensemble du territoire canadien.

Le modèle conceptuel RRN a été élaboré en collaboration avec les fournisseurs de données intéressés et a été adopté par
le Conseil canadien de géomatique (COCG). La norme ISO 14825 — *Systèmes de transport intelligents — Fichiers de
données géographiques — Spécification des données globales* a servi de guide pour l'élaboration du modèle conceptuel et
du catalogue RRN. Le vocabulaire RRN (nom de classes, nom d'attributs et définitions) est en grande partie extrait de
l'ISO 14825.

Portée des spécifications
=========================

Cette section décrit la portée à laquelle fait référence l'information des sections subséquentes qui décrivent le
produit.

Identification de la portée
---------------------------

Globale

.. admonition:: Notez

    "Globale" signifie que la portée réfère à toutes les parties des spécifications de produit.

Niveau
------

Cette portée fait référence au niveau suivant de la norme ISO 19115 et de la norme CAN/CGSB-171.100-2009 :

006 - séries

Nom du niveau
-------------

RRN

Étendue
-------

Cette section décrit l'étendue spatiale et temporelle de la portée.

Description
^^^^^^^^^^^

Masse continentale canadienne

Les données du RRN sont continues entre les jeux de données et constituent un réseau ininterrompu couvrant l'ensemble
de la masse continentale canadienne.

Étendue verticale
^^^^^^^^^^^^^^^^^

Les données RRN sont bidimensionnelles. Il n'y a pas d'élévation (z) associée aux données.

Valeur minimale
"""""""""""""""

Ne s'applique pas

Valeur maximale
"""""""""""""""

Ne s'applique pas

Unité de mesure
"""""""""""""""

Ne s'applique pas

Datum vertical
""""""""""""""

Ne s'applique pas

Étendue horizontale
^^^^^^^^^^^^^^^^^^^

L'étendue géographique est décrite par les coordonnées de boîte englobante suivante :

Longitude limitrophe ouest
""""""""""""""""""""""""""

-141.0

Longitude limitrophe est
""""""""""""""""""""""""

-52.6

Latitude limitrophe sud
"""""""""""""""""""""""

+41.7

Latitude limitrophe nord
""""""""""""""""""""""""

+76.5

Étendue temporelle
^^^^^^^^^^^^^^^^^^

L'étendue temporelle est définie par la période de temps suivante :

Date de début
"""""""""""""

1979-07

Date de fin
"""""""""""

Aujourd'hui

.. admonition:: Notez

    "Aujourd'hui" signifie la date de publication courante d'une instance du RRN. C'est-à-dire, une instance du RRN
    peut inclure un réseau routier qui est actuel à la date de publication.

Identification du produit
=========================

Titre
-----

Réseau routier national

Titre alternatif
----------------

RRN

Résumé
------

Le produit RRN est distribué sous forme de treize jeux de données provinciaux ou territoriaux et est composé de deux
entités linéaires (Segment routier et Segment de liaison par transbordeur) et de trois entités ponctuelles (Jonction,
Passage obstrué et Poste de péage) auxquelles est associée une série d'attributs descriptifs dont, entre autres :
Numéro première maison, Numéro dernière maison, Corps nom rue, Nom de lieu, Classification routière fonctionnelle, État
revêtement, Nombre de voies, Type de structure, Numéro de route, Nom de route, Numéro de sortie.

Le développement de l'édition 2.0 du RRN a été réalisé à l'aide de rencontres individuelles et des ateliers nationaux
avec les producteurs de données intéressés des gouvernements fédéraux, provinciaux, territoriaux et municipaux.

En 2005, le RRN édition 2.0 a été adopté à tour de rôle par les membres du Comité mixte des organismes intéressés à la
géomatique (CMOIG) et les membres du Conseil canadien de géomatique (COCG). Son contenu s'appuie en grande partie sur
la norme ISO 14825 de ISO/TC 204.

But
---

Le RRN vise à fournir une description géométrique et attributive de qualité (actuelle, précise, cohérente), homogène et
normalisée de l'ensemble du réseau routier canadien.

Les données RRN servent de fondation pour plusieurs applications. Cette base géométrique commune est acquise et
maintenue à jour sur une base régulière par les organisations les plus près de la source sélectionnées pour leurs
intérêts spécifiques ou leur facilité à offrir des représentations adéquates et actualisées des phénomènes routiers,
conformément à l'initiative `GéoBase <http://www.geobase.ca>`_. Cette infrastructure commune facilite le processus
d'intégration entre les données RRN et d'autres données complémentaires.

Catégories
----------

Thèmes principaux du produit, tels que définis selon la norme ISO 19115 ou CAN/CGSB-171.100-2009 :

013 – localisation

018 – transport

Type de représentation spatiale
-------------------------------

Type de représentation spatiale du produit, tel que défini dans la norme ISO 19115 :

001 - vectorielle

Résolution spatiale
-------------------

Dénominateur de la résolution spatiale des données : 10 000.

.. admonition:: Notez

    La résolution spatiale nominale est un estimé général du fait que les données sont issues de plusieurs sources
    (GPS, données existantes fédérales, provinciales ou municipales) mais est estimée être de l'ordre de 1/10 000.

Description géographique
------------------------

Autorité
^^^^^^^^

Organisation internationale de normalisation (ISO)

Titre
"""""

Norme des codes de régions géographiques :

ISO 3166-1:1997 Codes pour la représentation des noms de pays et de leurs subdivisions – Partie 1 : Codes pays

Date
""""

Date de référence de la norme ISO 3166-1 : 1997-10-01.

Type de date
""""""""""""

Type de date selon la norme ISO 19115 :

002 - publication

Code
^^^^

Code de la région géographique couverte par le produit selon la liste de codes de la norme ISO 3166-1 :

CA – Canada

Type de code
^^^^^^^^^^^^

Type de code du polygone de délimitation de l'étendue selon la norme ISO 19115 :

1 - inclusion (le polygone de délimitation est inclusif)

Contenu et structure de l'information
=====================================

Description
-----------

Le RRN est un produit numérique distribué sous forme de treize jeux de données provinciaux ou territoriaux. Chaque jeu
de données est composé de deux entités linéaires (Segment routier et Segment de liaison par transbordeur) et de trois
entités ponctuelles (Jonction, Passage obstrué et Poste de péage) auxquelles est associée une série d'attributs
descriptifs dont, entre autres : Numéro première maison, Numéro dernière maison, Corps nom rue, Nom de lieu,
Classification routière fonctionnelle, État revêtement, Nombre de voies, Type de structure, Numéro de route, Nom de
route, Numéro de sortie.

Les informations d'adressage (intervalle d'adresse, nom de rue et nom de lieu) liées aux entités segment routier sont
également distribuées dans trois tables distinctes (intervalle d'adresse, noms de rue et de lieu et lien nom de rue non
officiel).

Modèle de données d'entités
---------------------------

Schéma d'application
^^^^^^^^^^^^^^^^^^^^

L'implantation physique du produit RRN diffère du modèle conceptuel en ce qui a trait à la gestion des métadonnées
d'objet et à l'ajout de certains attributs à l'entité segment routier.

Pour les métadonnées d'objet, le modèle conceptuel prévoit deux séries distinctes d'attributs de métadonnées décrivant
les sources respectives utilisées pour créer et réviser les données. Seules les dates distinctes de création et de
révision ont été implantées. Lorsqu'une date de révision est indiquée et qu'une modification attributive ou géométrique
a été appliquée à l'objet (par rapport à l'édition précédente du jeu de données), la série d'attributs de métadonnées
d'objet décrit alors les sources utilisées pour la révision. Autrement, les métadonnées d'objet décrivent les sources
utilisées pour la création des données.

Le nom de rue, nom de lieu et l'intervalle d'adresse ont été aussi ajoutés en attribut sur la géométrie de l'entité
segment routier.

:doc:`product_distribution_formats` illustre la matérialisation du modèle conceptuel du Catalogue d'entités dans le
modèle physique des données du produit RRN selon les formats de distribution GML, GPKG, KML et SHP.

Catalogue d'entités
^^^^^^^^^^^^^^^^^^^

:doc:`feature_catalogue`

Systèmes de référence
=====================

Système de référence spatial
----------------------------

Les données spatiales sont exprimées en coordonnées géographiques de latitude (φ) et de longitude (λ) en référence au
Système de référence nord-américain de 1983 Système canadien de référence spatiale (NAD83SCRS). La longitude s'exprime
à l'aide d'un nombre négatif pour représenter une position à l'ouest du méridien central (0°). L'unité de mesure des
coordonnées est le degré exprimé sous forme de valeur réelle à sept décimales.

Autorité
^^^^^^^^

Titre
"""""

Registre du système de référence : EPSG Geodetic Parameter Dataset.

Date
""""

Date de référence : 2007-02-08.

Type de date
""""""""""""

Type de date selon la norme ISO 19115 :

002 - publication

Responsable du registre
"""""""""""""""""""""""

`OGP – International Organisation of Oil and Gas Producers <http://www.epsg.org>`_

Code
^^^^

Identifiant du système de référence (CRSID) : 4617.

Espace de codage
^^^^^^^^^^^^^^^^

EPSG – European Petroleum Survey Group

Version
^^^^^^^

6.12

Qualité des données
===================

Complétude
----------

Le produit RRN contient une description géométrique et attributive de qualité (actuelle, précise, cohérente), homogène
et normalisée de l'ensemble du réseau routier canadien.

La représentation des routes contenues dans le RRN correspond à la ligne médiane de toutes les routes à usage non
restreint (largeur de 5 mètres ou plus, carrossables et sans obstacle limitant l'accès). Les réseaux de routes qui ne
sont pas reliées au réseau routier principal, les ruelles, les routes d'accès ressources et loisirs ainsi que les
informations d'adressage peuvent ne pas faire partie des données de certains jeux de données RRN. Ces données devraient
être ajoutées au fil des mises à jour.

.. admonition:: Notez

    Les segments de liaison par transbordeur sont inclus au RRN afin d'assurer un réseau routier complet.

Commission
^^^^^^^^^^

Chaque fournisseur possède sa méthode d'évaluation pour la détection des données en trop.

Omission
^^^^^^^^

Chaque fournisseur possède sa méthode d'évaluation pour la détection des données manquantes.

Cohérence logique
-----------------

Cohérence conceptuelle
^^^^^^^^^^^^^^^^^^^^^^

L'implantation physique du produit RRN a été effectuée, le plus possible, en conformité au modèle conceptuel du RRN.
L'implantation physique diffère du modèle conceptuel en ce qui a trait à la gestion des métadonnées d'objet et à
l'ajout de certains attributs à l'entité segment routier.

Pour les métadonnées d'objet, le modèle conceptuel prévoit deux séries distinctes d'attributs de métadonnées décrivant
les sources respectives utilisées pour créer et réviser les données. Seules les dates distinctes de création et de
révision ont été implantées. Lorsqu'une date de révision est indiquée et qu'une modification géométrique a été
appliquée à l'objet (par rapport à l'édition précédente du jeu de données), la série d'attributs de métadonnées d'objet
décrit alors les sources utilisées pour la révision. Autrement, les métadonnées d'objet décrivent les sources utilisées
pour la création des données.

Le nom de rue, nom de lieu et l'intervalle d'adresse ont été aussi ajoutés en attribut sur la géométrie de l'entité
segment routier.

Cohérence de domaine
^^^^^^^^^^^^^^^^^^^^

Les valeurs attributives sont validées à l'aide d'un schéma XML contenant la définition des domaines de valeurs
autorisées définis dans le catalogue d'entités.

Les combinaisons de valeurs d'attribut autorisées sont validées à l'aide d'un logiciel développé à l'interne.

Cohérence de format
^^^^^^^^^^^^^^^^^^^

Les formats des données RRN se conforment aux formats de distribution décrits dans le
:doc:`product_distribution_formats`.

Cohérence topologique
^^^^^^^^^^^^^^^^^^^^^

Les relations spatiales des entités des jeux de données RRN sont validées systématiquement à l'aide de logiciels
développés à l'interne.

La validation réalisée consiste à détecter et à corriger dans la mesure du possible : la duplication d'entités, la
connexion entre les entités linéaires et ponctuelles du réseau routier, la cardinalité entre les segments et les
jonctions, l'assignation des identifiants (IDN), les incohérences géométriques (« spikes ») ainsi que la continuité des
réseaux de numéro de route, nom de route, nom de rue et des intervalles d'adresse.

Précision spatiale
------------------

Précision spatiale absolue
^^^^^^^^^^^^^^^^^^^^^^^^^^

La précision géométrique des objets est représentée par la différence entre la position de ces objets dans le jeu de
données et leurs positions réelles mesurées relativement au réseau géodésique. La précision peut varier d'un objet à un
autre. Celle-ci est donc est fournie en attribut à chaque occurrence d'entité et est exprimée selon la Précision
cartographique circulaire normalisée (PCCN).

Erreur circulaire standard :

.. math::
    \sigma_c = 0.7071 (\sigma_x^{2} + \sigma_y^{2})^{\frac12}

    \sigma_x : \text{écart-type dans l'axe X}

    \sigma_y : \text{écart-type dans l'axe Y}

Précision circulaire cartographique normalisée :

.. math:: \text{PCCN} = 2.1460 \sigma_c

La précision planimétrique visée est de 10 mètres ou mieux à un niveau de confiance de 90%. Dans le cadre de la
maintenance des données, aucune validation systématique de la précision géométrique et attributive n'est effectuée sur
l'ensemble des jeux de données RRN.

La précision des données est évaluée en fonction des méthodes utilisées pour contrôler les sources d'acquisition
utilisées (GPS, imagerie, photogrammétrie, etc.) et des erreurs de positionnement liées à l'extraction des données. La
méthode d'évaluation de la précision est déterminée par le fournisseur des données.

Précision spatiale relative
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Inconnu

Précision temporelle
--------------------

Précision d'une mesure de temps
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ne s'applique pas

Cohérence temporelle
^^^^^^^^^^^^^^^^^^^^

Ne s'applique pas

Validité temporelle
^^^^^^^^^^^^^^^^^^^

Ne s'applique pas

Exactitude thématique
---------------------

Exactitude de classification
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Inconnu

Exactitude des attributs non quantitatifs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

La méthode utilisée pour évaluer l'exactitude des attributs non quantitatifs par rapport à la réalité est déterminée
par le fournisseur des données.

Précision des attributs quantitatifs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

La méthode utilisée pour évaluer la précision des attributs quantitatifs par rapport à la réalité est déterminée par le
fournisseur des données.

Acquisition des données
=======================

Description
-----------

Chaque fournisseur est libre d'utiliser la méthode d'acquisition de son choix. La méthode sélectionnée doit permettre
d'obtenir des données géospatiales de qualité (précises, actuelles, cohérentes) pour l'ensemble du jeu de données.
Plusieurs sources d'acquisition sont utilisées : GPS, ortho-images, ortho-photos, photogrammétrie.

La technique d'acquisition utilisée par le fournisseur est décrite dans les métadonnées d'objet attribuées à chaque
occurrence d'entité.

Maintenance des données
=======================

Description
-----------

La maintenance des données RRN est effectuée par l'entremise d'ententes de partenariat intergouvernemental (fédéral,
provincial, territorial et municipal) par les organismes gouvernementaux intéressés, identifiés être les plus près de
la source et capables d'offrir des représentations adéquates et actualisées des phénomènes routiers. La fréquence de
maintenance visée est d'au moins une mise à jour par an.

Afin d'aider les utilisateurs des données RRN dans leur gestion des mises à jour, ces dernières sont également
distribuées selon les effets de mise à jour (ajout, destruction, modification, confirmation). Pour ce faire, des règles
d'identification et des méthodes de classification des modifications ont été établies.

Les règles d'identification ont pour but d'identifier de façon univoque chaque occurrence des entités et sont
expliquées dans le :doc:`identification_rules`.

Les méthodes utilisées pour déterminer les effets de mise à jour (ajout, destruction, modification et confirmation)
sont décrites dans le :doc:`change_management`.

Livraison du produit
====================

Les formats de fichiers de sortie disponibles pour le produit sont : GML (*Geography Markup Language*), GPKG (*OGR
Geopackage*), KML (*Keyhole Markup Language*) and SHP (*ESRI*\ |trade| *Shapefile*).

:doc:`product_distribution_formats` décrit le nom des fichiers, entités et attributs.

L'utilisation des données est soumise aux conditions énoncées dans l'`Accord de licence d'utilisation sans restriction
de GéoBase <http://www.geobase.ca>`_.

Métadonnées
===========

Ne s'applique pas
