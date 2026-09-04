---
type: fiche-document
source: 2026-09-04_veille_ai-act.docx
date_creation: 2026-09-04
date_veille: 2026-09-04
veille: ai-act
statut: veille-active
tags:
  - veille/ai-act
  - theme/litteratie-ia
  - theme/article-50
  - theme/chatbots-medicaux
  - theme/gouvernance-ia
  - theme/echeance-2-decembre-2026
  - source/cnil
  - source/conseil-ue
  - source/iapp
---

# 2026-09-04_veille_ai-act

Document source : [[2026-09-04_veille_ai-act.docx]]

## Résumé

**Première note du job recréé le 30/08, et c'est la veille la mieux tenue du corpus sur le régime des sources.** Elle ne se contente pas de dire ce qu'elle a lu : elle dit ce qu'elle n'a **pas** lu. Les articles IAPP sont marqués **[LIBRE]** ou **[MEMBER]**, les payants portent la mention *« corps non accessible — titre et thème uniquement »*, et — c'est ce qui la distingue — même pour les articles librement accessibles elle précise que *« leur corps n'a pas été reproduit dans cette note »*, chaque thème étant annoncé « d'après le titre ». La source morte porte son mode d'emploi : *artificialintelligenceact.eu — rendu JavaScript côté client, non extractible en headless (constaté juillet et août 2026, **ne plus tenter**)*. Le 403 du Conseil est contourné proprement, page principale inaccessible mais PDF vérifié en 200 sur `data.consilium.europa.eu`, les deux dits. Et le décompte final déclare jusqu'à ce qui manque : *« EUR-Lex non directement interrogée dans cette exécution »*. **J'ai testé les dix URL : toutes en 200**, pour treize liens cliquables.

**La chronologie réglementaire se vérifie ligne à ligne sur sa propre source, y compris là où je la soupçonnais.** J'avais un doute sur l'échéance du 2 décembre 2026 rattachée à l'**article 50 §2** — les périodes transitoires relevant plutôt des dispositions finales. La page de l'AI Act Service Desk, que la note cite comme référence, confirme exactement sa lecture : cette date porte bien sur l'article 50(2), avec ses **deux volets** — interdiction des hypertrucages sexuels non consentis et des contenus pédocriminels, **et** fin du délai transitoire pour les fournisseurs d'IA générative commercialisée avant août 2026. Les autres jalons concordent aussi : bacs à sable au 2 août 2027, haut risque Annexe III au 2 décembre 2027, Annexe I au 2 août 2028. Le **J-89** est juste au jour près, je l'ai recalculé. Et la note s'ouvre sur une **révision de l'édition précédente** — celle du 29/08, qui corrigeait elle-même cinq points de juillet — en concluant qu'aucune inexactitude n'est à reprendre.

**Ce qui te concerne, dans l'ordre d'urgence.** ① La **littératie IA de l'article 4** est en vigueur depuis le 2 août et le régime de sanction est actif : pour les douze professionnels des deux équipes, il faut une trace — contenu, date, émargement — et la note dit la chose juste, *la trace doit exister avant toute évaluation*. Le document du Conseil du 28/08 sur les compétences IA confirme la direction. ② L'échéance du **2 décembre, J-89** : vérifier tout outil d'IA générative en production avant le 2 août 2026. ③ Le cadrage de l'**article 50** est repris à l'identique de la note du 29/08, et il reste le plus utile — un compte rendu rédigé avec l'aide d'une IA **puis relu et validé** n'entre pas dans le champ ; une page d'actualités alimentée automatiquement ou un chatbot pour les familles, oui. ④ Les autorités nationales françaises ne sont **toujours pas désignées** au 04/09, ce qui ne suspend aucune obligation : le DPO reste l'interlocuteur.

**La limite est l'envers de sa qualité.** La section « Analyses & gouvernance » repose sur quatre articles IAPP dont **aucun corps n'a été lu** — la note le dit quatre fois, honnêtement. Mais les impacts ESSMS s'appuient ensuite dessus : *« l'article IAPP du 02/09 rappelle la pertinence de ce périmètre »* pour les chatbots médicaux, *« l'article IAPP du 03/09 rappelle les enjeux de propriété intellectuelle »*. Une recommandation professionnelle adossée à un titre reste une recommandation adossée à un titre, même quand elle est par ailleurs sensée. Les conseils tiennent d'eux-mêmes — recenser les outils conversationnels, vérifier la politique d'attribution du prestataire — mais leur justification affichée est plus mince qu'elle n'en a l'air. Reste une coquille : *« chatbot famililles »*.

## Notes liées

- **⬅️ Précédente** · [[2026-08-29_veille_ai-act.fiche]]
  la reprise ponctuelle qui corrigeait cinq points de l'édition de juillet et documentait l'entrée en application du 2 août. Celle-ci la relit et n'y trouve rien à reprendre — première note du job une fois recréé, et le cadrage de l'article 50 y est repris à l'identique
- **🗂️ Dossier** · [[AI-Act_dossier.fiche]]
  à compléter de deux éléments : la chronologie complète vérifiée sur l'AI Act Service Desk — 2/12/2026 art. 50(2), 2/08/2027 bacs à sable, 2/12/2027 Annexe III, 2/08/2028 Annexe I — et la mention que `artificialintelligenceact.eu` est définitivement écartée
- **🔗 Pont** · [[RGPD_dossier.fiche]]
  l'articulation que la mise à jour CNIL du 17/08 fixe : les deux règlements s'appliquent simultanément aux systèmes à haut risque traitant des données personnelles, et le déployeur peut s'appuyer sur l'AIPD du fournisseur (art. 26 et 27). C'est le point d'entrée si un chatbot entre un jour dans l'établissement
- **🔗 Pont** · [[2026-09-02_veille_SERAFIN-PH.fiche]]
  **deux veilles, deux régimes de liens à deux jours d'écart** : celle-ci porte treize liens tous testés et déclare jusqu'aux sources qu'elle n'a pas interrogées ; SERAFIN n'en portait aucun et publiait une adresse CNSA en 404 marquée « consultée ». C'est ce contraste qui a fait durcir le prompt serafin le 02/09
