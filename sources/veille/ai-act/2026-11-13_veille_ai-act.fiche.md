---
type: fiche-document
source: 2026-11-13_veille_ai-act.docx
date_creation: 2026-11-15
date_veille: 2026-11-13
veille: ai-act
statut: non-corrigee
tags:
  - veille/ai-act
  - registre/perso
  - concept/sommet-dublin
  - concept/digital-fairness-act
  - concept/edpb-admt-recrutement
  - concept/plafond-depasse
  - concept/livrable-sans-controle
  - concept/338-refuse
  - concept/zero-hyperlien
  - concept/5bis-inerte
  - concept/chiffre-contredit-par-la-source
  - concept/traduction-entre-guillemets
  - concept/fils-de-veille-abandonnes
---

# 2026-11-13_veille_ai-act.fiche

Document source : [[2026-11-13_veille_ai-act.docx]]

## Résumé

**Les trois faits marquants sont réels et le bloc EDPB est le mieux étayé de la note : tout ce qu'il affirme est au degré ①.** L'article IAPP du 11/11, lu à **4 799 caractères utiles**, porte littéralement `Article 22`, `Coordinated Enforcement Framework`, `sixth`, `automated decision-making` et `candidate screening tools` — donc la 6ᵉ action coordonnée, l'article 22 RGPD, la décision entièrement automatisée et les outils d'examen de candidatures sont tous sourcés. Le bloc Digital Fairness Act est lui aussi sourcé sur une page lue (**10 125 caractères**) : `Digital Fairness Act`, `dark patterns`, `human customer service`, `Virkkunen` et `6% of` y sont littéraux. Et le jalon du **2 décembre 2026** est confirmé mot pour mot sur la frise officielle : *« Prohibitions, for AI systems generating non-consensual sexual deepfakes and child sexual abuse material, start to apply. Transitional deadline … to comply with **Article 50(2)** »*.

**🔴 Le run est mort sur son plafond, aucun contrôle n'a tourné, ㊳ refuse le document — et il a pourtant été commité.** Mesures du log : `is_error=True`, `subtype=error_max_budget_usd`, `stop_reason=tool_use`, **5,0444 $ pour 5,00 $, soit 101 %**, **78 tours**, 735 476 ms, 1 tentative, exit **1**, et la dernière ligne est `[git] Job en erreur (exit 1) — pas de commit.` Le `.docx` est néanmoins dans `5c5e755`. `controle_livrable_du_job.py` rend **`⛔ REFUSÉ`, exit 1** : *« contrôles tracés dans le log : 0 — AUCUN : ce document n'a été vérifié par personne »*. ✅ **Et le garde a tenu jusqu'au bout de la chaîne** : `HEAD` vaut `e151d86` et `origin/main` vaut `0c27f4e` — **deux commits non publiés**, celui-ci et la note de contrôle du 15/11, tous deux issus de runs morts sur leur plafond. Le document est donc commité mais **pas publié**, et il ne le sera pas tant qu'il ne **déclarera** pas lui-même ① l'échec de son exécution **et** ② sa relecture hors du job — l'exemption est en ET. ⚠️ **Et c'est le troisième dépassement de ce job** après le 16/10 (108 %, qui lui avait valu son passage de 3 à 5 $) : le plafond relevé d'un tiers est de nouveau crevé, et cette fois **pour la plus petite note de la série depuis le 17/10**.

