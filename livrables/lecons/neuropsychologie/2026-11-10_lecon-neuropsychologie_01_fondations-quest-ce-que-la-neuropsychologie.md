---
type: fiche-document
source: 2026-11-10_lecon-neuropsychologie_01_fondations-quest-ce-que-la-neuropsychologie.docx
date_creation: 2026-11-10
date_lecon: 2026-11-10
parcours: neuropsychologie
numero: 1
statut: parcours-actif
tags:
  - parcours/neuropsychologie
  - neuropsychologie/fondations
  - neuropsychologie/broca
  - neuropsychologie/luria
  - theme/premier-creneau-d-un-parcours-neuf
  - theme/plafond-a-96-pourcent-au-premier-creneau
  - theme/faux-positif-du-motif-3-en-avertissement
  - theme/interdit-respecte-qui-rend-un-motif-inerte
  - theme/fait-precis-sans-page
  - theme/guillemets-sur-une-synthese-declaree-non-citation
  - theme/lateralite-ajoutee-sans-page
  - theme/premier-verdict-propre-des-noms-propres
---

# 2026-11-10_lecon-neuropsychologie_01_fondations-quest-ce-que-la-neuropsychologie

Document source : [[2026-11-10_lecon-neuropsychologie_01_fondations-quest-ce-que-la-neuropsychologie.docx]]

## Résumé

**Le premier créneau d'un parcours neuf a consommé 96 % de son plafond, et le 4,00 $ posé le 07/11 n'a tenu que de 0,1404 $.** Mesure du log : **3,8596 $ pour 4,00 $**, **67 tours**, 556 252 ms, out 26 347, cache-read 8 957 972, cache-write 150 902, `exit 0` en **1 tentative**, `stop_reason=end_turn`. À 0,0576 $ par tour, la marge restante valait **2,4 tours** : deux vérifications de plus et le créneau mourait en `stop_reason=tool_use`, c'est-à-dire exactement comme `astrologie-karmique` le 08/10 (3,0218 $ / 3,00 $) et `ai-act` le 16/10 (3,2339 $ / 3,00 $) — **après avoir écrit un livrable complet qu'aucun contrôle n'a vu**. Le chiffre est 28 % au-dessus du maximum des 16 derniers runs de leçon, qui était précisément ce 3,0218 $ : les quatre mesures qui avaient fixé le plafond à 4,00 $ (le 50 % de `psychopathologie`, le maximum de 3,0218 $, le bloc des noms propres qui prescrit un tour à ~3,3 %, et l'absence de leçon N-1) ont donné le bon ordre de grandeur **et pas la bonne marge**. Et la prédiction « les deux premiers créneaux explorent » est vérifiée dans le mauvais sens : c'est le créneau n°1 qui a exploré, et il reste onze leçons.

**Les trois interdits absolus du parcours sont respectés, et ce n'est pas une impression de lecture : c'est mécanique.** Zéro posologie dans le corps (le motif `(\d+)\s?(mg|µg|mcg|g|ml|UI)` ne rend rien), zéro occurrence des **15 noms de test** de la liste `TESTS` du prompt (`MMSE`, `MoCA`, `BREF`, `FAB`, `WAIS`, `WISC`, `NPI-ES`, `CMAI`, `Vineland`, `GRECO`, `RL/RI`, `TMT`, `Stroop`, `Rey`, `Wechsler`), zéro molécule, et le bilan de l'exercice 3 est **déclaré fictif** avec un « M. F. » qui ne porte aucun verbe de diagnostic dans sa fenêtre de 80 caractères. La leçon va plus loin que l'interdit : elle écrit en propre que *« il n'appartient pas au chef de service de coter ou d'interpréter le bilan, mais de poser ces questions au psychologue »* — elle énonce la limite de rôle au lieu de la subir.

