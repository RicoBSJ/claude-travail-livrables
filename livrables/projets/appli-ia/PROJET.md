# Projet fil rouge — « Portail Livrables »

> Mémoire du parcours **Développement d'applications avec l'IA** (12 leçons, vendredi 8h03).
> Le job `appli-ia-lecon` lit ce fichier au début de chaque leçon et le met à jour à la fin.
> **Ne pas supprimer** : sans lui, la continuité du fil rouge est perdue.

---

## État de l'application

**async/await en place, API enrichie — leçon 04 terminée et documentée (21/08/2026).**

Le Portail Livrables tourne avec `node scripts/serveur.js` (port 3000, configurable via `PORT=N`).
L'API expose désormais deux routes :
- `/api/inventaire` — inventaire complet compatible avec le frontend (leçons 1-3)
- `/api/livrables?categorie=X` — liste complète d'une catégorie (nouveau leçon 04)

Chaque livrable retourné par l'API contient maintenant `{ nom, date, slug, taille, extension }`.

**Écart n°3 résolu (21/08/2026)** : la date affichée dans les cartes provient désormais du
NOM du fichier (`extracterDate()`), et non du `mtime`. Les fichiers hors convention ont
`date: null` — ils sont inclus dans l'inventaire, triés en fin de liste.

**TypeScript** : `src/inventaire.ts` réécrit en async/await, `src/types.ts` mis à jour
(Livrable enrichi : date, slug, extension). `npm run build && npm run inventaire:ts` reste fonctionnel.

**Inventaire lors de la compilation de référence (14/08/2026)** : lecons 195 fichiers, quiz 19,
infographies 38, veilles (dossier récursif), documents, controles 1.

## Choix techniques arrêtés

| Élément | Choix | Décidé en |
|---|---|---|
| Langage | JavaScript (CommonJS) côté serveur/scripts + TypeScript côté `src/` | leçon 01 & 03 |
| Runtime | **Node.js v24 LTS** (vérifié nodejs.org le 14/08/2026) | leçon 01 |
| TypeScript | **7.0.2** (vérifié npm show le 14/08/2026) + @types/node 26.2.0 | leçon 03 |
| tsconfig | `target: ES2022`, `module: commonjs`, `strict: true`, sans `moduleResolution` (supprimé dans TS7) | leçon 03 |
| Serveur HTTP | Module natif `node:http` — sans framework | leçon 02 |
| Style asynchrone | `fs.promises` + `async/await` (remplace callbacks et méthodes Sync) | leçon 04 |
| Interface | HTML/CSS/JS vanilla — sans framework frontend (React/Vue à décider leçon 05) | leçon 02 |
| Framework d'interface | *à décider leçon 05* | — |
| Base de données | *à décider leçon 07* | — |

Aucune bibliothèque tierce n'est installée (devDependencies TypeScript uniquement) : c'est délibéré.

## Fichiers du projet

| Fichier | Rôle |
|---|---|
| `SPEC.md` | Spécification **v1.2** : problème, utilisateur, données, fonctions, hors périmètre, critère de réussite, journal des révisions |
| `package.json` | **v0.4.0** · scripts `inventaire`, `demo-recursivite`, `serveur`, `build`, `inventaire:ts` · devDependencies typescript+@types/node |
| `tsconfig.json` | Configuration TypeScript : target ES2022, module commonjs, strict, types:[node], outDir ./dist, rootDir ./src |
| `.gitignore` | Exclut `node_modules/`, `.env`, `*.log`, `dist/`, `.DS_Store` |
| `scripts/inventaire.js` | Inventaire terminal (JavaScript synchrone) — version d'origine. Lecture seule. |
| `scripts/demo_recursivite.js` | Annexe pédagogique — même logique qu'inventaire.js, commentée. |
| `scripts/serveur.js` | **Mis à jour leçon 04** — Serveur HTTP local (port 3000, `PORT` depuis env). async/await, `extracterDate()`, `extraerSlug()`. Route `/api/inventaire` (compat) + route `/api/livrables?categorie=X` (nouveau). |
| `src/types.ts` | **Mis à jour leçon 04** — Interface `Livrable` enrichie (date, slug, extension). `Categorie` avec `livrables[]` complets. |
| `src/inventaire.ts` | **Mis à jour leçon 04** — Version TypeScript async/await, extrait date + slug, affiche les 3 premiers avec date et slug. |
| `dist/` | Généré par `npm run build` — Ne pas éditer. |
| `public/index.html` | Page web du portail : grille de cartes, pied de page totaux. |
| `public/style.css` | Feuille de style (94 lignes). |
| `public/app.js` | Orchestration (`type="module"`). |
| `public/api.js` | Accès aux données : `chargerInventaire()` → `/api/inventaire`. |
| `public/rendu.js` | **Mis à jour leçon 04** — `f.date` remplace `f.modifie` (écart n°3 résolu). |
| `exercices/` | Artefacts pédagogiques leçon 01. Hors application. |
| `PROJET.md` | Ce fichier — mémoire du parcours |

