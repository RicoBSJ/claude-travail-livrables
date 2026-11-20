---
type: fiche-document
source: 2026-11-18_veille_SERAFIN-PH.docx
date_creation: 2026-11-19
date_veille: 2026-11-18
veille: serafin-ph
statut: corrigee
date_correction: 2026-11-19
date_relecture_sources: 2026-11-20
tags:
  - veille/serafin-ph
  - registre/pro
  - concept/recueil-ph-2026
  - concept/sidoba
  - concept/dotation-complementaire
  - concept/modulation-de-l-activite
  - concept/comite-strategique
  - source/cnsa
  - source/atih
  - source/handicap-gouv
  - theme/semaine-creuse
  - theme/facade-js-93-caracteres
  - theme/mur-marque-coche-sans-compte
  - theme/attribution-deplacee-vers-la-mauvaise-source
  - theme/correction-des-attributions
  - theme/date-inferee-donnee-pour-lue
  - theme/recapitulatif-qui-decrit-d-autres-pages
  - theme/recapitulatif-qui-rapporte-la-conclusion
  - theme/passes-inertes-sur-une-note-sans-citation
  - theme/route-de-lecture-perdue
  - theme/mur-waf-qui-repond-200-sur-un-404
---

# 2026-11-18_veille_SERAFIN-PH

Document source : [[2026-11-18_veille_SERAFIN-PH.docx]]

## Résumé

**Semaine creuse honnêtement déclarée, zéro bloquant à tous les contrôles du dépôt — et quatre défauts de fond que rien ne pouvait voir, parce que la note ne cite personne.** `controle_attributions.py` rend `0 problème(s) bloquant(s)` et imprime lui-même pourquoi : **cinq de ses passes sont INERTES** sur ce document (B, B-FR, B-NOM, C, C2) — zéro citation entre guillemets, zéro affirmation prêtée à une source nommée. Or les trois défauts d'attribution de cette note sont tous en **style indirect, sous un en-tête de section qui nomme la source** : une forme que B-NOM ne reconnaît pas. *Une passe inerte n'est pas une passe réussie*, et c'est la troisième semaine d'affilée que cette phrase décide du verdict.

**Le défaut qui change un fait : « la dotation globale » là où la page écrit « à la modulation de l'activité ».** La note écrit *« Phase 2 : recueil centré sur les indicateurs visant la dotation globale (une dizaine de variables) et la dotation complémentaire (6 variables) »*. La page CNSA écrit, dans la phrase même qui est paraphrasée : *« Courant mai 2026, seconde phase centrée sur les indicateurs visant à la modulation de l'activité (une dizaine de variables) et à la dotation complémentaire (six variables) »*. Mesuré sur les 8 741 caractères utiles : **« dotation globale » = 0 occurrence · « modulation » = 1**. Ce n'est pas une variante de graphie, c'est un **autre composant du modèle** — et la note bâtit dessus son point de vigilance *« Dotation complémentaire : identifier les 6 variables qui vous concernent »*, qui reste juste, à côté d'une phase 2 qui ne mesure pas ce qu'elle dit.

**Le deuxième défaut déplace une échéance vers la mauvaise source, et c'est l'échéance qui rend la semaine actionnable.** *« Automne 2026 — Vérification et validation des données par les établissements et les ARS »* figure dans la liste *« Calendrier du recueil PH 2026 (au moment de la publication — 17/12/2025) »*, sous la source CNSA. **« automne » : 0 occurrence sur la page CNSA.** L'énoncé est réel, mais il vient du **communiqué handicap.gouv.fr publié le 27/03/2026** — *« les établissements et les agences régionales de santé seront mobilisés jusqu'à l'automne 2026 pour fiabiliser les données »* —, soit trois mois **après** la date sous laquelle la note le range. Le fait est juste, l'attribution et la date de publication sont fausses, et c'est de cette ligne que descendent le tableau de bord (*« 🟡 En cours — automne 2026 »*) et le point de vigilance *« délai automne 2026 — imminente »*.

