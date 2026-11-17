---
type: fiche-document
source: 2026-11-16_veille_has-actualite.docx
date_creation: 2026-11-16
date_veille: 2026-11-16
veille: has-actualite
statut: veille-active
tags:
  - veille/has-actualite
  - registre/pro
  - concept/csms
  - concept/universite-automne-has
  - concept/calendrier-has
  - source/has
  - source/flux-rss
  - theme/prescription-de-fiche-ignoree-par-le-job
  - theme/le-job-relit-la-note-jamais-la-fiche
  - theme/flux-rss-effondre-donne-pour-lu
  - theme/source-inerte-donnee-pour-exploitee
  - theme/perte-de-faits-devenue-acquise
  - theme/facade-au-dessus-du-plancher-du-depot
  - theme/nom-d-instance-reecrit-par-la-note
---

# 2026-11-16_veille_has-actualite

Document source : [[2026-11-16_veille_has-actualite.docx]]

## Résumé

**Tout ce que cette note affirme sur la foi d'une page est exact au degré ①, et son défaut n'est pas dans le document : il est dans le fait que la fiche de l'édition précédente avait prescrit TROIS vérifications nommées, que les trois sont ignorées, et que le mécanisme est mesurable en une commande.** Les douze appariements de citations sortent en ① LITTÉRAL, les horaires et les deux titres de session de l'Université d'automne sont au mot, la semaine creuse est prouvée sur un flux lu, les cinq contrôles sortent en 0, le gate `--docs` accepte, et le run est allé au bout à **64 % de son plafond** en une tentative. Mais la fiche du 09/11 se terminait par trois points à vérifier d'emblée — les quatre adresses murées, le flux Actualité à marquer `⚠` et non `✅`, le nom de la commission — et le document du 16/11 rend **0 adresse revenue, un `✅` sur un flux toujours à un item de 2024, et le même nom réécrit**. Trois sur trois.

