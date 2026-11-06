---
type: fiche-document
source: 2026-10-25_veille_imac.docx
date_creation: 2026-10-25
date_veille: 2026-10-25
veille: imac
statut: veille-active
tags:
  - veille/imac
  - registre/perso
  - concept/comparateur-prix
  - concept/reconditionne-apple
  - concept/tout-en-un-windows
  - concept/calendrier-m6
  - concept/cycle-de-vie-windows
  - source/consomac
  - source/apple
  - source/macrumors
  - source/theapplepost
  - source/ldlc
  - source/hp
  - source/microsoft
  - theme/le-push-du-job-a-echoue-trois-fois
  - theme/le-hook-a-refuse-sur-un-motif-faux
  - theme/connexion-ssh-morte-en-plein-hook-la-veille-du-26-10
  - theme/epilogue-code-zero-n-est-pas-une-publication
  - theme/troisieme-date-fausse-de-suite-sur-le-support-windows
  - theme/axe-un-aveugle-a-un-defaut-qui-revient-avec-une-autre-valeur
  - theme/provenance-demolie-survit-au-changement-d-url
  - theme/tsmc-est-source-contrairement-a-ce-que-disent-deux-fiches
  - theme/pourcentage-cpu-recopie-sur-le-gpu
  - theme/estimation-de-prix-fausse-de-cent-euros-reserve-tenue
  - theme/deux-editions-qui-se-contredisent-sur-l-evolutivite
  - theme/page-vivante-non-verifiable-retrospectivement
---

# 2026-10-25_veille_imac

Document source : [[2026-10-25_veille_imac.docx]]

## Résumé

**Le fait le plus grave de cette édition n'est pas dans le document : le créneau a produit son livrable et n'a pas pu le publier, trois fois de suite.** Le log fait **40 609 octets** là où les autres de la série en font 3 000 à 7 000, et les 450 lignes de surplus sont le hook `pre-push` joué **trois fois** — une fois par tentative. Chaque tentative dit la même chose : le gate documentaire passe (`✓ aucun verdict n'a changé`), puis **`Connection to github.com closed by remote host.`** apparaît **en plein hook**, puis le hook continue son aspiration et sort en 1. Verdict final : `[git] ⛔ push ÉCHEC après 3 tentatives — 2 commit(s) en avance sur origin/main`. Le `.docx` a été poussé plus tard par un autre run — `faf914f` est bien sur `origin/main` aujourd'hui — mais **le squelette de fiche n'a jamais été commité du tout**, ce qui explique qu'il soit encore non suivi par git douze jours après.

**Et le hook a refusé sur un motif faux, pour une cause qui n'a rien à voir avec ce dépôt.** Le message imprimé est *« ✗ PUSH REFUSÉ — un verdict a changé, un témoin ne sort plus en 1 »*. La vraie ligne d'échec est trois écrans plus haut : `✗ controle_astrologie_karmique.py : le témoin conforme sort en 1 — faux positif du contrôle : REFUSÉ — 1 motif(s) : page sans réponse …promenade.imcce.fr/fr/pages2/221.html`. C'est **exactement** le blocage du 23/10 — l'hébergement de l'Observatoire de Paris éteint, un témoin conforme refusé, et le dépôt entier interdit au push — et `non_regression/tolerance_page_morte.py` a été écrit **le 25/10** pour l'excuser. Le créneau de 08:03 est passé **avant** le correctif : cette édition est la **victime de production** de ce blocage, celle que la consignation du 23/10 n'a jamais nommée. Deux causes indépendantes suffisantes se superposent dans le même log, puisque le `--complet` de chaque tentative dure plus longtemps que la connexion SSH ouverte avant lui.

