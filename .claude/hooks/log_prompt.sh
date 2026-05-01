#!/bin/bash
# Hook UserPromptSubmit — Journalise chaque prompt dans session_YYYY-MM-DD_prompts.txt

# Lire le JSON depuis stdin
INPUT=$(cat)

# Extraire le texte du prompt (champ "prompt")
PROMPT_TEXT=$(echo "$INPUT" | /usr/bin/python3 -c "
import sys, json
data = json.load(sys.stdin)
print(data.get('prompt', '').strip())
" 2>/dev/null)

# Si le prompt est vide, ne rien faire
if [ -z "$PROMPT_TEXT" ]; then
  exit 0
fi

# Fichier cible : session du jour
DATE=$(date +%Y-%m-%d)
TARGET="/Users/utilisateur/kDrive/Claude_Travail/Prompt/session_${DATE}_prompts.txt"

# Créer le fichier s'il n'existe pas encore
if [ ! -f "$TARGET" ]; then
  cat > "$TARGET" << HEADER
═══════════════════════════════════════════════════════════════════
  JOURNAL DES PROMPTS — Session du ${DATE}
  Projet : Claude_Travail / ESSMS médico-social
═══════════════════════════════════════════════════════════════════

───────────────────────────────────────────────────────────────────
  Prompts enregistrés automatiquement par le hook UserPromptSubmit
───────────────────────────────────────────────────────────────────

HEADER
fi

# Calculer le numéro du prochain prompt
LAST_NUM=$(grep -o '^\[0-9\{3\}\]' "$TARGET" 2>/dev/null | tail -1 | tr -d '[]' | sed 's/^0*//')
NEXT_NUM=$(( ${LAST_NUM:-0} + 1 ))
PADDED=$(printf "%03d" $NEXT_NUM)

# Horodatage
TIMESTAMP=$(date +"%H:%M:%S")

# Ajouter le prompt au fichier
{
  echo "[${PADDED}] [${TIMESTAMP}] ${PROMPT_TEXT}"
  echo ""
} >> "$TARGET"

exit 0
