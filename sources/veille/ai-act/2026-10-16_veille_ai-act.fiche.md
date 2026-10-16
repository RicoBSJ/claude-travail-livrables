---
type: fiche-document
source: 2026-10-16_veille_ai-act.docx
date_creation: 2026-10-16
date_veille: 2026-10-16
veille: ai-act
statut: alerte/a-corriger
tags:
  - veille/ai-act
  - registre/pro
  - theme/panel-scientifique
  - theme/perte-de-controle
  - theme/ddadue
  - theme/cnil
  - source/commission
  - source/cnil
  - source/iapp
  - alerte/plafond-depasse
  - alerte/non-controle-par-son-job
  - alerte/plafond-releve-16-10
  - audit/standard
---

# 2026-10-16_veille_ai-act

Document source : [[2026-10-16_veille_ai-act.docx]]

## Résumé

**Cette édition n'a jamais été contrôlée par son propre job, et elle n'est pas publiée : le job est mort sur son plafond de coût, en pleine vérification.** Mesures du créneau de 9h03 : `is_error=True`, `subtype=error_max_budget_usd`, **3,2339 $ pour un plafond de 3,00 $ — 108 %**, **34 tours**, `stop_reason=tool_use`. Le `.docx` de 17 159 octets est sur le disque, **non suivi par git**, et le log ne porte **aucune** trace d'un contrôle lancé : ni `controle_attributions.py`, ni l'étape 5 bis, ni `non_regression.sh`. Tous les verdicts de cette fiche sont donc les miens, rejoués à la main après coup, et non ceux du job.

**C'est le troisième dépassement de cette famille, et le deuxième à survenir après un durcissement de prompt.** Le 08/10/2026, `astrologie-karmique` mourait à **3,0218 $ pour 3,00 $ (101 %)**, également en `stop_reason=tool_use`, également après avoir écrit un livrable complet — son plafond fut porté à 5 $ le jour même, et la leçon 11 d'hier a coûté **2,8591 $**, ce qui aurait crevé l'ancien plafond. Le prompt d'`ai-act` a été durci le **09/10/2026** (39 464 → 56 742 octets, cinq motifs ajoutés), puis allégé à 45 803 en sortant `controle_ai_act.py`. **Le durcissement a été payé, le plafond n'a pas bougé.** Trajectoire à vérifier sur les logs : c'est le même scénario annoncé pour astrologie une semaine avant qu'il ne se produise.

**Les contrôles communs sont verts, et les six citations sont appariées au mot.** `controle_attributions.py` rend **exit 0, 0 problème bloquant** ; les **quatre citations anglaises** et les **deux françaises** sortent toutes en `OK`, appariées à leur page — trois titres d'articles de l'IAPP, la phrase de la Commission *« The EU has the first law in the world that addresses systemic risk from AI »*, le fil « Publication 09 October 2026 » et la phrase de la CNIL. `controle_decompte.py` rend **COHÉRENT** (5 ✅ · 1 ⚠ · 2 ⛔ · 5 consultées · 13 tentées). `controle_edition_precedente.py` rend **exit 0** : aucune correction du 09/10 n'est rejouée, son motif ① ayant réellement travaillé — 64 citations d'origine dans le journal de N-1, 3 retenues, 2 jetons distinctifs examinés.

**Et une correction du 12/10 a tenu, ce qui est le contraire d'un rejeu.** La note cite la CNIL : *« Une version amendée du RIA a été **adopté** le 24 juillet 2026 »* — avec la faute d'accord de la CNIL, conservée. C'est exactement l'objet de la correction du 12/10/2026 sur l'édition du 11/09, où « adoptée » avait été remis en « adopté » parce qu'une citation qui corrige silencieusement sa source n'est plus littérale. **Quatre semaines plus tard, la série écrit la forme juste, et B-FR l'apparie en `OK`.**

