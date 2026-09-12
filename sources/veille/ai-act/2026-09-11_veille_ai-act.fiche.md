---
type: fiche-document
source: 2026-09-11_veille_ai-act.docx
date_creation: 2026-09-11
date_veille: 2026-09-11
veille: ai-act
statut: veille-archive
tags:
  - veille/ai-act
  - registre/pro
  - theme/rgpd
  - theme/sanctions-cnil
  - theme/litteratie-ia
  - theme/transparence-art50
  - source/cnil
  - source/commission-europeenne
  - source/iapp
  - alerte/decompte-contradictoire
  - alerte/source-ecartee-a-tort
  - alerte/corrige
  - correction/2026-09-12
---

# 2026-09-11_veille_ai-act

Document source : [[2026-09-11_veille_ai-act.docx]]

## Résumé

**Tout ce que la note affirme sur ses sources ouvertes est exact — et elle en affirme beaucoup, chiffres et dates compris.** Les douze URL ont été retestées : onze rendent du contenu réel, la douzième — les communiqués du Conseil — est un vrai mur à **130 caractères**, comme la note le dit. Les deux sanctions CNIL sont vérifiées au chiffre près : EXTIA **300 000 €**, délibération du **9 septembre 2026**, droit à l'effacement et article 17 ; Hôpital Privé de la Loire **500 000 €**, délibération du **21 juillet 2026** publiée le **3 septembre**, **524 867** patients et **202 246** « tiers de confiance », et les quatre manquements retenus — VPN et MFA absents pour les accès externes, contrôles d'accès, surveillance, information des personnes (art. 34) que la note traduit correctement par « notification aux tiers », puisque seuls les patients avaient été informés. Les Rencontres Informatique & Libertés du **29 septembre** sont bien la « 2 ème édition », inscriptions **complètes**, Auditorium Marceau Long, **20 avenue de Ségur**, avec le bilan **83 sanctions / 487 M€** pour 2025. La Q/R CNIL est datée du **17 août**, les lignes directrices art. 50 du **6 août**, la dernière actualité de la Commission du **31 août** (Virkkunen au G20). Les deux titres IAPP sont **verbatim**, l'article de Roccia daté du 10 septembre, celui de Hengesbaugh du 8 ; *« comme un paquebot, pas un hors-bord »* rend fidèlement *« a cruise ship, not a speed boat »* ; Türk, les 1,4 milliard de catholiques, *Rerum Novarum* 1891 et le chapitre 4 sont sur la page. La chronologie du Service Desk porte les quatre jalons dans l'ordre et avec leurs libellés — le contrôle avait signalé cette page « sous 3 000 caractères », c'était une fausse alerte : 2 760 caractères, mais complets. Et le **J-82** est juste. Contrôles : *21 liens · 51 puces, 0 vide*, test d'attribution à `exit 0`. Coût **0,94 $** (31 %).

**Le défaut est dans ce que la note dit d'elle-même : son décompte de sources se contredit d'une rubrique à l'autre.** L'en-tête annonce *« 6 tentées — 5 exploitées ✅, 1 bloquée ⚠️ »*. La rubrique « Sources du jour » annonce *« 5 sources ✅, 1 ⚠️, 1 ⛔ »*. Puis elle en liste **douze** : **dix** marquées ✅, une ⚠️, une ⛔. Trois comptes pour la même liste, dont aucun n'est celui qu'on peut vérifier en comptant les lignes. C'est exactement le motif consigné le 09/09 dans le prompt de `serafin-ph-veille` — *la note ne se contredit pas d'une rubrique à l'autre* —, et il touche ici la partie de la note qui prétend rendre compte de sa propre méthode. La ligne *« WebFetch et WebSearch sont des outils, pas des sources »* est juste et bienvenue ; le compte qui la suit ne l'est pas. **Corrigé le 12/09/2026** : en-tête et décompte disent ce que la liste contient — 13 sources, 11 ✅, 2 ⚠️, 0 ⛔ — et la règle 3 du prompt, qui exigeait déjà ce recompte sans l'outiller, a reçu son test.

**Une source « définitivement écartée » qui répond parfaitement.** La note écrit : *« artificialintelligenceact.eu : rendu JavaScript côté client, non extractible en headless. Constat confirmé en juillet, août et septembre 2026. Source définitivement écartée. »* Retestée le 12/09/2026 avec un agent de navigateur : **200, 16 376 caractères utiles**. Le site rend son contenu ; c'est l'agent par défaut du job qu'il refuse. Trois constats successifs faits avec le même outil ne font pas une preuve — ils répètent la même mesure. « Définitivement » est un mot lourd pour une source qui n'a jamais été essayée autrement, et c'est le troisième cas en deux jours d'un 403 ou d'une page « vide » qui ne concernait que l'agent : ABE Infoservice la veille, cpalondon avant-hier. **Corrigé** : le ⛔ devient ⚠️, « définitivement » disparaît, la mesure est écrite. Et la règle 10 du prompt `ai-act-veille` le dit désormais : *un blocage pour ton agent n'est pas un blocage pour le lecteur, et « définitivement » est interdit*.

