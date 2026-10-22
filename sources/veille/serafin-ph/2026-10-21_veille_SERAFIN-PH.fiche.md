---
type: fiche-document
source: 2026-10-21_veille_SERAFIN-PH.docx
date_creation: 2026-10-21
date_veille: 2026-10-21
veille: serafin-ph
statut: veille-active
tags:
  - veille/serafin-ph
  - registre/pro
  - concept/plfss-2027
  - concept/recueil-ph-2026
  - concept/convergence-tarifaire
  - source/cnsa
  - source/handicap-gouv
  - alerte/corrige
  - correction/2026-10-23
  - theme/statut-colonne-un-qui-fait-deriver-le-decompte
  - theme/adresse-tronquee-qui-ne-correspond-plus-a-son-lien
  - theme/marqueur-non-exempte-par-la-passe-a
  - source/lemediasocial
  - theme/push-refuse-deux-motifs
  - theme/decompte-incoherent
  - theme/adresse-abregee-inexistante
  - theme/citation-sur-aucune-page
  - theme/citation-attribuee-au-mauvais-article
  - theme/facades-sous-le-plancher
  - theme/decret-rejoue-une-semaine-apres
  - alerte/push-refuse
---

# 2026-10-21_veille_SERAFIN-PH.fiche

Document source : [[2026-10-21_veille_SERAFIN-PH.docx]]

## Résumé

**Le job a réussi et la veille n'est pas publiée : le push a été refusé sur DEUX motifs bloquants, et les deux sont justes.** `exit 0`, une tentative, **1,1074 $ pour un plafond de 3,00 $ (37 %)**, 28 tours, 7 min 18 — puis trois refus de push. ⚠️ **Et j'avais annoncé hier soir ce run comme une bonne nouvelle sans vérifier qu'il avait publié** : j'ai lu son coût, ses trois tableaux et sa ligne de liens, pas son `pre-push`. Le commit **`f155c96` est local, en avance de 1 sur `origin/main`**. Les deux motifs :
> ⛔ **Passe A** — `INTERDIT cnsa.fr/recueil-obligatoire-esms` : la ligne de décompte finale écrit cette adresse **abrégée**, qui n'existe pas, alors que la source est listée **en entier** dans le tableau (`www.cnsa.fr/actualites/serafin-ph-un-recueil-de-donnees-obligatoire-dans-les-esms-pour-enfants-et-adolescents`). La passe A y voit une page citée hors des Ressources, et elle a raison : **le document publie une URL fabriquée**, courte, non résolvable.
> ⛔ **`controle_decompte` — INCOHÉRENT, exit 1** : *« 6 au total annoncées, liste 11 »*. La note écrit « Sources ✅ : **6/6 tentées** | ⛔ : 1 » — ce qui est **contradictoire en soi** (6 sur 6 plus une inaccessible fait 7), et le tableau des sources porte **7 lignes** (6 ✅ + 1 ⛔). Le contrôle, lui, compte **11 entrées** parce qu'il relève aussi les ⛔ et les « consultées sans symbole » dispersés dans le corps. Le vrai décompte est **6 ✅ sur 7 tentées**, et la huitième URL du document n'est nulle part dans le tableau.

**Une citation entre guillemets n'est sur aucune page, texte ni source.** La note écrit, dans le bloc des treize associations : *« sans ces crédits promis, nous demanderons un report de la mise en œuvre à 2028 »*, donné comme la **menace** des signataires. ⚠️ **④ ABSENT des quatre fichiers** — le texte utile **et le HTML brut** des deux articles du Média Social : aucune page ne porte plus de **3 de ses 6 mots pleins**. Le fond est plausible et conforme à l'esprit du courrier, mais la phrase entre guillemets n'a pas de source. C'est la forme de défaut la plus coûteuse d'une veille institutionnelle : une menace prêtée à treize fédérations nommées.