**Le troisième donne à l'ATIH un rôle et une date qui sont ceux de la DGCS et de la CNSA.** La note écrit *« L'ATIH co-pilote la documentation méthodologique de SERAFIN-PH depuis fin 2014, en lien avec DGCS et CNSA »*. La page ATIH écrit : *« Depuis fin 2014, la Direction générale de la cohésion sociale (DGCS) et la Caisse nationale de solidarité pour l'autonomie (CNSA) conduisent les travaux nécessaires à la réforme »* — **1 occurrence de « 2014 », et elle porte sur les deux co-pilotes, pas sur l'ATIH**. ⚠️ Et la note se contredit elle-même quatre paragraphes plus loin, dans son tableau des acteurs, où l'ATIH est *« Appui méthodologique et technique »* : c'est la bonne formulation, et c'est celle qui aurait dû servir.

**Le quatrième est une date juste présentée comme une lecture : « 23 mars » n'est écrit nulle part sur la page.** La note l'affirme deux fois (*« Réunion du 23 mars 2026 »*, *« 14e comité, 23 mars 2026 »*). Le communiqué est **publié le 27/03/2026** et dit *« Ce lundi »*. Calculé : **27/03/2026 est un vendredi, 23/03/2026 le lundi de la même semaine** — l'inférence est donc **exacte**, et c'est une inférence. Une veille qui nomme sa source et donne une date sans dire qu'elle l'a déduite rend indiscernables ce qu'elle a lu et ce qu'elle a calculé.

**🔴 Et la mesure qui tranche tout cela, le dépôt ne peut pas la faire : la page sert 93 caractères à `curl` et 4 600 une fois rendue.** `aspirer.py` rend `HTTP 200 · 6 116 octets bruts · 93 car. utiles  ⚠ SOUS 3000 : façade, ou page rendue en JS ? regarde le brut` — le contrôle **demandait d'aller voir le brut**, et personne n'y était allé. Je l'ai ouverte dans le navigateur de l'application et interrogée **par fenêtres**, jamais en entier, comme le fait `lire_page.py --autour` : `innerText` **4 600 caractères**, et tout ce que la note tire de cette page y est, **mot pour mot** — *« Ce lundi, Camille Galliard-Minier, ministre chargée de l'Autonomie et des Personnes handicapées, a présidé le 14ᵉ comité stratégique de la réforme SERAFIN-PH »*, *« une mise en œuvre opérationnelle de la réforme tarifaire au 1er janvier 2027 pour les ESMS … du secteur « enfant » »*, *« Le recueil de données, lancé à partir du 30 mars 2026 »*. 🟢 **Donc le détour par WebFetch était le bon geste et il a rendu du contenu exact** ; et `controle_noms_propres.py` a été **honnête** en répondant *« 1/3 page(s) NON LUE(s) »* au lieu d'accuser. Le plancher de 3 000 caractères a produit ici un **faux négatif** : il a classé « façade » une page qui porte 4 600 caractères de communiqué réel.

**🔴 Le marquage du mur a régressé, et le motif du 05/11 se tait pour une raison NEUVE.** Mesuré sur les cinq dernières éditions de la série : **21/10 → `⚠️ Mur JavaScript` + « 93 caractères servis »** · **11/11 → `⚠️ JS` + « Page rendue en JS (93 car. utiles) »** · **18/11 → `✅ Consultée (page JS, contenu via WebFetch)`**. Le `⚠` devient `✅` **et le compte disparaît**. Le motif `murs_lus` exige le compte **dans la ligne du statut** (sa borne ②) : il ne peut donc pas mordre, alors que sa borne ① — qui épargne les `⚠` honnêtes — protégeait justement les éditions du 21/10 et du 11/11. **La forme de cette semaine est intermédiaire et c'est ce qui la rend invisible** : elle avoue le **mécanisme** (« page JS », « via WebFetch ») et tait le **compte**, donc elle prévient un lecteur humain et désarme le contrôle. 📌 **Piste bornée, mesurée, non faite, non ordonnée** : accuser un `✅` dans une cellule qui dit que **la page** est rendue en JS, sans compte — forme resserrée jouée sur les **126 éditions** du dossier `sources/veille/` : **1 seul signalement, ce document**, et **6 lignes qui doivent être ACCEPTÉES** (les `⚠️` du 21/10 et du 11/11, et l'entrée de journal du 04/11). ⛔ La forme naïve, elle, est **inacceptable et c'est mesuré** : en acceptant « WebSearch » et « WebFetch » comme marqueurs, elle rend **37 signalements dont 36 légitimes** — des lignes de décompte et des notes méthodologiques où `✅` et « WebSearch » se croisent sans qu'aucune page ne soit murée.

