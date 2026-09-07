#!/bin/bash
# ============================================================
# setup_launchd.sh — Installe/recharge les agents launchd des jobs Claude_Travail
# Génère un fichier .plist par job dans ~/Library/LaunchAgents/ et le charge.
# Idempotent : relançable à volonté (décharge puis recharge).
#
# Horaires (= champ "cron" de jobs_config.json) :
#   revenus-passifs-lecon  dimanche 7h03
#   controle-livrables     dimanche 11h03 (contrôle qualité de la semaine)
#   imac-veille        dimanche 8h03
#   rbpp-pipeline      lundi    8h30
#   dzogchen-lecon     mardi    8h03
#   serafin-ph-veille  mercredi 8h03
#   enneagramme-lecon  mercredi 9h03
#   stoicisme-lecon    jeudi    8h03
#   appli-ia-lecon     vendredi 8h03
#   astrologie-karmique-lecon      jeudi 9h33
# Weekday launchd : 0/7=dimanche, 1=lundi … 5=vendredi, 6=samedi (vide = quotidien)
# ============================================================

PROJECT="/Users/utilisateur/kDrive/Claude_Travail"
RUNNER="$PROJECT/outils/scripts/run_job.sh"
AGENTS_DIR="$HOME/Library/LaunchAgents"
LABEL_PREFIX="com.claudetravail"
LOG_DIR="$PROJECT/outils/scripts/logs"

mkdir -p "$AGENTS_DIR" "$LOG_DIR"
chmod +x "$RUNNER"

# ------------------------------------------------------------------
# GARDE-FOU — ne jamais recharger pendant qu'un job tourne (07/09/2026)
#
# "launchctl unload" TUE le processus en cours de l'agent déchargé.
# Incident du 07/09/2026 : rbpp-pipeline démarré à 8h30 avait écrit son
# livrable à 8h35 ; un setup_launchd.sh lancé à 8h37 l'a tué avant
# maj_xlsx_jobs.py et avant l'auto-commit/push. Symptôme trompeur :
# "launchctl list" affiche exit 0, le livrable existe, le log s'arrête
# sans ligne de fin, et rien ne signale que la publication n'a pas eu lieu.
# ------------------------------------------------------------------
EN_VOL=""

# a) le runner lui-même (couvre aussi un lancement manuel)
for PID in $(pgrep -f "outils/scripts/run_job.sh" 2>/dev/null); do
  [ "$PID" = "$$" ] && continue
  EN_VOL="${EN_VOL}  • PID ${PID} : $(ps -o args= -p "$PID" 2>/dev/null | head -c 120)\n"
done

# b) les agents launchd dont la 1re colonne est un PID (et non "-")
while read -r PID _STATUS LABEL; do
  case "$PID" in
    ''|*[!0-9]*) continue ;;
  esac
  EN_VOL="${EN_VOL}  • agent ${LABEL} (PID ${PID})\n"
done < <(launchctl list 2>/dev/null | grep "$LABEL_PREFIX")

if [ -n "$EN_VOL" ] && [ "$1" != "--force" ]; then
  echo "⛔ REFUS : un job est en cours d'exécution."
  printf "%b" "$EN_VOL"
  echo ""
  echo "Recharger maintenant le tuerait avant son auto-commit/push."
  echo "Attends la fin du job (les leçons durent ~10 min), puis relance."
  echo "Pour passer outre en connaissance de cause : bash $0 --force"
  exit 1
fi


# job_id | minute | hour | weekday (vide = quotidien)
JOBS="revenus-passifs-lecon|3|7|0
imac-veille|3|8|0
rbpp-pipeline|30|8|1
psychopathologie-lecon|3|8|1
dzogchen-lecon|3|8|2
serafin-ph-veille|3|8|3
enneagramme-lecon|3|9|3
stoicisme-lecon|3|8|4
appli-ia-lecon|3|8|5
placement-financier-lecon|3|8|6
hypnose-lecon|3|9|2
astrologie-karmique-lecon|33|9|4
controle-livrables|3|11|0
ai-act-veille|3|9|5"

echo "=== Installation des agents launchd Claude_Travail ==="
echo ""

COUNT=0
while IFS='|' read -r JOB_ID MIN HOUR WDAY; do
  [ -z "$JOB_ID" ] && continue
  LABEL="${LABEL_PREFIX}.${JOB_ID}"
  PLIST="$AGENTS_DIR/${LABEL}.plist"

  # Bloc StartCalendarInterval (avec ou sans Weekday)
  if [ -n "$WDAY" ]; then
    CAL="    <key>StartCalendarInterval</key>
    <dict>
        <key>Weekday</key>
        <integer>${WDAY}</integer>
        <key>Hour</key>
        <integer>${HOUR}</integer>
        <key>Minute</key>
        <integer>${MIN}</integer>
    </dict>"
    WHEN="weekday=${WDAY} ${HOUR}h$(printf '%02d' "$MIN")"
  else
    CAL="    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>${HOUR}</integer>
        <key>Minute</key>
        <integer>${MIN}</integer>
    </dict>"
    WHEN="quotidien ${HOUR}h$(printf '%02d' "$MIN")"
  fi

  # Écriture du plist
  cat > "$PLIST" <<PLISTEOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${LABEL}</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>${RUNNER}</string>
        <string>${JOB_ID}</string>
    </array>
${CAL}
    <key>RunAtLoad</key>
    <false/>
    <key>StandardOutPath</key>
    <string>${LOG_DIR}/${JOB_ID}.launchd.out</string>
    <key>StandardErrorPath</key>
    <string>${LOG_DIR}/${JOB_ID}.launchd.err</string>
    <key>ProcessType</key>
    <string>Background</string>
</dict>
</plist>
PLISTEOF

  # Recharge : décharge si déjà présent, puis charge
  launchctl unload "$PLIST" 2>/dev/null
  if launchctl load "$PLIST" 2>/dev/null; then
    echo "✅ ${JOB_ID}  (${WHEN})  → ${PLIST}"
    COUNT=$((COUNT+1))
  else
    echo "❌ ÉCHEC chargement : ${JOB_ID}"
  fi
done <<< "$JOBS"

echo ""
echo "=== ${COUNT} agents installés ==="
echo "Vérifier  : launchctl list | grep claudetravail"
echo "Désactiver: $PROJECT/outils/scripts/teardown_launchd.sh"