**Et le mécanisme n'est pas une négligence de l'agent : le prompt du job lit l'édition précédente par un glob qui EXCLUT les fiches, et le prompt le dit lui-même dans une de ses propres phrases.** Mesuré sur `jobs_config.json` : son étape 7 ouvre sur `1. D'ABORD, relis l'édition précédente de cette note : ls …/sources/veille/has-actualite/*_veille_has-actualite.docx`, un motif qui ne peut pas atteindre un `*.fiche.md`. Recensement du prompt : **`fiche de l'` → 0 occurrence, `la fiche` → 0**, et les **2** occurrences de `.fiche.md` sont des règles de NOMMAGE (« le suffixe est réservé aux fiches Obsidian, et il est EXCLU de la publication automatique »), pas une consigne de lecture. 🔴 **Et la phrase qui nomme le trou est DANS le prompt** : *« La fiche du 02/09 l'avait établi ; la note du 02/09, que tu relis, ne l'a jamais su. »* Le prompt diagnostique exactement l'asymétrie — la fiche sait ce que la note ignore — puis ne la referme pas. **Toute mesure de fiche est donc structurellement hors de portée du job qui écrira l'édition suivante**, et c'est pourquoi les trois prescriptions du 09/11 n'avaient aucun chemin pour arriver.

**Le flux RSS Actualité est toujours mort, remesuré par une sonde du jour, et le document le porte en `✅` pour la deuxième semaine d'affilée.** `feed/Rss2.jsp?id=p_3081656`, sondé seul, faisceau de certificats compris : **HTTP 200 · curl rc 0 · 3 058 octets bruts · 2 207 caractères utiles · UN SEUL `<item>` · `pubDate Tue, 9 Jul 2024 15:09:21`** — *« Accréditation des médecins et des équipes médicales : la HAS vient à votre rencontre »*. Le document écrit `✅ HAS, flux RSS Actualité — lu le 16/11/2026, HTTP 200. Aucune publication concernant le secteur social et médico-social dans la fenêtre.` ⚠️ **L'énoncé est littéralement VRAI et structurellement creux** : un flux qui ne contient qu'un item de juillet 2024 ne PEUT pas contenir une publication du 09–16/11, donc l'absence qu'on y lit est indiscernable d'un flux muet — c'est la règle du 12/10 (une mention absente est indiscernable d'une mention non lue) un étage plus haut, et **2 207 caractères est sous le plancher de façade de 3 000 du dépôt**. 🔴 **Et deux pièces du pipeline se contredisent sur cette page, le document ayant pris le côté optimiste** : `controle_noms_propres.py` rend `1/6 page(s) NON LUE(s)` et la **nomme**, cette page exactement, pendant que le document la compte parmi ses 5 ✅.

**Et ce flux n'a PAS toujours été mort : la mesure sur la série démolit l'hypothèse commode, et il faut le dire.** Recensement des huit éditions qui le citent (28/09 → 16/11) : l'édition du **05/10** en tirait *« seule entrée de la fenêtre, une offre d'emploi (archiviste CDD, 02/10/2026) »*, et celle du **02/11** *« 3 offres d'emploi HAS publiées le 30/10/2026 — hors périmètre ESSMS »*. Le flux servait donc des items **courants** il y a quinze jours. Sa chute est tombée entre le 02/11 et le 09/11, la fiche du 09/11 l'a mesurée à **2 206 caractères et 1 item de 2024** — chiffre que ma sonde d'aujourd'hui reproduit à **un caractère près** —, et la régression est acquise. ⛔ **Ce n'est donc pas une source périmée depuis toujours qu'on aurait recopiée par paresse : c'est une source qui est morte sous le job, et qu'aucun contrôle ne peut déclasser**, puisque `murs_lus.py` exige que le **document avoue le compte** et que le document n'avoue rien — seul le log écrit « 2 207 car. ».

**La semaine creuse est pourtant exacte, et elle tient sur UN seul des deux flux — la note en annonce deux.** `feed/Rss2.jsp?id=p_3081452` (Recommandations et guides), sondé seul aujourd'hui : **HTTP 200 · 61 386 octets · 50 items · item le plus récent du 13 octobre 2026**. L'absence de nouvelle RBPP sur la fenêtre 09–16/11 y est donc **vérifiable**, et le verdict du document est juste. ⚠️ **Mais son « En bref » écrit *« confirmé sur le flux RSS Recommandations et guides ET le flux RSS Actualité de la HAS, lus le 16/11/2026 »*** : la corroboration annoncée est double, la corroboration réelle est simple. Le fait est bon, le sourçage surévalue. 📌 Et une mesure de contexte que la note ne donne pas : sur ce flux vivant, **rien n'a été publié depuis le 13/10**, soit cinq semaines — la « semaine creuse » est en réalité la cinquième d'affilée.

**Les huit adresses perdues le 09/11 ne sont pas revenues, et la perte est désormais ACQUISE : les lignes murées ne portent plus ni ⛔ localisable ni adresse.** Mesuré jeton par jeton sur les deux textes extraits, `p_4159151 · p_3892562 · p_3578307 · p_4549164 · p_4159155 · p_4559635 · p_4549147 · p_4554297` : **0 occurrence dans N-1 (09/11), 0 dans N (16/11)**. La fiche du 09/11 avait établi que quatre de ces adresses venaient de **mes propres corrections des 02 et 03/11**, posées pour que l'inaccessibilité devienne *« vérifiable par quiconque »*, et elle plaçait ce point en tête de ce qu'il fallait vérifier *« avant que l'édition suivante ne recopie la version amputée »*. 🔴 **C'est exactement ce qui s'est produit** : les sept lignes « RBPP en cours d'élaboration » du 16/11 écrivent `⛔ Page inaccessible` **sans aucune adresse** — le lecteur lit une inaccessibilité qu'il ne peut pas constater. Le fait reste vrai (les pages répondaient 200 derrière leur mur au 09/11) ; c'est la **vérifiabilité** qui est perdue pour la deuxième édition consécutive, et la règle en tête du prompt — *« UNE ÉDITION NE PEUT PAS SAVOIR MOINS QUE LA PRÉCÉDENTE (14/09/2026) »* — reste la seule que rien n'instrumente.

**La commission est rebaptisée pour la troisième édition, et le document écrit la seule forme qu'aucune page HAS ne porte.** `Commission sociale et médico-sociale` : **1 occurrence dans la note**, et les formes des pages — `Commission en charge du social et du médico-social`, `Commission CSMS` — à **0 occurrence chacune** dans la note. La fiche du 09/11 avait mesuré l'inverse sur les pages (la forme de la page en ① LITTÉRAL, la forme de la note à 0 sur six pages) et avait listé ce point comme troisième vérification. ⛔ **Et la cécité est mesurée et structurelle, elle ne se répare pas en durcissant une passe** : le nom n'est pas entre guillemets (B et B-FR aveugles), il est cohérent avec lui-même dans le document (B-NOM aveugle), il ne porte aucun chiffre (D aveugle), et `controle_noms_propres.py` l'écarte parce que `commission`, `sociale` et `médico-sociale` existent **tous en minuscules** dans le corpus — c'est le discriminant de casse du 31/10 qui le jette, et c'est la limite mesurée de la méthode « corpus pour dictionnaire ». Le contrôle n'a interrogé **qu'un seul nom** sur ce document, et ce n'était pas celui-là.

**Le document est PLUS SÉVÈRE que le dépôt sur un point, et cela casse une bande que le dépôt croyait vide.** Il déclare `⛔ HAS, appel GT Surdicécité en ESSMS … HTTP 200 mais rendu JS, contenu non lisible (3 184 caractères utiles, probable façade)`. Vérifié : les **cinq** requêtes passées sur cette page (`surdicécité`, `candidature`, `clôture`, `13 novembre`, `groupe de travail`) sortent **④ ABSENT toutes les cinq**, et la fenêtre montre un habillage de site, un formulaire d'identification et un bloc base64 — **c'est bien une façade**. 🔴 **Or 3 184 caractères est AU-DESSUS du plancher de 3 000 du dépôt, et au-dessus de la « bande vide » que le balayage du 05/11 avait mesurée** — façade la plus haute **2 997**, vivante la plus basse **3 077**. Le motif `FAÇADE ?` de `balayer_adresses.py` classerait donc cette page **VIVANTE**. ⛔ **Et relever le plancher est exclu par une mesure de la fiche du 09/11** : la vraie page d'événement CSMS fait **3 693 caractères**, soit **509 de plus** seulement — un plancher qui attraperait ce mur accuserait une page réelle. **Le seul discriminant mesuré reste le mot `Identification`, jamais le volume**, et c'est le document, pas l'outil, qui a eu raison ici.

**Cinq passes sur onze n'ont rien cherché, dont D pour la cinquième édition d'affilée, et c'est la passe qui vérifie les valeurs attribuées.** `controle_attributions.py` : **exit 0, 0 problème bloquant**, 6 ressources listées, 0 page citée hors Ressources, 0 lien mort, 0 hyperlien sans cible — et **5 passes INERTES déclarées** : B (0 citation anglaise), B-NOM, C, C2 et **D (0 valeur chiffrée en contexte d'attribution)**. ⚠️ *Une passe inerte n'est PAS une passe réussie : elle n'a rien cherché* — et une note faite de dates et d'horaires échappe donc entièrement à la seule passe qui confronte une valeur à sa page. **Les quatre horaires et les six dates de ce document ne sont vérifiés par aucun contrôle ; ils le sont par cette fiche.** Son unique réserve B-FR est la **phrase-gabarit** `d'après l'édition du JJ/MM/AAAA de cette veille` — **sixième récurrence** après les 12/10, 19/10, 26/10, 02/11 et 09/11 : le bornage posé le 01/11 pour l'axe ② de `controle_edition_precedente.py` n'a toujours pas été porté à `controle_attributions.py`, et la piste est consignée depuis le 12/10.

**Les trois axes de la relecture d'édition sortent en OK, et l'axe ③ a raison de faire revérifier deux phrases — la réponse est la même que la semaine passée.** `controle_edition_precedente.py` **exit 0** : axe ① aucune correction de N-1 rejouée ; axe ② une formulation à relire (la phrase SERAFIN-PH, 6 mots repris) ; axe ③ **2 phrases d'absence recopiées MOT POUR MOT sans mention d'héritage** — *« Bascule SERAFIN-PH 2027 — aucune publication HAS spécifique cette semaine »* et *« Aucune publication concernant le secteur social et médico-social dans la fenêtre »*. Vérifié : `SERAFIN` compte **0 occurrence** sur les cinq pages lues et **0 entrée** dans le flux vivant depuis le 09/11, donc la première absence est **vraie**. 🔴 **La seconde est celle du flux mort** — et là l'axe ③ a mis le doigt sur le vrai défaut sans pouvoir le nommer : sa ligne de réserve dit *« une absence vraie la semaine passée peut être fausse celle-ci »*, alors que le problème est que cette absence n'est **vérifiable ni cette semaine ni la précédente**. **L'axe a signalé la bonne phrase pour la mauvaise raison, et c'est la convergence de ce signalement avec le `1/6 page NON LUE` de `controle_noms_propres.py` qui désigne le défaut** — aucun des deux ne le voit seul.

**㊳ accepte le livrable, et ㊳ bis est muet parce que le run n'a pas écrit la ligne qu'on lui prescrit.** `controle_livrable_du_job.py` : le run est `is_error=False`, donc ㊳ ne refuse rien. Mais son volet bis rend `○ le récapitulatif de son run ne dit pas combien d'URL ont été testées ni écartées — consigne du 20/10/2026, non bloquante`. Mesuré dans le log : le run a écrit `🔗 Liens : 12 externes` là où la consigne demande `🔗 Liens : N testés · X retenus · Y écartés (codes : …)`. ⚠️ **Conséquence exacte, non bloquante mais réelle** : un lien jeté sur un `000` reste invisible — c'est précisément le trou que la consigne du 20/10 avait comblé, et il est réouvert sur cette édition. `controle_decompte.py` rend **COHÉRENT** (liste 5 ✅ · 0 ⚠ · 1 ⛔ · total 6 ; annoncé 5 ✅ ; 0 ⚠ ; 1 ⛔ ; 6 tentées).

