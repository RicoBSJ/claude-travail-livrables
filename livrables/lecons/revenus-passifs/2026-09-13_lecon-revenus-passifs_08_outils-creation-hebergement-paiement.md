---
type: fiche-document
source: 2026-09-13_lecon-revenus-passifs_08_outils-creation-hebergement-paiement.docx
date_creation: 2026-09-13
date_lecon: 2026-09-13
parcours: revenus-passifs
numero: 8
statut: parcours-actif
tags:
  - parcours/revenus-passifs
  - registre/perso
  - module/outils
  - outil/stripe
  - outil/gumroad
  - outil/lemonsqueezy
  - outil/ghost
  - outil/substack
  - outil/ovh
  - outil/wordpress-com
  - outil/brevo
  - concept/merchant-of-record
  - concept/prix-appel-vs-renouvellement
  - theme/arnaques
  - source/amf
  - alerte/corrige
  - correction/2026-09-13
  - theme/source-non-citee
---

# 2026-09-13_lecon-revenus-passifs_08_outils-creation-hebergement-paiement

Document source : [[2026-09-13_lecon-revenus-passifs_08_outils-creation-hebergement-paiement.docx]]

## Résumé

**Une leçon de tarifs, et tous les tarifs sont justes — c'est la première du parcours dont je peux l'écrire sans réserve.** Neuf pages de prix ouvertes à la main le 13/09 avec un en-tête navigateur, neuf fois le chiffre de la leçon est sur la page : Stripe **1,5 % + 0,25 €** pour les cartes standard de l'EEE (la leçon se limite cette fois à la ligne qu'elle utilise, leçon retenue du 06/09) ; Gumroad **10 % + 0,50 $** en direct, **30 %** via Discover, *Merchant of Record* **depuis le 1er janvier 2025** — mot pour mot sur la page ; Lemon Squeezy **5 % + 50¢** et email gratuit **jusqu'à 500 abonnés** ; Ghost(Pro) **18 / 29 / 199 $** facturés à l'année, *« No payment fees »* verbatim, 1 000 membres ; Substack *« Writers keep 90% of their revenue minus credit card fees »* — la leçon en tire « 10 % + frais CB », fidèlement ; OVH Starter **1,59 € HT promo, 2,59 € au renouvellement**, Perso **2,99 / 5,99** ; WordPress.com Premium **18 € mensuel, 8 € annuel** ; Brevo gratuit, Starter **dès 5 000 emails/mois**, **−10 %** à l'année ; AMF *« Listes noires des acteurs non autorisés »* et l'alerte sur les *« arnaques prenant la forme de faux articles de presse »*, toutes deux sur la page. Le cadre déontologique est là (CIF, ORIAS, « les tarifs peuvent changer »), les dates de lecture sont dans le texte, et la leçon tient ce qu'elle annonçait le 06/09 : *création, hébergement, paiement, distribution*, 8/10.

**L'idée forte est la bonne : le prix affiché n'est pas le prix payé.** La section « ancrage réaliste » fait exactement ce que le garde-fou A7 du parcours demande depuis la leçon 07 — un prix commercial s'écrit avec sa condition : OVH +63 % après la première année (la leçon écrit 62 %, c'est 2,59/1,59 = 1,629 — arrondi vers le bas, un point de trop peu), WordPress.com **+125 %** sans engagement, exact. La notion de *Merchant of Record* est bien posée — c'est la plateforme qui porte la TVA mondiale, d'où une commission plus haute qu'un processeur nu — et l'arbitrage final est honnête : *« il n'existe pas de solution universellement meilleure »*. Le paragraphe sur la franchise en base de TVA reste sans source et se termine par « à vérifier avec un comptable ou service-public.fr » : c'est une consigne, pas une affirmation, et c'est le bon réflexe sur un point que la leçon ne maîtrise pas.

**L'arithmétique est juste au centime, sauf là où la leçon oublie sa propre leçon.** Refait ligne à ligne : le tableau à 97 € (Stripe 1,71 → 95,29 ; Discover 29,10 → 67,90), l'exercice 1 (25,63 · 28,32 · 27,08 ; 2,99/1,24 = 2,41 → 3 ventes), le challenge (2,37 € par vente, 47,40 et 237 ; 56,49 en Stripe + OVH). Trois accrocs. ① Le tableau annonce *« 1 $ ≈ 0,93 € »* en note, puis calcule avec 0,50 € : Lemon Squeezy fait 5,315 € (écrit 5,35), Gumroad 10,165 € (écrit 10,20) — trois centimes, mais la note et les chiffres ne disent pas la même chose, alors que l'exercice 1, lui, applique bien 0,47 €. ② **L'exercice 1c calcule le seuil de rentabilité avec OVH Perso à 2,99 € — le prix promo de la première année — deux paragraphes après avoir expliqué que le renouvellement est à 5,99 €.** Avec le prix de renouvellement, le seuil passe de 3 à **5 ventes par mois** (5,99/1,24 = 4,83). C'est le cas type de la famille C : un corrigé qui contredit la théorie de sa propre leçon. ③ Le challenge annonce un seuil de bascule *« autour de 3-4 ventes/mois (comme calculé en exercice 1) »* — mais ses propres nombres donnent autre chose : à 19 €, l'économie Stripe est de 1,835 € par vente, soit **2 ventes** en promo (2,99/1,835 = 1,63) et **4** au renouvellement ; « 3 » était le seuil d'un autre produit à un autre prix face à une autre plateforme.