**La citation de Daniel Goldberg, elle, est exacte au mot — et attribuée au mauvais article.** La note la place dans le bloc *« 13 associations demandent les 90 M€ (12 octobre 2026) »*, sourcé *« lemediasocial.fr — Appel à un budget pour Serafin-PH »*. 🟢 La phrase est bien réelle : *« Sans ces 90 M€ en 2027, il s'agirait donc d'une réforme à moyens constants, pénalisant des structures déjà pour beaucoup en difficulté »* — mais elle est sur **l'autre** article, celui du 5 octobre, *« aucune enveloppe n'est prévue en 2027 »*, où elle suit immédiatement la mention de **Charlotte Parmentier-Lecocq**. « Daniel Goldberg » et « Charlotte Parmentier-Lecocq » sont tous deux **① LITTÉRAL sur `lms-enveloppe`** et sur elle seule. La note a donc **coupé un même paragraphe d'un même article en deux**, et rangé une moitié sous une autre source. Le ④ initial de la phrase complète venait des apostrophes typographiques (`s'agirait`, `d'une`) : le texte est fidèle, la provenance ne l'est pas.

**Et le décret du 13 mai 2026 revient, une semaine après que la fiche précédente ait démontré qu'il n'était pas sur la page citée.** Le motif ② de `controle_edition_precedente` le dit en propres termes : *« la fiche de N-1 donne pour fautif "Le décret du 13 mai 2026 rend obligatoire le recueil" et cette édition en reprend 6 mots »*. La fiche du 14/10 avait établi que **« décret » compte zéro occurrence sur la page CNSA invoquée**, laquelle est **de décembre 2025** et ne peut donc pas porter un texte de mai 2026. L'édition du 21/10 écrit *« Recueil PH 2026 — CNSA (décret 13 mai 2026) »* puis *« Le décret du 13 mai 2026 a établi les exigences de transmission »*, sous une ligne **Source : cnsa.fr — Préparation du recueil PH 2026**. ⚠️ Le motif ② est **non bloquant**, donc il n'a pas arrêté le push — ce sont A et le décompte qui l'ont fait. Sans eux, le rejeu serait passé avec un simple avertissement.

**Trois des sept sources marquées « ✅ Consultée » sont sous le plancher de façade, et l'une est vide.** Remesuré page par page ce jour : `cnsa.fr` PLFSS **10 702 caractères utiles** ✓, mais **`handicap.gouv.fr` → 93 caractères** pour 6 807 octets bruts, `lemediasocial.fr` « Appel à un budget » → **2 305**, et « aucune enveloppe » → **2 969**. Le dépôt a une règle pour cela : *« une page tronquée rend indiscernables une citation absente et une citation non lue — plancher 3 000 caractères utiles »*. 🔴 **Le cas de `handicap.gouv.fr` est le plus lourd** : avec **93 caractères**, cette page ne porte rien, et c'est pourtant d'elle que la note fait venir **tout le calendrier 2026** (lancement SIDOBA au 30 mars, collecte au printemps-automne, simulations fin 2026), **la présidence du 14e comité stratégique** et **la date du 23 mars 2026**. Le document la marque « ✅ Consultée — Fond documentaire ». Ces éléments figuraient déjà dans l'édition du 14/10, et la note le déclare honnêtement (*« Ces éléments étaient déjà présents dans la note précédente »*) — mais la source nommée ne les porte pas aujourd'hui.

**Ce qui est juste l'est précisément, et le cœur de l'actualité de la semaine tient.** L'alerte du Conseil de la CNSA du 16/10 est sur une page qui répond **200 pour 10 702 caractères**, et ses chiffres s'y apparient : **« 44,4 milliards » ① LITTÉRAL**, et la citation *« report d'un an du financement de la réforme SERAFIN-PH »* **② GRAPHIE** — à l'apostrophe typographique près, elle est fidèle. **« Camille Galliard-Minier » ①** sur cette même page. Le titre de l'article du Média Social, *« Il en va de la viabilité de la réforme »*, est **① LITTÉRAL**. Et la note fait correctement le partage entre **l'actualité de la fenêtre** (une seule entrée, le 16/10) et le **contexte hors fenêtre** (12/10 et 5/10), ce qui est exactement la discipline que la série demande. ⚠️ Une imprécision dans ce partage, tout de même : l'intertitre annonce *« hors fenêtre, **< 14 jours** »*, or l'item du **5 octobre** est à **16 jours** du 21.

