---
type: fiche-document
source: 2026-11-22_veille_imac.docx
date_creation: 2026-11-22
date_veille: 2026-11-22
veille: imac
statut: veille-active
publication: "oui — 74f6da7, apres un rattrapage a 99 % du plafond releve a 7 $"
tags:
  - veille/imac
  - registre/perso
  - concept/black-friday-m4
  - concept/m6-sans-remise
  - concept/reconditionne-apple
  - concept/tout-en-un-windows
  - concept/plafond-depasse
  - concept/plafond-releve-a-7
  - concept/zero-hyperlien
  - concept/gate-passe-faute-de-prise
  - concept/un-fait-juste-en-n-et-faux-au-rattrapage
  - concept/instrumentation-sans-mesure
  - concept/rendement-d-un-run
---

# 2026-11-22_veille_imac.fiche

Document source : [[2026-11-22_veille_imac.docx]]

## Résumé

**Ce document est le SECOND de la journée, et il n'a rien en commun avec le premier : le créneau de 8h03 est mort à 105 % de son plafond, et c'est un rattrapage à 14h10, sous un plafond relevé à 7 $, qui a produit le fichier publié.** Le créneau : **5,2747 $ / 5,00 $ (105 %)**, 66 tours, `tool_use`, exit 1, `pas de commit`, **0 contrôle tracé** — ㊳ refusait, la passe A portait un bloquant (`darty.com/fnac.com`) et j'avais mesuré six défauts factuels, dont un `1 299 $` faux là où MacRumors écrit `$1,499` au degré ①. Le rattrapage a tenu : **6,9201 $ / 7,00 $ (99 %)**, 67 tours, 22 min 1 s, `end_turn`, exit 0, publié en `74f6da7` à 14:29:38. ⚠️ **Le choix de +2 $ et non +1 est validé par la mesure, et de justesse** : à 6,00 $ ce run aurait crevé son plafond une troisième fois. ⛔ **Et il reste à 99 % : ce que 7 $ achète n'est pas de la marge, c'est tout juste l'aboutissement.**

**Le document publié a perdu les deux défauts bloquants et il a perdu, avec eux, tout ce par quoi les contrôles le tenaient — c'est la mesure la plus importante de cette fiche.** `controle_attributions.py` rend **0 bloquant**, et le détail dit pourquoi : **B, B-FR, B-NOM, C et C2 sont INERTES** — *« aucune citation française de 9 lettres ou plus »*, *« aucune affirmation prêtée à un nom sans guillemets »* —, et la passe **D n'examine plus que 2 valeurs chiffrées contre 14 ce matin**, parce que toute la grille de prix vit désormais dans des tableaux dont la colonne « Source » porte un nom de site, ce qui n'est pas un contexte d'attribution. `controle_decompte.py` sort en **2** : *« AUCUN DÉCOMPTE ANNONCÉ »*, l'en-tête `Sources : N ✅ · M ⚠️` du matin a disparu. Et `extract_docx.py` rend **`URLS (0)` · `LIENS (0)`** : **le document ne porte plus un seul hyperlien**, les adresses sont en texte brut dans sa rubrique Sources. ㊳ ter le dit — *« ZÉRO HYPERLIEN SERVI … c'est l'état du 13/11/2026 »*. 🔴 **Le push est donc passé non pas parce que le document est devenu juste, mais parce qu'il a cessé d'énoncer ce qui se vérifie.** C'est la phrase de la fiche du 15/11 — *« un document qui garde ses liens se fait attraper ; un document qui les perd passe »* — réalisée dans sa propre série une semaine plus tard. ⚠️ Et je corrige au passage ce que j'allais écrire : l'absence d'hyperliens **n'empêche pas** `controle_attributions.py` de lire les adresses, qu'il prend dans le texte — il a bien aspiré les **7** pages. Ce qui l'a désarmé est l'absence de **citations** et d'**attributions**, pas l'absence de liens.

