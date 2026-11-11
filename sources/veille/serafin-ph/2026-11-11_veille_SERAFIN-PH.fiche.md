---
type: fiche-document
source: 2026-11-11_veille_SERAFIN-PH.docx
date_creation: 2026-11-11
date_veille: 2026-11-11
serie: serafin-ph
edition: 32
statut: relue
tags:
  - veille/serafin-ph
  - serafin-ph/recueil-ph-2026
  - serafin-ph/plfss-2027
  - serafin-ph/comite-strategique
  - source/cnsa
  - source/atih
  - source/handicap-gouv
  - source/uniopss
  - theme/semaine-creuse
  - theme/plafond-creve-apres-un-avertissement-chiffre
  - theme/livrable-pousse-par-un-run-mort
  - theme/controle-aveugle-au-moment-du-push
  - theme/route-de-lecture-perdue-par-l-edition-suivante
  - theme/motif-sans-notion-de-negation
  - theme/trois-corrections-de-n-1-heritees
---

# 2026-11-11_veille_SERAFIN-PH

Document source : [[2026-11-11_veille_SERAFIN-PH.docx]]

## Résumé

**Le document est sur le dépôt public, et il vient d'un run mort à 101 % de son plafond que personne n'a pu arrêter.** Mesure du log : **4,0529 $ pour 4,00 $**, `error_max_budget_usd`, **49 tours**, 737 997 ms, out 37 316, cache-read 6 355 989, `exit 1`, marque d'échec posée. Et pourtant le commit `abb0305` existe, horodaté **08:09:46**, écrit par l'agent du run lui-même (`Co-Authored-By: Claude Sonnet 4.6`), poussé — alors que `run_job.sh` a conclu à **08:15:29** par `[git] Job en erreur (exit 1) — pas de commit`. Les deux phrases sont vraies : le run a publié **avant** de mourir, et le bloc git de `run_job.sh` n'avait effectivement rien à committer. **Le livrable est public, ㊳ le refuse, et rien ne peut plus l'arrêter.**

**Et ㊳ n'a pas failli : au moment du push, le fait qu'il lit n'existait pas encore.** Mesuré dans les deux sens avec le **vrai `verdict()`** du contrôle, `LOGS` redirigé vers un dossier fabriqué, aucun log vivant touché : avec le log tel qu'il était à 08:09 — c'est-à-dire s'arrêtant à `--- Tentative 1/3 ---` —, le contrôle rend **aucune alerte, le gate passe** ; avec le log complet de 08:15, il rend **REFUS**. `run_job.sh` n'écrit `[diagnostic]` et `[mesure]` qu'au **retour** de `claude -p` : un document poussé en cours de run est donc jugé sur un log qui ne sait encore rien. C'est la cinquième variante de la classe qui revient le plus ici — après « `$SEMENCE` non vide », « les deux photos vides », « un `✅` sur un mur », « un log n'est pas un run » et « un run n'est pas une publication » : **un push n'est pas une fin de run.**

**Le gate imprime `✓ 0 bloquant(s)` sur un document que `controle_attributions.py` refuse en `exit 1`.** Vérifié en lisant le code et non en le supposant : le bloc `--docs` n'exécute que la tranche du contrôle allant jusqu'à `# ── aspiration des pages` et ne compte que `len(orph) + len(snl) + len(a2) + len(a3) + len(a4)`, soit **A + A2 + A3 + A4**. B-FR n'y tourne jamais. Ce n'est pas un bug — c'est la frontière voulue, et sa raison est écrite : le gate porte des pushs, et le 26/10 a montré qu'un hook long **tue la connexion SSH du transport**. Mais le mot « bloquant » y nomme un ensemble **strictement plus petit** que dans le VERDICT du contrôle, et un lecteur du gate prend `✓ 0 bloquant(s)` pour « ce document est propre ». Aujourd'hui le gate sort en **1** avec **0 `✗`** : le refus vient de ㊳ seul.

**Le seul bloquant du contrôle complet est un faux positif, et son mécanisme est celui de la veille, à vingt-quatre heures d'intervalle.** B-FR refuse le span `« Recueil PH 2026 »` comme « ABSENTE DE LA SOURCE NOMMÉE … prêtée à atih.sante.fr » — or la phrase qui le porte est *« Aucune page « Recueil PH 2026 » distincte n'a été trouvée sur atih.sante.fr au 11/11/2026 »*. **La phrase affirme l'absence, et le motif l'accuse de l'affirmer.** B-FR n'a aucune notion de négation, exactement comme le motif ③ de l'Étape 5 bis de neuropsychologie a accusé hier *« il n'appartient pas au chef de service de coter »*. Deux faux positifs en deux jours, même cause — **à ceci près que celui d'hier était en avertissement et que celui-ci est BLOQUANT**.

