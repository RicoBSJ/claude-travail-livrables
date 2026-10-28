---
type: fiche-document
source: 2026-10-28_veille_SERAFIN-PH.docx
date_creation: 2026-10-28
date_veille: 2026-10-28
veille: serafin-ph
statut: veille-active
tags:
  - veille/serafin-ph
  - registre/pro
  - concept/plfss-2027
  - concept/recueil-ph-2026
  - concept/convergence-tarifaire
  - concept/semaine-creuse
  - source/handicap-gouv
  - source/atih
  - source/lemediasocial
  - source/cnsa
  - theme/mur-anti-robot-qui-rend-200
  - theme/contenu-repris-d-une-page-illisible
  - theme/decret-rejoue-deux-semaines-de-suite
  - theme/motif-2-inerte-et-motif-1-aveugle
  - theme/affirmation-chiffree-sans-source-listee
  - theme/date-inferee-donnee-pour-un-fait
  - theme/plafond-a-90-pour-cent
  - theme/archive-qui-supplee-une-page-muree
---

# 2026-10-28_veille_SERAFIN-PH.fiche

Document source : [[2026-10-28_veille_SERAFIN-PH.docx]]

## Résumé

**La semaine creuse est déclarée honnêtement, la panne CNSA est dite, et le job a fait exactement ce qu'on attendait de lui sur ce point précis.** `exit 0`, une tentative, 30 tours, 7 min 20, **4 tableaux Word** (plancher 3 pour cette série), 95 paragraphes porteurs pour une marge de 88, `0 bloquant` à la passe A, ㊳ `Accepté`, et la note écrit noir sur blanc *« ⛔ SEMAINE CREUSE — Aucune publication officielle dans la fenêtre 21-28 octobre 2026 »* au lieu de meubler. Elle déclare aussi que les informations CNSA *« proviennent de la recherche par moteur et de la note précédente »* — c'est la bonne conduite, et c'était l'attente laissée en suspens depuis le 26/10 : la panne `cnsa.fr` devait être **dite** par le créneau du mercredi, elle l'est. Rejoué ce jour sous `env -i` : la page CNSA rend toujours **HTTP 500, trois essais, `curl` exit 0** — le serveur est en panne, la chaîne TLS est réparée depuis le 26/10, et le contrôle la classe `NON LUE : rien ne sera conclu d'elle`.

**Le défaut central est que la source la plus citée du document est illisible, qu'elle l'était déjà la semaine dernière, et que le récapitulatif du run annonce pourtant « contenu repris ».** `handicap.gouv.fr` rend **HTTP 200 · 5 024 octets bruts · 93 caractères utiles** : *« Please enable JavaScript to view the page content. Your support ID is… »*, signature **TSPD/`bobcmn`** d'un mur anti-robot. Mesuré deux fois, dont une avec un **UA Chrome 131 complet** : réponse identique à l'octet, donc le mur n'est pas une affaire d'agent. ⚠️ **Et ce n'est pas une découverte : la fiche du 21/10 porte déjà les « 93 caractères utiles » et recommandait de ne plus s'en servir comme fond documentaire sans la rouvrir autrement.** Elle a été recitée sans l'être. La passe A le signale — `<-- SOUS 3000 : facade, ou page rendue en JS ?` — mais le motif n'est pas bloquant, et c'est la règle du 25/10 qui mord ici une seconde fois : **un 200 ne prouve pas qu'une page existe**, et `balayer_adresses.py`, qui lit un code et jamais un contenu, continuera à la classer « vivante ».

**La substance, elle, tient — et c'est l'archive qui l'établit, pas le document.** Second point de vue sur le catalogue Wayback : **4 instantanés, tous à 200, 11 à 12 Ko, le dernier le 18/05/2026 et aucun depuis** — le mur a fermé la page au moissonneur comme à nous. Aspiré, cet instantané rend **5 761 caractères utiles**, et les affirmations du document s'y vérifient : **« Camille Galliard-Minier » ①**, **« 30 mars 2026 » ①**, **« simulations » ①**, **« webinaires » ①**, et la décision de fond mot pour mot — *« une mise en œuvre opérationnelle de la réforme tarifaire au 1 er janvier 2027 pour les ESMS […] du secteur « enfant » »*. 🔴 **Deux points attribués au comité n'y sont pourtant pas du tout** : **« SIDOBA » compte 0 occurrence** et **« convergence », « 8 ans », « huit ans » comptent 0 occurrence** sur cette page, alors que le document les range parmi les *« Points traités lors du comité »*, juste au-dessus du lien. La convergence sur 8 ans est **entrée dans la série le 21/10** (0 occurrence les 07 et 14/10), où elle s'écrivait *« progressive sur 8 ans (2027–2035) »* au milieu de **quatre** pages `cnsa.fr` listées ; cette semaine le millésime de fin a disparu et les quatre pages avec, donc **l'affirmation survit sans la source qui la portait**.

**Et la date du comité est une inférence donnée pour un fait, juste par chance arithmétique.** La page archivée ne dit nulle part « 23 mars 2026 » : elle dit *« Communiqué de presse · Publié le 27/03/2026 »* et *« Ce lundi, Camille Galliard-Minier […] a présidé le 14ᵉ comité stratégique »*. Vérifié : **23/03/2026 est bien un lundi**, et le 27/03/2026 un vendredi — le calcul est exact. Mais il est refait chaque semaine depuis au moins le 07/10 sans jamais être signalé comme tel, et une inférence recopiée quatre fois devient indiscernable d'une citation.

**Le rejeu du décret du 13 mai 2026 est le défaut qui compte le plus, parce qu'il traverse une seconde fois deux contrôles différents.** Le document écrit *« Le recueil 2026 (périmètre réduit, décret du 13 mai 2026) est clôturé »*. Or ce décret a été **retiré de l'édition du 21/10 par une correction datée du 23/10**, dont le journal dit exactement pourquoi : *« décret », « 13 mai » et « 40 variables » comptent ZÉRO occurrence sur la page CNSA citée, texte ET HTML brut — cette page est datée du 17/12/2025 et ne peut pas porter un texte de mai 2026*. Mesuré aujourd'hui : dans le **corps corrigé** de N-1, marqueurs et journal exclus, « décret » et « 13 mai » sont à **0 occurrence** — la correction a bien eu lieu ; ils ne subsistent qu'au marqueur (ligne 123) et au journal (ligne 163), deux zones exemptées. Sur la page ATIH listée cette semaine, « décret du 13 mai 2026 » sort en **④ ABSENT, 1 mot plein sur 2**, et « 40 variables » à **0 occurrence**. 🔴 **La passe de relecture d'édition sort pourtant en `exit 0`, et le relais entre ses deux motifs est l'endroit exact où la claim passe** : le motif ② se déclare **INERTE** — *« édition précédente CORRIGÉE (5 marqueurs) — motif ② hors sujet : ses défauts sont tracés dans son journal, et c'est ① qui les suit »* — et le motif ① annonce *« 30 citations d'origine […] dont 11 retenues · **2 jetons distinctifs** · **0 retirés du corps corrigé** »*. Autrement dit : **② se retire parce que ① prend la suite, et ① ne retient que 2 jetons sur 11 citations.** ⚠️ **Ce que je n'ai PAS établi, et je ne le devine pas** : lesquels de ces 2 jetons ont été retenus, donc à quelle étape précise la claim se perd. L'hypothèse à tester est la borne du 19/10, qui exige un **accompagnateur** à moins de 80 caractères en écartant les millésimes — or ici « décret » n'a pour voisins qu'une date, et le coût annoncé ce jour-là était précisément *« un vrai rejeu dont la citation n'a qu'un seul mot distinctif sort en avertissement »*. Ici il ne sort même pas en avertissement. **Et l'histoire est une récidive : la fiche du 21/10 portait déjà le tag `theme/decret-rejoue-une-semaine-apres` — c'est le troisième passage de la même phrase en trois semaines, attrapée par ② le 21/10, par personne le 28/10.**

**Deux affirmations chiffrées n'ont aucune source listée dans ce document, et l'une des deux en avait une la semaine dernière.** *« Treize associations et fédérations […] ont adressé une lettre aux ministres »* : sur la **seule** page du Média Social listée cette semaine, « Treize » et « 13 associations » sortent en **④ ABSENT, 0 mot plein sur 1**. N-1 l'attribuait à un **second** article du Média Social (`appel-a-un-budget-pour-serafin-ph…`), que cette édition ne liste plus. La note dit honnêtement *« Source secondaire. Les lettres n'ont pas été consultées en source primaire »* — mais elle ne nomme plus **quelle** source secondaire, et la passe A2 ne peut pas le voir puisqu'aucun nom n'est avancé : **l'affirmation est non attribuée par construction, donc hors de portée du contrôle**. Dans le même mouvement, les **90 M€** — 9 occurrences dans le corps de N-1, le chiffre même que ces treize fédérations réclamaient — **disparaissent sans un mot**, de même que le vote parlementaire de novembre 2026 que N-1 donnait pour décisif ; l'agenda du 28/10 ne garde qu'un *« Automne 2026 — surveiller les amendements »*.

**La seule citation entre guillemets du document est exacte, et c'est ma requête qui a d'abord dit le contraire.** La note prête au dossier de presse du PLFSS 2027, via Le Média Social, la phrase *« sera accompagnée d'une enveloppe de 360 M€ versés sur une période de quatre ans à partir de 2028 »*. Interrogée avec une **apostrophe droite** : **④ ABSENT**. Interrogée avec l'**apostrophe courbe** que la page écrit : **① LITTÉRAL**. La page la porte elle-même entre guillemets — c'est donc bien une citation de seconde main, et le document le déclare deux fois (*« source secondaire »*, *« le PLFSS n'a pas été lu directement »*). ⚠️ **Et la passe B-FR l'avait déclarée `OK` : son verdict porte sur une clé normalisée, pas sur le degré ① — un `OK` de B-FR ne vaut pas preuve de citation**, c'est `chercher.py` qui tranche, et il a tranché dans le bon sens une fois la requête écrite comme la page.

**Trois comportements de contrôle à verser au dossier, aucun bloquant, aucun faux refus.** ① `controle_decompte` compte **5 entrées pour 4 sources** — il relève les ⛔ dispersés dans la prose en plus des lignes du tableau, l'ambiguïté d'aplatissement consignée le 23/10 — et il ne sort en **2** (`AUCUN DÉCOMPTE ANNONCÉ`) que parce que la note n'annonce aucun total ; annoncer « 4 sources » l'aurait fait crier. ② La passe D rend **`OK` pour « 200 » et « 500 »**, appariés dans le **JavaScript minifié** de pages qui n'ont rien à voir (`brut (rendu JS)`) : ce sont des valeurs d'**instrumentation**, que ㊲ est censé exempter, et leur « vérification » ne prouve rien — la direction est bénigne, mais un `OK` vide ressemble à un `OK`. ③ `㊳ bis` lit **8 testés · 5 retenus · 3 écartés (codes : 500×3)** : cohérent avec les 7 liens cliquables et la panne CNSA.

**Enfin, le coût : 90 % du plafond, et c'est le cran qui précède le dépassement.** Trajectoire mesurée sur les cinq derniers créneaux — **25 · 27 · 39 · 37 · 90 %** — soit **2,6916 $ pour 3,00 $**, 0,31 $ de marge. Le prompt n'est pas en cause : **32 843 octets les deux dernières semaines**, identique à N-1. La durée non plus : **440 122 ms contre 438 287**, deux secondes d'écart. Ce qui a changé est le **contexte relu à chaque tour** : `cache-read` **998 956 → 2 978 967 (×2,98)**, `out` 18 828 → 20 441, 28 → 30 tours — pour la note **la plus courte de la série** (14 252 octets, 7 036 caractères). Le seul fait nouveau de la tâche est la panne CNSA, qui a forcé trois URL écartées sur un code HTTP, un repli sur le moteur de recherche et la relecture de la note précédente. ⚠️ **Les deux seuls dépassements documentés du dépôt — astrologie le 08/10, ai-act le 16/10 — ont tous deux été précédés d'un avertissement à 86 et 93 %**, et la règle écrite est de faire suivre le plafond dans le même geste. Relever `serafin-ph-veille` n'est pas commandé ici : c'est une décision du propriétaire, et la mesure est posée.

### Requêtes passées

| Source | Requête | Degré |
|---|---|---|
| Média Social (2 969 car. — **façade sous le plancher de 3 000**) | `sera accompagnée d'une enveloppe de 360 M€ versés sur une période de quatre ans à partir de 2028` (apostrophe **droite**) | ④ ABSENT — **ma requête** |
| idem | même phrase, apostrophe **courbe** (celle de la page) | **① LITTÉRAL** |
| idem | `360 M€` · `05 octobre 2026` · `report` · `crédits` | ① ×4 |
| idem | `Treize` · `13 associations` | **④ ABSENT, 0 mot plein** |
| idem | `1er octobre 2026` | ④ — la page écrit « le 1 er octobre », **sans millésime** |
| ATIH (8 903 car.) | `14/05/2025` · `CDAPH` · `exclusivement` · `orientés par la commission` | ① ×4 |
| idem | `e-Pass` | ② GRAPHIE |
| idem | `mineurs et jeunes adultes` · `guides méthodologiques` | ④ — **mes requêtes** ; la page dit « personnes **mineures** et jeunes adultes », comme le document |
| idem | `décret du 13 mai 2026` · `40 variables` · `périmètre réduit` | **④ ABSENT** |
| handicap.gouv.fr **en direct** | — | **illisible** : 200 · 5 024 o · **93 car.** · mur TSPD, idem sous UA Chrome |
| handicap.gouv.fr **archive 18/05/2026** (5 761 car.) | `Camille Galliard-Minier` · `30 mars 2026` · `simulations` · `webinaires` | ① ×4 |
| idem | `1er janvier 2027` · `secteur enfance` | présents sous « 1 er janvier 2027 » et « secteur « enfant » » |
| idem | `23 mars 2026` | ④ — la page dit « Publié le **27/03/2026** » + « **Ce lundi** » ; 23/03/2026 **est** un lundi |
| idem | `SIDOBA` · `convergence` · `huit ans` · `8 ans` | **0 occurrence** |
| cnsa.fr | — | **HTTP 500**, 3 essais, `curl` exit 0 → `NON LUE` |

