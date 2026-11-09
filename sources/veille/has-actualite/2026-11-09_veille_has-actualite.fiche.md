---
type: fiche-document
source: 2026-11-09_veille_has-actualite.docx
date_creation: 2026-11-09
date_veille: 2026-11-09
veille: has-actualite
statut: veille-active
tags:
  - veille/has-actualite
  - registre/pro
  - concept/csms
  - concept/appels-a-candidatures
  - concept/calendrier-has
  - source/has
  - source/flux-rss
  - theme/edition-qui-sait-moins-que-la-precedente
  - theme/correction-defaite-par-l-edition-suivante
  - theme/flux-rss-effondre-donne-pour-lu
  - theme/plancher-de-facade-sans-aveu-du-compte
  - theme/nom-d-instance-reecrit-par-la-note
  - theme/heritage-sans-marqueur-hors-des-trois-formes-gardees
  - theme/creneau-accuse-anterieur-a-la-naissance-du-job
---

# 2026-11-09_veille_has-actualite

Document source : [[2026-11-09_veille_has-actualite.docx]]

## Résumé

**Tout ce que cette note affirme sur la foi d'une page est exact, au degré ① : son unique défaut est une SOUSTRACTION, et aucun contrôle du dépôt ne regarde les soustractions.** Les six sources sont lues et répondent 200, les treize dates interrogées s'apparient littéralement, les deux titres de session de l'Université d'automne sont au mot, le courriel de candidature est au caractère, la semaine creuse est prouvée sur le flux. Les dix contrôles sortent en 0, le gate `--docs` accepte le document, `audit_vault.py` rend 9/9, et le run est allé au bout à **56 % de son plafond**. Le défaut est ailleurs : **douze faits que l'édition du 02/11 avait établis tombent à zéro dans celle du 09/11**, dont quatre adresses que mes propres corrections des 02 et 03/11 avaient rétablies. La règle enfreinte est écrite en tête du prompt du job — *« UNE ÉDITION NE PEUT PAS SAVOIR MOINS QUE LA PRÉCÉDENTE (14/09/2026) »* — et c'est la seule que rien n'instrumente.

**Les douze pertes sont mesurées une par une sur les deux textes extraits, pas estimées.** Compte d'occurrences dans N-1 (02/11) puis dans N (09/11) :

| Fait établi par N-1 | N-1 | N |
|---|---|---|
| `has-sante.fr/jcms/p_4159151` — page de l'appel Vie quotidienne 3-11 ans | 5 | **0** |
| `has-sante.fr/jcms/p_3892562` — page de l'appel Habitat volet 3 | 5 | **0** |
| `has-sante.fr/jcms/p_3578307` — page de l'appel Prévention spécialisée | 5 | **0** |
| `has-sante.fr/jcms/p_4549164` — page de l'appel Mineurs | 5 | **0** |
| `08/12/2026` — première réunion du GT CVS, à la HAS | 3 | **0** |
| `Saint-Denis` — son lieu | 1 | **0** |
| `1er trimestre 2027` — fin des travaux du GT CVS | 1 | **0** |
| `SAAD` — l'appel SAAD Familles, clos le 02/11 | 4 | **0** |
| `compte-rendu` — celui de la CSMS du 29/09, toujours non publié | 3 | **0** |
| `sessions transversales` — les 3 de l'Université d'automne | 1 | **0** |
| `rôle et missions` — la 4ᵉ session, sur la HAS elle-même | 1 | **0** |
| `26/10/2026` — clôture de l'appel Mineurs | 9 | **0** |

Et un treizième, qui est une forme et non un fait : **le tableau des appels à candidatures disparaît** — `1 <w:tbl>` dans N-1, **`0` dans N**. L'assertion d'intégrité du prompt ne bronche pas, et c'est son bornage du 18/10 qui travaille comme prévu : l'assertion de tableau est **bornée au chemin `/rbpp/`**, donc muette sur une note d'Étape 7 rangée dans `has-actualite/`, où les seize éditions du dépôt n'en portaient aucun. Le bornage est juste ; il laisse simplement cette régression de forme hors de portée.