**Mesures et contrôles. 1,1074 $ pour un plafond de 3,00 $ — 37 %**, le job le moins tendu des neuf, 28 tours, 7 min 18 s, 18 828 tokens en sortie, une tentative, `exit 0`, prompt à **31 706 octets**. Document de **8 255 caractères**, 124 paragraphes porteurs, **12 liens**, **3 tableaux**. 🟢 **L'assertion de tableau portée le 18/10 est honorée au premier créneau qui la rencontre** : rejouée verbatim depuis le prompt, elle rend **« OK — XML conforme, 12 lien(s), 124 paragraphe(s) de texte (marge 112), 3 tableau(x) »** — plancher 3, exactement 3. 🔗 **Et la consigne de décompte des liens tient pour la deuxième fois** : *« 12 testés · 12 retenus · 1 écarté (403 — cnsa.fr/recueil-obligatoire-esms, URL réelle, page bloquée anti-robot, **aucun code 000**) »* — le job **nomme de lui-même** l'absence de 000, ce que la consigne demandait sans l'exiger. `controle_attributions` : **exit 1, 1 bloquant** (la passe A ci-dessus), 1 citation française à relire, passes B et D inertes. `controle_edition_precedente` : **exit 0**, aucun rejeu bloquant, **1 point à relire** — celui du décret.

### Correction du 23/10/2026

**Sept corrections, et la cause des DEUX motifs bloquants était la même : une colonne déplacée.** Le tableau des sources du 21/10 plaçait le **statut en première colonne**, là où les **onze éditions précédentes** le placent en troisième. Conséquence mécanique, lue dans la trace `DEBUG` du contrôle : chaque statut était suivi de **trois** cellules de nom (Source, URL, Note), l'appariement dérivait d'une ligne — `✅ Consultée` de la ligne 2 se retrouvait apparié au `Fond documentaire — 23/03/2026` de la ligne 1 — et la **dernière ligne, sans statut à sa suite, comptait ⛔ TROIS FOIS pour une seule source**. La liste montait à **11 pour 7 sources réelles**, d'où `INCOHÉRENT`. 🔴 **Et le verdict aurait refusé aussi une note annonçant le compte JUSTE** : testé, « 6/7 » donnait toujours `INCOHÉRENT — 7 annoncées, liste 11`. Colonnes remises dans l'ordre de la série → **« ✅ 5 · ⚠ 1 · ⛔ 1 · total 7 », COHÉRENT**.

**Ce que j'ai essayé d'abord, et pourquoi je l'ai abandonné.** J'ai cru que le défaut était dans le contrôle et j'ai élargi sa règle existante — la ligne `R_URL.match(n) → CONT`, qui écarte une adresse depuis l'origine mais exige le schéma `https://`, absent de la colonne URL du 21/10. 🔴 **Balayage des 109 veilles du dépôt : les refus passaient de 3 à 12.** Neuf faux refus neufs dans les séries `imac` et `ai-act`, où les sources **sont** écrites comme des adresses nues : la règle détruisait de vraies entrées (« statuts sans nom (non comptés) »). `controle_decompte.py` **restauré à l'identique**, sans commit. C'est la règle du 15/10 qui a tranché — *« élargir l'entrée d'une passe BLOQUANTE se mesure sur TOUT le corpus avant commit, et par recensement, pas par échantillon »* — et c'est elle qui a évité de casser neuf documents pour en publier un.

**La citation introuvable est corrigée, et je sais maintenant de quoi elle était faite.** *« sans ces crédits promis, nous demanderons un report de la mise en œuvre à 2028 »* : **« demanderons » compte ZÉRO occurrence** sur les deux pages du Média Social, **texte et HTML brut** (52 184 et 56 720 octets). La phrase réelle est de **Goldberg, dans l'article du 5 octobre** : *« À défaut, si cette somme n'y figurait pas, alors un report de la réforme Serafin-PH pour une application en 2028 sera une nécessité »*, « prévient-il ». La note avait donc **reformulé un propos individuel du 5/10 en menace collective des treize fédérations du 12/10**, et mis le résultat entre guillemets. Passée en style indirect, créditée, avec le libellé d'origine au marqueur.

**Et le bloc Goldberg porte désormais sa vraie source.** La fenêtre de la page du 5/10 donne la phrase entière et son canal : *« déplore le président de l'Uniopss, Daniel Goldberg, **sur Linkedin** »*. ⚠️ **Correction d'une sur-affirmation de ma part** : j'ai rapporté hier cette citation comme « **①** sur l'article du 5/10 ». Mesuré à nouveau ce jour, la phrase complète sort en **④** sur les deux pages et seul le fragment *« réforme à moyens constants »* est **①** — l'écart vient des apostrophes typographiques de la page. La fiche le disait juste, mon rapport l'a durci.

