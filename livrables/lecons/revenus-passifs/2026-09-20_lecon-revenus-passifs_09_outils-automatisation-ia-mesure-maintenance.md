---
type: fiche-document
source: 2026-09-20_lecon-revenus-passifs_09_outils-automatisation-ia-mesure-maintenance.docx
date_creation: 2026-09-20
date_lecon: 2026-09-20
parcours: revenus-passifs
numero: 9
statut: parcours-actif
tags:
  - parcours/revenus-passifs
  - registre/perso
  - module/outils
  - outil/zapier
  - outil/make
  - outil/n8n
  - outil/openai-api
  - outil/claude-api
  - outil/google-analytics
  - outil/plausible
  - outil/uptimerobot
  - outil/brevo
  - outil/gumroad
  - concept/unites-de-facturation
  - concept/cout-du-stack
  - theme/arnaques
  - source/amf
  - alerte/corrige-contredit-theorie
  - alerte/lien-mort-mal-declare
  - alerte/corrige
  - correction/2026-09-20
---

# 2026-09-20_lecon-revenus-passifs_09_outils-automatisation-ia-mesure-maintenance

Document source : [[2026-09-20_lecon-revenus-passifs_09_outils-automatisation-ia-mesure-maintenance.docx]]

## Résumé

**Les tarifs recopiés des pages qui se laissent lire sont exacts, et la leçon dit honnêtement ce qu'elle n'a pas pu lire.** Neuf des onze pages répondent 200 à un agent de navigateur, Make répond **403** comme la leçon l'annonce (tarifs obtenus « via WebFetch », vérification renvoyée au lecteur — le bon geste). La grille OpenAI est **exacte ligne à ligne** sur `pricing.md` : gpt-4.1-nano $0,10/$0,40, gpt-4o-mini $0,15/$0,60, gpt-5-mini $0,25/$2,00, gpt-4o $2,50/$10, gpt-5 $1,25/$10 ; Claude aussi — Haiku 4.5 **$1/$5**, Sonnet 5 **$2/$10**, Opus 5 **$5/$25** (la page porte déjà Fable 5.1 à $10/$50, non repris, ce qui est défendable pour un usage « économique »). Gumroad est cité **verbatim** — *« 10 % + $0.50 Per transaction for all sales through your profile or direct links to your customers »* — et le 30 % Discover est là. n8n : *« 20€ /mo, billed annually »*, *« 2.5K workflow executions »*, Business *« 667€ /mo … 40K »*, essai *« 1,000 executions »* ; UptimeRobot : Solo *« Starts at € 108 /y »*, Team *« € 420 /y … ★ Most popular »*, Scale *« € 780 /y »*, 50 moniteurs gratuits, intervalles 5 min / 60 s / 30 s / 15 s ; Zapier : *« 100 tasks /mo »*, *« Two-step Zap workflows »* en gratuit, *« Professional Starting from $19.99 /month »*, *« Pay yearly (Save 33%) »* ; GA4 *« free of charge »*. Brevo : « Starter … à partir de 5 000 emails/mois », « Annuel (−10 %) », « Le plus populaire Standard » sont sur la page — les **prix** (€7, €15, €75,96) sont rendus en JavaScript, invisibles dans le HTML, ils ne se vérifient pas d'ici. L'arithmétique du Challenge est juste au centime : $3,70 de commission, $28,30 net, 20 ventes (20 × 28,30 = 566 ≥ 550), Haiku 1,60 + 2,00 = **$3,60**, surcoût Zapier $10,99 × 12 = **$131,88** soit 4,66 ebooks ; le ROI de l'exercice 3 aussi (1 127 € de coûts, 13 873 € puis 1 873 €, 797/1 873 = 42,6 %). Le cadre déontologique ouvre la leçon, le refus de convertir USD/EUR sans taux sourcé est tenu jusqu'au bout, et le « travail non passif » est nommé sans complaisance. **9 leçons `.docx` = n°09**. Coût **1,78 $** (59 %), 49 tours, 13 min 50 s — **+56 %** sur la leçon 08.

