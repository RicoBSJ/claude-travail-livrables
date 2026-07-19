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

# ---- Authentification headless (jeton longue durée) ----
# Le jeton OAuth du Keychain (login de l'app Claude Code) expire ~chaque semaine et
# NE se rafraîchit PAS en contexte launchd → 401 sur tous les jobs (panne du 09→15/07/2026).
# Solution durable : un jeton LONGUE DURÉE (généré par `claude setup-token`, adossé à
# l'abonnement Pro, sans facturation API), stocké HORS git dans :
#   outils/scripts/claude_auth.env   (gitignoré ; chmod 600)
#   contenu : CLAUDE_CODE_OAUTH_TOKEN=...    (ou, à défaut, ANTHROPIC_API_KEY=...)
AUTH_ENV="$PROJECT/outils/scripts/claude_auth.env"
if [ -f "$AUTH_ENV" ]; then
  set -a; . "$AUTH_ENV"; set +a
  echo "[auth] Jeton longue durée chargé depuis claude_auth.env." >> "$LOG"
fi
if [ -z "$CLAUDE_CODE_OAUTH_TOKEN" ] && [ -z "$ANTHROPIC_API_KEY" ]; then
  echo "[auth] ⚠️ Aucun jeton longue durée (CLAUDE_CODE_OAUTH_TOKEN / ANTHROPIC_API_KEY) : repli sur le jeton Keychain, susceptible d'expirer (401). Générer : 'claude setup-token'." >> "$LOG"
fi

# Exécution headless : Claude lit jobs_config.json et exécute le job demandé.
# --permission-mode bypassPermissions : pas de prompt interactif (WebFetch/Bash/Write autorisés)
# --add-dir : accès au dossier projet
# --model sonnet : modèle économique pour l'exécution autonome (modifiable)
# --max-budget-usd : plafond de coût de sécurité par exécution
#
# Retry : les échecs transitoires (timeout réseau/API, pic de charge au réveil du Mac)
# faisaient perdre tout le créneau — pour un job hebdo, c'était 7 jours de retard.
# On réessaie jusqu'à MAX_ATTEMPTS fois, avec backoff. Un skip pour doublon renvoie
# exit 0 → il n'est jamais retenté ; seul un vrai échec (exit ≠ 0) relance une tentative.
MAX_ATTEMPTS=3
RETRY_DELAYS=(90 180)   # attente (s) avant les tentatives 2 et 3

# Plafond de coût par exécution (modifiable). Défaut 2 $, mais certains jobs
# très lourds en sources (WebFetch + boucles WebSearch de repli) dépassent
# régulièrement ce plafond → claude -p sort en erreur, les 3 tentatives
# échouent et le créneau (hebdo) est perdu. On relève le plafond au cas par cas.
BUDGET_DEFAULT="2.00"
case "$JOB_ID" in
  rgpd-veille)   BUDGET="4.00" ;;   # 7 sources (CNIL×2, EDPB, EDPS…) + repli WebSearch : job le plus coûteux
  ai-act-veille) BUDGET="3.00" ;;   # veille multi-sources également gourmande
  imac-veille)   BUDGET="3.50" ;;   # 10 sources (Apple ×6, 9to5Mac, Fnac/Darty) : a dépassé les 2 $ le 19/07/2026 (sauvé par le retry)
  rbpp-pipeline) BUDGET="4.00" ;;   # peut générer jusqu'à 3 livrables (veille + quiz 100 Q + infographie)
  *)             BUDGET="$BUDGET_DEFAULT" ;;
esac
echo "[budget] Plafond de coût pour $JOB_ID : ${BUDGET} \$" >> "$LOG"

