**********************
Matériaux de référence
**********************

.. include:: <isonum.txt>
.. include:: <isopub.txt>

.. contents:: Matières :
   :depth: 1

Sigles et abréviations
======================

.. glossary::
    CMOIG
        Comité mixte des organismes intéressés à la géomatique

    COCG
        Conseil canadien de géomatique

    CRSID
        Coordinate Reference System Identifier

    DVN
        Données vectorielles nationales

    GDF
        Geographic Data File

    GML
        Geography Markup Language

    GPKG
        Open Geospatial Consortium Geopackage

    GPS
        Système mondial de localisation

    GUID
        Identifiant unique globale

    ID
        Identifiant

    IDN
        Identifiant national

    IDUU
        Identifiant unique universel

    IEEE
        Institute of Electrical and Electronics Engineers

    ISO
        Organisation internationale de normalisation

    KML
        Keyhole Markup Language

    MNE
        Modèle numérique d'élévation

    NAD83CSRS
        Système de référence nord-américain de 1983 (Système canadien de référence spatiale)

    NatProvTer
        National, provincial ou territorial

    NSDI
        National Spatial Data Infrastructure - USA

    OGC
        Open Geospatial Consortium

    PCCN
        Précision cartographique circulaire normalisée

    RHN
        Réseau hydrographique national

    RNCan
        Ressources naturelles Canada

    RRN
        Réseau routier national

    SHP
        ESRI Shapefile

    StatsCan
        Statistique Canada

    TC
        Comité technique

    XML
        Extensible Markup Language

Terms and Definitions
=====================

Attribut
    Caractéristique d'entité. Par exemple, nombre de voies ou type de chaussée.

Classe
    Description d'un ensemble d'objets partageant les mêmes attributs, opérations, méthodes, relations et sémantique.
    Une classe n'a pas toujours une géométrie associée (ex. la classe Intervalles d'adresse).

Données vectorielles nationales
    Plusieurs couches de données vectorielles partageront les mêmes spécifications. Ces couches sont appelées Données
    vectorielles nationales (DVN). Le Réseau routier national (RRN) et le Réseau hydrographique national (RHN) sont des
    exemples de DVN.

Élément linéaire du réseau
    Classe abstraite qui englobe les entités Élément routier et Liaison par transbordeur.

Élément routier
    Une route est une section linéaire à la surface de la Terre qui a été conçue pour la circulation de véhicules ou
    qui en est le résultat. Un Élément routier est la représentation d'une route entre deux Jonctions. Un Élément
    routier est toujours limité par deux Jonctions. Un Élément routier est composé d'un ou plusieurs Segments routiers.

Entité
    Représentation numérique d'un phénomène réel. Par exemple, la représentation numérique de la rue King est une
    entité.

Identifiant unique universel
    La définition et la méthode utilisée pour la génération d'un Identifiant universel unique (IDUU) est décrite dans
    le document :doc:`identification_rules.rst`.

Jeu de données
    Collection de données identifiable pour une province ou un territoire canadien.

Liaison par transbordeur
    La route approximative suivie par un navire transbordeur qui transporte des véhicules entre deux emplacements sur
    le réseau routier. Deux jonctions limitent toujours une liaison par transbordeur.

Objet
    Un objet est une instance d'une classe.

Segment
    Portion d'un Élément linéaire du réseau présentant un ensemble commun de caractéristiques (attributs) définies.