**Et c'est cette phrase-là que l'Étape 5 bis a accusée : le motif ③ a rendu son premier faux positif au premier créneau, sur le mot « coter » placé dans une clause prohibitive.** Le motif s'écrit `re.finditer(r"\b(cotation|coter|passation|administrer le test|barème|étalonnage|note brute|note standard)\b", CORPS, re.I)` — un `finditer` nu, sans aucune notion de portée ni de négation. Il ne distingue pas *« voici comment coter »* de *« il ne t'appartient pas de coter »*, c'est-à-dire qu'il **accuse la phrase même qui applique l'interdit qu'il garde**. C'est le défaut nommé dans `CLAUDE.md` le 07/11 pour les motifs ① et ③ — *« un contrôle et la consigne qu'il garde doivent nommer la même chose »* — reproduit par le motif voisin. Conséquence directe sur le **critère de promotion** écrit dans le prompt : après la leçon n°3, seuls les motifs à **zéro faux positif** passent en bloquant ; **③ est déjà disqualifié**, et le resserrer demandera de borner la clause, pas de bouger le seuil. Le choix du 07/11 de laisser l'Étape 5 bis en **avertissement** est donc payé : en bloquant, ce créneau à 96 % du plafond aurait été refusé pour une phrase exemplaire.

**Le motif ② est resté totalement inerte, et sa cause est que l'interdit est respecté — un motif que la conformité éteint est un motif qui ne garde rien.** Il est gardé par `if LUES:` et ne confronte un chiffre à une page que s'il trouve un nom de test : il n'y en a aucun, donc il imprime `⛔ … NON APPLIQUÉ`. C'est la borne que le 07/11 avait posée à bon droit (une mention absente est indiscernable d'une mention non lue), mais elle produit ici un effet non prévu : **le seul motif capable de confronter un chiffre aux pages est éteint par le respect du périmètre**, et c'est lui qui aurait pu attraper le défaut ci-dessous si les dates avaient été dans sa portée.

**Trois faits précis de la leçon ne figurent sur aucune des cinq pages lues : « 1861 », « Bicêtre » et « Tan ».** Zéro occurrence chacun sur les 5 pages aspirées (Wikipédia FR 32 839 car., Wikipédia EN 54 895, SEP 146 920, EHC Vaud 14 842, SFNP), vérifié au degré ① par `chercher.py`. Le nom du patient, `Leborgne`, n'existe qu'**en titre d'une note bibliographique** de la page EN — donc pas comme contenu attribuable. Et **aucun contrôle du dépôt ne pouvait les voir** : `« Tan »` est entre guillemets mais fait **3 lettres et 1 mot**, sous les deux seuils de B-FR (9 lettres, ou 4 mots sans source nommée) ; `1861` et `Bicêtre` ne sont pas entre guillemets, donc hors de B et B-FR ; `Bicêtre` est un nom propre d'un seul jeton, donc sous le `MIN_JETONS = 2` de `controle_noms_propres.py` ; et la passe D ne cherche un chiffre que dans les paragraphes liés. **Les trois faits sont exacts dans la littérature — ce qui manque n'est pas la véracité, c'est la page.**

**Un seul énoncé est entre guillemets alors que la leçon elle-même le déclare non cité, et la même leçon fait correctement le contraire une page plus loin.** Elle écrit *« un pilier de la recherche en aphasie jusqu'à aujourd'hui » (synthèse, non citation directe)* en attribuant à la Stanford Encyclopedia of Philosophy section 5 — les guillemets et la dénégation dans le même paragraphe. Et le sujet de la SEP n'est pas la méthode de Broca mais *« More recent and more careful lesion studies »* : la nuance perdue n'est pas décorative, elle déplace l'éloge d'un siècle. Par contraste, la synthèse sur l'IRM fonctionnelle rend fidèlement le *« indicating regions where further data and analysis are warranted »* de la même source **sans guillemets** et en se disant synthèse : le bon geste existe dans le document, deux paragraphes plus loin.

**Une latéralité a été ajoutée sans page : le « lobe temporal gauche » de Wernicke.** `left temporal` et `temporal gauche` rendent **0 occurrence sur les cinq pages**. Le fait est juste, et le motif ④ de l'Étape 5 bis ne peut structurellement pas le voir : il est gardé par un marqueur d'attribution (`selon|d'après|montre que|établit que|objective|met en évidence`), et la phrase n'en porte aucun — *« identifiant une zone lésée dans le lobe temporal gauche »*. **Une affirmation anatomique non attribuée échappe au motif anatomique par conception**, ce qui est l'angle mort jumeau de celui de ⑦ dans les contrôles 5 bis d'astrologie (« une ligne purement nominative est hors de portée »).

**La page française porte la réfutation de Broca par Pierre Marie, et la colonne « Limite reconnue » de la leçon ne la rapporte pas.** Ce n'est pas une erreur, c'est une omission : la leçon dit les limites de la méthode anatomo-clinique en général, pas qu'un auteur a contesté le cas fondateur en propre. Sur un parcours dont l'objet déclaré est *lire un bilan et le traduire en objectifs*, la controverse historique est secondaire — mais c'est exactement la classe de perte que les douze faits tombés à zéro de la veille HAS du 09/11 ont rendue visible la veille : **ce qu'une source établit et que la note ne reprend pas n'est vu par aucun contrôle.**

**Et `controle_noms_propres.py` rend ici son premier verdict entièrement propre depuis sa création le 31/10 : 4 interrogés · 0 non retrouvés · 0 page non lue.** Comparé au 09/11, où il rendait un nom non retrouvé et une page sous le plancher, c'est le premier document du dépôt où ses trois compteurs sont au vert ensemble. Ce que ce vert ne couvre pas est mesuré, pas supposé : `MIN_JETONS = 2` exclut **`Gall` et `Bouillaud`**, cités en un seul jeton, donc les deux noms les plus anciens de la leçon n'ont **jamais été interrogés** — le verdict propre porte sur 4 noms, pas sur tous. `controle_attributions.py` rend **0 bloquant**, après que le run a corrigé lui-même un bloquant ㉖ en retirant les guillemets de « systèmes fonctionnels » et en précisant que c'est la traduction de *functional systems* : le job s'est corrigé avant d'écrire, ce que `serafin-ph-veille` ne sait pas faire faute d'appeler ce contrôle.

**Tout ce que la leçon source tient au degré ①, et c'est la majorité du document.** Luria « father of modern neuropsychology » sur la page EN, `functional systems` traduit fidèlement avec le bon nom de section, *Higher Cortical Functions in Man* et **1962** tous deux ① sur la même page, l'aire de Broca dans le lobe frontal gauche, le terme « aphasique ». Le gate `--docs` sort en **0** avec **0 `✗`**, l'intégrité `.docx` est conforme (XML valide, 5 liens, 118 paragraphes porteurs de texte, **marge 113** pour un plancher de 10, 0 tableau — ce parcours n'en prescrit aucun), les 5 liens testés sont les 5 retenus, et `audit_vault.py` rend ses 9 contrôles au vert, la seule ligne `○` étant **cette fiche** restée à renseigner.

