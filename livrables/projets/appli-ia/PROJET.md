# Projet fil rouge — « Portail Livrables »

> Mémoire du parcours **Développement d'applications avec l'IA** (12 leçons, vendredi 8h03).
> Le job `appli-ia-lecon` lit ce fichier au début de chaque leçon et le met à jour à la fin.
> **Ne pas supprimer** : sans lui, la continuité du fil rouge est perdue.

---

## État de l'application

**React + Vite opérationnel — leçon 05 terminée et documentée (28/08/2026).**

Le Portail Livrables dispose maintenant de deux couches distinctes :
- **API (port 3000)** : `node scripts/serveur.js` — inchangé depuis la leçon 04
- **Frontend React (port 5173 en dev)** : `cd frontend && npm install && npm run dev`

Le frontend React lit `/api/inventaire` via un proxy Vite et affiche les livrables en grille
de cartes React, par catégorie. La décision de framework est tranchée : **React + Vite**.

Interface vanilla (`public/`) toujours présente pour référence ; le frontend React la remplace
fonctionnellement. Les deux coexistent sans conflit.

## Choix techniques arrêtés

| Élément | Choix | Décidé en |
|---|---|---|
| Langage | JavaScript (CommonJS) côté serveur/scripts + TypeScript côté `src/` | leçon 01 & 03 |
| Runtime | **Node.js v24 LTS** (vérifié nodejs.org le 14/08/2026) | leçon 01 |
| TypeScript | **7.0.2** (vérifié npm show le 14/08/2026) + @types/node 26.2.0 | leçon 03 |
| tsconfig | `target: ES2022`, `module: commonjs`, `strict: true`, sans `moduleResolution` (supprimé dans TS7) | leçon 03 |
| Serveur HTTP | Module natif `node:http` — sans framework | leçon 02 |
| Style asynchrone | `fs.promises` + `async/await` (remplace callbacks et méthodes Sync) | leçon 04 |
| Framework d'interface | **React + Vite v8.2.2** (vérifié vite.dev le 28/08/2026) | leçon 05 |
| Composants | JSX fonctionnels, `useState` + `useEffect`, props immuables | leçon 05 |
| Base de données | *à décider leçon 07* | — |

Aucune bibliothèque tierce côté serveur. Côté frontend : React + react-dom + @vitejs/plugin-react
(versions résolues à `npm install` — `"*"` dans package.json pour éviter d'écrire des versions
non vérifiées). Vite v8.2.2 est la seule version explicitement vérifiée côté frontend.

## Fichiers du projet

| Fichier | Rôle |
|---|---|
| `SPEC.md` | Spécification **v1.2** : problème, utilisateur, données, fonctions, hors périmètre, critère de réussite, journal des révisions |
| `package.json` | **v0.4.0** · scripts `inventaire`, `demo-recursivite`, `serveur`, `build`, `inventaire:ts` · devDependencies typescript+@types/node |
| `tsconfig.json` | Configuration TypeScript : target ES2022, module commonjs, strict, types:[node], outDir ./dist, rootDir ./src |
| `.gitignore` | Exclut `node_modules/`, `.env`, `*.log`, `dist/`, `.DS_Store` |
| `scripts/inventaire.js` | Inventaire terminal (JavaScript synchrone) — version d'origine. Lecture seule. |
| `scripts/demo_recursivite.js` | Annexe pédagogique — même logique qu'inventaire.js, commentée. |
| `scripts/serveur.js` | **Mis à jour leçon 04** — Serveur HTTP local (port 3000). async/await, `extracterDate()`, `extraerSlug()`. Routes `/api/inventaire` + `/api/livrables?categorie=X`. |
| `src/types.ts` | **Mis à jour leçon 04** — Interface `Livrable` enrichie (date, slug, extension). |
| `src/inventaire.ts` | **Mis à jour leçon 04** — Version TypeScript async/await. |
| `dist/` | Généré par `npm run build` — Ne pas éditer. |
| `public/index.html` | Interface vanilla (leçon 02) — conservée pour référence. |
| `public/style.css` | Feuille de style vanilla. |
| `public/app.js` · `api.js` · `rendu.js` | Modules JS vanilla (leçon 02-03). |
| `exercices/` | Artefacts pédagogiques leçon 01. |
| `frontend/package.json` | **Nouveau leçon 05** — v0.5.0, type module, scripts dev/build/preview, Vite ^8.2.2 |
| `frontend/vite.config.js` | **Nouveau leçon 05** — Plugin React + proxy `/api` → localhost:3000 |
| `frontend/index.html` | **Nouveau leçon 05** — Point d'entrée Vite, monte `#root` |
| `frontend/src/main.jsx` | **Nouveau leçon 05** — `createRoot` + `StrictMode` |
| `frontend/src/App.jsx` | **Nouveau leçon 05** — Composant racine : fetch `/api/inventaire`, 3 états (inventaire/chargement/erreur) |
| `frontend/src/GrilleCategorie.jsx` | **Nouveau leçon 05** — Affiche une catégorie + ses fichiers récents |
| `frontend/src/CarteLivrable.jsx` | **Nouveau leçon 05** — Carte individuelle : ext, slug, date (ou null), taille |
| `frontend/src/index.css` | **Nouveau leçon 05** — Styles React : portail, en-tête, grille de cartes |
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

