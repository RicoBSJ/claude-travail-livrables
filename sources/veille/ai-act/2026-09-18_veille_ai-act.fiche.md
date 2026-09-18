---
type: fiche-document
source: 2026-09-18_veille_ai-act.docx
date_creation: 2026-09-18
date_veille: 2026-09-18
veille: ai-act
statut: veille-archive
tags:
  - veille/ai-act
  - registre/pro
  - theme/etat-de-l-union
  - theme/frontier-ai
  - theme/eu-kids-act
  - theme/ia-agentique
  - theme/article-50
  - theme/litteratie-ia
  - theme/digital-omnibus
  - source/commission-europeenne
  - source/iapp
  - source/cnil
  - source/eur-lex
  - alerte/citation-absente-de-la-source
  - alerte/source-primaire-non-lue
  - alerte/a-corriger
---

# 2026-09-18_veille_ai-act

Document source : [[2026-09-18_veille_ai-act.docx]]

## Résumé

**Les faits de la semaine sont justes, datés, et presque tous retrouvés sur leurs pages.** Treize URL retestées avec un agent de navigateur : dix rendent du contenu, la page du Conseil est un vrai 403 à **160 caractères**, la fiche presscorner est une coquille JavaScript (3 882 caractères de squelette), et EUR-Lex répond **202** — c'est un défi AWS WAF, lisible seulement dans un navigateur : ouvert dans le navigateur intégré le 18/09/2026, le règlement **2026/1744** y porte bien *« of 8 July 2026 »*, *« OJ L, 24.7.2026 »*, *« In force »* — la référence héritée du 29/08 tient, et la note la déclare héritée, comme la règle 11 l'exige depuis le 12/09. La chronologie du **Service Desk** est exacte jalon par jalon : *02 Dec 2026 — new prohibitions + Article 50(2) transition*, *02 Aug 2027 — at least one AI regulatory sandbox*, *02 Dec 2027 — Annex III*, *02 Aug 2028 — Annex I*, et le **J-75** est juste. Les trois articles IAPP sont **verbatim** dans leurs titres, leurs signatures (*Alex LaCasse, Staff Writer* ; *Isabelle Roccia, CIPP/E, Managing Director, Europe*) et leurs dates (16, 17, 17 septembre) ; les deux titres MEMBER du 16/09 sont sur la page des actualités, mot pour mot, marqués *ANALYSIS MEMBER*. Le **EU Kids Act** est rendu fidèlement : interdiction sous 13 ans, comptes limités « accessibles seulement via le compte d'un parent » pour 13-14 ans, comptes complets dès 15, **6 %** du chiffre d'affaires mondial, audit indépendant de tout nouveau produit, défilement infini, mécaniques de récompense, notifications nocturnes, solution de vérification d'âge open source *« expected to be released by the end of the year »*. Les **cinq secteurs** et l'échéance de **novembre** sont dans le discours *et* dans les deux articles ; la coopération Canada / Royaume-Uni sur *« model evaluation, verification, early warning, AI security »* aussi. Côté français : dernière actualité CNIL le **26 août** (l'outil de traçabilité des modèles en source ouverte), Q/R du **17 août** qui écrit toujours *« adopté le 24 juillet 2026 »* — la discordance avec EUR-Lex est signalée, comme demandé —, note CNIL/CIANum du **20 juillet**, dernière actualité de la Commission le **31 août**. Le décompte de sources est **cohérent** : 9 = 3 ✅ + 1 primaire non lue + 2 sans nouveauté + 3 bloquées, et c'est ce que la liste contient. Contrôles : `controle_decompte` COHÉRENT, `controle_attributions` **exit 3, 0 bloquant** — les deux pages non lues sont EUR-Lex et le Conseil, exactement celles que la note déclare. Coût **1,57 $** (52 %), 39 tours, 12 min 24 s — **+66 %** sur l'édition du 11/09 (0,94 $), pour une semaine qui avait, il est vrai, trois articles à lire au lieu d'un.

**Le défaut central : trois expressions entre guillemets qu'aucune page ne porte, et une liste de chantiers prêtée à une autrice qui ne l'écrit pas.** *« pacing the frontier »*, attribué à von der Leyen *via* l'IAPP : l'article de LaCasse écrit *« the EU should "pace" innovation »* — un mot, pas trois ; le discours, lui, dit *« To pace the frontier. »* — deux fois, à l'infinitif. C'est une paraphrase présentée comme une citation, et attribuée à une source qui ne la contient pas. *« pacing with them »* (« L'UE doit "pacing with them" ») : **nulle part** — ni dans l'article, ni dans les 48 000 caractères du discours, où « pace with » n'apparaît qu'à propos de la doctrine de défense. *« human-centric »*, prêté à Isabelle Roccia : **absent** de son texte, qui parle de *« value-based digital order »*. Et la phrase *« Trois chantiers législatifs en cours signalés : Digital Omnibus IA (partiellement conclu via 2026/1744…), Cloud and AI Development Act, révision du Cybersecurity Act »* est attribuée à son article, qui **ne nomme aucun des trois** — il nomme le Digital Fairness Act et l'AI Continent Strategy. Ce sont des connaissances de fond, probablement justes, écrites sous la signature d'une page « lue en entier » qui ne les porte pas : la forme exacte des fiches dzogchen, hypnose, stoïcisme et astrologie de cette semaine, sur un job qui, lui, avait la page ouverte. **Le contrôle ne pouvait pas le voir** : la passe B commence à six mots depuis le 13/09, et ces trois citations en font trois, trois et un. Un guillemet sur un mot est une attribution comme une autre ; en dessous de six mots, elle passe sans être cherchée.

**La source primaire était à une adresse, et le job a lu trois commentaires à la place.** La note le dit honnêtement — *« discours primaire identifié (presscorner HTTP 200) mais non lu directement »* — et c'est vrai que la page `presscorner/detail/ov/SPEECH_26_1868` ne rend rien en headless. Mais le presscorner a une API publique : `presscorner/api/documents?reference=SPEECH/26/1868&language=en` répond **200, 51 848 octets**, le discours entier. Y lire trois lignes aurait changé la note : *« CEOs of the most advanced companies tell us that it is time to slow down on the self-recursive models. To pace the frontier »* — la citation exacte, en anglais, à mettre entre guillemets ; *« from 13 until a child turns 15, only mini accounts set up and supervised by parents »* — d'où vient le « 13-15 ans » de la note, que l'IAPP écrit « 13 and 14 » ; *« I will invite the main frontier labs for a discussion on how we can support ongoing industry efforts to pace the frontier »* — l'invitation, telle quelle. Rien de ce que la note dit du discours n'est faux ; tout est de seconde main alors que la première était ouverte, et les deux guillemets fautifs viennent de là. Même mécanique sur **artificialintelligenceact.eu** : la note écrit *« ~314 000 caractères retournés avec agent de navigateur, mais contenu non extractible via WebFetch (HTML brut) … à retenter avec un agent de navigateur »* — elle *a* utilisé l'agent de navigateur, a *reçu* la page (313 980 octets, mesurés ce soir), et n'a pas retiré les balises : il reste **16 376 caractères** de texte lisible, les mêmes que le 12/09, une page d'accueil sans actualité datée entre le 11 et le 18. La conclusion honnête n'était pas « non extractible », c'était « lue, rien dans la fenêtre ». La règle 10 du prompt, écrite le 12/09 pour ce site, demandait l'agent de navigateur ; il a servi à mesurer, pas à lire.

**Ce qui vaut pour un foyer d'hébergement est bien choisi, et proportionné.** La note ne dramatise pas : l'appel sur les modèles frontière est dit sans portée juridique immédiate, le Kids Act sans application directe à un établissement d'adultes, et le vrai signal de la semaine est désigné — l'IA agentique face au RGPD, avec la note CNIL/CIANum du 20/07 comme lecture préalable à tout déploiement d'assistant autonome (planification, comptes rendus, agendas). Les deux obligations actives depuis le 2 août sont rappelées avec leur article — transparence (art. 50) et littératie (art. 4) —, l'inventaire des outils génératifs avant le **2 décembre** (art. 50 §2) est la bonne action à J-75, et la ligne sur les autorités françaises non désignées (« via la CNIL et le DPO ») est reprise du 04/09 sans reculer. Deux réserves : *« mesure de soutien à la littératie »* entre guillemets est une reformulation, le job l'a signalé lui-même — bien — mais l'a laissée ; et l'affirmation *« volet numérique du DDADUE toujours en navette au 18/09/2026 »* n'a de source dans **aucune** des trois éditions qui la portent (04/09, 11/09, 18/09) : elle se recopie de semaine en semaine, ce qui est exactement le mécanisme que la règle 16 d'appli-ia nomme pour `PROJET.md`. À corriger : les trois guillemets (citer le discours à l'API, ou retirer les guillemets), la liste des chantiers sous une source qui les porte ou sans attribution, la conclusion sur artificialintelligenceact.eu ; à durcir : lire le presscorner par son API, extraire le texte d'une page reçue avant de la dire illisible, et sourcer ou dater la ligne DDADUE.

## Notes liées

- **⬅️ Précédente** · [[2026-09-11_veille_ai-act.fiche]]
  la note qui a fixé les deux règles que celle-ci applique — EUR-Lex hérité mais cité, discordance CNIL signalée, « définitivement » proscrit — et celle qui a mesuré artificialintelligenceact.eu à 16 376 caractères lisibles : le même chiffre ce soir, que le job a reçu sans le lire
- **🔗 Pont** · [[2026-08-29_veille_ai-act.fiche]]
  **l'édition qui a établi le règlement 2026/1744 sur EUR-Lex** ; trois semaines plus tard la page est derrière un défi AWS WAF (202) et ne s'ouvre plus que dans un navigateur — vérifié ce soir, la référence tient
- **🗂️ Dossier** · [[AI-Act_dossier.fiche]]
  à compléter de l'API du presscorner (`/api/documents?reference=SPEECH/26/1868&language=en`), seule voie headless vers un discours de la Commission, et du passage du discours sur *« pace the frontier »* comme citation de référence
- **🔗 Pont** · [[2026-09-17_lecon-astrologie-karmique_07_saturne-retour-cycle-karma]]
  **la même famille, hier** : des affirmations exactes prêtées à une page qui ne les porte pas (« d'après les synthèses » qui ne nomment pas Schulman). Ici « human-centric » et trois chantiers législatifs sous la signature de Roccia. Là-bas le contrôle B-FR avait la phrase ; ici B s'arrête à six mots et les trois citations en ont trois, trois et un
- **🔗 Pont** · [[2026-09-18_lecon-appli-ia_08_api-architecture-contrats]]
  **la même matinée, l'autre job** : une chose « non lisible » qu'on n'a pas essayé de lire. Là, une frontière Vite affirmée sans test ; ici un discours « non lu directement » avec son API à portée, et une page reçue à 314 000 octets déclarée non extractible
