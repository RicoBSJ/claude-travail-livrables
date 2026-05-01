---
name: lancer-job
description: Déclenche manuellement et immédiatement un job planifié du projet. Usage : /lancer-job [nom] où nom est : serafin, rbpp, nocode, webapp, agents, mcp
disable-model-invocation: false
---

# Déclenchement manuel d'un job

L'argument reçu est : $ARGUMENTS

## Étape 1 — Identifier le job demandé

Lis le fichier : /Users/utilisateur/kDrive/Claude_Travail/jobs_config.json

Identifie le job correspondant à l'argument selon cette correspondance :
- "serafin" ou "serafin-ph" ou "veille"                              → job id "serafin-ph-veille"
- "rbpp" ou "pipeline"                                               → job id "rbpp-pipeline"
- "nocode" ou "no-code" ou "ia" ou "nocode-ia" ou "lecon-nocode"    → job id "nocode-ia-veille"
- "webapp" ou "web" ou "nextjs" ou "portail"                         → job id "projet-webapp"
- "agents" ou "claude-agents" ou "api" ou "sdk"                      → job id "projet-claude-agents"
- "mcp" ou "mcp-integrations" ou "serveur-mcp"                       → job id "projet-mcp"

Si l'argument est vide ou non reconnu, affiche la liste des jobs disponibles :
```
Jobs disponibles :
  /lancer-job serafin  — Veille SERAFIN-PH (mercredi 8h03)
  /lancer-job rbpp     — Pipeline RBPP HAS (lundi 8h30)
  /lancer-job nocode   — Leçon NO-CODE + IA (vendredi 8h03)
  /lancer-job webapp   — Projet Web App Livrables Next.js (vendredi 8h20)
  /lancer-job agents   — Projet Agents Claude autonomes (vendredi 8h35)
  /lancer-job mcp      — Projet Intégrations MCP (vendredi 8h50)
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
