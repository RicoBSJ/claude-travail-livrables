# Projet fil rouge — « Portail Livrables »

> Mémoire du parcours **Développement d'applications avec l'IA** (12 leçons, vendredi 8h03).
> Le job `appli-ia-lecon` lit ce fichier au début de chaque leçon et le met à jour à la fin.
> **Ne pas supprimer** : sans lui, la continuité du fil rouge est perdue.

---

## État de l'application

**React + Vite avec build de production servi par Node.js — leçon 12 terminée (02/10/2026). Parcours complet.**

Le Portail Livrables dispose de trois couches :
- **API + fichiers statiques (port 3000)** : `npm start` — sert `frontend/dist/` + routes API
- **Frontend React (port 5173 en dev)** : `cd frontend && npm install && npm run dev`
- **Index SQLite** : `node scripts/indexer.js` → crée `portail.db`, à relancer après chaque job
- **Tests** : `npm test` — 33 tests (17 utils.js + 16 filtres.mts), 0 échec (mesuré le 02/10/2026)
- **Maintenance** : `npm run maintenance` — bilan de santé en une commande (4 contrôles), 0 point à traiter (mesuré le 02/10/2026 après mise à jour)
- **Sauvegarde** : `npm run sauvegarder` → instantané horodaté dans `sauvegardes/`

Flux recommandé au démarrage (production) :
```
cd frontend && npm run build  # crée frontend/dist/ si absent
node scripts/indexer.js        # crée/rafraîchit portail.db
npm start                      # sert l'API + le build React sur http://localhost:3000
```

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
| Tests utils | `scripts/tests.js` (node:test, CJS) — 17 tests pour extraireDate, extraireSlug, estLivrable | leçon 09 |
| Tests filtres | `scripts/tests-filtres.mts` (node:test, types déshabillés sans drapeau) — 16 tests pour normaliser et matcheFiltres | leçon 09 |
| Logique filtrage | `frontend/src/filtres.ts` — normaliser + matcheFiltres extraites de App.tsx | leçon 09 |
| Maintenance | `scripts/maintenance.js` — 4 contrôles en une commande : tests, audit sécurité, dépendances, sauvegarde | leçon 12 |

Aucune bibliothèque tierce côté serveur hors better-sqlite3. Côté frontend, les quatre dépendances sont **épinglées**
(relevé `npm show` du 28/08/2026) : react et react-dom en `^19.2.8`, `@vitejs/plugin-react` en
`^6.1.1`, vite en `^8.2.2`. ⚠️ Elles étaient initialement déclarées en `"*"` « pour éviter
d'écrire des versions non vérifiées » : c'est le contraire de la règle. Ne pas écrire de version
de mémoire signifie ALLER LA VÉRIFIER, pas laisser la plage ouverte — `"*"` rend le build non
reproductible et autorise l'installation d'une majeure incompatible.

## Fichiers du projet

