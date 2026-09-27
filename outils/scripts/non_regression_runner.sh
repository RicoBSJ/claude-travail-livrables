#!/bin/bash
# ============================================================
# non_regression_runner.sh — témoins permanents du RUNNER (outils/scripts/run_job.sh)
#
# Usage :  outils/scripts/non_regression_runner.sh [--garder]
#          --garder : conserve le dossier de travail pour inspection
#
# POURQUOI CE HARNAIS EXISTE (27/09/2026)
# run_job.sh décide, pour les 14 jobs, ce qui est retenté et ce qui est PUBLIÉ sur le
# dépôt public. Rien ne le testait. Deux incidents l'ont montré coup sur coup :
#   • 26/09/2026 — appli-ia-lecon : la tentative 1 meurt sur le plafond (3,0689 $ = 102 %,
#     64 tours) APRÈS avoir écrit la leçon sur le disque ; la tentative 2 s'arrête en 9,9 s
#     et 3 tours sur la vérification de doublon, rend exit 0, et le runner publie du travail
#     partiel en écrivant « ✅ Succès à la tentative 2 ».
#   • Cause racine : le fail-fast du plafond cherchait « Exceeded USD budget », la sortie
#     TEXTE de claude -p. L'étape 0 du 07/09/2026 est passée à --output-format json, qui
#     dit « subtype=error_max_budget_usd ». Le garde-fou était mort depuis 19 jours, et
#     AUCUN test ne pouvait le dire.
# D'où ce harnais : un faux `claude` piloté par un scénario (une ligne par tentative),
# run_job.sh recopié avec PROJECT détourné vers un dépôt jetable. Le vrai dépôt n'est
# jamais touché, aucun jeton n'est utilisé, aucun réseau n'est appelé.
#
# ⚠️ IL TESTE LES DÉCISIONS, PAS LA GÉNÉRATION. Ce que ce harnais ne voit pas : la qualité
# du livrable (c'est non_regression.sh), l'authentification réelle, le push réel.
# ============================================================
set -o pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
# RUNNER_SOUS_TEST : pour PROUVER QUE CE HARNAIS A DES DENTS. Un harnais qui passe aussi
# sur la version fautive ne teste rien. Vérification à refaire après toute retouche :
#   RUNNER_SOUS_TEST=/chemin/vers/run_job.sh.avant outils/scripts/non_regression_runner.sh
# Mesuré le 27/09/2026 sur la version d'avant correctif : S1, S3, S4 et S5 tombent.
RUNNER="${RUNNER_SOUS_TEST:-$ROOT/outils/scripts/run_job.sh}"
GARDER=0; [ "${1:-}" = "--garder" ] && GARDER=1
STATUT=0

[ -f "$RUNNER" ] || { echo "✗ runner introuvable : $RUNNER"; exit 1; }

H="$(mktemp -d -t nrrunner)"
nettoyer() { [ "$GARDER" -eq 1 ] && echo "  (dossier conservé : $H)" || rm -rf "$H"; }
trap nettoyer EXIT

mkdir -p "$H/outils/scripts/logs"
( cd "$H" && git init -q . && git config user.email t@local && git config user.name T \
  && echo x > .semence && git add -A && git commit -qm init ) >/dev/null 2>&1
cat > "$H/jobs_config.json" <<'JSON'
{ "_derniere_mise_a_jour": "2026-09-27",
  "jobs": [ { "id": "test-job", "cron": "0 0 * * 0", "livrable": "aucun", "prompt": "prompt de test" } ] }
JSON

# faux claude : lit $HARN/scenario, une ligne « code|sortie » par tentative
cat > "$H/faux_claude" <<'FAUX'
#!/bin/bash
N=$(cat "$HARN/compteur" 2>/dev/null || echo 0); N=$((N+1)); echo "$N" > "$HARN/compteur"
LIGNE="$(sed -n "${N}p" "$HARN/scenario")"
[ -z "$LIGNE" ] && { echo '{"is_error":true,"subtype":"error","result":"scenario epuise"}'; exit 1; }
echo "${LIGNE#*|}"
exit "${LIGNE%%|*}"
FAUX
chmod +x "$H/faux_claude"

