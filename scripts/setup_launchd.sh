#!/bin/bash
# ============================================================
# setup_launchd.sh — Installe/recharge les agents launchd des jobs Claude_Travail
# Génère un fichier .plist par job dans ~/Library/LaunchAgents/ et le charge.
# Idempotent : relançable à volonté (décharge puis recharge).
#
# Horaires (= champ "cron" de jobs_config.json) :
#   ai-act-veille      tous les jours 7h03
#   rbpp-pipeline      lundi    8h30
#   dzogchen-lecon     mardi    8h03
#   serafin-ph-veille  mercredi 8h03
#   enneagramme-lecon  mercredi 9h03
#   stoicisme-lecon    jeudi    8h03
#   nocode-ia-veille   vendredi 8h03
# Weekday launchd : 0/7=dimanche, 1=lundi … 5=vendredi, 6=samedi
# ============================================================

PROJECT="/Users/utilisateur/kDrive/Claude_Travail"
RUNNER="$PROJECT/scripts/run_job.sh"
AGENTS_DIR="$HOME/Library/LaunchAgents"
LABEL_PREFIX="com.claudetravail"
LOG_DIR="$PROJECT/scripts/logs"

mkdir -p "$AGENTS_DIR" "$LOG_DIR"
chmod +x "$RUNNER"

# job_id | minute | hour | weekday (vide = quotidien)
JOBS="ai-act-veille|3|7|
rgpd-veille|33|7|
rbpp-pipeline|30|8|1
psychopathologie-lecon|3|8|1
dzogchen-lecon|3|8|2
serafin-ph-veille|3|8|3
enneagramme-lecon|3|9|3
stoicisme-lecon|3|8|4
nocode-ia-veille|3|8|5"

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
echo "Désactiver: $PROJECT/scripts/teardown_launchd.sh"
