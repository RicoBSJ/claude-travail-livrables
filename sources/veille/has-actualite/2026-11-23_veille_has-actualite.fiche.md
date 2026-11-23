---
type: fiche-document
source: 2026-11-23_veille_has-actualite.docx
date_creation: 2026-11-23
date_veille: 2026-11-23
veille: has-actualite
statut: veille-active
tags:
  - veille/has-actualite
  - registre/pro
  - concept/gt-surdicecite
  - concept/calendrier-has
  - concept/salon-services-personne
  - source/has
  - source/flux-rss
  - theme/rattrapage-apres-anomalie-de-plafond
  - theme/faux-succes-sur-un-vrai-travail
  - theme/correction-d-une-erreur-de-deux-editions
  - theme/page-muette-revenue
  - theme/citation-completee-hors-page
  - theme/decompte-de-liens-illisible-au-controle
  - theme/document-non-publie
---

# 2026-11-23_veille_has-actualite

Document source : [[2026-11-23_veille_has-actualite.docx]]

## Résumé

**Ce document est le second de la journée à ce chemin, et il remplace un document fabriqué : le rattrapage a corrigé un incident et il en a produit un autre, bénin.** Le créneau de 8h30 était mort sur une anomalie — 5,0134 $ pour 5,00 $, **1 tour, 4 ms, les quatre compteurs à zéro**, `error_max_budget_usd`, 0 contrôle tracé — et le document qu'il avait laissé sur le disque portait **quatre fabrications mesurées** : une section de continuité attribuant au 16/11 un récapitulatif dont **8 chaînes sur 8** étaient à zéro occurrence dans cette édition, un « 3e signalement consécutif » dont ni le 1er ni le 2e n'existent, une liste de 8 RBPP dite « héritée » **sans un seul titre en commun** avec celle du 16/11, et un agenda du 24-25/11 dont la page citée ne porte **aucune** des dates (`24/11`, `25/11`, `CPEP` → 0 occurrence). Plafond relevé à **6,00 $**, document fabriqué retiré du disque, rattrapage lancé à 13h30.

**Le rattrapage a réussi au sens de l'API et a été retenu par un garde dont le diagnostic est faux.** Mesure : `is_error=False | subtype=success | stop_reason=end_turn`, **4,3183 $ pour 6,00 $ (72 %)**, **6 tours**, 401 524 ms, out 3 098, cache-read 812 366. Puis `⛔ FAUX SUCCÈS À LA TENTATIVE 1 — 6 tour(s), sous le plancher de 7`, exit **7**, `[git] ⛔ PAS DE PUBLICATION`. 🔴 **Et le message du garde affirme une cause qui n'est pas la bonne** : *« celle-ci s'est arrêtée sur un garde-fou (doublon) sans rien regénérer »* — or ce run a régénéré, et les chiffres du dépôt le disent. Une sortie sur doublon coûte **0,1541 $ et 3 tours** (mesures consignées aux lignes 82-100 de `run_job.sh`) ; celle-ci coûte **4,3183 $ et 6 tours en 6 min 42 s**, soit un **facteur 28 sur le coût**. ⚠️ **La calibration de `TOURS_MINI` déclarait cette bande vide** : « 3 tours pour une sortie sur doublon, 27 à 64 pour une génération », d'où `TOURS_MINI ∈ [6, 9]` et la valeur 7. Un run de **6 tours qui génère** tombe exactement dans l'intervalle que la mesure annonçait inoccupé — et le garde le lit comme un skip.

**Le document produit est bon, et c'est la mesure qui le dit : le gate `--docs` sort en 0 et les cinq tailles annoncées sont exactes au caractère.** `controle_attributions.py` : **0 bloquant**, 5 passes inertes, 2 citations `A RELIRE` non bloquantes. `controle_decompte.py` : **exit 0** (contre exit 2 le matin). `controle_edition_precedente.py` : **exit 0**, aucun rejeu, 3 points à relire. `controle_integrite_livrables.py` : 777 suivis, 0 divergence. Et chacune des cinq sources annonce un volume que ma sonde reproduit **exactement** : `p_3081452` **48 281 car. utiles**, `p_3081656` **2 207**, `calendrier-detaille` **19 286**, `p_4554304` **14 776**, `CSMS` **8 210**. C'est le contraire exact du document du matin, qui annonçait **2 274 octets** pour un flux qui en fait 61 386.