**🔴 Le document a perdu TOUS ses hyperliens, et la conséquence n'est pas cosmétique : son propre contrôle d'étape 5 bis en devient inerte.** Mesuré sur `word/_rels/document.xml.rels` : **24 relations externes le 30/10, 17 le 06/11, 0 le 13/11**. Les huit adresses sont là, mais en **texte ordinaire**. Or `controle_ai_act.py` construit sa liste d'adresses depuis les relations seules — `rels = dict(re.findall(…, z.read("word/_rels/document.xml.rels")…))`, puis `liens(q)` ne lit que les `r:id` des paragraphes — et **neuf de ses sites** en dépendent, dont la variable `urls` tout entière. Mesure hors réseau, la tête du contrôle **extraite** et exécutée sur trois éditions : **30/10 → 18 ¶ porteurs de lien, 11 urls · 06/11 → 15 et 10 · 13/11 → 0 et 0**. Son `exit 0` et son *« OK — … pages reçues lues, … tailles de page mesurées »* sont donc **un vert sur du vide** pour tout ce qui confronte un paragraphe à sa page. Même mécanique pour `controle_noms_propres.py`, qui annonce de lui-même **`0/0 page(s)`**. ⛔ **Et `balayer_adresses.py` est structurellement hors jeu** : il sonde des **cibles de relation**, donc ces huit adresses sont désormais hors de portée de tout balayage, y compris rétrospectif — c'est le prix du décliquage, consigné le 26/10, payé ici sur un document entier.

**🔴 Et le chiffre de tête du bloc DFA est contredit par la seule page qui le porte — 13,7 contre 10,3 milliards d'euros.** La note écrit *« Économies annuelles estimées pour les consommateurs de l'UE : **13,7 milliards €/an** (Commission, IP/26/2407) »*. L'article IAPP, lu, écrit : *« The DFA is estimated to save EU consumers **10.3 billion euros annually** that are lost to hidden fees, unknown digital subscriptions and manipulati… »*. L'écart est de **+33 %**. Et la source que la note invoque pour l'arbitrer — le communiqué `presscorner/detail/en/IP_26_2407` — rend **HTTP 200, 22 235 octets bruts et 40 caractères utiles** : une **façade**, au sens exact du motif du 05/11, donc rien ne peut corroborer le 13,7. ⚠️ **La direction de l'erreur est la plus coûteuse** : un chiffre d'économies surévalué d'un tiers, attribué nominativement à un communiqué de la Commission, sur un document destiné à être relu dans six mois.

**🟡 Et l'amende de 6 % est juste sur son taux et fausse sur sa portée.** La page écrit : *« financial penalties of up to **6% of a company's global profits** in "large-scale cases that have a significant impact on consumers across the Single Market" »*. La note retient *« Amendes pouvant atteindre 6 % des profits mondiaux **annuels** »*, et en fait un mécanisme **général** du règlement. Deux dérives mesurées : l'adjectif `annuels` n'est **pas** sur la page, et surtout la **condition restrictive** — les seuls cas de grande ampleur à impact significatif sur le marché intérieur — disparaît, alors qu'elle est dans la même phrase et entre guillemets sur la page. ✅ Le taux de 6 % et l'assiette « profits » sont, eux, exacts : `6% of` est **①**, et c'est bien `global profits` que la page écrit, non un chiffre d'affaires.

**🟡 Une citation entre guillemets qui est une traduction n'est pas une citation — second cas de la semaine.** La note attribue à la vice-présidente Virkkunen *« moderniser les règles de protection des consommateurs »*. La page la cite ainsi : *« time to **update** consumer protection rules to ensure they remain a strong safety net in the digital world »*. La substance est fidèle, l'attribution est bonne, la **forme** est fautive : le dépôt tient qu'une citation se prouve au degré ①, et un énoncé traduit ne peut pas l'être. `controle_attributions.py` le dit, non bloquant — `B-FR … A RELIRE … traduction ou reformulation ?`. ⚠️ La veille imac du **15/11** porte le même défaut sur *« jusqu'à 2× plus rapide en graphiques … »*. **Deux notes, deux jours, un même défaut de forme : c'est une classe, pas un accident.**

