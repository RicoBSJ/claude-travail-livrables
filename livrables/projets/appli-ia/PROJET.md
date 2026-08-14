# Projet fil rouge — « Portail Livrables »

> Mémoire du parcours **Développement d'applications avec l'IA** (12 leçons, vendredi 8h03).
> Le job `appli-ia-lecon` lit ce fichier au début de chaque leçon et le met à jour à la fin.
> **Ne pas supprimer** : sans lui, la continuité du fil rouge est perdue.

---

## État de l'application

**TypeScript en place — leçon 03 terminée (14/08/2026).**

Le Portail Livrables tourne toujours avec `node scripts/serveur.js` (JavaScript, port 3000).
Un couche TypeScript est désormais installée en parallèle : `npm run build` compile `src/`
vers `dist/`, et `node dist/inventaire.js` affiche l'inventaire complet en version typée.

**Écart n°4 résolu (14/08/2026)** : `README.md` est maintenant exclu de l'inventaire dans
`scripts/serveur.js` et `src/inventaire.ts`. La carte Contrôles affiche 1 fichier (et non 2).

**Inventaire lors de la compilation de test (14/08/2026)** : lecons 195 fichiers, quiz 19,
infographies 38, veilles (dossier), documents, controles 1.

TypeScript installé : version 7.0.2. @types/node : 26.2.0.

## Choix techniques arrêtés

| Élément | Choix | Décidé en |
|---|---|---|
| Langage | JavaScript (CommonJS) côté serveur/scripts + TypeScript côté `src/` | leçon 01 & 03 |
| Runtime | **Node.js v24 LTS** (LTS Active, vérifié nodejs.org le 14/08/2026) | leçon 01 |
| TypeScript | **7.0.2** (vérifié npm show le 14/08/2026) + @types/node 26.2.0 | leçon 03 |
| tsconfig | `target: ES2022`, `module: commonjs`, `strict: true`, sans `moduleResolution` (supprimé dans TS7) | leçon 03 |
| Serveur HTTP | Module natif `node:http` — sans framework | leçon 02 |
| Interface | HTML/CSS/JS vanilla — sans framework frontend (React/Vue à décider leçon 05) | leçon 02 |
| Framework d'interface | *à décider* | leçon 05 |
| Base de données | *à décider* | leçon 07 |

Aucune bibliothèque tierce n'est installée : c'est délibéré.

## Fichiers du projet