**Le fait neuf de la semaine est une correction, et elle est fondée au degré ① : l'appel GT Surdicécité ESSMS n'est pas clos, il court jusqu'au 30/11/2026.** La page `p_4554304`, muette lors des deux éditions précédentes (**3 184 caractères**, rendu JS), est **revenue** : ré-aspirée au frais, `HTTP 200 · 88 517 octets bruts · 14 776 car. utiles`, soit le chiffre exact qu'annonce le document. Elle écrit **`Clôture de l'appel le 30/11/2026`** (① LITTÉRAL), **`Les candidatures doivent être envoyées par courriel au plus tard le 30 novembre 2026`** (① LITTÉRAL) et **`Appel à candidature - Mis en ligne le 07 oct. 2026`** (`07/10/2026` ① LITTÉRAL) ; **`13/11/2026` y est ④ ABSENT**. Or l'édition du **09/11 écrit `13/11/2026` sept fois** et celle du **16/11 cinq fois**, la seconde portant aussi le `3 184` de la page muette. **Deux éditions ont donc annoncé close, sur la foi d'une page illisible, une candidature encore ouverte** — et il reste **7 jours**. ⚠️ Impact direct pour un foyer d'hébergement : le profil recherché inclut les professionnels accompagnant des personnes sourdes-aveugles en ESSMS, le dépôt se fait à `rbpp.surdicecite@has-sante.fr`, et la page précise 8 rencontres de janvier à décembre 2027.

**La continuité, qui était la fabrication la plus grave du matin, est cette fois réelle : les huit RBPP héritées sont bien dans l'édition du 16/11, 8 sur 8.** Vérifié titre par titre — *Vie quotidienne des enfants de 3 à 11 ans (PE)*, *Habitat volet 3*, *Prévention spécialisée*, *Autodétermination et pouvoir d'agir en ESSMS*, *Pair-aidance*, *Bonnes pratiques de simulation en santé*, *Mineurs en situation de prostitution*, *Surdicécité en ESSMS* : **toutes présentes**. Chacune porte sa provenance datée au gabarit que le dépôt exempte (« d'après l'édition du JJ/MM/AAAA de cette veille ») et les trois pages réellement inaccessibles gardent leur `⛔`. Le document ajoute même une **note méthodologique** disant que les informations héritées ne sont pas comptées dans les sources de l'édition — ce qui est la doctrine du dépôt écrite par le job lui-même.

**L'agenda est vérifié au degré ①, et c'est l'autre contraire exact du matin.** Sur le calendrier ré-aspiré au frais : `08h30` ①, `18h` ①, `Salle Amérique` ①, `Porte de Versailles` ①, `Université d'automne` ①, `20 novembre` ①. Le document ne cite plus une seule date que la page ne porte pas, là où celui du matin en avançait trois avec des horaires à la minute.

**Un seul défaut mesuré dans ce document, et B-FR l'a vu sans que j'aie à le chercher : une citation entre guillemets complétée par trois mots que la page ne porte pas.** Le document écrit « Du cahier des charges des SAD à l'évaluation HAS : **deux leviers au service de la qualité** » ; la page écrit « …deux leviers au service **la Haute autorité de santé Anni ...** », c'est-à-dire un libellé **tronqué par la page elle-même**. `chercher.py` rend **④ ABSENT LITTÉRALEMENT, 6 mots pleins sur 7**, et la divergence n'est pas l'apostrophe mais une **substitution de trois mots**. 🟢 `controle_attributions.py` le signale `A RELIRE  Du cahier des charges des SAD à l'évaluation HAS : deux leviers au service d` — non bloquant, ce qui est le bon registre : le support de la page est tronqué, donc le titre complet est **inconnu** et non pas faux. Mais il est entre guillemets, et une citation entre guillemets se prouve au ①. La forme courte, « Du cahier des charges des SAD à l'évaluation HAS », sort en `OK`.

**㊳ accepte ce document alors que le pipeline a refusé de le publier, et c'est un écart structurel qu'il faut nommer.** Mesuré : `controle_livrable_du_job.py` rend **exit 0** sur ce `.docx`, parce qu'il lit la ligne `[diagnostic]` — `is_error=False | subtype=success` — et **ne lit ni la ligne `[retry] ⛔ FAUX SUCCÈS`, ni le `code de sortie : 7` de l'épilogue, ni le `[git] ⛔ PAS DE PUBLICATION`**. Entre « le run a échoué » et « le run a publié » il existe donc un état que ㊳ ne distingue pas : **le run a réussi et le pipeline a refusé de le publier**. C'est la classe du 06/11 (*un run n'est pas une publication*) d'un cran plus loin, et la direction d'erreur est la mauvaise — ㊳ laisserait passer au push un document que `run_job.sh` a explicitement retenu. ⚠️ Le remède est à portée et il est petit : lire le code de sortie de l'épilogue en plus du `[diagnostic]`. **Non fait, non ordonné.**

