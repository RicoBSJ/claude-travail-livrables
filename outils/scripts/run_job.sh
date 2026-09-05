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
  imac-veille)   BUDGET="3.50" ;;   # 10 sources (Apple ×6, 9to5Mac, Fnac/Darty) : a dépassé les 2 $ le 19/07/2026 (sauvé par le retry)
  rbpp-pipeline) BUDGET="4.00" ;;   # peut générer jusqu'à 3 livrables (veille + quiz 100 Q + infographie)
  controle-livrables) BUDGET="4.00" ;;   # contrôle toute la semaine : nombreux curl + remontées aux sources primaires
  astrologie-karmique-lecon) BUDGET="3.00" ;;   # deux régimes de sources à croiser (astronomie institutionnelle + corpus) ; a dépassé les 2 $ le 27/08/2026 après le durcissement du prompt du 20/08
  ai-act-veille) BUDGET="3.00" ;;   # 7 sources socle + textes EUR-Lex + curl de chaque lien ; la note du 29/08 comptait 14 URL pour 20 Ko
  placement-financier-lecon) BUDGET="3.00" ;;   # relevé le 05/09/2026 : la règle A1 bis ajoutée le même jour impose de rechercher littéralement chaque citation dans le texte récupéré, en plus du garde-fou fiscal A3 à quatre niveaux (source primaire, agrégateur ≠ autorité, régimes dérogatoires, valeurs révisées) qui fait déjà de ce parcours l'un des plus coûteux en vérifications
  appli-ia-lecon) BUDGET="3.00" ;;      # relevé le 04/09/2026 : job le plus lourd des parcours — il produit la leçon ET le code du projet fil rouge, valide le .docx (étape 5 bis), tient PROJET.md, et vérifie versions et signatures d'API à la doc officielle. Les règles 10 et 11 du même jour ajoutent la relecture des chiffres et des identifiants
  enneagramme-lecon) BUDGET="3.00" ;;   # relevé le 03/09/2026, un jour après le durcissement du 02/09 : la règle B1 de hiérarchie des sources impose de chercher une source indépendante à comité de lecture au lieu de se rabattre sur des blogs, de compter ses références et de dire d'où elles parlent
  stoicisme-lecon) BUDGET="3.00" ;;     # relevé préventivement le 03/09/2026 : la règle B1 « thème textuel = sources textuelles » ajoutée le même jour impose d'ouvrir au moins un texte intégral par leçon (Diogène Laërce, Lettres à Lucilius, Perseus) en plus des sources du socle, et de vérifier chaque référence de passage
  serafin-ph-veille) BUDGET="3.00" ;;   # relevé préventivement le 02/09/2026 : le durcissement du même jour impose de republier l'URL exactement testée, de poser de vrais ExternalHyperlink, et de recompter les relations externes dans le .docx produit — avec régénération complète si le compte est nul
  hypnose-lecon) BUDGET="3.00" ;;   # relevé préventivement le 01/09/2026 : la règle B1 de hiérarchie des sources ajoutée le même jour impose de remonter aux sources institutionnelles (INSERM, HAS, APA, Cochrane, PMC, Cairn) au lieu de se rabattre sur des sites de praticiens, et de compter ses références avant publication
  dzogchen-lecon) BUDGET="3.00" ;;  # relevé préventivement le 01/09/2026 : le durcissement du même jour impose une recherche de littérature savante en plus des sources du socle, et la consultation de textes traduits sur les leçons de corpus (15, 16, 18). Même profil qu'astrologie-karmique, qui a dépassé les 2 $ une semaine après son propre durcissement
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
  #
  # ⚠️ ÉLARGISSEMENT DU 27/08/2026 : le motif d'origine ("hit your limit|usage limit|
  # quota exceeded") ne couvrait PAS le libellé réellement renvoyé ce jour-là —
  # "You're out of extra usage · resets 1pm (Europe/Paris)" — qui ne contient aucune
  # de ces trois formes ("out of extra usage" ≠ "usage limit"). Résultat : le fail-fast
  # n'a pas déclenché, les tentatives 2 et 3 d'astrologie-karmique-lecon ont été brûlées
  # en 18 minutes face à un quota qui se rétablissait 3 heures plus tard.
  # Motif volontairement restreint : il ne doit JAMAIS capturer un 403 de source
  # bloquée (ATIH, Fnac, Darty…), qui est normal et géré par les prompts.
  LIMIT_RE="hit your limit|usage limit|quota exceeded|out of (extra )?usage|resets [0-9]"
  if tail -n +"$((LOG_MARK + 1))" "$LOG" | grep -qiE "$LIMIT_RE"; then
    RESET_LINE="$(tail -n +"$((LOG_MARK + 1))" "$LOG" | grep -iE "$LIMIT_RE" | head -1)"
    echo "[limit] ⛔ LIMITE D'USAGE atteinte — arrêt des tentatives (le backoff ne peut pas la lever)." >> "$LOG"
    echo "[limit] 👉 $RESET_LINE" >> "$LOG"
    echo "[limit] 👉 Rejouer après réinitialisation : bash outils/scripts/rattrapage_jobs.sh $JOB_ID" >> "$LOG"
    break
  fi

  # Fail-fast n°3 : plafond de coût dépassé. Rejouer à l'identique redonnera exactement
  # le même résultat — le plafond ne bougera pas tout seul. Constaté le 27/08/2026 sur
  # astrologie-karmique-lecon : la tentative 1 est morte sur "Exceeded USD budget (2)"
  # après le durcissement du prompt du 20/08, qui a renchéri l'exécution.
  # Le correctif est humain : relever la valeur dans le case BUDGET, plus haut dans ce
  # script — d'où un message qui pointe l'endroit exact à modifier.
  if tail -n +"$((LOG_MARK + 1))" "$LOG" | grep -qiE "Exceeded USD budget"; then
    echo "[budget] ⛔ PLAFOND DE COÛT DÉPASSÉ (${BUDGET} \$) — arrêt des tentatives : rejouer à l'identique échouerait pareil." >> "$LOG"
    echo "[budget] 👉 Relever la valeur pour ce job dans le 'case \$JOB_ID' de outils/scripts/run_job.sh (section BUDGET), puis : bash outils/scripts/rattrapage_jobs.sh $JOB_ID" >> "$LOG"
    echo "[budget] 👉 Un dépassement récurrent signale souvent un prompt alourdi : vérifier les dernières modifications du job dans jobs_config.json." >> "$LOG"
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

