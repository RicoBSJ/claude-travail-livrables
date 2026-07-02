#!/bin/bash
# ============================================================
# teardown_launchd.sh — Désinstalle tous les agents launchd Claude_Travail
# Décharge et supprime les fichiers .plist com.claudetravail.*
# ============================================================

AGENTS_DIR="$HOME/Library/LaunchAgents"
LABEL_PREFIX="com.claudetravail"

echo "=== Désinstallation des agents launchd Claude_Travail ==="
COUNT=0
for PLIST in "$AGENTS_DIR/${LABEL_PREFIX}."*.plist; do
  [ -e "$PLIST" ] || continue
  launchctl unload "$PLIST" 2>/dev/null
  rm -f "$PLIST"
  echo "🗑️  Supprimé : $(basename "$PLIST")"
  COUNT=$((COUNT+1))
done
echo "=== ${COUNT} agent(s) désinstallé(s) ==="