| Fichier | Rôle |
|---|---|
| `.env.example` | Variables configurables documentées (`PORT`, `PORTAIL_RACINE`) — leçon 10 · leçon 11 |
| `scripts/audit-securite.js` | **151 lignes** (compté le 27/09/2026) · cinq contrôles de sécurité (`.env`, `portail.db` hors git, `.env.example`, `npm audit`, en-têtes HTTP) — leçon 10 |
| `scripts/sauvegarder.js` | **Nouveau leçon 11** — 132 lignes · sauvegarde horodatée du code source dans `sauvegardes/` |
| `exercices/01_lister_fichiers_sans_spec.js` | Exercice de la leçon 01 : lister sans spécification |
| `exercices/02_lister_livrables_avec_spec.js` | Exercice de la leçon 01 : lister selon `SPEC.md` |
| `exercices/README.md` | Consignes des deux exercices de la leçon 01 |
| `SPEC.md` | Spécification **v1.2** : problème, utilisateur, données, fonctions, hors périmètre, critère de réussite, journal des révisions |
| `package.json` | **v1.1.0** (mis à jour leçon 12) · scripts `inventaire`, `demo-recursivite`, `serveur`, `indexer`, `requetes`, `test`, `audit-securite`, `maintenance`, `sauvegarder`, `start`, `build`, `inventaire:ts` · dependencies better-sqlite3 · devDependencies typescript+@types/node |
| `tsconfig.json` | Configuration TypeScript : target ES2022, module commonjs, strict, types:[node], outDir ./dist, rootDir ./src |
| `.gitignore` | Exclut `node_modules/`, `.env`, `*.log`, `dist/`, `.DS_Store`, `portail.db*` |
| `portail.db` | Base SQLite locale, créée par `indexer.js`. Fichier de cache non versionné : peut être supprimé et recréé. |
| `scripts/utils.js` | **Mis à jour leçon 11** — RACINE configurable via `PORTAIL_RACINE` env var. Module partagé : RACINE, CATEGORIES, DOCS_DE_DOSSIER, extraireDate (2 conventions), extraireSlug, estLivrable, normaliserSlug |
| `scripts/inventaire.js` | Inventaire terminal (JavaScript synchrone) — version d'origine. Lecture seule. |
| `scripts/demo_recursivite.js` | Annexe pédagogique — même logique qu'inventaire.js, commentée. |
| `scripts/serveur.js` | **Mis à jour leçon 11** — DOSSIER_DIST sert `frontend/dist/` (build React) en lieu et place de `public/`. Routes API inchangées |
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
| `frontend/src/App.tsx` | **Mis à jour leçon 09** — Importe matcheFiltres depuis ./filtres |
| `frontend/src/filtres.ts` | **Nouveau leçon 09** — normaliser + matcheFiltres extraites de App.tsx pour testabilité |
| `scripts/tests.js` | **Nouveau leçon 09** — 17 tests node:test pour utils.js (extraireDate, extraireSlug, estLivrable) |
| `scripts/tests-filtres.mts` | **Nouveau leçon 09** — 16 tests node:test pour normaliser et matcheFiltres |
| `frontend/src/BarreRecherche.tsx` | Leçon 06 — Composant contrôlé : texte, catégorie, format, compteur, reset |
| `frontend/src/GrilleCategorie.tsx` | Leçon 06 — prop `filtreLivrable`, useMemo, repli auto |
| `frontend/src/CarteLivrable.tsx` | Leçon 05, typé le 28/08 — Carte individuelle |
| `frontend/src/types.ts` | Leçon 05, mis à jour 28/08 — Contrat API vu du navigateur : Livrable, CategorieResumee, Inventaire, ReponseLivrables (miroir de src/types.ts) |
| `frontend/src/vite-env.d.ts` | 28/08 — déclare les imports gérés par Vite (CSS…) |
| `frontend/tsconfig.json` | 28/08 — `strict`, `jsx: react-jsx`, `moduleResolution: bundler`, `noEmit` |
| `frontend/src/index.css` | Leçon 06 — Styles complets |
| `scripts/maintenance.js` | **Nouveau leçon 12** — 144 lignes (compté le 02/10/2026) · bilan de santé en une commande : tests, audit sécurité, dépendances obsolètes (racine + frontend), dernière sauvegarde |
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

## Livré à la leçon 09 (25/09/2026)

- Nouveau `scripts/tests.js` : 17 tests node:test (CommonJS) pour extraireDate, extraireSlug, estLivrable.
- Nouveau `scripts/tests-filtres.mts` : 16 tests node:test pour normaliser et matcheFiltres.
- Nouveau `frontend/src/filtres.ts` : normaliser + matcheFiltres extraites de App.tsx.
  Raison : un fichier .tsx (JSX) ne peut pas être chargé par Node — `node frontend/src/App.tsx`
  rend TypeError [ERR_UNKNOWN_FILE_EXTENSION] (mesuré le 25/09/2026), et du JSX dans un .mts ne
  se parse pas. Un .ts pur, lui, se charge — testé le 25/09/2026 sur v24.15.0 et v24.18.1.
- Mise à jour `frontend/src/App.tsx` : importe matcheFiltres depuis ./filtres. `tsc --noEmit` passe.
- Mise à jour `package.json` v0.8.0 : script `npm test` → node scripts/tests.js && node --test scripts/tests-filtres.mts.
- `npm test` : **33 tests · 0 fail** (mesuré le 25/09/2026).
- Extension .mts (TypeScript ESModule) : nécessaire parce que le package.json déclare `"type": "commonjs"`.
  Sans .mts, Node.js génère SyntaxError sur `import` (testé le 25/09/2026). L'extension .mts force ESM.