**L'étape 5 bis, elle, REFUSE la note — et trois de ses quatre refus sont des erreurs d'appariement de lien, vérifiées une par une.** ⛔ Elle reproche l'absence de « EU AI Act » et de « Publication 09 October 2026 » sur `digital-strategy.ec.europa.eu/en/news/special-meeting-ai-scientific-panel`. Mesure : ce nom d'acte appartient dans la note à **une autre adresse** — `ai-act-service-desk.ec.europa.eu/en/ai-act/timeline/timeline-implementation-eu-ai-act`, où il figure jusque dans l'URL ; et la chaîne « Publication 09 October 2026 » est **littéralement présente** sur `commission-holds-special-meeting-scientific-panel-frontier-ai-safety-and-risks`, l'autre page de l'événement. **Les deux contrôles se contredisent sur cette chaîne, et c'est la passe B-FR qui a raison** : elle l'apparie en `OK` à la bonne page, que l'étape 5 bis n'a pas regardée. Les deux URL existent, répondent en 200, et portent deux titres distincts — « Special meeting of the AI Scientific Panel » et « Commission holds special meeting of Scientific panel on frontier AI safety and risks ». Il n'y a pas de soft 404 : il y a **deux pages voisines et un motif qui prend la mauvaise**, exactement la faiblesse déjà réparée le 09/10 sur le motif (2) du même contrôle, qui cherchait l'adresse ailleurs qu'où elle est.

**Le quatrième refus est défendable, et c'est la seule réserve de fond de cette édition.** Le ¶112 écrit : *« Legifrance.gouv.fr requiert JavaScript (retour : 44 caractères). Sources secondaires consultées via WebSearch signalent que le DDADUE serait toujours en première lecture à l'Assemblée nationale… »* Le mode conditionnel tient lieu de réserve et l'illisibilité de la source primaire est déclarée — mais **aucune source secondaire n'est nommée** : « via WebSearch » est une méthode, pas une source. Le ¶48 porte la même affirmation avec une réserve mieux formée (*« non vérifié à source primaire lors de cette exécution »*). **La claim sur l'état d'avancement du DDADUE est donc à prendre comme non vérifiée.**

**Six des sources de cette note ne prouvent rien, et le verdict « 0 bloquant » doit être lu à cette lumière.** Quatre pages rendent **0 octet après trois essais** : `eur-lex.europa.eu/…CELEX:32026R1744` (HTTP 202, le comportement connu d'EUR-Lex), `consilium.europa.eu/en/press/press-releases/` (403), `legifrance.gouv.fr` (403) — et une **URL malformée**, `https://www.legifrance.gouv.fr,` avec sa virgule collée, que curl rejette en code 3. Deux autres sont sous ou au ras du plancher de façade : `ai-act-service-desk…/timeline` à **2 760** caractères utiles, et `commission-holds-special-meeting…` à **2 984 — seize sous le seuil de 3 000**. ⚠️ **Une page tronquée rend indiscernables une citation absente et une citation non lue** : c'est la règle du 12/10, et c'est précisément sur la seconde de ces deux façades que l'étape 5 bis a cru lire une absence.

**La passe D ajoute deux réserves qui sont l'instrumentation du document, pas son contenu.** Elle signale « **403** » — tiré de *« ⛔ consilium.europa.eu/en/press/press-releases/ — HTTP 403 »*, soit **un code de statut HTTP lu comme une valeur chiffrée attribuée** — et « **26 012** », le compte de caractères que la note annonce pour une de ses pages. La seconde est la pathologie mesurée hier sur astrologie-karmique n°11 (26 réserves sur onze leçons, aucune n'étant un défaut) ; **la première est nouvelle**. Même remède que le 11/10 pour les marqueurs : exempter les nombres qui ne vivent que dans une annotation d'instrumentation.

🟢 **Et l'exemption de ⑩ posée hier a passé sa première épreuve en production.** Elle a mordu **deux fois** sur cette édition fraîche — ¶44 et ¶84 —, nommant à chaque fois `iapp.org/news/` comme page d'index dont la taille n'est pas une propriété du document. Sans elle, le compte des refus de l'étape 5 bis aurait pu être de cinq. C'est la validation sur une édition neuve que la règle du 14/10 exige, et qu'un balayage rétrospectif ne donne pas.

### Requêtes passées pour cet audit

Profondeur **standard** : les pages lisibles ont été aspirées sur disque et interrogées par appariement exact, aucune n'est entrée en contexte. Ce qui n'a pas été interrogé n'a pas été vu.