**Et un fait qui était juste à 08:13 est faux à 14:23 : la configuration à 2 219 €.** Le document publié écrit *« la configuration intermédiaire M6 12c · 16 Go · **512 Go** à 2 219 € »* et lui donne une ligne de tableau « iMac M6 — milieu+ · 512 Go ». Le comparateur, au degré ① et **34 fois sur la page**, écrit : `iMac 24" Retina 4,5K 2026, M6 12 coeurs, 16 Go, SSD 256 Go, 4 ports USB, Argent, Mat … 2 219,00 €`, et un revendeur détaille `CPU 12 cœurs, GPU 12 cœurs, SSD de 256 Go, écran Retina, Verre nano-texturé`. **Ce qui distingue cette référence n'est pas le stockage, c'est le verre nano-texturé** — et le document du matin l'avait écrit correctement (« 256 Go · 4 ports + nano-texturé »). La note se félicite en outre d'avoir « ajouté » cette configuration, que l'édition du 15/11 n'aurait pas relevée : elle l'ajoute fausse.

**Deuxième affirmation neuve, et elle n'existe sur aucune page : « Neural Engine 38 TOPS ».** Cherché sur les **douze** pages aspirées — les trois comparateurs consomac, les deux pages Apple reconditionné, le guide MacRumors cité, les deux articles du 27/10 et du 06/11, la page LDLC, les deux pages d'accueil —, le jeton `TOPS` a **zéro occurrence**. Ce que les sources portent, au degré ①, c'est `5x faster on-device AI performance` (9to5Mac 27/10). ⚠️ Et le document a **perdu** au passage le `Dual` que 9to5Mac écrit (`Dual 16-core Neural Engine`) : le défaut du matin — donner au M6 le chiffre du M4 — n'est pas corrigé, il est **remplacé** par un chiffre inventé. En revanche `PCIe 5.0` est au **①** sur le guide MacRumors, `Bluetooth 6` et `Wi-Fi 7` aussi (le `.0` de « Bluetooth 6.0 » est l'ajout du document), et `+40 % CPU` et `×2 GPU` sont au ① sur 9to5Mac.

**Les heures de relevé sont de nouveau impossibles, et cette fois j'ai testé l'explication évidente — elle est fausse.** La note écrit *« relevé 05:16-05:20 CET »* pour le comparateur M6 et *« relevé 08:04 »* pour le M4, alors que le run a tourné de **14:10:02 à 14:32:06**. Le `08:04` appartient au **créneau mort du matin** ; le `05:16-05:20` n'appartient à rien : la copie de la page que ce run a réellement aspirée est horodatée **14:21:54** et porte des dates de prix par ligne de **13:19 à 13:26**, pas une seule à 05:1x. 🔴 **J'ai soupçonné le cache d'`aspirer.py`** — qui réutilise une page déjà aspirée sans la rafraîchir — **et la mesure l'écarte** : la copie en cache est bien celle de l'après-midi. Même constat pour les **`17 838 car. utiles`** annoncés : c'est **le chiffre exact du document du matin**, quand j'ai mesuré **17 721** à 09:28 et que la page en rend **18 010** à 14h1x. Deux éléments d'instrumentation du document publié ne correspondent donc à **aucune mesure qui existe sur cette machine**, et ils ont traversé une régénération dont le document d'origine avait été **retiré du disque** avant le lancement. ⛔ **Je ne nomme pas le canal, faute de l'avoir mesuré.**

**Les quatre prix Windows ne reposent sur rien, et c'est la troisième semaine de suite — mais la mesure est pire que les semaines précédentes.** La page citée, `ldlc.com/informatique/ordinateur-de-bureau/tout-en-un/c4625/`, rend **6 814 caractères** et contient **zéro prix**, **zéro « IdeaCentre »**, **zéro « Yoga »** et **une** occurrence de « Lenovo », dans un menu : c'est une page de catégorie dont la liste de produits n'est pas rendue en headless. Les jetons `1 049` et `1 249` sont **absents des douze pages** ; `1 049` ne s'apparie qu'en **③ LOCALE** sur la page d'accueil de 9to5Mac, qui écrit `1,049` à propos d'autre chose. Les quatre modèles — Lenovo IdeaCentre AIO 27 ILL11, Lenovo Yoga AIO 27IAH10, Dell 24 AIO EC24260, HP OmniStudio X 27-cx0025nf — et leurs prix sont donc **invérifiables sur les sources citées**, et toute l'« analyse comparative » de la section 4 en dépend.

**Ce qui est juste l'est entièrement, et c'est la moitié Apple du document.** Les quatre prix M6 (`1 799,00 €`, `1 999,00 €`, `2 219,00 €`, `2 439,00 €`) sont au **①** sur le comparateur M6 ; les trois prix M4 (`1 569,00 €`, `1 619,00 €`, `2 199,00 €`) au **①** sur le comparateur M4. **Le reconditionné est exact sur ses trois affirmations** : en appariant libellé → prix sur `apple.com/fr/shop/refurbished/mac/imac`, **28 entrées** (la note dit « 28 lignes »), minimum **`1 429,00 €`** en 8c/8c, et **17 entrées en 10c/10c dont le minimum est `1 599,00 €`** — les deux lignes « dès 1 429 € » et « dès 1 599 € » sont vérifiées au centime. L'arithmétique est juste partout : `+750 €/+71 %`, `+550 €/+44 %`, `+180 €/+14 %`, `+310 €/+25 %`, `−370 €` et `−20 %` se recalculent exactement, et `J−8` au 30/11 aussi. **Et le `1 299 $` faux du matin a disparu** : le document ne donne plus de prix US, alors que le guide MacRumors qu'il cite porte `$1,499` **trois fois**.

**㊳ ter rend le pire rendement de toute la série, et il a doublé en six heures.** `1.369 $ / 1 000 car. utiles` pour 6,9201 $ et **5 056 caractères** — contre `0.726` ce matin (7 261 car.) et une **médiane de série de 0.272**, soit **5×**. Rang **5/5**, drapeau levé. En une journée, le job a dépensé **12,19 $** sur deux tentatives pour publier un document **plus court de 2 205 caractères** que celui qu'il avait écrit le matin. ⚠️ **Et le contrôle porte un faux positif que je dois nommer, puisque je l'ai écrit hier** : il annonce *« document CORRIGÉ depuis le run »* alors que rien ne l'a été — son motif `CORRIGE` apparie le titre `📝 Journal des corrections`, et la section dit *« Aucune correction à ce jour »*. Le rendement affiché **est** celui du run ; c'est l'avertissement qui est de trop.

**Un dernier chiffre que je ne peux pas prouver : « édition n° 29 ».** Le disque porte **24** `.docx` de cette série, du 14/06 au 22/11, soit exactement **24 dimanches consécutifs** — la numérotation du document est donc probablement en avance de cinq, mais rien dans le dépôt ne dit qu'il n'a pas existé d'éditions antérieures au 14/06, et je ne tranche pas sur une absence.

**Trois erreurs à moi dans cette séance, dont deux sur des raisonnements que la mesure a démentis.** ① J'ai **écarté la fiche de `sources/veille/`** de peur que l'auto-push la publie : le `git add` de `run_job.sh:476` porte `':(exclude)sources/veille/*.fiche.md'`, ce motif **franchit le `/`**, et un `git add --dry-run` l'a montré en une commande — seul le `.docx` serait pris. Le retrait restait nécessaire, mais pour une autre raison : **le garde anti-doublon du prompt apparie `veille_imac`, pas `.docx`**, donc la fiche seule aurait fait retomber le job dans son arrêt d'Étape 1. ② J'ai **extrait le bloc `case` des plafonds sans la ligne `BUDGET_DEFAULT="2.00"`** qui le précède, donc un id inconnu rendait une chaîne vide et j'ai failli consigner une régression ; rejoué avec la ligne : **2,00 $**. ③ J'ai **lu `exit=0`** sur un `controle_attributions.py` tuyauté dans `tail` — le code lu était celui de `tail` ; sans tuyau : **exit 1**. La règle du 15/10, enfreinte encore.

| Affirmation de la note publiée | Page | Verdict |
|---|---|---|
| `1 799 €` · `1 999 €` · `2 219 €` · `2 439 €` (grille M6) | consomac M6 | **①** |
| `1 569 €` · `1 619 €` · `2 199 €` (M4 revendeur) | consomac M4 | **①** |
| « 28 lignes » · « dès 1 429 € » · « dès 1 599 € » (reconditionné) | apple.com refurb/imac | **①** — 28 entrées, min 1 429,00 €, min 10c/10c 1 599,00 € sur 17 |
| `PCIe 5.0` · `Bluetooth 6` · `Wi-Fi 7` | MacRumors roundup | **①** (le `.0` de « Bluetooth 6.0 » est un ajout) |
| `+40 % CPU` · `×2 GPU` · `×5 performance IA` | 9to5Mac 27/10 | **①** (`40% faster CPU`, `2x faster graphics`, `5x faster on-device AI`) |
| **« M6 12c · 16 Go · 512 Go à 2 219 € »** | consomac M6 | **FAUX** — la page écrit `SSD 256 Go … Verre nano-texturé`, 34 fois, au ① |
| **« Neural Engine 38 TOPS »** | aucune | **④** — `TOPS` : 0 occurrence sur les 12 pages |
| **« relevé 05:16-05:20 CET »** · **« relevé 08:04 »** | log du run + horodatage des pages | **impossibles** — run 14:10→14:32, page datée 13:19–13:26 ; `08:04` est l'heure du créneau MORT |
| **« 17 838 car. utiles »** | mesure directe | **non remesuré** — 17 721 à 09:28, **18 010** à 14h1x ; chiffre repris du document du matin |
| `1 049 €` · `1 249 €` · `~1 328 €` · `2 199 €` (Windows) | ldlc.com (citée) | **④** — la page rend **0 prix**, 0 « IdeaCentre », 0 « Yoga » |
| « édition n° 29 » | disque | **24** éditions, 24 dimanches — non prouvable, probablement en avance de 5 |
| `1 299 $` (défaut du matin) | — | **disparu** ✅ |
| `darty.com/fnac.com` (bloquant du matin) | — | **disparu** ✅ — passe A rend 0 bloquant |

### Requêtes passées

| Requête | Résultat |
|---|---|
| `1 799,00 €` · `1 999,00 €` · `2 219,00 €` · `2 439,00 €` | **①** consomac M6 |
| `1 569,00 €` · `2 199,00 €` · `1 619,00 €` | **①** consomac M4 |
| `1 599,00 €` | **①** apple.com refurb/imac |
| `38 TOPS` | **④** — 0 occurrence de `TOPS` sur les 12 pages aspirées |
| `PCIe 5.0` | **①** MacRumors roundup (1 occurrence) |
| `Bluetooth 6.0` | **④** — la page écrit `Bluetooth 6` (2 occurrences) |
| `1 049` · `1 249` | **③** sur une page d'accueil sans rapport · **④** — absents des 12 pages |
| `IdeaCentre AIO 27 ILL11` · `Yoga AIO 27IAH10` | **④** — la page LDLC citée n'en porte aucun |
| fenêtre `2 219,00` sur consomac M6 | `M6 12 coeurs, 16 Go, SSD 256 Go, 4 ports USB, Argent, Mat` — **256 Go, nano-texturé** |
| appariement libellé → prix sur refurb/imac | **28** entrées, min **1 429,00 €**, **17** en 10c/10c dont min **1 599,00 €** |
| comptage `Lenovo` / `IdeaCentre` / `Yoga` / prix sur la page LDLC | **1 / 0 / 0 / 0** |
| horodatages `Prix datant du … CET` du comparateur M6 à 14h1x | `13:19` ×1 · `13:21` ×3 · `13:22` ×7 · `13:23` ×2 · `13:26` ×4 — **aucun 05:1x** |
| `mtime` de la page en cache | **14:21:54** — le cache d'`aspirer.py` est écarté comme explication |
| `TOPS` · `$1,499` · `Neural Engine` sur le guide MacRumors | **0** · **3** · **4** |

## Correction du livrable — 22/11/2026 (soir)

🔴 **Cette fiche accusait un document qui avait raison, et c'est la mesure qui l'a dit.** Elle écrivait que la ligne « M6 12c · 16 Go · **512 Go** à 2 219 € » était **FAUSSE** et qu'elle ne devait pas être versée au dossier. Les 14 références Apple du comparateur consomac, extraites une à une le 22/11/2026 : **`2 219 €` désigne DEUX configurations** — 16 Go/**256 Go** à verre nano-texturé (`MH2U4FN/A`, une référence) **ou** 16 Go/**512 Go** à verre standard (`MH154FN/A`, `MH1J4FN/A`, `MH1Q4FN/A`, `MH1F4FN/A`, quatre coloris) —, chaque option valant **+220 €** sur la base de 1 999 €. **Le prix et la capacité de la ligne de tableau étaient justes ; aucune cellule n'a été touchée.**

| Ce qui a été corrigé | Avant | Après |
|---|---|---|
| **annonce de nouveauté**, en tête | `la configuration intermédiaire M6 12c · 16 Go · 512 Go à 2 219 € n'avait pas été relevée la semaine précédente` | `figurait déjà dans l'édition du 15 novembre 2026, à ce prix et à cette capacité` |
| **point de vigilance** | `⚠ Config M6 2 219 € (12c · 16Go · 512Go) : non relevée le 15/11 — tableau complet désormais` | `déjà relevée à ce prix dans l'édition du 15 novembre 2026` |

⚠️ **Le seul défaut réel de ce document était donc l'affirmation sur l'édition précédente, énoncée deux fois.** L'édition du 15/11 porte bien cette configuration à ce prix ; ce qu'elle écrivait de travers est la mention du **verre** (`512 Go + nano-texturé`, qui cumule les deux options), corrigée le même jour dans l'édition concernée.

🔴 **Et ma consignation de la veille était fausse sur sa prémisse.** J'avais écrit que deux faits avaient été « **justes puis défaits dans la même journée** ». Mesuré sur les 24 éditions : les **deux étaient déjà faux dans l'édition PUBLIÉE du 15/11**. Le document de 8h03 n'a rien défait — il a **reconduit** le `1 299 $` et **corrigé** la capacité ; c'est le rattrapage de 14h10 qui est revenu au `512 Go` de N-1 en y perdant « nano-texturé », et ce 512 Go n'était pas faux. **J'avais lu la fiche du 15/11, qui portait `$1,499` au degré ①, et j'en avais conclu que le document le portait aussi : une fiche n'est pas son document.**

🟢 **Quatrième état, après « le défaut revient » et « le juste se défait » : un faux jamais corrigé se reconduit.** Les trois axes de `controle_edition_precedente.py` partent du journal des corrections de N-1, et le 15/11 n'avait **jamais** été corrigé : il n'y avait aucune correction à voir se défaire. Un contrôle qui part d'une **correction** ne voit que les défauts déjà vus ; pour voir un faux jamais vu, il faut une référence **extérieure au corpus** — ici la grille mesurée au degré ①.

⚠️ **Ce que la correction ne ferme pas.** `controle_faits_imac.py` compare des **chiffres** à une grille : il ne voit **ni** l'affirmation corrigée ici (une assertion sur l'édition précédente), **ni** une grille Apple qui changerait, auquel cas il accuserait un document juste jusqu'à ce qu'on remesure. Mesuré : il rend **0 contradiction sur ce document, avant comme après** la correction.