## Livré à la leçon 05 (28/08/2026)

- Création de `frontend/` : application React + Vite v8.2.2.
- Composants : `App.jsx` (état global + fetch), `GrilleCategorie.jsx`, `CarteLivrable.jsx`.
- Proxy Vite `/api` → `http://localhost:3000` (évite les erreurs CORS en développement).
- Styles CSS dans `frontend/src/index.css` (grille responsive, cartes, badges d'extension).
- Décision de framework tranchée : React + Vite (pas Next.js — serveur API déjà en place).
- Note versions : Vite ^8.2.2 vérifiée ; React version résolue à `npm install` (non épinglée).

## Reste à faire

6. Recherche et filtres : champ de texte, filtres par catégorie et extension (leçon 06)
7. Persistance (SQLite, leçon 07)
8. API et architecture (leçon 08)
9. Qualité, tests, débogage (leçon 09)
10. Sécurité et données (RGPD, leçon 10)
11. Mise en production : build Vite → fichiers statiques servis par Node.js (leçon 11)
12. Maintenance et évolution (leçon 12)

## Points en suspens

- **9 livrables sans date dans leur nom** (constaté le 08/08/2026) : quiz, infographies et
  documents antérieurs à la convention `YYYY-MM-DD_`. La spec v1.2 tranche : ne pas les exclure,
  les signaler (`date: null`) et les classer en fin de liste. Traité côté interface en leçon 06.

- **Périmètre tranché en leçon 01** : lecons, quiz, infographies, sources/veille, documents, controles.
  Extensions : `.docx`, `.pptx`, `.pdf`, `.md`.

- **Branche 403 inatteignable** (vérifié le 21/08/2026) : garde-fou path traversal correct mais
  non atteignable via HTTP normal. Protection de défense en profondeur à revoir en leçon 10.

- **Chemin racine en dur** : tous les scripts remontent de 4 niveaux depuis `__dirname`.
  Fonctionnel mais cassant si le projet est déplacé. Dette assumée, à traiter en leçon 08.

- **Versions React non épinglées** : `package.json` de frontend/ utilise `"*"` pour react et
  react-dom — la version installée dépend de la date d'installation. À figer en leçon 11 (mise
  en production) une fois que les versions sont connues et validées.

- **Interface vanilla coexistante** : `public/` reste présent et fonctionnel. Le port 3000
  sert encore les fichiers statiques vanilla si on navigue sur http://localhost:3000. La leçon 11
  tranchera : servir le build React depuis le serveur Node.js et retirer l'interface vanilla.