**Deux faits d'infrastructure méritent d'être consignés, parce qu'ils se sont bien passés et qu'on ne l'aurait pas su.** L'autoremisage de `run_job.sh` a fonctionné pour la première fois sur un arbre sale de huit chemins : `Autoremisage créé : 8af417b`, livrable committé puis poussé, `Autoremisage appliqué`, et `git stash list` **vide** après coup — rien perdu. Et **le job est publié alors que sa propre définition ne l'est pas** : `jobs_config.json` porte **5 jobs à HEAD contre 6 dans l'arbre**, `neuropsychologie-lecon` est à **0 occurrence** dans la version publique. Il est planifié dans launchd, il produit, il pousse — et le dépôt distant ne sait pas qu'il existe. C'est sans conséquence sur la production (launchd et `run_job.sh` lisent le disque) et ce serait une perte sèche en cas de restauration depuis le distant.

**Volume : 12 534 caractères, soit 48 % de plus que la leçon 01 de `psychopathologie` (8 470) et 37 % de moins que sa leçon 03 (19 828), où ce parcours jumeau avait trouvé son format.** La trajectoire du seul autre parcours clinique du dépôt suggère que le volume monte encore avec le rodage — or le plafond est déjà à 96 %.

### Avocat du diable

Le faux positif du motif ③ est le défaut **visible**, et il est bénin puisque le contrôle est en avertissement. Le vrai sujet est le plafond : à **96 % au premier créneau**, la leçon 02 part sans marge, et les deux leviers connus tirent dans le mauvais sens — un parcours se rode en s'allongeant, et le bloc des noms propres prescrit au moins un tour supplémentaire quand un nom n'est pas retrouvé, ce qui n'est pas arrivé cette fois. Relever à 5,00 $ coûterait 1,00 $ de cumul hebdomadaire (26 → 27 $) et serait la **troisième fois** qu'un plafond est relevé *avant* le dépassement (`rbpp` le 19/10, `serafin` le 31/10) ; ne pas le relever, c'est accepter de perdre un créneau sur douze dans un parcours qui n'a pas de leçon de rattrapage. Rien de tout cela n'est ordonné.

