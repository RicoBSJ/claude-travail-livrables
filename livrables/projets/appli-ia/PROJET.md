# Projet fil rouge — « Portail Livrables »

> Mémoire du parcours **Développement d'applications avec l'IA** (12 leçons, vendredi 8h03).
> Le job `appli-ia-lecon` lit ce fichier au début de chaque leçon et le met à jour à la fin.
> **Ne pas supprimer** : sans lui, la continuité du fil rouge est perdue.

---

## État de l'application

**React + Vite avec recherche, filtres et index SQLite — leçon 07 terminée (11/09/2026).**

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

La leçon 07 a ajouté :
- `scripts/indexer.js` : scanne les 6 catégories et insère les livrables dans `portail.db` via transaction SQLite.
- `scripts/requetes.js` : 4 requêtes SQL d'exploration (totaux, récents, recherche LIKE, formats).
- Route `/api/db/search?q=terme` dans `serveur.js` : recherche textuelle SQL avec LIKE sur `portail.db`.
- `better-sqlite3` v13.0.3 installé comme dépendance de production.
- `package.json` v0.7.0 : scripts `indexer` et `requetes` ajoutés.

## Choix techniques arrêtés

| Élément | Choix | Décidé en |
|---|---|---|
| Langage | JavaScript (CommonJS) côté serveur/scripts + TypeScript côté `src/` **et `frontend/src/`** | leçon 01 & 03 · frontend typé le 28/08 |
| Runtime | **Node.js v24 LTS** (vérifié nodejs.org le 14/08/2026) | leçon 01 |
| TypeScript | **7.0.2** (vérifié npm show le 14/08/2026) + @types/node 26.2.0 | leçon 03 |
| tsconfig | `target: ES2022`, `module: commonjs`, `strict: true`, sans `moduleResolution` (supprimé dans TS7) | leçon 03 |
| Serveur HTTP | Module natif `node:http` — sans framework | leçon 02 |
| Style asynchrone | `fs.promises` + `async/await` (remplace callbacks et méthodes Sync) | leçon 04 |
| Framework d'interface | **React + Vite v8.2.2** (vérifié vite.dev le 28/08/2026) | leçon 05 |
| Composants | **TSX** fonctionnels, `useState` + `useEffect` + `useMemo`, props typées par interface | leçon 05-06 |
| Filtrage | Composant contrôlé + prop fonction + useMemo + normalisation NFD | leçon 06 |
| Base de données | **SQLite via better-sqlite3 v13.0.3** (vérifié npm show le 11/09/2026) | leçon 07 |
| API SQLite | Synchrone — better-sqlite3 (pas d'async/await) — Node.js >=22 requis | leçon 07 |
| Schéma | Table `livrables` : id, categorie, nom, date, slug, taille, extension, indexe_le | leçon 07 |
| Index SQL | `idx_categorie_date(categorie, date DESC)` + `idx_extension(extension)` | leçon 07 |

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
| `.gitignore` | Exclut `node_modules/`, `.env`, `*.log`, `dist/`, `.DS_Store` |
| `portail.db` | **Nouveau leçon 07** — Base SQLite locale, créée par `indexer.js`. Fichier de cache : peut être supprimé et recréé à tout moment. |
| `scripts/inventaire.js` | Inventaire terminal (JavaScript synchrone) — version d'origine. Lecture seule. |
| `scripts/demo_recursivite.js` | Annexe pédagogique — même logique qu'inventaire.js, commentée. |
| `scripts/serveur.js` | **Mis à jour leçon 07** — Serveur HTTP local (port 3000). Routes : /api/inventaire, /api/livrables?categorie=X, /api/db/search?q=terme (SQLite). |
| `scripts/indexer.js` | **Nouveau leçon 07** — Scanne les 6 catégories et insère dans portail.db. Schema DROP+CREATE, transaction, 2 index. |
| `scripts/requetes.js` | **Nouveau leçon 07** — 4 requêtes SQL d'exploration. Ouvert en readonly. Point d'entrée du challenge (requête mensuelle). |
| `src/types.ts` | **Mis à jour leçon 04** — Interface `Livrable` enrichie (date, slug, extension). |
| `src/inventaire.ts` | **Mis à jour leçon 04** — Version TypeScript async/await. |
| `dist/` | Généré par `npm run build` — Ne pas éditer. |
| `public/index.html` | Interface vanilla (leçon 02) — conservée pour référence. |
| `public/style.css` | Feuille de style vanilla. |
| `public/app.js` · `api.js` · `rendu.js` | Modules JS vanilla (leçon 02-03). |
| `exercices/` | Artefacts pédagogiques leçon 01. |
| `frontend/package.json` | Leçon 05 — v0.5.0, type module, scripts `dev`/`build`/`preview`/`typecheck`, dépendances épinglées |
| `frontend/vite.config.js` | **Nouveau leçon 05** — Plugin React + proxy `/api` → localhost:3000 |
| `frontend/index.html` | **Nouveau leçon 05** — Point d'entrée Vite, monte `#root` |
| `frontend/src/main.tsx` | Leçon 05, typé le 28/08 — `createRoot` + `StrictMode`, garde explicite sur `#root` |
| `frontend/src/App.tsx` | **Mis à jour leçon 06** — Composant racine : état des filtres (recherche, catégorieActive, extensionActive), useMemo sur categoriesVisibles et totalFichiers, fonction matcheFiltres exportée |
| `frontend/src/BarreRecherche.tsx` | **Nouveau leçon 06** — Composant contrôlé : champ texte + 2 <select> + compteur résultats + bouton reset |
| `frontend/src/GrilleCategorie.tsx` | **Mis à jour leçon 06** — reçoit prop `filtreLivrable`, applique useMemo sur la liste filtrée, useEffect pour replier quand le filtre change |
| `frontend/src/CarteLivrable.tsx` | Leçon 05, typé le 28/08 — Carte individuelle : ext, slug, date (ou null), taille |
| `frontend/src/types.ts` | **Nouveau 28/08** — contrat de l'API vu du navigateur : `Livrable`, `CategorieResumee`, `Inventaire`, `ReponseLivrables` |
| `frontend/src/vite-env.d.ts` | **Nouveau 28/08** — déclare les imports gérés par Vite (CSS…) |
| `frontend/tsconfig.json` | **Nouveau 28/08** — `strict`, `jsx: react-jsx`, `moduleResolution: bundler`, `noEmit` |
| `frontend/src/index.css` | **Mis à jour leçon 06** — Ajout styles `.barre-recherche`, `.barre-label`, `.barre-input`, `.barre-select`, `.barre-resultats`, `.barre-reset` |
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

- Création de `frontend/` : application React + Vite v8.2.2.
- Composants : `App.jsx` (état global + fetch), `GrilleCategorie.jsx`, `CarteLivrable.jsx`.
- Proxy Vite `/api` → `http://localhost:3000` (évite les erreurs CORS en développement).
- Styles CSS dans `frontend/src/index.css` (grille responsive, cartes, badges d'extension).
- Décision de framework tranchée : React + Vite (pas Next.js — serveur API déjà en place).
- Versions : vite `^8.2.2` (vérifiée vite.dev le 28/08). react, react-dom `^19.2.8` et
  `@vitejs/plugin-react` `^6.1.1` — d'abord laissées en `"*"`, épinglées le 28/08 après
  relecture (`npm show`).

## Ajouté hors leçon (28/08/2026)

- `frontend/src/GrilleCategorie.tsx` : charge la liste complète de sa catégorie via
  `/api/livrables?categorie=X` (route créée en leçon 04, jusque-là inutilisée). Quatre
  états locaux — `livrables`, `chargement`, `erreur`, `deplie` — un `useEffect` avec la
  dépendance `[nomCle]` et sa fonction de nettoyage, et un état **dérivé** pour les
  cartes visibles. Dépliage à partir de `APERCU = 12` cartes.
- `frontend/src/index.css` : styles `.statut-categorie` et `.bouton-deplier`.
- `frontend/package.json` : dépendances épinglées — react et react-dom `^19.2.8`,
  `@vitejs/plugin-react` `^6.1.1`, vite `^8.2.2` (relevé `npm show` du 28/08).
- **Frontend typé** : `.jsx` → `.tsx`, ajout de `frontend/tsconfig.json`
  (`strict: true`, `jsx: react-jsx`, `moduleResolution: bundler`),
  `frontend/src/types.ts` (contrat de l'API vu du navigateur) et
  `frontend/src/vite-env.d.ts` (déclare les imports CSS). Dépendances ajoutées :
  typescript `^7.0.2` — la même version que côté serveur —, `@types/react` `^19.2.18`,
  `@types/react-dom` `^19.2.5`. Script `typecheck` ajouté et branché dans `build`.
- Le typage a trouvé trois défauts réels : l'import CSS non déclaré, et surtout deux
  conditions d'affichage qui testaient `!chargement && !erreur` pour en déduire que
  `livrables` était chargé — un invariant vrai en pratique, que rien dans le code ne
  garantissait. Elles testent maintenant `livrables !== null`.

## Livré à la leçon 06 (04/09/2026)

- Nouveau composant `frontend/src/BarreRecherche.tsx` : composant contrôlé avec champ de texte libre,
  menu Catégorie, menu Format (extension), compteur de résultats, bouton « Effacer les filtres ».
- Mise à jour `frontend/src/App.tsx` : 3 nouveaux états (`recherche`, `categorieActive`, `extensionActive`),
  fonction `matcheFiltres` (exportée, testable), `useMemo` sur `categoriesVisibles` et `totalFichiers`,
  normalisation NFD pour la recherche insensible aux accents.
- Mise à jour `frontend/src/GrilleCategorie.tsx` : nouvelle prop `filtreLivrable: (livrable: Livrable) => boolean`,
  `useMemo` sur la liste filtrée, `useEffect([filtreLivrable])` pour replier automatiquement quand le filtre change,
  masquage de la section entière si aucun résultat.
- Mise à jour `frontend/src/index.css` : styles `.barre-recherche`, `.barre-input`, `.barre-select`,
  `.barre-resultats`, `.barre-reset`.

## Livré à la leçon 07 (11/09/2026)

- Installation de `better-sqlite3` v13.0.3 (dépendance de production, Node.js >=22).
- Nouveau `scripts/indexer.js` : scanne les 6 catégories en synchrone, crée `portail.db`,
  insère les livrables en transaction, crée `idx_categorie_date` et `idx_extension`.
- Nouveau `scripts/requetes.js` : 4 requêtes SQL d'exploration, ouvert en readonly.
  Contient le point de départ du challenge (requête mensuelle à compléter).
- Mise à jour `scripts/serveur.js` : import de `better-sqlite3`, constante `DB_PATH`,
  nouvelle route `GET /api/db/search?q=terme` avec validation du terme, gestion d'erreur
  distinguant "base absente" et "erreur SQL".
- Mise à jour `package.json` v0.7.0 : scripts `indexer` et `requetes`, dependency `better-sqlite3`.
- Indexation initiale : 519 fichiers indexés (au 11/09/2026) — lecons 269, veilles 177,
  infographies 37, quiz 19, documents 13, controles 4.

## Reste à faire

8. API et architecture (leçon 08) — réconcilier les deux contrats de types, refactoriser le serveur
9. Qualité, tests, débogage (leçon 09)
10. Sécurité et données (RGPD, leçon 10)
11. Mise en production : build Vite → fichiers statiques servis par Node.js (leçon 11)
12. Maintenance et évolution (leçon 12)

## Points en suspens

- ✅ ~~La route `/api/livrables?categorie=X` n'est pas consommée~~ — **soldé le 28/08/2026**

- ✅ ~~Le frontend n'est pas typé~~ — **soldé le 28/08/2026**

- ✅ ~~Recherche et filtres absents~~ — **soldé le 04/09/2026** (leçon 06)

- ✅ ~~Base de données absente~~ — **soldé le 11/09/2026** (leçon 07) : portail.db créé,
  route `/api/db/search` exposée.

- ⚠️ **Deux contrats de données coexistent** (constaté le 28/08/2026 en typant le
  frontend). `src/types.ts` déclare `Categorie` avec `recents` ET `livrables`
  obligatoires — or aucune route ne renvoie cette forme : `/api/inventaire` omet
  `livrables`, et `/api/livrables` renvoie une enveloppe `{ categorie, nombre,
  livrables }`. Le frontend a donc son propre `frontend/src/types.ts`, qui décrit ce qui
  circule réellement. **À réconcilier en leçon 08** (API et architecture).

- **66 lignes à `date = NULL` sur 520** (remesuré le 11/09/2026 — la note disait « 9 » depuis
  le 08/08/2026, sans avoir jamais été revérifiée). Le diagnostic d'origine était faux, pas
  seulement le chiffre : **53 de ces 66 fichiers PORTENT une date dans leur nom**, simplement pas
  en tête. Les quiz et les infographies suivent la convention `quiz_[type]_[slug]_YYYY-MM-DD.pptx`
  prescrite par CLAUDE.md — date en **fin** de nom — tandis que `extraireDate()` n'ancre que le
  début (`/^(\d{4}-\d{2}-\d{2})/`). Ce sont donc **les 19 quiz et les 37 infographies en
  totalité** qui basculent à `NULL`, par construction du motif et non par ancienneté. Seuls **13**
  fichiers n'ont réellement aucune date, dont 6 notes `_dossier.fiche.md` qui n'en ont pas à avoir.
  La spec v1.2 tranche : ne pas les exclure, les signaler (`date: null`) et les classer en fin de
  liste. Traité côté interface depuis leçon 05.
  **Conséquences à traiter en leçon 08** : la requête 2 de `requetes.js` (`WHERE date IS NOT NULL`)
  travaille sur **454 lignes sur 520** et n'affichera jamais un quiz ni une infographie ; le
  Challenge « 3 mois les plus productifs » calcule une productivité dont tous les PPTX sont absents ;
  et l'index `idx_categorie_date` est sans effet pour ces deux catégories. Le correctif est un
  second motif dans `extraireDate()` (date en fin de nom), pas une exclusion.

- **Périmètre tranché en leçon 01** : lecons, quiz, infographies, sources/veille, documents, controles.
  Extensions : `.docx`, `.pptx`, `.pdf`, `.md`.

- **Branche 403 inatteignable** (vérifié le 21/08/2026) : garde-fou path traversal correct mais
  non atteignable via HTTP normal. Protection de défense en profondeur à revoir en leçon 10.

- **Chemin racine en dur** : tous les scripts remontent de 4 niveaux depuis `__dirname`.
  Fonctionnel mais cassant si le projet est déplacé. Dette assumée, à traiter en leçon 08.

- **Interface vanilla coexistante** : `public/` reste présent et fonctionnel. Le port 3000
  sert encore les fichiers statiques vanilla si on navigue sur http://localhost:3000. La leçon 11
  tranchera : servir le build React depuis le serveur Node.js et retirer l'interface vanilla.

- **Compteur de résultats dans BarreRecherche** : affiche le nombre de fichiers dans les
  catégories visibles d'après les compteurs de `/api/inventaire`, pas le nombre exact de
  résultats après filtre textuel (ces données vivent dans GrilleCategorie, pas dans App).
  Approximation acceptable en l'état ; à améliorer en leçon 08 (remontée des compteurs).

- ✅ ~~**portail.db non versionné** : ajouter `portail.db` au `.gitignore` en leçon 08~~ —
  **soldé le 11/09/2026, en urgence**. La leçon 07 avait posé le diagnostic ET reporté le correctif
  d'une semaine : entre les deux, l'auto-push du job a publié sur le dépôt public `portail.db`
  (126 976 o), `portail.db-shm` (32 768 o) et `portail.db-wal` (commit `678cc01`). La liste blanche
  de `run_job.sh` prend `livrables/projets` en entier, sans filtre d'extension. Aucune fuite de
  périmètre — l'indexeur ne scanne que les six dossiers déjà publiables — mais un binaire de cache
  produit un diff illisible chaque semaine, et les fichiers `-shm`/`-wal` ne doivent jamais être
  versionnés. Les trois sont désormais dans le `.gitignore` du projet et retirés du suivi.
  **Leçon générale : un défaut constaté pendant une exécution qui publie ne se reporte pas.**

- **La recherche SQL LIKE n'est pas accentuée** : contrairement à la recherche NFD du frontend,
  LIKE dans SQLite est sensible à la casse et aux accents par défaut. "lecon" ne trouve pas "leçon".
  À noter comme limite documentée ; une solution (extension ICU ou normalisation à l'insertion)
  sera évaluée en leçon 09.
