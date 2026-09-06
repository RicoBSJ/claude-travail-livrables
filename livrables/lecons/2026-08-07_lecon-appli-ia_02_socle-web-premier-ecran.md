---
type: fiche-document
source: 2026-08-07_lecon-appli-ia_02_socle-web-premier-ecran.docx
date_creation: 2026-08-07
date_lecon: 2026-08-07
parcours: appli-ia
numero: 2
statut: parcours-actif
tags:
  - parcours/appli-ia
  - registre/technique
  - techno/html-css-js
  - techno/node-http
  - notion/requete-reponse
  - notion/path-traversal
  - theme/bonne-raison-mauvaise-raison
  - alerte/corrige
  - correction/2026-09-06
---

# 2026-08-07_lecon-appli-ia_02_socle-web-premier-ecran

Document source : [[2026-08-07_lecon-appli-ia_02_socle-web-premier-ecran.docx]]

## Résumé

**La leçon la plus vérifiable du corpus — trois de ses affirmations se testent en une commande, et je les ai toutes exécutées. Relue et corrigée le 06/09/2026**, avec un second journal. Le socle web : rôles respectifs de HTML, CSS et JavaScript, boucle requête-réponse, et lecture d'un serveur HTTP Node.js **sans aucune bibliothèque externe** — choix délibéré, Express n'arrivant qu'en leçon 08 pour qu'on comprenne d'abord la couche native. La pédagogie repose sur quatre gestes appliqués à du code déjà déposé sur le disque : **lire, prédire, modifier, casser**. On ne recopie rien.

**Tout ce qui se vérifie a été vérifié, et tout est exact.** Les **4 URL répondent 200 et aucune ne redirige** — contrairement à celle de la leçon 03. `path.join('a/','/b')` retourne bien `'a/b'` là où la concaténation produit `'a//b'` : **exécuté**. La documentation de Node, section `path.sep`, dit bien *« On Windows, both the forward slash ( / ) and backward slash ( \ ) are accepted as path segment separators »* — **la correction du 09/08 est donc elle-même exacte, et citée dans la bonne section**. Le préfixe `node:` est bien disponible depuis **14.18** : la table *History* porte *« v16.0.0, v14.18.0 — Added node: import support to require(...) »*. Le décompte des six requêtes est cohérent avec la liste qui le suit, et les chiffres de l'état du projet (202 = 79 + 19 + 38 + 66) sont exacts et datés.

**Le défaut : le bon conseil, la mauvaise raison — pour la seconde fois dans la même section.** Le piège n°1 écrivait qu'une requête `GET /../../../etc/passwd` *« pourrait lire n'importe quel fichier du système »*. Les clients HTTP **normalisent les segments `..` avant d'émettre**, conformément à la RFC 3986 §5.2.4. Mesuré sur un serveur Node d'essai : avec `curl` standard, le serveur reçoit `req.url = "/etc/passwd"` — les `..` ont déjà disparu ; il faut `--path-as-is` pour qu'il reçoive `"/../../../etc/passwd"`. L'attaque est réelle, mais elle passe par un client brut ou un encodage. **Le garde-fou `path.resolve()` + `startsWith()` reste indispensable** : seule sa justification par l'exemple était fausse.

**Et c'est exactement le même motif que le piège n°2, corrigé le 09/08.** Là, *« ça casse sur Windows »* était faux, la vraie raison étant la normalisation. Ici, l'exemple d'attaque est faux, la vraie raison étant le client brut. **Deux fois de suite, dans la section « Ce que l'IA rate »** — celle qui prétend apprendre à repérer les affirmations non vérifiées sur le comportement d'un système, et qui en concentre le plus. Le garde-fou n°7 du prompt le dit déjà (*« relis spécifiquement cette section »*) ; cette relecture le confirme une seconde fois.

## Notes liées

- **⬅️ Précédente** · [[2026-08-02_lecon-appli-ia_01_cadrage-specification]]
  dont la spécification est ici mise à l'épreuve du code. Elle a donné les **règles 13 et 14** du prompt le 06/09 — dont la 14, née d'un geste juste et non d'une faute
- **➡️ Suivante** · [[2026-08-14_lecon-appli-ia_03_typescript-structure-projet]]
  qui type le code écrit ici, et résout l'écart n°4 laissé ouvert. C'est elle qui a donné la **règle 15** — elle cite `nodejs.org/en/about/releases`, qui redirige ; cette leçon-ci citait déjà la bonne adresse pour le même tableau
- **🔗 Pont** · [[2026-09-04_lecon-appli-ia_06_recherche-filtres]]
  **le même motif, deux mois plus tard** : la section « Ce que l'IA rate » y décrit un piège que le code de la leçon avait, lui, correctement évité. Ici elle décrit deux pièges réels avec deux justifications fausses. C'est la section la plus exposée du format
- **🔗 Pont** · [[2026-04-10_lecon01_fondamentaux]]
  même famille d'outils vue deux ans plus tôt sous l'angle de l'usage ; ici sous celui de la production de code
