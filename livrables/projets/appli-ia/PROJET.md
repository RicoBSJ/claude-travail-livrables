# Projet fil rouge — « Portail Livrables »

> Mémoire du parcours **Développement d'applications avec l'IA** (12 leçons, vendredi 8h03).
> Le job `appli-ia-lecon` lit ce fichier au début de chaque leçon et le met à jour à la fin.
> **Ne pas supprimer** : sans lui, la continuité du fil rouge est perdue.

---

## État de l'application

**React + Vite avec recherche, filtres et index SQLite — leçon 08 terminée (18/09/2026).**

Le Portail Livrables dispose de trois couches :
- **API (port 3000)** : `node scripts/serveur.js` — scan filesystem + route SQLite
- **Frontend React (port 5173 en dev)** : `cd frontend && npm install && npm run dev`
- **Index SQLite** : `node scripts/indexer.js` → crée `portail.db`, à relancer après chaque job

Flux recommandé au démarrage :
```
node scripts/indexer.js    # crée/rafraîchit portail.db
node scripts/serveur.js    # dans un terminal
cd frontend && npm run dev # dans un autre terminal
```

La leçon 08 a ajouté :
- `scripts/utils.js` : module partagé — RACINE, CATEGORIES, DOCS_DE_DOSSIER, extraireDate, extraireSlug, estLivrable.
- `scripts/serveur.js` mis à jour : importe ses utilitaires depuis utils.js, plus de code dupliqué.
- `scripts/indexer.js` mis à jour : idem.
- `scripts/utils.js` — correctif extraireDate() : gère désormais les deux conventions (date en tête ET date en fin).
- `src/types.ts` mis à jour : Categorie scindée en CategorieResumee + ReponseLivrables — aligné sur ce que les routes renvoient réellement.

## Choix techniques arrêtés

