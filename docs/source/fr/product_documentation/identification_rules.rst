***********************
Règles d'identification
***********************

.. include:: <isonum.txt>
.. include:: <isopub.txt>

.. contents:: Matières :
   :depth: 2

Aperçu
======

L'objectif est d'actualiser les produits DVN sur une base régulière dès que des mécanismes auront été implantés parmi
les partenaires de DVN. Un de ces mécanismes est la mise en œuvre de principes de gestion des modifications. Deux
concepts de base sont nécessaires : règles d'identification et définition des classifications des modifications.

Quant à l'identification, les objets qui illustrent les phénomènes du monde réel varient avec le temps, soit par leur
description, soit par la précision des instruments et méthodes utilisées pour leur acquisition initiale. Il est donc
possible que plus d'une représentation des mêmes phénomènes existent. À titre d'exemple, dans le cadre de cette
initiative, nous voulons élaborer et maintenir **une seule** représentation du réseau routier national. Les rôles des
identifiants sont fondamentaux en vue d'assurer le bon échange et la bonne circulation des objets qui ont été modifiés
à la source et qui ont déjà été livrés aux utilisateurs. L'implantation d'une norme pour l'identification permanente
d'un phénomène et de son application vise deux objectifs primaires :

* faciliter la gestion et la distribution des modifications d'objets d'une manière progressive;
* faciliter le processus de fusion, si nécessaire.

Chaque occurrence des entités fondamentales des DVN doit être identifiée de façon unique. Par exemple dans le RRN,
chaque objet géométrique : *élément routier*, *liaison par transbordeur* et *jonction*, décrivant des caractéristiques
spécifiques du réseau linéaire doivent également être identifiés de façon unique.

Norme d'identification
======================

