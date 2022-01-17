Contribuant
===========

Ce document explique le processus de contribution au projet de Réseau routier national (RRN).

Le mode de contribution préféré est via les *issues* (problèmes) GitHub. Les ajouts, modifications et suppressions de 
code doivent être laissés aux membres du projet RRN.

## Déclaration de disponibilité publique

Le RRN est exposé en tant que référentiel accessible au public pour s'aligner sur le nombre croissant d'initiatives et 
de politiques en faveur des données ouvertes et de la transparence au sein du Gouvernement du Canada et, en 
particulier, de Statistique Canada. Cependant, le RRN est toujours un produit officiel du gouvernement et, bien que le 
code soit accessible au public, tous les composants et détails ne peuvent pas être exposés, notamment :
- Sources de données originales (à l'exclusion de celles qui sont accessibles au public).
- Fournisseurs de données et coordonnées.
- Produits et scripts historiques (y compris ceux créés par Statistique Canada ou tout autre RRN affilié).

## Problèmes d'ouverture

Les commentaires sont grandement appréciés, qu'il s'agisse d'un problème, d'une idée ou d'une question générale. Suivez 
ces étapes lors de l'ouverture d'un problème GitHub :
1. **Vérifier les problèmes préexistants :** Parcourez les problèmes ouverts et fermés pour vérifier si votre problème 
a déjà été traité. Si tel est le cas, commentez le problème existant plutôt que d'ouvrir un nouveau problème.
2. **Ouvrir un problème :** Lorsque vous ouvrez un nouveau problème, utilisez les étiquettes et modèles GitHub 
préexistants. Toutes les sections du modèle ne sont pas obligatoires. Pour éviter les redondances, ne remplissez que 
les sections que vous jugez essentielles à votre problème.
3. **Fermer un problème :** Ne fermez pas un problème, même si vous pensez qu'il est résolu ou qu'il n'est plus 
pertinent. Cette responsabilité devrait être laissée aux membres du projet RRN.

## Modification du code

Les ajouts, modifications et suppressions de code sont autorisés par les non-membres du projet RRN. Cependant, étant 
donné la nature du RRN en tant que projet officiel du gouvernement, un examen approfondi du code doit être prévu avant 
l'acceptation et l'intégration. De plus, tout code fourni deviendra la propriété du RRN et de Statistique Canada.

### Mise en page

Le projet NRN n'applique aucune norme de formatage, cependant, vous devriez essayer de suivre les normes PEP 8 autant 
que possible.

### Gestion des versions

Le projet NRN met périodiquement à jour les dépendances du projet, y compris la version de base de Python. La 
compatibilité est considérée comme un non-problème puisque le RRN est destiné à être exécuté dans son propre 
environnement conda.
