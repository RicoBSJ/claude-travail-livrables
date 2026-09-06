---
type: fiche-document
source: 2026-08-14_lecon-appli-ia_03_typescript-structure-projet.docx
date_creation: 2026-08-15
date_lecon: 2026-08-14
parcours: appli-ia
numero: 3
statut: parcours-actif
tags:
  - parcours/appli-ia
  - techno/typescript
  - techno/tsconfig
  - notion/typage-statique
  - notion/interface
  - notion/compilation
  - notion/coupure-de-connaissance
  - registre/technique
  - theme/url-qui-redirige
  - theme/sortie-attendue-perimee
  - alerte/corrige
  - correction/2026-09-06
---

# 2026-08-14_lecon-appli-ia_03_typescript-structure-projet

Document source : [[2026-08-14_lecon-appli-ia_03_typescript-structure-projet.docx]]

## Résumé

**Relue et corrigée le 06/09/2026 — et c'est la leçon la plus testable du corpus : tout ce qui s'y vérifie a été exécuté.** L'erreur **TS5108** a été **reproduite mot pour mot** avec le `tsc 7.0.2` du projet. L'*excess property checking* annoncé à l'étape 2 se produit bien (`TS2353: […] 'chemin' does not exist in type 'Livrable'`). Le fichier `dist/types.js` est bien quasi vide — **388 octets**, dont l'essentiel en commentaires. La correction de l'écart n°4 est **réellement dans le code** : `serveur.js` porte `const DOCS_DE_DOSSIER = ['readme.md']` et son filtre. Et **v24 Krypton / v22 Jod** sont exacts sur nodejs.org. Sa section Ressources reste la meilleure du parcours : chaque source avec son code HTTP et ce qu'elle a apporté, versions relevées au `npm show` et datées.

TypeScript ajoute au JavaScript **une couche de vérification avant l'exécution**. La leçon prend soin de dire ce que ça ne change pas : le comportement au runtime reste identique, puisque tout est compilé vers du JavaScript ordinaire. Le coût se paie à la compilation, pas à l'usage. L'exemple est parlant — `cat.tailleko` au lieu de `cat.taille_ko` passe inaperçu en JavaScript jusqu'au premier lancement ; le compilateur l'arrête immédiatement.

Les **interfaces** sont présentées pour ce qu'elles sont : des contrats sur la forme des données, sans aucune logique exécutable. Puis `tsconfig.json` est décortiqué option par option — `target`, `module`, `outDir`, `rootDir`, `strict`, `types`, `declaration`, `sourceMap` — chacune avec sa fonction réelle plutôt qu'une valeur à recopier.

**Le passage le plus instructif est un incident rencontré pendant la génération même.** TypeScript 7.0.2 a supprimé l'option `moduleResolution: "node"` ; le compilateur a renvoyé l'erreur TS5108, et la leçon documente le diagnostic et la correction. C'est le garde-fou du parcours — *ne jamais écrire de version ni d'option de configuration de mémoire* — pris en flagrant délit sur sa propre production : la première version du `tsconfig.json` générée contenait l'option périmée. La règle qui en découle est nette : **faire confiance au compilateur, pas à la suggestion**.

La section sur les manques de l'IA prolonge ce constat avec trois travers reconnaissables : recourir à `any` pour faire taire une erreur au lieu de la résoudre — `unknown` étant le bon réflexe quand le type est encore indéterminé ; produire des interfaces qui décrivent le code montré plutôt que les données réelles, TypeScript faisant confiance aux déclarations et jamais aux données à l'exécution ; et inventer des noms de paquets, d'où la vérification par `npm show`. **L'écart n°4 du projet — le `README.md` compté comme livrable — est enfin résolu ici**, comme prévu depuis la leçon 02.

**Trois corrections, aucune sur un fait technique.** ① **L'adresse publiée n'était pas celle de la page** : `nodejs.org/en/about/releases` **redirige** vers `/en/about/previous-releases`. Le test `curl` du parcours suit les redirections — le 200 ne révélait rien. Le contenu cité est exact ; l'URL a été corrigée **dans la relation du .docx**, et elle ne redirige plus. La leçon 02 publiait déjà, elle, la bonne adresse pour ce même tableau : c'est cet écart entre deux leçons du même parcours qui a donné la **règle 15** du prompt. ② **Une sortie attendue qui se périme toute seule** : la liste de contrôle annonçait *« controles 1 fichier(s) »*. Exact au 14/08 — l'historique du dépôt le confirme — mais le dossier reçoit un fichier par semaine et la même commande renvoie **4** au 06/09. Or ce que l'exercice vérifie n'est pas le **nombre**, c'est que `README.md` ne soit plus compté : une **propriété**, qui ne bouge pas. La consigne le dit désormais, avec une commande de recoupement. **La règle 10 du prompt a été étendue le jour même aux sorties attendues des commandes de vérification.** ③ *« ES2022 est supportée par Node.js v18+ »* — affirmation sur un runtime, **absente des quatre sources**, exactement ce que vise le garde-fou n°2. Remplacée par ce qui est vérifiable localement : `engines.node >= 24` dans le `package.json` du projet.

## Notes liées

- **⬅️ Précédente** · [[2026-08-07_lecon-appli-ia_02_socle-web-premier-ecran]]
  dont les trois modules du navigateur (app.js, api.js, rendu.js) constituent le code que cette leçon commence à typer, et dont l'écart n°4 était resté ouvert
- **➡️ Suivante** · [[2026-08-21_lecon-appli-ia_04_donnees-reelles-api-fichiers]]
  le typage posé ici sert de socle : `Livrable` s'enrichit de `date`, `slug` et `extension` quand la source des données passe du `mtime` au nom de fichier
- **🔗 Pont** · [[2026-08-02_lecon-appli-ia_01_cadrage-specification]]
  une interface TypeScript est une spécification exécutable : ce que SPEC.md dit en français, l'interface le fait vérifier par le compilateur. Le fil du parcours — décider avant de générer — trouve ici sa forme technique
- **🔗 Pont** · [[2026-09-04_lecon-appli-ia_06_recherche-filtres]]
  la leçon qui a donné la **règle 10** — « 232 leçons » qui comptait des fichiers. Le défaut trouvé ici en est la face cachée : la règle imposait de dater les chiffres du TEXTE, pas les sorties attendues des COMMANDES. Elle couvre les deux depuis le 06/09/2026
- **🔗 Pont** · [[2026-06-26_lecon-nocode-ia_12_comprendre-les-llm-tokens-contexte]]
  la coupure de connaissance y était exposée comme limite théorique des LLM ; l'option moduleResolution supprimée en est l'illustration concrète, sur la production du jour même
