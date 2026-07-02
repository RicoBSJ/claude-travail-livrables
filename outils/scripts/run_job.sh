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
LOG_DIR="$PROJECT/outils/scripts/logs"
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

# ---- Auto-commit + push des livrables produits (option 2) ----
# Portée STRICTE : uniquement les dossiers de livrables générés (veilles + Livrables).
# Jamais "git add -A" → les dossiers personnels sensibles restent hors git.
# sources/veille (récursif) couvre tous les sous-dossiers de veille présents et futurs
# (AI-Act, RGPD, iMac, …) ainsi que les .docx/.md de veille à la racine.
if [ "$EXIT" -eq 0 ]; then
  export GIT_SSH_COMMAND="ssh -i $HOME/.ssh/id_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes -o StrictHostKeyChecking=accept-new"
  git add sources/veille livrables/lecons livrables/quiz livrables/infographies 2>/dev/null
  if git diff --cached --quiet 2>/dev/null; then
    echo "[git] Rien de nouveau à committer." >> "$LOG"
  else
    git -c user.name="Claude (launchd)" -c user.email="claude@local" \
        commit -q -m "chore($JOB_ID): livrables auto $(date +%Y-%m-%d)" >> "$LOG" 2>&1
    # Intègre d'éventuels changements distants avant de pousser (autostash = robuste aux changements parasites)
    git pull --rebase --autostash -q origin main >> "$LOG" 2>&1 || echo "[git] pull --rebase a échoué (on tente quand même le push)" >> "$LOG"
    if git push -q origin main >> "$LOG" 2>&1; then
      echo "[git] ✅ push OK" >> "$LOG"
    else
      echo "[git] ⛔ push ÉCHEC (livrables commités localement, à pousser manuellement)" >> "$LOG"
    fi
  fi
else
  echo "[git] Job en erreur (exit $EXIT) — pas de commit." >> "$LOG"
fi

# Purge des logs de plus de 30 jours
find "$LOG_DIR" -name "*.log" -mtime +30 -delete 2>/dev/null

exit $EXIT