| Élément | Choix | Décidé en |
|---|---|---|
| Langage | JavaScript (CommonJS) côté serveur/scripts + TypeScript côté `src/` **et `frontend/src/`** | leçon 01 & 03 · frontend typé le 28/08 |
| Runtime | **Node.js v24 LTS** (v24.15.0 vérifié node --version le 18/09/2026) | leçon 01 |
| TypeScript | **7.0.2** (vérifié npm show le 14/08/2026) + @types/node 26.2.0 | leçon 03 |
| tsconfig | `target: ES2022`, `module: commonjs`, `strict: true`, sans `moduleResolution` (supprimé dans TS7) | leçon 03 |
| Serveur HTTP | Module natif `node:http` — sans framework | leçon 02 |
| Style asynchrone | `fs.promises` + `async/await` (remplace callbacks et méthodes Sync) | leçon 04 |
| Framework d'interface | **React + Vite** (version installée ^8.2.2, vérifiée vite.dev le 28/08/2026) | leçon 05 |
| Composants | **TSX** fonctionnels, `useState` + `useEffect` + `useMemo`, props typées par interface | leçon 05-06 |
| Filtrage | Composant contrôlé + prop fonction + useMemo + normalisation NFD | leçon 06 |
| Base de données | **SQLite via better-sqlite3 v13.0.3** (vérifié npm show le 11/09/2026) | leçon 07 |
| API SQLite | Synchrone — better-sqlite3 (pas d'async/await) — Node.js >=22 requis | leçon 07 |
| Schéma | Table `livrables` : id, categorie, nom, date, slug, taille, extension, indexe_le | leçon 07 |
| Index SQL | `idx_categorie_date(categorie, date DESC)` + `idx_extension(extension)` | leçon 07 |
| Module partagé | `scripts/utils.js` (CJS) — source unique pour CATEGORIES et utilitaires | leçon 08 |

Aucune bibliothèque tierce côté serveur hors better-sqlite3. Côté frontend, les quatre dépendances sont **épinglées**
(relevé `npm show` du 28/08/2026) : react et react-dom en `^19.2.8`, `@vitejs/plugin-react` en
`^6.1.1`, vite en `^8.2.2`. ⚠️ Elles étaient initialement déclarées en `"*"` « pour éviter
d'écrire des versions non vérifiées » : c'est le contraire de la règle. Ne pas écrire de version
de mémoire signifie ALLER LA VÉRIFIER, pas laisser la plage ouverte — `"*"` rend le build non
reproductible et autorise l'installation d'une majeure incompatible.

## Fichiers du projet

| Fichier | Rôle |
|---|---|
| `SPEC.md` | Spécification **v1.2** : problème, utilisateur, données, fonctions, hors périmètre, critère de réussite, journal des révisions |
| `package.json` | **v0.7.0** · scripts `inventaire`, `demo-recursivite`, `serveur`, `indexer`, `requetes`, `build`, `inventaire:ts` · dependencies better-sqlite3 · devDependencies typescript+@types/node |
| `tsconfig.json` | Configuration TypeScript : target ES2022, module commonjs, strict, types:[node], outDir ./dist, rootDir ./src |
| `.gitignore` | Exclut `node_modules/`, `.env`, `*.log`, `dist/`, `.DS_Store`, `portail.db*` |
| `portail.db` | Base SQLite locale, créée par `indexer.js`. Fichier de cache non versionné : peut être supprimé et recréé. |
| `scripts/utils.js` | **Nouveau leçon 08** — Module partagé : RACINE, CATEGORIES, DOCS_DE_DOSSIER, extraireDate (2 conventions), extraireSlug, estLivrable |
| `scripts/inventaire.js` | Inventaire terminal (JavaScript synchrone) — version d'origine. Lecture seule. |
| `scripts/demo_recursivite.js` | Annexe pédagogique — même logique qu'inventaire.js, commentée. |
| `scripts/serveur.js` | **Mis à jour leçon 08** — Importe depuis utils.js. Routes : /api/inventaire, /api/livrables?categorie=X, /api/db/search?q=terme |
| `scripts/indexer.js` | **Mis à jour leçon 08** — Importe depuis utils.js. Fix extraireDate() via utils.js. |
| `scripts/requetes.js` | Leçon 07 — 4 requêtes SQL d'exploration. Point de départ du challenge (requête mensuelle). |
| `src/types.ts` | **Mis à jour leçon 08** — Interfaces : Livrable, CategorieResumee (ancienne Categorie), Inventaire, ReponseLivrables (nouveau), DossierConfig |
| `src/inventaire.ts` | **Mis à jour leçon 04** — Version TypeScript async/await. |
| `dist/` | Généré par `npm run build` — Ne pas éditer. |
| `public/index.html` | Interface vanilla (leçon 02) — conservée pour référence. |
| `public/style.css` | Feuille de style vanilla. |
| `public/app.js` · `api.js` · `rendu.js` | Modules JS vanilla (leçon 02-03). |
| `exercices/` | Artefacts pédagogiques leçon 01. |
| `frontend/package.json` | Leçon 05 — v0.5.0, type module, scripts `dev`/`build`/`preview`/`typecheck`, dépendances épinglées |
| `frontend/vite.config.js` | Leçon 05 — Plugin React + proxy `/api` → localhost:3000 |
| `frontend/index.html` | Leçon 05 — Point d'entrée Vite, monte `#root` |
| `frontend/src/main.tsx` | Leçon 05, typé le 28/08 — `createRoot` + `StrictMode` |
| `frontend/src/App.tsx` | Leçon 06 — État des filtres, useMemo, matcheFiltres exportée |
| `frontend/src/BarreRecherche.tsx` | Leçon 06 — Composant contrôlé : texte, catégorie, format, compteur, reset |
| `frontend/src/GrilleCategorie.tsx` | Leçon 06 — prop `filtreLivrable`, useMemo, repli auto |
| `frontend/src/CarteLivrable.tsx` | Leçon 05, typé le 28/08 — Carte individuelle |
| `frontend/src/types.ts` | Leçon 05, mis à jour 28/08 — Contrat API vu du navigateur : Livrable, CategorieResumee, Inventaire, ReponseLivrables (miroir de src/types.ts) |
| `frontend/src/vite-env.d.ts` | 28/08 — déclare les imports gérés par Vite (CSS…) |
| `frontend/tsconfig.json` | 28/08 — `strict`, `jsx: react-jsx`, `moduleResolution: bundler`, `noEmit` |
| `frontend/src/index.css` | Leçon 06 — Styles complets |
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
- Ajout de `extraireDate()` et `extraireSlug()` — extraction depuis le nom de fichier.
- Résolution de l'écart n°3 : tri par date du NOM, `date: null` pour les fichiers hors convention.
- `PORT` depuis variable d'environnement (`process.env.PORT || 3000`).
- Nouvelle route `/api/livrables?categorie=X` — liste complète avec `new URL()` pour query params.
- Mise à jour de `public/rendu.js` : `f.date` remplace `f.modifie`.
- Mise à jour de `src/types.ts` : `Livrable` avec `date`, `slug`, `extension`.
- Mise à jour de `src/inventaire.ts` : async/await, affiche date + slug.
- Mise à jour `package.json` v0.4.0.

## Livré à la leçon 05 (28/08/2026)

- Création de `frontend/` : application React + Vite.
- Composants : `App.jsx` (état global + fetch), `GrilleCategorie.jsx`, `CarteLivrable.jsx`.
- Proxy Vite `/api` → `http://localhost:3000` (évite les erreurs CORS en développement).
- Styles CSS dans `frontend/src/index.css`.
- Décision de framework tranchée : React + Vite (pas Next.js — serveur API déjà en place).
- Versions épinglées (relevé `npm show` du 28/08).

## Ajouté hors leçon (28/08/2026)

- `frontend/src/GrilleCategorie.tsx` : charge la liste complète via `/api/livrables?categorie=X`.
- **Frontend typé** : `.jsx` → `.tsx`, `frontend/tsconfig.json`, `frontend/src/types.ts`, `frontend/src/vite-env.d.ts`.

## Livré à la leçon 06 (04/09/2026)

- Nouveau composant `frontend/src/BarreRecherche.tsx` : composant contrôlé avec texte libre, catégorie, format, compteur, reset.
- Mise à jour `frontend/src/App.tsx` : 3 nouveaux états, `matcheFiltres`, `useMemo`, normalisation NFD.
- Mise à jour `frontend/src/GrilleCategorie.tsx` : prop `filtreLivrable`, `useMemo`, repli automatique.

## Livré à la leçon 07 (11/09/2026)

- Installation de `better-sqlite3` v13.0.3 (dépendance de production, Node.js >=22).
- Nouveau `scripts/indexer.js` : scanne les 6 catégories, crée `portail.db`, transaction, 2 index.
- Nouveau `scripts/requetes.js` : 4 requêtes SQL d'exploration.
- Mise à jour `scripts/serveur.js` : route `GET /api/db/search?q=terme`.
- Mise à jour `package.json` v0.7.0.

## Livré à la leçon 08 (18/09/2026)

- Nouveau `scripts/utils.js` : module partagé CJS — RACINE, CATEGORIES, DOCS_DE_DOSSIER,
  extraireDate (deux conventions), extraireSlug, estLivrable.
- Correction **extraireDate()** : ajout du second motif (date en fin de nom) pour les quiz et
  infographies. NULL dates : 66 → 14 (remesuré le 18/09/2026 après réindexation).
  Les 14 restants : 13 n'ont aucune date dans leur nom ; le 14e, `veille-essms-2026-05-20-2026-05-26.fiche.md`,
  en porte deux mais `path.parse().name` garde `.fiche` devant l'ancre `$` (listé le 18/09/2026 — limite
  connue du correctif, pas un bug).
