---
type: fiche-document
source: 2026-08-02_lecon-appli-ia_01_cadrage-specification.docx
date_creation: 2026-08-02
date_lecon: 2026-08-02
parcours: appli-ia
numero: 1
statut: parcours-actif
tags:
  - parcours/appli-ia
  - registre/technique
  - techno/nodejs
  - notion/specification
  - outil/claude-code
  - notion/hallucinations-dependances
  - source/arxiv
  - theme/regime-des-chiffres
  - alerte/corrige
  - correction/2026-09-06
---

# 2026-08-02_lecon-appli-ia_01_cadrage-specification

Document source : [[2026-08-02_lecon-appli-ia_01_cadrage-specification.docx]]

## Résumé

**Ouverture du parcours fil rouge « Portail Livrables », et la leçon qui a donné une règle au prompt — pas pour une faute, pour un geste juste. Corrigée le 06/09/2026**, avec journal. Elle distingue d'abord deux familles d'outils : les **générateurs d'application** (v0, Lovable, Bolt), excellents pour un prototype jetable mais enfermants ; et les **agents de codage** (Claude Code, Cursor), qui travaillent dans ton dépôt — c'est la voie retenue, parce que **le code t'appartient et reste lisible, corrigeable, versionnable**. Les 4 URL répondent 200.

**Le résultat central est exact de bout en bout — je l'ai vérifié sur la page arXiv.** `arXiv:2603.25146`, *« Factors Influencing the Quality of AI-Generated Code: A Synthesis of Empirical Evidence »*, par **Vehid Geruslu, Zulfiyya Aliyeva et Eray Tüzün**, soumis le **26 mars 2026**. Le résumé qu'en donne la leçon est fidèle au mot près : l'étude porte bien sur **24 études primaires**, et sa conclusion — la qualité du code dépend d'une combinaison de facteurs humains, de caractéristiques du système d'IA et de la dynamique d'interaction, les facteurs clés étant **la conception des invites, la spécification de la tâche et l'expertise du développeur** — correspond exactement à l'abstract. D'où l'exercice principal de la séance : écrire `SPEC.md`. C'est la première référence bibliographique complète du parcours, et elle est juste.

**Le défaut : deux organismes nommés comme sources, sans adresse.** L'encadré « Trois chiffres à garder en tête » attribuait ses données à *« des travaux référencés notamment sur arXiv, **Cloud Security Alliance**, **OX Security** »*. Seul arXiv figure en Ressources avec une URL testée. Les deux autres étaient nommés **une seule fois dans toute la leçon, sans aucune adresse** — invérifiables par le lecteur comme par le job. Écrire le nom d'un organisme lui confère une autorité que le lecteur ne peut pas distinguer d'une source réellement ouverte : **c'est le nom qui fait la caution**. Les deux noms sont retirés ; les trois chiffres restent, avec leur régime déclaré.

**Et ce qu'elle a apporté au parcours vaut mieux que sa correction.** L'encadré de transparence sur ces trois chiffres — *« Les études d'origine n'ont PAS été ouvertes une à une : traite ces valeurs comme des ordres de grandeur convergents, non comme des mesures que tu pourrais citer telles quelles dans un document professionnel »* — a été produit **spontanément**, alors qu'aucune consigne ne le demandait. Il a été repris **mot pour mot** le 06/09/2026 comme modèle obligatoire dans le prompt du parcours, sous la **règle 14**. Une règle peut naître d'un geste juste autant que d'une faute : celle-ci vient d'une leçon qui a fait, seule, ce qu'on ne lui avait pas demandé.

## Notes liées

- **➡️ Suivante** · [[2026-08-07_lecon-appli-ia_02_socle-web-premier-ecran]]
  du script en ligne de commande à la page web. C'est elle qui a donné la **règle 2 étendue** du prompt — le « sur Windows, le séparateur est \ » qui était faux, dans la section même qui prétend apprendre à repérer ce que l'IA rate
- **🔗 Pont** · [[2026-08-14_lecon-appli-ia_03_typescript-structure-projet]]
  la meilleure section Ressources du parcours : chaque source avec son code HTTP et ce qu'elle a apporté, versions relevées au `npm show` et datées. C'est elle aussi qui a donné la **règle 15** — elle cite `nodejs.org/en/about/releases`, qui redirige vers `previous-releases`
- **🔗 Pont** · [[2026-09-04_lecon-appli-ia_06_recherche-filtres]]
  la leçon qui a donné les **règles 10 et 11** — « 232 leçons » qui comptait des fichiers, et `livrablesFiltes` mal orthographié que ni TypeScript ni le lint ne voyaient. Le parcours a maintenant 15 règles, dont 5 nées de ses propres leçons
- **🔗 Pont** · [[2026-08-28_lecon-appli-ia_05_interface-react-composants]]
  l'exemple opposé sur les versions : `package.json` laissait `"*"` sur trois dépendances. Le journal de cette leçon le dit bien — n'écrire aucune version **contourne** le garde-fou au lieu de le respecter