**Et les quatre adresses perdues ne sont pas périmées : je les ai sondées à l'instant, une par une, et les quatre répondent.** `p_4159151` **HTTP 200 · curl 0 · 3 208 caractères utiles**, `p_3892562` **200 · 3 168**, `p_3578307` **200 · 3 160**, `p_4549164` **200 · 3 216** — les quatre sous le titre *« Haute Autorité de Santé - Identification »*, faisceau de certificats compris. Comparées à ma mesure du 02/11 (3 220 · 3 180 · 3 172) la dérive est de **−12 caractères chacune** : même mur, même habillage. 🟢 **Donc le « ⛔ Page inaccessible » du corps reste EXACT**, et c'est la vérifiabilité qui a été perdue, pas le fait. ⚠️ **C'est précisément ce que la correction du 02/11 avait acheté** : sa propre note de journal écrivait *« il est désormais vérifiable par quiconque, ce qu'il n'était pas »*. Sept jours plus tard, il ne l'est plus.

**La prédiction de la fiche du 02/11 était « un quatrième ⛔ » ; ce qui est arrivé est pire, et la mesure le montre.** Elle avait établi qu'une page d'appel HAS passe derrière le mur dès l'appel clos, et prédit que Mineurs suivrait. Mesuré aujourd'hui : `p_4549164` **est** derrière le mur (3 216 car., titre « Identification »). Mais la ligne Mineurs de N ne porte **ni ⛔ ni adresse** — elle a perdu les deux. Le mur est donc réel, non signalé, et non vérifiable. **La prédiction portait sur le symbole ; la régression a emporté le lien.**

**Le flux RSS Actualité de la HAS s'est effondré en une semaine, et la note le porte en `✅ lu`.** Mesuré, puis **remesuré à froid quinze secondes plus tard, identique à l'octet** : `feed/Rss2.jsp?id=p_3081656` rend **HTTP 200 · 3 057 octets bruts · 2 206 caractères utiles**, titre de flux `HAS - Actualité`, et **UN SEUL `<item>`, daté du 9 juillet 2024** — *« Accréditation des médecins et des équipes médicales : la HAS vient à votre rencontre »*. Ma propre fiche du 02/11 avait mesuré **3 entrées, toutes du 30/10/2026**, toutes des offres d'emploi. Le flux a donc perdu tout contenu courant entre les deux éditions. ⚠️ **L'énoncé de la note — *« Pas de nouvelle publication dans le flux RSS Actualité HAS entre le 02 et le 09/11/2026 »* — est littéralement VRAI et structurellement creux** : une absence lue dans un flux qui ne contient qu'un item de 2024 est indiscernable d'un flux muet, ce qui est la règle du 12/10 appliquée un étage plus haut. **Et 2 206 caractères est sous le plancher de façade de 3 000 du dépôt** : la note marque `✅ lu` une source que la doctrine maison appelle une façade.

**Trois outils du dépôt l'ont dit, chacun à sa place, et aucun ne pouvait refuser.** `aspirer.py` imprime `⚠ SOUS 3000 : façade, ou page rendue en JS ?` ; `controle_attributions.py` imprime `2206 car. utiles / 3004 octets bruts  <-- SOUS 3000` ; `controle_noms_propres.py` compte **1/6 page(s) NON LUE(s)** et **nomme l'adresse**. Le récapitulatif du job l'écrit même en clair dans son log : *« Page non lue = flux RSS Actualité (2 206 car., rendu RSS tronqué) »*. **Le chiffre existait, à trois endroits, pendant que le document écrivait `✅ lu le 09/11/2026, HTTP 200`.**

**Et le motif écrit le 05/11 pour exactement ce cas est muet — c'est sa limite, nommée le jour où il a été écrit, atteinte quatre jours plus tard.** Le motif `✅` + une cellule qui s'avoue sous le plancher exige que **le document AVOUE le compte** ; la consignation du 05/11 le dit mot pour mot : *« un mur non confessé reste hors de portée »*. Mesuré **dans les deux sens**, sur une copie **fabriquée au scratchpad** (le `.docx` du dépôt intouché, `git status` vérifié vide), avec garde par **soustraction** sur le XML — retirer exactement ce qui a été ajouté rend le XML d'avant :

