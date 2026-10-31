---
type: fiche-document
source: 2026-10-30_veille_ai-act.docx
date_creation: 2026-10-30
date_veille: 2026-10-30
veille: ai-act
statut: veille-active
tags:
  - veille/ai-act
  - registre/pro
  - concept/transposition-nationale
  - concept/huderia
  - concept/responsabilite-civile-ia
  - concept/article-50-transparence
  - source/nicfab
  - source/edps
  - source/gazzetta-ufficiale
  - source/cnil
  - theme/trois-noms-propres-faux-dans-une-source-juste
  - theme/eurodepute-substitue-et-change-de-groupe
  - theme/source-primaire-declaree-403-et-lisible-par-aspirer
  - theme/confirmation-attribuee-a-la-mauvaise-page
  - theme/cinq-passes-inertes-faute-de-citation
  - theme/deux-tours-pour-trois-dollars
  - theme/tours-mini-ne-mesure-plus-le-travail
  - theme/facade-de-697-caracteres-non-declaree
---

# 2026-10-30_veille_ai-act.fiche

Document source : [[2026-10-30_veille_ai-act.docx]]

## Résumé

**Tous les contrôles sont verts, et trois noms propres sont faux — dont un député européen remplacé par une autre personne, du groupe politique opposé.** `exit 0`, une tentative, **11 liens testés · 9 retenus · 2 écartés (403×2)**, décompte `COHÉRENT`, passe A `0 bloquant`, **5 bis : les onze motifs OK** avec l'exemption ⑩ qui joue correctement sur `iapp.org/news`, intégrité XML conforme (24 liens, 89 paragraphes, marge 65). Le document est par ailleurs **honnête sur son instrumentation** : les tailles de page qu'il annonce sont de vraies mesures — NicFab **67 329** ✓ exact, CNIL Q/R **26 014** ✓ exact, CNIL thématique **8 270** ✓ exact, et les trois autres à 2 ou 40 caractères près, l'écart d'une page qui bouge. Son « 2 décembre 2026 — dans 33 jours » est juste au jour près.

**L'article italien est une traduction fidèle et précise, et c'est la meilleure page du document.** La newsletter source écrit : *« On 23 October 2026 Legislative Decree No 179 of 7 October 2026, published in Official Gazette No 234 of 8 October, entered into force. It adapts Italian law to Regulation (EU) 2024/1689 as regards the powers of national authorities and the use of artificial intelligence in training »* — et le document rend les **trois** dates exactement, avec le bon objet. ⚠️ **Et ma première lecture était fausse** : j'avais vu dans l'adresse ELI `…/2026/10/08/…` une date **hors de la fenêtre** 23-30/10 et commencé à y voir un fait placé à tort dans la semaine. Le document dit précisément ce qu'il faut — décret du 7 octobre, publié le 8, **entré en vigueur le 23** —, et c'est l'entrée en vigueur qui est le fait de la fenêtre. `179/2026`, `234`, `HUDERIA`, `CDNET`, `170`, `Strasbourg`, `GPT-6.1 Sol`, `Astra`, `Norforge`, `Cairn`, `van Sparrentak`, `Lagodinsky`, `Arba Kokalari` : **tous ① LITTÉRAL** sur la newsletter.

**🔴 Mais dans la même parenthèse, deux députés sur quatre sont faux, et la source les écrivait justes.** Le document écrit : *« des eurodéputés (dont **Lara Comi**, **Leonardo Benifei**, Kim van Sparrentak et Sergey Lagodinsky) ont demandé à la Commission de soumettre de nouvelles règles sur la responsabilité civile »*. La newsletter écrit : *« Socialists and Greens (among them **Alex Agius Saliba**, **Brando Benifei**, Kim van Sparrentak and Sergey Lagodinsky) asked the Commission to table new civil liability rules for AI »*. Mesuré sur les **sept pages lisibles** du document : **« Lara Comi » → ④ ABSENT, 0 mot plein sur 2**, tandis que **« Alex Agius Saliba » → ①** et **« Brando Benifei » → ①**. ⚠️ **Et la substitution n'est pas neutre politiquement** : le paragraphe oppose les Socialistes et Verts, qui réclament les règles, au PPE qui les juge inutiles — et Lara Comi est une élue **du PPE**, placée dans le camp adverse. Le prénom de Benifei est faux là où la page portait le bon. **« Benifei » seul s'apparie en ①** : un contrôle par jetons ne pouvait pas voir l'erreur, seule la lecture de la fenêtre l'a montrée.