**Ce que STANDARD n'a pas interrogé** : le texte du PLFSS 2027 lui-même (le document dit ne pas l'avoir lu) · les courriers des treize fédérations (non consultés, et plus aucune source listée ne les porte) · les pages `cnsa.fr`, inaccessibles · le **tableau des rôles DGCS/CNSA/ATIH/ARS**, boilerplate institutionnel confronté à aucune page · la question de savoir si la demande des **90 M€** est encore vivante après sa disparition · et l'origine de la **convergence sur 8 ans**, qu'aucune source listée cette semaine ne porte.

**Mes erreurs de cette séance, et elles sont du même genre toutes les trois** : deux ④ rendus sur ma propre graphie — l'apostrophe droite contre la courbe de la page, « mineurs » contre « mineures » — où j'ai failli accuser un paragraphe **exact**, et c'est la sixième fois que la règle du 25/10 (« le ④ vient de la requête avant de venir du document ») se vérifie contre moi ; et une lecture de la série des coûts dans le **mauvais ordre**, parce qu'un `grep -h` sur un glob tuyauté dans `sed` ne dit pas de quel fichier vient chaque ligne — corrigée en mesurant fichier par fichier, après avoir commis exactement la même chose dix minutes plus tôt sur les tailles de prompt.

## Notes liées