🧪 **Gardes du patch** : identiques à ceux du 15/11 — sauvegarde d'abord, édits de la fin vers le début, **garde par soustraction dans l'espace XML**, marqueurs en fin de paragraphe hors hyperlien et ne nommant pas la section du journal, `testzip()`. Gate `--docs` sur les deux documents : **exit 0, zéro ✗**.

## Notes liées

- **⬅️ Précédente** · [[2026-11-15_veille_imac.fiche]]
  **ses trois questions ont une réponse mesurée, et sa phrase la plus incidente est devenue le sujet du jour.** ① Les premières remises M6, attendues « à partir du 20/11 » : **toujours aucune** à J+16, prix conseillé sur les quatre configurations. ② Le Black Friday côté Windows : il est là, et **attribuable à aucune page** pour la troisième semaine — avec cette fois une page de catégorie LDLC qui ne rend aucun prix. ③ *« si le reconditionné Apple revient dans la note avec ses prix »* : **oui, et c'est la partie la mieux établie du document** — 28 lignes, 1 429 € et 1 599 € vérifiés au centime, après le `exit 28` du 15/11. ⚠️ Et sa phrase sur la veille AI Act du 13/11 — *« un document qui garde ses liens se fait attraper ; un document qui les perd passe »* — décrit exactement ce qui s'est passé ici : le document du matin, qui portait sept hyperliens et des citations, a été refusé ; celui de l'après-midi, qui n'en porte aucun et ne cite plus personne, est passé.