**Trois corrections de l'édition précédente sont héritées, et c'est la première fois cette semaine que je peux l'écrire.** Mesure dans les deux sens, document contre document : les **360 M€ sur quatre ans**, que la fiche du 04/11 disait manquants, passent de **0 à 2 occurrences** ; *« l'Uniopss + 12 organisations »*, que cette fiche donnait pour une affirmation que la page ne tranche pas, passe de **1 à 0** et devient *« À l'initiative de l'Uniopss, 13 associations »*, la forme même de la page ; le *« J-57 »* faux d'un jour passe de **1 à 0** et aucun décompte ne le remplace. C'est l'exact inverse des **douze faits tombés à zéro** de la veille HAS du 09/11.

**Et l'axe ② de la relecture d'édition accuse précisément la correction.** Il signale `« À l'initiative de l'Uniopss, 13 associations et fédérations nationales »` comme « donnée pour fautive par la fiche de N-1 et reprise ici » — alors que la fiche du 04/11 citait cette formulation comme **ce que la page écrit**, par opposition à la formulation fautive de la note. Le motif apparie « une citation de la fiche voisine d'un mot de faute » et ne distingue pas la dénonciation de son remède, qui vivent dans la même phrase. Même direction d'erreur que le bug de la passe A du 23/10 — *reproduire le libellé corrigé rouvrait le motif qu'on venait de fermer*. Non bloquant, donc le coût est du bruit ; le second signalement est un **titre de section** et relève du même mécanisme.

**La vraie régression de la semaine n'est pas un fait : c'est une ROUTE DE LECTURE, et l'édition précédente l'avait trouvée.** Le recensement par soustraction des jetons distinctifs rend **88 absences** de N-1 dans N, dont la grande majorité est le journal de corrections et l'instrumentation de N-1 — normal. Celle qui compte est **`18/05/2026` / `20260518063812`** : N-1 écrivait noir sur blanc *« le contenu est lu sur un instantané d'archive du 18/05/2026, le dernier du catalogue »*, mesurait **60 227 octets bruts et 5 761 caractères utiles**, et listait les quatre instantanés disponibles (27/03, 16/04, 17/05, 18/05/2026). **N a perdu l'archive** et s'est rabattue sur des extraits de moteur de recherche, en écrivant *« à confirmer sur la page dès qu'elle est lisible »* — **alors qu'une voie lisible existait, mesurée, dans sa propre édition d'il y a sept jours.**

**Mesuré aujourd'hui, l'archive répond, et elle porte au degré ① tout ce que les pages lisibles rendaient ④.** `HTTP 200 · 60 230 octets · 5 761 caractères utiles` — le chiffre exact que N-1 annonçait. Sur elle : `30 mars 2026` **①**, `14e réunion` **①**, `Camille Galliard-Minier` **①**, `automne 2026` **①**, `Comité stratégique` **②**, `ministre chargée de l'Autonomie et des Personnes handicapées` **②**, et `1er janvier 2027` écrit *« au 1 er janvier 2027 »* avec le verbe de la page elle-même : *« a permis de **confirmer** une mise en œuvre opérationnelle de la réforme tarifaire »*. Sur les trois pages lisibles, ces six énoncés sortaient **tous en ④** — `Comité stratégique`, `CSMS` et `14e réunion` n'ont **aucune** occurrence, et seul `à compter de 2027` est ① (page CNSA), pas la date au jour. **Donc la note est juste, et elle l'est sans l'avoir prouvé : le « confirmé » de son tableau de vigilance est le mot de la source primaire qu'elle n'a pas lue.**

**La date du 23 mars 2026 est exacte, et l'établir demande un calendrier.** L'archive ne la porte nulle part : le communiqué est *« Publié le 27/03/2026 »* et dit *« Ce lundi, Camille Galliard-Minier … a présidé le 14ᵉ comité stratégique »*. Le 27/03/2026 est un **vendredi**, le 23/03/2026 un **lundi** : la déduction tient. C'est le genre de fait qu'aucun appariement littéral ne peut valider — `chercher.py` rend ④ sur `23 mars 2026` **sur l'archive comme sur les trois autres pages**, et il a raison.

**Le mur de handicap.gouv.fr est un bouclier Imperva dont le corps contient un jeton ALÉATOIRE, donc le compte de caractères annoncé n'est pas reproductible par construction.** La page rend aujourd'hui **94** caractères : *« Please enable JavaScript to view the page content. Your support ID is: 11628238347645533333. »* — un identifiant de **20 chiffres**. À **19 chiffres**, le corps fait exactement **93** caractères, le nombre que la note annonce. La note n'a donc pas tort : elle a mesuré un autre tirage. ⚠️ **Et ce n'est pas le mur « Identification » de la HAS** — la chaîne en est absente. Conséquence bornée pour le motif `murs_lus` du 05/11 : il compare un compte **avoué** au plancher de 3 000, et sur ce genre de mur le compte avoué dérive d'un caractère à chaque lecture. Sans effet ici (93 et 94 sont tous deux très au-dessous du plancher), à savoir pour un mur qui serait proche du seuil.