**🔴 Et deux affirmations n'ont de source nulle part dans le document.** *« dont OpenAI et **Anthropic**, annoncé le 14 octobre 2026 »* : **« Anthropic » compte 0 occurrence sur les sept pages lisibles**, et **0** dans les trois éditions antérieures de la série (16, 17 et 24/10) — l'affirmation n'a ni source listée ni antécédent. Et *« avec un **réseau de correspondants** AI Act désormais actif »* : **« correspondent » compte 0 occurrence sur la newsletter ET 0 sur la page EDPS**, dont le seul « network » est un *« DPO network list »* de navigation. Ces deux détails sont vraisemblables et bien tournés ; c'est exactement ce qui les rend coûteux.

**🔴 La source primaire déclarée inaccessible est lisible par le dépôt lui-même, et elle portait le fait mot pour mot.** Le document écrit *« EDPS — Page AI Act (HTTP 403 au test direct ; contenu confirmé par la newsletter NicFab) »*. Mesuré **dans la même minute**, sur la même adresse : la commande que le prompt prescrit — `curl -L --max-time 20 --cacert "$CA" -A "Mozilla/5.0"` — rend **HTTP 403, 118 octets** ; **`aspirer.py` rend HTTP 200 · 54 430 octets bruts · 7 428 caractères utiles**, et `controle_attributions.py` l'a lue de la même façon. 🔴 **Et cette page porte le fait marquant n° 3 littéralement** : *« **EDPS Newsletter 123 out now** · 27 October 2026 · In this edition, find out why cyberattacks so often start with us in our latest podcast episode, and hear how **the AI Act's transparency obligations are being put into practice across the EU institutions** »*. ⚠️ **Le fait est donc VRAI et de source primaire — et le document le fait passer par le mauvais chemin** : la section EDPS de la newsletter NicFab ne parle pas de transparence de l'AI Act, elle contient deux items, *« Cybersecurity and the human factor: the EDPS's new podcast episode »* (23 octobre, mois européen de la cybersécurité) et *« ARETE: assessing the risk to individuals in personal data breaches »*. **La « confirmation par la newsletter » n'existe pas, alors que la confirmation primaire était à portée d'`aspirer.py`.** C'est le défaut du 20/10 par un bout neuf : là, un `000` faisait écarter une source valide ; ici c'est un **403 rendu par la seule commande prescrite**, quand l'autre outil du même prompt passe.

**⚠️ Et la vraie source primaire du décret italien est une façade de 697 caractères, non déclarée.** `gazzettaufficiale.it/eli/id/2026/10/08/026G0158/SG` rend **200 · 11 296 octets bruts · 697 caractères utiles** — un bandeau de navigation (*« Gazzetta in fase di caricamento »*), rien du décret. La passe A le signale (`<-- SOUS 3000 : facade, ou page rendue en JS ?`), non bloquant. Le document **déclare** ses deux `403` et ses deux `202` EUR-Lex, ce qui est la bonne pratique — mais pas cette façade-là, et c'est la seule page qu'il présente comme la source officielle du fait n° 1.

**🔴 La raison structurelle pour laquelle trois noms faux sont passés est mesurable : ce document ne cite rien, donc il n'y a presque rien à contrôler.** `controle_attributions.py` annonce **cinq passes INERTES sur dix** — `B` (0 citation anglaise de six mots ou plus), `B-FR` (0 citation française), `C`, `C2` et **`D` (0 valeur chiffrée en contexte d'attribution)** —, et sa seule sortie est un **`B-NOM` « À RELIRE » non bloquant** sur la newsletter EDPS, classé *« page(s) en anglais, 6 mots pleins sur 13 — traduction, non tranché »*. Le dépôt vérifie des **citations** et des **chiffres attribués** ; un nom propre dans une parenthèse n'est ni l'un ni l'autre, et **aucun motif du dépôt ne confronte un nom propre à la page qui est censée le porter**. ⚠️ Autrement dit : **la surface de contrôle d'un document est proportionnelle à ce qu'il cite**, et une veille écrite entièrement au style indirect, chaque fait suivi d'une simple ligne « Source : <lien> », désarme presque tout l'appareil. Le rappel du script est exactement à sa place : *« Une passe inerte n'est PAS une passe réussie : elle n'a rien cherché. »*

