# Portail Livrables — Spécification v1.1

> Rédigée en leçon 01 (02/08/2026). Toute évolution du périmètre passe par ce fichier.
>
> **v1.1 — 02/08/2026** : mise à jour après confrontation de la spec au code et au disque.
> Trois écarts constatés le jour même de la rédaction (voir « Journal des révisions » en fin
> de document). La spec fait foi : c'est au code de s'aligner, pas l'inverse.

## Problème
Plus de 100 livrables (.docx, .pptx) sont produits automatiquement chaque semaine dans
`livrables/` et `sources/veille/`. Les retrouver suppose aujourd'hui de fouiller les
dossiers à la main.

## Utilisateur
Une seule personne : moi. Pas de compte, pas de connexion, pas de multi-utilisateur.
L'application tourne en local sur ma machine.

## Données
Uniquement des fichiers déjà présents sur le disque :

| Dossier | Contenu | Couvert par le code ? |
|---|---|---|
| `livrables/lecons/` | leçons des parcours d'apprentissage | ✅ |
| `livrables/quiz/` | quiz PowerPoint | ✅ |
| `livrables/infographies/` | infographies PowerPoint | ✅ |
| `sources/veille/` | veilles, y compris les sous-dossiers | ✅ |
| `livrables/documents/` | documents divers, fiches synthèse, annexes | ⛔ **pas encore** |
| `livrables/controles/` | notes de contrôle qualité hebdomadaires | ⛔ **pas encore** |

**Extensions retenues** : `.docx`, `.pptx`, `.pdf`, `.md`.

**Exclusions explicites** : les fichiers de verrouillage temporaires créés par Office, dont le
nom commence par `~$`, ne sont **pas** des livrables et ne doivent jamais être comptés.

Aucune donnée personnelle de tiers. **Lecture seule** : l'application ne modifie ni ne
supprime jamais un livrable.

## Fonctions attendues (v1)
1. Lister tous les livrables avec date, type, taille.
2. Rechercher par mot-clé dans le nom du fichier.
3. Filtrer par type (leçon, quiz, infographie, veille, document, contrôle).
4. Trier par date, du plus récent au plus ancien.
5. Ouvrir un livrable d'un clic.

**Précision sur la date** (fonctions 1 et 4) : la date qui fait référence est celle contenue
dans le NOM du fichier (`YYYY-MM-DD_...`), et non la date de dernière modification du fichier
sur le disque. Un livrable corrigé aujourd'hui ne doit pas remonter en tête du classement.

## Hors périmètre (v1)
- Lire le CONTENU des fichiers .docx (seulement leur nom et leurs dates).
- Modifier, renommer ou supprimer un fichier.
- Publier l'application en ligne.
- Indexer `livrables/projets/` : c'est le code du portail lui-même, pas un livrable.

## Critère de réussite
Retrouver un livrable précis en **moins de 10 secondes**, à partir de l'application **déjà
ouverte**, sans avoir à ouvrir le Finder ni l'Explorateur.

---

## Journal des révisions

### v1.1 — 02/08/2026
Trois écarts constatés en confrontant la spec au code (`scripts/inventaire.js`) et au contenu
réel du disque, le jour même de la rédaction de la v1 :

1. **Extensions** — la v1 ne mentionnait que `.docx` et `.pptx` par dossier, alors que le code
   acceptait déjà `.pdf` et `.md`. Les quatre extensions sont désormais déclarées explicitement.
2. **Dossiers manquants** — `livrables/documents/` et `livrables/controles/` existaient sans
   figurer ni dans la spec ni dans le code. Conséquence concrète : l'annexe pédagogique du
   02/08 et les notes de contrôle qualité étaient invisibles pour le portail. Ils sont ajoutés
   à la spec ; **le code ne les couvre pas encore** (voir « reste à faire » dans `PROJET.md`).
3. **Critère de réussite** — « moins de 10 secondes » ne disait pas à partir de quel moment.
   Précisé : à partir de l'application déjà ouverte.

Deux précisions ajoutées au passage, issues de l'exécution réelle du script :
- exclusion des fichiers de verrouillage Office (`~$…`), qui étaient comptés comme livrables ;
- la date de référence est celle du NOM du fichier, pas son `mtime`.