Les identifiants doivent être attribués d'une manière permanente. Pour assurer leur stabilité, les ID attribués doivent
être insignifiants (sans conséquence) dans leur expression [#f1]_. En d'autres mots, les ID ne doivent pas contenir
d'information relative aux données. Des expériences antérieures ont démontré qu'encapsuler de l'information dans les ID
peut provoquer une modification des ID sans qu'aucun changement réel ne se produise dans les données.

Plusieurs normes ont traité la problématique du réseau routier. La plupart de celles-ci invoquent l'importance
d'utiliser des identifiants sans ne jamais préciser d'aucune manière le format ou la méthode d'application. Les
documents suivants, GDF [#f2]_, GIS-T (SIG en normes de données des transports) [#f3]_ et CEN TC 278 [#f4]_ ne
comportent aucune spécification reliée aux identifiants. La norme National Spatial Data Infrastructure – USA (NSDI)
Framework Transportation Identification Standard a été le seul document qui a clairement défini et expliqué un code
d'identifiant [#f5]_. Dans la norme ISO TC 211/SC: Geographic Information Standard - Encoding [#f6]_, il y a une
définition des IDUU qui correspond exactement aux exigences fondamentales recherchées :

    « Un domaine d'application définit un univers et un schéma d'identification appelés identifiants universels uniques
    (IDUU). Un IDUU est attribué à un objet quand il est créé et demeure stable pendant toute la durée de vie de
    l'objet. L'IDUU d'un objet supprimé ne peut pas être réutilisé. Les IDUU servent à faire la gestion à long terme de
    données distribuées et à réaliser des mécanismes d'actualisation. Ces identifiants sont également appelés
    identifiants persistants. Un serveur de noms spéciaux peut être utilisé pour résoudre les identifiants persistants.
    Les identifiants sont uniques à l'intérieur d'un univers limité bien défini caractérisé par un domaine
    d'application. »

Cette définition de l'ISO pour les identifiants a été adoptée. Le mécanisme de génération est présenté à la section
suivante.

Norme d'identification des DVN
==============================

Le caractère unique des ID est l'une des caractéristiques fondamentales qu'il faut maintenir. Deux techniques pour
rendre les ID uniques ont été étudiées.

* La première consiste à mandater une entreprise de générer et de gérer les étendues des ID selon les producteurs de
  données.
* La seconde consiste à utiliser un algorithme de génération d'ID unique [#f7]_ dont pourraient se servir les
  producteurs de données sans gestion particulière de l'étendue ou du domaine.

C'est la seconde méthode qui a été retenue.

Un IDUU est un identifiant qui est unique dans le temps et l'espace, relativement à l'espace de tous les IDUU. La
génération des IDUU ne demande pas une autorité d'enregistrement pour chacun des identifiants. Plutôt, l'identifiant
demande une valeur unique pour l'espace pour chacun des générateurs d'IDUU. Cette valeur spatialement unique est
spécifiée en tant qu'adresse IEEE 802, qui est normalement déjà appliquée aux systèmes reliés en réseau. Cette adresse
de 48 bits peut être attribuée à partir d'un bloc d'adresses obtenu par l'entremise de l'autorité d'enregistrement
IEEE. Cette spécification IDUU présume de la disponibilité d'une adresse IEEE 802.

L'IDUU consiste en un enregistrement de 16 octets et ne doit pas contenir de remplissage entre les champs. Les valeurs
hexadécimales ``a`` à ``f`` doivent être en minuscule. La taille totale est de 128 bits. Pour fin de lecture par des
humains, une représentation de chaîne IDUU (32 caractères) est spécifiée comme une séquence de champs. La chaîne
suivante est un exemple d'IDUU :

* 378a3917e824422cb25f268b8295da51

Pour plus de renseignements : http://www.opengroup.org/onlinepubs/9629399/apdxa.htm#tagcjh_20

Les règles d'attribution et de persistance relativement aux IDUU sont expliquées dans le document
:doc:`change_management`.

Valeurs IDN
===========

L'algorithme abordé au paragraphe précédent permet de la souplesse pour travailler avec plusieurs partenaires. Cet
algorithme bien connu pourrait être utilisé par n'importe quel utilisateur de données pour modifier les données et y
ajouter un nouvel IDN. **Les IDN doivent être générés seulement par des organismes autorisés**. Un soin particulier
doit être accordé aux IDN. Ces IDN permettront éventuellement la synchronisation des données parmi des organismes. Les
utilisateurs de données doivent s'assurer de **ne pas modifier d'aucune manière** ces valeurs IDN. Sinon, l'utilisation
des IDN pour fin de synchronisation sera inutile.

Références
==========

.. [#f1] Bédard Y., Larrivé S. et Proulx M.-J. *Travaux de modélisation pour la mise en place de la base de données
    géospatiale ISIS*, Université Laval, mars 2000.
.. [#f2] ISO Technical Committee 204, Working Group 3. *ISO/TR 14825 GDF – Geographic Data Files – Version 4.0*, ISO/TC
    204 N629, 12 octobre 2000.
.. [#f3] Dueker, K. J. et Butler, J. A. *GIS-T Enterprise Data Model with Suggested Implementation Choices*, Center for
    Urban Studies, School of Urban and Public Affairs, Portland State University, 1 octobre 1997.
.. [#f4] http://www.nen.nl/cen278
.. [#f5] National Spatial Data Infrastructure. *NSDI FRAMEWORK TRANSPORTATION IDENTIFICATION STANDARD -- Public Review
    Draft*, FGDC-STD-999.1-2000, Ground Transportation Subcommittee, Federal Geographic Data Committee, décembre 2000.
.. [#f6] ISO Technical Committee 211, Working Group 4. *Geographic Information – Encoding*, ISO/CD 19118.3, 15 juin
    2001.
.. [#f7] Si vous désirez consulter une définition officielle de IDUU/GUID, nous vous encourageons à aller à : `ISO/IEC
    11578:1996 Technologies de l'information -- Interconnexion de systèmes ouverts (OSI) -- Appel de procédures à
    distance (RPC) <http://www.iso.org/iso/en/CatalogueDetailPage.CatalogueDetail?CSNUMBER=2229&ICS1=35&ICS2=100&
    ICS3=70>`_ ou `DCE 1.1: Remote Procedure Call Open Group Technical Standard Document Number C706, août 1997, 737
    pages <https://pubs.opengroup.org/onlinepubs/009629399/toc.pdf>`_ (ce document remplace C309 DCE: Remote Procedure
    Call 8/94 qui a servi de base pour la spécification ISO).
