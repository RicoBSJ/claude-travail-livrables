---
type: fiche-document
source: 2026-11-01_veille_imac.docx
date_creation: 2026-11-01
date_veille: 2026-11-01
veille: imac
statut: veille-active
tags:
  - veille/imac
  - registre/perso
  - concept/comparateur-prix
  - concept/reconditionne-apple
  - concept/tout-en-un-windows
  - concept/lancement-m6
  - concept/noms-propres
  - source/consomac
  - source/apple
  - source/macrumors
  - source/macg
  - source/fnac
  - source/phonandroid
---

# 2026-11-01_veille_imac.fiche

Document source : [[2026-11-01_veille_imac.docx]]

## Résumé

**Le créneau du jour est le premier à exercer en production le contrôle des noms propres, il le passe proprement — et le seul nom propre faux de la note lui est invisible par construction.** Mesures du run : `exit 0`, **2,5460 $ pour 4,00 $ (64 %)**, 24 tours, 1 tentative, 610 853 ms, `in 28 · out 23 532 · cache-read 2 618 467`. La ligne prescrite est écrite : `👤 Noms propres : 12 interrogés · 10 non retrouvés · 0 page non lue`. Rejeu sous `env -i` : les dix non-retrouvés sont reproduits **à l'identique**, et la déclaration du job — *« tous termes techniques PC Windows, aucun nom de personne »* — est **vérifiée** : `Core Ultra`, `Intel Core Ultra`, `Lenovo IdeaCentre AIO`, `Lenovo AIO`, `Windows AiO`, `AiO Windows`, `SSD PCIe`, `Meteor Lake`, `Arrow Lake`, `Évolutivité RAM`. Dix signalements, **zéro vrai positif**. Et `TSMC`, qui est un organisme attribué en style indirect et absent des huit pages, **n'est pas dans les douze** : `MIN_JETONS = 2` exige deux jetons capitalisés, un sigle seul est hors de portée du motif. Le contrôle né de l'incident du 30/10 sur une veille de personnes rend donc, sur une veille de matériel, **dix fausses alertes et aucun des deux noms qui comptaient**. ⚠️ `Évolutivité RAM` montre en outre que la classe d'aplatissement survit au resserrement du 31/10 : la barre oblique de `RAM/SSD` coupe la cellule, et le séparateur de même ligne ne peut rien contre un `/`.

**« 2 nm TSMC » est à sa cinquième édition, et la mesure dit exactement où la chaîne de continuité a lâché — pas une fois, deux fois, pour deux raisons différentes.** `TSMC` : **0 occurrence sur les huit pages**, texte et brut, toutes casses ; la page Fnac écrit *« la M6 est gravée en 2 nm »* sans nommer de fondeur, et c'est la seule page à porter `2 nm`. Trajectoire mesurée sur les `.docx` :

| édition | `TSMC` | marqueurs | lecture |
|---|---|---|---|
| 04/10 | 1 | 7 | présent, et corrigé |
| 11/10 | 5 | 0 | rejoué |
| 18/10 | **0** | 17 | le fondeur disparaît — correction tenue |
| 25/10 | 2 | 0 | **rejoué, et rien ne l'a vu** |
| 01/11 | 3 | 0 | rejeu poursuivi, désormais attribué à MacRumors 27/10 |

Au maillon **18/10 → 25/10**, `controle_edition_precedente.py` répond `OK — aucune correction rejouée` sur 41 citations d'origine, 14 retenues et 16 jetons distinctifs. Deux aveuglements indépendants l'expliquent : l'axe ① ne suit que les jetons **retirés du corps corrigé de N-1 et revenus**, or le 18/10 porte `TSMC = 0` — la correction avait **supprimé le mot sans le citer**, donc il n'existe aucun jeton à suivre ; et l'axe ② est **déclaré inerte dès que N-1 est corrigée** (*« édition précédente CORRIGÉE (17 marqueurs) — motif ② hors sujet »*), donc le constat explicite de la fiche du 18/10, `TSMC : 0 occurrence sur les dix pages lisibles`, n'a **jamais été lu**. 🔴 **Un défaut corrigé par omission ne laisse rien à ① et est caché de ② par la règle d'inertie de ② lui-même.** Au maillon **25/10 → 01/11**, les deux axes sont muets pour une raison plus banale : le 25/10 n'a **aucun marqueur et aucun journal**, et sa fiche est un **talon de 294 octets**. Même mécanisme pour `SSD PCIe 5.0` : **0 occurrence de « pcie »** sur les huit pages.

