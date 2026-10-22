---
type: fiche-document
source: 2026-10-15_lecon-stoicisme_19_critiques-stoicisme-insensibilite-quietisme-objections.docx
date_creation: 2026-10-21
date_lecon: 2026-10-15
parcours: stoicisme
numero: 19
statut: parcours-actif
tags:
  - parcours/stoicisme
  - registre/perso
  - concept/apatheia
  - concept/quietisme
  - concept/argument-paresseux
  - concept/objections-feministes
  - source/iep
  - source/sep
  - source/modern-stoicism
  - source/stoa-gallica
  - theme/dix-citations-aucune-inventee
  - theme/analyse-pretee-a-qui-la-cite
  - theme/termes-grecs-sans-page
  - theme/calque-de-traduction
  - theme/apostrophe-typographique-contre-droite
  - theme/chercher-apparie-des-sous-chaines
  - theme/fiche-ecrite-six-jours-apres
---

# 2026-10-15_lecon-stoicisme_19_critiques-stoicisme-insensibilite-quietisme-objections

Document source : [[2026-10-15_lecon-stoicisme_19_critiques-stoicisme-insensibilite-quietisme-objections.docx]]

## Résumé

**Dix citations vérifiées, aucune inventée — et c'est le meilleur résultat de ce parcours depuis que je le fiche.** Les quatre citations anglaises entre guillemets sont sur la page qui leur est attribuée : *« it is grossly incorrect to say that the Stoics aimed at a passionless life, or at the suppression of emotions »* est **① LITTÉRAL** sur l'IEP de Pigliucci ; *« a fundamental and uncompromising commitment to social good »* **①** sur le symposium Modern Stoicism, bien prêtée à Gyulay ; *« Stoic misogyny »* et *« uneven track record »* **①** sur l'entretien du Daily Stoic. Les trois formules des critiques religieuses le sont aussi, sur la recension de Normand Doiron : *« la folie ridicule du sage »* **①**, *« indolence sans espérance »* **①**, *« l'orgueil d'Épictète »* **②** (apostrophe typographique). Le *« co-fated »* du co-fatalisme est **①** sur la Stanford Encyclopedia. Et le reproche factuel sur Épictète est exact au sens près : la page écrit *« Epictetus, for all of his forward-thinking, dismisses Epicureanism by saying it's not even fit for women »*, la leçon rend « Épictète raille l'épicurisme comme inadapté aux femmes ». **Les sept URL répondent 200**, comme le récapitulatif l'annonçait, et **les sept servent dans le corps** — ce qui n'était pas le cas de la leçon 18 du parcours hypnose fichée le même jour.

**Le défaut central est une analyse prêtée à celui qui la cite.** La leçon écrit : *« Alex Richardson, dans un article intitulé "The Stoic's Lacuna" publié dans Philosophy Now, identifie une faille structurelle dans la doctrine : le glissement de la polis vers le domaine privé, accéléré par la décadence des cités grecques. »* ⚠️ **La page de Richardson attribue explicitement cette analyse à quelqu'un d'autre** : *« In this case I follow the analysis of Ellen Meiksins Wood in Citizens to Lords (2008) : "as polis gave way to empire, the main arena of philosophical reflection shifted. The sphere of civic action and deliberation receded, bringing into focus the pr[ivate]…" »*. Richardson **suit** une analyse, il ne l'**identifie** pas — et la leçon fait disparaître Ellen Meiksins Wood, son livre et sa date. Le fond est juste, la paternité ne l'est pas. C'est la même famille que l'affirmation prêtée à Robertson relevée dans la fiche du 08/10 : **une page lue, une attribution déplacée d'un cran.**

**Et le « recède » qui m'avait fait tiquer n'est pas une faute de frappe, c'est un calque — la preuve est dans la phrase source.** La leçon écrit *« L'espace de la délibération collective recède »* ; la page écrit *« The sphere of civic action and deliberation **receded** »*. Le verbe français n'existe pas dans cet emploi — on recule, on régresse, on se retire — et sa forme suit l'anglais mot pour mot. Un calque est plus instructif qu'une coquille : il montre que la phrase a été traduite au fil du texte, et il signale précisément où regarder pour vérifier.

