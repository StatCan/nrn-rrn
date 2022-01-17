********
Validate
********

.. include:: <isonum.txt>
.. include:: <isopub.txt>

.. contents:: Matières :
   :depth: 3

Aperçu
======

Le processus `validate` applique un ensemble de validations et de restrictions sur la géométrie et l'attribution des
ensembles de données RRN. L'intention du processus `validate` est de signaler les erreurs de données réelles et
potentielles avant de continuer avec le reste du pipeline RRN.

La seule sortie de `validate` est un fichier journal (.log) qui sera exporté vers :
``nrn-rrn/data/interim/validations.log``. Le processus prévu consiste pour l'utilisateur à réparer les données source
d'origine en fonction des erreurs spécifiées dans le journal de sortie. Une fois terminé, l'ensemble du pipeline doit
être réexécuté à partir du processus initial.

Structure du journal
====================

Le journal de sortie contiendra une série de journaux standardisés pour chaque validation exécutée par le processus
`validate`. Chaque validation enregistrée aura la même structure de contenu.

Structure générique : ::

    <horodatage> - WARNING: E<code d'erreur> - <jeu de données RRN> - <Description de l'erreur>.

    Values:
    <uuid>
    ...

    Query: "uuid" in ('<uuid>', ...)

Structure spécifique : ::

    2022-01-04 16:00:51 - WARNING: E201 - roadseg - Features within the same dataset must not be duplicated.

    Values:
    76d283b46076400c900ed84c02ab605f
    c9ac2f60a0814eec9ff56bf95ad79804

    Query: "uuid" in ('76d283b46076400c900ed84c02ab605f', 'c9ac2f60a0814eec9ff56bf95ad79804')

**Composants :**

:Values: « Valeurs » en français. Une liste contenant la valeur ``uuid`` de chaque enregistrement marqué par la
         validation pour l'ensemble de données RRN. ``uuid`` est un identifiant unique attribué à chaque enregistrement
         de chaque ensemble de données RRN dans le but de suivre et d'identifier les enregistrements tout au long du
         pipeline RRN.
:Query: « Requête » en français. Une expression QGIS pour interroger tous les enregistrements marqués par la validation
        du jeu de données RRN. Celui-ci contiendra les mêmes valeurs que ``Values``.

Erreurs de validation
=====================

Structure d'erreur
------------------

Toutes les validations se sont vu attribuer un code d'erreur unique avec la structure suivante: ::

    E<code majeur (1-2 chiffres)><code mineur (2 chiffres)>

Les codes d'erreur majeure et mineure sont utilisés pour fournir une classification plus simplifiée et plus efficace
des validations en fonction du type général de problème que la validation tente de résoudre.

Codes d'erreur
--------------

E100 - Construction
^^^^^^^^^^^^^^^^^^^

:E101: Les arcs doivent avoir une longueur >= 3 mètres, à l'exception des structures (par exemple, les ponts).
:E102: Les arcs doivent être simples (c'est-à-dire qu'ils ne doivent pas se chevaucher, se croiser ou toucher leur
       intérieur).
:E103: Les arcs doivent avoir une distance >= 0,01 mètre entre les sommets adjacents (tolérance de cluster).

E200 - Dédoublement
^^^^^^^^^^^^^^^^^^^

:E201: Les entités d'un même jeu de données ne doivent pas être dupliquées.
:E202: Les arcs du même jeu de données ne doivent pas se chevaucher (c'est-à-dire contenir des sommets adjacents
       dupliqués).

E300 - Connectivité
^^^^^^^^^^^^^^^^^^^

:E301: Les arcs ne doivent se connecter qu'aux extrémités (nœuds).
:E302: Les arcs doivent être >= 5 mètres les uns des autres, à l'exclusion des arcs connectés (c'est-à-dire sans
       pendants).

E400 - Dates
^^^^^^^^^^^^

:E401: Les attributs « datecre » et « daterev » doivent avoir des longueurs de 4, 6 ou 8. Par conséquent, en utilisant
       des chiffres complétés par des zéros, les dates peuvent représenter les formats : AAAA, AAAAMM ou AAAAMMJJ.
:E402: Les attributs « datecre » et « daterev » doivent avoir une combinaison AAAAMMJJ valide.
:E403: Les attributs « datecre » et « daterev » doivent être compris entre 19600101 et la date actuelle, inclusivement.

E500 - Identifiants
^^^^^^^^^^^^^^^^^^^

:E501: Les ID doivent être des chaînes hexadécimales à 32 chiffres.
:E502: Les liaisons IDN doivent être valides.

E600 - Numéros de sortie
^^^^^^^^^^^^^^^^^^^^^^^^

:E601: L'attribut « numsortie » doit être identique, à l'exception de la valeur par défaut ou « Aucun », pour tous les
       arcs partageant un IDN.
:E602: Lorsque l'attribut « numsortie » n'est pas égal à la valeur par défaut ou « Aucun », l'attribut « classroute »
       doit être égal à l'un des éléments suivants : « Autoroute », « Bretelle », « Réservée transport commun »,
       « Route express », « Service ».

E700 - Intégration de traversier
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:E701: Les arcs de ferry doivent être connectés à un arc routier à au moins un de leurs nœuds.

E800 - Nombre de voies
^^^^^^^^^^^^^^^^^^^^^^

:E801: L'attribut « nbrvoies » doit être compris entre 1 et 8 inclus.

E900 - Vitesse
^^^^^^^^^^^^^^

:E901: L'attribut « vitesse » doit être compris entre 5 et 120, inclusivement.

E1000 - Codage
^^^^^^^^^^^^^^

:E1001: L'attribut contient un ou plusieurs points d'interrogation (« ? »), qui peuvent être le résultat d'un codage de
        caractères non valide.

E1100 - Étendue
^^^^^^^^^^^^^^^

:E1101: La géométrie n'est pas complètement dans la région source.
