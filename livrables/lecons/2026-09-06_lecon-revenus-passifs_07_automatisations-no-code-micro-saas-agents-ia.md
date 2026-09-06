---
type: fiche-document
source: 2026-09-06_lecon-revenus-passifs_07_automatisations-no-code-micro-saas-agents-ia.docx
date_creation: 2026-09-06
date_lecon: 2026-09-06
parcours: revenus-passifs
numero: 7
statut: parcours-actif
tags:
  - parcours/revenus-passifs
  - registre/perso
  - module/modeles
  - modele/micro-saas
  - modele/no-code
  - modele/ai-wrapper
  - concept/mrr
  - concept/churn
  - theme/arnaques
  - source/amf
  - alerte/corrige
  - correction/2026-09-06
---

# 2026-09-06_lecon-revenus-passifs_07_automatisations-no-code-micro-saas-agents-ia

Document source : [[2026-09-06_lecon-revenus-passifs_07_automatisations-no-code-micro-saas-agents-ia.docx]]

## Résumé

**Sur un sujet où tout invite à vendre du rêve, la leçon fait l'inverse — et c'est ce qu'elle a de plus précieux.** L'avertissement d'ouverture nomme le statut **CIF** et le registre **ORIAS**, puis écrit noir sur blanc que le secteur est *« saturé de promesses trompeuses et de formations creuses »*. Elle tient parole : elle expose les taux d'échec, le travail non passif — support, mises à jour d'API qui cassent les intégrations, marketing, churn, RGPD, cotisations —, et rappelle que *l'automatisation elle-même ne génère pas de revenu*. Deux gestes méritent d'être relevés parce qu'ils sont rares. Le taux d'échec de 90 % des AI wrappers est **donné comme non vérifié** : *« issue de sources secondaires non vérifiées directement pendant cette exécution — ordre de grandeur indicatif, non chiffre officiel »*. Et sur les cotisations micro-entrepreneur, elle **refuse d'écrire un taux** : *« non recopiés depuis une source primaire pendant cette exécution »*. Refuser un chiffre plutôt que l'approximer, c'est le garde-fou A4 appliqué à la lettre.

**Toute l'arithmétique est juste, y compris là où elle pouvait déraper.** J'ai tout refait : le seuil de couverture (19/15 → 2 abonnés), les frais Stripe (0,475 € arrondi à 0,48), la marge à 30 abonnés (416,60 €), et surtout **la table de churn sur six mois** — 3, 6, 8, 10, 12, 14 abonnés, arrondis compris, jusqu'à la marge finale de 184 €. Rien à redire. **7 URL sur 8 répondent 200**, et la huitième est déclarée en 403 dans le texte — `economie.gouv.fr`, que j'ai confirmé. L'exercice 2 est le meilleur du parcours : une fausse offre de formation construite sur des schémas AMF réels, six signaux à retrouver, et surtout les questions à poser avant d'acheter — dont celle qui vaut pour toute promesse chiffrée : *« quel est le revenu **médian** (non moyen) de vos étudiants six mois après la formation ? »*.

**La contradiction 30 % / 70 % cachait pire : la distribution était fabriquée. Corrigé le 06/09/2026**, avec journal. Le texte annonçait une répartition en quatre tranches — 30 % sous 1 000 $/mois, 50 % entre 1 000 et 10 000, 15 % entre 10 000 et 100 000, 5 % au-delà — puis affirmait deux lignes plus bas, **« même source »**, que *70 % gagnent moins de 1 000 $/mois*. J'ai fini par ouvrir la page (elle m'avait rendu un 403 la veille, elle a répondu 200 avec un en-tête navigateur). **Aucune des quatre tranches n'y figure.** La source donne d'autres bornes et d'autres proportions : *« 70 % of micro SaaS businesses generate under $1,000 monthly »*, une *« sustainability zone »* de 1 000 à 5 000 $ que **18 %** seulement atteignent, et **1 à 2 %** au-dessus de 50 000 $. Ce n'était donc pas une discordance entre deux chiffres d'une même page : c'était **une distribution complète inventée puis attribuée nommément à un tiers**, posée à côté d'un chiffre, lui, fidèle. La leçon porte maintenant les valeurs relevées, plus deux repères qu'elle avait omis — 95 % de rentabilité sous 12 mois, et la moyenne de 83 300 $/mois qui ne vaut que pour les *top performers*.