**Quatre termes grecs ne sont sur aucune des sept pages, et c'est la seule partie de la triple distinction qui ne soit pas sourcée.** La distinction elle-même est bien chez Goarzin : **« propatheiai » et « eupatheiai » sont ① LITTÉRAL** sur Stoa Gallica, et le « kathêkon » du devoir est **②** sur l'IEP. ⚠️ Mais les trois noms que la leçon donne aux émotions positives — *« joie sereine (chara), circonspection (eulabeia), volonté (boulêsis) »* — et le nom du destin — *« (heimarmenê) »* — comptent **zéro occurrence sur les sept pages**. Ce sont de vrais termes de la doxographie stoïcienne, pas des inventions ; mais la leçon les présente dans une phrase qui crédite Goarzin de « présenter avec précision » la distinction, et ces quatre mots-là ne viennent pas de lui. 🔴 **Et c'est ici que j'ai failli écrire le contraire** : `chercher.py` m'a d'abord rendu **① LITTÉRAL** pour « chara » sur la page du Daily Stoic. Vérification en fenêtre : la page écrit *« strengthening the **chara**cter »* et *« strengthening of her **chara**cter »*. **L'outil appariait une sous-chaîne.**

**🔴 ET C'EST UNE CÉCITÉ MESURÉE DE `chercher.py`, LA PREMIÈRE SUR CE POINT : son degré ① n'a AUCUNE frontière de mot.** Épreuve directe sur la même page : **« aract » → ① LITTÉRAL**, **« haracte » → ① LITTÉRAL**, **« trengthenin » → ① LITTÉRAL**. Trois fragments qui ne sont pas des mots sortent au degré le plus fort. Conséquence : **toute requête plus courte qu'un mot peut être satisfaite à l'intérieur d'un mot plus long**, et un « ① » sur une requête de cinq lettres ne prouve rien. ⚠️ Le dépôt a déjà une règle voisine — *« un jeton se cherche ponctuation CONSERVÉE »*, parce qu'une clé qui écrase la ponctuation apparie « 1 338 » à « 1 338,23 » — mais rien n'était écrit sur les frontières de mot, et `present()` de `controle_edition_precedente.py`, lui, les pose (`(?<![0-9A-Za-zÀ-ÿ.,])`). 📌 **Piste bornée** : donner à `chercher.py` les mêmes lookarounds pour les requêtes d'un seul mot, en laissant les requêtes à plusieurs mots inchangées — à mesurer sur ses 21 auto-tests avant de toucher quoi que ce soit, puisque c'est l'outil par lequel tout le dépôt vérifie ses citations.

**Deux citations ne sortent qu'au degré ② et la raison est l'apostrophe, pas le mot.** Les deux phrases de Brittany Polat — *« we should only accept those things we can't change »* et *« If it's within our power to change or influence something for the better, we should do it »* — sont **② GRAPHIE**, et la fenêtre montre pourquoi : la page écrit `can’t` et `If it’s` avec l'apostrophe typographique, la leçon avec l'apostrophe droite. **Le texte est fidèle mot pour mot** ; seule la ponctuation a été normalisée. ⚠️ C'est la même famille que ㊱, le motif des guillemets courbes posé le 15/10 : droit contre courbe, et un degré perdu pour rien. Un troisième cas mérite d'être dit : *« comme des hommes »*, prêté à Sénèque entre guillemets français, est la **traduction** du *« like men »* de la page — exact, mais la leçon ne déclare pas qu'elle traduit.