**Les mesures du job, et l'arithmétique dit cette semaine l'INVERSE de la semaine passée.** **3,2242 $ pour un plafond de 5,00 $ — 64 %**, **43 tours**, 8 min 36 s (515 976 ms), 20 890 jetons en sortie, **5 605 428 de cache lu**, 269 744 écrits, **une seule tentative**, `exit 0`, chemin **Étape 7**, push `9d909b5..c2fda60`. Trajectoire sur six créneaux : **59 · 93 · 42 · 55 · 56 · 64 %**. 🟢 **Le prompt est IDENTIQUE À L'OCTET depuis `df175b3`** — sha256 `2e777945e59e`, **58 782 octets**, vérifié à `df175b3`, à `HEAD` et dans l'arbre — donc rien de la dépense ne vient d'un alourdissement. Décomposition : **tours 34 → 43, soit +26,5 %**, **coût par tour 0,0819 → 0,0750 $, soit −8,4 %**, **cache-read par tour 135 681 → 130 359, soit −3,9 %**, pour un coût total **+15,8 %**. ⚠️ **Dit autrement : la semaine passée le job avait payé presque le même prix en faisant un tiers de tours en MOINS ; cette semaine il paie 16 % de plus en faisant un quart de tours en PLUS, à tarif unitaire plus bas.** Les deux semaines sont donc explicables, par des causes opposées, et le plafond de 5,00 $ garde **1,78 $ de marge** — pas de relèvement à mesurer. Document de **13 331 octets** pour **6 423 caractères**, **46 paragraphes tous porteurs de texte**, **12 hyperliens, 12 relations externes (0 orphelin)**, **0 tableau** — l'assertion de volume rend `46 − 12 = 34`, plancher 10, et l'absence de tableau est voulue (la série n'en porte aucun, mesure du 18/10).

