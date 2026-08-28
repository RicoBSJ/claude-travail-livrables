---
type: fiche-document
source: 2026-08-21_lecon-appli-ia_04_donnees-reelles-api-fichiers.docx
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
  - notion/event-loop
  - notion/query-params
  - notion/variable-environnement
  - projet/portail-livrables
---

# 2026-08-21_lecon-appli-ia_04_donnees-reelles-api-fichiers

Document source : [[2026-08-21_lecon-appli-ia_04_donnees-reelles-api-fichiers.docx]]

## Résumé

Leçon de bascule vers les **données réelles** : le serveur passe en `async/await` avec `node:fs/promises`, extrait date et slug **depuis le nom du fichier**, lit les query params avec `new URL()` et expose une route ciblée `/api/livrables?categorie=X`. **L'écart n°3 est résolu** — la date vient du nom, plus du `mtime` — deux séances avant la leçon 06 où il était planifié. *(Seconde version : le document du matin était défectueux et a été régénéré ; le slug a changé au passage.)*

La théorie va au bon endroit : **pourquoi** Node est asynchrone, boucle d'événements à l'appui, avec le *callback hell* montré une fois pour qu'on comprenne ce qu'`async/await` remplace. La règle est nette — **toute opération d'I/O rend la fonction `async`** — et le tableau `fs` / `fs/promises` distingue les trois méthodes réellement utilisées (`readdir` avec `withFileTypes`, `stat`, `readFile` réservée à la leçon 08). Deux points datés et sourcés à la doc officielle : la base `http://localhost` est **obligatoire** dans `new URL(req.url, …)` sous peine de `TypeError`, et **`url.parse()` est déprécié depuis Node v11** — l'IA le propose encore parce qu'il était partout jusqu'en 2019.

**Le tableau « ce que l'IA fait bien / fait mal » est le meilleur du parcours jusqu'ici**, parce qu'il donne des symptômes et non des principes : `readdir` en callback hérité d'un entraînement d'avant 2020, `try/catch` oublié autour de `readdir` faisant planter le serveur sur `ENOENT`, **race condition** entre `readdir` et `stat` jamais signalée, et surtout le double import de `fs` et `fs/promises` **sous le même nom** — la confusion garantie. Le tableau des erreurs au démarrage prolonge la logique : `EADDRINUSE`, `ERR_INVALID_URL`, `ENOENT`, et les deux erreurs symétriques ESM / CommonJS.

**J'ai exécuté l'étape 4 (« CASSER ») plutôt que de la croire — un des quatre résultats annoncés était faux, corrigé dans le document le 21/08/2026.** Le paramètre manquant et la catégorie inconnue renvoient bien **400**, la route inconnue **404**, et l'API répond correctement (215 leçons, `date` et `slug` conformes). Mais la tentative de *path traversal* `curl 'http://localhost:3000/../../etc/passwd'` était annoncée en **403** et retourne **404** — y compris avec `--path-as-is`, donc ce n'est pas curl qui normalise, et les formes encodées (`%2e%2e`, `..%2f`) ne changent rien. La cause est en amont : `new URL()` réduit le chemin à `/etc/passwd`, qui reste sous `DOSSIER_PUBLIC` et échoue à la lecture avant d'atteindre le garde-fou. **La branche 403 de la ligne 238 n'est donc atteignable par aucune requête HTTP en l'état** — le garde-fou est correct, c'est l'exercice qui ne l'exerçait pas. La correction ajoute au document l'explication technique et ce que le cas enseigne : **un garde-fou inatteignable reste utile**, il couvre le jour où la couche d'avant changera.

Une relecture complète a relevé quatre points de plus, corrigés le même jour. Le plus gênant est l'indice de l'étape « PRÉDIRE » : `ls livrables/lecons/*.docx | wc -l` donne **107** quand l'API en retourne **~214**, la catégorie étant déclarée `['.docx', '.md']` — **une prédiction fausse d'un facteur 2 dans l'exercice dont le principe est justement de prédire puis vérifier**. Ensuite, la dépréciation d'`url.parse()`, annoncée « depuis v11, marquée Legacy » : le tableau *History* officiel montre une trajectoire en zigzag — dépréciée en v11, **révoquée en v14.17/v15.13** (« Legacy » était justement l'état *non* déprécié), redocumentée en v18.13/v19, puis *application deprecation* en **v24.0.0**, la version que le projet fait tourner. Enfin 276 lignes et non 277, et un avertissement ajouté sur l'écart entre la doc citée (v26.7.0) et le runtime local (v24.15.0). **Les quatre plages d'extraits citées, elles, sont exactes** — vérifiées une à une.

## Notes liées

- **⬅️ Précédente** · [[2026-08-14_lecon-appli-ia_03_typescript-structure-projet]]
  qui typait l'inventaire sans changer sa source de données ; cette leçon change la source — le nom de fichier devient la donnée d'autorité, et `Livrable` s'enrichit de `date`, `slug` et `extension`
- **➡️ Suivante** · [[2026-08-28_lecon-appli-ia_05_interface-react-composants]]
  l'interface React annoncée ici — mais qui **n'utilise pas** `/api/livrables?categorie=X` : elle consomme `/api/inventaire` et affiche toujours les cinq plus récents. La promesse faite en fin de cette leçon n'est pas tenue
- **🔗 Pont** · [[2026-08-07_lecon-appli-ia_02_socle-web-premier-ecran]]
  le `serveur.js` écrit là en callbacks est ici réécrit en `async/await` — même comportement, lecture linéaire. C'est aussi la leçon où l'écart n°3 était né, faute de mieux que le `mtime`
- **🔗 Pont** · [[2026-08-02_lecon-appli-ia_01_cadrage-specification]]
  la spec décidait que la date vient du nom et que les fichiers hors convention restent visibles. Deux séances plus tard, c'est elle qui tranche le cas `date: null` — décider avant de générer, le fil du parcours
