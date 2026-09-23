---
type: fiche-document
source: 2026-09-04_lecon-appli-ia_06_recherche-filtres.docx
date_creation: 2026-09-04
date_lecon: 2026-09-04
parcours: appli-ia
numero: 6
statut: parcours-actif
tags:
  - parcours/appli-ia
  - registre/technique
  - module/react
  - concept/composant-controle
  - concept/etat-derive
  - concept/usememo
  - concept/dependances-hooks
  - projet/portail-livrables
  - source/react-dev
  - source/mdn
  - alerte/corrige
  - correction/2026-09-04
---

# 2026-09-04_lecon-appli-ia_06_recherche-filtres

Document source : [[2026-09-04_lecon-appli-ia_06_recherche-filtres.docx]]

## Résumé

**Le fil rouge tient, et cette fois j'ai tout vérifié en exécutant.** Le code existe et il est daté de ce matin : `BarreRecherche.tsx` est nouveau, `App.tsx`, `GrilleCategorie.tsx` et `index.css` sont modifiés. **`npm run typecheck` passe** — je l'ai lancé, sortie vide, comme la leçon l'annonce. Le **`PROJET.md` est à jour** avec un tableau fichier par fichier disant ce qui a changé et à quelle leçon : la mémoire du parcours fait son travail. Côté forme, le **contrôle d'intégrité de l'étape 5 bis**, ajouté après l'incident du 21/08, tient sur un document qui contient un tableau et cinq hyperliens : XML bien formé, **zéro balise `<0/>`**. Et les cinq URL sont toutes en 200, toutes de la documentation officielle — react.dev et MDN —, ce qu'exige le garde-fou propre à ce parcours.

**La pédagogie est la meilleure produite jusqu'ici, parce qu'elle fait casser.** La séquence est lire → prédire → modifier → **casser volontairement**. L'exercice 4 demande de retirer `filtreLivrable` du tableau de dépendances de `useMemo`, puis constate ce qui compte : *TypeScript ne verra rien*, et *pas d'erreur console — juste un comportement silencieusement faux*. La leçon nomme ensuite le seul outil capable de l'attraper, `react-hooks/exhaustive-deps`. Trois autres notions sont posées nettement : le **composant contrôlé** avec la bonne question (*qui a besoin de cette valeur ?*), l'**état dérivé** contre l'état dupliqué qui se désynchronise, et surtout le contre-emploi de `useMemo` — *ne pas l'ajouter partout par précaution*, avec renvoi à la section « When to use useMemo » de react.dev. S'y ajoute un tableau de dépannage à six entrées, symptôme → cause → correction, directement utilisable.

**La section « ce que l'IA rate » se vérifie dans le code du jour.** Elle affirme que l'IA ne signale pas le piège de la référence de fonction : `filtreLivrable` est créée dans `App` à chaque render, sa référence change à chaque frappe. Or le code, lui, le commente explicitement — *« sa référence change à chaque frappe dans le champ de recherche — c'est voulu »* — et les dépendances réelles sont bien `[livrables, filtreLivrable]`. Même chose pour le quatrième point, l'effet de bord oublié : le `useEffect([filtreLivrable])` qui replie les catégories est présent, avec sa raison écrite en commentaire. La leçon décrit donc un piège qu'elle a elle-même évité, ce qui est la bonne façon de le faire.

**Deux défauts, dont un qu'aucun contrôle automatique ne peut attraper — corrigés le 04/09/2026 dans la leçon ET dans le code**, avec journal. ① **La variable centrale de la leçon est mal orthographiée** : `livrablesFiltes`, sans le « r ». Elle l'est **dans le code** — huit occurrences dans `GrilleCategorie.tsx` — et dans la leçon, avec **trois graphies différentes** (`livablesFiltres`, `setLivrablesFiltes`, `livrablesFiltes`) ; l'orthographe correcte n'apparaît **jamais**. Le code compile et `typecheck` passe parce que l'identifiant est cohérent avec lui-même : c'est exactement le type de défaut que ni TypeScript ni un lint ne voient. Le commentaire de la ligne 55 emploie même une graphie différente de la variable qu'il décrit. ② **« Sur 232 leçons » compte des fichiers, pas des leçons.** La catégorie `lecons` du serveur indexe `.docx` **et** `.md` — donc les fiches Obsidian avec les leçons. Le dossier contient aujourd'hui **125 `.docx` pour 125 `.md`**, soit 250 fichiers : le vrai nombre de leçons est 125, à peu près la moitié. C'est précisément la confusion que le prompt du parcours documente pour la numérotation — *« sans le filtre sur .docx, le nombre de leçons est doublé »* —, règle écrite pour l'étape 1 mais non appliquée à l'affichage. Les deux sont repris des deux côtés : la variable est renommée `livrablesFiltres` dans `GrilleCategorie.tsx` comme dans les extraits, **`npm run typecheck` revérifié après renommage**, et le texte distingue désormais les 250 fichiers des 125 leçons. `package.json` passe de **0.5.0** à **0.6.0**, et `PROJET.md` porte la trace de l'ensemble.

## Notes liées

- **⬅️ Précédente** · [[2026-08-28_lecon-appli-ia_05_interface-react-composants]]
  l'état du projet en ouverture est fidèle et daté — React + Vite sur 5173, typage strict, dépliage à 12 cartes. La leçon 06 branche la recherche sur cette grille sans rien casser : `typecheck` passait alors, il passe encore
- **🔗 Pont** · [[2026-08-21_lecon-appli-ia_04_donnees-reelles-api-fichiers]]
  **la leçon dont le docx était corrompu** par trois balises `<0/>` — `condition && element` renvoyant `0` en JSX. Le contrôle d'intégrité ajouté au prompt dans la foulée tient ici, sur un document plus riche : tableau, cinq hyperliens, XML valide
- **🔗 Pont** · [[2026-09-02_lecon-enneagramme_14_niveaux-developpement-riso-hudson]]
  **même schéma, autre parcours** : une règle écrite quelque part et non appliquée là où elle vaudrait aussi. L'ennéagramme n'avait pas repris le cadrage des sources de sa leçon précédente ; ici, la règle de comptage sur `.docx` existe pour la numérotation et pas pour l'affichage
- **🔗 Pont** · [[2026-09-02_veille_has-actualite.fiche]]
  **la même erreur de nature, à deux jours d'écart** : compter des fichiers en croyant compter des objets métier. La veille HAS prenait des dates de fichier pour des dates de publication, cette leçon prend des fichiers pour des leçons
