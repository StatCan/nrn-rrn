Réseau routier national (RRN)
=============================

[![Repository](https://img.shields.io/badge/Repository-nrn--rrn-brightgreen.svg?style=flat-square&logo=github)](https://github.com/jessestewart1/nrn-rrn)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg?style=flat-square)](https://opensource.org/licenses/BSD-3-Clause)
[![Documentation Status](https://readthedocs.org/projects/nrn-rrn-docs/badge/?style=flat-square)](https://nrn-rrn-docs.readthedocs.io/en/latest/)

## Description

Le RRN a été adopté par les membres du Comité mixte des organismes intéressés à la géomatique (CMOIG) et du Conseil 
canadien de géomatique (COCG) pour fournir des données géospatiales et attributives de qualité (actuelles, précises, 
cohérentes), homogènes et normalisées de l'ensemble du réseau routier canadien. Le RRN fait partie de l'initiative 
GéoBase qui vise à fournir une infrastructure géospatiale commune qui est maintenue régulièrement par les organisations 
les *plus proches de la source*.

Le RRN est distribué sous forme de treize ensembles de données provinciaux/territoriaux constitués de deux entités 
linéaires (segments routiers et segments de liaison par transbordeur), de trois entités ponctuelles (jonctions, 
passages obstrués et points de péage) et de trois entités tabulaires (intervalles d'adresses, noms de rue et de lieu et 
liens de noms non officiels). Actuellement, le RRN est accessible au public sur le portail de données ouvertes du 
gouvernement (https://open.canada.ca/fr).

Le contenu du RRN est largement conforme à la norme ISO 14825 (https://www.iso.org/standard/54610.html).

## Configuration

Le référentiel du projet NRN est désigné par son nom de référentiel réel : `nrn-rrn`.

### Dépendances logicielles

Le `nrn-rrn` n'a pas de dépendances logicielles obligatoires mais recommande fortement le logiciel spécifié dans cette 
section. De plus, la documentation pour l'installation et l'utilisation de `nrn-rrn` utilisera ce logiciel car il 
représente l'approche la plus simple et recommandée.

#### Anaconda / conda

Le `nrn-rrn` est écrit en Python pur, mais a plusieurs dépendances écrites avec des bibliothèques C. Ces bibliothèques 
C peuvent être difficiles à installer (surtout sous Windows) et, par conséquent, il est recommandé de créer et 
d'utiliser l'environnement virtuel conda défini dans le `nrn-rrn`. conda est un gestionnaire d'environnement et de 
packages et est le choix préférable pour la gestion des dépendances car il fournit des binaires pré-construits pour 
toutes les dépendances du `nrn-rrn` pour toutes les plates-formes (Windows, Mac, Linux).

Anaconda avec conda >= 4.9 (la dernière version d'Anaconda satisfera à cette exigence).  
Télécharger : https://docs.anaconda.com/anaconda/install/

Miniconda suffira également (distribution minimale ne contenant que Python et conda).  
Télécharger : https://docs.conda.io/en/latest/miniconda.html

#### Git

Git est recommandé pour une installation plus simple du référentiel et l'intégration des mises à jour.  
Télécharger : https://git-scm.com/downloads

### Installation

Utilisez les étapes suivantes pour installer le référentiel `nrn-rrn` et l'environnement conda :

1. Installer le référentiel.

   a) Utilisation de Git :  
   ```
   git clone https://github.com/jessestewart1/nrn-rrn.git
   ```

   b) Installation manuelle : Téléchargez et décompressez le référentiel : https://github.com/jessestewart1/nrn-rrn.


2. Créez l'environnement conda à partir du fichier `environment.yml` :
```
conda env create -f <path to environment.yml>
```