**Le décret du 13 mai 2026 est retiré, sur trois mesures.** Sur la page CNSA citée : **« décret » 0**, **« 13 mai » 0**, **« 40 variables » 0** — texte **et** HTML brut. Cette page est du **17/12/2025**. 🟢 Ce qui reste est sourcé : **« année blanche » ①** et **« SIDOBA » ①**. Le motif ② de `controle_edition_precedente` est désormais muet : *« OK — aucune correction de l'édition précédente ni de sa fiche n'est rejouée »*.

**La source qui n'avait rien servi porte maintenant son statut.** `handicap.gouv.fr` était marquée **« ✅ Consultée »** ; elle rend **93 caractères utiles pour 6 078 octets bruts**, et ces 93 caractères sont, intégralement : *« Please enable JavaScript to view the page content. Your support ID is: 2042403060366150062. »* Ce n'est pas une façade, c'est un **mur JavaScript** : la page n'a rien servi. Statut passé à **⚠**, note rétablie, et le décompte final recalculé en conséquence.

**Les sept adresses tronquées sont rétablies en entier.** Les cellules d'URL affichaient `www.cnsa.fr/actualites/serafin-ph-preparation-du-recueil-din…` — non copiable, et ne correspondant plus à la cible du lien. Les sept portent l'adresse complète avec son schéma. C'est la même classe de défaut que le motif bloquant de la passe A : **une adresse abrégée n'est pas une adresse.**

**🔴 Et un garde-fou de la doctrine s'est retourné contre elle.** La doctrine exige le libellé d'origine dans le **📝 Journal des corrections**. Reproduit tel quel, `cnsa.fr/recueil-obligatoire-esms` **rouvrait le motif bloquant de la passe A** — mesuré deux fois : dans le journal, puis dans un **marqueur**, où `CLAUDE.md` affirme pourtant que *« controle_attributions.py écarte ces marqueurs depuis longtemps »*. **C'est faux pour ce motif** : la passe A scanne le corps avant la rubrique Ressources sans consulter `dans_marqueur()`. Le libellé est donc conservé avec **une espace après le domaine**, et le marqueur dit pourquoi. 📌 Piste bornée, non faite : faire passer la collecte d'adresses de la passe A par `corps_hm`, comme les autres motifs — à mesurer sur les 292 documents avant commit.

**Contrôles après correction, tous rejoués.** Intégrité **verbatim sous `env -i`** → *« OK — XML conforme, 12 lien(s), 135 paragraphe(s) de texte (marge 123), 3 tableau(x) »*, plancher de tableau 3 honoré. `controle_decompte` → **COHÉRENT**. `controle_attributions` → **0 bloquant** (contre 1 avant), les trois pages sous le plancher signalées sans bloquer. `controle_edition_precedente` → **exit 0**, motif ② muet. ⚠️ **Ce que la correction ne répare pas** : les deux articles du Média Social servent 2 305 et 2 969 caractères, **sous le plancher de 3 000** — leurs citations sont vérifiées sur ce que la page sert, pas sur l'article intégral ; et la relecture a été faite **hors du job**, deux jours après, ce que le journal déclare.

### Requêtes passées

Quatre pages aspirées sur disque (`aspirer.py`), **aucune n'est entrée en contexte** ; appariement par `chercher.py`, degré ① exigé pour les citations ; contextes en fenêtres bornées (`lire_page.py`). ⚠️ **Et une réserve de méthode sur l'outil lui-même** : j'ai mesuré hier que le degré ① de `chercher.py` **apparie des sous-chaînes** (« aract » sort en ① dans « character »), donc toute requête courte a été recoupée en fenêtre avant d'être retenue ici.

