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
---

# 2026-08-14_lecon-appli-ia_03_typescript-structure-projet

Document source : [[2026-08-14_lecon-appli-ia_03_typescript-structure-projet.docx]]

## Résumé

TypeScript ajoute au JavaScript **une couche de vérification avant l'exécution**. La leçon prend soin de dire ce que ça ne change pas : le comportement au runtime reste identique, puisque tout est compilé vers du JavaScript ordinaire. Le coût se paie à la compilation, pas à l'usage. L'exemple est parlant — `cat.tailleko` au lieu de `cat.taille_ko` passe inaperçu en JavaScript jusqu'au premier lancement ; le compilateur l'arrête immédiatement.

Les **interfaces** sont présentées pour ce qu'elles sont : des contrats sur la forme des données, sans aucune logique exécutable. Puis `tsconfig.json` est décortiqué option par option — `target`, `module`, `outDir`, `rootDir`, `strict`, `types`, `declaration`, `sourceMap` — chacune avec sa fonction réelle plutôt qu'une valeur à recopier.

**Le passage le plus instructif est un incident rencontré pendant la génération même.** TypeScript 7.0.2 a supprimé l'option `moduleResolution: "node"` ; le compilateur a renvoyé l'erreur TS5108, et la leçon documente le diagnostic et la correction. C'est le garde-fou du parcours — *ne jamais écrire de version ni d'option de configuration de mémoire* — pris en flagrant délit sur sa propre production : la première version du `tsconfig.json` générée contenait l'option périmée. La règle qui en découle est nette : **faire confiance au compilateur, pas à la suggestion**.

La section sur les manques de l'IA prolonge ce constat avec trois travers reconnaissables : recourir à `any` pour faire taire une erreur au lieu de la résoudre — `unknown` étant le bon réflexe quand le type est encore indéterminé ; produire des interfaces qui décrivent le code montré plutôt que les données réelles, TypeScript faisant confiance aux déclarations et jamais aux données à l'exécution ; et inventer des noms de paquets, d'où la vérification par `npm show`. **L'écart n°4 du projet — le `README.md` compté comme livrable — est enfin résolu ici**, comme prévu depuis la leçon 02.

## Notes liées

- **⬅️ Précédente** · [[2026-08-07_lecon-appli-ia_02_socle-web-premier-ecran]]
  dont les trois modules du navigateur (app.js, api.js, rendu.js) constituent le code que cette leçon commence à typer, et dont l'écart n°4 était resté ouvert
- **➡️ Suivante** · [[2026-08-21_lecon-appli-ia_04_donnees-reelles-api-fichiers]]
  le typage posé ici sert de socle : `Livrable` s'enrichit de `date`, `slug` et `extension` quand la source des données passe du `mtime` au nom de fichier
- **🔗 Pont** · [[2026-08-02_lecon-appli-ia_01_cadrage-specification]]
  une interface TypeScript est une spécification exécutable : ce que SPEC.md dit en français, l'interface le fait vérifier par le compilateur. Le fil du parcours — décider avant de générer — trouve ici sa forme technique
- **🔗 Pont** · [[2026-06-26_lecon-nocode-ia_12_comprendre-les-llm-tokens-contexte]]
  la coupure de connaissance y était exposée comme limite théorique des LLM ; l'option moduleResolution supprimée en est l'illustration concrète, sur la production du jour même