**Les contrôles, et une famille de faux positifs qui appartient au format de la leçon.** Rejoués **verbatim sous `env -i`** : l'**étape 5 bis du prompt, sept motifs → « OK — aucun des sept motifs »** ; l'**intégrité → « OK — XML conforme, 7 lien(s), 116 paragraphe(s) de texte (marge 109) »**. `controle_attributions` : **exit 0, 0 bloquant**, passe **B à 3 citations anglaises, toutes OK et toutes appariées sur leur page nommée**. ⚠️ **Mais B n'en a vu que trois sur quatre** : *« Stoic misogyny »* (deux mots) et *« uneven track record »* (trois) passent sous son plancher de **six mots** — le même angle mort que celui mesuré le 18/10 sur la veille iMac, où la seule citation fautive de la note était précisément l'une de celles qu'aucune passe ne regardait. Ici les deux sont justes, et c'est moi qui l'ai vérifié, pas la machine. Enfin **B-FR relève 14 citations françaises et en met 7 « à relire »** : les voir de près suffit à les classer — *« De toute façon, ça ne changera rien »*, *« J'ai eu un mouvement involontaire de… »*, *« J'ai laissé une impulsion déraisonnable s'installer… »* sont les **phrases que la leçon propose au lecteur d'écrire dans ses exercices**. Ce ne sont pas des attributions, ce sont des consignes entre guillemets. Le contrôle a un garde pour cela — la « parole d'une vignette » — et il ne mord pas sur ce format d'exercice à la première personne.

**Mesures du job. 2,0372 $ pour un plafond de 3,00 $ — 68 %**, **29 tours**, 11 min 57 s, 35 563 tokens en sortie, une seule tentative, `exit 0`, prompt à **55 458 octets**. C'était alors le job le plus tendu du dépôt après ai-act, et il l'est resté : au 20/10, `stoicisme-lecon` est **le plus tendu des neuf** avec 0,96 $ de marge. Document de **18 Ko** pour **15 348 caractères**, 116 paragraphes porteurs, 7 liens, 1 tableau récapitulatif des six familles d'objections. ⚠️ **Et cette fiche est écrite six jours après la leçon**, le 21/10 : les sept pages ont été rouvertes ce jour-là, pas le 15. Rien n'a bougé — les sept répondent 200 et portent toujours leurs citations — mais une fiche tardive ne mesure pas l'état du web au moment de la rédaction, et pour un article de presse en ligne comme celui de Philosophy Now, ce décalage pourrait un jour compter.

**La continuité est juste dans les deux sens, et la leçon tient sa place dans la progression.** Elle ouvre sur *« la leçon 18 avait exploré la filiation entre stoïcisme et thérapies cognitives (TCC, REBT) »* — ce qui est bien le sujet de la 18 — et annonce *« Avant de clore le parcours avec le bilan (leçon 20) »*. Elle se présente en **19 / 20** et ferme sur *« Leçon 20 / 20 — BILAN »* avec une formule qui situe exactement l'enjeu : *« Après 19 leçons, la question n'est plus "qu'est-ce que le stoïcisme ?" mais "qu'est-ce que je retiens, et comment ?" »*. 🟢 Et sur le fond, la leçon fait ce qu'elle annonce : elle ne défend pas le stoïcisme contre ses critiques, elle **nomme ce qui résiste** — le résidu déterministe de l'argument paresseux, la tension entre autosuffisance et dépendance, et le bilan historique inégal sur la condition des femmes, qu'elle qualifie de *« point de tension non résolu »*.

### Requêtes passées

Sept pages aspirées sur disque (`aspirer.py`), **aucune n'est entrée en contexte** ; appariement par `chercher.py`, degré ① exigé pour tout ce qui est entre guillemets ; contextes lus en fenêtres bornées par `lire_page.py`.

| Requête | Verdict |
|---|---|
| `it is grossly incorrect… suppression of emotions` | **① LITTÉRAL** iep.utm.edu |
| `a fundamental and uncompromising commitment to social good` | **①** modernstoicism.com |
| `we should only accept those things we can't change` · `If it's within our power…` | **②** — la page écrit `can’t` / `it’s`, apostrophe typographique ; mot pour mot identique |
| `Stoic misogyny` · `uneven track record` | **①** dailystoic.com — et toutes deux **sous le plancher de six mots** de la passe B |
| `co-fated` | **①** plato.stanford.edu |
| `la folie ridicule du sage` · `indolence sans espérance` | **①** laviedesidees.fr |
| `l'orgueil d'Épictète` | **②** laviedesidees.fr (apostrophe) |
| `Lagrée` · `néostoïcisme` | **①** laviedesidees.fr — la recension et son objet sont exacts |
| `propatheiai` · `eupatheiai` | **①** stoagallica.fr · `kathêkon` **②** iep |
| `chara` · `eulabeia` · `boulêsis` · `heimarmenê` | **④ ABSENTS des sept pages** — le « ① » initial de `chara` venait de « cha**racter** » |
| `aract` · `haracte` · `trengthenin` | **① LITTÉRAL** — **`chercher.py` apparie des sous-chaînes** |
| `Epictetus` · `Seneca` · `like men` | **①** dailystoic — le reproche sur Épictète est exact au sens près |
| `polis` · `private` · `decline` | **①** philosophynow — et la fenêtre révèle **Ellen Meiksins Wood**, absente de la leçon |
| `neoliberal` | **①** philosophynow — la récupération néolibérale est bien de Richardson |