| Document | Verdict de `controle_decompte.py` |
|---|---|
| Témoin fabriqué, la ligne de source ajoutant « Consultée (2 206 car. utiles) » | **`SOURCE DONNÉE POUR LUE SOUS LE PLANCHER (non bloquant) : 2206 caractères annoncés pour une ligne ✅, plancher 3000`** |
| Le document RÉEL, qui n'avoue rien | **aucune ligne** — `COHÉRENT`, exit 0 |

🔴 **C'est le premier cas de production de cet angle mort, et il tombe sur une autre série que celle qui l'a fait naître** (`ai-act` 30/10, `SERAFIN-PH` 04/11 → `has-actualite` 09/11). 📌 **La piste que cela ouvre est bornée et n'est pas ordonnée** : le compte des caractères utiles est déjà mesuré par `controle_attributions.py` à chaque passage — le faire **écrire par le prompt** dans la ligne de source rendrait le motif du 05/11 actif sans rien changer au contrôle.

**La note rebaptise la commission, et la page qu'elle lie l'écrit autrement — mesuré à zéro occurrence.** `Commission sociale et médico-sociale` : **0 occurrence sur les six pages lues**. Ce que les pages écrivent : `Commission en charge du social et du médico-social` (**① LITTÉRAL**, 1 occurrence, page CSMS) et `Commission CSMS` (**①**, 2 occurrences, calendrier). Balayage des **vingt éditions de la série** : la forme de la note n'apparaît que dans **deux** — le 04/07/2026 (1 occurrence) et le 09/11/2026 (**3**) — tandis que le 12/10 et le 02/11 écrivaient tous deux la forme de la page. ⛔ **Et aucune passe ne pouvait le voir, pour quatre raisons qui ne se recouvrent pas** : le nom n'est pas entre guillemets (B et B-FR aveugles), il est cohérent avec lui-même dans le document (B-NOM aveugle), il ne porte aucun chiffre (D aveugle), et `controle_noms_propres.py` l'écarte parce que `commission`, `sociale` et `médico-sociale` existent **tous en minuscules** dans le corpus — c'est le discriminant de casse du 31/10 qui le jette, et c'est la limite mesurée de la méthode « corpus pour dictionnaire ». **Le contrôle n'a interrogé qu'UN nom sur ce document ; celui-là n'en faisait pas partie.**

**La convention d'héritage est tenue 7 fois sur 7 là où elle est gardée, et elle tombe une fois, sur la seule date qu'aucune page ne porte.** Recensement de toutes les dates du corps : **7 lignes de « RBPP en cours d'élaboration » portent leur marqueur « d'après l'édition du JJ/MM/AAAA de cette veille », 7 sur 7**, plus la ligne CVS — même score que le 02/11. Toutes les autres dates non marquées sont **①** sur une page de la note (`09/11/2026`, `13/11/2026`, `20/11/2026`) ou sont la date de production. 🔴 **Une seule échappe : `29/09/2026`**, dans la rubrique Impacts — *« première réunion de la Commission … depuis le 29/09/2026 »* —, **④ ABSENT sur les six pages** et portée par **six éditions consécutives** (28/09 → 02/11). Fait vrai, héritage traçable, marqueur absent. ⚠️ **Et le motif 2 du bloc 7.6 bis ne peut pas le voir : il n'apparie que trois formes verbales** — `clos le`, `clôture le`, `N séances`. « première réunion … depuis » n'en est aucune. **La convention est gardée sur des tournures, pas sur la notion d'héritage.**

**Trois des cinq motifs du bloc 7.6 bis n'ont rien cherché, pour la deuxième semaine d'affilée — et le défaut latent de sa fonction `page()` reste donc inexercé.** Rejoué verbatim depuis `jobs_config.json` sous `env -i` : **exit 0**. Instrumenté sur une copie du scratchpad : **motif 1 INERTE** (0 en-tête « Dernières … publiées », 0 ligne de bloc), **motif 3 INERTE** (0 ¶ portant un mot de projection), **motif 4 INERTE** (6 lignes ✅ dans les sources, **0 titre entre guillemets dedans**), **motifs 2 et 5 exercés** (4 phrases « clos le / clôture le / N séances », phrase de semaine creuse présente et flux `p_3081452` lié). 🔴 **Et `page()` a fait ZÉRO appel réseau** — mesuré, 0 page en cache : les deux seuls motifs qui l'appellent sont 1 et 4, inertes. Le défaut relevé le 02/11 — **`page()` construit son propre `curl` sans `--cacert`** — est donc **latent pour la deuxième semaine, et aucun créneau ne peut le prouver**. ⚠️ Il mordrait le jour où un hôte casse sa chaîne, comme `has-sante.fr` le 18/10 et `cnsa.fr` le 26/10.

