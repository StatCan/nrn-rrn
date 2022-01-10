***************************
Modèle d'échange de données
***************************

.. include:: <isonum.txt>
.. include:: <isopub.txt>

.. contents:: Matières :
   :depth: 2

Aperçu
======

Ce document décrit les recommandations et le format utilisé pour l'échange de données entre les fournisseurs de données
RRN. C'est important à noter que ce modèle de données physique ne constitue pas le modèle de distribution final des
données RRN.

Le document résulte de huit réunions de consultation réalisées avec les fournisseurs de données les *Plus proches de la
source*. La large gamme des participants aux comités de producteurs et d'utilisateurs a permis à ce processus
d'identifier et d'examiner de nombreux aspects de la modèle physique d'échange de données.

Modèle d'échange de données
===========================

.. figure:: /_static/figures/modèle_d'échange_de_données.png
    :alt: Modèle d'échange de données

    Figure 1 : Modèle d'échange de données.

Recommendations
===============

Divers points de discussion ont été soulevés au cours des consultations. Les résolutions ou recommandations suivantes
ont été établi par consensus. Certaines des recommandations incluses ci-après n'ont pas été discutées lors de la
consultation mais sont fondées sur des pratiques préalablement établies.

Etendue de l'intervalle d'adresse
---------------------------------

Les intervalles d'adresses ne doivent pas se chevaucher sur plus d'un IDN élément routier. Un IDN élément routier
peut cependant avoir plus d'un intervalles d'adresses adjacents. Dans le cas où une valeur de Numéro de maison n'est
pas connue lors de la segmentation, les valeurs interpolées peuvent être calculé ou l'intervalle d'adressage du Segment
routier adjacent peut être répété. La segmentation peut être introduite pour signaler la valeur connue du Numéro de
maison. Aux jonctions où aucune valeur de Numéro de maison n'est connue, les valeurs interpolées peuvent être calculé
ou une valeur -1 (pour inconnu) peut être attribuée comme Numéro de maison.

Incrément d'intervalle d'adresse
--------------------------------

Une valeur de Numéro première maison d'un intervalle d'adresses peut être inférieure, égale ou supérieure à sa valeur
de Numéro dernière maison. Avoir une valeur du Numéro première maison toujours inférieure ou égale à la valeur du
Numéro dernière maison est possible grâce à l'utilisation de l'Indicateur sens numérisation.

Une valeur de Numéro de maison 0 ne peut être combinée qu'avec une autre valeur de Numéro de maison 0. Cela signifie
que le Segment routier ne avoir un intervalle d'adresses.

Sens numérisation
-----------------

La direction de numérisation de tous les Segments routiers avec des Intervalles d'adresses remplis doit suivre
l'orientation de l'Intervalle d'adresses de la Première à la Dernière valeur du Numéro de maison. L'orientation à
partir de la coordonnée Inférieure gauche d'un vecteur n'est plus requis mais peut toujours être utilisé lorsqu'il n'y
a pas d'intervalle d'adresse.

Type de rue et type de lieu
---------------------------

Les valeurs Type de rue et Type de lieu sont complètement épelées sans abréviations dans la casse appropriée (Première
lettre du premier mot en majuscule et caractères restants en minuscule). Valeurs non répertoriées actuellement dans
l'attribut RRN des domaines peuvent être ajoutés. Lorsque les listes seront bien établies, l'utilisation de codes sera
envisagée.

Caractères spéciaux
-------------------

Les caractères spéciaux doivent rester s'ils font partie du Nom de lieu officiel ou du Corps du nom. Des caractères
unicode sont utilisés.

Noms des routes, numéros des routes et noms des rues
----------------------------------------------------

À moins qu'il ne soit officiellement reconnu comme nom de rue, il n'est pas recommandé d'insérer des valeurs Numéros
des routes et Noms des routes dans le tableau des Noms des rues.

Noms de lieux
-------------

L'information sur le fournisseur de la source provinciale ou territoriale est considérée comme le fournisseur de la
valeur valide du Nom de lieu. Devrait un polygone administratif géopolitique de Nom de lieu soit disponible à partir
d'une autre source qui n'est pas couverte par le provincial ou le fournisseur de la source territoriale, ce polygone
sera considéré comme valide jusqu'à ce qu'il soit remplacé par le Province ou territoire.

Éléments routiers situés dans les territoires non organisés
-----------------------------------------------------------

Lorsque le fournisseur le *Plus proche de la source* est incapable de définir ou d'associer un nom administratif
géopolitique pour régions de son ensemble de données que d'autres sources doivent être prises en compte et utilisées
pour remplir le champ Nom de lieu jusqu'à ce que temps qu'il puisse être remplacé par une source plus autorisée.