**🔴 Et le récapitulatif du log décrit d'autres pages que le livrable : sur ses quatre sources, trois ne figurent nulle part dans le document, et l'une rend 404 aujourd'hui.** Le log liste `handicap.gouv.fr/serafin-ph`, `handicap.gouv.fr/comites-strategiques-serafin-ph`, `cnsa.fr/accompagnement-et-autonomie/serafin-ph` et l'ATIH 2026 ; la note cite `handicap.gouv.fr/reforme-tarifaire-…-14e-reunion-…`, `cnsa.fr/actualites/serafin-ph-preparation-…` et `atih.sante.fr/recueil-national-ph-2025`. **Seule la quatrième — le 404 — est commune aux deux listes.** Pire, le log crédite `cnsa.fr/accompagnement-et-autonomie/serafin-ph` de *« ✅ 8 741 car. (aspirer.py + CA bundle) »* : cette URL rend **404** (mesuré le 19/11), et les **8 741 caractères sont ceux de l'URL que la note cite** — `aspirer.py` les reproduit **exactement**. Le chiffre est juste, l'adresse à laquelle il est attaché ne l'est pas. ⚠️ Et rien ne pouvait le dire : **㊳ bis relit la ligne `🔗`, personne ne relit la liste des sources du log.**

**🔴 La ligne `👤` rapporte la conclusion au lieu de la mesure, et c'est la trace qu'elle devait garder qui disparaît.** Le log écrit `1 interrogé · 0 non retrouvé · 1 page non lue`. Le contrôle, **rejoué verbatim**, écrit : `1 nom(s) interrogé(s) · 5 écarté(s) aux bornes · 1/3 page(s) NON LUE(s)` puis `⚠️ NOM NON RETROUVÉ : « Camille Galliard-Minier » ne figure sur AUCUNE des 2 page(s) LUE(s)`. Le nom **est juste** — la page rendue le porte au littéral — et la démarche du job était conforme (vérification par `WebSearch`, consignée). Mais le récapitulatif prescrit le **30/10** existe pour que le log garde le verdict du contrôle, et **écrire le résultat résolu à la place de la mesure vide la ligne de sa fonction**. ⛔ Et le harnais ne peut pas le voir : ses quatre exigences portent sur le **prompt** — l'appel, la ligne au littéral, la borne des pages non lues, l'existence du script —, jamais sur la **concordance** entre les nombres écrits et la sortie du contrôle.

**Ce qui est exact, et il faut le dire avec la même précision.** Les deux comptes de caractères annoncés sont **justes au caractère** — CNSA **8 741**, ATIH **8 905**, reproduits par `aspirer.py`. L'année blanche est au **degré ① LITTÉRAL** : *« sans incidence sur le financement des structures en 2026 »*. Sont exacts sur leur page : `30 mars 2026`, `1er janvier 2027`, *« Du 03 février au 13 avril 2025 »*, *« Du 17 février au 16 mai 2025 »*, `RAMSECE-PH`, `e-PH`, la date de publication ATIH `14/05/2025`, SIDOBA et son développement *« dans le système d'information de l'offre de la branche autonomie (SIDOBA) de la CNSA »*, la *« quarantaine de variables strictement nécessaires »* au **degré ②**, et l'approche ciblée *« Contrairement au recueil du printemps 2025 »*. Le seul calcul de la note — *« Déploiement 1er janvier 2027 : moins de 7 semaines »* — est **juste** : du 18/11/2026 au 01/01/2027, **44 jours, soit 6,3 semaines**. Et le décompte des sources est cohérent : `✅ 3 · ⛔ 1 · total 4` pour un `3/4` annoncé.