# ---- copie instrumentée du runner, avec VÉRIFICATION que chaque substitution a pris ----
# Sans ces trois contrôles, un renommage de variable dans run_job.sh rendrait le harnais
# muet : il testerait une copie non instrumentée, ou le VRAI projet. C'est la leçon du
# fail-fast mort — un motif qui ne correspond plus ne dit rien, il ne crie pas.
sed -e "s|^PROJECT=.*|PROJECT=\"$H\"|" \
    -e "s|/usr/local/bin/claude|$H/faux_claude|" \
    -e "s|^RETRY_DELAYS=.*|RETRY_DELAYS=(1 1)   # accéléré par le harnais|" \
    "$RUNNER" > "$H/runner_test.sh"
for v in "PROJECT=\"$H\"" "$H/faux_claude" "RETRY_DELAYS=(1 1)"; do
  grep -qF "$v" "$H/runner_test.sh" || {
    echo "✗ INSTRUMENTATION MANQUÉE : « $v » absent de la copie."
    echo "  run_job.sh a changé de forme (PROJECT=, chemin de claude, ou RETRY_DELAYS=)."
    echo "  Adapte les sed de ce harnais AVANT de conclure quoi que ce soit."
    exit 1; }
done
grep -qF "$ROOT" "$H/runner_test.sh" && {
  echo "✗ DANGER : la copie instrumentée référence encore le vrai projet ($ROOT) — arrêt."
  exit 1; }
bash -n "$H/runner_test.sh" || { echo "✗ la copie instrumentée ne passe pas bash -n"; exit 1; }

# ---- sorties JSON types, calquées sur les vraies (champs vérifiés sur les logs) ----
OK40='{"is_error":false,"subtype":"success","stop_reason":"end_turn","result":"lecon ecrite","total_cost_usd":1.9,"num_turns":40,"duration_ms":600000,"usage":{"input_tokens":30,"output_tokens":27000}}'
OK3='{"is_error":false,"subtype":"success","stop_reason":"end_turn","result":"arret etape 1 : doublon du jour","total_cost_usd":0.15,"num_turns":3,"duration_ms":16000,"usage":{"input_tokens":4,"output_tokens":590}}'
BUDGJ='{"is_error":true,"subtype":"error_max_budget_usd","stop_reason":"tool_use","result":"arret sur plafond","total_cost_usd":3.07,"num_turns":64,"duration_ms":844000,"usage":{"input_tokens":54,"output_tokens":52618}}'
RESEAU='{"is_error":true,"subtype":"error_during_execution","stop_reason":"","result":"timeout reseau","total_cost_usd":0.4,"num_turns":8,"duration_ms":30000,"usage":{"input_tokens":4,"output_tokens":20}}'
# 12 tours : juste AU-DESSUS de TOURS_MINI=10. Sert à borner le seuil par le haut (voir S8).
OK12='{"is_error":false,"subtype":"success","stop_reason":"end_turn","result":"veille ecrite","total_cost_usd":0.8,"num_turns":12,"duration_ms":180000,"usage":{"input_tokens":12,"output_tokens":9000}}'
BUDGTXT='Error: Exceeded USD budget (3)'
NONJSON='recapitulatif en texte brut, sans json'

# ---- un scénario : nom | exit attendu | tentatives attendues | doit contenir | doit NE PAS contenir | lignes ----
essai () {
  local nom="$1" att_exit="$2" att_tent="$3" doit="$4" interdit="$5"; shift 5
  rm -f "$H/compteur" "$H"/outils/scripts/logs/test-job_*.log
  printf '%s\n' "$@" > "$H/scenario"
  ( cd "$H" && HARN="$H" bash runner_test.sh test-job ) >/dev/null 2>&1
  local code=$? tent log ok=1 motifs
  tent="$(cat "$H/compteur" 2>/dev/null || echo 0)"
  log="$(cat "$H"/outils/scripts/logs/test-job_*.log 2>/dev/null)"
  [ "$code" = "$att_exit" ] || { ok=0; motifs="exit $code au lieu de $att_exit"; }
  [ "$tent" = "$att_tent" ] || { ok=0; motifs="$motifs; $tent tentative(s) au lieu de $att_tent"; }
  local IFS='|'
  for m in $doit;     do [ -n "$m" ] && { grep -qF -- "$m" <<<"$log" || { ok=0; motifs="$motifs; « $m » ABSENT du log"; }; }; done
  for m in $interdit; do [ -n "$m" ] && { grep -qF -- "$m" <<<"$log" && { ok=0; motifs="$motifs; « $m » PRÉSENT alors qu'il ne devrait pas"; }; }; done
  unset IFS
  if [ "$ok" = 1 ]; then
    printf '  ✓ %-58s exit %s · %s tentative(s)\n' "$nom" "$code" "$tent"
  else
    printf '  ✗ %-58s %s\n' "$nom" "${motifs# ; }"
    echo "$log" | sed 's/^/      /' | grep -aE "retry|budget\]|git\]|Fin du job" | head -8
    STATUT=1
  fi
}

