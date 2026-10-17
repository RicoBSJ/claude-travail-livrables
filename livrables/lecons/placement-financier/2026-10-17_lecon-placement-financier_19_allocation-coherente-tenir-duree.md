---
type: fiche-document
source: 2026-10-17_lecon-placement-financier_19_allocation-coherente-tenir-duree.docx
date_creation: 2026-10-17
date_lecon: 2026-10-17
parcours: placement-financier
numero: 19
statut: parcours-actif
tags:
  - parcours/placement-financier
  - registre/perso
  - theme/allocation-actifs
  - theme/horizon-placement
  - theme/trois-seaux
  - theme/reequilibrage
  - theme/glidepath
  - source/amf
  - source/abe-infoservice
  - source/lafinancepourtous
  - audit/standard
---

# 2026-10-17_lecon-placement-financier_19_allocation-coherente-tenir-duree

Document source : [[2026-10-17_lecon-placement-financier_19_allocation-coherente-tenir-duree.docx]]

## Résumé

**Dix-neuvième leçon sur vingt, produite par une exécution propre, et le document le plus sain de la semaine sur le plan mécanique.** Le job a rendu `success` à **1,3586 $ pour un plafond de 3,00 $ — 45 %**, en **37 tours**, `stop_reason=end_turn`, et son auto-push a publié le livrable sans intervention. ㊳, rendu bloquant la veille, est resté muet : c'est exactement son comportement attendu sur un run réussi, et c'est sa première rencontre avec un livrable sain. La leçon traite l'allocation cohérente avec l'horizon — bandes par profil, stratégie dite des trois seaux, règles de pouce de désensibilisation, rééquilibrage à seuil de dérive — en 18 991 octets.

**Les contrôles communs sont verts sans réserve, et ses cinq sources répondent toutes.** `controle_attributions.py` rend **exit 0, 0 problème bloquant** ; la passe **A6 ne trouve aucun lien mort** et les cinq adresses listées reviennent en **HTTP 200**, de 5 944 à 25 715 caractères utiles — **aucune façade**. Les passes B, B-NOM, C, C2 et D rendent **zéro** ; B-FR compte deux candidats, « seau court terme » et « trois seaux », tous deux des **termes de moins de quatre mots sans source nommée**, que la passe écarte par une règle qu'elle annonce dans son propre en-tête. `controle_clauses_parcours` : **annoncé 20 · réels 19 · clause oui · limite oui**.

**Le garde-fou du parcours est tenu trois fois, et c'est plus que le minimum.** Une clause formelle — *« Cette leçon relève de l'éducation financière générale. Elle n'est en aucun cas un conseil en investissement personnalisé. Tout placement comporte un risque de perte en capital »* —, un avertissement attaché à l'exemple chiffré lui-même — *« Ces exemples sont pédagogiques, non une recommandation — un CGP agréé est indispensable pour une décision réelle »* —, et une réserve sur l'analogie employée. **AMF** est cité neuf fois, **CIF** trois fois. C'est la contrainte qui compte le plus sur ce parcours, et elle n'est pas reléguée en bas de page.

**Les six calculs de l'exemple chiffré sont exacts, et c'est une vérification qu'aucun contrôle du dépôt ne fait.** `20 000 × 1,03^7 = 24 597,48` pour 24 597 annoncés · `30 000 × 1,05^7 = 42 213,01` pour 42 213 · `55 000 × 1,20 = 66 000` · le rééquilibrage (total 111 000, cible 55 % = 61 050, vente de **4 950 €**) · `32 000 + 8 000 = 40 000` · et la règle « 100 − âge » qui donne bien **39 %** d'actions à 61 ans. ⚠️ **Et la passe D rend zéro à bon droit, contrairement à ce que j'avais soupçonné** : elle extrait 40 candidats et 77 pourcentages du corps, mais aucun ne vit dans une phrase portant un marqueur d'attribution — parce que ce sont des **hypothèses et des calculs propres à la leçon**, non des faits prêtés à une page. Son silence est donc juste, et non une cécité de plus.

**Le renvoi à la leçon 15 est exact, et c'est le seul du document.** *« Les biais (aversion aux pertes, panique en période de baisse) sont bien documentés (leçon 15) »* : vérifié sur le `.docx` de la n°15, qui porte les deux termes **au mot**. Après quatre documents de la semaine qui se sont trompés sur ce qu'ils résumaient — un manque déclaré à tort, un chiffre contredisant sa leçon 9, un renvoi à une leçon 2 muette, une dérive de vocabulaire —, celui-ci ne se trompe pas. ⚠️ Mais il ne renvoie **qu'une fois** : à deux leçons de son bilan, un parcours de vingt leçons sur l'épargne pourrait relier davantage.

🔴 **LE SEUL VRAI DÉFAUT EST UNE FAMILLE D'ATTRIBUTIONS À PERSONNE, ET AUCUN CONTRÔLE DU DÉPÔT NE LA REGARDE.** Quatre formulations prêtent une règle à une autorité qui n'est jamais nommée : *« **Règle pratique couramment citée** : réduire l'allocation actions de 5 % par an pendant les années précédant l'échéance »* (deux fois), *« un profil équilibré à dynamique modéré (40–60 % actions) est **généralement considéré comme cohérent dans la littérature** »*, et *« **La plupart des praticiens** suggèrent d'utiliser la règle des 110 ou 120 moins l'âge »*. **Mesuré sur les cinq pages aspirées : « 110 moins l'âge », « 120 moins l'âge » et « 100 moins l'âge » sont absents des cinq ; « réduire l'allocation actions » n'y figure littéralement nulle part.** Ces règles existent dans la pratique — ce n'est pas de l'invention —, mais **la leçon les source à un consensus qu'aucune de ses pages ne porte**.