Métadonnées sur les composants d'adressage
------------------------------------------

Lors de la consultation, il a été établi que seuls les Dates et le Fournisseur feraient partie des métadonnées de
l'objet à renseigner dans les tables d'adressage. Par conséquent, d'autres attributs de Métadonnées d'objet tels que
Précision planimétrique, Technique acquisition et Couverture des métadonnées peuvent être définies sur une valeur
inconnue (-1). Nom jeu de données et Version normes peut et doit toujours être renseignée.

Métadonnées sur la jonction
---------------------------

As an option, Object Metadata attributes on Junctions can be populated by the data provider. Otherwise, they will be
automatically populated by the data publisher using the following default values and rules.

En option, les attributs de Métadonnées d'objet sur les Jonctions peuvent être renseignés par le fournisseur de
données. Sinon, ils seront automatiquement renseigné par l'éditeur de données à l'aide des valeurs et règles par défaut
suivantes.

:Technique acquisition: 12 (Calculé)
:Fournisseur: 2 (Fédéral)
:Couverture: 1 (Complet)
:Précision planimétrique: Valeur de précision planimétrique la plus élevée des segments de connexion.
:Date création: Date de création la plus basse des segments de connexion ou date actuelle pour la jonction nouvellement
                créée.
:Date révision: Date de révision la plus élevée des segments de connexion ou valeur par défaut pour la jonction
                nouvellement créée.

Gestion des IDN et des métadonnées d'objets
-------------------------------------------

Un IDN ne peut avoir qu'un seul ensemble d'informations de Métadonnées d'objet. Dans le cas d'une caractéristique
linéaire, ces attributs de métadonnées doit être constant sur toute la longueur d'un IDN. Les effets sur les IDN et
Métadonnées d'objet sont basés sur les mises à jour appliquées au fonction ou enregistrement de table. Les effets de
mise à jour sont décrits dans :doc:`change_management`.

Segmentation
------------

Les Segments routiers sont interrompus à n'importe quel nœud topologique (notez qu'un passage à niveau n'est pas
considéré comme une rupture topologique). Segments routiers ne sont pas rompus en raison d'un passage à niveau. Là où
il y a des passages à niveau, les Segments routiers bissectrice ne partagent pas de Jonction. Les Passages à niveau
entre les Segments routiers impliquent des Objets de structure de route, soit des Ponts, soit des Tunnels. Si une
Jonction est présente à l'emplacement de la Séparation de niveau, elle est soit connectée à l'ensemble inférieur de
Segments routiers ou vers l'ensemble supérieur mais jamais vers les deux.

Les Segments routiers sont interrompus en raison de tout changement d'attribution.

Attribution d'IDN
-----------------

Le même IDN est attribué à chaque Segments Routiers ou Segments de liaison par transbordeur adjacent entre les
Jonctions.

Intégrité de la classification routière fonctionnelle
-----------------------------------------------------

Une Classification routière fonctionnelle ne devrait pas changer sur la longueur d'une structure et la structure
devrait avoir la même Classification routière fonctionnelle comme l'un des segments routiers auxquels elle est
connectée.

Les routes avec Classification routière fonctionnelle Artère, Route express, Autoroute, Bretelle et Réservée transport
commun ne doivent pas former une boucle fermée.

Les Segments de liaison par transbordeur sont affectés avec la même valeur de Classification routière fonctionnelle des
deux Segments routiers qu'il rejoint quand ce sont les mêmes. Si les Classification routière fonctionnelle diffèrent,
la valeur la plus basse (c'est-à-dire la classe la plus importante) prévaut.

Noms des routes et numéros des routes continuité du réseau
----------------------------------------------------------

Numéros des routes et noms des routes ne doivent pas avoir d'espaces sur leur étendue et les noms doivent s'étendre au
service associé voies et rampes.

Segment de liaison par transbordeur valence
-------------------------------------------

Dans le monde réel, il n'y a qu'un seul accès à un ferry-boat, donc une fin de Segment de liaison par transbordeur ne
devrait se connecter avec un Segment routier. Une liaison par transbordeur est toujours délimitée par deux Jonctions et
composée d'un ou plusieurs Segments de liaison par transbordeur.

Les liaisons par transbordeur se croisent sans créer de segmentation.

Les Segments de liaison par transbordeur peuvent se terminer en impasse.

Numéro de sortie sur les Jonctions
----------------------------------

When a Road Segment portrays a one-way ramp with an exit number, only the Junction marking its point of entrance (in
the real world) is assigned with the same Exit Number value.

Lorsqu'un Segment routier représente une bretelle à sens unique avec un numéro de sortie, seule la Jonction marquant
son point d'entrée (en le monde réel) se voit attribuer la même valeur de Numéro de sortie.
