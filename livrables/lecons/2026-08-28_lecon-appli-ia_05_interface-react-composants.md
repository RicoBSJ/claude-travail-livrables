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
  - alerte/a-corriger
---

# 2026-08-28_lecon-appli-ia_05_interface-react-composants

Document source : [[2026-08-28_lecon-appli-ia_05_interface-react-composants.docx]]

## Résumé

Le choix annoncé en leçon 04 est tranché : **React + Vite**, dans un dossier `frontend/` séparé, et `scripts/serveur.js` n'est pas touché — React consomme l'API telle quelle. Sept fichiers déposés, que le lecteur lit, modifie, casse et répare.

**La théorie est la meilleure du parcours jusqu'ici**, parce qu'elle explique au lieu de décrire. L'opposition impératif / déclaratif est illustrée sur le cas réel — le frontend vanilla détruit et recrée 200 `<article>` à chaque `fetch()`, React ne touche que ce qui a changé, d'où le fait que **l'état survit aux mises à jour** (champ de recherche, position du scroll). Et l'ouverture est juste : la déclarativité n'a rien de propre à React, SQL, CSS et HTML le sont aussi. Surtout, la **règle des hooks** est donnée avec sa raison — *React identifie les hooks par leur ordre d'appel* — ce qui la rend mémorisable au lieu d'arbitraire. Le cas réel qui suit est exactement le bon niveau : demander à l'IA « n'appelle l'API que si l'utilisateur est connecté » produit un `if (…) { useEffect(…) }`, et la correction consiste à mettre la condition **dans** l'effet, pas autour. Le proxy Vite est expliqué par le problème qu'il résout (CORS) et assorti de la bonne réserve : il n'existe qu'en développement.

**La promesse de la leçon 04 n'était pas tenue — dette soldée le 28/08/2026.** Celle-ci annonçait noir sur blanc : *« L'API `/api/livrables?categorie=X` — créée cette semaine — sera la source de données de la nouvelle interface. Pour la première fois, le portail affichera la liste complète d'une catégorie, pas seulement les 5 plus récents. »* Or `App.jsx` n'appelle que `/api/inventaire`, et `GrilleCategorie` affiche `categorie.recents` — **les cinq plus récents, comme avant**. `/api/livrables` n'apparaissait nulle part dans `frontend/`. **`GrilleCategorie.jsx` a été repris le jour même** : il charge la liste complète de sa catégorie, avec dépliage au-delà de 12 cartes. L'incrément ajoute quatre notions absentes du corps de la leçon — un `useEffect` à **dépendance** `[nomCle]` et non à tableau vide, sa **fonction de nettoyage** contre le `setState` après démontage, un **état dérivé** recalculé plutôt que stocké, et `encodeURIComponent` sur le paramètre d'URL. Vérifié pour de bon : `npm install` puis `npm run build` passent (18 modules, vite 8.2.2), et le portail affiche **232 leçons après dépliage, 462 fichiers au total**. Le listing de la leçon est conservé comme version pédagogique, signalé comme tel ; `PROJET.md` porte l'incrément.

**La seconde dette est soldée aussi : le frontend est typé.** Quatre composants passés en `.tsx`, `strict: true`, `typecheck` branché dans le `build`. **Le typage a trouvé trois erreurs réelles** — l'import CSS non déclaré, et surtout deux conditions qui testaient `!chargement && !erreur` pour en déduire que la liste était chargée : vrai en pratique, garanti par rien. Elles testent maintenant `livrables !== null`. Le compilateur n'a pas signalé un bug qui plantait aujourd'hui, il a signalé **une hypothèse implicite**. Il a aussi mis au jour que `src/types.ts` déclare `Categorie` avec `recents` **et** `livrables` obligatoires, forme qu'aucune des deux routes ne renvoie — réconciliation renvoyée à la leçon 08.

**Et le garde-fou des versions a été contourné, pas respecté.** Vite est correctement traité : `^8.2.2`, annoncé comme vérifié le 28/08 — je l'ai confirmé, c'est bien la version courante. Mais `frontend/package.json` déclare **`"react": "*"`, `"react-dom": "*"` et `"@vitejs/plugin-react": "*"`**. Trois dépendances sur quatre en plage totalement ouverte. La règle du parcours dit de ne jamais écrire une version de mémoire ; y échapper en n'écrivant **aucune** version est pire qu'une version périmée — le build cesse d'être reproductible, et un `npm install` dans six mois peut ramener une majeure incompatible. **Corrigé le 28/08** : les trois dépendances sont épinglées — React et React-DOM en `^19.2.8`, `@vitejs/plugin-react` en `^6.1.1`, versions relevées avec `npm show`. La leçon le dit maintenant à l'endroit où l'on installe, et `PROJET.md` a été aligné : il justifiait le `"*"` par « pour éviter d'écrire des versions non vérifiées », ce qui inverse la règle — **ne pas écrire de version de mémoire veut dire aller la vérifier**.

## Notes liées

- **⬅️ Précédente** · [[2026-08-21_lecon-appli-ia_04_donnees-reelles-api-fichiers]]
  qui construisait `/api/livrables?categorie=X` *en annonçant* qu'elle serait la source de la nouvelle interface. C'est la leçon à relire pour mesurer l'écart : la route existe, elle est testée, et le frontend l'ignore
- **🔗 Pont** · [[2026-08-14_lecon-appli-ia_03_typescript-structure-projet]]
  le frontend était en `.jsx` sans `tsconfig.json`, alors que la leçon 03 avait typé l'inventaire — **régression réparée le 28/08** : quatre composants en `.tsx`, `strict: true`, `typecheck` branché dans le `build`. Et le typage a confirmé l'avertissement de cette leçon-là : `Categorie` dans `src/types.ts` déclare une forme qu'**aucune route ne renvoie**. TypeScript fait confiance aux déclarations, jamais aux données
- **🔗 Pont** · [[2026-08-07_lecon-appli-ia_02_socle-web-premier-ecran]]
  le `public/` vanilla que React remplace, et dont la leçon se sert d'exemple négatif : c'est bien lui qui reconstruit toute la grille à chaque appel
- **🔗 Pont** · [[2026-08-02_lecon-appli-ia_01_cadrage-specification]]
  `CarteLivrable` applique la décision de la spec v1.2 sur les fichiers hors convention : afficher « date inconnue » plutôt que rien, puisque `{null}` ne rend rien en React. Décider avant de générer, jusque dans le rendu d'une case vide