**Et ㊳ bis est aveugle au décompte de liens de ce run, pour une troisième forme du défaut du 24/10.** Le log porte bien `- 🔗 **Liens** : 5 testés · 5 retenus · 0 écarté`, et le contrôle répond que *« le récapitulatif de son run ne dit pas combien d'URL ont été testées ni écartées »*. 🔴 **Cause isolée en jouant le VRAI motif `LIENS` extrait du contrôle**, et ce n'est pas ce que j'avais d'abord supposé : ni le singulier `écarté`, ni l'absence de `(codes : …)` ne gênent — une ligne **sans gras** finissant sur `0 écarté` rend bien `('5','5','0',None)`. Ce qui échoue est **`**Liens**`** : le gras qui n'entoure que le **mot du champ** place `**` entre `Liens` et son `:`, et le motif commence par `Liens\s*:`. Le correctif du 24/10 traitait la forme **englobante** (`**Liens : … **`), où `Liens : ` reste contigu. ⚠️ Et la direction compte : le contrôle affirme l'absence d'un décompte qui existe, donc **un lien jeté sur un 000 resterait invisible** — exactement ce que le motif du 20/10 existe pour empêcher. **Non corrigé, non ordonné.**

**Le rendement reste le pire de la série, et il s'est amélioré de moitié.** ㊳ ter rend `0,636 $ / 1 000 car. utiles (4,3183 $ · 6 790 car. · 6 tours · 72 % du plafond)`, `rang 5/5 des runs encore mesurables de cette série (médiane des autres : 0,452)`, contre **1,386 $** pour le run du matin. Le rapport à la médiane passe de **3,07 à 1,41**. L'alerte se lève encore — c'est la conjonction « le pire **et** le plus récent » que j'ai bornée le 21/11 — et elle est juste : ce document coûte 41 % de plus par caractère que la médiane de sa série. ⚠️ **Mais le dénominateur est trompeur ici** : 6 790 caractères pour **5 sources lues, une page revenue et une erreur de deux éditions corrigée** n'est pas la même chose que 6 790 caractères de prose. Le rendement mesure le coût par caractère, pas le coût par fait établi.

**Des quatre vérifications prescrites par la fiche du 16/11, trois sont pleinement honorées et la quatrième est écrite mais illisible.** ① Le flux `p_3081656` porte bien **`⚠`** et non `✅`, avec sa mesure (2 207 car.) et la phrase qui le déclasse — *« ne sert plus de source active … depuis au moins le 02/11/2026 »* : prescription tenue au quatrième report. ② Les adresses murées : **la page `p_4554304` est revenue** et est lue à 14 776 caractères, les trois réellement inaccessibles gardant leur `⛔` — c'est mieux que ce que la prescription demandait, puisque le retour a produit la correction du jour. ③ La commission est nommée **comme la page la nomme** : `Commission en charge du social et du médico-social` ① et `CSMS` ① sur la page `c_2859583`. ④ Le récapitulatif porte la forme prescrite, mais `**Liens**` la rend invisible au contrôle. ⚠️ **Et l'auto-évaluation du run est inexacte sur ce dernier point** : il écrit « 4 points prescrits · 3 honorés · 1 écarté (récapitulatif 🔗) » alors qu'il **a bien écrit** le décompte — il s'attribue un manquement qu'il n'a pas commis, et le vrai manquement est de forme.

**Ce qui reste à décider, et ce n'est pas à moi de le trancher : ce document n'est pas publié.** Il est non suivi sur le disque, le pipeline a refusé de le committer, et relancer le job ne peut pas aider — l'anti-doublon verrait le fichier du jour et sortirait en 3 tours, donc de nouveau sous `TOURS_MINI`, donc de nouveau exit 7. Les voies sont : publier à la main après l'avoir relu (ce que `run_job.sh` invite à faire mot pour mot), corriger d'abord la citation complétée, ou retirer le document et rejouer pour ~4,3 $ de plus sans garantie que le prochain run fasse plus de 6 tours.

### Requêtes passées

Pages ré-aspirées **au frais** (le cache portait des copies périmées), une par une, espacées de 15 s, aucune en parallèle, aucune page entrée en contexte.