**Mes deux erreurs de la séance, et la première est exactement la classe que cette fiche reproche au job.** ① **J'ai formé l'hypothèse que le flux mort était une découverte du jour, et la mesure de la série l'a démolie** : la fiche du 09/11 l'avait mesuré à l'octet près sept jours plus tôt, avait écrit *« la note le porte en ✅ lu »*, et avait même prescrit le remède. **J'allais écrire comme une trouvaille ce que ma propre fiche avait déjà établi** — c'est-à-dire que je ne relisais pas la fiche de N-1 avant de l'ouvrir, le reproche même que je fais au prompt. Ce qui l'a dit est d'avoir balayé les huit éditions **avant** de conclure, et non ma relecture. ② **J'ai annoncé « 72 porteurs » pour un document de 46 paragraphes** : 72 est le nombre de runs `<w:t>`, pas de paragraphes, et l'assertion de volume est **paragraphique**. Chiffre juste, unité fausse, et la marge réelle est **34**, non 60. C'est la règle du 01/11 — *comparer dans le même espace de représentation* — payée sur une simple mesure de structure.

| Verdict | Mesure |
|---|---|
| Affirmations tirées d'une page | **12/12 au degré ①**, horaires et titres de session compris |
| Semaine creuse | **exacte**, prouvée sur le flux `p_3081452` (50 items, dernier du 13/10/2026) |
| Sourçage de cette semaine creuse | ⚠️ **annoncé double, réel simple** — le second flux ne peut rien corroborer |
| Flux `p_3081656` donné `✅ lu` | 🔴 **1 item du 09/07/2024 · 2 207 car.**, sonde du jour, faisceau compris |
| Prescriptions de la fiche du 09/11 | 🔴 **0 / 3 honorées** — adresses, symbole du flux, nom de la commission |
| Cause mesurée | 🔴 le prompt relit `*_veille_has-actualite.**docx**` — **le glob exclut les fiches** |
| Adresses murées perdues le 09/11 | 🔴 **8 / 8 toujours à 0** — perte acquise, `⛔` sans adresse |
| Nom de la commission | 🔴 forme de la note **1**, formes des pages **0** — 3ᵉ édition |
| Façade déclarée par le document | 🟢 **exacte et plus sévère que le dépôt** (3 184 car. > plancher 3 000) |
| `controle_decompte.py` | **COHÉRENT** |
| `controle_attributions.py` | **exit 0 · 0 bloquant · 1 A RELIRE · 5 passes INERTES dont D** |
| `controle_edition_precedente.py` | **exit 0** · 3 axes OK · 2 absences recopiées à revérifier |
| `controle_noms_propres.py` | **exit 0** · 1 interrogé · 1 non retrouvé · **1/6 page NON LUE, nommée** |
| `controle_livrable_du_job.py` | **㊳ accepte** · **㊳ bis ○** : décompte de liens non écrit |
| Run | **3,2242 $ / 5,00 $ = 64 %** · 43 tours · 1 tentative · `exit 0` · push `c2fda60` |
| Prompt | **inchangé à l'octet** depuis `df175b3` — sha256 `2e777945e59e` |