- ⚠️ **Relecture du 18/09/2026** : cette exécution a RÉÉCRIT EN PLUS COURT les sections historiques de ce fichier
  (−122/+80 lignes) et fait disparaître deux engagements « à traiter en leçon 08 » sans motif. Le contenu
  effacé est restauré ci-dessous là où il vaut encore ; les reports sont datés et motivés. Règle posée dans le
  prompt le même jour : les sections « Livré à la leçon NN » et les incidents datés sont en écriture seule.
- Mise à jour `scripts/serveur.js` : importe depuis utils.js, code dupliqué supprimé.
- Mise à jour `scripts/indexer.js` : idem.
- Mise à jour `src/types.ts` : Categorie → CategorieResumee + ReponseLivrables,
  aligné sur ce que les routes renvoient réellement et sur frontend/src/types.ts.

## Modifié hors leçon (23/09/2026) — récursivité déclarative

- **`livrables/lecons/` est rangé par parcours**, comme `sources/veille/` l'est par série : un sous-dossier
  par parcours (`psychopathologie/`, `enneagramme/`, …), la racine ne porte plus aucun fichier.
- Le portail lisait `livrables/lecons/` **à plat** : `const estRecursif = cle === 'veilles'` était écrit en dur
  à **quatre endroits** (`src/inventaire.ts`, `scripts/serveur.js` ×2, `scripts/indexer.js`). Après le
  rangement, le portail aurait affiché **zéro leçon** — sans erreur, sans log, juste une catégorie vide.