**🔴 Le récapitulatif des noms propres annonce une vérification que rien ne peut reproduire, et il nomme une personne absente de la note.** Il écrit : *« 👤 Noms propres : 3 interrogés · 0 non retrouvés · **0 page(s) non lue(s)** | Arthur Mensch ✅ Euronews · Geoffrey Hinton ✅ Euronews · **Kim van Sparrentak** ✅ IAPP »*. Trois mesures le contredisent. ① `controle_noms_propres.py` rejoué rend **`0/0 page(s)`** et deux `NOM NON RETROUVÉ` sur Mensch et Hinton — non pas parce qu'ils sont faux, mais parce qu'il n'y a **aucune page** à lire. ② La page Euronews, seule source des deux noms **et** du premier fait marquant, rend **0 caractère après trois essais** pour `controle_attributions.py`, et sondée seule aujourd'hui avec le faisceau : **HTTP 406, `curl` exit 0** — un **refus d'automate**, donc la page existe et nous est refusée ; ni morte, ni défaut de notre pile TLS. ③ `Kim van Sparrentak` compte **une seule occurrence dans tout le document : celle-là**. La note déclare donc avoir vérifié un nom qu'elle n'emploie pas. ⚠️ **Et il faut être juste** : le run du 13/11 a pu lire Euronews par `WebSearch`, qui ne passe pas par notre pile — le ✅ était peut-être honnête à l'instant où il a été écrit. Ce qui est certain, c'est que **plus rien dans le dépôt ne peut le re-vérifier**, et que l'affirmation « 0 page non lue » est fausse pour tout outil d'aujourd'hui.

**🟡 Le tableau d'échéances porte une ligne qui contredit la source dont la note dit l'avoir tirée.** Elle écrit *« Dates vérifiées sur le calendrier officiel AI Act Service Desk lors de cette exécution »*, et la frise — **brève mais complète**, 2 860 caractères, ce que la fiche du 06/11 avait déjà mesuré contre le faux positif `FACADE` du balayage du 05/11 — sert bien son tableau entier. Confrontation : le **2 décembre 2026** et le **2 déc. 2027** (`Rules for high-risk AI systems in Annex III apply`) sont **conformes** ; mais la frise date le **02 Aug 2027** de *« Member States should have at least one AI regulatory sandbox per country operational »* et place les règles d'IA à usage général au **02 Aug 2025** (`Rules for general-purpose AI apply`), là où la note écrit *« 2 août 2027 — Application des règles GPAI (art. 51-56) »*. ⚠️ Lecture charitable et plausible : la note vise la mise en conformité des modèles GPAI **mis sur le marché avant** le 2 août 2025, échéance réelle du règlement — mais ce n'est **pas** ce que porte la source invoquée, et l'intitulé est donc à reformuler. ⚠️ Deux autres bornes : la frise liste un **02 Aug 2028** (`Annex I`) que le tableau de la note ne porte pas, et la ligne *« Fév. 2027 — CEN-CENELEC JTC 21 »* repose sur un sigle **④ ABSENT de toutes les pages lues** — il vient du dossier, pas d'une page du jour.

**🔴 Trois fils de veille ont été abandonnés dans cette édition, dont celui que la frise officielle désigne comme déterminant.** Mesuré sur les occurrences : `EDPS` **15 → 0**, `consilium.europa.eu` **4 → 0**, `Omnibus` **6 → 0**. Or la frise du Service Desk ouvre par *« The timeline takes into account the AI Act amendments introduced by **Digital Omnibus on AI** »* et renvoie à lui en note de bas de page — c'est l'amendement qui **conditionne** les dates que la note recopie, et il a disparu alors que **chaque édition depuis le 02/10 le portait** (4, 14, 3, 0, 19, 4, 6, puis 0). ⚠️ **Et l'abandon répond par la disparition à la question posée par la fiche du 06/11**, qui demandait *« si l'EDPS est encore déclaré inaccessible, auquel cas le défaut sera à sa troisième édition consécutive »* : il n'y a pas de troisième occurrence du défaut parce que la **source est sortie de la note**, en emportant les cinq faits ① que cette fiche prescrivait de verser au dossier (autorité de surveillance pour les institutions, réseau des correspondants des 78 organes, revoyure du 23/02/2027, bac à sable art. 57(3)). **Une source qu'on ne sait pas lire et qu'on retire n'est pas une source corrigée.**