### Requêtes passées

| Requête | Degré / mesure |
|---|---|
| `20 novembre 2026` · `20/11/2026` (page Université) | **① LITTÉRAL** |
| `13h30 - 17h45` · `100 % en ligne` | **① LITTÉRAL** |
| `Un logement c'est bien, avec un projet de vie c'est mieux` | **① LITTÉRAL** |
| `Protection de l'enfance : la visite en présence d'un tiers aujourd'hui` | **① LITTÉRAL** (titre entier, non tronqué cette semaine) |
| `15h00` · `16h00` · `inscription gratuite et obligatoire` | **① LITTÉRAL** |
| `09/11/2026` · `9 novembre 2026` · `09h30` · `17h` (page CSMS) | **① LITTÉRAL** |
| `Ordre du jour` · `relevé de décision` (page CSMS) | **④ ABSENT** — corrobore l'énoncé du corps |
| `CSMS` · `Université d'automne` (calendrier) | **① LITTÉRAL** |
| flux `p_3081452` — items et dates | **50 items · 0 depuis le 09/11 · dernier 13/10/2026** |
| flux `p_3081656` — items et dates | 🔴 **1 item · `9 Jul 2024` · 2 207 car. · 3 058 o** (sonde du jour) |
| `surdicécité` · `candidature` · `clôture` · `13 novembre` · `groupe de travail` (p_4554304) | **④ ABSENT les cinq** — façade confirmée |
| `Commission sociale et médico-sociale` dans la note / sur les pages | **1 / 0** |
| `p_4159151` · `p_3892562` · `p_3578307` · `p_4549164` et 4 autres | **0 dans N-1, 0 dans N** |
| Série : qui cite `p_3081656`, et avec quel statut | **8 éditions depuis le 28/09** ; items courants encore au **02/11** |
| Prompt : `fiche de l'` · `la fiche` · `.fiche.md` | **0 · 0 · 2 (règles de nommage seulement)** |
| sha256 du prompt à `df175b3`, à `HEAD`, dans l'arbre | **identique trois fois** |

### Ce que STANDARD n'a pas interrogé

- **La note de cadrage Surdicécité du 07/10/2026**, repérée sur le flux vivant et **non ouverte** — c'est la source que la doctrine du 14/09 prescrit pour une page murée, et la troisième fiche d'affilée à la signaler sans la lire.
- **Les sept pages murées des lignes « RBPP en cours d'élaboration »** : elles n'ont **plus d'adresse dans le document**, donc elles n'étaient pas sondables à partir de lui. Je n'ai pas réinjecté les adresses de N-2 pour les sonder : ce serait reconstituer ce que le document a perdu, pas auditer ce qu'il dit.
- **Le bloc 7.6 bis du prompt n'a pas été instrumenté cette semaine** — rejoué verbatim sous `env -i`, il sort en 0, mais je n'ai pas mesuré lesquels de ses cinq motifs étaient inertes ; les deux fiches précédentes en comptaient trois.
- **Les 50 items du flux vivant au-delà de leurs dates** : je n'ai lu que `pubDate` et le titre le plus récent. Ce que la fiche du 09/11 avait trouvé là — deux notes de cadrage que la série ignore — n'est pas remesuré.
- **L'écart d'un octet du log** (`58781` contre 58 782) n'est pas reconsigné : constant, bénin, déjà expliqué le 02/11.

