# Projet fil rouge — « Portail Livrables »

> Mémoire du parcours **Développement d'applications avec l'IA** (12 leçons, vendredi 8h03).
> Le job `appli-ia-lecon` lit ce fichier au début de chaque leçon et le met à jour à la fin.
> **Ne pas supprimer** : sans lui, la continuité du fil rouge est perdue.

---

## État de l'application

**Socle web opérationnel — leçon 02 terminée (07/08/2026).**

Le Portail Livrables dispose désormais d'une interface web locale. `node scripts/serveur.js`
démarre un serveur HTTP sur le port 3000 ; ouvrir http://localhost:3000 affiche une grille de
cartes, une par catégorie de livrables, avec le nombre de fichiers, le poids total et les 5 plus
récents. Les données sont chargées en direct depuis le disque via `fetch('/api/inventaire')`.

**Inventaire lors du démarrage test du 07/08/2026** : 6 catégories — lecons (86 fichiers),
quiz, infographies, veilles, documents, controles. Les fichiers temporaires Office (`~$…`) sont
désormais exclus du comptage.

Pas encore de recherche ni de filtres : c'est l'objet de la leçon 06.

## Choix techniques arrêtés

| Élément | Choix | Décidé en |
|---|---|---|
| Langage | JavaScript (CommonJS) — TypeScript introduit en leçon 03 | leçon 01 |
| Runtime | **Node.js v24 LTS** (`v24.18.1` relevée sur nodejs.org le 02/08/2026) | leçon 01 |
| Serveur HTTP | Module natif `node:http` — sans framework | leçon 02 |
| Interface | HTML/CSS/JS vanilla — sans framework frontend (React/Vue à décider leçon 05) | leçon 02 |
| Dépendances externes | **aucune** à ce stade | leçon 02 |
| Framework d'interface | *à décider* | leçon 05 |
| Base de données | *à décider* | leçon 07 |

Aucune bibliothèque tierce n'est installée : c'est délibéré.

## Fichiers du projet

| Fichier | Rôle |
|---|---|
| `SPEC.md` | Spécification **v1.1** : problème, utilisateur, données, fonctions, hors périmètre, critère de réussite, journal des révisions |
| `package.json` | Métadonnées du projet, scripts `inventaire`, `demo-recursivite` et `serveur`, `engines.node >= 24`, `private: true` |
| `.gitignore` | Exclut `node_modules/`, `.env`, `*.log`, `dist/`, `.DS_Store` |
| `scripts/inventaire.js` | Parcours récursif des dossiers de livrables, inventaire par catégorie — sortie terminal. **Lecture seule.** |
| `scripts/demo_recursivite.js` | **Annexe pédagogique** — même logique qu'inventaire.js, mais commente chaque appel de la fonction. Lancé par `npm run demo-recursivite`. |
| `scripts/serveur.js` | Serveur HTTP local (port 3000). Route `/api/inventaire` → JSON. Routes statiques → fichiers de `public/`. Garde-fou path traversal inclus. **Lecture seule.** Créé le 07/08/2026. |
| `public/index.html` | Première page web du portail : grille de cartes par catégorie, chargement dynamique via `fetch('/api/inventaire')`. CSS intégré (variables, grille responsive). Créé le 07/08/2026. |
| `PROJET.md` | Ce fichier — mémoire du parcours |

## Livré à la leçon 01 (02/08/2026)

- Vérification de l'environnement (Node, npm, git) avec les versions de référence relevées à la source.
- Rédaction de `SPEC.md`.
- Initialisation du dépôt : `package.json`, `.gitignore`, dossier `scripts/`.
- Premier script exécutable `scripts/inventaire.js`, testé et fonctionnel.

## Livré à la leçon 02 (07/08/2026)

- Ajout de `dossiers documents/` et `livrables/controles/` dans l'inventaire (écart n°1 résolu).
- Filtre sur les fichiers temporaires Office `~$…` dans `estLivrable()` (écart n°2 résolu).
- Création de `scripts/serveur.js` : serveur HTTP natif Node.js, route `/api/inventaire`, route
  statique avec garde-fou path traversal, lecture asynchrone `fs.readFile`.
- Création de `public/index.html` : grille responsive CSS, chargement des données via `fetch()`,
  gestion d'erreur réseau.

## Écarts spec / code résiduels (ouverts)

| # | Écart | Où le traiter |
|---|---|---|
| 3 | La date affichée dans les cartes est le `mtime` du fichier, alors que la spec impose la date contenue dans le NOM | leçon 06 (tri et filtres) |

## Reste à faire

3. TypeScript et structure de projet — typer Livrable et Categorie, compiler avec tsc
4. Données réelles côté serveur — mieux structurer la route API, ajouter la pagination
5. Interface — React ou Next.js (à décider)
6. Recherche et filtres
7. Persistance (base de données locale SQLite)
8. API et architecture
9. Qualité, tests, débogage
10. Sécurité et données (RGPD)
11. Mise en production
12. Maintenance et évolution

## Points en suspens

- **Périmètre tranché en leçon 01** : le portail couvre `livrables/lecons`, `livrables/quiz`,
  `livrables/infographies`, `sources/veille`, `livrables/documents`, `livrables/controles`.
  Extensions retenues : `.docx`, `.pptx`, `.pdf`, `.md`.
- **Poids des quiz** : essentiel du volume. À surveiller si on veut afficher des aperçus — hors périmètre v1.
- **Chemin racine en dur** : `scripts/serveur.js` et `inventaire.js` remontent de 4 niveaux depuis `__dirname`.
  Ça marche, mais ça casserait si le projet était déplacé. Dette assumée, à traiter en leçon 04 ou 08.
- **Port 3000 en dur** : acceptable pour l'usage local. En leçon 08, on lira PORT depuis une variable d'environnement.
- Le choix du framework d'interface (leçon 05) dépendra de ce que révèlent les leçons 03 et 04.
