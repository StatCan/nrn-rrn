********************
Utilisation générale
********************

.. include:: <isonum.txt>
.. include:: <isopub.txt>

.. contents:: Matières :
   :depth: 2

Aperçu
======

Le pipeline RRN est séparé en 4 processus distincts destinés à être exécutés en séquence :

1. ``conform``: Standardisation et harmonisation des sources de données au format RRN.
2. ``confirm``: Génération et récupération d'identifiants nationaux uniques (IDN).
3. ``validate``: Application d'un ensemble de validations et de restrictions sur la géométrie et l'attribution des
   ensembles de données RRN.
4. ``export``: Configuration et exportation des formats de distribution de produits requis.

.. figure:: /source/_static/figures/nrn_process_diagram.png
    :alt: Diagramme de processus du RRN

    Figure 1 : Diagramme de processus du RRN.

Mise en œuvre
=============

Chaque processus RRN est implémenté en tant qu'outil d'Interface en ligne de commande (ILC) qui peut être appelé à
partir de n'importe quel shell. Les paramètres de chaque outil ILC sont en grande partie les mêmes, la ``source``
(abréviation de la source provinciale/territoriale) étant le seul paramètre universel et obligatoire pour tous les
outils ILC. Des informations de référence spécifiques, y compris les spécifications des paramètres, peuvent être
affichées en passant :code:`--help` à l'outil ILC.

.. admonition:: Notez

    Il est fortement recommandé d'utiliser le pipeline RRN dans l'environnement conda ``nrn-rrn``. Sinon, le résultat
    et le comportement attendus, tels que documentés, ne peuvent être garantis. Les environnements conda peuvent être
    activés via : :code:`conda activate nrn-rrn`.

Exemples
========

Exécution d'un processus RRN : ::

    python conform.py bc -r

Affichage des informations de référence pour un processus RRN : ::

    python conform.py --help

Tâches de post-traitement
=========================

Une fois le pipeline RRN complet terminé, les tâches manuelles suivantes doivent être effectuées :

1. Copiez les documents de sortie dans le référentiel RRN, en écrasant les fichiers existants :

   i. Depuis ``nrn-rrn/data/processed/<source>.zip/distribution_docs/en/release_notes.yaml`` à ``nrn-rrn/src/export/distribution_docs/data/release_notes.yaml``.
   #. Depuis ``nrn-rrn/data/processed/<source>.zip/distribution_docs/en/release_notes.rst`` à ``nrn-rrn/docs/source/en/product_documentation/release_notes.rst``.
   #. Depuis ``nrn-rrn/data/processed/<source>.zip/distribution_docs/fr/release_notes.rst`` à ``nrn-rrn/docs/source/fr/product_documentation/release_notes.rst``.

#. Utilisez ``git`` pour ``commit`` et ``push`` les fichiers de documentation mis à jour vers le référentiel.

#. Copiez les données traitées sur le serveur RRN concerné sous le sous-répertoire : ``5_Process``. Ignorez les documents de sortie susmentionnés.

#. Décompressez les données WMS de sortie et copiez le File GeoDatabase (``NRN_<SOURCE>_WMS.gdb``) sur le serveur RRN concerné sous le sous-répertoire : ``7_Disseminate/wms``.

#. Générez un nouveau fichier .sd (pour WMS) :

   i. Dans le projet WMS (.aprx), situé dans ``7_Disseminate/wms``, ouvrez l'outil
      « Save As Offline Service Definition » comme indiqué dans la figure 2.

   #. Sélectionnez / remplissez les paramètres requis dans chaque onglet illustré dans la figure 3. Les propriétés du
      service dans la figure 3c sont renseignées à l'aide des données suivantes (exclut les propriétés vides) :

      :Name: WMS
      :Title: National Road Network / Réseau routier national
      :Abstract: NRN WMS service / service WMS du RRN
      :Keyword: canada, geographic infrastructure, infrastructure géographique, nrn, rrn, national road network, réseau routier national, transport, road transport, transport routier, infrastructure, road maps, carte routière, road networks, réseau routier
      :ContactOrganization: Statistics Canada / Statistique Canada
      :Address: 170 Tunney’s Pasture Driveway / 170, Promenade Tunney’s Pasture
      :AddressType: Civic / Civique
      :City: Ottawa
      :StateOrProvince: Ontario
      :PostCode: K1A 0T6
      :Country: Canada
      :ContactVoiceTelephone: 1-800-263-1136
      :ContactFacsimileTelephone: 1-514-283-9350
      :ContactElectronicMailAddress: infostats@statcan.gc.ca

   #. « Analyze », puis « Save » le fichier .sd (voir bas de la figure 3c).

#. Informer les personnes concernées de la nouvelle version du RRN par e-mail.

.. figure:: /source/_static/figures/wms_sd_tool_location.png
    :alt: Emplacement de l'outil « Save As Offline Service Definition »

    Figure 2 : Emplacement de l'outil « Save As Offline Service Definition ».

.. figure:: /source/_static/figures/wms_sd_tool_parameters.png
    :alt: Paramètres de l'outil « Save As Offline Service Definition »

    Figure 3 : Paramètres de l'outil « Save As Offline Service Definition ».