**La route de lecture que N-1 avait ouverte a été reperdue, et sa fiche n'en avait pas gardé l'adresse.** La fiche du 11/11 avait déjà prouvé **au degré ①**, sur un **instantané d'archive** de cette même page (`HTTP 200 · 60 230 octets · 5 761 caractères utiles`), les six énoncés que les pages lisibles rendaient `④` : `30 mars 2026`, `14e réunion`, `Camille Galliard-Minier`, `automne 2026`, et le `1er janvier 2027` avec le verbe de la page. Mesuré sur cette fiche : **15 mentions du mot « archive », zéro adresse `web.archive.org`**. Le run du 18/11 a donc refait le chemin par une autre route, et ma lecture du jour redémontre à la live ce que N-1 avait démontré sur l'archive — **trois mesures du même fait, aucune réutilisable par la suivante**. C'est le mécanisme nommé le 09/11 pour la série HAS : *le job relit la note, jamais la fiche*.

### Avocat du diable

**Les quatre défauts ne changent aucune décision d'un chef de service, et c'est précisément ce qui les rend durables.** Un directeur qui lit cette note retient trois choses — vérifier ses données PH 2026 avant la fin de l'automne, former son référent à SIDOBA, préparer la gouvernance pour le 1er janvier 2027 — et les trois sont **justes**. Rien dans le livrable ne sera jamais contredit par la réalité : la correction d'une attribution ne produit pas de bénéfice visible, donc elle ne sera jamais priorisée, et la note suivante héritera des mêmes formes. ⚠️ **Et l'erreur « dotation globale » est la seule des quatre qui puisse mordre pour de vrai** : un établissement qui prépare sa phase 2 en croyant qu'elle mesure sa dotation globale regarde les mauvais indicateurs. C'est aussi la seule qui ne se répare pas en déplaçant une ligne : il faut relire la source.

### Correction du 19/11/2026

**Les quatre défauts sont corrigés dans le `.docx`, et le contrôle qui ne pouvait pas voir le défaut valide deux des quatre corrections.** `controle_attributions.py` était INERTE sur le corps faute de citation ; mais depuis le 03/11 sa passe B-FR lit **aussi le 📝 Journal des corrections**, où une formulation citée avec un verbe de portage au présent *est* confrontée à sa page. Les deux libellés rétablis y reviennent donc en `JOURNAL OK` : *« les indicateurs visant à la modulation de l'activité »* contre la page CNSA, *« Depuis fin 2014, la Direction générale de la cohésion sociale (DGCS) et la Caisse nationale de solidarité pour l'autonomie (CNSA) conduisent les travaux »* contre la page ATIH. **La correction d'une attribution en style indirect devient vérifiable par le dépôt au moment où elle est consignée** — c'est le journal qui donne la prise que le corps ne donnait pas.

| ¶ | Ce que la note écrivait | Ce qu'elle écrit maintenant | La preuve |
|---|---|---|---|
| Calendrier, ligne 2 | *« les indicateurs visant **la dotation globale** »* | *« les indicateurs visant **la modulation de l'activité** »* | citation de la page au **degré ① LITTÉRAL** · « globale » **0 occurrence** sur 8 741 car. |
| Calendrier, ligne 3 | *« **Automne 2026** — Vérification et validation … »*, rangé sous la CNSA du 17/12/2025 | la même échéance, le verbe de sa source (*« fiabiliser »*) et **la source nommée** : le communiqué du 27/03/2026 | « automne » **0 occurrence** sur la page CNSA, qui n'annonce que **deux** phases, et dont l'unique *« validation »* porte sur la CNIL |
| Section ATIH, ligne 1 | *« **L'ATIH co-pilote** la documentation … **depuis fin 2014** »* | *« Depuis fin 2014, **la DGCS et la CNSA conduisent les travaux** … ; l'ATIH en assure l'appui méthodologique et technique »* | citation de la page au **degré ①** · la formulation reprise est celle du **tableau des acteurs de la note elle-même** |
| Ligne de source institutionnelle | *« Réunion du 23 mars 2026. »* | *« Communiqué publié le 27/03/2026, qui situe la réunion au lundi précédent — soit le 23 mars 2026, **date déduite et non écrite sur la page** »* | « 23 mars » **0 occurrence** · *« Ce lundi »* + publication un **vendredi** → la date est juste, son statut manquait |

