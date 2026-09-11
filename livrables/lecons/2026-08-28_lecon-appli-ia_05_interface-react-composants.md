---
type: fiche-document
source: 2026-08-28_lecon-appli-ia_05_interface-react-composants.docx
date_creation: 2026-08-28
date_lecon: 2026-08-28
parcours: appli-ia
numero: 5
statut: parcours-actif
tags:
  - parcours/appli-ia
  - registre/pro
  - techno/react
  - techno/vite
  - notion/composant
  - notion/hooks
  - notion/jsx
  - notion/proxy-cors
  - projet/portail-livrables
  - theme/fichiers-vs-lecons
  - theme/comportement-runtime-non-verifie
  - alerte/corrige
  - correction/2026-09-06
  - correction/2026-09-11
  - alerte/puces-vides
  - theme/source-non-citee
---

# 2026-08-28_lecon-appli-ia_05_interface-react-composants

Document source : [[2026-08-28_lecon-appli-ia_05_interface-react-composants.docx]]

## Résumé

Le choix annoncé en leçon 04 est tranché : **React + Vite**, dans un dossier `frontend/` séparé, et `scripts/serveur.js` n'est pas touché — React consomme l'API telle quelle. Sept fichiers déposés, que le lecteur lit, modifie, casse et répare.

**La théorie est la meilleure du parcours jusqu'ici**, parce qu'elle explique au lieu de décrire. L'opposition impératif / déclaratif est illustrée sur le cas réel — le frontend vanilla détruit et recrée 200 `<article>` à chaque `fetch()`, React ne touche que ce qui a changé, d'où le fait que **l'état survit aux mises à jour** (champ de recherche, position du scroll). Et l'ouverture est juste : la déclarativité n'a rien de propre à React, SQL, CSS et HTML le sont aussi. Surtout, la **règle des hooks** est donnée avec sa raison — *React identifie les hooks par leur ordre d'appel* — ce qui la rend mémorisable au lieu d'arbitraire. Le cas réel qui suit est exactement le bon niveau : demander à l'IA « n'appelle l'API que si l'utilisateur est connecté » produit un `if (…) { useEffect(…) }`, et la correction consiste à mettre la condition **dans** l'effet, pas autour. Le proxy Vite est expliqué par le problème qu'il résout (CORS) et assorti de la bonne réserve : il n'existe qu'en développement.

**La promesse de la leçon 04 n'était pas tenue — dette soldée le 28/08/2026.** Celle-ci annonçait noir sur blanc : *« L'API `/api/livrables?categorie=X` — créée cette semaine — sera la source de données de la nouvelle interface. Pour la première fois, le portail affichera la liste complète d'une catégorie, pas seulement les 5 plus récents. »* Or `App.jsx` n'appelle que `/api/inventaire`, et `GrilleCategorie` affiche `categorie.recents` — **les cinq plus récents, comme avant**. `/api/livrables` n'apparaissait nulle part dans `frontend/`. **`GrilleCategorie.jsx` a été repris le jour même** : il charge la liste complète de sa catégorie, avec dépliage au-delà de 12 cartes. L'incrément ajoute quatre notions absentes du corps de la leçon — un `useEffect` à **dépendance** `[nomCle]` et non à tableau vide, sa **fonction de nettoyage** contre le `setState` après démontage, un **état dérivé** recalculé plutôt que stocké, et `encodeURIComponent` sur le paramètre d'URL. Vérifié pour de bon : `npm install` puis `npm run build` passent (18 modules, vite 8.2.2), et le portail affiche **232 leçons après dépliage, 462 fichiers au total**. Le listing de la leçon est conservé comme version pédagogique, signalé comme tel ; `PROJET.md` porte l'incrément.

**La seconde dette est soldée aussi : le frontend est typé.** Quatre composants passés en `.tsx`, `strict: true`, `typecheck` branché dans le `build`. **Le typage a trouvé trois erreurs réelles** — l'import CSS non déclaré, et surtout deux conditions qui testaient `!chargement && !erreur` pour en déduire que la liste était chargée : vrai en pratique, garanti par rien. Elles testent maintenant `livrables !== null`. Le compilateur n'a pas signalé un bug qui plantait aujourd'hui, il a signalé **une hypothèse implicite**. Il a aussi mis au jour que `src/types.ts` déclare `Categorie` avec `recents` **et** `livrables` obligatoires, forme qu'aucune des deux routes ne renvoie — réconciliation renvoyée à la leçon 08.