**Le Mac mini est la seule erreur du jour dont la source dit littéralement le contraire, et le signe est inversé.** La note écrit : *« contrairement au Mac mini M6 (+100 € sur son prédécesseur au tarif courant de 949 €) »*. macg.co écrit, au degré ① : *« Promo : le Mac mini M6 à 949 €, soit **100 € de moins** »*. Trois erreurs dans une parenthèse : le sens de l'écart (**−100 € et non +100 €**), la nature du prix (une **promotion**, pas un « tarif courant »), et l'objet de la comparaison. ⚠️ Et la phrase ne vient pas du corps de l'article mais du bandeau **« Poursuivez votre lecture »** — une liste de liens connexes lue comme du contenu, la classe de défaut que le dépôt connaît déjà par le mobilier de navigation.

**Le reconditionné annonce deux nano-texturés à 1 789 € ; la page Apple en porte un, à 1 909 €, et publie ses propres économies.** Extraction des sept fiches de `apple.com/fr/shop/refurbished/mac` : **5 × 1 599 €** standard (ancien prix 1 879 €, *« Économisez 280,00 € »*) · **1 × 1 789 €** **standard** (ancien 2 099 €, économie 310 €) · **1 × 1 909 €** **nano-texturé** (ancien 2 249 €, économie 340 €). La note écrit `×5 coloris à 1 599 € (neuf 1 999 €, −400 €/−20 %)` et `Nano-texturé (×2) à 1 789 € (neuf 2 219 €, −430 €/−19 %)`. Donc : le 1 789 € est **standard**, le nano-texturé est **unique et à 1 909 €**, et **`2 219 €` a zéro occurrence sur la page**. Les économies que la page publie sont **280, 310 et 340 €, soit −15 %** — la note annonce −20 % et −19 % en recalculant contre des prix neufs qu'elle choisit elle-même, tout en présentant le tableau comme un relevé *« sur apple.com (relevé 01/11/2026) »*. ✅ Sont justes en revanche : le **compte de 7**, le **minimum à 1 599 €**, et *« tous des 10c/10c »* — les sept libellés portent `CPU 10 cœurs et GPU 10 cœurs`. ⚠️ **La passe D n'a rien vu, et c'est structurel** : ces chiffres vivent dans des **cellules de tableau**, hors du contexte d'attribution qu'elle examine.

**« 7 couleurs — une de plus que le M4 » est démentie mot pour mot par une source que la note classe ✅.** Phonandroid écrit : *« Même les coloris sont identiques : vert, jaune, orange, rose, violet, bleu et argent »* — sept, **identiques** au M4. L'origine est traçable dans la série : le 25/10 écrivait *« Nouvelles couleurs prévues (sans précision officielle à ce stade) »*, une rumeur correctement réservée ; le 01/11 l'a durcie en fait chiffré **que la page du jour contredit**. C'est le même mécanisme que `TSMC` — une anticipation promue en fait sourcé —, deux fois dans la même édition.

**Le cadrage « 0 € identique » est défendable au tarif courant, et il tait la comparaison que sa propre source publie.** Phonandroid, degré ① : *« Le modèle avec deux ports Thunderbolt est commercialisé à partir de 1 799 euros, **soit 300 euros de plus que l'iMac 2024** »* — et le titre de l'article, cité en clair dans la rubrique des sources, est *« des prix qui grimpent »*. La note affirme *« Prix identiques à l'actuelle grille M4 »*, `0 € (identique)` deux fois, *« pas de surcoût »*. La réconciliation existe et elle est sourcée — macg confirme *« Apple avait lancé l'iMac M4 à 10 cœurs à partir de 1 749 € »*, et 1 999 − 1 749 = 250 —, mais **elle n'est jamais dite au lecteur** : la hausse a eu lieu en juillet 2026, donc « identique » ne vaut **qu'au tarif post-hausse**. ⚠️ Et lue au littéral, la ligne est fausse dans son propre tableau : le M6 **10c/10c** à 1 799 € fait face au M4 **10c/10c** que la note chiffre elle-même à 1 999 €, soit **−200 €**, pas 0 € — la colonne compare des **paliers**, pas des configurations, et ne le dit pas.