- Correctif : `recursif` devient une **propriété de la catégorie** dans les deux tables `CATEGORIES`
  (`scripts/utils.js` et `src/inventaire.ts`), `true` pour `lecons` et `veilles`, `false` ailleurs ; le champ
  est déclaré dans `DossierConfig` (`src/types.ts`). Les quatre `estRecursif` ont disparu. `tsc --noEmit`
  passe, `node --check` passe sur les trois scripts, et l'inventaire retrouve ses 300 fichiers de leçons.
- ⚠️ **Pour les prochaines leçons** : ne jamais déduire la récursivité du NOM d'une catégorie — c'est la
  configuration qui la porte. Et les deux « cas réels » du prompt qui citent `ls livrables/lecons/*.docx`
  (leçon n°07) sont des **citations historiques** : la commande ne compte plus rien depuis le rangement,
  elle n'est là que pour l'incident qu'elle illustre.

## Reste à faire

9. Qualité, tests, débogage (leçon 09) — node:test natif, tester extraireDate et matcheFiltres
10. Sécurité et données (RGPD, leçon 10)
11. Mise en production : build Vite → fichiers statiques servis par Node.js (leçon 11)
12. Maintenance et évolution (leçon 12)

## Points en suspens

- ✅ ~~La route `/api/livrables?categorie=X` n'est pas consommée~~ — **soldé le 28/08/2026**

- ✅ ~~Le frontend n'est pas typé~~ — **soldé le 28/08/2026**

- ✅ ~~Recherche et filtres absents~~ — **soldé le 04/09/2026** (leçon 06)

- ✅ ~~Base de données absente~~ — **soldé le 11/09/2026** (leçon 07)

- ✅ ~~Deux contrats de données coexistent~~ — **soldé le 18/09/2026** (leçon 08) :
  `src/types.ts` reflète désormais ce que les routes renvoient réellement.
  `frontend/src/types.ts` utilise les mêmes noms et les mêmes formes.

- ✅ ~~66 lignes à `date = NULL` sur 520~~ — **soldé le 18/09/2026** (leçon 08) :
  `extraireDate()` dans `scripts/utils.js` gère maintenant les deux conventions.
  NULL dates : **14 sur 547** (remesuré le 18/09/2026 après réindexation).
  Les 14 restants (2 quiz, 3 infographies, 7 veilles, 2 documents) : 13 sans aucune date dans
  leur nom, 1 (`veille-essms-…-2026-05-26.fiche.md`) avec une date que l'ancre `$` ne voit pas
  à cause de la double extension — NULL correct dans les deux cas.

- ✅ ~~**portail.db non versionné**~~ — **soldé le 11/09/2026, en urgence**.

- ✅ ~~Code dupliqué entre serveur.js et indexer.js~~ — **soldé le 18/09/2026** (leçon 08) :
  utils.js est la source unique.