**Et le garde-fou des versions a été contourné, pas respecté.** Vite est correctement traité : `^8.2.2`, annoncé comme vérifié le 28/08 — je l'ai confirmé, c'est bien la version courante. Mais `frontend/package.json` déclare **`"react": "*"`, `"react-dom": "*"` et `"@vitejs/plugin-react": "*"`**. Trois dépendances sur quatre en plage totalement ouverte. La règle du parcours dit de ne jamais écrire une version de mémoire ; y échapper en n'écrivant **aucune** version est pire qu'une version périmée — le build cesse d'être reproductible, et un `npm install` dans six mois peut ramener une majeure incompatible. **Corrigé le 28/08** : les trois dépendances sont épinglées — React et React-DOM en `^19.2.8`, `@vitejs/plugin-react` en `^6.1.1`, versions relevées avec `npm show`. La leçon le dit maintenant à l'endroit où l'on installe, et `PROJET.md` a été aligné : il justifiait le `"*"` par « pour éviter d'écrire des versions non vérifiées », ce qui inverse la règle — **ne pas écrire de version de mémoire veut dire aller la vérifier**.

**Défaut 1 — « 232 leçons » comptait des fichiers, et le libellé apparaissait trois fois.** Au 28/08, `livrables/lecons/` contenait **117 `.docx` et 117 `.md`** : **117 leçons pour 232 fichiers indexés**. Le nombre était juste, le libellé faux. Et la même leçon écrit correctement *« Afficher les 220 autres **fichiers** »* quelques lignes plus haut — le bon mot d'un côté, le mauvais de l'autre, sur le même nombre. C'est le défaut qui a donné la **règle 10** le 04/09 à partir de la leçon 06 : **cette occurrence est antérieure d'une semaine.** Ma première passe de correction n'en avait vu que deux sur trois ; la troisième se cachait dans la section « Dette soldée ».

**Défaut 2 — la règle des hooks était juste, la description de son échec ne l'était pas.** La leçon écrivait que le hook conditionnel *« crashera silencieusement en production »* et que cette syntaxe *« lance React Error Boundary »*. Deux affirmations sur le comportement d'un runtime, **étayées par aucune des quatre sources**, et **que je n'ai pas pu reproduire** : un test avec React 19.2.8 et `renderToString` rend sans erreur, parce qu'un rendu serveur remonte le composant à chaque fois. Une Error Boundary ne se « lance » pas non plus — c'est un composant qui **intercepte**, s'il existe. Les deux passages renvoient désormais à ce qui est documenté sur react.dev, cité mot pour mot. **Troisième leçon du parcours avec ce motif**, après les deux pièges de la leçon 02 — et à chaque fois dans la section « Ce que l'IA rate ».

**Ce qui est intact.** La liste *« null, undefined et false ne rendent rien »* est exacte **et complète** : le `0` en est justement absent, alors que c'est lui qui avait corrompu le `.docx` de la leçon 04. Virtual DOM, majuscule des composants, `className`, racine unique, tableau de dépendances : conformes. Et le journal du 28/08 sur l'épinglage reste l'un des meilleurs passages du parcours — laisser `"*"` dans un `package.json` ne respecte pas le garde-fou interdisant d'écrire une version de mémoire, il le **contourne**, et c'est pire.

**Défaut 3 — quinze puces vides, dans cinq listes annoncées : deux relectures ne l'avaient pas vu (relevé et corrigé le 11/09/2026).** Le document portait **quinze puces sans aucun texte** : trois dans « État du projet après la leçon 04 — repris de `PROJET.md` », qui n'en montrait que **deux sur cinq** ; **quatre sous « Ce que l'IA fait bien »**, c'est-à-dire la **colonne entière** — la section promettait un bien/mal et ne livrait que le mal ; quatre sous « Contrôles visuels dans le navigateur » ; quatre sous « Leçon 06 ajoutera ». Signature identique à l'octet sur les quinze : un `<w:p>` de 372 octets, style `ListParagraph`, numérotation intacte, `<w:t xml:space="default"/>` auto-fermant. **Pourquoi personne ne l'a vu** : le contrôle d'intégrité de l'étape 5 bis, né des `<0/>` de la leçon 04, ne vérifiait que XML bien formé / balises invalides / au moins un lien — il répondait `OK` sur ce fichier ; et à la lecture, une puce vide ressemble à une respiration. Le défaut a été découvert le 11/09 en auditant la leçon 07, qui en portait huit ; la mesure étendue au parcours donne **01/02/03/06 à zéro, 05 à quinze sur trente-huit, 07 à huit sur vingt-sept**. Le contrôle compte désormais les puces vides et refuse le document. **Les quinze sont remplies** : les trois premières relues dans l'historique du dépôt (`f8dcd3c`, l'état réel au 21/08 — l'amorce dit « repris de `PROJET.md` », je ne les ai pas inventées), les quatre de « Leçon 06 ajoutera » écrites d'après ce que la 06 a **réellement** livré le 04/09 (recherche NFD, deux filtres, composant contrôlé, `useMemo`), et les huit restantes — perdues — réécrites à la date du 11/09. Les contrôles visuels sont rédigés en **propriétés** avec une commande de recoupement, pas en nombres : c'est la règle 10 du parcours, née de l'incident des « 232 leçons » de ce document même.