**🔴 Et c'est une récidive que le journal de l'édition précédente avait déjà nommée, en disant que rien ne pouvait la voir.** Le motif ① du journal du 24/10 : *« Organisateur inexistant. La note nommait « Poitiers Métropole » comme troisième organisateur de la Journée RGPD de la CNIL. Le mot « Métropole » compte ZÉRO occurrence sur cette page […] **Aucun contrôle du dépôt ne pouvait voir** »*. **Cinq jours plus tard, trois noms propres faux dans la même série.** `controle_edition_precedente` rend `OK — aucun rejeu` : littéralement juste — ce ne sont pas les mêmes jetons — et aveugle à la **classe**. 🟢 À l'inverse, la correction ④ du 24/10 a **tenu** : le document distingue bien le règlement **2026/1744** (« AI Omnibus », qui a décalé les échéances de décembre 2027 et d'août 2028) de l'« Omnibus numérique » du Conseil, les deux instruments que N-1 confondait. Et sa déclaration *« aucun des faits de la semaine précédente (EN 18286, Omnibus numérique) n'est répété »* est **vraie** : les deux seules occurrences de ces chaînes dans le document sont **dans la phrase qui l'affirme**. ⚠️ **J'avais commencé à l'accuser sur un `grep -c` à 1 avant de regarder où tombait l'occurrence** — troisième fois dans la séance.

**⚠️ Enfin, une anomalie de mesure qui touche un garde-fou du dépôt : ce run a coûté 3,2958 $ en DEUX tours.** Trajectoire de la série : **27 · 31 · 34 · (interrompu) · 90 · 2 tours**, pour des `out` de **25 424 · 34 980 · 72 205 · — · 43 093 · 2 624** et des `cache-read` de 1,5 M · 1,4 M · 2,0 M · — · 5,6 M · **99 766**. Un livrable de 16 Ko, 24 liens, 11 URL testées et trois contrôles ne se fait pas en deux tours et 2 624 jetons de sortie : la cause probable est que le travail a été **délégué**, et la mécanique de `run_job.sh` l'explique — `num_turns` et `usage` viennent du **fil principal** de la sortie JSON, tandis que `total_cost_usd` est le coût **de toute la session**. 🔴 **Conséquence sur un garde-fou** : `TOURS_MINI=7` existe pour refuser un « faux succès » — *« un `exit 0` obtenu en moins de 7 tours après un échec n'est pas publié »* —, et ce run est à **2**. Il a publié parce que le garde est conditionné à `ECHEC_ANTERIEUR=1` et qu'aucun `.echec_` n'existait le 30/10. **Le défaut est donc LATENT, pas subi** — mais si une tentative avait échoué d'abord, ce livrable correct et contrôlé aurait été refusé en `exit 7`. **Le nombre de tours ne mesure plus le travail accompli.**

### Requêtes passées

| Source | Requête | Degré |
|---|---|---|
| NicFab #44 (67 329 car.) | `179/2026` · `234` · `HUDERIA` · `CDNET` · `170` · `Strasbourg` | ① ×6 |
| idem | `GPT-6.1 Sol` · `Astra` · `Norforge` · `Cairn` | ① ×4 |
| idem | `van Sparrentak` · `Lagodinsky` · `Arba Kokalari` · `Brando Benifei` · `Alex Agius Saliba` | ① ×5 |
| **les 7 pages lisibles** | **`Lara Comi`** | **④ ABSENT, 0 mot plein sur 2** |
| **les 7 pages lisibles** | **`Anthropic`** | **④ ABSENT** (et 0 dans les éditions des 16, 17 et 24/10) |
| NicFab #44 **et** page EDPS | **`correspondent`** | **0 occurrence sur les deux** |
| page EDPS (7 428 car., **lisible**) | `123` · `Newsletter` · `transparency` · `network` | ① ×4 — la page porte le fait marquant n° 3 **verbatim** |
| page EDPS | commande **prescrite** par le prompt | **HTTP 403 · 118 o** |
| page EDPS | **`aspirer.py`**, même minute | **HTTP 200 · 7 428 car.** |
| Gazzetta Ufficiale | — | 200 · **697 car. utiles** → façade, **non déclarée** |
| EUR-Lex ×2 | — | **HTTP 202**, 0 octet → `NON LUE`, **déclarées** par le document |
| Conseil de l'UE | — | **403**, déclaré |
| tailles annoncées vs mesurées | NicFab · CNIL Q/R · CNIL thème · Commission · aiact.eu · Service Desk | **67 329 ✓ · 26 014 ✓ · 8 270 ✓** · 18 079/18 039 · 16 208/16 210 · 2 758/2 760 |