| Page | Mesure | Annoncé par le document |
|---|---|---|
| `p_4554304` (GT Surdicécité) | HTTP 200 · 88 517 o bruts · **14 776 car.** | 14 776 ✓ |
| `c_2859583` (CSMS) | HTTP 200 · 78 724 o bruts · **8 210 car.** | 8 210 ✓ |
| `c_6025` (calendrier) | HTTP 200 · 152 027 o bruts · **19 286 car.** | 19 286 ✓ |
| `p_3081452` (flux RBPP) | 48 281 car. / 60 498 o | 48 281 ✓ |
| `p_3081656` (flux Actualité) | 2 207 car. / 3 005 o | 2 207 ✓ |

`chercher.py --fichier` sur `p_4554304` (6 requêtes) : `30/11/2026` ① · `30 novembre 2026` ① · **`13/11/2026` ④ ABSENT** · `07/10/2026` ① · `surdicécité` ① · titre de la RBPP ②.

`chercher.py --fichier` sur `c_2859583` (2) : `Commission en charge du social et du médico-social` ① · `CSMS` ①.

`chercher.py --fichier` sur `c_6025` (7) : `08h30` ① · `18h` ① · `Salle Amérique` ① · `Porte de Versailles` ① · `Université d'automne` ① · `20 novembre` ① · **titre long de l'atelier ④ ABSENT LITTÉRALEMENT (6/7 mots)**.

`lire_page.py --autour` : `candidatu` sur `p_4554304` (11 occurrences), `Salle Am` sur `c_6025` (2).

Mesures hors réseau : les 8 titres de RBPP cherchés un par un dans le 16/11 ; occurrences de `13/11/2026` dans le 09/11 et le 16/11 ; le motif `LIENS` **extrait du contrôle** et joué sur quatre variantes de la ligne du log ; `MIN_JETONS`, `retenus()` et `noms()` de `controle_noms_propres.py` importés.

Contrôles rejoués sous `env -i` : `non_regression.sh --docs` (exit **0**), `controle_livrable_du_job.py` (㊳ exit 0, ㊳ bis, ㊳ ter), `controle_attributions.py`, `controle_decompte.py`, `controle_edition_precedente.py`, `audit_vault.py`, `non_regression.sh --integrite`.

### Ce que STANDARD n'a pas interrogé

- **Le titre complet de l'atelier HAS du 02/12** reste inconnu : la page du calendrier le **tronque elle-même** (« …au service la Haute autorité de santé Anni ... »). Le vérifier demanderait la page du Salon, que le document ne cite pas.
- **« Aucun compte rendu ni résumé n'était disponible en ligne au 23/11/2026 »** pour l'Université d'automne est une affirmation d'absence, non vérifiable sans une recherche que le document ne cadre pas.
- **Les trois pages `⛔ Page inaccessible`** (Vie quotidienne 3-11 ans, Habitat volet 3, Prévention spécialisée) n'ont pas été sondées : le document ne porte pas leurs adresses, et c'est le défaut de forme que la fiche du 16/11 signalait déjà — l'inaccessibilité n'est pas constatable par le lecteur.
- **La cause de l'anomalie de 8h30** — 5,0134 $ pour 1 tour et 4 ms avec quatre compteurs à zéro — n'est pas élucidée. Deuxième occurrence de cette signature après imac le 08/11, et ce que le log ne porte pas n'y est pas mesurable.
- **Le `17 950` que j'avais relevé ce matin sur le calendrier est élucidé** : c'était une **copie périmée du cache** d'une session antérieure, pas un écart de contrôle. La page fraîche fait bien 19 286 caractères. ⚠️ Et la leçon est que `aspirer.py` rend `♻ déjà aspirée` sans dire l'âge du fichier : une mesure de taille se fait **au frais** ou ne vaut rien.

## Notes liées

- ⬅️ **Précédente** — [[2026-11-16_veille_has-actualite.fiche]]
  **elle obtient enfin ses quatre prescriptions, et l'une d'elles a produit la correction du jour.** ① le flux Actualité porte `⚠` et sa mesure ; ② **la page murée est revenue** — `p_4554304`, de 3 184 à **14 776 caractères** — et c'est ce retour qui a révélé que la clôture du GT Surdicécité est au **30/11** et non au 13/11 ; ③ la commission est nommée `Commission en charge du social et du médico-social (CSMS)`, **① sur sa page** ; ④ le décompte de liens est écrit, mais `**Liens**` le rend illisible à ㊳ bis. 🔴 **Et c'est elle qui portait l'erreur corrigée** : elle écrit `13/11/2026` **cinq fois** et cite le `3 184` de la page muette — la date venait d'une page que personne n'a pu lire, ce que son propre marquage disait. **Le mécanisme qu'elle avait nommé — *« le job relit la note et jamais la fiche »* — n'est donc pas démenti** : ce run a lu la note du 16/11, pas sa fiche, et il a quand même convergé, parce que le retour de la page lui a donné la mesure