**Défaut 4 — deux affirmations justes rattachées à la mauvaise page (relevé le 11/09/2026, non corrigé).** Le contenu est exact dans les deux cas ; c'est l'attribution qui ne tient pas. ① **La citation de la règle des hooks, ajoutée par la correction du 06/09** — *« Don't call Hooks inside loops, conditions, nested functions, or try / catch / finally blocks »* — est verbatim, mais elle ne figure sur **aucune des quatre pages listées en Ressources**. Elle vit sur `react.dev/reference/rules/rules-of-hooks` (200, **6 018 caractères utiles**, mesuré), que la leçon ne cite pas : le journal du 06/09 écrit « sur react.dev, section Rules of Hooks » — une attribution au site, pas à une page. ② **La configuration du proxy Vite**, `changeOrigin: true` compris, est correcte et documentée sur `vite.dev/config/server-options` — alors que le commentaire du fichier et le libellé de la ressource désignent `vite.dev/guide/`, qui ne contient **ni « proxy », ni « changeOrigin », ni le numéro 8.2.2** qu'on lui attribue (**9 766 caractères utiles**, mesurés). Les versions, elles, viennent bien de `npm show`, comme la leçon le dit ailleurs. C'est **la règle 13 du parcours, écrite le 06/09 — le jour même de la correction qui a introduit le premier des deux défauts**.

**Ce qui a été revérifié le 11/09 et tient.** Les quatre URL répondent **200 sans redirection** (14 303 · 9 766 · 26 204 · 42 073 caractères utiles). Les versions annoncées sont celles **réellement installées**, lues dans `node_modules` : react et react-dom **19.2.8**, `@vitejs/plugin-react` **6.1.1**, vite **8.2.2**. L'extrait de `vite.config.js` reproduit dans la leçon est **identique au fichier sur le disque**. `npm run build` passe dans `frontend/` : `tsc --noEmit` au vert puis **19 modules** transformés par vite 8.2.2 — le 19 confirmant la note de fraîcheur ajoutée le 06/09.

## Notes liées

- **⬅️ Précédente** · [[2026-08-21_lecon-appli-ia_04_donnees-reelles-api-fichiers]]
  qui construisait `/api/livrables?categorie=X` *en annonçant* qu'elle serait la source de la nouvelle interface. C'est la leçon à relire pour mesurer l'écart : la route existe, elle est testée, et le frontend l'ignore
- **➡️ Suivante** · [[2026-09-04_lecon-appli-ia_06_recherche-filtres]]
  la recherche et les filtres se branchent sur la grille construite ici, sans rien casser — `typecheck` passe toujours. Elle fait aussi casser volontairement les dépendances de `useMemo` pour montrer un bug que TypeScript ne voit pas
- **🔗 Pont** · [[2026-09-11_lecon-appli-ia_07_persistance-sqlite]]
  **c'est en auditant celle-là que le défaut d'ici a été trouvé.** Huit puces vides sur vingt-sept, même signature à l'octet près, et le même contrôle répondant `OK` sur les deux. La 07 a servi de révélateur : sans elle, les quinze puces de la 05 tenaient depuis quinze jours
- **🔗 Pont** · [[2026-08-14_lecon-appli-ia_03_typescript-structure-projet]]
  le frontend était en `.jsx` sans `tsconfig.json`, alors que la leçon 03 avait typé l'inventaire — **régression réparée le 28/08** : quatre composants en `.tsx`, `strict: true`, `typecheck` branché dans le `build`. Et le typage a confirmé l'avertissement de cette leçon-là : `Categorie` dans `src/types.ts` déclare une forme qu'**aucune route ne renvoie**. TypeScript fait confiance aux déclarations, jamais aux données
- **🔗 Pont** · [[2026-08-07_lecon-appli-ia_02_socle-web-premier-ecran]]
  le `public/` vanilla que React remplace, et dont la leçon se sert d'exemple négatif : c'est bien lui qui reconstruit toute la grille à chaque appel
- **🔗 Pont** · [[2026-08-02_lecon-appli-ia_01_cadrage-specification]]
  `CarteLivrable` applique la décision de la spec v1.2 sur les fichiers hors convention : afficher « date inconnue » plutôt que rien, puisque `{null}` ne rend rien en React. Décider avant de générer, jusque dans le rendu d'une case vide