| requête | degré obtenu | source |
|---|---|---|
| `Publication 09 October 2026` | **① littéral** | `commission-holds-special-meeting-…` |
| `EU AI Office` | **① littéral** | idem |
| `EU AI Act` · `AI Act` | ④ absent des **deux** pages digital-strategy | — |
| `artificial intelligence act` | ④ absent — la page écrit *« Scientific Panel on artificial intelligence (AI) »* | idem |
| `scientific panel` | ② graphie (casse) | idem |
| titres servis des deux URL | **deux pages distinctes, 200, pas de soft 404** | digital-strategy ×2 |
| 4 citations anglaises · 2 françaises | **toutes `OK`** par les passes B et B-FR | iapp · commission · cnil |

**Non interrogé** : les quatre pages illisibles (EUR-Lex 202, Consilium 403, Legifrance 403, URL malformée) — rien n'en sera conclu, dans un sens ni dans l'autre ; la claim DDADUE, dont la source primaire est inaccessible et les sources secondaires non nommées ; et le contenu réel des deux façades au-delà des chaînes testées ci-dessus.

## Notes liées

- **⬅️ Précédente** · [[2026-10-09_veille_ai-act.fiche]]

- **➡️ Suivante** · vendredi **23/10/2026** à 9h03. ⚠️ **À DÉCIDER AVANT** : le plafond est toujours à **3,00 $** et cette édition a coûté **3,2339 $**. Rejouer à l'identique échouera pareil — c'est ce que le runner écrit lui-même (*« arrêt des tentatives : rejouer à l'identique échouerait pareil »*). Les deux issues sont : **relever le plafond** comme le 08/10 l'a fait pour astrologie, ou **alléger le prompt**. ⚠️ Et le précédent est documenté : pour astrologie, le 86 % du 01/10 avait été consigné sans qu'aucune conséquence en soit tirée, et le dépassement est tombé le créneau suivant. **Ici le 108 % est déjà consommé.**

- **🔗 Pont** · [[2026-10-15_lecon-astrologie-karmique_11_aspects-noeuds-carre-nodal-configurations]] — même semaine, même pathologie de passe D (la métrologie du document lue comme une valeur attribuée), et le contre-exemple du plafond : relevé à temps pour astrologie, pas pour ai-act

- **🔗 Pont** · [[2026-10-14_veille_SERAFIN-PH.fiche]] — l'autre veille de la série institutionnelle dont des claims reposent sur une page que le contrôle a déclarée « consultée » sans la lire : là une coquille anti-bot en HTTP 200, ici deux façades à 2 760 et 2 984 caractères

- **🗂️ Dossier** · série **ai-act**, édition du **16/10/2026**. 🟢 **PUBLIÉE LE 16/10/2026 PAR DÉCISION EXPLICITE, AVEC ALERTE.** Son job ne l'avait pas publiée — il est mort sur son plafond en pleine vérification, sans lancer **aucun** contrôle. Les verdicts de cette fiche sont donc **les miens**, rejoués à la main : 0 bloquant, 6/6 citations appariées, décompte cohérent, aucun rejeu de l'édition précédente. ⚠️ **DEUX RÉSERVES NOMMÉES, à traiter si le document est corrigé** : ① la claim sur l'état d'avancement du **DDADUE** repose sur des « sources secondaires consultées via WebSearch » **non nommées** — à prendre comme non vérifiée ; ② l'**URL malformée** `https://www.legifrance.gouv.fr,`, dont la virgule collée fait rendre curl 3. 🔵 **Et le plafond a été relevé de 3 à 5 $ le jour même** pour que le créneau du 23/10 ne meure pas de la même façon. 📌 **Trois pistes mesurées ici** : ① faire pointer les motifs (1) et (2) de l'étape 5 bis sur **l'adresse que la note associe à la citation**, et non sur un lien du paragraphe ou de ses voisins — trois refus sur quatre viennent de là, et la passe B-FR, elle, apparie correctement ; ② exempter de la passe D les nombres d'**instrumentation** — comptes de caractères et **codes HTTP** —, comme le 11/10 a exempté ceux des marqueurs ; ③ corriger l'**URL malformée** `https://www.legifrance.gouv.fr,`, dont la virgule collée fait rendre curl 3 et gonfle d'une unité le compte des pages injoignables. ⚠️ **À ne pas perdre si le document est corrigé** : la citation CNIL doit garder « adopté » — la faute d'accord est celle de la CNIL, et c'est l'objet de la correction du 12/10/2026.