# ---- Fiches Obsidian des nouvelles leçons ----
# Crée la note .md adossée à chaque .docx de livrables/lecons/ qui n'en a pas encore.
# Idempotent, n'écrase jamais une fiche existante, ne touche à aucun .docx.
# La fiche est volontairement VIDE (tags « a-classer », sections Résumé et Notes liées
# à remplir) : ce qui est déductible du nom de fichier est pré-rempli, le reste suppose
# d'avoir lu la leçon. Ces fiches restent locales — elles sont exclues de l'auto-push
# ci-dessous, et apparaissent donc dans `git status` tant qu'elles ne sont pas
# committées à la main. C'est voulu : la liste des fiches à compléter est visible.
if [ "$EXIT" -eq 0 ] && [ -f "$PROJECT/outils/scripts/fiches_obsidian.py" ]; then
  /usr/bin/python3 "$PROJECT/outils/scripts/fiches_obsidian.py" >> "$LOG" 2>&1 \
    || echo "⚠️ fiches_obsidian.py a échoué (sans conséquence sur le livrable)" >> "$LOG"
fi
if [ "$EXIT" -eq 0 ] && [ -f "$PROJECT/outils/scripts/fiches_veille.py" ]; then
  /usr/bin/python3 "$PROJECT/outils/scripts/fiches_veille.py" >> "$LOG" 2>&1 \
    || echo "⚠️ fiches_veille.py a échoué (sans conséquence sur le livrable)" >> "$LOG"
fi