| Fichier | Rôle |
|---|---|
| `SPEC.md` | Spécification **v1.2** : problème, utilisateur, données, fonctions, hors périmètre, critère de réussite, journal des révisions |
| `package.json` | v0.3.0 · scripts `inventaire`, `demo-recursivite`, `serveur`, `build`, `inventaire:ts` · devDependencies typescript+@types/node |
| `tsconfig.json` | Configuration TypeScript : target ES2022, module commonjs, strict, types:[node], outDir ./dist, rootDir ./src |
| `.gitignore` | Exclut `node_modules/`, `.env`, `*.log`, `dist/`, `.DS_Store` |
| `scripts/inventaire.js` | Inventaire terminal (JavaScript) — 4 dossiers seulement (version d'origine). Lecture seule. |
| `scripts/demo_recursivite.js` | **Annexe pédagogique** — même logique qu'inventaire.js, commentée. `npm run demo-recursivite`. |
| `scripts/serveur.js` | Serveur HTTP local (port 3000). **Modifié leçon 03** : ajout DOCS_DE_DOSSIER — résout écart n°4. Lecture seule. |
| `src/types.ts` | **Nouveau leçon 03** — Interfaces : `Livrable`, `Categorie`, `Inventaire`, `DossierConfig`. Aucune logique. |
| `src/inventaire.ts` | **Nouveau leçon 03** — Version TypeScript de l'inventaire (6 dossiers, écart n°4 résolu). Compilé vers `dist/inventaire.js`. |
| `dist/` | **Généré par `npm run build`** — Ne pas éditer. Contient `.js`, `.d.ts`, `.js.map` pour chaque source de `src/`. |
| `public/index.html` | Page web du portail : grille de cartes, pied de page totaux. 29 lignes. |
| `public/style.css` | Feuille de style (94 lignes). Extraite d'index.html le 09/08/2026. |
| `public/app.js` | Point d'entrée (33 lignes) : orchestration. `type="module"`. |
| `public/api.js` | Accès aux données (21 lignes) : `chargerInventaire()`. Sans DOM. |
| `public/rendu.js` | Affichage (65 lignes) : `afficherStatut()`, `afficherCartes()`, `afficherTotaux()`. Sans réseau. |
| `exercices/` | Artefacts pédagogiques leçon 01 (deux scripts de listage + README). Hors application. |
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

## Ajouté hors leçon (08/08/2026)

Pied de page de totaux dans `public/index.html`, travaillé par l'apprenant puis corrigé
ensemble. Trois bugs rencontrés, instructifs pour la suite :

| Bug | Cause | Correction |
|---|---|---|
| `fetch("URL_DE_TON_API")` | placeholder jamais remplacé | supprimé — les données étaient déjà disponibles |
| `categorie.info?.nombre` | niveau `.info` inexistant dans l'API ; le `?.` masquait l'erreur au lieu de la signaler | `cat.nombre` |
| `querySelector("#footer")` | aucun élément ne portait cet id | `<div id="totaux">` ajouté, ciblé par `getElementById` |

Enseignement retenu : les données reçues par un `fetch` existant se réutilisent, plutôt que
de refaire un appel réseau pour la même chose.

**Format aligné le 09/08/2026** sur le critère de réussite du Challenge A de la leçon 02 :
le pied de page affiche désormais « N livrables · X,Y Mo — chargé à HH:MM:SS ». Deux points
de méthode au passage : l'heure est prise DANS le `.then()`, au moment où les données
arrivent réellement, et non au chargement de la page qui le précède ; et `#totaux` porte un
état initial « chargement… » plutôt qu'un vide silencieux si le serveur ne répond pas.

⚠️ À signaler pour les prochaines leçons : l'énoncé du Challenge A parlait de « somme des
`info.nombre` », en reprenant le nom d'une variable LOCALE de la boucle des cartes
(`const info = data[cle]`). Présenté ainsi, ce nom passe pour un niveau de la structure de
l'API — qui n'en comporte pas. C'est la cause directe du bug `categorie.info?.nombre`. Un
énoncé d'exercice doit décrire la FORME DES DONNÉES, pas emprunter un nom de variable au
code environnant.

## Séparation du CSS (09/08/2026)

Question posée par l'apprenant : pourquoi le CSS est-il dans le fichier HTML plutôt que dans un
fichier `.css` ? Réponse : c'était un choix de simplicité de la leçon 02 — défendable pour une
première page, mais périmé dès lors que le CSS représentait **41 % du fichier** (91 lignes sur 190).

Argument décisif relevé dans le code : `scripts/serveur.js` déclarait **déjà** le type MIME
`text/css` dans sa table `TYPES_MIME`. Le serveur était écrit prêt pour cette séparation — elle
n'avait simplement pas été franchie.

| | Avant | Après |
|---|---|---|
| `index.html` | 190 lignes | 100 lignes |
| `public/style.css` | — | 94 lignes |

Vérifié dans le navigateur après extraction : feuille chargée depuis `/style.css`, **17 règles CSS
appliquées**, type MIME `text/css; charset=utf-8` (et non `octet-stream`), rendu identique, garde-fou
path traversal toujours en 403, aucune erreur console.

## Séparation du JavaScript (09/08/2026)

Même démarche, poursuivie dans la foulée. Après l'extraction du CSS, le JavaScript représentait
**80 % du fichier restant** (71 lignes sur 100).

| | Au départ | Après CSS | Après JS |
|---|---|---|---|
| `index.html` | 190 lignes | 100 lignes | **29 lignes** |
| `public/style.css` | — | 94 lignes | 94 lignes |
| `public/app.js` | — | — | **80 lignes** |

`index.html` ne contient plus que de la structure : en-tête, zone principale avec deux conteneurs
vides, pied de page, et deux balises de liaison.

**Point technique consigné dans l'en-tête d'`app.js`** : la balise `<script src="/app.js">` reste en
FIN de `<body>`, à la place exacte du bloc inline. Cette position garantit que le HTML existe déjà
quand le script s'exécute — `document.getElementById()` trouve donc ses éléments. La déplacer dans
le `<head>` casserait tout, sauf à lui ajouter l'attribut `defer`.

Vérifié dans le navigateur : `app.js` et `style.css` chargés comme ressources externes, types MIME
corrects (`application/javascript` et `text/css`), 6 cartes construites, totaux calculés, garde-fou
path traversal en 403, aucune erreur console.

À enchaîner en leçon 03 (« TypeScript et **structure de projet** ») : les trois rôles sont désormais
dans trois fichiers. La question suivante est celle du découpage d'`app.js` lui-même, aujourd'hui
d'un seul bloc — et du typage des données qu'il manipule.

## Découpage d'app.js en modules (09/08/2026)

Troisième étape de séparation, demandée par l'apprenant dans la foulée des deux précédentes.
`app.js` faisait 80 lignes d'un seul bloc mélangeant réseau, DOM et orchestration.

**Réserve assumée** : 80 lignes ne *nécessitent* pas de modules. L'intérêt est pédagogique —
apprendre le découpage sur un cas maîtrisable plutôt que le découvrir sur 800 lignes. Le découpage
suit donc les vraies coutures fonctionnelles, pas un tranchage arbitraire.

| Fichier | Lignes | Responsabilité | Ce qu'il ignore délibérément |
|---|---|---|---|
| `api.js` | 21 | Parler au serveur | le DOM — il n'y touche jamais |
| `rendu.js` | 65 | Écrire dans la page | le réseau — aucun `fetch` |
| `app.js` | 33 | Orchestrer | *comment* les deux autres travaillent |

`app.js` se lit désormais comme un résumé de l'application : charger, afficher le statut, afficher
les cartes, afficher les totaux, et traiter l'erreur.

**Deux pièges documentés dans l'en-tête d'`app.js`** :
1. La balise doit porter `type="module"`, sinon le navigateur refuse `import` et `export`.
2. Les chemins d'import exigent l'extension : `"./api.js"` et non `"./api"`. Le navigateur ne la
   devine pas, contrairement à Node.js — source de confusion classique en passant de l'un à l'autre.

À noter : un module est différé (`defer`) par défaut, sa position en fin de `<body>` n'est donc plus
indispensable. Conservée quand même, elle reste correcte.

Vérifié dans le navigateur via le journal réseau : `/app.js` chargé, puis `/api.js` et `/rendu.js`
tirés en cascade par ses imports, puis `/api/inventaire`. 6 cartes construites, totaux calculés,
CSS appliqué, aucune erreur console.

**Choix de méthode** : le style `.then` a été conservé plutôt que converti en `async/await`. Une
seule chose à la fois — ce changement modularise, il ne réécrit pas. Mélanger les deux aurait rendu
la comparaison avant/après illisible. La conversion reste un candidat pour une leçon ultérieure.

## Écarts spec / code résiduels (ouverts)

| # | Écart | Où le traiter |
|---|---|---|
| 3 | La date affichée dans les cartes est le `mtime` du fichier, alors que la spec impose la date contenue dans le NOM | leçon 06 (tri et filtres) |
| 4 | ~~README.md compté comme livrable~~ **Résolu leçon 03** : ajout de DOCS_DE_DOSSIER dans serveur.js et src/inventaire.ts | ✅ |

## Livré à la leçon 03 (14/08/2026)

- Fix écart n°4 : ajout de `DOCS_DE_DOSSIER = ["readme.md"]` dans `scripts/serveur.js`.
- Création de `src/types.ts` : interfaces `Livrable`, `Categorie`, `Inventaire`, `DossierConfig`.
- Création de `src/inventaire.ts` : version TypeScript de l'inventaire (6 dossiers, écart n°4 inclus).
- Création de `tsconfig.json` : target ES2022, module commonjs, strict, types:[node].
- Mise à jour `package.json` v0.3.0 : scripts `build` et `inventaire:ts`, devDependencies.
- Installation de `typescript@7.0.2` et `@types/node@26.2.0` (2 packages, 0 vulnérabilités).
- Compilation réussie : `npm run build` → `dist/inventaire.js` fonctionnel.
- Point technique documenté : TypeScript 7 a supprimé `moduleResolution: "node"` (TS5108). Solution : retirer l'option de tsconfig.json.

## Reste à faire

4. Données réelles côté serveur — mieux structurer la route API, extraire la date du nom, pagination
5. Interface — React ou Next.js (à décider)
6. Recherche et filtres
7. Persistance (base de données locale SQLite)
8. API et architecture
9. Qualité, tests, débogage
10. Sécurité et données (RGPD)
11. Mise en production
12. Maintenance et évolution

## Points en suspens

- **9 livrables sans date dans leur nom** (constaté le 08/08/2026) : quiz, infographies et
  documents antérieurs à la convention `YYYY-MM-DD_`. Ce sont de VRAIS livrables — la spec v1.2
  tranche : ne pas les exclure, mais les signaler et les classer en fin de liste. À prévoir dans
  l'interface (leçon 06) : ils ne doivent pas disparaître d'un tri par date.

- **Périmètre tranché en leçon 01** : le portail couvre `livrables/lecons`, `livrables/quiz`,
  `livrables/infographies`, `sources/veille`, `livrables/documents`, `livrables/controles`.
  Extensions retenues : `.docx`, `.pptx`, `.pdf`, `.md`.
- **Poids des quiz** : essentiel du volume. À surveiller si on veut afficher des aperçus — hors périmètre v1.
- **Chemin racine en dur** : `scripts/serveur.js` et `inventaire.js` remontent de 4 niveaux depuis `__dirname`.
  Ça marche, mais ça casserait si le projet était déplacé. Dette assumée, à traiter en leçon 04 ou 08.
- **Port 3000 en dur** : acceptable pour l'usage local. En leçon 08, on lira PORT depuis une variable d'environnement.
- Le choix du framework d'interface (leçon 05) dépendra de ce que révèlent les leçons 03 et 04.