**Ce que STANDARD n'a pas interrogé** : les deux textes EUR-Lex, en `202` — donc **rien de ce que le document dit du règlement 2026/1744 n'est vérifié à sa source**, exactement la réserve que portait déjà le journal du 24/10 · le communiqué du Conseil de l'UE, en 403 · le **contenu du décret italien lui-même** (sanctions, bac à sable), pris de la newsletter et de son blog, jamais du texte · les **incidents OpenAI et Cairn**, relayés par la newsletter seule, aucune source primaire listée · la question de savoir si le **réseau de correspondants** existe sous un autre nom · et l'origine de la mention **« OpenAI et Anthropic »** du 14 octobre, qu'il faudrait chercher hors du document.

**Mes erreurs, et les trois sont la même** : j'ai soupçonné un fait hors fenêtre d'après la date d'une **adresse** avant de lire le paragraphe qui donne les trois dates justes ; j'ai soupçonné une déclaration de non-répétition fausse d'après un `grep -c` à 1, sans regarder que l'occurrence **était dans la phrase elle-même** ; et j'ai soupçonné le fait EDPS d'être une confusion avec un podcast de cybersécurité, alors que **la page EDPS le porte mot pour mot**. Trois fois, la mesure a démenti le soupçon — et ce qui restait après mesure était un défaut **différent** de celui que je croyais tenir : non pas un fait faux, mais un **chemin de confirmation faux**.

## Notes liées

- **⬅️ Précédente** · [[2026-10-24_veille_ai-act.fiche]]
  **son journal avait nommé exactement ce défaut et constaté que rien ne pouvait le voir.** Motif ① du 24/10 : *« Organisateur inexistant […] Aucun contrôle du dépôt ne pouvait voir »*, pour « Poitiers Métropole » au lieu de « la Communauté urbaine du Grand Poitiers ». Cinq jours après, **trois** noms propres faux. 🟢 Sa correction ④ en revanche **tient** : la distinction entre le règlement 2026/1744 et l'« Omnibus numérique » du Conseil est juste cette semaine. **Une correction de fait se transmet, une correction de méthode non — seul un contrôle la transmettrait.**
- **🔗 Pont** · [[2026-10-28_veille_SERAFIN-PH.fiche]]
  **deux veilles de la même semaine, deux sources primaires inaccessibles, et deux conduites opposées.** Là-bas `handicap.gouv.fr` rend 200 pour 93 caractères derrière un mur TSPD, et le récapitulatif annonce « contenu repris » ; ici la page EDPS est déclarée **403** alors qu'`aspirer.py` en tire 7 428 caractères et le fait marquant mot pour mot. **Dans un cas on a lu une page qu'on ne pouvait pas lire, dans l'autre on a renoncé à une page qu'on pouvait lire** — et les deux fois le verdict venait d'un code HTTP, jamais d'un contenu.
- **🔗 Pont** · [[2026-10-24_lecon-placement-financier_20_bilan-synthese-feuille-de-route]]
  **le même angle mort, et la même semaine : un contrôle qui apparie des mots ne juge pas une proposition.** Là-bas `B-NOM` a classé `OK` la phrase qui inversait le statut de l'IEFP, parce que ses mots étaient sur la page ; ici `B-NOM` ne relève qu'une attribution, non bloquante, et **cinq passes sur dix sont inertes faute de citation et de chiffre attribué**. **Un document qui ne cite rien n'offre rien à vérifier, et c'est le style indirect qui désarme l'appareil, pas une faille de l'appareil.**
- **🗂️ Dossier** · [[AI-Act_dossier.fiche]]
  à mettre à jour sur six points mesurés : **le décret italien n° 179 du 7 octobre 2026** (GU n° 234 du 8 octobre, en vigueur le **23 octobre**) est la première transposition nationale complète dans un grand État membre, sanctions et bac à sable compris, et **la France n'a pas publié son dispositif** ; **deux composantes du modèle HUDERIA** ont été adoptées par le CDNET les 21-23 octobre à Strasbourg ; **l'article 50 entre en pratique dans les institutions européennes** (EDPS Newsletter 123 du 27 octobre, lisible par `aspirer.py` et non par la commande prescrite) ; **l'échéance du 2 décembre 2026** — interdictions CSAM et deepfakes sexuels non consentis, fin de la période transitoire art. 50 §2 — est le prochain jalon, et **le haut risque annexe III est reporté au 2 décembre 2027** par le règlement 2026/1744, ce qui concerne directement l'aide à la décision en ESSMS ; **la responsabilité civile de l'IA reste un vide juridique**, la proposition de directive de 2022 ayant été retirée et la majorité étant divisée ; enfin **`edps.europa.eu` et `consilium.europa.eu` sont à ajouter à la liste des hôtes qui refusent la commande de test** mais répondent à `aspirer.py` — à vérifier avant de les déclarer inaccessibles.