# ---- Tableau de bord des jobs (informatif, JAMAIS bloquant) ----
# Met à jour la colonne « Numéro de la dernière leçon » du classeur
# livrables/documents/2026-08-09_Les 14 Jobs.xlsx. Le numéro est LU dans le nom du
# dernier .docx du parcours, pas compté : un créneau manqué crée un trou de
# numérotation, et compter donnerait alors un chiffre faux.
# Idempotent : n'écrit le fichier que si une valeur a changé — donc pas de commit
# parasite les jours où le job est sauté pour doublon.
if [ "$EXIT" -eq 0 ] && [ -f "$PROJECT/outils/scripts/maj_xlsx_jobs.py" ]; then
  /usr/bin/python3 "$PROJECT/outils/scripts/maj_xlsx_jobs.py" >> "$LOG" 2>&1 \
    || echo "⚠️ maj_xlsx_jobs.py a échoué (sans conséquence sur le livrable)" >> "$LOG"
fi

# ---- Audit du vault (informatif, JAMAIS bloquant) ----
# Contrôle le nommage, la cohérence des fiches et l'intégrité des liens juste
# avant la publication. Il n'interrompt rien et ne corrige rien : un faux
# positif ne doit pas empêcher un livrable de partir. Son rôle est de laisser
# une trace dans le journal, à relire quand quelque chose cloche.
# Motif : le 17/08/2026, le pipeline RBPP a nommé sa note de veille HAS
# « .fiche.md » — le suffixe exclu de l'auto-push. Le livrable n'aurait jamais
# été publié, et rien dans le journal ne l'aurait signalé.
if [ "$EXIT" -eq 0 ] && [ -f "$PROJECT/outils/scripts/audit_vault.py" ]; then
  if /usr/bin/python3 "$PROJECT/outils/scripts/audit_vault.py" >> "$LOG" 2>&1; then
    echo "[audit] vault conforme" >> "$LOG"
  else
    echo "⚠️ [audit] ANOMALIES DÉTECTÉES dans le vault — voir le détail ci-dessus." >> "$LOG"
    echo "         Le livrable a bien été produit ; l'audit n'interrompt rien." >> "$LOG"
    echo "         Relancer à la main : python3 outils/scripts/audit_vault.py --verbeux" >> "$LOG"
  fi
fi

# ---- Auto-commit + push des livrables produits (option 2) ----
# Portée STRICTE : uniquement les dossiers de livrables générés (veilles + Livrables).
# Jamais "git add -A" → les dossiers personnels sensibles restent hors git.
# sources/veille (récursif) couvre tous les sous-dossiers de veille présents et futurs
# (iMac, …) ainsi que les .docx/.md de veille à la racine.
# livrables/projets couvre le projet fil rouge du parcours appli-ia (code + PROJET.md).
# livrables/documents couvre les documents Word divers et fiches synthèse.
# EXCLUSION sources/veille/*.fiche.md : même principe pour les veilles. Le suffixe
# « .fiche.md » est indispensable ici — sources/veille/ contient AUSSI des veilles
# rédigées directement en markdown (veille HAS notamment), qui sont des livrables et
# doivent continuer d'être publiées. Une exclusion sur *.md les bloquerait.
# ⚠️ Ne pas écrire '**/*.fiche.md' : en pathspec git, ** exige au moins un répertoire
# intermédiaire et laisserait passer les fiches à la racine de sources/veille/.
# EXCLUSION livrables/lecons/*.md : les fiches Obsidian adossées aux leçons sont des
# notes de travail personnelles. Elles sont versionnées (commit manuel du 14/08/2026)
# mais ne doivent JAMAIS repartir seules : dès qu'un résumé personnel y est écrit, un
# job qui les pousserait le publierait sur le dépôt public sans intervention.
# Les autres .md restent couverts : PROJET.md et SPEC.md (mémoire du parcours appli-ia)
# et les veilles de sources/veille en dépendent.
# NB : la portée reste une LISTE BLANCHE explicite. Ne jamais la remplacer par un
# 'git add -A' : les dossiers personnels (contexte/, sources/rbpp, en_cours…) doivent
# rester hors de toute publication automatique.
if [ "$EXIT" -eq 0 ]; then
  export GIT_SSH_COMMAND="ssh -i $HOME/.ssh/id_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes -o StrictHostKeyChecking=accept-new"
  git add sources/veille livrables/lecons livrables/quiz livrables/infographies livrables/projets livrables/controles livrables/documents \
          ':(exclude)livrables/lecons/*.md' ':(exclude)sources/veille/*.fiche.md' 2>/dev/null
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
