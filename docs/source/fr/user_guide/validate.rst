********
Validate
********

.. include:: <isonum.txt>
.. include:: <isopub.txt>

.. contents:: Matières :
   :depth: 3

Aperçu
======

Le processus ``validate`` applique un ensemble de validations et de restrictions sur la géométrie et l'attribution des
ensembles de données RRN. L'intention du processus ``validate`` est de signaler les erreurs de données réelles et
potentielles avant de continuer avec le reste du pipeline RRN.

La seule sortie de ``validate`` est un GeoPackage qui contiendra un sous-ensemble de fonctionnalités pour chaque
validation et ensemble de données marqué par cette validation. Ce GeoPackage sera exporté vers :
``nrn-rrn/data/interim/validations.gpkg``. Le processus prévu consiste pour l'utilisateur à réparer les données sources
d'origine en fonction des sous-ensembles de données du GeoPackage de sortie. Une fois terminé, l’ensemble du pipeline
doit être réexécuté depuis le début.

Erreurs de validation
=====================

Structure d'erreur
------------------

Toutes les validations se sont vu attribuer un code d'erreur unique avec la structure suivante: ::

    <code majeur (1-2 chiffres)><code mineur (2 chiffres)>

Les codes d'erreur majeure et mineure sont utilisés pour fournir une classification plus simplifiée et plus efficace
des validations en fonction du type général de problème que la validation tente de résoudre.

Codes d'erreur
--------------

Certaines validations sont des avertissements destinés à détecter des problèmes potentiels de données et peuvent ne pas
devoir être résolus selon les circonstances. Pour faire la distinction entre les avertissements et les vraies erreurs,
chacun des codes d'erreur suivants est étiqueté comme « ferme » ou « légère » :

:ferme: L'erreur doit être résolue.
:légère: L'erreur doit être examinée et résolue uniquement s'il s'agit réellement d'un problème. Si ce n'est pas un
         problème, on peut l'ignorer.

100 - Construction
^^^^^^^^^^^^^^^^^^^

:101 [légère]: Les arcs doivent avoir une longueur >= 1 mètre, à l'exception des structures (par exemple, les ponts).
:102 [ferme]: Les arcs ne doivent pas avoir une longueur nulle.
:103 [ferme]: Les arcs doivent être simples (c'est-à-dire qu'ils ne doivent pas se chevaucher, se croiser ou toucher
              leur intérieur).

200 - Dédoublement
^^^^^^^^^^^^^^^^^^^

:201 [ferme]: Les entités d'un même jeu de données ne doivent pas être dupliquées.
:202 [ferme]: Les arcs du même jeu de données ne doivent pas se chevaucher (c'est-à-dire contenir des sommets adjacents
              dupliqués).

300 - Connectivité
^^^^^^^^^^^^^^^^^^^

:301 [légère]: Les arcs doivent être >= 5 mètres les uns des autres, à l'exclusion des arcs connectés (c'est-à-dire
               sans pendants).

400 - Dates
^^^^^^^^^^^^

:401 [ferme]: Les attributs « datecre » et « daterev » doivent avoir des longueurs de 4, 6 ou 8. Par conséquent, en
              utilisant des chiffres complétés par des zéros, les dates peuvent représenter les formats : AAAA, AAAAMM
              ou AAAAMMJJ.
:402 [ferme]: Les attributs « datecre » et « daterev » doivent avoir une combinaison AAAAMMJJ valide.
:403 [ferme]: Les attributs « datecre » et « daterev » doivent être compris entre 19600101 et la date actuelle,
              inclusivement.

500 - Identifiants
^^^^^^^^^^^^^^^^^^^

:501 [ferme]: Les liaisons IDN doivent être valides.

600 - Numéros de sortie
^^^^^^^^^^^^^^^^^^^^^^^^

:601 [ferme]: L'attribut « numsortie » doit être identique, à l'exception de la valeur par défaut ou « Aucun », pour
              tous les arcs partageant un IDN.
:602 [légère]: Lorsque l'attribut « numsortie » n'est pas égal à la valeur par défaut ou « Aucun », l'attribut
               « classroute » doit être égal à l'un des éléments suivants : « Autoroute », « Bretelle »,
               « Réservée transport commun », « Route express », « Service ».

700 - Intégration de traversier
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:701 [légère]: Les arcs de ferry doivent être connectés à un arc routier à au moins un de leurs nœuds.

800 - Nombre de voies
^^^^^^^^^^^^^^^^^^^^^^

:801 [légère]: L'attribut « nbrvoies » doit être compris entre 1 et 8 inclus.

900 - Vitesse
^^^^^^^^^^^^^^

:901 [légère]: L'attribut « vitesse » doit être compris entre 5 et 120, inclusivement.

1000 - Codage
^^^^^^^^^^^^^^

:1001 [légère]: L'attribut contient un ou plusieurs points d'interrogation (« ? »), qui peuvent être le résultat d'un
                codage de caractères non valide.