**Le motif `murs_lus` est resté muet, et c'est sa borne ① qui fonctionne.** La ligne de la source murée porte `⚠️ JS` et non `✅`, avec sa remarque *« Page rendue en JS (93 car. utiles) — extraits via WebSearch »* : c'est la **forme honnête**, celle que la borne ① du 05/11 refuse d'accuser. `controle_decompte.py` sort en **2** (aucun décompte annoncé) et lit la liste juste : **3 ✅ · 1 ⚠ · 0 ⛔ · total 4**. La réserve « source secondaire » est portée **7 fois** pour la page e-solidarites — rigueur exemplaire —, et **1 fois sur 4** pour le `1er janvier 2027` : elle vit dans le §4 et ne voyage pas jusqu'au tableau de bord, au tableau de vigilance ni à l'agenda. Le tableau de vigilance écrit même *« Le déploiement est confirmé au 1er janvier 2027 »*. **Une réserve posée à la source ne suit pas le fait**, et aucune passe du dépôt ne peut le voir : B-FR exige des guillemets, B-NOM un marqueur d'attribution, D un chiffre dans un paragraphe attribuant — **D rend 0**.

**`controle_noms_propres.py` sort en 0 en n'ayant interrogé qu'UN nom sur la dizaine que la note porte.** Verdict : **1 interrogé · 8 écartés aux bornes · 1 page sur 4 NON LUE**. Le seul nom interrogé est `Camille Galliard-Minier`, trouvé sur e-solidarites — donc par la **source secondaire**, la primaire étant le mur. `CNSA`, `DGCS`, `ATIH`, `ARS`, `SIDOBA`, `RAMSECE-PH`, `Uniopss`, `CSMS` sont tous à **un seul jeton** et tombent sous le `MIN_JETONS = 2`. Le vert porte sur un nom, pas sur la note.

**Le plafond a crevé exactement là où la fiche de l'édition précédente l'avait annoncé, avec le chiffre.** Trajectoire mesurée fichier par fichier : **27 · 39 · 37 · 90 · 95 · 101 %**, soit 0,82 → 1,16 → 1,11 → 2,69 → 3,78 → **4,0529 $**. La fiche du 04/11 écrivait *« il reste 0,22 $ de marge »* et *« c'est le second avertissement de suite sur ce job »*, et rappelait que les deux seuls dépassements du dépôt avaient été précédés d'avertissements à 86 et 93 %. **Le relèvement de 3 à 4 $ du 31/10 a été absorbé en un créneau, et le créneau suivant a crevé le nouveau plafond.** Le prompt n'a pas bougé (**35 312 octets** les deux semaines) : ce qui monte est le `cache-read` **par tour** — 91 266 le 04/11, **129 714** le 11/11, soit +42 % à prompt identique. **Relever n'était pas commandé le 04/11 et ne l'est pas ici** ; ce qui est acquis, c'est que la mesure a précédé l'incident d'une semaine, pour la troisième fois.

### Avocat du diable

La note est **juste sur tout ce que j'ai pu vérifier**, elle a hérité des trois corrections de N-1, et son seul bloquant est un faux positif. Le problème n'est pas le document : c'est que **rien dans le dépôt ne peut dire ce qui est vrai de lui**. `--manques` rend `✓ tracé, exit 0` (mesuré **sans tuyau**), `publication_run.py` se tait parce que `Job en erreur (exit 1)` est l'un de ses quatre états terminaux acceptés, le gate a laissé passer à 08:09 et refuse à 08:15, et `㊳` refuse un document qu'il est trop tard pour retenir. **Quatre outils, et aucun qui sache formuler « ce livrable est sur le distant public et ㊳ le refuse ».** Le cinquième état `✗ PUBLIÉ SANS CONTRÔLE` déjà consigné comme piste couvrirait exactement ce cas ; rien n'est ordonné.

### Requêtes passées