**Ce qui n'a PAS été corrigé, et ce sont des décisions.** Les deux défauts du **log** restent : sa liste de sources décrit d'autres pages que le livrable, et sa ligne `👤` écrit `0 non retrouvé` là où le contrôle dit l'inverse. Les corriger reviendrait à **réécrire la trace d'une exécution**, ce qui n'est pas permis — ils sont consignés ici et dans `JOBS.md`. La date du 23 mars est **conservée partout ailleurs** (tableau des sources, titre de section, tableau des acteurs) : elle hérite de la ligne corrigée, que son marqueur nomme. Et la question de fond laissée ouverte par l'audit — *« modulation de l'activité » et « dotation globale » désignent-ils la même enveloppe ?* — **n'est toujours pas tranchée**, parce qu'aucune des trois pages lues ne définit les deux termes côte à côte : la correction rétablit donc **le libellé de la source**, geste qui est juste dans les deux hypothèses, et le journal dit explicitement qu'aucune équivalence n'est supposée.

**Mesures de la correction.** `word/document.xml` **63 093 → 74 209 octets**, texte visible **37 705 → 45 121 caractères** — **ajouts seuls, aucun retrait** —, **4 marqueurs** gris italiques datés, **journal de 8 paragraphes** inséré avant `<w:sectPr>`, **4 tableaux** inchangés (plancher 3), marge d'intégrité **107 → 115**, conteneur reconstruit à **19 entrées, CRC OK, ordre identique**. Contrôles rejoués un par un, sans parallélisme : attributions **0 bloquant** (2 citations du journal, **les deux `JOURNAL OK`**), décompte **`COHÉRENT 3/4`**, édition précédente **`OK`** sur ses quatre axes, ㊳ **`exit 0`** avec `5 testés · 4 retenus · 1 écarté (404×1)`, intégrité des publiés **`DIVERGENT` non bloquant** — l'état exact d'une correction en cours —, et `non_regression.sh --docs` **exit 0, zéro `✗`**. ⚠️ `controle_noms_propres.py` rend **le même verdict qu'avant** (`NOM NON RETROUVÉ` + `1/3 page NON LUE`) et c'est normal : le nom est sur la page que le dépôt ne sait pas lire. Le journal porte désormais **la route qui le lit**, ce qui est la seule réponse possible à ce signalement.

