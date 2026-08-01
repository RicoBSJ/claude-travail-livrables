# Projet fil rouge — « Portail Livrables »

> Mémoire du parcours **Développement d'applications avec l'IA** (12 leçons, vendredi 8h03).
> Le job `appli-ia-lecon` lit ce fichier au début de chaque leçon et le met à jour à la fin.
> **Ne pas supprimer** : sans lui, la continuité du fil rouge est perdue.

---

## État de l'application

**Amorcée — leçon 01 terminée (02/08/2026).**

Le projet dispose d'une spécification écrite, d'une structure de dépôt Node.js et d'un
premier script fonctionnel en ligne de commande. `npm run inventaire` parcourt les dossiers
de livrables (y compris les sous-dossiers de `sources/veille/`) et affiche, par catégorie,
le nombre de fichiers, leur poids total et les trois plus récents.

**Exécution réelle du 02/08/2026** : 202 livrables détectés — 79 leçons (1 435 Ko),
19 quiz (47 256 Ko), 38 infographies (4 945 Ko), 66 veilles (915 Ko).

Pas encore d'interface : la sortie est du texte dans le terminal. C'est l'objet de la leçon 02.

## Choix techniques arrêtés

| Élément | Choix | Décidé en |
|---|---|---|
| Langage | JavaScript (CommonJS) — TypeScript introduit en leçon 03 | leçon 01 |
| Runtime | **Node.js v24 LTS** (`v24.18.1` relevée sur nodejs.org le 02/08/2026) | leçon 01 |
| Dépendances externes | **aucune** à ce stade — uniquement `fs` et `path` (modules internes) | leçon 01 |
| Framework d'interface | *à décider* | leçon 05 |
| Base de données | *à décider* | leçon 07 |

Aucune bibliothèque tierce n'est installée : c'est délibéré, pour que le projet reste lisible
et sans surface d'attaque au démarrage.

## Fichiers du projet

| Fichier | Rôle |
|---|---|
| `SPEC.md` | Spécification v1 : problème, utilisateur, données, fonctions, **hors périmètre**, critère de réussite |
| `package.json` | Métadonnées du projet, script `inventaire`, `engines.node >= 24`, `private: true` |
| `.gitignore` | Exclut `node_modules/`, `.env`, `*.log`, `dist/`, `.DS_Store` |
| `scripts/inventaire.js` | Parcours récursif des dossiers de livrables, inventaire par catégorie. **Lecture seule.** |
| `PROJET.md` | Ce fichier — mémoire du parcours |

## Livré à la leçon 01

- Vérification de l'environnement (Node, npm, git) avec les versions de référence relevées à la source.
- Rédaction de `SPEC.md` — exercice central de la leçon, appuyé sur le résultat de Geruslu,
  Aliyeva & Tüzün (arXiv, 26/03/2026) : la spécification et l'expertise du développeur sont
  des facteurs déterminants de la qualité du code généré par IA.
- Initialisation du dépôt : `package.json`, `.gitignore`, dossier `scripts/`.
- Premier script exécutable `scripts/inventaire.js`, **testé et fonctionnel**.

## Reste à faire

2. Socle web : transformer la sortie texte en page HTML affichable — générer avec l'IA, puis relire et corriger
3. TypeScript et structure de projet
4. Lecture des données réelles côté serveur (exposer l'inventaire en JSON)
5. Interface (React / Next.js)
6. Recherche et filtres
7. Persistance (base de données locale)
8. API et architecture
9. Qualité, tests, débogage
10. Sécurité et données (RGPD)
11. Mise en production
12. Maintenance et évolution

## Points en suspens

- **Périmètre tranché en leçon 01** : le portail couvre `livrables/lecons`, `livrables/quiz`,
  `livrables/infographies` et `sources/veille` (récursif). Extensions retenues : `.docx`,
  `.pptx`, `.pdf`, `.md`.
- **Poids des quiz** : 19 fichiers pour 47 Mo, soit l'essentiel du volume. À surveiller si un
  jour on veut afficher des aperçus — hors périmètre v1.
- **Chemin racine en dur** : `inventaire.js` remonte de 4 niveaux depuis `__dirname`. Ça marche,
  mais ça casserait si le projet était déplacé. Dette assumée, à traiter en leçon 04 ou 08.
- Le choix du framework d'interface (leçon 05) dépendra de ce que révèlent les leçons 02 à 04.
