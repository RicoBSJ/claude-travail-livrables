# Portail Livrables — Spécification v1

> Rédigée en leçon 01 (02/08/2026). Toute évolution du périmètre passe par ce fichier.

## Problème
Plus de 100 livrables (.docx, .pptx) sont produits automatiquement chaque semaine dans
`livrables/` et `sources/veille/`. Les retrouver suppose aujourd'hui de fouiller les
dossiers à la main.

## Utilisateur
Une seule personne : moi. Pas de compte, pas de connexion, pas de multi-utilisateur.
L'application tourne en local sur ma machine.

## Données
Uniquement des fichiers déjà présents sur le disque :
- `livrables/lecons/` (.docx)
- `livrables/quiz/` (.pptx)
- `livrables/infographies/` (.pptx)
- `sources/veille/` (.docx, y compris sous-dossiers)

Aucune donnée personnelle de tiers. **Lecture seule** : l'application ne modifie ni ne
supprime jamais un livrable.

## Fonctions attendues (v1)
1. Lister tous les livrables avec date, type, taille.
2. Rechercher par mot-clé dans le nom du fichier.
3. Filtrer par type (leçon, quiz, infographie, veille).
4. Trier par date, du plus récent au plus ancien.
5. Ouvrir un livrable d'un clic.

## Hors périmètre (v1)
- Lire le CONTENU des fichiers .docx (seulement leur nom et leurs dates).
- Modifier, renommer ou supprimer un fichier.
- Publier l'application en ligne.

## Critère de réussite
Retrouver un livrable précis en moins de 10 secondes, sans ouvrir le Finder ni l'Explorateur.