**Ce que la note affirme sur la foi d'une page est exact, et les treize appariements sont au degré ①.** Page CSMS : `09/11/2026`, `9 novembre 2026`, `09h30 - 17h`, `CSMS` — **① les quatre**. L'argument de contraste pour l'ordre du jour est remesuré et il tient : `Ordre du jour`, `Documents` et `Télécharger` sont **④ tous trois** sur la page de la réunion, pendant que le calendrier porte `Documents Ordre du jour CEESP 10 novembre 2026` pour la commission voisine — l'absence est donc significative, pas une lacune de lecture. Page Université d'automne : `20 novembre 2026`, `20/11/2026`, `13h30 - 17h45`, `100 % en ligne`, `Inscription gratuite et obligatoire`, `4 sessions thématiques`, `sessions transversales`, `Un logement c'est bien, avec un projet de vie c'est mieux`, `Protection de l'enfance : la visite en présence`, `15h00`, `16h00` — **① les onze**. Page Surdicécité : `13/11/2026`, `13 novembre 2026`, `rbpp.surdicecite@has-sante.fr`, `personnes présentant une surdicécité` — **① les quatre**. Calendrier : `09/11/2026`, `CSMS`, `09h30 - 17h`, `20/11/2026`, `Université d'automne` — **① les cinq**.

**La semaine creuse est prouvée, et c'est le seul des deux flux qui prouve quelque chose.** `feed/Rss2.jsp?id=p_3081452` (Recommandations et guides) : **0 entrée depuis le 02/11/2026 sur ses 50 items**, **47 945 caractères utiles**, item le plus récent du **13/10/2026** (*Analyse des déclarations d'EIGS liés aux gaz à usage médical*). L'énoncé *« Aucune nouvelle RBPP publiée … entre le 02 et le 09 novembre 2026 »* est donc exact et lié, et le motif 5 du 7.6 bis le vérifie. ⚠️ **Et ce même flux porte deux notes de cadrage que la note ignore**, dont `L'accompagnement des familles … par les SAAD Familles – Note de cadrage` du **08/10/2026** — la série avait l'appel SAAD la semaine passée et l'a laissé tomber en entier.

**Deux réserves sur les guillemets, dont une qui tronque un titre qui tenait.** ① `« Surdicécité en ESSMS »` sort en **② GRAPHIE, pas ①** : la page écrit `surdicécité en ESSMS` en minuscules, **5 occurrences**, et son titre complet est *« L'accompagnement des personnes présentant une surdicécité en ESSMS »*. C'est un **libellé abrégé entre guillemets**, pas une citation — le degré ② y est acceptable (règle du 25/10 sur la capitale de position), mais la règle du dépôt reste qu'une citation se prouve au degré ①. ② `« Protection de l'enfance : la visite en présence... »` **tronque un titre que la page donne en entier** : `Protection de l'enfance : la visite en présence d'un tiers aujourd'hui`. La troncature est signalée par les points de suspension, donc honnête — mais elle était évitable, et la règle du 15/10 vaut d'être rappelée : *une capture tronquée est introuvable sur sa page*. ⚠️ **Et un détail du programme n'est pas dit** : la session logement est à `15h00-15h45` **en parallèle** de `Fertilité : avant l'arrivée de la cigogne, il y a les bons réflexes`, même créneau. L'horaire de la note est exact ; la concurrence ne l'est pas mentionnée.

**La source que la doctrine du job nomme pour les pages murées est publique, liée depuis une page lue, et la note ne la prend pas.** La règle du 14/09 inscrite dans le prompt dit : *« Quand la page directe est fermée, tu vas à la note de cadrage et tu la lies »*. La page Surdicécité porte en clair *« La note de cadrage présentant les enjeux de cette recommandation est disponible sur le site de la HAS »* et lie `Accompagnement des personnes présentant une surdicécité en ESSMS – Note de cadrage`, **Recommandation de bonne pratique 07/10/2026**. 🟢 **Ce n'est pas un défaut au sens du prompt** — la note n'écrit **aucune** projection de publication, donc le motif 3 du 7.6 bis est inerte à bon droit — **mais c'est la source qui aurait permis d'écrire un calendrier au lieu d'« aucune date de publication connue »**, et c'est aussi celle qui manque aux trois lignes murées.