- **⬅️ Précédente** · [[2026-10-21_veille_SERAFIN-PH.fiche]]
  **elle avait déjà mesuré les 93 caractères de `handicap.gouv.fr` et demandé qu'on cesse de s'en servir ; la page est recitée, et le run annonce « contenu repris ».** Elle portait aussi le tag `theme/decret-rejoue-une-semaine-apres` : le décret du 13 mai 2026 y était attrapé par le motif ② **non bloquant**, puis corrigé le 23/10. Cette semaine, ② se déclare **inerte** parce que N-1 est corrigée et renvoie à ①, qui ne retient que **2 jetons distinctifs sur 11 citations** et ne voit rien. **Le passage de relais entre les deux motifs est le trou, et il n'était visible qu'en comparant leurs deux sorties.**
- **🔗 Pont** · [[2026-10-27_lecon-hypnose_20_bilan-synthese-feuille-de-route]]
  **deux documents de la même semaine dont la substance tient et dont l'appareil de sources ne tient pas.** Là-bas la carte des vingt leçons concordait un par un avec le disque tandis que la moitié des sources ne résistait pas à la vérification ; ici les faits du comité stratégique se vérifient **sur une archive de mai**, et ce sont deux des points attribués à la page vivante — SIDOBA, la convergence sur 8 ans — qui n'y figurent pas. **Dans les deux cas le défaut n'est pas dans ce qui est dit, mais dans ce à quoi c'est attribué.**
