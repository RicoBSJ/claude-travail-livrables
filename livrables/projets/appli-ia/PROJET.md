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
| `SPEC.md` | Spécification **v1.2** : problème, utilisateur, données, fonctions, hors périmètre, critère de réussite, journal des révisions |
| `package.json` | Métadonnées du projet, scripts `inventaire`, `demo-recursivite` et `serveur`, `engines.node >= 24`, `private: true` |
| `.gitignore` | Exclut `node_modules/`, `.env`, `*.log`, `dist/`, `.DS_Store` |
| `scripts/inventaire.js` | Parcours récursif des dossiers de livrables, inventaire par catégorie — sortie terminal. **Lecture seule.** |
| `scripts/demo_recursivite.js` | **Annexe pédagogique** — même logique qu'inventaire.js, mais commente chaque appel de la fonction. Lancé par `npm run demo-recursivite`. |
| `scripts/serveur.js` | Serveur HTTP local (port 3000). Route `/api/inventaire` → JSON. Routes statiques → fichiers de `public/`. Garde-fou path traversal inclus. **Lecture seule.** Créé le 07/08/2026. |
| `public/index.html` | Première page web du portail : grille de cartes par catégorie, chargement dynamique via `fetch('/api/inventaire')`. Créé le 07/08/2026. **Enrichi le 08/08** d'un pied de page affichant les totaux (nombre de livrables et poids en Mo), calculés dans le `.then()` existant via `Object.values(data).reduce(...)` — sans second appel réseau. |
| `public/style.css` | Feuille de style du portail (94 lignes) : variables CSS, grille responsive, cartes, badges. **Extraite d'index.html le 09/08/2026** — le CSS y représentait 41 % du fichier. |
| `public/app.js` | **Point d'entrée** (33 lignes) : orchestre les étapes, sans savoir comment elles sont réalisées. Chargé par `<script src="/app.js" type="module">` en fin de `<body>`. |
| `public/api.js` | **Accès aux données** (21 lignes) : `chargerInventaire()`. Ne touche JAMAIS au DOM — réutilisable tel quel dans une autre page. |
| `public/rendu.js` | **Affichage** (65 lignes) : `afficherStatut()`, `afficherCartes()`, `afficherTotaux()`. Ne fait AUCUN appel réseau — contrepartie exacte d'api.js. |
| `exercices/` | **Artefacts pédagogiques**, hors application. Contient le Challenge de la leçon 01 (deux scripts de listage : sans spec puis avec spec) et son README explicatif. Créé le 08/08/2026. |
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
| 4 | `README.md` est compté comme un livrable dans `scripts/serveur.js`, alors que `SPEC.md` v1.2 l'exclut explicitement (« un fichier qui décrit un dossier n'en est pas un livrable »). Visible sur le portail : la carte *Controles* affiche 2 fichiers au lieu de 1. Ouvert le 08/08/2026. | **leçon 03** |

## Reste à faire

3. TypeScript et structure de projet — typer Livrable et Categorie, compiler avec tsc. **Traiter au passage l'écart n°4** : aligner `estLivrable()` de `scripts/serveur.js` sur la spec v1.2 en excluant les fichiers de documentation de dossier. Le filtre existe déjà dans `exercices/02_lister_livrables_avec_spec.js` (constante `DOCS_DE_DOSSIER`) et peut servir de référence — c'est un bon premier cas de typage : que vaut la liste des exclusions, et comment la typer proprement ?
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