**Le discriminant du mur d'identification, posé le 02/11, est confirmé et affiné — et le plancher de façade reste incapable de le voir.** `Identification` : **0 occurrence sur les six pages lues** (dont la page CSMS, vraie page d'événement à **3 693 caractères**), contre le titre `Haute Autorité de Santé - Identification` sur **les quatre murs**. 🔴 **Et l'écart de taille s'est resserré** : le mur le plus épais fait **3 216** caractères, la vraie page d'événement **3 693** — **477 caractères d'écart**, tous deux **au-dessus** du plancher de 3 000. **Relever le plancher accuserait la page CSMS ; le laisser laisse passer les murs. Le seul discriminant mesuré reste le mot, pas le volume.**

**`rattrapage_jobs.sh --manques` accuse un créneau ANTÉRIEUR à la naissance du job, et c'est une classe neuve.** Il imprime `Tue 03/11 08h03 neuropsychologie-lecon ⛔ MANQUÉ` et sort en **1**. Or le job a été créé le **07/11/2026** — quatre jours après ce mardi. ⚠️ **Le mécanisme est structurel** : `--manques` lit les créneaux prescrits dans `jobs_config.json` **de l'arbre de travail** et les compare aux logs présents ; il n'a aucune notion de la **date de naissance** d'un job. 🟢 **Et la gravité est bornée par deux mesures** : l'accusation se **guérit seule** le 10/11, quand la fenêtre de 7 jours lâche le 03/11 ; et l'outil n'est **pas câblé au hook**, donc il ne refuse aucun push. ⛔ **Mais le job lui-même n'est PAS publié** : `neuropsychologie-lecon` compte **0 occurrence dans `jobs_config.json` à HEAD** — il est planifié dans launchd, présent sur le disque, et absent du dépôt public. 📌 Piste bornée, non ordonnée : ne compter un créneau manqué qu'à partir du premier commit qui introduit son id — lisible sans réseau, par `git log -S`.

**Les mesures du job, et le chiffre qui dit que ce n'est pas le prompt qui paie.** **2,7834 $ pour un plafond de 5,00 $ — 56 %**, **34 tours**, 7 min 14 s (433 750 ms), 22 912 jetons en sortie, **4 613 148 de cache lu**, 153 670 écrits, **une seule tentative**, `exit 0`, chemin **Étape 7**. Trajectoire sur cinq créneaux : **59 · 93 · 42 · 55 · 56 %**. 🔴 **Le prompt est IDENTIQUE À L'OCTET depuis `df175b3`** — sha256 `2e777945e59e`, 58 782 octets, vérifié à HEAD, au commit du jour et dans l'arbre — donc l'écart de coût avec le 02/11 ne vient **que** du cache : **cache-read par tour 125 471 → 135 681 (+8 %)**, et **coût par tour 0,0588 → 0,0819 $, soit +39 %**, pour **13 tours de moins** (47 → 34). ⚠️ **Dit autrement : le job a payé presque le même prix en faisant un tiers de tours en moins** — et c'est le troisième créneau consécutif où la mécanique du cache explique seule la dépense. Document de **13 342 octets** pour **6 152 caractères**, 42 paragraphes porteurs de texte, **6 adresses, 15 liens, 0 tableau**, marge 27. ⚠️ **Et un écart d'un octet, dit une fois** : le log annonce `58781` là où la valeur JSON fait **58 782** — `${#JOB_PROMPT}` perd la fin de ligne que la substitution de commande rogne. Constant, bénin, et ma correction du 02/11 portait sur le nombre que le log imprime, non sur la valeur.

