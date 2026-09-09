---
type: fiche-document
source: 2026-09-08_lecon-hypnose_13_hypnose-anxiete-gestion-stress.docx
date_creation: 2026-09-08
date_lecon: 2026-09-08
parcours: hypnose
numero: 13
statut: parcours-actif
tags:
  - parcours/hypnose
  - registre/perso
  - module/applications
  - theme/anxiete
  - theme/stress
  - concept/axe-hpa
  - concept/parasympathique
  - source/inserm
  - source/pmc
  - etude/rosendahl-2023
  - etude/fisch-2017
  - theme/citation-fabriquee
  - theme/soft-200
  - theme/rate-limit
  - theme/chiffre-non-source
  - alerte/a-corriger
---

# 2026-09-08_lecon-hypnose_13_hypnose-anxiete-gestion-stress

Document source : [[2026-09-08_lecon-hypnose_13_hypnose-anxiete-gestion-stress.docx]]

## Résumé

**Le cadre de sécurité et la revue Fisch sont irréprochables — c'est ce que la leçon a de plus solide.** L'encadré d'ouverture nomme trois contre-indications précises (trouble anxieux généralisé sévère, trouble panique fréquent, TOC sévère ; trouble dissociatif connu pour les approfondissements ; aggravation en cours de pratique), et le pont pro se ferme deux fois : *« ce n'est pas un outil à transmettre à l'équipe ni à pratiquer sur les personnes accompagnées »*. Surtout, la revue systématique de **Fisch, Brinkhaus & Teut (2017, BMC Complementary and Alternative Medicine, 17:323)** est reprise avec une exactitude parfaite : **9 essais randomisés**, **6 sur 9** avec effets positifs significatifs, et la conclusion citée **mot pour mot**, y compris son anglais un peu bancal — *« due to exploratory designs and high risk of bias, the effectiveness of hypnosis or hypnotherapy in stress reduction remains still unclear »*. Citer contre soi la limite méthodologique de sa meilleure source est le geste le plus difficile de ces relectures, et il est fait ici. La section 5 « Limites importantes » le prolonge honnêtement.

**Mais la leçon met entre guillemets une phrase qui ne figure nulle part dans le rapport qu'elle cite — et cette phrase inverse la prudence de la source.** Elle écrit : *« Il souligne que les risques liés à l'hypnose sont “particulièrement limités” »*, à propos du rapport INSERM 2015. J'ai récupéré le rapport intégral — **213 pages, 517 901 caractères** — et cherché la formule : **absente**. Or le rapport consacre un chapitre entier à la sécurité de l'hypnose, y liste les effets indésirables *« considérés comme rares : céphalées, somnolence, vertiges, anxiété, **création de faux souvenirs** »*, et rapporte que le Dr Daniel Annequin *« évoque les risques de manipulation mentale et rappelle que la pratique de l'hypnose a été plusieurs fois incriminée en Grande-Bretagne et aux États-Unis dans la fabrication de faux souvenirs de traumatismes et d'abus sexuels dans l'enfance »*. La leçon ne se contente donc pas d'inventer une citation : elle lui fait dire à peu près le contraire de ce que la source développe. Sur une leçon d'auto-pratique destinée à quelqu'un qui travaille auprès d'adultes vulnérables, c'est le défaut le plus lourd de la semaine.

**Un second chiffre est attribué à une source qui ne le porte pas.** *« Selon Psychology Today, environ 25 % des individus montreraient une hypnotisabilité faible »* : sur la page citée, **« 25 % » et « 25% » comptent zéro occurrence**. Ce qu'elle dit est qualitatif — *« Not everyone is equally hypnotizable »*, avec des différences de connectivité cérébrale entre répondeurs et non-répondeurs. Le chiffre circule dans la littérature, mais pas là. À quoi s'ajoute une **précision qui déplace l'indication** : la leçon retient de l'INSERM un intérêt *« notamment en anesthésie **péri**-opératoire »*, quand la conclusion du rapport écrit *« en particulier en anesthésie **per**-opératoire ou dans la colopathie fonctionnelle (colon irritable) »*. Un tiret et une lettre séparent deux périmètres cliniques distincts, et la seconde indication nommée dans la même phrase — la colopathie fonctionnelle — disparaît.