| Requête | Page | Degré |
|---|---|---|
| `Camille Galliard-Minier` | e-solidarites · archive | ① ×2 |
| `A l'initiative de l'Uniopss, 13 associations et fédérations nationales` | e-solidarites | ① (`A` **sans accent** sur la page) |
| `13 associations et fédérations nationales` · `13 organisations` · `Uniopss` | e-solidarites | ① ×3 |
| `360 millions sur quatre ans` · `quatre ans` · `90 millions d'euros` · `2028` · `2027` | e-solidarites | ① ×5 |
| `9 octobre 2026` | e-solidarites | ① |
| `ministre déléguée chargée de l'Autonomie` | e-solidarites | ② |
| `année blanche` · `SIDOBA` · `quarantaine de variables` · `dotation complémentaire` · `six variables` | CNSA | ① ×5 |
| `à compter de 2027` | CNSA | ① |
| `17/12/2025` | CNSA | ① |
| `Système d'information de l'offre de la branche autonomie` | CNSA | ② |
| `RAMSECE-PH` · `3 février` · `13 avril 2025` | ATIH | ① ×3 |
| `14/05/2025` | ATIH | ① |
| `30 mars 2026` · `14e réunion` · `automne 2026` | **archive 18/05/2026** | ① ×3 |
| `Comité stratégique` · `ministre chargée de l'Autonomie et des Personnes handicapées` | **archive 18/05/2026** | ② ×2 |
| `1er janvier 2027` | archive (`au 1 er janvier 2027`) | ① aux blancs près |
| `23 mars 2026` · `23/03/2026` | **les 4 pages + l'archive** | ④ — établi par le calendrier |
| `Comité stratégique` · `CSMS` · `14e réunion` · `1er janvier 2027` | les 3 pages lisibles | **④ ×4** |
| `controle_attributions.py` | le `.docx` | **exit 1** — 1 bloquant B-FR, faux positif |
| `controle_decompte.py` | le `.docx` | exit 2 · liste 3 ✅ · 1 ⚠ · total 4 |
| `controle_edition_precedente.py` | N vs N-1 + fiche | exit 0 · ① propre · ② 2 à relire |
| `controle_noms_propres.py` | le `.docx` | exit 0 · **1 · 8 · 1/4 non lue** |
| `controle_livrable_du_job.py` (㊳) | le `.docx` | **exit 1** — run mort, 0 contrôle tracé |
| ㊳ avec le log de 08:09 | le `.docx` | **aucune alerte** |
| gate `--docs` | le `.docx` | **exit 1**, 0 `✗`, `✓ 0 bloquant(s)` |
| `rattrapage_jobs.sh --manques` | les 7 derniers jours | **exit 0** · `✓ tracé` |

### Ce que STANDARD n'a pas interrogé

1. **Le corps du communiqué sur la page vivante** — mur Imperva, 94 caractères ; seul l'instantané du 18/05/2026 a été lu, et il **précède** la fenêtre de veille de six mois.
2. **La 15e réunion du Comité stratégique** — la note la dit « date non communiquée » ; aucune page ne l'infirme ni ne la confirme, et aucune requête ne peut prouver une absence.
3. **Le courrier des 13 organisations lui-même** — la note le dit explicitement non consulté ; je ne l'ai pas cherché non plus.
4. **L'existence d'une page « Recueil PH 2026 » sur atih.sante.fr** — la note affirme l'absence au 11/11/2026 ; je n'ai pas balayé le site, donc cette absence reste **son** affirmation.
5. **Les débats PLFSS 2027 postérieurs au 9/10/2026** — la fenêtre du 4 au 11/11 est déclarée creuse sur les trois sources institutionnelles ; aucun flux ni aucun site d'actualité parlementaire n'a été interrogé.
6. **Les trois autres instantanés de l'archive** (27/03, 16/04, 17/05/2026) — un seul a été lu, celui que N-1 nommait.
7. **Le `.docx` en rendu Word** — intégrité XML vérifiée (**9 602 caractères**, 123 ¶ tous porteurs de texte, 8 hyperliens pour 4 adresses, **4 tableaux** pour un plancher de 3, marge 115, 0 dimension négative), apparence non ouverte.

## Notes liées

- **⬅️ Précédente** · [[2026-11-04_veille_SERAFIN-PH.fiche]] — celle qui a lu la page murée sur l'archive, nommé les trois défauts hérités cette semaine, et annoncé le dépassement avec ses 0,22 $ de marge
- **➡️ Suivante** · édition du **mercredi 18/11/2026 à 8h03** (le document n'existe pas encore, donc pas de lien)
- **🔗 Pont** · [[2026-11-08_veille_imac.fiche]] — l'autre run à **101 %** qui a publié son livrable, trois jours plus tôt, et dont la relance n'a pas été ordonnée
- **🔗 Pont** · [[2026-11-09_veille_has-actualite.fiche]] — douze faits de N-1 tombés à zéro ; ici trois corrections héritées et **une route de lecture perdue**
- **🔗 Pont** · [[2026-11-10_lecon-neuropsychologie_01_fondations-quest-ce-que-la-neuropsychologie]] — le faux positif du motif ③ sur « coter », même absence de notion de négation que le B-FR d'aujourd'hui, mais en avertissement
- **🗂️ Dossier** · [[SERAFIN-PH_dossier.fiche]]