## Notes liées

- ⬅️ **Précédente** — [[2026-11-09_veille_has-actualite.fiche]]
  **elle avait raison sur les trois points, elle les avait écrits noir sur blanc, et le job n'avait aucun chemin pour les lire.** Ses trois vérifications prescrites rendent aujourd'hui **0 / 3** : les quatre adresses murées restent à 0, le flux Actualité reste à 1 item de 2024 et garde son `✅`, la commission garde le nom qu'aucune page ne porte. 🟢 Trois de ses mesures resservent telles quelles — le **discriminant `Identification`**, l'**écart de volume mur/vraie page** (3 184 contre 3 693, donc 509 caractères : le plancher reste intouchable) et sa mesure du flux à **2 206 caractères**, que ma sonde reproduit à **un caractère près**. ⚠️ Et sa lecture la plus sombre est confirmée : la perte des adresses n'était pas réversible, l'édition suivante a bien recopié la version amputée
- ➡️ **Suivante** — à produire le 23/11/2026
  **quatre choses à vérifier d'emblée, et la quatrième est neuve.** ① le flux `p_3081656` s'est-il rempli — s'il reste à un item de 2024, **le marquer `⚠` et non `✅`**, prescription désormais à son troisième report ; ② les adresses murées sont-elles revenues, ou la série est-elle définitivement passée à des `⛔` sans adresse ; ③ la commission est-elle nommée **comme la page la nomme** ; ④ 🔴 **le récapitulatif écrit-il `🔗 Liens : N testés · X retenus · Y écartés (codes : …)`**, forme prescrite le 20/10 et non écrite cette semaine, sans laquelle un lien jeté sur un `000` reste invisible
- 🔗 **Pont** — [[2026-11-13_veille_ai-act.fiche]]
  **la même classe, deux jours d'écart, deux étages différents, et c'est la deuxième fois en une semaine.** Là-bas, une déclaration ㊳ annonçait « 0 bloquant » pour **trois contrôles qui n'avaient rien à examiner** — *une passe inerte n'est PAS une passe réussie* ; ici, c'est une **source** qui est inerte et que le document compte parmi ses `✅ exploitées`. Le motif est identique : **un verdict vide lu comme un verdict favorable**. Et les deux documents passent tous les contrôles du dépôt, parce que le dépôt sait compter des bloquants et ne sait pas compter des **silences**
- 🔗 **Pont** — [[2026-11-15_veille_imac.fiche]]
  **son défaut mesuré est la variante marchande du même silence.** `hp.com` y rend **40 caractères utiles pour 76 599 octets** — une façade —, et trois prix PC Windows reposent sur elle plus `WebSearch`, la règle ⑭ étant pourtant satisfaite à la lettre. Ici la façade est **déclarée par le document lui-même** et à **3 184 caractères**, c'est-à-dire **au-dessus** du plancher de 3 000 et de la bande vide mesurée le 05/11 : les deux éditions de la semaine montrent donc, chacune par un bout, que **le plancher de façade du dépôt ne suffit plus** — trop haut pour attraper 3 184, intouchable à cause des 3 693 d'une vraie page
- 🗂️ **Dossier** — [[HAS-actualite_dossier.fiche]]
  à mettre à jour sur quatre points mesurés : ① **le job relit la note et jamais la fiche** — glob `*_veille_has-actualite.docx`, `0` consigne de lecture de fiche, et le prompt nomme lui-même l'asymétrie : **toute prescription de fiche est hors de portée de l'édition suivante**, ce qui explique en un mécanisme les trois reports de cette semaine ; ② **le flux Actualité `p_3081656` n'est plus une source** — 1 item de juillet 2024, sonde du jour, et il servait encore des items courants le **02/11**, donc la mort est récente et datable ; ③ **la série est passée à des `⛔ Page inaccessible` sans adresse** sur sept lignes, l'inaccessibilité n'étant plus constatable par le lecteur ; ④ **la semaine creuse est la cinquième d'affilée** sur le flux vivant (rien depuis le 13/10/2026), ce qu'aucune édition ne dit