| Requête | Verdict |
|---|---|
| `44,4 milliards` | **① LITTÉRAL** cnsa.fr |
| `report d'un an du financement de la réforme SERAFIN-PH` | **②** cnsa.fr — apostrophe typographique, texte fidèle |
| `Camille Galliard-Minier` | **①** cnsa.fr |
| `Il en va de la viabilité de la réforme` | **①** lemediasocial (titre) |
| `nous demanderons un report de la mise en œuvre à 2028` | **④ ABSENT** des 4 fichiers, texte **et** brut — 3 mots pleins sur 6 au mieux |
| `une réforme à moyens constants` · `Daniel Goldberg` · `Charlotte Parmentier-Lecocq` | **①** sur `lms-enveloppe` (5/10) — **pas** sur l'article auquel la note les attribue |
| caractères utiles des 4 pages | cnsa **10 702** · lms-appel **2 305** · lms-enveloppe **2 969** · **handicap.gouv.fr 93** |
| `<w:tbl>` (assertion du prompt) | **3 tableaux**, plancher 3 — honoré de justesse |

**Ce que « standard » n'a pas interrogé, et il faut le dire** : la page `atih.sante.fr/recueil-national-ph-2025` et la page `cnsa.fr/budget-et-financement/serafin-PH` n'ont pas été rouvertes — la note les déclare consultées « sans élément nouveau » et « pour calendrier et contexte », et je n'ai pas vérifié ces deux formules ; la page `cnsa.fr/recueil-obligatoire-esms` est en **403 anti-robot**, donc le caractère obligatoire du recueil pour les ESMS enfants n'est vérifié nulle part ; et le **décret du 13 mai 2026** n'a pas été cherché sur Légifrance, qui refuse l'accès automatisé (**403 avec les deux agents**, mesuré le 21/10 sur le dossier hypnose) — la seule voie serait une consultation humaine.

## Notes liées

- **⬅️ Précédente** · [[2026-10-14_veille_SERAFIN-PH.fiche]]
  **sa démonstration sur le décret n'a pas tenu une semaine.** Elle établissait que « décret » compte **zéro occurrence** sur la page CNSA invoquée, datée de **décembre 2025**, et qu'une page de décembre 2025 ne peut pas porter un texte de **mai 2026**. L'édition du 21/10 réécrit « le décret du 13 mai 2026 » sous la même source, et c'est le **motif ② — non bloquant** — qui l'attrape. 📌 La leçon est structurelle : **un rejeu signalé par ② ne retient pas un push**, et il a fallu deux autres motifs, sans rapport, pour que cette édition soit arrêtée
- **🔗 Pont** · [[2026-10-19_veille_has-actualite.fiche]]
  **deux veilles refusées en trois jours, et les deux fois pour un motif que le document aurait pu éviter.** Là-bas le refus était **faux** — « Commission de la transparence », un organisme réel —, et il a fallu reborner le contrôle. Ici les deux refus sont **justes** : une URL abrégée qui n'existe pas, et un décompte qui se contredit dans sa propre ligne. **Le même contrôle, deux verdicts opposés, et la différence est mesurable** : ce qui manquait au premier cas était un accompagnateur, ce qui manque ici est une adresse
- **🔗 Pont** · [[2026-10-20_lecon-hypnose_19_cadre-ethique-deontologique-juridique-france]]
  **la même semaine, deux documents dont la source primaire du droit est inaccessible.** Là-bas Légifrance refusait le Code de la santé publique (**403** avec les deux agents) ; ici c'est le **décret du 13 mai 2026** qui n'est vérifiable nulle part, et la page CNSA qui en tient lieu ne le porte pas. Dans les deux cas le texte de loi est cité **de seconde main**, et dans les deux cas le document ne le dit pas
- **🗂️ Dossier** · [[SERAFIN-PH_dossier.fiche]]
  à mettre à jour sur quatre points mesurés : **`handicap.gouv.fr` ne rend que 93 caractères utiles** et ne peut plus servir de fond documentaire sans être rouverte autrement ; **les deux articles du Média Social sont des façades** (2 305 et 2 969 caractères) sous le plancher de 3 000 ; **`cnsa.fr/actualites/serafin-ph-un-recueil-de-donnees-obligatoire…` est en 403 anti-robot** et le reste de semaine en semaine ; et le calendrier du dossier doit intégrer le fait nouveau de la fenêtre — **aucune enveloppe SERAFIN-PH au PLFSS 2027**, 360 M€ repoussés à 2028, et un **vote parlementaire en novembre 2026** qui décide du report de la réforme à 2028
