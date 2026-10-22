---
name: lancer-job
description: Déclenche manuellement et immédiatement un job planifié du projet. Usage : /lancer-job [nom] où nom est : imac, serafin, rbpp, finance, hypnose, astro, stoicisme, ai-act, controle
disable-model-invocation: false
---

# Déclenchement manuel d'un job

L'argument reçu est : $ARGUMENTS

## Étape 1 — Identifier le job demandé

Lis le fichier : /Users/utilisateur/kDrive/Claude_Travail/jobs_config.json

Identifie le job correspondant à l'argument selon cette correspondance :
  Le parcours Revenus passifs était commandé en 10 leçons ; le job en avait produit une 11e.
  N'exécute rien : affiche « ⛔ Le job revenus-passifs-lecon a été supprimé le 04/10/2026 —
  parcours clos à 10 leçons (la 11e, hors feuille de route, est conservée et fichée). » et arrête-toi.
- "imac" ou "mac" ou "apple" ou "imac-m4" ou "imac-m5"               → job id "imac-veille"
- "serafin" ou "serafin-ph" ou "veille"                              → job id "serafin-ph-veille"
- "rbpp" ou "pipeline"                                               → job id "rbpp-pipeline"
- "finance" ou "placement" ou "placement-financier" ou "epargne"     → job id "placement-financier-lecon"
- "hypnose" ou "auto-hypnose" ou "autohypnose"                       → job id "hypnose-lecon"
  Le parcours Développement d'applications avec l'IA était fermé à 12 leçons, toutes livrées
  (bilan le 02/10/2026). N'exécute rien : affiche « ⛔ Le job appli-ia-lecon a été supprimé le
  04/10/2026 — parcours fermé, les 12 leçons et le projet fil rouge sont conservés. » et arrête-toi.
- "stoicisme" ou "lecon-stoicisme" ou "philosophie"                  → job id "stoicisme-lecon"
- "ai-act" ou "aiact" ou "ia-act" ou "reglement-ia"                  → job id "ai-act-veille"
- "controle" ou "qualite" ou "relecture" ou "verif"                  → job id "controle-livrables"

Si l'argument est vide ou non reconnu, affiche la liste des jobs disponibles :
```
Jobs disponibles :
  /lancer-job imac        — Veille marché tout-en-un : iMac M4/M5 + PC Windows (dimanche 8h03)
  /lancer-job serafin     — Veille SERAFIN-PH (mercredi 8h03)
  /lancer-job rbpp        — Pipeline RBPP HAS (lundi 8h30)
  /lancer-job finance     — Leçon Placement financier / éducation (samedi 8h03)
  /lancer-job hypnose     — Leçon Hypnose & auto-hypnose (mardi 9h03)
  /lancer-job astro       — Leçon Astrologie karmique (jeudi 9h33)
  /lancer-job stoicisme   — Leçon Stoïcisme (jeudi 8h03)
  /lancer-job ai-act      — Veille règlement IA européen (vendredi 9h03)
  /lancer-job controle    — Contrôle qualité des livrables de la semaine (dimanche 11h03)
```
Et arrête-toi.

## Étape 2 — Confirmer avant d'exécuter

Affiche :
```
▶️ Déclenchement manuel : [nom du job]
   Livrable attendu     : [champ livrable du job]
   Exécution en cours…
```

## Étape 3 — Exécuter le prompt du job

Exécute intégralement le contenu du champ "prompt" du job identifié.
Ne résume pas, ne raccourcis pas : exécute toutes les étapes du prompt.

## Étape 4 — Confirmer la fin

À la fin de l'exécution, affiche :
```
✅ Job [nom] terminé manuellement.
   Prochain déclenchement automatique : [récurrence du job]
```
