*************************
Gestion des modifications
*************************

.. include:: <isonum.txt>
.. include:: <isopub.txt>

.. contents:: Matières :
   :depth: 4

Aperçu
======

L'objectif est d'actualiser les produits DVN sur une base régulière dès que des mécanismes auront été implantés parmi
les partenaires des DVN. Un de ces mécanismes est la mise en œuvre de principes de gestion des modifications. Deux
concepts de base sont nécessaires : règles d'identification et définition des classifications des modifications.

:doc:`identification_rules` définit aussi précisément que possible le mécanisme d'identification utilisé. Du côté de la
gestion des modifications, les DVN ne tente pas de suivre l'évolution des phénomènes du monde réel (entités), mais
essaient plutôt de maintenir une certaine évolution des objets qui les représentent. En d'autres mots, les DVN ne fera
pas le suivi des changements réels dans le territoire, ils identifient seulement les *effets* que ceux-ci ont sur les
données.

Plusieurs projets (ou leur documentation) traitent de la gestion des mises à jour et de la modélisation temporelle
[#f1]_, [#f2]_, [#f3]_. Le modèle dans ce document a été mis au point en collaboration avec le Centre de recherche en
géomatique (CRG) de l'Université Laval [#f4]_.

Il est visé de suivre l'évolution des objets dans le but de relever tout changement qui peut s'être produit entre deux
observations, successives ou non. Les différences notées entre deux observations constituent ce qu'on appelle l'écart
[#f5]_. La gestion des modifications permet également de relever les mises à jour et les corrections apportées aux
données. Le but de la gestion des modifications est de faciliter la synchronisation des bases de données provenant de
partenaires producteurs et de clients selon les normes nationales en vigueur (voir la figure 1 : Évolution de la base
de données en temps).

Le processus de gestion des mises à jour doit aussi permettre la reconstitution des données comme elles existaient à
une date antérieure.

.. figure:: /_static/figures/évolution_de_la_base_de_données_en_temps.png
    :alt: Évolution de la base de données en temps

    Figure 1 : Évolution de la base de données en temps.

Cycle de vie de l'objet
=======================

Les DVN constituent la meilleure représentation des phénomènes d'intérêt du monde réel jusqu'à preuve du contraire. Les
données géométriques dans les DVN ne doivent subir qu'un minimum de changement. Les changements ont lieu quand une
nouvelle source d'information offre une meilleure représentation que la précédente.

Les effets sur les données DVN seront établis en fonction de la représentation précédente. Le cycle de vie des données
est limité par deux événements. Le cycle débute toujours par un « ajout » (attribution d'un nouvel IDN) et se termine
par « élimination ». Entre ces deux événements, la modification géométrique ou descriptive, ou encore la confirmation
de l'état précédent, peut se produire, tout en conservant le même IDN. Les données ayant les effets « ajout »,
« modification géométrique ou descriptive » et « confirmation » sont des entités dites *actives* (ou actuelles). Les
entités ayant l'effet « élimination » sont des données dites *non actives* (historiques).

.. _Effect Types:

Types d'effets
==============

L'actualisation permet d'établir un parallèle entre les données existantes et les nouvelles données provenant d'une
mise à jour. Ces dernières produisent certains *effets* sur les données. Les effets suivants peuvent être classés
comme :

Ajout (Existence)
-----------------

Quand un nouvel objet n'a pas son équivalent dans les DVN, un nouvel objet est *ajouté* avec un nouvel IDN.

Élimination (Existence)
-----------------------

Quand un objet ne représente plus une entité, il est *éliminé*. Ce type d'objet est éliminé des données courantes en
gardant son IDN.

Modification (Évolution)
------------------------

Un objet est dit *modifié* si l'un de ses attributs descriptifs ou sa représentation géométrique est différent. Le cas
échéant, l'IDN initial est préservé pour la nouvelle version de l'objet. Deux types de modification sont possibles.

Modification descriptive
^^^^^^^^^^^^^^^^^^^^^^^^

Une modification descriptive se produit quand une paire d'objets provenant de la même classe sont géométriquement
identiques mais ont des valeurs attributives différentes. Par exemple, le type de surface d'une route spécifique peut
avoir changé de « sans revêtement » à « avec revêtement ».

Modification géométrique
^^^^^^^^^^^^^^^^^^^^^^^^

Une modification géométrique se produit quand une paire d'objets provenant de la même classe ont des géométries
distinctes qui décrivent les mêmes phénomènes.

Trois types de modification géométrique sont actuellement définis à l'intérieur des DVN. Chacun de ces types comporte
un certain niveau de complexité. En comparant deux représentations (ancienne et nouvelle), on peut définir les
modifications géométriques comme étant :

Première méthode
""""""""""""""""

En comparant deux objets, si un sommet est différent de sa représentation précédente, l'ancienne représentation est
éliminée et une nouvelle est ajoutée avec un nouvel IDN. Cette méthode de gérer les modifications de représentation
signifie que *les modifications géométriques ne sont pas suivies*.

Deuxième méthode
""""""""""""""""

Cette méthode de gérer les changements de représentation consiste à comparer les emplacements des anciennes et
nouvelles Jonctions. Deux Jonctions limitent toujours un Élément Linéaire de réseau. Toute modification le long d'un
Élément Linéaire (représentation géométrique) peut se produire entre ses Jonctions. Cela est traité comme une
modification géométrique tout en conservant son IDN. Cependant, quelle qu'en soit la raison, si une des anciennes
Jonctions situées à une extrémité de l'Élément Linéaire de réseau a changé, cet Élément Linéaire de réseau est alors
éliminé et un nouvel Élément Linéaire est ajouté.

Troisième méthode
"""""""""""""""""

Cette méthode est fondée sur des liens topologiques. Si la représentation des Jonctions d'Éléments Linéaires conserve
les mêmes liens topologiques (même si les Jonctions ont changé de place et que la géométrie de l'Élément Linéaire de
réseau a été modifiée), ce changement est alors traité comme une modification géométrique et l'Élément Linéaire de
réseau ainsi que les Jonctions conservent tous leurs IDN.

Confirmation (Évolution)
------------------------

Conjointement avec le changement, il y a *confirmation* des objets quand les attributs géométriques et descriptifs
n'ont pas été modifiés.

Effets utilisés
===============

Données segmentées
------------------

La gestion des modifications sur les données segmentées est faite à l'aide des *effets* définis à :ref:`Effect Types`.

Dans le modèle segmenté, l'effet doit être associé à l'Élément Linéaire au complet même si celui-ci est décomposé en
plusieurs segments à cause d'un changement d'attribut. C'est-à-dire qu'un même effet doit être utilisé pour l'ensemble
des segments qui ont la même valeur d'attribut IDN. Les segments qui décrivent un même Élément Linéaire peuvent avoir
un seul effet et l'ordre de priorité est le suivant : Ajout, Modification descriptive et Confirmation.

La méthode de suivi utilisée pour les modifications géométriques est indiquée par le fournisseur des gestions des
modifications.

Exemple
=======

L'exemple suivant sert à illustrer la gestion d'une mise à jour pour en faciliter la compréhension. Figure 2 : Exemple
d'une mise à jour pour démontrer la comparaison entre les données d'origine et les nouvelles données. En matière de
géométrie, un seul élément route (objet 6) a été ajouté par rapport aux données d'origine. Quant à la description, le
type de surface de l'élément route (objet 2) a changé de sans revêtement à avec revêtement.

.. figure:: /_static/figures/exemple_d'une_mise_à_jour.png
    :alt: Exemple d'une mise à jour

    Figure 2 : Exemple d'une mise à jour.

.. csv-table::
   :header: "Object", "Explication", "Effect"
   :widths: auto
   :align: left

   3, "Aucune correspondance avec un nouvel objet.", "Élimination"
   4, "Aucune correspondance avec un objet dans les données d'origine; l'arrivée de l'objet 6 a modifié la structure
   topologique des objets (et par conséquent, la géométrie).", "Ajout"
   5, "Aucune correspondance avec un objet dans les données d'origine; l'arrivée de l'objet 6 a modifié la structure
   topologique des objets (et par conséquent, la géométrie).", "Ajout"
   6, "Aucune correspondance avec un objet dans les données d'origine; l'entité n'était pas représentée.", "Ajout"
   e, "Aucune correspondance avec un objet dans les données d'origine.", "Ajout"
   f, "Aucune correspondance avec un objet dans les données d'origine.", "Ajout"
   2, "Valeur d'attribut modifiée.", "Modification descriptive"
   1, "La géométrie et les attributs n'ont pas été modifiés.", "Confirmation"
   a, "La géométrie et les attributs n'ont pas été modifiés.", "Confirmation"
   b, "La géométrie et les attributs n'ont pas été modifiés.", "Confirmation"
   c, "La géométrie et les attributs n'ont pas été modifiés.", "Confirmation"
   d, "La géométrie et les attributs n'ont pas été modifiés.", "Confirmation"

Tableau 1 : Mise à jour des effets.

Références
==========

.. [#f1] Langran, Gail. *Time in Geographic Information Systems*, Éd. Taylor & Francis, 1993, 187 p.
.. [#f2] Peuquet, Donna J. *It's About Time: A Conceptual Framework for the Representation of Temporal Dynamics in
    Geographic Information Systems*, Annals of the Association of American Geographers, vol. 84, n° 3, 1994, p. 441-461.
.. [#f3] Worboys, Michael F. *A Unified Model for Spatial and Temporal Information*, The Computer Journal, vol 37,
    n° 1, p. 26-34.
.. [#f4] Pouliot, J., Larrivé, S., and Bédard, Y. *Typologie des mises à jour*, 2000, 11 p.
.. [#f5] L'écart correspond à l'ensemble des différences notées entre deux repères du territoire [#f4]_.