**Les dix contrôles sortent en 0, et cinq passes sur onze n'ont rien cherché.** `controle_decompte.py` **COHÉRENT** (6 ✅ · 0 ⚠ · 0 ⛔ · 6 tentées, annoncé = listé). `controle_attributions.py` **exit 0, 0 bloquant**, avec **5 passes INERTES déclarées** — B (0 citation anglaise), B-NOM, C, C2 et **D (0 valeur chiffrée en contexte d'attribution, quatrième édition d'affilée)** : *une note faite de dates échappe à la seule passe qui vérifie les valeurs attribuées.* Son unique réserve B-FR est **la phrase-gabarit « d'après l'édition du JJ/MM/AAAA de cette veille »** — **cinquième récurrence** après les 12/10, 19/10, 26/10 et 02/11, et le bornage posé le 01/11 pour l'axe ② n'y a toujours pas été porté. `controle_edition_precedente.py` **exit 0**, 2 points à relire, tous deux sur la phrase SERAFIN-PH. `controle_noms_propres.py` **exit 0**, 1 nom interrogé, 11 écartés, **1/6 page non lue** nommée. `controle_livrable_du_job.py` accepte (㊳ muet, `is_error=False`) et relève **6 testés · 6 retenus · 0 écarté**. Assertion d'intégrité rejouée verbatim : `OK — XML conforme, 15 lien(s), 42 paragraphe(s) de texte (marge 27), 0 tableau(x)`. Gate `--docs` **exit 0**, document accepté comme **nouveau**. `audit_vault.py` **9/9**. Et `HEAD` = `origin/main` = **`2685291`** : le document **est publié**.

**L'axe ③ a eu raison de faire revérifier la phrase SERAFIN-PH, et la réponse est la même que la semaine passée.** Il signale *« Bascule SERAFIN-PH 2027 — aucune publication HAS spécifique cette semaine »* comme **recopiée mot pour mot de N-1 sans mention d'héritage**, avec sa ligne de réserve : *une absence vraie la semaine passée peut être fausse celle-ci*. Vérifié : `SERAFIN` et `SERAFIN-PH` comptent **0 occurrence** sur les six pages, et **0 entrée** dans les deux flux depuis le 02/11. L'absence est donc vraie. ⚠️ **Mais elle est recopiée sans marqueur, comme `29/09/2026`** — deux héritages non marqués dans la même rubrique, pour un document qui tient 7/7 ailleurs. Et l'axe ② signale la même phrase, pour l'autre raison : la fiche de N-1 la donne pour fautive. **Les deux axes convergent sur la seule phrase du document que personne n'a réécrite depuis le 26/10.**

**Mon erreur de la séance, et c'est la même que les deux dernières fois.** J'ai lu `--manques exit=0` sur une commande tuyautée dans `tail -18` : c'est le code de `tail`. Remesuré sans tuyau, **exit 1**. C'est la règle du 15/10 — *« un garde qui ne fait pas sortir en 1 est décoratif »*, dont le corollaire est qu'un code lu derrière un tuyau n'est pas le code qu'on croit — enfreinte par moi le **31/10** sur un `git push`, le **06/11** dans un témoin, et **ici une troisième fois**. Le défaut n'est pas dans l'outil ; il est dans ma manière de le lire.

### Requêtes passées

Sept pages aspirées sur disque (`aspirer.py`), **aucune n'est entrée en contexte** ; appariement par `chercher.py`, degré **①** exigé pour tout ce qui est entre guillemets, chaque date interrogée dans ses **deux graphies**. Les six adresses de la note, plus une **relecture à froid** du flux Actualité. Les deux flux lus par `lire_page.py --items`, le programme et les mentions d'édition par `lire_page.py --autour`, **jamais une page en entier**. Les quatre murs sondés par `curl --cacert` sans aspiration. Aspiration et sondages **strictement séquentiels, 15 s d'intervalle** (règle du 12/10).