**Le défaut central est un corrigé qui contredit la théorie de sa propre leçon — sur le point que la théorie présentait comme LE piège.** La section 1 explique, en gras, que les unités ne sont pas équivalentes : *« Zapier compte des tâches : chaque action exécutée dans un workflow = 1 tâche »*, *« Make : chaque module = 1 crédit. Un scénario à 4 modules consomme 4 crédits par exécution »*, et conclut *« comparer les prix exige de traduire d'abord vos volumes réels dans chaque unité »*. L'exercice 1 pose un workflow à **3 modules** (email de bienvenue, ajout à une liste, notification), puis le corrigé traduit : *« 50 ventes/mois = 150 crédits Make, **50 tâches Zapier**, 50 exécutions n8n »*. Trois actions par vente font **150 tâches Zapier**, pas 50 — la leçon vient de le dire. Et le plan gratuit Zapier, que le tableau limite à *« workflows 2 étapes max »* (la page : *« Two-step Zap workflows »*), n'accepte pas un workflow à trois modules, quel que soit le volume. Le corrigé conclut pourtant *« Zapier Free ($0) : suffisant — 50 tâches < 100 »*. À 500 ventes, même erreur : *« 500 tâches > 100 → Professional 750 tâches suffit »* — c'est **1 500 tâches**, au-delà du palier Professional 750, il faudrait le palier 2K. La réponse B (« Make Core le moins cher ») reste vraie, mais pour de mauvais chiffres, et la réponse C (« le risque du gratuit Zapier au-delà de 100 ventes ») porte sur un plan qui ne fait pas tourner ce workflow. Le même raccourci traverse le Challenge (*« 20 workflows × 3 modules = 60 crédits »*, en ignorant le module déclencheur que Make compte aussi). Ce parcours a sa règle C1 — *un corrigé qui contredit la théorie de sa propre leçon est un défaut grave* — écrite, datée, et sans test : elle n'a pas tenu.