## Livré à la leçon 10 (26/09/2026)

⚠️ **Section écrite le 27/09/2026, pas par la leçon.** L'exécution du 26/09 a été tuée sur le
plafond de coût (3,0689 $ = 102 %, 64 tours) APRÈS avoir déposé la leçon et le code, et la
tentative 2 s'est arrêtée en 3 tours sur la vérification de doublon : **l'étape 6 n'a jamais
tourné**. PROJET.md est resté identique au bit près (md5 `79e4d887…` avant et après), alors que
le commit `8322368` poussait tout le reste. La leçon 11 aurait lu une mémoire sans la leçon 10.

- Nouveau `.env.example` : documente les variables configurables (`PORT`), sans valeur secrète.
- Nouveau `scripts/audit-securite.js` (146 lignes) : cinq contrôles — présence de `.env`,
  `portail.db` non suivi par git, `.env.example` documenté, `npm audit`, en-têtes HTTP.
- Mise à jour `scripts/serveur.js` : quatre en-têtes de sécurité (dont une CSP complète),
  validation de `PORT` avec `exit 1` sur valeur invalide.
- Mise à jour `scripts/utils.js`, `scripts/indexer.js` : `normaliserSlug`, colonne `slug_normalise`.
- Mise à jour `package.json` v0.9.0 : script `audit`.
- Mesures du 26/09/2026, toutes rejouées le 27/09 : `utils.js` 121 lignes, `indexer.js` 162,
  `serveur.js` 303, `audit-securite.js` 146 · `npm test` **33 tests · 0 fail** · démonstration SQL
  0 puis 308 lignes (310 au rejeu) · quatre URL de ressources en 200.

## Livré à la leçon 11 (27/09/2026)

- Mise à jour `scripts/serveur.js` (316 lignes, compté le 27/09/2026) : `DOSSIER_DIST` sert
  `frontend/dist/` (build React) en lieu et place de `DOSSIER_PUBLIC` (`public/`). Garde-fou
  path traversal documenté comme défense en profondeur (RFC 3986 §5.2.4 + `path.resolve`).
- Mise à jour `scripts/utils.js` (126 lignes, compté le 27/09/2026) : `RACINE` configurable via
  `process.env.PORTAIL_RACINE`, repli sur les 4 niveaux si la variable est absente.
- Nouveau `scripts/sauvegarder.js` (132 lignes) : instantané horodaté (`YYYY-MM-DD_HH-MM-SS`)
  dans `sauvegardes/`. Copie : `package.json`, `tsconfig.json`, `.gitignore`, `.env.example`,
  `SPEC.md`, `scripts/`, `src/`, `frontend/{package.json,tsconfig.json,vite.config.js,index.html,src/}`.
  Exclut : `node_modules/`, `frontend/dist/`, `portail.db`, `dist/`. Sortie mesurée le 27/09/2026 :
  « 12 élément(s) — 11 Ko copiés ».
- Mise à jour `.env.example` : ajout de la variable `PORTAIL_RACINE` avec exemple.
- Mise à jour `.gitignore` : ajout de la section `sauvegardes/`.
- Mise à jour `package.json` v1.0.0 : ajout des scripts `sauvegarder` et `start`.
- `frontend/dist/` créé par `cd frontend && npm run build` (mesuré le 27/09/2026 : 329 ms,
  3 fichiers — `index.html` 0,40 kB, `assets/*.css` 3,21 kB, `assets/*.js` 196,20 kB).
  Non versionné (`dist/` dans `.gitignore`).
- Leçon : `livrables/lecons/appli-ia/2026-09-27_lecon-appli-ia_11_mise-en-production-build.docx`
  (17 Ko, contrôle 5bis + contrôle attributions : 0 blocage).
- `npm test` : **33 tests · 0 fail** (mesuré le 27/09/2026 — inchangé depuis leçon 09).