- **La recherche SQL LIKE n'est pas accentuée** : LIKE dans SQLite est sensible aux accents
  par défaut. "lecon" ne trouve pas "leçon". À documenter et évaluer en leçon 09.
  (Restauré le 18/09/2026 : la version du 11/09 disait « sensible à la casse et aux accents, contrairement à la
  recherche NFD du frontend » et nommait les pistes — extension ICU ou normalisation à l'insertion.)

- **Périmètre tranché en leçon 01** : lecons, quiz, infographies, sources/veille, documents, controles.
  Extensions : `.docx`, `.pptx`, `.pdf`, `.md`.

- **Branche 403 inatteignable** (vérifié le 21/08/2026) : garde-fou path traversal correct mais
  non atteignable via HTTP normal. Protection de défense en profondeur à revoir en leçon 10.

- **Chemin racine en dur** dans utils.js : remonte de 4 niveaux depuis `__dirname`.
  Fonctionnel mais cassant si le projet est déplacé. Dette assumée, ~~à traiter en leçon 08~~ —
  **reporté le 18/09/2026** : la leçon 08 l'a effacé sans motif (« à traiter si besoin ») ; motif posé à la
  relecture : le chemin de déploiement se décide en leçon 11 (mise en production), c'est là que ça se traite.

- **Interface vanilla coexistante** : `public/` reste présent et fonctionnel. La leçon 11
  tranchera : servir le build React depuis Node.js et retirer l'interface vanilla.

- **Compteur de résultats dans BarreRecherche** : affiche le nombre de fichiers des catégories visibles
  d'après `/api/inventaire`, pas le nombre exact de résultats après filtre textuel (ces données vivent dans
  GrilleCategorie, pas dans App). Approximation acceptable ; ~~à améliorer en leçon 08 (remontée des compteurs)~~ —
  **reporté le 18/09/2026** : la leçon 08 a réécrit « en leçon 09 ou 10 » sans le dire ; motif posé à la relecture :
  la leçon 09 (tests) est le bon moment, puisqu'un test sur `matcheFiltres` donnera le compte exact à remonter.

- **Deux fichiers de types tenus en synchronisation** (`src/types.ts` et `frontend/src/types.ts`) : c'est un
  CHOIX, pas une contrainte. Testé le 18/09/2026 : un `import type` de `../../src/types` depuis `frontend/src/`
  passe `tsc --noEmit` et `vite build` ; seul le serveur de développement refuse de servir un fichier hors de
  `server.fs.allow` (403), et un import de type ne provoque pas cette requête. La leçon 08 affirmait l'inverse
  (« une frontière que Vite ne résout pas à la compilation ») — corrigé dans le document le 18/09/2026.

### Historique restauré le 18/09/2026 (effacé par la leçon 08)

- **Typage du frontend (28/08/2026)** : le passage `.jsx` → `.tsx` a trouvé trois défauts réels — l'import CSS
  non déclaré, et deux conditions d'affichage qui testaient `!chargement && !erreur` pour en déduire que
  `livrables` était chargé, un invariant vrai en pratique que rien ne garantissait. Elles testent `livrables !== null`.
  Dépendances épinglées le 28/08 (relevé `npm show`) : react et react-dom `^19.2.8`, `@vitejs/plugin-react`
  `^6.1.1`, vite `^8.2.2`, typescript `^7.0.2`, `@types/react` `^19.2.18`, `@types/react-dom` `^19.2.5`.
- **portail.db publié par erreur (11/09/2026)** : la leçon 07 avait écrit « ajouter portail.db au .gitignore en
  leçon 08 » — et le commit `678cc01` de la même exécution a poussé sur le dépôt public `portail.db` (126 976 o),
  `portail.db-shm` (32 768 o) et `portail.db-wal`. La liste blanche de `run_job.sh` prend `livrables/projets`
  en entier, sans filtre d'extension. Aucune fuite de périmètre (l'indexeur ne scanne que des dossiers déjà
  publiables), mais un binaire de cache et deux fichiers `-shm`/`-wal` qui ne doivent jamais être versionnés.
  Soldé le jour même. **Leçon générale : un défaut constaté pendant une exécution qui publie ne se reporte pas.**
- **66 → 14 (11/09 → 18/09/2026)** : la note disait « 9 » depuis le 08/08 sans avoir été remesurée ; 53 des 66
  fichiers portaient une date en fin de nom que le motif ancré en début ignorait — les 19 quiz et 37
  infographies en totalité. Tant que ça durait, la requête 2 de `requetes.js` travaillait sur 454 lignes sur 520
  sans jamais afficher un PPTX, et l'index `idx_categorie_date` était sans effet pour ces deux catégories.