- **🔗 Pont** · [[2026-10-14_veille_SERAFIN-PH.fiche]]
  **c'est l'édition qui avait établi la démonstration sur le décret, et elle n'a tenu ni une semaine ni deux.** « décret » à zéro occurrence sur une page CNSA de décembre 2025, donc impossible pour un texte de mai 2026 : la phrase est revenue le 21/10, a été corrigée le 23/10, et revient le 28/10. **Une démonstration écrite dans un livrable ne protège pas le livrable suivant — seul un contrôle le fait, et celui qui devait le faire s'est tu.**
- **🗂️ Dossier** · [[SERAFIN-PH_dossier.fiche]]
  à mettre à jour sur cinq points mesurés ce jour : **`handicap.gouv.fr` est muré (TSPD, 93 car., 200 constant, insensible à l'UA)** et son **instantané du 18/05/2026** est désormais la seule voie de lecture — dernière capture du catalogue, 5 761 car. utiles ; **`cnsa.fr` est toujours en HTTP 500** au 28/10, TLS réparé, serveur en panne depuis le 26/10 ; **la convergence sur 8 ans et SIDOBA ne sont portés par aucune source listée** et doivent être rattachés à une page CNSA quand elle répondra ; **le décret du 13 mai 2026 reste non vérifié** et doit être cherché sur Légifrance, pas sur une page d'actualité ; et **la fenêtre 21-28/10 est vide** — rien ne s'est produit, le prochain fait attendu est le vote du PLFSS 2027 à l'Assemblée.
