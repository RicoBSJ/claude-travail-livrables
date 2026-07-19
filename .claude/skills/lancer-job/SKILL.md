---
name: lancer-job
description: Déclenche manuellement et immédiatement un job planifié du projet. Usage : /lancer-job [nom] où nom est : ai-act, rgpd, imac, serafin, rbpp, dzogchen, psychopathologie, finance, hypnose, enneagramme, em, nocode, stoicisme
disable-model-invocation: false
---

# Déclenchement manuel d'un job

L'argument reçu est : $ARGUMENTS

## Étape 1 — Identifier le job demandé

Lis le fichier : /Users/utilisateur/kDrive/Claude_Travail/jobs_config.json

Identifie le job correspondant à l'argument selon cette correspondance :
- "ai-act" ou "aiact" ou "ia-act" ou "reglement-ia"                  → job id "ai-act-veille"
- "rgpd" ou "gdpr" ou "donnees-personnelles" ou "cnil"               → job id "rgpd-veille"
- "imac" ou "mac" ou "apple" ou "imac-m4" ou "imac-m5"               → job id "imac-veille"
- "serafin" ou "serafin-ph" ou "veille"                              → job id "serafin-ph-veille"
- "rbpp" ou "pipeline"                                               → job id "rbpp-pipeline"
- "dzogchen" ou "lecon-dzogchen" ou "bouddhisme"                     → job id "dzogchen-lecon"
- "psychopathologie" ou "psychopatho" ou "psycho" ou "clinique"      → job id "psychopathologie-lecon"
- "finance" ou "placement" ou "placement-financier" ou "epargne"     → job id "placement-financier-lecon"
- "hypnose" ou "auto-hypnose" ou "autohypnose"                       → job id "hypnose-lecon"
- "enneagramme" ou "lecon-enneagramme" ou "personnalite"             → job id "enneagramme-lecon"
- "em" ou "entretien-motivationnel" ou "motivation" ou "motivationnel" → job id "entretien-motivationnel-lecon"
- "nocode" ou "no-code" ou "ia" ou "nocode-ia" ou "lecon-nocode"    → job id "nocode-ia-veille"
- "stoicisme" ou "lecon-stoicisme" ou "philosophie"                  → job id "stoicisme-lecon"

Si l'argument est vide ou non reconnu, affiche la liste des jobs disponibles :
```
Jobs disponibles :
  /lancer-job ai-act      — Veille AI Act (dimanche 7h03)
  /lancer-job rgpd        — Veille RGPD (dimanche 7h33)
  /lancer-job imac        — Veille marché tout-en-un : iMac M4/M5 + PC Windows (dimanche 8h03)
  /lancer-job serafin     — Veille SERAFIN-PH (mercredi 8h03)
  /lancer-job rbpp        — Pipeline RBPP HAS (lundi 8h30)
  /lancer-job dzogchen    — Leçon Dzogchen (mardi 8h03)
  /lancer-job psychopathologie — Leçon Psychopathologie clinique (lundi 8h03)
  /lancer-job finance     — Leçon Placement financier / éducation (samedi 8h03)
  /lancer-job hypnose     — Leçon Hypnose & auto-hypnose (mardi 9h03)
  /lancer-job enneagramme — Leçon Ennéagramme (mercredi 9h03)
  /lancer-job em          — Leçon Entretien Motivationnel (jeudi 9h33)
  /lancer-job nocode      — Leçon NO-CODE + IA (vendredi 8h03)
  /lancer-job stoicisme   — Leçon Stoïcisme (jeudi 8h03)
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