## Livré à la leçon 01 (02/08/2026)

- Vérification de l'environnement (Node, npm, git).
- Rédaction de `SPEC.md`.
- Initialisation du dépôt : `package.json`, `.gitignore`, dossier `scripts/`.
- Premier script exécutable `scripts/inventaire.js`.

## Livré à la leçon 02 (07/08/2026)

- Ajout de `documents/` et `livrables/controles/` dans l'inventaire (écart n°1 résolu).
- Filtre `~$…` dans `estLivrable()` (écart n°2 résolu).
- Création de `scripts/serveur.js` v1 : serveur HTTP natif, route `/api/inventaire`, fichiers statiques.
- Création de `public/index.html` : grille CSS, `fetch()`, gestion d'erreur réseau.

## Ajouté hors leçon (08-09/08/2026)

- Pied de page totaux dans `public/index.html`.
- Séparation CSS → `public/style.css`.
- Séparation JS → `public/app.js`, `public/api.js`, `public/rendu.js` (modules ES).
- `app.js` refactorisé en trois modules (api / rendu / app).

## Livré à la leçon 03 (14/08/2026)

- Fix écart n°4 : `DOCS_DE_DOSSIER = ["readme.md"]` dans `scripts/serveur.js`.
- Création de `src/types.ts` : interfaces `Livrable`, `Categorie`, `Inventaire`, `DossierConfig`.
- Création de `src/inventaire.ts` : version TypeScript de l'inventaire.
- Création de `tsconfig.json` : target ES2022, module commonjs, strict.
- Mise à jour `package.json` v0.3.0.
- Installation typescript@7.0.2 et @types/node@26.2.0.
- Point technique : TypeScript 7 a supprimé `moduleResolution: "node"` (TS5108).

## Livré à la leçon 04 (21/08/2026)

- Réécriture de `scripts/serveur.js` en `fs.promises` + async/await.
- Ajout de `extracterDate()` et `extraerSlug()` — extraction depuis le nom de fichier.
- Résolution de l'écart n°3 : tri par date du NOM, `date: null` pour les fichiers hors convention.
- `PORT` depuis variable d'environnement (`process.env.PORT || 3000`).
- Nouvelle route `/api/livrables?categorie=X` — liste complète avec `new URL()` pour query params.
- Mise à jour de `public/rendu.js` : `f.date` remplace `f.modifie`.
- Mise à jour de `src/types.ts` : `Livrable` avec `date`, `slug`, `extension`.
- Mise à jour de `src/inventaire.ts` : async/await, affiche date + slug.
- Mise à jour `package.json` v0.4.0.

## Reste à faire

5. Interface — React ou Next.js (à décider leçon 05) — consommera `/api/livrables?categorie=X`
6. Recherche et filtres (leçon 06)
7. Persistance (SQLite, leçon 07)
8. API et architecture (leçon 08)
9. Qualité, tests, débogage (leçon 09)
10. Sécurité et données (RGPD, leçon 10)
11. Mise en production (leçon 11)
12. Maintenance et évolution (leçon 12)

## Points en suspens

- **9 livrables sans date dans leur nom** (constaté le 08/08/2026) : quiz, infographies et
  documents antérieurs à la convention `YYYY-MM-DD_`. La spec v1.2 tranche : ne pas les exclure,
  les signaler (`date: null`) et les classer en fin de liste. À traiter côté interface (leçon 06).

- **Périmètre tranché en leçon 01** : lecons, quiz, infographies, sources/veille, documents, controles.
  Extensions : `.docx`, `.pptx`, `.pdf`, `.md`.

- **Chemin racine en dur** : tous les scripts remontent de 4 niveaux depuis `__dirname`.
  Fonctionnel mais cassant si le projet est déplacé. Dette assumée, à traiter en leçon 08.

- **Le choix du framework d'interface** (leçon 05) dépendra des besoins révélés par les leçons 03 et 04.