**Ce que « standard » n'a pas interrogé, et il faut le dire** : le livre d'Ellen Meiksins Wood, *Citizens to Lords* (2008), n'a pas été ouvert — seule la citation qu'en fait Richardson a été lue ; l'ouvrage de Jacqueline Lagrée non plus, seule la recension de Doiron ; les trois formules de Pascal, Malebranche et Leibniz n'ont donc été vérifiées **que chez leur recenseur**, pas dans les textes ; et les quatre termes grecs manquants n'ont pas été cherchés hors des sept pages de la leçon, donc je ne dis pas qu'ils sont introuvables — je dis qu'ils ne sont pas là où la leçon les fait venir.

## Notes liées

- **⬅️ Précédente** · [[2026-10-08_lecon-stoicisme_18_stoicisme-therapies-cognitives]]
  **le même défaut d'attribution, déplacé d'un cran et d'un auteur.** Là-bas une affirmation prêtée à Robertson reposait sur son nuage de tags ; ici une analyse prêtée à Richardson est celle d'Ellen Meiksins Wood, que sa page nomme explicitement. Dans les deux cas la page a bien été lue et le fond est juste — **c'est la paternité qui glisse**. En sens inverse, le lien de contenu que la 19 écrit sur la filiation TCC/REBT correspond exactement au sujet de la 18
- **🔗 Pont** · [[2026-10-20_lecon-hypnose_19_cadre-ethique-deontologique-juridique-france]]
  **deux leçons n°19 fichées le même jour, et l'écart sur les sources est net.** Les deux sont des leçons « de cadre » avant un bilan ; celle-ci mobilise ses **sept** sources dans le corps, l'autre en laisse **une sur cinq** inutilisée. Celle-ci n'a aucune citation inventée ; l'autre ajoute « (master ou doctorat) » à une phrase sourcée qui s'arrêtait avant. Et là-bas la source primaire — Légifrance — **refusait l'accès (403 avec les deux agents)** ; ici les sept pages répondent 200
- **🔗 Pont** · [[2026-10-18_veille_imac.fiche]]
  **le plancher de six mots de la passe B, mesuré deux fois dans le même sens.** Là-bas les six citations anglaises de la note faisaient deux à cinq mots et **B n'en a examiné aucune** — or c'est précisément la fautive qui échappait. Ici B en examine **trois sur quatre** : « Stoic misogyny » et « uneven track record » passent sous le plancher. Les deux sont justes, mais c'est la vérification à la main qui le dit, pas le contrôle
- **🗂️ Dossier** · [[2026-10-01_lecon-stoicisme_17_stoicisme-christianisme-emprunts-divergences-posterite]]
  **ses critiques religieuses sont le revers exact de ce que la 17 avait étudié par ses emprunts.** La leçon 17 travaillait les emprunts et divergences entre stoïcisme et christianisme ; la 19 en donne la face polémique, et avec ses noms — Pascal et *« l'orgueil d'Épictète »*, Malebranche et *« la folie ridicule du sage »*, Leibniz et *« l'indolence sans espérance »*. Le reproche central est le même objet vu de l'autre côté : l'autosuffisance de la vertu contre la grâce. 📌 À reprendre au bilan (leçon 20), dans l'ordre d'importance : la **triple distinction** pathê / propatheiai / eupatheiai, qui est le vocabulaire manquant de toutes les leçons sur les émotions ; la **récupération néolibérale** nommée ici, qui est la limite contemporaine du parcours ; et le **bilan historique inégal** sur la condition des femmes, que la leçon qualifie de « point de tension non résolu » — un bilan qui l'escamoterait trahirait celle-ci