**Le défaut qui a retenu la leçon à la porte : Mailchimp, décrit sans avoir été lu, et nommé sans lien.** *« Les plans sont similaires (Free, Essentials, Standard, Premium)… Donnée de prix non lue sur la page lors de cette exécution — vérifier directement sur mailchimp.com/pricing. »* La page répond **200 et 38 230 caractères utiles** à un navigateur, et porte bien les quatre plans — la description est exacte, mais elle vient de la mémoire du modèle, pas de la page, et la page n'est pas dans les ressources. Le hook `pre-push` installé la veille a fait son premier arrêt réel : **1 bloquant, « nouveau », push refusé trois fois**, `run_job.sh` a écrit « à pousser manuellement ». Effet collatéral prévu et à connaître : la veille iMac du même matin, **conforme** (0 bloquant, décompte cohérent), est retenue avec elle — un push porte la branche, pas un document. Deux commits en avance sur `origin`, rien de publié ce dimanche.

**Corrigé le 13/09/2026, journal dans le document — et la leçon peut être publiée.** Mailchimp lu, daté, lié et ajouté aux ressources ; l'exercice 1c donne les deux seuils (3 la première année, **5** au renouvellement) et dit lequel compte ; le challenge recalcule avec ses propres nombres (2 ventes en promo, 4 au renouvellement) au lieu de recopier « 3-4 » ; le tableau applique le 0,93 qu'il annonce (5,32 · 10,17), OVH passe à +63 %. Contrôle rejoué : 0 bloquant, `--docs` conforme. Le prompt reçoit quatre règles, chacune avec ce cas : **B4** une page décrite est une page ouverte, une page nommée est une page liée — avec le contrôle commun en test, le même que le pre-push ; **C2** un prix promo ne fonde pas un calcul quand la leçon a donné le renouvellement ; **C3** un seuil ne se recopie pas d'un exercice à l'autre ; **E4** chaque « ≈ » se recalcule par une commande — la règle que placement-financier avait reçue la veille pour la même faute.

**Ce que le contrôle a vu, ce qu'il n'a pas vu.** `controle_attributions.py` : A a mordu (Mailchimp), C2 a validé les trois tarifs OVH et le 125 % sur leurs pages, B, C et D inertes — pas de citation anglaise de huit mots (« No payment fees » en fait deux), pas de version. Il n'a pas vu les trois accrocs d'arithmétique, hors de son périmètre : c'est la relecture qui les tient, et c'est la règle E bis de `placement-financier` (recalculer chaque « ≈ » par une commande) qui manque à ce parcours. Coût du job : **1,14 $** (38 % du plafond), 54 tours, 400 secondes.

## Notes liées

- **⬅️ Précédente** · [[2026-09-06_lecon-revenus-passifs_07_automatisations-no-code-micro-saas-agents-ia]]
  l'annonce tenue mot pour mot — *« création de contenu, hébergement, paiement, distribution »* — et un progrès mesurable : la leçon 07 avait dû être corrigée sur deux tarifs sans condition et une grille Stripe tronquée ; la 08 écrit chaque prix avec sa condition et ne cite de Stripe que la ligne qu'elle utilise. Le garde-fou A7 a tenu là où il a été écrit
- **🔗 Pont** · [[2026-08-16_lecon-revenus-passifs_04_economie-reelle-couts-fiscalite]]
  la leçon des coûts réels, dont celle-ci est la mise en œuvre outil par outil ; c'est aussi la leçon 04 qui a reçu hier deux sources liées et un chiffre défait (kiwezo/thunderbit) — même famille de défaut que Mailchimp ici : une source décrite de mémoire, nommée sans page
- **🔗 Pont** · [[2026-09-13_veille_imac.fiche]]
  conforme au contrôle, et pourtant non publiée : retenue sur la même branche par le refus de cette leçon. Premier cas concret de ce que le hook coûte — à garder en tête si l'on veut un jour découpler les jobs
- **🔗 Pont** · [[2026-09-12_lecon-placement-financier_14_gestion-libre-pilotee-mandat-arbitrage]]
  le parcours voisin a reçu le 12/09 la règle E bis — *chaque « ≈ » se recalcule par une commande* — après un facteur arrondi avant d'être multiplié. Les trois accrocs d'arithmétique de cette leçon (0,93 annoncé et 0,50 appliqué ; promo au lieu du renouvellement ; « 3-4 » pour 2) sont exactement de cette famille, et `revenus-passifs-lecon` n'a pas cette règle