- **➡️ Suivante** · édition du **dimanche 29/11/2026 à 8h03** — à surveiller : la **fin des promotions M4 au 30/11**, donc le dernier créneau où elles vivent ; les premières remises M6 à **J+23** ; et surtout **si le plafond de 7,00 $ tient**, puisque celui-ci a été consommé à **99 %**. ⚠️ Trois contraintes de méthode : une **marque d'échec est posée jusqu'au 25/11**, donc `TOURS_MINI=7` s'applique à tout rattrapage d'ici là ; le **garde anti-doublon apparie `veille_imac`**, donc toute reprise manuelle exige d'écarter le `.docx` **et** la fiche ; et si le prochain run reproduit un document **sans citations ni hyperliens**, le gate le laissera passer de nouveau — ce n'est pas un défaut du gate, c'est un défaut de prise.
- **🔗 Pont** · [[2026-11-20_veille_ai-act.fiche]]
  **c'est la fiche où le remède a été écrit, et la journée en donne deux cas de plus.** Là-bas, les lettres de l'article 5 §1 — justes le 15/11, fausses le 20/11 malgré une fiche qui demandait de les reconduire — ont été **versées au prompt comme un fait acquis**, gardées par un contrôle d'**appariement**. Ici, deux faits se sont défaits : `$1,499` était au ① dans la fiche du 15/11 et le document du matin l'a remplacé par `1 299 $` ; la configuration à **2 219 € / 256 Go nano-texturé** était juste dans le document du matin et le rattrapage l'a republiée en **512 Go**. **Entre « le défaut revient » et « le juste se défait », le second n'est surveillé par rien** — les trois axes de `controle_edition_precedente.py` lisent les corrections de N-1, pas les justesses de N-1. 📌 Piste bornée, non ordonnée : verser au prompt `imac-veille` quatre faits acquis — le prix de lancement `$1,499`, la configuration d'entrée en **10c/10c**, la référence à **2 219 € = 256 Go nano-texturé**, et les deux adresses d'articles à la place des racines — avec un garde d'appariement sur le modèle de `non_regression/lettres_article5.py`.