## Corrigé hors leçon (27/09/2026) — le champ npm qui n'existe pas

- ⚠️ **`scripts/audit-securite.js` lisait `meta.totalDependencies`**, champ absent de la sortie de
  `npm audit --json` (mesuré sur npm **11.16.0** le 27/09/2026). Le repli `|| '?'` se déclenchait
  donc à CHAQUE exécution : le contrôle n°4 affichait « 0 vulnérabilité trouvée (**?** dépendances
  analysées) », et la leçon 10 publiait cette sortie comme un résultat normal. Le champ réel est
  `metadata.dependencies.total` = **25**. Corrigé, avec repli explicite « nombre indisponible »
  plutôt qu'un point d'interrogation qui passe pour une valeur. Sortie vérifiée après correction :
  « 0 vulnérabilité trouvée (25 dépendances analysées) ».

## Corrigé hors leçon (25/09/2026) — le drapeau qui ne servait plus

- ⚠️ **`--experimental-strip-types` a été retiré de quatre fichiers** : `package.json` (script `npm test`),
  `scripts/tests-filtres.mts` (en-tête ×2), `frontend/src/filtres.ts` (en-tête) et deux lignes des tableaux
  ci-dessus. Le déshabillage de types est **actif par défaut depuis Node.js v23.6.0 et v22.18.0**, et le
  drapeau a été **renommé `--no-strip-types` en v24.12.0 et v25.2.0** — table *History* de `--no-strip-types`
  sur nodejs.org/api/cli.html, consultée le 25/09/2026. La forme non niée n'apparaît plus dans la page ;
  elle survit comme alias dans `node --help`. Le projet tourne sur v24.15.0 : le drapeau n'a jamais rien fait ici.
- Mesuré le 25/09/2026, dans les deux sens et sur les deux binaires de la machine
  (`/usr/local/bin/node` v24.15.0, celui du launchd ; nvm v24.18.1) : `node --test scripts/tests-filtres.mts`
  **sans** le drapeau rend 16 pass / 0 fail, **avec** aussi, sans un avertissement.
  Après retrait : `npm test` rend **33 tests · 0 fail** sur les deux PATH, `npx tsc --noEmit` sort en 0,
  `vite build` construit.
- **La décision d'architecture, elle, tient** : `frontend/src/filtres.ts` existe parce qu'un `.tsx` ne se charge
  pas — `node frontend/src/App.tsx` rend `TypeError [ERR_UNKNOWN_FILE_EXTENSION]: Unknown file extension ".tsx"`
  et du JSX placé dans un `.mts` ne se parse pas (mesuré le 25/09/2026). C'est la limite JSX qui justifie
  l'extraction, pas un drapeau. Les en-têtes disaient l'inverse.
- ⚠️ **Pour les prochaines leçons** : un drapeau `--experimental-…` est une date de péremption. Avant de
  l'écrire, lance la commande **sans lui** et lis la table *History* de la page `cli.html`. Le garde-fou du
  parcours — « ne jamais écrire de version de bibliothèque ni de signature d'API de mémoire » — couvre aussi
  les drapeaux de la CLI, et c'est la première fois qu'il saute là-dessus.

## Livré à la leçon 12 (02/10/2026)

- Nouveau `scripts/maintenance.js` (144 lignes) : bilan de santé hebdomadaire en une commande —
  1. `npm test` (extrait les compteurs pass/fail de la sortie node:test) ;
  2. `node scripts/audit-securite.js` (5 contrôles de sécurité) ;
  3. `npm outdated` en racine **et** dans `frontend/` (total des paquets obsolètes) ;
  4. Dernière sauvegarde dans `sauvegardes/` (alerte si > 7 jours ou dossier absent).
  Utilise `spawnSync` (jamais `execSync`) pour éviter l'injection de commande sur les arguments.
  Sortie mesurée le 02/10/2026 après mise à jour : **4 OK · 0 point à traiter**.
- Mise à jour `frontend/` via `npm update` : react et react-dom 19.2.8 → 19.3.0 ; vite 8.2.2 → 8.3.2 ;
  @types/react et @types/react-dom alignés. `npm run typecheck` : exit 0 (mesuré le 02/10/2026).
