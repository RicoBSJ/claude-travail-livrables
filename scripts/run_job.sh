#!/bin/bash
# ============================================================
# run_job.sh — Runner launchd pour les jobs planifiés Claude_Travail
# Exécute un job (par son id) en mode Claude Code headless (claude -p),
# même lorsque l'application Claude Code n'est pas ouverte.
#
# Usage : run_job.sh <job_id>
# Appelé par les agents launchd (~/Library/LaunchAgents/com.claudetravail.*.plist)
# ============================================================

# launchd fournit un PATH minimal : on le complète pour trouver claude/node
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

PROJECT="/Users/utilisateur/kDrive/Claude_Travail"
JOB_ID="$1"
LOG_DIR="$PROJECT/scripts/logs"
mkdir -p "$LOG_DIR"
STAMP="$(date +%Y%m%d_%H%M%S)"
LOG="$LOG_DIR/${JOB_ID}_${STAMP}.log"

if [ -z "$JOB_ID" ]; then
  echo "[ERREUR] Aucun job_id fourni. Usage : run_job.sh <job_id>" | tee -a "$LOG"
  exit 1
fi

cd "$PROJECT" || { echo "[ERREUR] Projet introuvable : $PROJECT" >> "$LOG"; exit 1; }

echo "=========================================================" >> "$LOG"
echo ">>> $(date '+%Y-%m-%d %H:%M:%S') — Démarrage du job : $JOB_ID" >> "$LOG"
echo "=========================================================" >> "$LOG"

# Exécution headless : Claude lit jobs_config.json et exécute le job demandé.
# --permission-mode bypassPermissions : pas de prompt interactif (WebFetch/Bash/Write autorisés)
# --add-dir : accès au dossier projet
# --model sonnet : modèle économique pour l'exécution autonome (modifiable)
# --max-budget-usd : plafond de coût de sécurité par exécution
/usr/local/bin/claude -p "Tu es dans le projet Claude_Travail ($PROJECT). Lis le fichier jobs_config.json, trouve le job dont l'id est \"$JOB_ID\", puis exécute INTÉGRALEMENT le contenu de son champ \"prompt\" (toutes les étapes, sans en raccourcir aucune). Respecte la vérification des doublons propre au job. Note : le MCP Chrome n'est pas disponible en mode headless — si une source l'exige, signale-la comme inaccessible (⛔) et continue avec les autres. À la fin, affiche un récapitulatif du livrable produit, ou indique que le job s'est arrêté pour cause de doublon." \
  --permission-mode bypassPermissions \
  --add-dir "$PROJECT" \
  --model sonnet \
  --max-budget-usd 2.00 \
  >> "$LOG" 2>&1

EXIT=$?
echo "" >> "$LOG"
echo "<<< $(date '+%Y-%m-%d %H:%M:%S') — Fin du job $JOB_ID (code de sortie : $EXIT)" >> "$LOG"

# Purge des logs de plus de 30 jours
find "$LOG_DIR" -name "*.log" -mtime +30 -delete 2>/dev/null

exit $EXIT