**🔴 Deux défauts à moi, et le premier a été trouvé par le contrôle, pas par ma relecture.** ① Mon premier journal citait `« 0 non retrouvé »` entre guillemets pour dénoncer la ligne du log : B-FR l'a aussitôt lu comme une **citation attribuée à `cnsa.fr`** et l'a classée `JOURNAL A RELIRE` — *« le journal affirme qu'une page la porte, et aucune page lue ne la porte »*. **La mesure que j'écrivais créait, dans le document même qui la consigne, le faux positif qu'elle décrivait** : c'est la leçon du 31/10 (« un chiffre d'instrumentation posé dans un ¶ qui porte un lien devient une taille annoncée ») par l'autre bout. Reformulé sans guillemets, le signalement disparaît et il ne reste que les deux `JOURNAL OK`. ② J'avais oublié de consigner que le **nom de la ministre** avait été lu, lui aussi, sur la page rendue — c'est-à-dire la réponse au seul signalement que la note conserve. 🟢 **Les deux fois, le document a été restauré depuis la sauvegarde au sha256 identique, puis repatché EN ENTIER depuis la source intacte**, jamais rattrapé par-dessus : *une correction partielle est pire qu'un échec* (25/10).

### Lecture du 20/11/2026 — les deux URL du log

**Les deux adresses que le log crédite de son contenu ont été lues : l'une est une archive de 2017, l'autre n'existe pas — et `curl` répond `200` aux deux.**

| URL du log | `curl` + faisceau | Navigateur intégré | Ce qu'elle porte |
|---|---|---|---|
| `handicap.gouv.fr/serafin-ph` | **200** · 93 car. | **200** · **17 805 car.** | **« Publié le 23/06/2017 »**, section « Les chantiers **2018-2019** », ENC 2018/2019 ; dernière date citée **10 janvier 2019** |
| `handicap.gouv.fr/comites-strategiques-serafin-ph` | **200** · 93 car. | 🔴 **404 — « Page non trouvée »** | rien : la page n'existe pas |

🔴 **Le fait de forme, et il touche tout l'appareil de test du dépôt : un mur WAF qui répond `200` masque un `404`.** Le mur — `Please enable JavaScript to view the page content. Your support ID is: …`, **5 695 octets**, **même gabarit aux deux URL** (elles ne diffèrent qu'à l'octet 574, l'identifiant de support) — est servi **avant le routage** : `curl` ne voit jamais le code de la page. Donc `balayer_adresses.py` classe cette adresse morte en `FACADE ?`, ce qui est le bon degré de prudence, mais **aucun outil du dépôt ne peut dire qu'elle est morte**, et la ligne `🔗 5 testés · 4 retenus · 1 écarté (codes : 404×1)` du log compte son unique 404 ailleurs (ATIH). *Un `200` ne prouve pas qu'une page existe* (25/10) — ici c'est un cran plus grave, parce que le `200` masque un **code d'erreur réel** et non une page vide.

🟢 **Et la lecture tranche la question de fond que la correction du 19/11 avait laissée ouverte : « dotation globale » et « modulation » ne sont PAS la même chose.** La page que le document cite vraiment (`…14e-reunion-du-comite-strategique`, **publiée le 27/03/2026**) porte les deux et les distingue : *« intégrer notamment la question du financement des transports dans **la dotation globale** »* — l'enveloppe — contre *« des groupes de travail dédiés aux **modulations de financement** »* — les paramètres. La correction ① n'était donc pas seulement fidèle à sa source : **le libellé d'origine était un vrai défaut de fond.**

🟢 **Deux corrections du 19/11 sont confirmées par une page que je n'avais pas lue.** ② au mot, **degré ①** : *« Les établissements et les agences régionales de santé seront mobilisés jusqu'à l'automne 2026 pour **fiabiliser les données** »*, et la même page porte *« Cabinet de Mme. **Camille Galliard-Minier** »*, ce que le journal du document consigne. ③ par l'archive de 2017, qui écrit *« L'équipe projet SERAFIN-PH (**DGCS-CNSA**) travaille en concertation et co-construction… »*, l'ATIH n'y apparaissant que comme co-publicateur des études de coûts.