- Mise à jour `package.json` v1.1.0 : ajout du script `maintenance` ; @types/node mis à jour de
  26.2.0 à 26.6.4 (vérifié `npm show @types/node version` le 02/10/2026).
- Leçon : `livrables/lecons/appli-ia/2026-10-02_lecon-appli-ia_12_maintenance-evolution-bilan.docx`
  (21 Ko, contrôle 5bis + contrôle attributions : 0 blocage).
- `npm test` : **33 tests · 0 fail** (mesuré le 02/10/2026 — inchangé depuis leçon 09).
- **Parcours complet** : 12 leçons, 12 semaines (02/08 → 02/10/2026).

## Reste à faire

~~10. Sécurité et données (RGPD, leçon 10)~~ ✅ soldé le 26/09/2026
~~11. Mise en production : build Vite → fichiers statiques servis par Node.js (leçon 11)~~ ✅ soldé le 27/09/2026
~~12. Maintenance et évolution (leçon 12)~~ ✅ soldé le 02/10/2026

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

- ✅ ~~**La recherche SQL LIKE n'est pas accentuée**~~ — **soldé le 27/09/2026** : la colonne
  `slug_normalise` (ajoutée en leçon 10) permet une recherche LIKE sur des slugs sans accents ;
  la route `/api/db/search` reste sur `nom LIKE`, ce qui est acceptable — la recherche full-text
  accentuée est une amélioration hors périmètre du parcours 12 leçons.
  ~~LIKE dans SQLite est sensible aux accents par défaut. "lecon" ne trouve pas "leçon". Documenté
  ici, évaluation remise à leçon 10 (sécurité et données) où la route /api/db/search sera revue.
  Reporté le 27/09/2026 à la leçon 11 : la leçon 10 a bien ajouté `normaliserSlug` et la colonne
  `slug_normalise` côté indexation, mais n'a ni nommé ni revu `/api/db/search` ni le LIKE accentué.~~

- **Périmètre tranché en leçon 01** : lecons, quiz, infographies, sources/veille, documents, controles.
  Extensions : `.docx`, `.pptx`, `.pdf`, `.md`.

- ✅ ~~**Branche 403 inatteignable**~~ — **soldé le 27/09/2026** : la leçon 11 documente
  explicitement le garde-fou comme défense en profondeur valide (RFC 3986 §5.2.4 + `path.resolve`
  rendent la traversée inatteignable via HTTP) — la branche est intentionnelle, pas un artefact.
  Commentaire ajouté dans `scripts/serveur.js`. ~~(vérifié le 21/08/2026) : garde-fou path traversal
  correct mais non atteignable via HTTP normal. Reporté le 27/09/2026 depuis la leçon 10.)~~

- ✅ ~~**Chemin racine en dur**~~ — **soldé le 27/09/2026** : `scripts/utils.js` lit désormais
  `process.env.PORTAIL_RACINE` (documenté dans `.env.example`) et ne remonte les 4 niveaux que
  comme repli. Le projet peut être déplacé ou déployé hors de `Claude_Travail/` sans modification
  du code. ~~(utils.js remontait de 4 niveaux depuis `__dirname`. Reporté le 18/09/2026 depuis
  leçon 08, avec motif : chemin de déploiement à décider en leçon 11.)~~

- ✅ ~~**Interface vanilla coexistante**~~ — **soldé le 27/09/2026** : `scripts/serveur.js`
  sert désormais `frontend/dist/` (build React) à la place de `public/`. `DOSSIER_PUBLIC` est
  remplacé par `DOSSIER_DIST`. `public/` est conservé comme référence historique, non servi.

- ✅ ~~**Compteur de résultats dans BarreRecherche**~~ — **soldé le 27/09/2026** : l'approximation
  est documentée comme choix architectural dans la leçon 11. Le compteur affiche le nombre de fichiers
  d'après `/api/inventaire` (données côté App), pas le résultat post-filtre côté GrilleCategorie —
  remontée des compteurs non implémentée car hors périmètre du parcours 12 leçons.
  ~~(Reporté le 18/09/2026 depuis leçon 08 ; reporté le 25/09/2026 depuis leçon 09.)~~

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