EXIT=1
ATTEMPT=1
while [ "$ATTEMPT" -le "$MAX_ATTEMPTS" ]; do
  echo "--- Tentative $ATTEMPT/$MAX_ATTEMPTS — $(date '+%H:%M:%S') ---" >> "$LOG"
  LOG_MARK=$(wc -l < "$LOG")   # repère : lignes du log AVANT cette tentative (pour scanner sa seule sortie)
  /usr/local/bin/claude -p "Tu es dans le projet Claude_Travail ($PROJECT). Lis le fichier jobs_config.json, trouve le job dont l'id est \"$JOB_ID\", puis exécute INTÉGRALEMENT le contenu de son champ \"prompt\" (toutes les étapes, sans en raccourcir aucune). Respecte la vérification des doublons propre au job. Note : le MCP Chrome n'est pas disponible en mode headless — si une source l'exige, signale-la comme inaccessible (⛔) et continue avec les autres. À la fin, affiche un récapitulatif du livrable produit, ou indique que le job s'est arrêté pour cause de doublon." \
    --permission-mode bypassPermissions \
    --add-dir "$PROJECT" \
    --model sonnet \
    --max-budget-usd "$BUDGET" \
    >> "$LOG" 2>&1
  EXIT=$?

  if [ "$EXIT" -eq 0 ]; then
    [ "$ATTEMPT" -gt 1 ] && echo "[retry] ✅ Succès à la tentative $ATTEMPT." >> "$LOG"
    break
  fi

  # Fail-fast : une erreur d'AUTHENTIFICATION (401 / jeton expiré) n'est PAS transitoire.
  # Réessayer 3× + backoff ne sert à rien (constat de la panne du 09→15/07/2026) → on arrête net.
  # Motif CIBLÉ sur l'échec d'auth du CLI (PAS un simple "401/403" qui pourrait
  # provenir d'un WebFetch de source bloquée — ex. ATIH 403, normal et géré).
  if tail -n +"$((LOG_MARK + 1))" "$LOG" | grep -qiE 'Failed to authenticate|authentication_error|Invalid authentication credentials|OAuth token (has )?expired|Please run.*(login|setup-token)'; then
    echo "[auth] ⛔ Échec d'AUTHENTIFICATION détecté — erreur non transitoire, arrêt des tentatives." >> "$LOG"
    echo "[auth] 👉 Régénérer un jeton : 'claude setup-token', puis le placer dans outils/scripts/claude_auth.env (CLAUDE_CODE_OAUTH_TOKEN=...)." >> "$LOG"
    break
  fi

  # Fail-fast n°2 : limite d'usage du plan atteinte. Elle ne se lève qu'à une heure
  # de réinitialisation donnée (souvent plusieurs heures plus tard) : un backoff de
  # 90s/180s n'y changera rien. Constaté le 19/07/2026 sur hypnose-lecon (3 tentatives
  # perdues, dimanche empilant 4 jobs de 7h03 à 9h03).
  if tail -n +"$((LOG_MARK + 1))" "$LOG" | grep -qiE "hit your limit|usage limit|quota exceeded"; then
    RESET_LINE="$(tail -n +"$((LOG_MARK + 1))" "$LOG" | grep -iE "hit your limit|usage limit|quota exceeded" | head -1)"
    echo "[limit] ⛔ LIMITE D'USAGE atteinte — arrêt des tentatives (le backoff ne peut pas la lever)." >> "$LOG"
    echo "[limit] 👉 $RESET_LINE" >> "$LOG"
    echo "[limit] 👉 Rejouer après réinitialisation : bash outils/scripts/rattrapage_jobs.sh $JOB_ID" >> "$LOG"
    break
  fi

  echo "[retry] ⚠️ Tentative $ATTEMPT échouée (exit $EXIT)." >> "$LOG"
  if [ "$ATTEMPT" -lt "$MAX_ATTEMPTS" ]; then
    DELAY="${RETRY_DELAYS[$((ATTEMPT - 1))]}"
    echo "[retry] ⏳ Nouvelle tentative dans ${DELAY}s…" >> "$LOG"
    sleep "$DELAY"
  fi
  ATTEMPT=$((ATTEMPT + 1))
done

echo "" >> "$LOG"
echo "<<< $(date '+%Y-%m-%d %H:%M:%S') — Fin du job $JOB_ID (code de sortie : $EXIT, tentatives : $((ATTEMPT > MAX_ATTEMPTS ? MAX_ATTEMPTS : ATTEMPT)))" >> "$LOG"

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

    # Intègre d'éventuels changements distants avant de pousser (autostash = robuste aux changements parasites).
    # Si le rebase échoue (vrai conflit de contenu), il laisse le dépôt en état "mid-rebase" :
    # sans --abort, TOUS les jobs suivants héritent du blocage et empilent leurs commits en local.
    # On abandonne donc proprement le rebase raté avant de tenter le push (le commit local est préservé).
    if ! git pull --rebase --autostash -q origin main >> "$LOG" 2>&1; then
      echo "[git] ⚠️ pull --rebase a échoué — abandon du rebase (git rebase --abort) pour ne pas bloquer les jobs suivants." >> "$LOG"
      git rebase --abort >> "$LOG" 2>&1
    fi

    # Push avec retries réseau (backoff), pour absorber les coupures transitoires au réveil du Mac.
    PUSH_OK=0
    for PUSH_TRY in 1 2 3; do
      if git push -q origin main >> "$LOG" 2>&1; then
        echo "[git] ✅ push OK (tentative $PUSH_TRY)" >> "$LOG"
        PUSH_OK=1
        break
      fi
      echo "[git] ⚠️ push tentative $PUSH_TRY échouée." >> "$LOG"
      [ "$PUSH_TRY" -lt 3 ] && sleep $((PUSH_TRY * 15))
    done

    if [ "$PUSH_OK" -ne 1 ]; then
      # Alerte explicite : des commits sont bloqués en local et ne sont PAS sur origin.
      AHEAD="$(git rev-list --count origin/main..HEAD 2>/dev/null || echo '?')"
      echo "[git] ⛔ push ÉCHEC après 3 tentatives — $AHEAD commit(s) en avance sur origin/main, à pousser manuellement (git push origin main)." >> "$LOG"
    fi
  fi
else
  echo "[git] Job en erreur (exit $EXIT) — pas de commit." >> "$LOG"
fi

# Purge des logs de plus de 30 jours
find "$LOG_DIR" -name "*.log" -mtime +30 -delete 2>/dev/null

exit $EXIT