### Requêtes passées

| Requête | Cible | Degré |
|---|---|---|
| `father of modern neuropsychology` | Wikipédia EN Neuropsychology | ① |
| `functional systems` | Wikipédia EN Neuropsychology | ① |
| `Higher Cortical Functions in Man` | Wikipédia EN Neuropsychology | ① |
| `1962` | Wikipédia EN Neuropsychology | ① |
| `Luria` | 5 pages | ① |
| `Louria` | 5 pages | ① (FR) |
| `aire de Broca` | Wikipédia FR Neuropsychologie | ① |
| `lobe frontal gauche` | Wikipédia FR Neuropsychologie | ① |
| `aphasique` | Wikipédia FR Neuropsychologie | ① |
| `indicating regions where further data and analysis are warranted` | SEP Philosophy of Neuroscience | ① |
| `More recent and more careful lesion studies` | SEP Philosophy of Neuroscience | ① |
| `pilier de la recherche en aphasie` | 5 pages | ④ (synthèse, guillemets à retirer) |
| `1861` | 5 pages | ④ **0 occurrence** |
| `Bicêtre` | 5 pages | ④ **0 occurrence** |
| `Tan` | 5 pages | ④ **0 occurrence** |
| `Leborgne` | Wikipédia EN | ① mais **en titre de note bibliographique seulement** |
| `left temporal` | 5 pages | ④ **0 occurrence** |
| `temporal gauche` | 5 pages | ④ **0 occurrence** |
| `tomographie par émission de positons` | 5 pages | ④ **0 occurrence** |
| `Pierre Marie` | Wikipédia FR | ① (réfutation présente, non reprise) |
| 15 noms de `TESTS` | corps du `.docx` | **0 occurrence** (interdit respecté) |
| posologies `mg|µg|mcg|g|ml|UI` | corps du `.docx` | **0 occurrence** |
| `coter` | corps du `.docx` | 1 occurrence, **clause prohibitive** |
| `controle_attributions.py` | le `.docx` | **0 bloquant** |
| `controle_noms_propres.py` | le `.docx` | **4 · 0 · 0** |
| gate `--docs` | le `.docx` | **exit 0, 0 `✗`** |
| `audit_vault.py` | le coffre | **9/9** |

### Ce que STANDARD n'a pas interrogé

1. **`Gall` et `Bouillaud`** — un seul jeton chacun, sous `MIN_JETONS = 2` : jamais interrogés, et le verdict « 0 non retrouvé » ne les couvre pas.
2. **Les dates autres que 1861 et 1962** — la passe D ne cherche un chiffre que dans un paragraphe lié, et le motif ② de l'Étape 5 bis est inerte faute de nom de test.
3. **Le contenu des 5 pages hors des 20 requêtes ci-dessus** — l'appariement exact ne trouve que ce qu'on lui demande ; aucune page n'est entrée en contexte.
4. **La page SFNP** — testée à 200 et retenue, mais aucune citation ne lui est attribuée, donc rien n'y a été cherché.
5. **La justesse pédagogique des trois exercices** — la fiche vérifie les faits et les interdits, pas la progression didactique.
6. **Le périmètre des 11 leçons à venir** — le prompt annonce la leçon 02 (cartographie des fonctions cognitives) ; rien ne vérifie que le découpage en 12 couvre l'objectif déclaré.
7. **Le `.docx` en rendu Word** — conformité XML vérifiée, apparence non ouverte.

## Notes liées

- **➡️ Suivante** · leçon 02 — Cartographie des fonctions cognitives, créneau du **mardi 17/11/2026 à 8h03** (le document n'existe pas encore, donc pas de lien)
- **🔗 Pont** · [[2026-06-13_lecon-psychopathologie_01_intro-modeles-psychopatho]] — la leçon 01 du seul autre parcours **clinique** du dépôt, celui dont le 50 % de 4,00 $ a servi à fixer ce plafond
- **🔗 Pont** · [[2026-06-29_lecon-psychopathologie_03_semiologie-psychiatrique]] — où ce parcours jumeau a trouvé son format, à 19 828 caractères
- **🔗 Pont** · [[2026-11-09_veille_has-actualite.fiche]] — où `controle_noms_propres.py` rendait un faux positif et une page non lue ; ici son premier verdict entièrement propre