**Cette connexion morte est datée du 25/10, soit la veille du jour que le dépôt tient pour la première observation du défaut.** `CLAUDE.md` consigne le défaut de transport au **26/10** (*« mesuré deux fois de suite »*), puis corrige le **31/10** que la cause n'est pas le mode `--complet` mais la **durée** du hook. Le log du 25/10 porte la ligne `Connection to github.com closed by remote host.` **trois fois**, et la porte sur un **job**, pas sur un push manuel. Deux conséquences : l'antériorité est d'un jour, et la portée est plus large — un hook long ne fait pas seulement échouer un push qu'on relance, il fait **perdre une publication à un créneau qui ne sera pas rejoué**. ⚠️ Et rien dans le dépôt ne l'a vu : `rattrapage_jobs.sh --manques` exige l'épilogue `Fin du job … (code de sortie : N` par sa ligne 77, sans jamais lire le `N`, et renvoie `✓ tracé` ligne 102. Ce log porte `(code de sortie : 0, tentatives : 1)` : **un épilogue à zéro n'est pas une publication**, et c'est la classe du 23/10 (*« un log n'est pas un run »*) d'un cran plus loin.

**Le support de Windows 11 est faux pour la troisième édition consécutive, avec une troisième valeur différente — et l'axe ① ne peut pas voir cela.** La note écrit *« Windows 11 Home : support jusqu'au 14 octobre 2025 annoncé, Windows 12 attendu »*, c'est-à-dire, le 25 octobre 2026, que la plateforme qu'elle compare est hors support depuis plus d'un an. Mesuré ce jour sur les pages de cycle de vie de Microsoft : *Windows 11 Home and Pro* porte `Start Date 10/4/2021` et **`Retirement Date : In Support`** — aucune date de retrait —, sa version la plus lointaine finissant le **10/10/2028** ; et le **14 octobre 2025** est la fin de support de **Windows 10** (`Retirement Date 10/15/2025 6:59:59 AM` PT). La transposition est double, donc plausible : mauvais produit **et** mauvaise année, puisque le « 14 octobre » existe bien chez Windows 11 — c'est la fin de service de la version **24H2**, le **14 octobre 2026**. Historique de la série : le **11/10** une correction remplace la ligne par *« durée de support non vérifiée sur les pages lues »* ; le **18/10** elle revient en *« jusqu'en octobre 2031 »*, et la fiche du 18/10 mesure **2031 = zéro occurrence sur quatre pages Microsoft** ; le **25/10** elle revient en *« 14 octobre 2025 »*. 🔴 **`controle_edition_precedente.py` cherche un JETON retiré qui revient : un défaut qui revient avec une VALEUR NEUVE lui est structurellement invisible.** Son axe ① rend ici `3 jeton(s) retiré(s) du corps corrigé → (aucun)`, et il a raison : « 2031 » n'est pas revenu. C'est le libellé qui est revenu, habillé d'un autre chiffre.

**La provenance que la fiche du 18/10 avait démolie a survécu au changement d'URL.** Le 18/10 rangeait ses spécifications M6 sous *« Spécifications de la puce M6 (source : page Apple Mac mini fr, lue ce jour) »* et sa fiche l'a détruit à la mesure : *« le "2 nm" de la puce M6 est attribué à une page qui n'en dit pas un mot, et c'est la quatrième édition de suite que cette spécification cherche un support »*, avec **zéro occurrence** de `2 nm`, `nanomètre`, `procédé` et `gravure` sur `apple.com/fr/mac-mini/` et sur les neuf autres pages du jour. Le 25/10 écrit *« Spécifications de la puce M6 — source : consomac.fr (26/08/2026), **d'après le communiqué Apple Mac mini M6** »* : l'URL a changé pour une page qui porte vraiment les specs, et le fantôme de la page Apple Mac mini **est resté dans la clause d'attribution**. Mesuré : **`communiqué` = ④ ABSENT, zéro occurrence** sur les 7 924 caractères de la page citée, qui n'attribue rien à un communiqué (elle écrit *« La puce M6 est désormais connue »*). C'est l'axe ② non bloquant qui pointe le passage — `A RELIRE … et cette édition en reprend 6 mots : « specifications de la puce m6 source »` — et il a raison pour une raison qu'il ne sait pas formuler : **la correction a déplacé la source et gardé la provenance**.

**Et contrairement à ce qu'écrivent les fiches du 18/10 et du 01/11, le fondeur TSMC est sourcé dans cette édition.** La fiche du 01/11 range le retour de `TSMC` au 25/10 parmi les corrections défaites et met en surveillance *« si TSMC revient une sixième fois »* ; celle du 04/10 dit *« seul le fondeur reste sans page »*. Mesuré aujourd'hui sur la page que **cette** édition cite : consomac 26/08 écrit *« Il s'agit de la première puce Apple Silicon gravée en 2 nanomètres par TSMC »* — **`TSMC` ① LITTÉRAL**, et `première puce Apple Silicon` ① aussi. Les deux fiches voisines mesuraient leurs **propres** jeux de pages, non celui du 25/10 : la cinquième édition est précisément celle où la spécification a trouvé sa page. 📌 Ce qui reste non sourcé dans la même parenthèse est le comparatif : **`3 nanomètres` = ④ ABSENT**, donc le *« M4 est en 3 nm »* est soudé à un fait sourcé sans l'être lui-même.

**Le +44 % du processeur a été recopié sur la carte graphique, et c'est une classe qu'aucun contrôle du dépôt ne voit.** La section specs dit, correctement, *« CPU : +44 % vs M4 actuel »* — la page écrit *« une puissance en hausse de 44% par rapport à l'iMac actuel »*, et l'arithmétique annoncée tient (1,20 × 1,20 = 1,44). Mais le scénario A écrit *« +44 % CPU, **+44 % GPU** »*, et la page ne donne **aucun pourcentage** au GPU : elle écrit *« Le GPU offre diverses évolutions améliorant le rendu dans les jeux vidéo et les performances en IA »*. Le nombre est sur la page, donc la passe D le valide (`OK`) ; il n'est pas entre guillemets, donc B et B-FR ne le voient pas ; ce n'est pas un nom propre, donc `controle_noms_propres.py` ne le voit pas. **Un chiffre juste attribué au mauvais sujet traverse les dix passes** — troisième occurrence de cette forme en trois audits consécutifs, après l'article 2 crédité à la mauvaise page de la veille ai-act du 06/11.

**L'estimation de prix était fausse de 100 € sur les deux configurations, et la réserve a tenu.** La note raisonne proprement : seul produit M6 tarifé, le Mac mini M6 à 1 049 € contre 949 € pour le M4 au tarif courant, soit +100 € / +10,5 %, *« si l'iMac suit la même logique : Config 1 M6 ≈ 1 899 €, Config 2 M6 ≈ 2 099 € »*. L'édition du 01/11 donne les prix réels de lancement : **iMac M6 10c à 1 799 € et 12c à 1 999 € chez Apple** — exactement les tarifs du M4, soit **+0 € et non +100 €**. Le précédent du Mac mini ne s'est pas transmis à l'iMac. Ce qui sauve le passage est que la note l'avait borné elle-même (*« Prix du M6 inconnu — estimé »*, *« annonce ≠ disponibilité immédiate »*), et au passage elle **corrige** une erreur qui circulait : le *« M6 à +50 % vs M4 »* porte sur le prix de lancement de 2024 (699 €) et non sur le tarif courant, *« l'écart réel sur le tarif courant est +100 €, pas +350 €»* — 1 049/699 = 1,50 exactement.

**Le reste de la note est exact, y compris la prédiction qui portait son alerte 🔴.** L'annonce est tombée le **27/10**, précommandes le **28/10**, disponibilité le **6 novembre 2026** — soit aujourd'hui — contre une note qui écrivait *« annonce officielle attendue le 27 ou 28 octobre 2026 »*. La continuité avec le 18/10 est juste au chiffre près : **13 reconditionnés** la semaine précédente (*« 13 iMac M4 disponibles, minimum 1 519 € »*), **E. Leclerc 1 639 € à −18 %** (−360 € sur 1 999 €), **Amazon 2 209 € à −9,4 %** (−230 € sur 2 439 €) ; les écarts du reconditionné tombent juste (−280 € / −15,6 %, −310 € / −15,5 %) et les deux écarts Mac/Windows aussi (−250 €, −739,05 € arrondi à 739). `controle_decompte.py` rend **COHÉRENT** (7 ✅ · 4 ⚠ · 0 ⛔ · 11), `controle_attributions.py` **0 bloquant** avec la citation de Gurman appariée en ㉖, `controle_edition_precedente.py` **OK**, `controle_noms_propres.py` **4 noms interrogés, 0 non retrouvé, 0 page non lue**, et ㊳ bis lit le décompte du log — **11 testés · 9 retenus · 2 écartés**, aucun 000.

**Quatre réserves de méthode, dont deux contradictions entre éditions sur des affirmations que personne n'a sourcées.** ① L'évolutivité : le 27/09 écrit *« SO-DIMM DDR5, extensible (ex. : 2 slots sur HP OmniStudio) »* et *« M.2 PCIe NVMe (modifiable) »*, le 25/10 écrit *« RAM et SSD non évolutifs sur les deux plateformes »* — quatre semaines d'écart, affirmations opposées, aucune source ni d'un côté ni de l'autre. ② Le support macOS : *« typiquement 7 à 9 ans »* ici, *« 5–7 ans (historique Apple) »* le 01/11, sans source dans les deux cas. ③ La Fnac est comptée **⚠️** quand le log du job la classe **écartée** (`403×1 fnac anti-robot`) et que son prix de 1 799,99 € est quand même employé dans le tableau Windows — le 27/09 comptait le même 403 en **⛔**. ④ La source 10 (`cx0022nf`, 1 799 €) est listée et **n'apparaît nulle part dans le corps**, et la ligne « Mid-range » compare un iMac à un Lenovo que la note déclare **épuisé**, en admettant *« pas d'exact »* dans la case même qui annonce une configuration équivalente.

### Requêtes passées

Cinq pages aspirées sur disque (`aspirer.py`), **aucune n'est entrée en contexte** ; appariement par `chercher.py`, degré ① exigé pour tout ce qui est entre guillemets ; fenêtres lues par `lire_page.py --autour`. Les six contrôles rejoués **un par un** sous `env -i`, jamais en parallèle.

| Source (car. utiles mesurés) | Requêtes | Degré |
|---|---|---|
| `consomac.fr` — news-24460 (7 924) | `la sortie de cette révision serait prévue vers la fin du mois d'octobre` · `Selon le journaliste Mark Gurman` · `TSMC` · `153 Go/s` · `170 Go/s` · `120 Go/s` · `Wi-Fi 7` · `Bluetooth 6` · `Mac mini` · `couleurs` · `première puce Apple Silicon` · `palette de couleurs inédite` | **① ×12** |
| `consomac.fr` — news-24460 | `2 nm` · `2,5 Gigabit Ethernet` | ④ → fenêtres lues : *« gravée en 2 nanomètres »*, *« du Gigabit au 2,5 Gigabit »* — **variantes, pas des absences** |
| `consomac.fr` — news-24460 | **`communiqué`** | 🔴 **④ ABSENT — zéro occurrence** |
| `consomac.fr` — news-24460 | **`3 nanomètres`** | ⚠️ **④ ABSENT** |
| `consomac.fr` — news-24460 | fenêtres `TSMC` et `44` | *« +44 % »* porte sur le **CPU** ; le GPU reçoit *« diverses évolutions »*, **sans chiffre** |
| `macrumors.com` — 25/08 (10 335) | `Apple is likely to unveil a new M6 MacBook Pro and refreshed M6 iMacs in October, based on its typical release schedule` · `All signs point to the M6 models being close to launch` · `before the end of the year` · `Power On` | **① ×4** |
| `learn.microsoft.com` — windows-11-home-and-pro (1 773) | fenêtre `2025` | 🔴 `Retirement Date : In Support` · versions → **10/10/2028** · **rien au 14/10/2025** |
| `learn.microsoft.com` — windows-10-home-and-pro (2 466) | fenêtre `Retirement` | 🔴 **`10/15/2025 6:59:59 AM`** — la date est celle de **Windows 10** |
| `apple.com/fr/shop/buy-mac/imac` (31 598) | prix produit · fenêtre `€` ×20 | **⚠️ confirmé** : 20 € tous de simulation de crédit, aucun prix produit |
| N-1 `2026-10-18_veille_imac.docx` | `13 iMac M4 disponibles` · `1 639 € chez E. Leclerc (−360 €, −18 %)` · `2 209 € (−230 €, −9,4 %)` | **① ×3**, continuité exacte |
| `2026-10-18_veille_imac.fiche.md` | passages `2031` et `Spécifications de la puce M6` | **①** — 2031 = 0 occurrence sur 4 pages Microsoft ; 4ᵉ édition sans support |
| N+1 `2026-11-01_veille_imac.docx` | `annoncé le 27/10/2026` · `1 799 €` · `1 999 €` · `5–7 ans` | **①** — prix réels du M6, et l'estimation démentie |
| `logs/imac-veille_20261025_080300.log` (40 609 o) | `Connection to github.com` ×3 · `PUSH REFUSÉ` ×3 · `controle_astrologie_karmique` · `[mesure]` | **①** — échec de publication mesuré |

**Ce qui n'a PAS été interrogé, et il faut le dire.** `theapplepost.com` (source 7) n'a pas été aspirée : son apport dans la note est *« M6 iMac en octobre avec nouvelles couleurs »*, déjà établi au degré ① sur consomac (*« palette de couleurs inédite »*) et sur iphonote (*« sept couleurs »*, mesuré pour la fiche du 27/09), et l'article est daté du 21/09 pour un événement désormais passé. Les **trois pages marchandes** — LDLC Lenovo, les deux HP — n'ont pas été rouvertes pour arbitrer leurs prix : une fiche produit porte un prix et un stock qui dérivent, et le `1 549 €` est validé par la passe D sur `hp.com` **aujourd'hui**, ce qui ne dit rien du 25 octobre. Et `all-day product launch experience` **n'est pas jugé ici** : relu aujourd'hui sur la page MacRumors du 25/08, il rend ④ — mais c'est une **page vivante**, et la fiche du 18/10 l'avait mesuré **① sur macrumors 25/08, 13/10 et 15/10**. Le rapporter absent aurait été une fausse accusation ; c'est la fiche de N-1 qui est la référence, pas la page du jour.

## Notes liées

- **⬅️ Précédente** · [[2026-10-18_veille_imac.fiche]]
  **elle avait mesuré les deux défauts qui reviennent ici, et ses deux constats ont eu des destins opposés.** Sur le support Windows, elle établit `2031` à **zéro occurrence sur quatre pages Microsoft** : le chiffre ne revient pas, mais **le libellé revient avec une autre valeur fausse** — et l'axe ① ne cherche qu'un jeton. Sur les specs M6, elle démolit l'attribution à la page Apple Mac mini : l'**URL** a été corrigée le 25/10, la **provenance** non. Deux corrections appliquées à la lettre et manquées sur le fond.
- **➡️ Suivante** · [[2026-11-01_veille_imac.fiche]]
  **elle a diagnostiqué l'effet de ce squelette avant que celui-ci ne soit écrit, et une de ses conclusions est à corriger.** Elle montre que l'axe ② a lu **0 citation** parce qu'il n'y avait rien à lire, et que l'axe ① n'avait rien non plus — le `.docx` du 25/10 ne porte **aucun marqueur ni journal**. ⚠️ Mais elle met en surveillance *« si `TSMC` revient une sixième fois »* en tenant son retour du 25/10 pour un défaut : mesuré sur la page que **cette** édition cite, `TSMC` est **① LITTÉRAL**. Le fondeur a trouvé sa page ici ; la surveillance doit porter sur la **provenance**, pas sur le jeton.
- **🔗 Pont** · [[2026-09-27_veille_imac.fiche]]
  **l'autre squelette, écrit le même jour que celui-ci, et les deux notes se contredisent sur l'évolutivité.** Le 27/09 donne la RAM et le SSD des tout-en-un Windows pour extensibles, exemple à l'appui (*« 2 slots sur HP OmniStudio »*) ; le 25/10 les donne pour non évolutifs *« sur les deux plateformes »*. **Aucune des deux affirmations n'est sourcée**, et aucun contrôle ne compare deux éditions sur un énoncé sans guillemets ni chiffre. Les deux notes partagent aussi la phrase vraie sur l'Apple Store rendu en JavaScript, vérifiée pour elles deux.
- **🔗 Pont** · [[2026-11-04_veille_SERAFIN-PH.fiche]]
  **même semaine, autre série, même forme : le gate dit vrai et le diagnostic imprimé est faux.** Là-bas, un marqueur nommant le « Journal des corrections » tronquait le corps lu par toutes les passes et rendait un **vert sur 30 % du document** ; ici le hook refuse en annonçant *« un verdict a changé »* alors que la cause est une page tierce éteinte et une connexion morte. Dans les deux cas le mécanisme a correctement **échoué** et incorrectement **expliqué** — et c'est l'explication qu'un lecteur pressé recopie.
- **🗂️ Dossier** · [[iMac_dossier.fiche]]
  **trois défauts de cette édition sont hors de portée de tout contrôle du dépôt, et pour trois raisons différentes.** Le support Windows faux une troisième fois : l'axe ① cherche un jeton revenu, pas un libellé revenu avec une valeur neuve. Le `+44 % GPU` : le nombre est sur la page, il n'est pas entre guillemets, ce n'est pas un nom propre — dix passes et aucune prise. Le push échoué : `--manques` lit l'épilogue sans lire son code, et ㊳ juge l'**exécution**, qui a bel et bien réussi. 📌 Pistes bornées, non faites, non ordonnées : faire lire le code de sortie par `--manques`, et lui faire comparer `HEAD` à `origin/main` en fin de run — *après un push, toujours comparer le local au distant* est déjà une règle du dépôt, elle n'est simplement appliquée par personne automatiquement.
