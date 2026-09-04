# Projet fil rouge — « Portail Livrables »

> Mémoire du parcours **Développement d'applications avec l'IA** (12 leçons, vendredi 8h03).
> Le job `appli-ia-lecon` lit ce fichier au début de chaque leçon et le met à jour à la fin.
> **Ne pas supprimer** : sans lui, la continuité du fil rouge est perdue.

---

## État de l'application

**React + Vite avec recherche et filtres — leçon 06 terminée et documentée (04/09/2026).**

> **Corrigé le 04/09/2026, après relecture.** La variable de la liste filtrée s'appelait `livrablesFiltes`
> (sans le « r ») dans `GrilleCategorie.tsx` — dix occurrences, plus un commentaire qui l'orthographiait encore
> autrement. Le fichier compilait et `npm run typecheck` passait : un identifiant mal orthographié mais cohérent
> avec lui-même échappe à TypeScript comme au lint. Renommé en `livrablesFiltres`, dans le code et dans la leçon.
> Le commentaire annonçant « 232 leçons » comptait en réalité les fichiers de la catégorie — l'inventaire indexe
> `.docx` et `.md`, donc les fiches Obsidian : 125 leçons pour 125 fiches au 04/09/2026. `package.json` passe
> par ailleurs en 0.6.0, resté en 0.5.0 depuis la leçon 05.

Le Portail Livrables dispose de deux couches distinctes :
- **API (port 3000)** : `node scripts/serveur.js` — inchangé depuis la leçon 04
- **Frontend React (port 5173 en dev)** : `cd frontend && npm install && npm run dev`

Le frontend React affiche désormais une barre de recherche + filtres par catégorie et extension.
La logique de filtrage est centralisée dans `App.tsx` (composant contrôlé) et transmise à
`GrilleCategorie.tsx` via une prop de type fonction (`filtreLivrable`). Le filtrage en mémoire
utilise `useMemo` pour éviter les recalculs inutiles. La normalisation NFD rend la recherche
insensible aux accents (« lecon » trouve « leçon »).

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
| Base de données | *à décider leçon 07* | — |

Aucune bibliothèque tierce côté serveur. Côté frontend, les quatre dépendances sont **épinglées**
(relevé `npm show` du 28/08/2026) : react et react-dom en `^19.2.8`, `@vitejs/plugin-react` en
`^6.1.1`, vite en `^8.2.2`. ⚠️ Elles étaient initialement déclarées en `"*"` « pour éviter
d'écrire des versions non vérifiées » : c'est le contraire de la règle. Ne pas écrire de version
de mémoire signifie ALLER LA VÉRIFIER, pas laisser la plage ouverte — `"*"` rend le build non
reproductible et autorise l'installation d'une majeure incompatible.

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
- Vérifié : `npm run typecheck` au vert, `npm run build` passe (18 modules, vite 8.2.2),
  le portail se charge sans erreur console — 6 catégories, 462 fichiers, 232 leçons après
  dépliage, 25 fichiers en « date inconnue ».

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

## Reste à faire

7. Persistance (SQLite, leçon 07)
8. API et architecture (leçon 08)
9. Qualité, tests, débogage (leçon 09)
10. Sécurité et données (RGPD, leçon 10)
11. Mise en production : build Vite → fichiers statiques servis par Node.js (leçon 11)
12. Maintenance et évolution (leçon 12)

## Points en suspens

- ✅ ~~La route `/api/livrables?categorie=X` n'est pas consommée~~ — **soldé le 28/08/2026**
  (voir « Ajouté hors leçon » ci-dessus). `GrilleCategorie.tsx` charge la liste complète de
  sa catégorie ; la leçon 06 partira donc de données complètes.

- ✅ ~~Le frontend n'est pas typé~~ — **soldé le 28/08/2026** : `frontend/src/` est en
  `.tsx`, `strict: true`, `npm run typecheck` au vert et intégré au `build`.

- ✅ ~~Recherche et filtres absents~~ — **soldé le 04/09/2026** (leçon 06) : barre de
  recherche textuelle (NFD), filtres catégorie et extension, useMemo, prop fonction.

- ⚠️ **Deux contrats de données coexistent** (constaté le 28/08/2026 en typant le
  frontend). `src/types.ts` déclare `Categorie` avec `recents` ET `livrables`
  obligatoires — or aucune route ne renvoie cette forme : `/api/inventaire` omet
  `livrables`, et `/api/livrables` renvoie une enveloppe `{ categorie, nombre,
  livrables }`. Le frontend a donc son propre `frontend/src/types.ts`, qui décrit ce qui
  circule réellement. **À réconcilier en leçon 08** (API et architecture) : le contrat
  devrait être unique et partagé.

- **9 livrables sans date dans leur nom** (constaté le 08/08/2026) : quiz, infographies et
  documents antérieurs à la convention `YYYY-MM-DD_`. La spec v1.2 tranche : ne pas les exclure,
  les signaler (`date: null`) et les classer en fin de liste. Traité côté interface depuis leçon 05.

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
  Approximation acceptable en l'état ; à améliorer si on remonte les compteurs vers App
  en leçon 08.