⚠️ **Et le `4 600` de cette fiche est le bon chiffre, mesuré de nouveau le 20/11** : `body` **4 600** (ce qu'aplatit `aspirer.py`), `main` **2 839**, `article` **2 656**. Comparer le plancher de 3 000 au `main` aurait inversé la conclusion — *une borne qui compare deux découpages différents ne compare rien* (31/10). Le faux négatif du plancher tient donc.

### Mesures du job

| | |
|---|---|
| Coût | **3,2231 $ / 5,00 $ = 64 %**, plafond relevé le 11/11 après un dépassement à 101 % — **le relèvement a tenu** |
| Tours · durée | **36 tours**, 576 685 ms (9 min 37 s) · 1 tentative · `exit 0` · `stop_reason=end_turn` |
| Jetons | out 26 422 · cache-read 4 755 672 · cache-write 262 633 · prompt **35 312 octets** |
| Intégrité | XML conforme · 6 liens · 113 ¶ (marge 107) · **4 tableaux** (plancher 3 pour cette série) ✅ |
| Publication | `✅ push OK`, commit `dbec1e8` · audit du coffre **9/9 au vert** · journal d'exécution **5 scripts, 0 orphelin** |

### Requêtes passées

| Requête | Verdict |
|---|---|
| `chercher.py --fichier` 14 requêtes **extraites du document** × 3 pages | **1 ①** · **1 ②** · 12 ④, tous élucidés par `lire_page.py` ou par la page rendue |
| `lire_page.py --autour` × 10 (CNSA : modulation, dotation globale, transport, SIDOBA, automne · ATIH : RAMSECE, 3 février, 16 mai, 2014, e-PH) | **« dotation globale » 0 · « automne » 0** sur CNSA ; tout le reste présent |
| `aspirer.py` × 3 | CNSA **8 741** · ATIH **8 905** · handicap.gouv.fr **93 ⚠ sous 3 000** |
| `curl … --cacert "$CA"` × 7, **verbatim du prompt**, tourniquet par hôte | 3 URL du document **200** · ATIH 2026 **404** (confirmé) · **`cnsa.fr/accompagnement-et-autonomie/serafin-ph` 404** |
| Page rendue, interrogée par fenêtres au navigateur de l'application | `innerText` **4 600 car.** · « 23 mars » **0 occurrence** · nom, titre, présidence, 30 mars, 1er janvier 2027, automne : **tous au littéral** |
| `controle_attributions.py` | **0 bloquant** · **5 passes INERTES** · 1 valeur en D à relire (le 404 déclaré) |
| `controle_decompte.py` · `controle_edition_precedente.py` | `COHÉRENT 3/4` · `OK` sur ①, ①bis (profondeur 4), ② et ③ |
| `controle_noms_propres.py`, **verbatim du prompt** | `NOM NON RETROUVÉ` + `1/3 page NON LUE` — **contredit le `0 non retrouvé` du log** |
| `controle_livrable_du_job.py` (㊳ · ㊳ bis) | run réussi, `exit 0` · `5 testés · 4 retenus · 1 écarté (404×1)`, **aucun 000** |
| `non_regression.sh --docs` | **exit 0**, `0 bloquant(s) (nouveau)`, 49/49 catégories, 771 livrables suivis |
| Balayage du marquage des murs, 126 éditions, 2 formes | resserrée **1 signalement + 6 à ACCEPTER** · naïve **37 dont 36 faux** |
| `WebSearch` « Camille Galliard-Minier … comité stratégique SERAFIN-PH » | fonction et date **corroborées** (en poste depuis le 26/02/2026) · **présidence du 14e comité non corroborée** par la recherche — c'est la page rendue qui l'établit |

### Ce que STANDARD n'a pas interrogé

- **Les quatre engagements du communiqué un par un.** J'ai vérifié les trois qui portent une date ou une échéance ; le quatrième — *« Poursuite des travaux des groupes techniques en 2026 »* — n'a pas été confronté à la page.
- **Le fond SERAFIN-PH lui-même.** Que « modulation de l'activité » et « dotation globale » soient deux composants distincts du modèle est l'état de ma connaissance du dispositif, **pas une mesure** : aucune des trois pages lues ne définit les deux termes côte à côte. Si les deux désignaient la même enveloppe, le premier défaut tomberait — c'est la vérification à faire avant toute correction du document.
- **La page `atih.sante.fr/recueil-national-ph-2026`**, qui rend 404 : la note en conclut *« page non encore publiée »*, ce qui est **une interprétation** — un 404 ne distingue pas une page jamais publiée d'une page déplacée. Aucune recherche d'URL de remplacement n'a été faite.
- ✅ **Les deux URL `handicap.gouv.fr` du log** (`/serafin-ph`, `/comites-strategiques-serafin-ph`) **ont été lues le 20/11/2026** — voir la section « Lecture du 20/11/2026 » ci-dessus. *Libellé du 19/11, conservé : « rendent **200** et n'ont **pas** été lues : si l'une d'elles porte une actualité de la fenêtre 11–18/11, la « semaine creuse » serait à revoir. C'est la vérification la plus rentable pour l'édition suivante. »* — elle l'était, mais pas pour la raison annoncée : **aucune actualité**, et un défaut de l'appareil de test.
- **Ce que les deux interventions ne ferment pas** : la question de fond ci-dessus reste ouverte, et les deux défauts du **log** restent dans le log. Le `.docx` est corrigé le **19/11** et les deux URL du log sont lues le **20/11**. *Libellé du 19/11, conservé : « les deux URL `handicap.gouv.fr` à 200 n'ont toujours pas été lues ».*

## Notes liées

- ⬅️ **Précédente** — [[2026-11-11_veille_SERAFIN-PH.fiche]]
  **elle avait ouvert la route de lecture que cette édition a reperdue, et elle n'en avait pas gardé l'adresse.** Ses six énoncés prouvés au degré ① sur un instantané d'archive (`5 761 car. utiles`) sont exactement ceux que la note du 18/11 reprend de la page murée — et ma lecture de la page rendue les redémontre **tous**, sept jours plus tard, par une troisième route. 🟢 Sa mesure la plus utile tient toujours : le plafond relevé à 5 $ après son dépassement à 101 % rend **64 %** cette semaine. ⚠️ Et son marquage `⚠️ JS` + « 93 car. utiles » était la **forme honnête** que cette édition abandonne
- ➡️ **Suivante** — édition du **mercredi 25/11/2026 à 8h03**
  **quatre vérifications, dont deux neuves.** ① ~~lire les **deux URL `handicap.gouv.fr` du log** qui rendent 200 et que personne n'a ouvertes — une actualité de la fenêtre y invaliderait la semaine creuse~~ → **FAIT le 20/11** : archive de 2017 et **404**, aucune actualité, la semaine creuse tient ; ce qui en reste pour l'édition suivante est de **ne plus citer ces deux adresses** et de savoir qu'un `200` de cet hôte ne prouve rien ; ② la page `atih.sante.fr/recueil-national-ph-2026` est-elle publiée, et si elle reste en 404, **chercher l'URL de remplacement** au lieu de conclure à la non-publication ; ③ 🔴 **ne pas reprendre « la dotation globale »** pour la phase 2 du recueil : la source écrit *« à la modulation de l'activité »* ; ④ si la page du 14e comité est toujours murée, **la marquer `⚠` avec son compte** comme le 11/11, et non `✅`
- 🔗 **Pont** — [[2026-11-16_veille_has-actualite.fiche]]
  **le même mécanisme, nommé là-bas et subi ici : le job relit la note, jamais la fiche.** La route d'archive mesurée le 11/11 était dans une fiche, donc hors de portée de l'édition du 18/11 — et le travail a été refait. 🔗 Et les deux séries partagent la **même cécité au mur** : là-bas une source inerte comptée parmi les `✅ exploitées`, ici un mur à 93 caractères marqué `✅`
- 🔗 **Pont** — [[2026-11-15_veille_imac.fiche]]
  **la variante marchande de la même façade, et elle montre le plancher par l'autre bout.** `hp.com` y rend **40 caractères utiles pour 76 599 octets** et trois prix reposent sur elle. Ici, la page rend **93 caractères à `curl` et 4 600 rendue** : le plancher de 3 000 produit donc un **faux négatif** là où, dans la série iMac, il attrape une vraie façade. **Le même seuil sépare mal deux choses différentes** — une page vide et une page que notre pile ne sait pas exécuter
- 🗂️ **Dossier** — [[SERAFIN-PH_dossier.fiche]]
  à mettre à jour de trois points mesurés : ① **le marquage du mur handicap.gouv.fr oscille** sur cinq éditions — `⚠️ Mur JavaScript` (21/10), `✅ 200` (28/10), `⚠️ JS` (11/11), `✅` sans compte (18/11) — donc la série n'a **pas** de convention stable pour une page qu'elle cite depuis des mois ; ② cette page porte **4 600 caractères** et non 93, ce qui change ce qu'on peut en tirer ; ③ `serafin-ph-veille` n'appelle toujours **ni `controle_attributions.py` ni `controle_decompte.py`** — mesuré sur son prompt, **0 occurrence de chacun** —, et les quatre défauts de cette semaine sont du ressort du premier