| Requête | Verdict |
|---|---|
| `09/11/2026` · `9 novembre 2026` · `09h30 - 17h` · `CSMS` | **① LITTÉRAL** les quatre — page CSMS |
| `Ordre du jour` · `Documents` · `Télécharger` | **④ ABSENT** les trois — page CSMS ; contraste `Documents Ordre du jour CEESP 10 novembre 2026` sur le calendrier |
| `Commission sociale et médico-sociale` | **④ ABSENT**, 0 occurrence sur les 6 pages |
| `Commission en charge du social et du médico-social` | **① LITTÉRAL** — page CSMS, 1 occurrence |
| `Commission CSMS` | **① LITTÉRAL** — calendrier, 2 occurrences |
| `29/09/2026` · `29 septembre 2026` | **④ ABSENT** sur les 6 pages ; portées par 6 éditions antérieures |
| `20 novembre 2026` · `20/11/2026` · `13h30 - 17h45` · `100 % en ligne` | **①** les quatre — page Université |
| `Inscription gratuite et obligatoire` · `4 sessions thématiques` · `sessions transversales` | **①** les trois — page Université |
| `Un logement c'est bien, avec un projet de vie c'est mieux` · `15h00` | **①** les deux — page Université |
| `Protection de l'enfance : la visite en présence` · `16h00` | **①** les deux ; titre complet de la page : `… d'un tiers aujourd'hui` |
| `2e édition` | **④** ; la page écrit `la deuxième édition` — conversion licite, hors guillemets |
| `13/11/2026` · `13 novembre 2026` · `rbpp.surdicecite@has-sante.fr` | **①** les trois — page Surdicécité |
| `personnes présentant une surdicécité` · `surdicécité` | **①** les deux — page Surdicécité |
| `Surdicécité en ESSMS` | **② GRAPHIE** ; la page écrit `surdicécité en ESSMS`, 5 occurrences |
| `sourdes-aveugles` | **④** ; vocabulaire de la note, hors guillemets |
| `Dossier de candidature` | **② GRAPHIE** — page Surdicécité |
| `20/11/2026` · `Université d'automne` | **①** les deux — calendrier |
| flux `p_3081452` — items depuis le 02/11/2026 | **0 entrée sur 50** · 47 945 car. · plus récent **13/10/2026** |
| flux `p_3081656` — tous les items | **1 entrée, 09/07/2024** · 2 206 car. · **remesuré identique à froid** |
| `SERAFIN` · `SERAFIN-PH` | **0 occurrence** sur les 6 pages et les 2 flux |
| `Identification` sur les 6 pages lues | **0** ; sur les 4 murs : titre de page |
| `p_4159151` · `p_3892562` · `p_3578307` · `p_4549164` | **200 · curl 0** · 3 208 / 3 168 / 3 160 / 3 216 car. · mur d'identification |
| Les 12 faits de N-1, comptés dans N | **0 occurrence** chacun — tableau du résumé |
| `Commission sociale et médico-sociale` sur les 20 éditions | **2 éditions** : 04/07 (1) et 09/11 (3) |
| sha256 du prompt rbpp-pipeline, 3 états | **`2e777945e59e`** partout — identique à l'octet |

### Ce que STANDARD n'a pas interrogé

- **L'ordre du jour réel de la CSMS du 09/11**, qui siège aujourd'hui — il n'existait pas au moment de la production de la note, et il n'existe pas davantage à celui de cette fiche. Le document a raison de ne rien en dire.
- **Les cinq sessions non ESSMS de l'Université d'automne** (`La HAS sans filtre`, `L'IA sur le terrain`, `Fertilité`, `Sécurité des patients`, `Vaccination`, `Professionnels de santé cherchent partenaires particuliers`) : relevées au passage sur la page, non vérifiées ligne à ligne — hors périmètre médico-social.
- **La note de cadrage Surdicécité du 07/10/2026**, repérée sur la page de l'appel et **non ouverte** : c'est la source que la doctrine du 14/09 prescrit pour une page murée, et son contenu n'est pas mesuré ici.
- **La note de cadrage SAAD Familles du 08/10/2026**, vue dans le flux et non ouverte.
- **Les quatre murs n'ont pas été lus au-delà de leur titre et de leur volume** : je n'ai mesuré que code HTTP, code `curl` et caractères utiles. Ce qu'ils cachent reste inconnu, par construction.
- **Aucune recherche hors has-sante.fr** : ni `WebSearch`, ni archive. Une page HAS déplacée ou un fait annoncé ailleurs resterait invisible.
- **Les huit « runs non publiés » hors fenêtre** que `--manques` compte sans les nommer : non examinés, et la purge des logs à 30 jours effacera cette mesure.

## Notes liées

