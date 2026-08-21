---
type: fiche-document
source: 2026-08-21_lecon-appli-ia_04_donnees-reelles-api-serveur.docx
date_creation: 2026-08-21
date_lecon: 2026-08-21
parcours: appli-ia
numero: 4
statut: parcours-actif
tags:
  - parcours/appli-ia
  - registre/pro
  - techno/node
  - techno/fs-promises
  - notion/async-await
  - notion/regex
  - notion/query-params
  - notion/variable-environnement
  - projet/portail-livrables
  - alerte/livrable-defectueux
---

# 2026-08-21_lecon-appli-ia_04_donnees-reelles-api-serveur

Document source : [[2026-08-21_lecon-appli-ia_04_donnees-reelles-api-serveur.docx]]

## Résumé

⚠️ **Le fichier `.docx` est défectueux — voir le dernier paragraphe.** Le résumé ci-dessous porte sur ce que le document contient réellement.

Leçon de bascule vers les **données réelles**. Quatre acquis : réécrire le serveur en `async/await` avec `node:fs/promises`, extraire date et slug **depuis le nom du fichier** par regex, lire les query params avec la classe `URL`, et exposer une route ciblée `/api/livrables?categorie=X`. Au passage, **l'écart n°3 est résolu** — la date affichée venait du `mtime`, elle vient désormais du nom, comme la spec l'exigeait. Il était planifié pour la leçon 06 : il arrive deux séances plus tôt.

**Le meilleur passage tient dans une valeur `null`.** Les fichiers antérieurs à la convention de nommage n'ont pas de date extractible : le code renvoie `date: null` et la spec demande de les **inclure, pas de les masquer**. La leçon en tire la bonne règle — *les données réelles ont des exceptions, et un code qui prétend que tous les fichiers ont une date est fragile*. Le `null` explicite rend les cas hors convention visibles plutôt que silencieux. Même logique pour le port, sorti du code en variable d'environnement (`PORT=8080 node scripts/serveur.js`), présenté comme la porte d'entrée du `.env` de la leçon 10.

Les trois pièges IA sont les plus utilisables du parcours jusqu'ici, parce qu'ils donnent le **symptôme** et pas seulement la règle : `require("node:fs")` suivi d'un `await fs.readdir()` ne lève aucune erreur, il retourne `undefined` — donc si un `await` rend `undefined` là où un tableau est attendu, c'est le mauvais module qui est chargé. Et `new URL(req.url)` lève une `TypeError` sur un chemin relatif, faute de base. J'ai vérifié le code livré : la base `http://localhost` est bien passée, la route et sa réponse **400** sont en place, `public/rendu.js` consomme bien `f.date`. Une inconsistance de nommage traîne en revanche dans le code — `extracterDate()` voisine avec **`extraerSlug()`**, verbe espagnol, dans le `.js` comme dans le `.ts`.

**Le document est cassé, et c'est un défaut de génération, pas de contenu.** Trois jetons `<0/>` ont été écrits dans `word/document.xml` à la place de trois éléments : le XML n'est **pas conforme**, Word refusera de l'ouvrir ou proposera de le réparer. Aux trois emplacements manquent la **check-list de vérification** (« Lance le serveur et vérifie ces quatre points » — suivi de rien), le **tableau des erreurs fréquentes** (annoncé, absent) et **toute la section « 📚 Ressources cliquables »** : le fichier ne contient **aucun lien**, alors que le parcours impose des URLs de documentation officielle testées. Le titre est également dupliqué en tête. **Le code du projet, lui, est complet et correct** — seul le support de cours est atteint.

## Notes liées

- **⬅️ Précédente** · [[2026-08-14_lecon-appli-ia_03_typescript-structure-projet]]
  qui typait l'inventaire sans changer sa source de données ; cette leçon change la source — le nom de fichier devient la donnée d'autorité, et `src/types.ts` s'enrichit de `date`, `slug` et `extension`
- **🔗 Pont** · [[2026-08-07_lecon-appli-ia_02_socle-web-premier-ecran]]
  le `serveur.js` écrit là en callbacks est ici réécrit en `async/await` — même comportement, lecture linéaire. C'est aussi la leçon où l'écart n°3 était né, en affichant le `mtime` faute de mieux
- **🔗 Pont** · [[2026-08-02_lecon-appli-ia_01_cadrage-specification]]
  la spec décidait que la date vient du nom et que les fichiers hors convention restent visibles. Deux séances plus tard, c'est elle qui tranche le cas `date: null` — décider avant de générer, le fil du parcours