**« macOS (Sequoia) » est au degré ① sur une page, et c'est la fiche marchande d'un M4 de 2024.** Le comparateur consomac écrit `Apple iMac Apple M M4 … macOS Sequoia Wi-Fi 6E (802.11ax)` dans une offre revendeur. La note porte `macOS (Sequoia)` dans la ligne **OS** du tableau qui compare l'**iMac M6** au PC Windows. Aucune des huit pages n'attache Sequoia au M6. ⚠️ **Un appariement littéral ne dit pas de quoi la page parle** — règle du dépôt, appliquée ici à un système d'exploitation.

**dell.com est lisible aujourd'hui, et le prix n'y est pas — mais la note avait raison à 08h03.** Le run a écarté la page en **403** et l'a déclarée telle : sonde du jour, **HTTP 200 · 309 086 octets · 18 945 caractères utiles**, et `EC27260` à **0 occurrence**. Le document ne se trompe pas : il écrit *« accès direct bloqué 403 »* et classe la source ⚠️ *« non confirmé directement »*. Ce qu'il faut en retenir est la portée : **les trois prix Windows — 1 338 €, 1 159,99 €, ~1 549 € — reposent entièrement sur des extraits WebSearch**, et ce sont exactement les trois réserves de la passe D. La moitié Windows de la veille est invérifiable, et elle porte l'écart *« −400 à −660 € en faveur du PC »* qui est la conclusion d'arbitrage la plus engageante du document. ⚠️ Conséquence pour le contrôle des noms propres : il a compté **0/8 page non lue**, ce qui est juste à sa définition (18 945 ≥ 3 000) — mais une page à **403 verbeux** passerait son plancher sans être lisible, car il ne consulte **pas le code HTTP**.

**Verdict — tous les contrôles sont verts, et les six défauts sont hors de leur portée.** `controle_decompte.py` **COHÉRENT** (7 ✅ · 2 ⚠ · 0 ⛔ · 9 annoncées, et l'ordre des colonnes n'a pas dérivé) · `controle_attributions.py` **0 bloquant**, 3 réserves D, 4 passes inertes (B, B-NOM, C, C2) · `controle_livrable_du_job.py` **exit 0** (㊳ : run réussi ; ㊳ bis : 8 · 7 · 1, aucun 000) · intégrité **8 tableaux, marge 204** · `controle_edition_precedente.py` **OK**, axe ② inerte faute de fiche en N-1 · `controle_noms_propres.py` **10 signalements non bloquants, 0 vrai** · gate `--docs` **exit 0**, 18/18 bornes des noms propres jouées.

### Requêtes passées