**Et c'est un angle mort structurel, pas un oubli du contrôle.** Les passes B et B-FR vérifient ce qui est **entre guillemets** ; B-NOM les affirmations prêtées à une source **nommée** — « selon X », « (X) », « X indique » ; la passe D les chiffres voisins d'un marqueur d'attribution. **Une affirmation attribuée à personne échappe aux quatre**, et c'est précisément le mouvement rhétorique dominant de cette leçon. C'est le pendant du trou mesuré trois fois cette semaine sur les bilans : là, aucun contrôle ne compare un bilan aux leçons qu'il résume ; ici, **aucun contrôle ne compare à quoi que ce soit une règle attribuée à tout le monde et à personne**. 📌 Piste bornée : signaler les formulations d'autorité diffuse — « couramment cité », « généralement considéré », « la plupart des praticiens », « il est admis » — comme ㉜ signale une citation d'ouvrage : **non bloquant**, et levé par une **déclaration** ou par une source nommée.

⚠️ **Une note de registre** : parmi quatre sources institutionnelles ou éducatives — AMF, ABE Info Service, La Finance pour Tous deux fois —, `assurance-vies.net` est un **site commercial**, et c'est de loin la page la plus longue (**25 715 caractères** contre 5 944 à 11 915 pour les autres). Elle n'est pas fautive et rien n'en est mal cité, mais sur un parcours d'éducation financière le poids relatif des registres mérite d'être vu.

### Requêtes passées pour cet audit

Profondeur **standard** : les cinq pages ont été aspirées sur disque et interrogées par appariement exact, aucune n'est entrée en contexte.

| requête | degré obtenu | source |
|---|---|---|
| `horizon de placement` | **① littéral** | lafinancepourtous (horizon) |
| `110 moins l'âge` · `120 moins l'âge` · `100 moins l'âge` | **④ absent des cinq pages** | — |
| `réduire l'allocation actions` | ④ absent — la page voisine parle de *« tyrannie du calendrier »* | assurance-vies |
| `trois seaux` | ④ absent — cadrage propre à la leçon | — |
| `aversion aux pertes` · `panique` | **① littéral** dans la **leçon 15** | `.docx` du parcours |
| six calculs de l'exemple chiffré | **tous exacts** (recalculés) | — |
| 5 adresses de la section Ressources | **toutes HTTP 200**, 5 944 à 25 715 car. utiles | — |

**Non interrogé** : les bandes d'allocation par profil (0–10 %, 60–70 %, 20–30 %…), qui sont des choix pédagogiques et non des faits ; le contenu des pages au-delà des chaînes ci-dessus ; et la pertinence patrimoniale des recommandations, qui n'est pas du ressort de cet audit et que la leçon renvoie elle-même à un professionnel agréé.

## Notes liées

- **⬅️ Précédente** · [[2026-10-10_lecon-placement-financier_18_droits-retraite-reconstitution-estimation]]

- **➡️ Suivante** · leçon **20 / 20**, samedi **24/10/2026** à 8h03 — le **BILAN**, après quoi la clause ⛔ **PARCOURS FERMÉ — 20 LEÇONS** mord et le job devient supprimable en une commande. ⚠️ **C'est la forme la moins contrôlable du dépôt** : les trois bilans du 12 au 14/10 se sont chacun trompés sur le contenu des leçons qu'ils résumaient, et un bilan sans guillemets met hors jeu cinq passes sur dix. **La n°19 ne se trompe pas sur son unique renvoi : c'est le minimum à exiger de la 20, qui en portera vingt.** 📌 Suppression ensuite : `outils/scripts/supprimer_job.sh placement-financier-lecon --confirmer`, qui refuse tant que les leçons réelles sont sous le compte annoncé

- **🔗 Pont** · [[2026-09-19_lecon-placement-financier_15_biais-comportementaux-epargnant]] — la leçon que celle-ci cite, et le lien est vérifié au mot : le plan d'allocation est présenté comme le dispositif qui contient les biais **avant** qu'ils ne surviennent

- **🔗 Pont** · [[2026-10-16_veille_ai-act.fiche]] — l'inverse exact sur le plan mécanique : là un job mort sur son plafond, zéro contrôle lancé, quatre refus dont trois artefacts ; ici un run à 45 % du plafond, tous les contrôles verts et aucune réserve. **Les deux documents du même dépôt, à un jour d'écart**

- **🗂️ Dossier** · parcours **Placement financier**, leçon **19 / 20**. 🟢 **Rien à corriger dans ce document.** Le seul défaut relevé — les règles attribuées à un consensus que les sources ne portent pas — est **une famille, pas une erreur de fait** : les règles sont réelles, c'est leur attribution qui est vide. 📌 **Et c'est un angle mort du dépôt, pas un manquement du job** : aucune des quatre passes d'attribution ne regarde une affirmation prêtée à personne. ⚠️ **À ne pas perdre si le document est corrigé** : les trois clauses de non-conseil, et l'exactitude des six calculs. 🔵 **Trois fois dans cet audit, c'est ma propre mesure qui était fautive** : j'ai retapé trois adresses depuis un affichage tronqué à 100 caractères et déclaré trois 404 — les URL du document sont justes et A6 avait raison ; j'ai soupçonné la passe D d'une cécité alors que son silence est fondé ; et j'ai failli accuser B-FR de compter sans rien dire, alors que sa règle des quatre mots est écrite dans son en-tête.