**La méta-analyse de référence est mal datée, et ses résultats redistribués.** La leçon cite *« Rosendahl, Alldredge & Haddenhorst (**2024**, Frontiers in Psychology), 14:1330238 »*. La notice Europe PMC donne **2023**, et le DOI lui-même porte l'année : **10.3389/fpsyg.2023.1330238**. Le volume 14 que la leçon indique est d'ailleurs celui de 2023 : la référence se contredit toute seule. Sur le fond, *« 49 méta-analyses portant sur 261 études primaires »* est **exact au mot** (« We included 49 meta-analyses with 261 distinct primary studies »). En revanche les trois puces sur l'anxiété ne se retrouvent pas dans le résumé : les seuils *d ≥ 0,5* et *d ≥ 0,8* y désignent la **distribution de tous les effets rapportés** — 25,4 % moyens, 28,8 % grands, toutes indications confondues — et non les effets anxieux en contexte médical ; et là où la leçon écrit *« effets grands pour les patients atteints de cancer »*, le résumé nomme trois populations, **qui n'incluent pas le cancer** : *« patients experiencing pain, patients undergoing medical procedures, and populations of children/adolescents »*. Réserve honnête : je n'ai lu que le résumé — le texte intégral m'est resté inaccessible, pour la raison qui suit.

**Et cette raison est un défaut structurel du parcours, mais pas celui que j'avais d'abord décrit.** J'ai écrit dans une première version de cette fiche que les deux articles PMC répondaient 200 en servant un mur reCAPTCHA, et que la vérification annoncée par la leçon n'était donc pas reproductible. **C'est faux, et je le corrige.** En reprenant la mesure proprement — dix requêtes, deux articles, cinq passes — le comportement est parfaitement régulier : **la première requête rend l'article** (97 211 puis 61 727 caractères utiles), **toutes les suivantes rendent 167 caractères** de *« Checking your browser — reCAPTCHA »*. PMC ne bloque pas : il limite le débit. La leçon a donc très probablement lu ses deux sources, et son *« effectivement consultées »* est crédible.

**Le risque réel est plus retors, et il vise le garde-fou lui-même.** La règle B2 du prompt impose de tester chaque URL au `curl` avant publication. Sur PMC, **ce test consomme l'accès** : la requête de vérification passe, celle qui suit tombe sur le mur — ou l'inverse, la lecture réussit et le test de contrôle en fin de course voit un **200 franc sur une page de 167 caractères**. Dans les deux cas le code HTTP est identique et ne dit rien. Ce qui distingue l'article du mur n'est pas le statut mais la **taille du texte utile** — et aucun des deux prompts de doctrine ne demande de la mesurer. La voie de contournement, elle, ne consomme rien et ne se heurte à aucun mur : l'**API Europe PMC** rend titre, auteurs, année, volume, DOI et résumé en JSON. C'est par elle que j'ai relevé le 2023 du DOI.

## Notes liées

- **⬅️ Précédente** · [[2026-09-01_lecon-hypnose_12_hypnose-douleur-usages-documentes]]
  la continuité est bien construite : la leçon 12 montrait que l'état hypnotique modifie le traitement cérébral de la douleur par l'attention et les attentes, celle-ci transpose aux mécanismes de l'anxiété. Le parallèle est explicite et les protocoles se recoupent — c'est le chaînage le plus net du parcours
- **🔗 Pont** · [[2026-08-04_lecon-hypnose_08_auto-hypnose-fondations]]
  l'exercice 2 réutilise nommément l'ancrage de lieu sûr de la leçon 8 et les inductions des leçons 5 et 6. Les trois protocoles sont réellement cumulatifs, et le Challenge demande d'en composer un personnel — c'est la pédagogie du parcours à son meilleur, indépendamment des défauts de sourçage
- **🔗 Pont** · [[2026-09-07_lecon-psychopathologie_15_crise-suicidaire-evaluation-risque-conduite]]
  **la règle B3 qui manque ici y a été écrite le 06/09** : un HTTP 200 ne prouve pas qu'on a la page, et la taille du fichier ne dit rien. Le cas de la psychopathologie était `has-sante.fr` servant l'ossature du site ; celui-ci est PMC servant un reCAPTCHA. Le motif est identique, le parcours n'a pas la règle
- **🔗 Pont** · [[2026-09-09_lecon-enneagramme_15_instincts-sous-types]]
  produite le lendemain, elle donne la mesure de l'écart entre deux parcours de doctrine. L'ennéagramme recopie un tableau de 27 cellules sans une erreur et **avertit lui-même** que ses sources ont un intérêt à la validité du modèle. L'hypnose cite parfaitement Fisch — puis fabrique une citation INSERM et un pourcentage. Les deux ont sept règles ; ce qui les sépare est l'endroit où l'attention s'est portée
- **🔗 Pont** · [[2026-09-06_veille_imac.fiche]]
  la citation fabriquée à partir d'une page **absente de la liste testée** — le cas MacRumors du 06/09. Ici c'est un cran plus grave : la page INSERM est bien citée, bien ouverte, et la phrase entre guillemets n'y est pas, ni dans les 213 pages du rapport qu'elle met à disposition. **Une source réellement consultée n'immunise pas contre la citation inventée**