**Le taux d'échec était le titre de l'article, que son propre corps dément — repris le même jour.** La leçon écrivait *« 92 % des micro-SaaS échouent dans les 18 premiers mois »*. C'est mot pour mot le **titre** de la page Rockingweb. Son corps dit autre chose : *« 92% of SaaS startups die within 3 years »*, et *« 45% of all startup failures occur between months 18-24 »*. L'horizon passe de 18 mois à 3 ans, et le chiffre des 18–24 mois n'est pas 92 mais 45. La source se contredit elle-même — c'est le cas type de la famille A —, mais la leçon n'a pas eu à trancher : elle n'a lu que le titre. Le texte corrigé donne les deux chiffres du corps, **dit que le titre les contredit**, et nomme la chaîne réelle (CB Insights, 483 post-mortems, HBR). Reste que ces trois statistiques, qui portent tout l'ancrage réaliste de la leçon, viennent du **blog d'une agence web australienne** dont le métier est de vendre du développement SaaS — la leçon le signale honnêtement, mais rien d'indépendant ne les étaye.

**Deux tarifs affichés sans leur condition — le travers exact que vise le garde-fou A4. Corrigés aussi.** ① **Stripe** : vérifié sur `stripe.com/fr/pricing`, cartes EEE standard **1,5 % + 0,25 €**, exact ; mais la grille compte quatre lignes, pas deux. Le « 2,5 % pour les cartes hors EEE » est le tarif des **cartes britanniques** ; les **internationales** sont à **3,15 %** et les **premium de l'EEE** à **2,8 %**, toutes deux absentes, les deux dernières majorées de 2 % en cas de conversion. La leçon écrivait pourtant elle-même qu'il fallait *« vérifier sur stripe.com/fr/pricing »* : consigne rédigée, pas appliquée. ② **Zapier à 19,99 $** : c'est le montant affiché par défaut, sélecteur sur *« Pay yearly (Save 33%) »* — j'ai vérifié dans le HTML que `checked` porte bien sur `value="year"`. Engagement annuel, donc. **Aucun des deux ne touche l'arithmétique** (les calculs utilisent 1,5 % et Make à 9 $), et c'est précisément ce qui rend le défaut instructif : le lien entre un chiffre et sa source peut céder sans qu'aucun calcul ne bronche.

## Notes liées

- **⬅️ Précédente** · [[2026-08-30_lecon-revenus-passifs_06_placements-etf-dividendes-scpi]]
  la continuité est bien posée et c'est l'un des apports du parcours : la leçon 06 traitait des modèles fondés sur le **capital**, celle-ci de ceux fondés sur la **compétence et le temps**. Deux extrémités du spectre, à comparer plutôt qu'à confondre
- **🔗 Pont** · [[2026-07-26_lecon-revenus-passifs_01_definition-mythes]]
  **le garde-fou A4 de ce parcours est né là** : la leçon 01 annonçait un PFU de 30 % en citant impots.gouv.fr, alors que la même page indiquait 31,4 %. Sept semaines plus tard, la règle tient exactement là où elle a été écrite — la leçon refuse d'écrire un taux de cotisations faute de source primaire — et cède partout où elle n'a pas été écrite : une distribution inventée, un titre pris pour un contenu, deux tarifs commerciaux sans leur condition. **Un garde-fou ne protège que le geste qu'il nomme**
- **🔗 Pont** · [[2026-08-16_lecon-revenus-passifs_04_economie-reelle-couts-fiscalite]]
  la leçon des coûts réels, dont celle-ci est l'application à un modèle précis. Le calcul de rentabilité y trouve sa méthode : charges de plateforme, frais de transaction, puis cotisations sur le **chiffre d'affaires brut** et non sur la marge — rappel que la leçon 07 place au bon endroit
- **🔗 Pont** · [[2026-09-05_lecon-placement-financier_13_etf-gestion-indicielle]]
  **deux jours de suite, la même fracture entre un chiffre et son origine.** Hier, une citation de l'AMF fabriquée à partir d'une page **ouverte**, d'où le chiffre voisin était pourtant tiré fidèlement ; ici, une distribution de revenus fabriquée à côté d'un pourcentage exact de la même page. La règle **A1 bis** écrite hier ne couvre que les citations — or ces deux cas montrent qu'un tableau de chiffres se fabrique exactement comme une citation, et se vérifie de la même façon : ligne à ligne, dans la page réellement récupérée. C'est ce qu'il manque à `revenus-passifs-lecon`, l'un des deux seuls prompts jamais durcis
- **🔗 Pont** · [[2026-09-04_veille_ai-act.fiche]]
  **le point aveugle de la leçon** : un *AI wrapper* mis sur le marché fait de son éditeur un **fournisseur** au sens du règlement IA, pas un simple déployeur. Obligations de transparence de l'article 50, période transitoire au 2 décembre 2026 pour les systèmes génératifs antérieurs au 2 août — rien de tout cela n'est mentionné dans la section « durabilité des modèles »