| Requête | Verdict |
|---|---|
| `précommandes` · `6 novembre` · `28 octobre` · `2 nm` · `170 Go/s` | ① leclaireur.fnac.com |
| `Wi-Fi 7` · `Thunderbolt` | ① macrumors 27/10 |
| `12 cœurs` | ① apple.com reconditionné **et** ① fnac (*« 12 cœurs CPU répartis entre 2 super cœurs, 4 cœurs de performance et 6 cœurs d'efficacité »*) |
| **`TSMC`** | **④ — 0 occurrence sur les huit pages**, texte et brut, toutes casses |
| **`PCIe`** | **④ — 0 occurrence sur les huit pages** |
| `1 799 €` | ① consomac bons plans · et `1 799 euros` ① phonandroid, **suivi de *« soit 300 euros de plus que l'iMac 2024 »*** |
| `1 999 €` · `1 736 €` · `1 953 €` · `2 209 €` · `1 749 €` | ① macg.co |
| `1 679 €` | ① consomac comparateur (`1 679,00 € −7 %`, M4 8c Rose) |
| `1 599 €` | ① apple.com reconditionné — **mais avec *« Ancien prix : 1 879,00 € · Économisez 280,00 € »*** |
| `2 219 €` | **④ — 0 occurrence** sur la page du reconditionné |
| `949` | ① macg.co — dans le bandeau *« Poursuivez votre lecture »*, **« soit 100 € de moins »** |
| `250 €` | ④ — chiffre **calculé** par la note (1 999 − 1 749), non cité |
| `Sequoia` | ① consomac — dans une **fiche marchande du M4 2024**, jamais rattachée au M6 |
| `coloris` | ① phonandroid — *« Même les coloris sont identiques »* |
| `15 € tous les 100 €` | ① consomac bons plans, marquée **« Expiré »**, 07/10/2026 à 18:46 ✅ |
| `EC27260` · `OmniStudio` · `IdeaCentre` | **④ — 0 occurrence** sur les huit pages, dell.com compris (lisible, 200) |
| `1 338 €` · `1 159,99 €` · `1 549 €` | ④ — **réserves D**, extraits WebSearch seuls |
| écarts M4 du 25/10 (`0 €` sur toutes les configurations) | ✅ vérifié sur le `.docx` du 25/10 |

### Ce que STANDARD n'a pas interrogé

- **Les benchmarks et les gains de performance** : *« performances graphiques jusqu'à deux fois plus rapides »* (phonandroid) n'a pas été confronté à MacRumors, et la note ne les reprend pas — elle écrit *« réf. benchmarks à venir »*, ce qui est honnête.
- **Les colonnes « Durée support logiciel », « Revente », « Garantie standard »** du tableau comparatif : aucune n'est chiffrée ni attribuée, donc hors de portée d'un appariement.
- **Les deux prix M6 au configurateur Apple** (24 Go, 512 Go) : la note les déclare *« non lisibles en headless »*, non vérifié.
- **Le `+30 € pour l'Ethernet 2,5 Gigabit`** et le **Bluetooth 6.0**, présents sur la page phonandroid et **absents de la note** — deux faits disponibles non repris.
- **L'offre reconditionnée à 1 569 €** (ancien 1 999 €, économie 430 €) présente sur la page Apple : elle n'est **pas** un iMac, vérifié sur son libellé, donc le minimum de 1 599 € tient ; mais c'est d'elle que vient, par coïncidence, le `−430 €` de la note.

### 🔴 Mes propres erreurs de mesure, ce jour

- **`lire_page.py --autour` fait une recherche LITTÉRALE pliée, pas une regex** : son code est `cible.startswith(m, i)` après `plie(motif)`. J'ai passé `"euros|€"` puis `"1 749|949|hausse"` et lu les deux `0 occurrence` comme des absences — j'ai failli écrire que la page phonandroid *« ne porte aucun prix »* alors qu'elle écrit `1 799 euros`, et que macg ignore la hausse alors qu'il l'écrit. C'est la mesure des octets qui a tranché, pas la relecture. ⚠️ **L'aide du dépôt dit « motif », ce qui invite à la regex** : le mot est trompeur et c'est la deuxième fois en une semaine que j'accuse un outil avant de relire mon invocation.
- **J'ai appelé `timeout`**, qui n'existe pas sur macOS — déjà consigné le 25/10, refait le 01/11.

## Notes liées

- **⬅️ Précédente** · [[2026-10-25_veille_imac.fiche]]
  **c'est un talon de 294 octets, et c'est précisément ce qui a laissé passer le défaut du jour.** L'axe ② de `controle_edition_precedente.py` lit la fiche de N-1 pour y chercher les formulations données pour fautives : il a lu **0 citation**, parce qu'il n'y a rien à lire. L'axe ① n'avait rien non plus — le `.docx` du 25/10 porte **0 marqueur et aucun journal**. Deux axes sur trois muets par absence de matière, et le troisième ne cherche que des phrases d'absence recopiées. ⚠️ Et le 25/10 est l'édition **où `TSMC` est revenu** : la fiche qui aurait pu le dire n'a jamais été écrite. Trois des vingt-deux fiches `imac` sont des talons (27/09, 25/10, et celle-ci avant aujourd'hui)
- **➡️ Suivante** · édition du **dimanche 08/11/2026 à 8h03** — à surveiller : les premiers prix marchands tiers du M6 (livraisons le 6/11), les premiers benchmarks indépendants, et si `TSMC` revient une sixième fois
- **🔗 Pont** · [[2026-10-18_veille_imac.fiche]]
  **elle avait déjà mesuré le défaut du jour, et son constat n'a jamais été lu par aucun contrôle.** Sa table de requêtes porte, en clair : `2 nm` · `nanomètre` · `procédé` · `gravure` · `TSMC` → **0 occurrence sur les dix pages lisibles**. Son édition a été corrigée — 17 marqueurs — et le fondeur en a **disparu** (`TSMC = 0`). C'est exactement cette réussite qui a créé l'angle mort : une correction **par omission** ne laisse aucun jeton à l'axe ①, et un N-1 corrigé rend l'axe ② **inerte par règle**. 📌 Piste bornée, non faite : quand N-1 est corrigée, ne pas rendre ② inerte mais le restreindre aux constats de la fiche **qui ne sont pas tracés dans le journal de N-1** — c'est la classe entière des corrections silencieuses
- **🔗 Pont** · [[2026-10-04_veille_imac.fiche]]
  **l'entrée 7 de son journal est à son quatrième rejeu, et elle n'a jamais été en portée.** Elle reprochait ensemble *« Bande passante 170 Go/s »* et *« Procédé 2 nm TSMC »*. Les 170 Go/s sont aujourd'hui **littéraux sur la page Fnac** et correctement attribués ; le `2 nm` est désormais **sourcé lui aussi** — seul le **fondeur** reste sans page. Le défaut a rétréci de deux termes à un en quatre semaines, mais il n'a jamais été vu par un contrôle : `controle_edition_precedente.py` ne lit que **N-1**
- **🔗 Pont** · [[2026-10-30_veille_ai-act.fiche]]
  **le contrôle qu'elle a fait naître tourne ici pour la première fois en production, et la mesure retourne son hypothèse.** Là-bas il voyait deux noms de **personnes** faux — « Lara Comi », « Leonardo » Benifei — là où dix passes étaient inertes. Ici, sur une veille de matériel, il rend **dix fausses alertes sur douze interrogations** et manque le seul nom propre faux, parce que `TSMC` est un **jeton unique**. ⚠️ Le portage du 31/10 est donc confirmé utile **et mal calibré pour cette série** : un motif non bloquant qui crie dix fois par créneau est sur le chemin de n'être plus lu — exactement le raisonnement qui avait fait écarter le seuil « 100 % d'exemptions » le 27/10. 📌 Piste bornée, non faite : exiger **deux** jetons **ou** un sigle de 3 lettres et plus **entièrement capitalisé et absent du lexique**, et mesurer le coût sur les 299 documents avant de câbler
- **🗂️ Dossier** · [[iMac_dossier.fiche]]
  à mettre à jour, et il reste la source d'origine du défaut : il écrit *« ce sera le M6, première puce Apple en 2 nm »* en l'adossant à Gurman le **23/08/2026**. Le `2 nm` est désormais **confirmé et sourcé** — la page Fnac l'écrit —, donc cette ligne du dossier a été **validée par l'événement** ; le fondeur, lui, n'a jamais eu de page et doit être **marqué comme inféré** dans le dossier, faute de quoi chaque édition continuera de le réattribuer à la page qu'elle vient d'ouvrir. À verser aussi : le lancement est **acquis** (annonce 27/10, précommandes 28/10 à 18h10, sortie 6/11), le M5 est **sauté**, et les coloris sont **inchangés** — ce dernier point contre ce que le dossier et le 25/10 laissaient attendre