**🟡 Le document se contredit sur son propre décompte de sources, et aucun contrôle ne peut l'attraper.** L'en-tête annonce *« Sources : 8 tentées — 3 ✅ exploitées · 4 ⚠️ consultées · 1 ⛔ inaccessible (403, fallback WebSearch) »*, et la ligne finale *« 🔗 Liens : 8 testés · **8 retenus · 0 écarté** (codes : aucun rejet) »* : une source déclarée inaccessible ne peut pas être « retenue sans aucun rejet ». `controle_decompte.py` sort en **exit 2, `LISTE NON RECONNUE`** — la rubrique 🔗 Sources ne porte **aucun symbole par ligne**, seulement `Euronews — « … » → url`, donc il n'y a rien à compter. ⛔ **Et c'est aussi ce qui met le motif « murs lus » du 05/11 hors jeu** : il exige qu'une ligne porte `✅` **et** avoue un compte sous le plancher ; ici aucune ligne ne porte de statut, donc le fait que la frise soit à 2 860 caractères et le communiqué à 40 n'est confessé nulle part. **C'est exactement la borne consignée le 05/11 : il faut que le document AVOUE son compte ; un mur non confessé reste hors de portée.**

**Le volume baisse et le coût monte.** Texte utile des cinq dernières éditions : **7 438 → 16 120 → 18 273 → 11 371 → 5 316** caractères ; paragraphes : **100 (30/10), 107 (06/11), 60 (13/11)**. Le créneau du 13/11 est donc **le plus cher de la série** (101 % d'un plafond relevé à 5 $, 78 tours, `cache-read` 10 597 955) pour **la plus petite note depuis le 17/10**, et pour un document qui a perdu ses liens, trois de ses fils et son décompte lisible. ⚠️ Ce n'est pas un jugement éditorial — angle mort partagé — mais une mesure de rendement, et elle pointe dans la même direction que les 78 tours : le run a dépensé son plafond ailleurs que dans la note.

| Affirmation de la note | Page | Verdict |
|---|---|---|
| `Article 22` · `Coordinated Enforcement Framework` · `sixth` · `automated decision-making` | IAPP EDPB 11/11 | **①** |
| `candidate screening tools` (→ « examen de CV, scoring de candidats ») | IAPP EDPB 11/11 | **①** en substance |
| `Digital Fairness Act` · `dark patterns` · `human customer service` · `Virkkunen` | IAPP DFA 11/11 | **①** |
| `6% of a company's global profits` | IAPP DFA 11/11 | **①** — mais la note ajoute `annuels` et **perd la condition** de grande ampleur |
| « 13,7 milliards €/an » | IAPP DFA 11/11 | **contredit** : la page écrit `10.3 billion euros annually` (+33 %) |
| « moderniser les règles de protection des consommateurs » (Virkkunen) | IAPP DFA 11/11 | la page écrit `update consumer protection rules…` — **traduction**, pas citation |
| « endless scrolling » (→ « scroll infini ») | IAPP DFA 11/11 | **①** en substance, hors guillemets : correct |
| Jalon du **2 décembre 2026** (CSAM, deepfakes, art. 50 §2) | frise Service Desk | **①** mot pour mot |
| « 2 déc. 2027 — annexe III » | frise Service Desk | **①** |
| « 2 août 2027 — règles GPAI (art. 51-56) » | frise Service Desk | **non conforme** : la frise y met le **bac à sable**, et les règles GPAI au 02/08/2025 |
| « Fév. 2027 — CEN-CENELEC JTC 21 » | aucune | **④** — le sigle n'est sur aucune page lue |
| Sommet de Dublin, Arthur Mensch, Geoffrey Hinton | Euronews 13/11 | **non vérifiable** — page **HTTP 406** (refus d'automate), 0 caractère lu |
| « 0 page(s) non lue(s) » (récapitulatif) | — | **faux** pour tout outil d'aujourd'hui : 1 page à 406, 1 façade à 40 caractères |
| « Kim van Sparrentak ✅ IAPP » | — | **1 seule occurrence dans le document** : cette ligne même |
| « 13,7 Md€ … (Commission, IP/26/2407) » | presscorner | **façade** : 200, 22 235 octets, **40 caractères utiles** |

### Requêtes passées

Pages aspirées : les **4** lisibles parmi les 8 citées — IAPP DFA (10 125 car.), IAPP EDPB (4 799), frise Service Desk (2 860), `artificialintelligenceact.eu` (16 210). Aucune n'entre en contexte. Sondes réseau faites **une par une**, 15 s d'intervalle.

| Requête | Verdict |
|---|---|
| `Article 22` · `sixth` · `Coordinated Enforcement Framework` · `automated decision-making` | **①** IAPP EDPB |
| `CV screening` | **④** littéralement, puis fenêtre : `ADMT-driven candidate screening tools` |
| `Digital Fairness Act` · `dark patterns` · `human customer service` · `Virkkunen` · `6% of` | **①** IAPP DFA |
| `6% of annual worldwide profits` | **④** — la page écrit `6% of a company's global profits`, **avec sa condition** |
| `worldwide turnover` | **④** sur toutes les pages : l'assiette est bien les **profits** |
| `13.7 billion` | **④** — fenêtre : `estimated to save EU consumers 10.3 billion euros annually` |
| `modernise consumer protection rules` | **④** — la page écrit `time to update consumer protection rules…` |
| `infinite scroll` | **④** — la page écrit `endless scrolling` |
| `Article 5` · `50(2)` | **①** frise Service Desk |
| `2 December 2026` · `2 August 2027` | **④** littéralement ; fenêtres : le 02/08/2027 est le **bac à sable**, le 02/08/2028 clôt la frise |
| `CEN-CENELEC` · `JTC 21` | **④** sur les quatre pages |
| fenêtre `Aug` sur la frise | frise **complète** servie en 2 860 caractères, ouverte par `amendments introduced by Digital Omnibus on AI` |
| `curl` sur `euronews.com/.../first-ai-summit` | **HTTP 406, exit 0** — refus d'automate, faisceau compris |
| `curl` sur `presscorner/.../IP_26_2407` | **HTTP 200, exit 0** · 22 235 octets · **40 caractères utiles** |
| relations externes de `document.xml.rels`, 3 éditions | **24 → 17 → 0** |
| tête de `controle_ai_act.py` **extraite** et exécutée, 3 éditions | **18/11 → 15/10 → 0/0** ¶ porteurs de lien / urls |
| `edps` · `consilium` · `Omnibus` · `Sparrentak` dans les deux éditions | **15→0 · 4→0 · 6→0 · 0→1** |
| volume de texte des 5 dernières éditions | **7 438 · 16 120 · 18 273 · 11 371 · 5 316** |

⚠️ **Ce qui n'a pas été interrogé** : la page Euronews (406 aux trois essais), le communiqué `IP_26_2407` (façade de 40 caractères), les deux articles IAPP en accès MEMBER que la note déclare elle-même en titres seuls, et `cnil.fr` et `digital-strategy.ec.europa.eu`, listés en sources mais qu'aucune affirmation de la note n'invoque.

## Notes liées

- **⬅️ Précédente** · [[2026-11-06_veille_ai-act.fiche]]
  **elle posait trois questions, et la plus importante est réglée par abandon.** ① La clôture du feedback art. 75c/75d du 9 novembre : la note la coche `✅ Clôturée` mais ne rapporte **aucune synthèse de la Commission** — le fait est daté, pas instruit. ② L'adoption des conclusions EYCS du 19 novembre : légitimement encore devant, portée comme `⚠️ Dans 6 jours`. ③ *« Si l'EDPS est encore déclaré inaccessible, le défaut sera à sa troisième édition consécutive »* : il n'y a pas de troisième occurrence parce que l'**EDPS a disparu de la note**, de 15 mentions à zéro, emportant les cinq faits ① que cette fiche-là prescrivait de verser au dossier. ⚠️ Et sa conclusion s'applique à son tour : *« une correction de fait se transmet, une correction de méthode non — seul un contrôle la transmettrait »*. Ici même la **source** ne s'est pas transmise.
- **➡️ Suivante** · édition du **vendredi 20/11/2026 à 9h03** — quatre points d'emblée : les **conclusions EYCS du 19/11** (adoptées ou non) ; le **2 décembre**, à cinq jours, qui mérite mieux qu'une ligne de tableau ; le retour du **Digital Omnibus**, que la frise officielle désigne comme conditionnant toutes les dates reprises ; et **si les hyperliens reviennent** — sans eux l'étape 5 bis du job est inerte et le balayage d'adresses aveugle. ⚠️ Et le plafond : **101 % de 5,00 $** au créneau du 13/11, troisième dépassement de ce job, avec une marque d'échec posée pour **72 h** qui impose `TOURS_MINI=7`.
- **🔗 Pont** · [[2026-11-15_veille_imac.fiche]]
  **l'autre veille de la semaine, et la comparaison isole ce qui protège un document.** Mêmes symptômes de run : plafond crevé à **101 %**, **0 contrôle tracé**, ㊳ qui refuse. Même défaut de forme : une **citation entre guillemets qui est une traduction**. Mais la note imac a **gardé ses six hyperliens**, et c'est tout ce qui change : ses contrôles mordent — `controle_attributions.py` sort en **exit 1** sur quatre attributions, la passe D désigne cinq chiffres sans page, `controle_noms_propres.py` lit **6 pages**. Ici, **0 lien** : attributions **exit 3**, 5 bis **inerte**, noms propres **0/0 page**. **Le même document, cliquable ou non, est vérifié ou pas du tout — et la version non cliquable est celle qui a été commitée.**
- **🔗 Pont** · [[2026-11-04_veille_SERAFIN-PH.fiche]]
  **elle a mesuré les deux bords du plancher de 3 000 caractères, et cette note les touche tous les deux dans le même document.** D'un côté une **vraie façade** : le communiqué `IP_26_2407` à **40 caractères utiles** pour 22 235 octets bruts, invoqué nominativement pour un chiffre que la seule page lisible démentit. De l'autre une page **brève mais complète** : la frise du Service Desk à 2 860 caractères, que le balayage du 05/11 avait classée `FACADE` à tort et qui sert ici son tableau d'échéances mot pour mot. **Le plancher reste un bon détecteur de murs et un mauvais juge de brièveté**, et la différence entre les deux cas ne se lit qu'en **ouvrant** la page.
- **🗂️ Dossier** · [[AI-Act_dossier.fiche]]
  à mettre à jour sur trois acquis mesurés, et à **protéger** de deux chiffres. À verser : la **6ᵉ action coordonnée de l'EDPB** porte sur l'**article 22 RGPD** appliqué à la décision entièrement automatisée dans le **recrutement** — examen de CV, entretien automatisé, scoring de candidats —, premier cadrage de l'EDPB sur l'ADMT depuis les lignes directrices du groupe de l'article 29 de 2018 ; le **Digital Fairness Act** est une proposition du **11/11/2026** qui révise le règlement de coopération en matière de protection des consommateurs, interdit les dark patterns, impose un service client humain et un opt-out des fonctionnalités addictives, avec des sanctions jusqu'à **6 % des profits mondiaux d'une entreprise** — mais **seulement** dans les *« large-scale cases that have a significant impact on consumers across the Single Market »* ; et le **premier sommet UE consacré à l'IA** s'est tenu à **Dublin le 13/11/2026** en format informel, sans conclusions formelles. ⛔ **À ne PAS verser** : les **13,7 Md€/an** d'économies, que la seule page lisible chiffre à **10,3** ; et le **2 août 2027 pour les règles GPAI**, que la frise officielle date du 02/08/2025 en réservant le 02/08/2027 au bac à sable réglementaire. 📌 Et à y porter comme ligne de méthode : **un document sans hyperlien n'est vérifié par aucun contrôle du dépôt** — c'est le premier de la série, et il faut que ce soit le dernier.