**Un lien mort déclaré sous une mauvaise raison, et deux attributions sans page.** La ressource Plausible est annoncée *« ⛔ page JS-only, non lue lors de cette exécution »* : `plausible.io/pricing` répond **404** — pas du JavaScript, une page qui n'existe plus (les tarifs sont sur la page d'accueil). Le contrôle ㉘ la laisse passer parce que le ⛔ à côté du libellé vaut déclaration ; mais la leçon invite le lecteur, deux fois, à *« vérifier directement sur le site »* à une adresse qui rend une erreur. Le ⛔ était juste, la raison fausse, et un lecteur qui suit le lien conclut que la leçon ne l'a pas testé — ce qui est le cas : un 404 n'est pas « JS-only ». Côté AMF : *« L'AMF a publié des mises en garde contre les offres frauduleuses liées aux robots de trading et aux formations à l'investissement (source : amf-france.org) »* — la page listée (espace épargnants) ne porte ni « robot », ni « trading », ni « mise en garde » : elle parle d'arnaques par faux articles de presse et de la radiation d'un acteur. Le fait est vraisemblable, la page nommée ne le porte pas, et la passe B-NOM ne le voit pas (« a publié » n'est pas dans ses marqueurs ; le domaine est listé, A est satisfait). Le *« rapport AMF/BVA d'octobre 2024 »* est dit non extrait — honnête, mais c'est un fait de mémoire dans une leçon dont le prompt interdit les faits de mémoire. De même *« n8n a migré ses utilisateurs cloud vers une nouvelle tarification en 2024 »* et *« Zapier a changé sa grille plusieurs fois en 5 ans »* : deux faits d'histoire tarifaire sans aucune page. Et *« Garantie de résultat sur un revenu : illégale en France (art. L121-2) »* — L121-2 définit la pratique commerciale trompeuse ; une garantie de revenu peut en relever, elle n'est pas « illégale » en soi. Plus petit : n8n *« tous les tarifs cloud sont facturés annuellement »* — la page a un bouton *« Monthly / Annually (Save 17%) »* ; les €20 sont le prix en facturation annuelle, pas le seul prix. Et *« 750 tokens ≈ 500 mots en français »* est une règle de pouce sans source.

**Ce qui est bon l'est vraiment, et c'est la partie qui compte pour ce parcours.** L'ancrage réaliste est le meilleur du parcours depuis la leçon 04 : APIs qui changent, prompts à itérer, debugging par incident, dépendance à un tiers, gestion des erreurs à 30-50 % du temps — sans un chiffre de revenu promis. L'exercice 3 démonte l'annonce à 797 € signal par signal, puis fait le calcul dans les deux sens (2 500 €/mois : 13 873 € ; 500 €/mois : 1 873 €, la formation à 43 % du bénéfice) — c'est exactement la pédagogie que le cadre déontologique demande. Le Challenge tient ses deux devises séparées plutôt que d'inventer un taux. À corriger : les tâches Zapier de l'exercice 1 (150 et 1 500, plan gratuit inapplicable à trois étapes), le crédit du déclencheur Make, la ressource Plausible en 404 avec la bonne adresse, la phrase AMF sous une page qui la porte ou sans « source : », les deux faits d'histoire tarifaire, la nuance L121-2, la facturation n8n. À durcir : la règle C1 existe et n'a pas de test qui recompte, dans un corrigé, les unités que la théorie a définies ; et ㉘ accepte un ⛔ comme déclaration de lien mort quelle que soit la raison écrite à côté — « JS-only » n'est pas « 404 ».

**Corrigé le 20/09/2026, journal de huit entrées dans le document.** L'exercice 1 traduit ses volumes dans chaque unité, multiplication écrite (50 × 3 = 150 tâches, 50 × 4 = 200 crédits, 500 × 3 = 1 500), dit que le plan gratuit Zapier ne fait pas tourner un workflow à quatre étapes, que Professional 750 ne suffit pas à 500 ventes, et que Make Free puis Make Core restent les moins chers ; le Challenge compte le module déclencheur (80 crédits) ; le lien Plausible est retargeté vers la page d'accueil, qui porte « $9 /month » et « Up to 10k monthly pageviews » dans le HTML — source primaire, plus secondaire ; la phrase AMF dit ce que la page dit (faux articles de presse, radiations) et le rapport AMF/BVA est dit cité de mémoire ; les deux faits d'histoire tarifaire cèdent la place aux rabais annuels affichés (33 % Zapier, 17 % n8n) ; L121-2 devient « peut relever de la pratique commerciale trompeuse » ; n8n a sa facturation mensuelle ; le ratio tokens/mots est dit non sourcé. Contrôle exit 0. Côté contrôle : **㉘ bis** — un ⛔ seul ne déclare plus un lien mort, il faut le code ou le fait (livrée → INTERDIT, exit 1 ; corrigée → 0 ; témoin ajouté) ; B-NOM lit « a publié / alerte / met en garde » et ignore le développé d'un sigle (livrée → *A RELIRE, absents : frauduleuses, trading* ; corrigée → aucune). Prompt (35 140 → 41 180) : C1 reçoit son cas réel et un test — *un volume d'unité s'écrit avec sa multiplication* (livrée → 2 refusés, corrigée et leçon 08 → OK ; il ne juge pas le facteur) ; B2 bis — un lien mort se déclare par son code ; A2 — un fait prêté à une page est sur cette page, un fait d'histoire sans page ne s'écrit pas. Et cette fiche se corrige elle-même : elle disait que ce prompt n'avait pas de C1 — il en avait une, sans test.

## Notes liées

- **⬅️ Précédente** · [[2026-09-13_lecon-revenus-passifs_08_outils-creation-hebergement-paiement]]
  l'annonce tenue — *« automatisation, IA, mesure, maintenance »* — et les mêmes forces (tarifs recopiés, devises séparées) ; la 08 avait été corrigée sur une source nommée sans lien, celle-ci l'est sur un corrigé qui oublie sa propre unité de compte
- **🔗 Pont** · [[2026-09-06_lecon-revenus-passifs_07_automatisations-no-code-micro-saas-agents-ia]]
  **la leçon qui a introduit Zapier, Make et n8n** ; celle-ci en donne enfin les unités de facturation — et se trompe en les appliquant
- **🔗 Pont** · [[2026-09-19_lecon-placement-financier_15_biais-comportementaux-epargnant]]
  **la règle C1 du parcours placement, durcie hier** — *une justification qui nomme un autre mécanisme que la réponse, c'est deux réponses* — et la C1 de ce parcours, qui existait sans test : le tableau dit « 1 action = 1 tâche », le corrigé compte une tâche par vente
- **🔗 Pont** · [[2026-09-17_lecon-astrologie-karmique_07_saturne-retour-cycle-karma]]
  **le lien mort et sa déclaration** : là-bas un 404 publié comme vivant (d'où ㉘), ici un 404 déclaré ⛔ mais sous la raison « JS-only ». ㉘ voit le ⛔, pas la raison — c'est sa limite, et elle est atteinte trois jours après sa création
- **🔗 Pont** · [[2026-08-16_lecon-revenus-passifs_04_economie-reelle-couts-fiscalite]]
  le baromètre AMF/BVA y était déjà, sourcé après correction ; ici il revient de mémoire, « non extractible », sans la page que la leçon 04 avait fini par lier