echo "▶ Témoins du runner — 8 scénarios de décision (faux claude, dépôt jetable)"

essai "S1 plafond dès la tentative 1 (forme JSON, cas du 26/09)" 1 1 \
      "PLAFOND DE COÛT DÉPASSÉ|pas de commit" "Succès à la tentative|FAUX SUCCÈS" \
      "1|$BUDGJ" "0|$OK3"

essai "S2 plafond dès la tentative 1 (forme texte historique)" 1 1 \
      "PLAFOND DE COÛT DÉPASSÉ" "Succès à la tentative" \
      "1|$BUDGTXT" "0|$OK3"

essai "S3 échec transitoire puis exit 0 en 3 tours = FAUX SUCCÈS" 7 2 \
      "FAUX SUCCÈS|PAS DE PUBLICATION|RIEN N'EST PUBLIÉ" "✅ Succès" \
      "1|$RESEAU" "0|$OK3"

essai "S4 échec transitoire puis vraie régénération (40 tours)" 0 2 \
      "Succès à la tentative 2 (régénération complète : 40 tours)" "FAUX SUCCÈS|PAS DE PUBLICATION" \
      "1|$RESEAU" "0|$OK40"

essai "S5 sortie non-JSON après un échec (tours inconnus)" 7 2 \
      "NOMBRE DE TOURS INCONNU|PAS DE PUBLICATION" "✅ Succès" \
      "1|$RESEAU" "0|$NONJSON"

essai "S6 arrêt sur doublon sans échec avant (rien à publier)" 0 1 \
      "Fin du job" "FAUX SUCCÈS|Tentative 1 échouée" \
      "0|$OK3"

essai "S7 trois échecs transitoires (comportement inchangé)" 1 3 \
      "Tentative 3 échouée|pas de commit" "FAUX SUCCÈS|Succès à la tentative" \
      "1|$RESEAU" "1|$RESEAU" "1|$RESEAU"

# S8 BORNE TOURS_MINI PAR LE HAUT, et c'est sa seule raison d'être (27/09/2026).
# S3 (3 tours → refusé) exige TOURS_MINI > 3 : il protège le seuil par le bas.
# Rien ne le protégeait par le haut : porté à 50, TOURS_MINI aurait transformé toute
# exécution courte mais RÉELLE en faux succès — une veille qui se boucle en 12 tours
# n'aurait plus jamais été publiée — et les sept premiers témoins seraient restés verts,
# S4 étant à 40 tours. S8 échoue dès que TOURS_MINI passe au-dessus de 12.
# Les deux ensemble enferment le seuil dans [4, 12] ; il vaut 10.
essai "S8 exécution courte mais RÉELLE (12 tours) = vrai succès" 0 2 \
      "Succès à la tentative 2 (régénération complète : 12 tours)" "FAUX SUCCÈS|PAS DE PUBLICATION" \
      "1|$RESEAU" "0|$OK12"

if [ "$STATUT" = 0 ]; then
  echo "  ✓ 8/8 — le runner publie ce qui a été fait, et refuse ce qui ne l'a pas été"
else
  echo "  ✗ AU MOINS UN TÉMOIN DU RUNNER A CHANGÉ DE COMPORTEMENT."
  echo "    Si le changement est voulu, mets à jour les attentes dans ce fichier — et dis pourquoi."
fi
# ⚠️ PAS « ▶ Terminé — exit N » : cette ligne est le sentinelle que le job controle-livrables
# lit sur la DERNIÈRE ligne de non_regression.sh, qui appelle ce harnais. Deux lignes identiques
# rendraient la lecture ambiguë (27/09/2026).
echo "▶ Témoins du runner — exit $STATUT"
exit $STATUT
