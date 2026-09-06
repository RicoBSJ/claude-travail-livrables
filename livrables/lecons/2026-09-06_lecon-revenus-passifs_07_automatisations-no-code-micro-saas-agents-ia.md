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
  - alerte/a-corriger
---

# 2026-09-06_lecon-revenus-passifs_07_automatisations-no-code-micro-saas-agents-ia

Document source : [[2026-09-06_lecon-revenus-passifs_07_automatisations-no-code-micro-saas-agents-ia.docx]]

## Résumé

**Sur un sujet où tout invite à vendre du rêve, la leçon fait l'inverse — et c'est ce qu'elle a de plus précieux.** L'avertissement d'ouverture nomme le statut **CIF** et le registre **ORIAS**, puis écrit noir sur blanc que le secteur est *« saturé de promesses trompeuses et de formations creuses »*. Elle tient parole : elle expose les taux d'échec, le travail non passif — support, mises à jour d'API qui cassent les intégrations, marketing, churn, RGPD, cotisations —, et rappelle que *l'automatisation elle-même ne génère pas de revenu*. Deux gestes méritent d'être relevés parce qu'ils sont rares. Le taux d'échec de 90 % des AI wrappers est **donné comme non vérifié** : *« issue de sources secondaires non vérifiées directement pendant cette exécution — ordre de grandeur indicatif, non chiffre officiel »*. Et sur les cotisations micro-entrepreneur, elle **refuse d'écrire un taux** : *« non recopiés depuis une source primaire pendant cette exécution »*. Refuser un chiffre plutôt que l'approximer, c'est le garde-fou A4 appliqué à la lettre.

**Toute l'arithmétique est juste, y compris là où elle pouvait déraper.** J'ai tout refait : le seuil de couverture (19/15 → 2 abonnés), les frais Stripe (0,475 € arrondi à 0,48), la marge à 30 abonnés (416,60 €), et surtout **la table de churn sur six mois** — 3, 6, 8, 10, 12, 14 abonnés, arrondis compris, jusqu'à la marge finale de 184 €. Rien à redire. **7 URL sur 8 répondent 200**, et la huitième est déclarée en 403 dans le texte — `economie.gouv.fr`, que j'ai confirmé. L'exercice 2 est le meilleur du parcours : une fausse offre de formation construite sur des schémas AMF réels, six signaux à retrouver, et surtout les questions à poser avant d'acheter — dont celle qui vaut pour toute promesse chiffrée : *« quel est le revenu **médian** (non moyen) de vos étudiants six mois après la formation ? »*.

**Deux chiffres de la même source se contredisent, et personne ne l'a vu.** La distribution des revenus est donnée comme : 30 % n'atteignent jamais 1 000 $/mois, 50 % plafonnent entre 1 000 et 10 000, 15 % entre 10 000 et 100 000, 5 % au-delà — total 100 %. La ligne suivante affirme, **« même source »**, que *70 % des micro-SaaS gagnent moins de 1 000 $/mois*. Les deux ne peuvent pas être vrais : la distribution ne place que **30 %** sous ce seuil. Je n'ai pas pu trancher — la page de Rockingweb répond 200 au `curl` mais **403 au fetch**, je ne l'ai donc pas ouverte et je ne dis pas laquelle des deux est fidèle. Mais la contradiction se voit sans la source, à deux lignes d'écart. À quoi s'ajoute que ces deux statistiques, qui structurent tout l'ancrage réaliste de la leçon, reposent sur **le blog d'une agence web australienne** — la leçon le signale honnêtement (*« source secondaire […] non un organisme officiel »*), mais rien d'autre ne les étaye.

**Deux tarifs affichés sans leur condition — le travers exact que le garde-fou A4 vise.** ① **Stripe.** J'ai vérifié sur la source primaire, `stripe.com/fr/pricing` : cartes EEE standard **1,5 % + 0,25 €**, exact ; mais la grille en compte quatre lignes, pas deux. La leçon donne « 2,5 % + 0,25 € pour les cartes hors EEE » — c'est le tarif des **cartes britanniques** ; les cartes **internationales** sont à **3,15 %**, et les cartes **premium de l'EEE** à **2,8 %**, toutes deux absentes. La leçon écrit pourtant elle-même qu'il faut *« vérifier sur stripe.com/fr/pricing »* : elle a rédigé la consigne sans l'appliquer. Le calcul de l'exercice 3 utilise 1,5 %, le bon taux — l'arithmétique n'est pas touchée. ② **Zapier à 19,99 $/mois** est le tarif **en facturation annuelle** ; en mensuel, c'est 29,99 $. Sans impact non plus, l'exercice utilisant Make à 9 $.

## Notes liées

- **⬅️ Précédente** · [[2026-08-30_lecon-revenus-passifs_06_placements-etf-dividendes-scpi]]
  la continuité est bien posée et c'est l'un des apports du parcours : la leçon 06 traitait des modèles fondés sur le **capital**, celle-ci de ceux fondés sur la **compétence et le temps**. Deux extrémités du spectre, à comparer plutôt qu'à confondre
- **🔗 Pont** · [[2026-07-26_lecon-revenus-passifs_01_definition-mythes]]
  **le garde-fou A4 de ce parcours est né là** : la leçon 01 annonçait un PFU de 30 % en citant impots.gouv.fr, alors que la même page indiquait 31,4 %. Sept semaines plus tard, la leçon refuse d'écrire un taux de cotisations qu'elle n'a pas lu à la source — mais publie deux tarifs commerciaux sans leur condition d'application
- **🔗 Pont** · [[2026-08-16_lecon-revenus-passifs_04_economie-reelle-couts-fiscalite]]
  la leçon des coûts réels, dont celle-ci est l'application à un modèle précis. Le calcul de rentabilité y trouve sa méthode : charges de plateforme, frais de transaction, puis cotisations sur le **chiffre d'affaires brut** et non sur la marge — rappel que la leçon 07 place au bon endroit
- **🔗 Pont** · [[2026-09-05_lecon-placement-financier_13_etf-gestion-indicielle]]
  **deux jours de suite, deux façons opposées de traiter un chiffre commercial.** Hier, un taux repris d'une source secondaire sans vérification et une citation fabriquée à partir d'une page ouverte ; ici, une donnée explicitement refusée faute de source primaire — et, dans la même leçon, deux tarifs publiés sans leur condition. La règle A1 bis écrite hier ne couvre que les citations : les grilles tarifaires restent à vérifier ligne à ligne
- **🔗 Pont** · [[2026-09-04_veille_ai-act.fiche]]
  **le point aveugle de la leçon** : un *AI wrapper* mis sur le marché fait de son éditeur un **fournisseur** au sens du règlement IA, pas un simple déployeur. Obligations de transparence de l'article 50, période transitoire au 2 décembre 2026 pour les systèmes génératifs antérieurs au 2 août — rien de tout cela n'est mentionné dans la section « durabilité des modèles »