**Une référence exacte portée sans sa source, et une discordance non signalée.** *« Règlement (UE) 2026/1744 du 8 juillet 2026, JOUE du 24 juillet, en vigueur le 27 »* — vérifié sur EUR-Lex le 12/09/2026, mot pour mot : *« RÈGLEMENT (UE) 2026/1744 … du 8 juillet 2026 »*, série L du 24.7.2026. Mais **EUR-Lex ne figure pas parmi les douze sources** de cette note : la référence a été établie par l'édition du 29/08, qui citait la page, et elle est reprise ici comme un fait acquis. Le lecteur de cette édition-ci ne peut pas l'ouvrir. Et la Q/R de la CNIL, elle, écrit *« une version amendée du RIA a été adoptée le 24 juillet 2026 »* — la date de publication, pas celle de l'acte : deux sources ouvertes disent deux dates, et la note, qui a la bonne, ne signale pas l'écart. Plus petit : la date de l'encyclique, **15/05/2026**, n'est pas imprimée sur la page IAPP, qui dit *« published on the 135th anniversary of Rerum Novarum »* — 15 mai 1891 + 135 ans ; la déduction est juste, mais c'en est une. **Corrigé** : EUR-Lex est la treizième source, la référence porte son adresse, la discordance CNIL / EUR-Lex est signalée, et la date de l'encyclique est dite déduite. Règle 11 du prompt : *une référence héritée porte sa source dans chaque édition, et deux sources qui divergent se signalent*.

**L'analyse ESSMS est la partie la plus solide, et elle avance.** Les cinq points de vigilance tiennent sur le texte : la littératie IA de l'art. 4 avec sa trace documentaire exigible, la transparence de l'art. 50 avec une lecture — *« un compte rendu rédigé avec l'aide d'une IA puis relu et validé par un professionnel ne déclenche pas l'obligation de marquage »* — conforme à l'exemption de contrôle éditorial humain de l'art. 50 §4, correcte mais que la note ne rattache pas au paragraphe. Le rappel Hôpital de la Loire est traduit en trois exigences concrètes pour un foyer — MFA sur les accès distants, profils au rôle, journaux consultés — et la note ne recule pas : elle reprend les repères du 04/09 (Conseil du 28/08, Q/R du 17/08, lignes directrices du 06/08) en les datant hors fenêtre, et son agenda ne porte que des dates à venir. Le niveau 🟢, annoncé comme *« honnête »*, l'est.

## Notes liées

- **⬅️ Précédente** · [[2026-09-04_veille_ai-act.fiche]]
  la note dont celle-ci reprend les repères sans reculer d'un jour — Conseil du 28/08, Q/R du 17/08, lignes directrices du 06/08 — et dont elle confirme la chronologie sur le Service Desk. Le décompte de sources y était juste ; il ne l'est plus ici
- **🔗 Pont** · [[2026-08-29_veille_ai-act.fiche]]
  **c'est là que le règlement 2026/1744 a été établi sur EUR-Lex**, à partir de la page même. Cette édition-ci en hérite sans la citer : la référence est exacte, la source a disparu en route
- **🗂️ Dossier** · [[AI-Act_dossier.fiche]]
  à compléter de la lecture de l'art. 50 §4 sur la relecture humaine, que la note applique correctement sans la nommer, et du décompte réel des sources de l'AI Act Service Desk et de la CNIL désormais stabilisées comme références de chaque édition
- **🔗 Pont** · [[2026-09-09_veille_SERAFIN-PH.fiche]]
  **même défaut de forme à deux jours d'écart** : une note qui se contredit d'une rubrique à l'autre. Là, le tableau de bord donnait le recueil comme terminé pendant que l'agenda attendait l'outil ; ici, trois décomptes de sources pour une seule liste. La règle 12 de `serafin-ph-veille` n'a pas d'équivalent dans le prompt `ai-act-veille`
- **🔗 Pont** · [[2026-09-12_lecon-placement-financier_14_gestion-libre-pilotee-mandat-arbitrage]]
  **la même page « bloquée » qui ne l'est que pour l'agent du job**, à un jour d'écart : ABE Infoservice annoncée en 403 et servant 22 051 caractères à un navigateur ; ici artificialintelligenceact.eu « définitivement écartée » et servant 16 376. La règle B1 écrite pour placement-financier le 12/09 vaut mot pour mot pour ce job