- **⬅️ Précédente** · [[2026-11-02_veille_has-actualite.fiche]]
  **son acquis a été défait par l'édition suivante, et ce sont MES corrections qui ont été perdues.** Elle avait fait rétablir **quatre adresses** de pages murées (les 02 et 03/11) et écrit que l'inaccessibilité devenait *« vérifiable par quiconque »* ; sept jours plus tard les quatre sont à **0 occurrence**, alors que les quatre pages répondent toujours **200** derrière leur mur. 🟢 Deux de ses mesures ont resservi telles quelles : son **argument de contraste** sur l'ordre du jour (`Documents` présent pour la commission voisine, absent pour la CSMS) et son **discriminant « Identification »**, aujourd'hui **0 sur 6 pages lues contre 4 murs sur 4** — et l'écart de volume s'est resserré à **477 caractères**, ce qui interdit définitivement de relever le plancher. ⚠️ Et sa prédiction d'un **quatrième ⛔** est démentie par le pire : le mur est bien là sur `p_4549164`, mais la ligne a perdu **le ⛔ ET l'adresse**
- **➡️ Suivante** · édition du 16/11/2026 (lundi 8h30, `rbpp-pipeline`)
  **trois choses à vérifier d'emblée, toutes mesurées aujourd'hui** : ① les **quatre adresses murées** sont-elles revenues, ou la perte est-elle acquise — c'est le seul point où une fiche peut encore agir avant que l'édition suivante ne recopie la version amputée ; ② le **flux Actualité `p_3081656`** s'est-il rempli, ou reste-t-il à **1 item de juillet 2024** — s'il reste creux, le marquer `⚠` et non `✅` ; ③ la commission est-elle de nouveau nommée **comme la page la nomme**
- **🔗 Pont** · [[2026-11-08_veille_imac.fiche]]
  **la classe de défaut qu'elle a nommée hier se mesure ici pour la deuxième fois en deux jours, sur une autre série.** Elle avait établi qu'un **fait perdu par oubli** n'est vu par aucun axe de `controle_edition_precedente.py` — ① ne suit que les corrections **rejouées**, ② les formulations que la fiche **dénonce**, ③ les phrases d'absence **recopiées** — et proposé de faire lire à l'axe ② les chiffres que la fiche de N-1 **établit**. Le cas d'aujourd'hui est **douze fois plus gros** et il ajoute un argument qu'elle n'avait pas : **quatre des douze pertes sont des adresses posées par une CORRECTION du dépôt**, donc l'axe pourrait les suivre sans heuristique — le journal de N-1 les nomme, et ① lit déjà ce journal
- **🔗 Pont** · [[2026-11-04_veille_SERAFIN-PH.fiche]]
  **le motif du 05/11 né de son incident rend ici son premier verdict de production, et c'est un silence prévu.** Elle portait la source primaire donnée pour lue à **93 caractères utiles** ; le motif écrit pour cette classe exige que **le document avoue le compte**, et il est **muet** sur les **2 206 caractères** du flux Actualité, que le document n'avoue pas. 🟢 Mesuré dans les deux sens sur un témoin **fabriqué** : la ligne apparaît dès que le compte est écrit. 📌 La piste qui fermerait la classe est donc dans le **prompt**, pas dans le contrôle — faire écrire le compte que `controle_attributions.py` mesure déjà à chaque passage
- **🗂️ Dossier** · [[HAS-actualite_dossier.fiche]]
  à mettre à jour sur cinq points mesurés : ① **la série perd ses acquis d'une semaine sur l'autre** — douze faits de N-1 à zéro dans N, dont quatre adresses issues de corrections, et le prompt porte pourtant la règle *« une édition ne peut pas savoir moins que la précédente »* en tête ; ② **le flux Actualité `p_3081656` n'est plus une source** — 1 item de 2024, 2 206 caractères, à marquer `⚠` tant qu'il reste creux ; ③ **le mur d'identification ne se distingue plus par le volume** (3 216 contre 3 693 pour une vraie page d'événement), le seul discriminant mesuré restant le mot `Identification` ; ④ **le nom de la commission est `Commission en charge du social et du médico-social`** sur la page HAS, et aucune passe du dépôt ne peut voir qu'une note le réécrit ; ⑤ **la convention d'héritage n'est gardée que sur trois tournures** — `clos le`, `clôture le`, `N séances` — donc un « depuis le JJ/MM/AAAA » y échappe