- ➡️ **Suivante** — à produire le 30/11/2026
  **quatre choses, et la première est une date qui tombe ce jour-là.** ① **la clôture du GT Surdicécité est le 30/11/2026** : l'édition du 30/11 doit dire si l'appel est clos et, le cas échéant, cesser de le compter parmi les appels ouverts — ne pas reconduire « il reste N jours » ; ② le titre de l'atelier du 02/12 est-il lisible en entier quelque part, la page du calendrier le tronquant (« au service la Haute autorité de santé Anni ... ») — sans quoi **ne pas le mettre entre guillemets** ; ③ le Salon a lieu les 1 et 2/12 : l'édition du 30/11 est la dernière avant l'événement, et son atelier SAD/évaluation HAS est le point le plus utilisable de ces trois semaines ; ④ 🔴 **le décompte de liens doit s'écrire `🔗 Liens :` sans gras autour du seul mot** — mesuré : `**Liens**` rend ㊳ bis muet, et un lien jeté sur un 000 resterait alors invisible
- 🔗 **Pont** — [[2026-11-22_veille_imac.fiche]]
  **les deux documents de la journée illustrent les deux moitiés de la même leçon, et c'est le rapprochement qui la complète.** Là-bas, un faux publié le 15/11 s'est **reconduit** le 22/11 pour un `OK sur ses trois axes`, et le remède a été de confronter le livrable à un **fait mesuré au degré ①** extérieur au corpus. Ici, le document du matin **fabriquait** sa continuité et celui de l'après-midi l'a établie — 8/8 titres réellement dans le 16/11 — **parce qu'une page est revenue et lui a donné une mesure**. Dans les deux cas ce qui tranche est une référence extérieure au corpus ; ce qui diffère est que has-actualite en a une à portée, son édition N-1 étant sur le disque, et que **aucune passe du dépôt ne la lit**
- 🔗 **Pont** — [[2026-11-20_veille_ai-act.fiche]]
  **le document de 8h30 en était la répétition exacte, et celui de 13h30 montre que le remède n'est pas toujours un garde.** Le 20/11 avait rendu **sept bases légales fausses** sur dix — des désignations bien formées et sans référent, `d · e · e bis · e ter · e quater` —, et le remède a été de **verser le fait au prompt** avec un garde d'appariement. Le matin du 23/11 a produit la même forme (un `CPEP` qu'aucune page ne porte, des horaires à la minute), mais le rattrapage l'a dissipée **sans qu'on touche au prompt** : le run a simplement eu 6 tours et des pages lisibles, là où l'anomalie lui en avait laissé **un seul, de 4 ms**. ⚠️ Autrement dit la fabrication du matin n'était pas un défaut de consigne mais **l'effet d'un run qui n'a pas pu travailler** — et c'est une hypothèse, pas une mesure : rien ne prouve qu'un run amputé confabule, c'est la seule différence observable entre les deux
- 🗂️ **Dossier** — [[HAS-actualite_dossier.fiche]]
  à mettre à jour sur cinq points mesurés : ① **la clôture du GT Surdicécité ESSMS est le 30/11/2026**, et les éditions du 09/11 (×7) et du 16/11 (×5) l'annonçaient au 13/11 sur la foi d'une page muette — **première erreur de fait de cette série corrigée par le retour de sa source** ; ② `p_4554304` est **revenue** (3 184 → 14 776 car.), donc une page murée de cette série n'est pas perdue définitivement, contrairement à ce que la fiche du 16/11 redoutait ; ③ **le flux Actualité `p_3081656` est mort depuis 28 mois** (1 item du 09/07/2024) et à **2 207 car.**, sous le plancher de 3 000 : ce n'est plus une source, et le document le dit enfin ; ④ **㊳ ne distingue pas un run qui a réussi d'un run que le pipeline a refusé de publier**, mesuré sur ce document (exit 0 de ㊳ contre exit 7 du job) ; ⑤ **㊳ bis est muet sur `**Liens**`**, troisième forme du défaut du 24/10, et la direction d'erreur est le silence