- **🔗 Pont** · [[2026-11-08_veille_imac.fiche]]
  **elle décrivait un run à 1 tour et 101 % sans un jeton compté ; la journée du 22/11 montre la forme achevée de la même panne.** Deux tentatives, **12,19 $** dépensés, un créneau perdu et un rattrapage à 99 % d'un plafond relevé de 2 $, pour un document **plus court** que celui du créneau mort. 📌 Sa piste d'un cinquième état `✗ PUBLIÉ SANS CONTRÔLE` pour `rattrapage_jobs.sh --manques` garde tout son objet : ce matin, `controle-livrables` a crevé son plafond à **101 %** (4,0446 $ / 4,00 $) et son agent a **commité la note une seconde avant de mourir** (`b92a8ea`, 11:15:54) sans la pousser — et ㊳ est **structurellement muet** dessus, sa table n'attribuant que 8 dossiers, dont `livrables/controles/` ne fait pas partie.
- **🗂️ Dossier** · [[iMac_dossier.fiche]]
  à mettre à jour, et il faut y **retirer** autant qu'y ajouter. **À verser, au degré ①** : grille M6 à quatre références — `1 799 €` (10c/10c · 16 Go · 256 Go · 2 ports), `1 999 €` (12c/12c · 256 Go · 4 ports), **`2 219 €` (12c/12c · 16 Go · 256 Go · verre nano-texturé)** et `2 439 €` (12c/12c · 24 Go · 512 Go), **aucune remise revendeur à J+16** ; `PCIe 5.0`, `Wi-Fi 7`, `Bluetooth 6`, `Dual 16-core Neural Engine`, `40% faster CPU`, `2x faster graphics`, `5x faster on-device AI` ; prix US **`$1,499`** pour le 10c/10c, `$1,699` pour le 12c/12c, `$1,449` en tarif éducation ; M4 en déstockage à `1 569 €` (−13 %), `1 619 €` (−19 %), `2 199 €` (−10 %), flash Amazon à `1 559 €` jusqu'au **30/11/2026** ; reconditionné Apple **28 lignes**, de `1 429,00 €` (8c/8c) à `2 619,00 €`, minimum 10c/10c `1 599,00 €`. ⛔ **À ne PAS verser** : la configuration `2 219 € / 512 Go`, fausse ; `Neural Engine 38 TOPS`, introuvable ; les quatre lignes Windows et leurs prix, attribuables à aucune page ; les heures de relevé `05:16-05:20` et `08:04`, que le log du run dément ; et l'« édition n° 29 », que le disque ne corrobore pas.
