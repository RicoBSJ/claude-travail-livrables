#!/bin/bash
# ============================================================
# non_regression_runner.sh — témoins permanents du RUNNER (outils/scripts/run_job.sh)
#
# Usage :  outils/scripts/non_regression_runner.sh [--mutations] [--garder]
#          --mutations : rejoue AUSSI les dix témoins contre sept runners MUTÉS, et vérifie
#                        que chaque mutation fait tomber exactement les témoins attendus.
#                        C'est la réponse à « qui teste le harnais ? ». Sans ce mode, un
#                        témoin devenu aveugle reste vert et personne ne le sait.
#          --garder    : conserve le dossier de travail pour inspection
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
# Mesuré le 27/09/2026 sur la version d'avant correctif : S1, S3, S4, S5, S9 et S10 tombent.
RUNNER="${RUNNER_SOUS_TEST:-$ROOT/outils/scripts/run_job.sh}"
GARDER=0; MUTATIONS=0
for a in "$@"; do
  case "$a" in
    --garder)    GARDER=1 ;;
    --mutations) MUTATIONS=1 ;;
    *) echo "option inconnue : $a (attendu --mutations et/ou --garder)"; exit 2 ;;
  esac
done
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
# Sans ces contrôles, un renommage de variable dans run_job.sh rendrait le harnais muet :
# il testerait une copie non instrumentée, ou le VRAI projet. C'est la leçon du fail-fast
# mort — un motif qui ne correspond plus ne dit rien, il se tait.
# RETRY_DELAYS=(0 0) : le backoff lui-même n'est pas sous test, et l'annuler rend les
# mutations abordables (sept passes au lieu d'une).
COPIE="$H/runner_test.sh"
instrumenter () {
  local src="$1" dest="$2"
  sed -e "s|^PROJECT=.*|PROJECT=\"$H\"|" \
      -e "s|/usr/local/bin/claude|$H/faux_claude|" \
      -e "s|^RETRY_DELAYS=.*|RETRY_DELAYS=(0 0)   # neutralisé par le harnais|" \
      "$src" > "$dest"
  local v
  for v in "PROJECT=\"$H\"" "$H/faux_claude" "RETRY_DELAYS=(0 0)"; do
    grep -qF "$v" "$dest" || {
      echo "✗ INSTRUMENTATION MANQUÉE : « $v » absent de la copie."
      echo "  run_job.sh a changé de forme (PROJECT=, chemin de claude, ou RETRY_DELAYS=)."
      echo "  Adapte les sed de ce harnais AVANT de conclure quoi que ce soit."
      return 1; }
  done
  grep -qF "$ROOT" "$dest" && {
    echo "✗ DANGER : la copie instrumentée référence encore le vrai projet ($ROOT) — arrêt."
    return 1; }
  bash -n "$dest" || { echo "✗ la copie instrumentée ne passe pas bash -n"; return 1; }
}
instrumenter "$RUNNER" "$COPIE" || exit 1

# ---- sorties JSON types, calquées sur les vraies (champs vérifiés sur les logs) ----
OK40='{"is_error":false,"subtype":"success","stop_reason":"end_turn","result":"lecon ecrite","total_cost_usd":1.9,"num_turns":40,"duration_ms":600000,"usage":{"input_tokens":30,"output_tokens":27000}}'
OK3='{"is_error":false,"subtype":"success","stop_reason":"end_turn","result":"arret etape 1 : doublon du jour","total_cost_usd":0.15,"num_turns":3,"duration_ms":16000,"usage":{"input_tokens":4,"output_tokens":590}}'
BUDGJ='{"is_error":true,"subtype":"error_max_budget_usd","stop_reason":"tool_use","result":"arret sur plafond","total_cost_usd":3.07,"num_turns":64,"duration_ms":844000,"usage":{"input_tokens":54,"output_tokens":52618}}'
RESEAU='{"is_error":true,"subtype":"error_during_execution","stop_reason":"","result":"timeout reseau","total_cost_usd":0.4,"num_turns":8,"duration_ms":30000,"usage":{"input_tokens":4,"output_tokens":20}}'
# 12 tours : au-dessus du seuil. Borne le seuil par le haut (S8).
OK12='{"is_error":false,"subtype":"success","stop_reason":"end_turn","result":"veille ecrite","total_cost_usd":0.8,"num_turns":12,"duration_ms":180000,"usage":{"input_tokens":12,"output_tokens":9000}}'
# 5 tours : arrêt précoce, aucune génération jamais observée à ce niveau. Borne par le bas (S9).
OK5='{"is_error":false,"subtype":"success","stop_reason":"end_turn","result":"arret precoce","total_cost_usd":0.22,"num_turns":5,"duration_ms":40000,"usage":{"input_tokens":6,"output_tokens":900}}'
# 9 tours : CAS RÉEL — serafin-ph-veille du 09/09/2026, 0,4298 $, veille de 18 781 octets
# écrite et poussée. Chiffres repris de mesures_couts.csv. Borne le seuil par le bas du haut (S10).
OK9='{"is_error":false,"subtype":"success","stop_reason":"end_turn","result":"veille SERAFIN-PH ecrite","total_cost_usd":0.4298,"num_turns":9,"duration_ms":220891,"usage":{"input_tokens":12,"output_tokens":9858}}'
BUDGTXT='Error: Exceeded USD budget (3)'
NONJSON='recapitulatif en texte brut, sans json'

# ---- un scénario : nom | exit attendu | tentatives attendues | doit contenir | doit NE PAS contenir | lignes ----
# Le nom commence par l'identifiant (S1, S2…) : c'est lui qu'on accumule dans ECHECS, et
# c'est sur cet ensemble que les mutations sont jugées.
SILENCE=0; ECHECS=""
essai () {
  local nom="$1" att_exit="$2" att_tent="$3" doit="$4" interdit="$5"; shift 5
  local id="${nom%% *}"
  rm -f "$H/compteur" "$H"/outils/scripts/logs/test-job_*.log
  printf '%s\n' "$@" > "$H/scenario"
  ( cd "$H" && HARN="$H" bash "$COPIE" test-job ) >/dev/null 2>&1
  local code=$? tent log ok=1 motifs=""
  tent="$(cat "$H/compteur" 2>/dev/null || echo 0)"
  log="$(cat "$H"/outils/scripts/logs/test-job_*.log 2>/dev/null)"
  [ "$code" = "$att_exit" ] || { ok=0; motifs="exit $code au lieu de $att_exit"; }
  [ "$tent" = "$att_tent" ] || { ok=0; motifs="$motifs; $tent tentative(s) au lieu de $att_tent"; }
  local IFS='|'
  for m in $doit;     do [ -n "$m" ] && { grep -qF -- "$m" <<<"$log" || { ok=0; motifs="$motifs; « $m » ABSENT du log"; }; }; done
  for m in $interdit; do [ -n "$m" ] && { grep -qF -- "$m" <<<"$log" && { ok=0; motifs="$motifs; « $m » PRÉSENT alors qu'il ne devrait pas"; }; }; done
  unset IFS
  if [ "$ok" = 1 ]; then
    [ "$SILENCE" = 0 ] && printf '  ✓ %-58s exit %s · %s tentative(s)\n' "$nom" "$code" "$tent"
  else
    ECHECS="$ECHECS $id"
    if [ "$SILENCE" = 0 ]; then
      printf '  ✗ %-58s %s\n' "$nom" "${motifs#; }"
      echo "$log" | grep -aE "retry|budget\]|git\]|Fin du job" | sed 's/^/      /' | head -8
      STATUT=1
    fi
  fi
}

lancer_les_dix () {
  ECHECS=""

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

  # S9 et S10 RESSERRENT LE SEUIL SUR LA MESURE, PAS SUR L'INTUITION (27/09/2026).
  # S3 (3 tours) n'exigeait que TOURS_MINI ≥ 4 : un seuil à 4 ou 5 aurait laissé passer
  # comme « succès » un arrêt à 5 tours. S9 exige ≥ 6.
  # Et le dépouillement de mesures_couts.csv a montré que la borne haute était FAUSSE :
  # serafin-ph-veille a écrit et poussé une veille de 18 781 octets en 9 TOURS le 09/09/2026
  # (0,4298 $). TOURS_MINI valait 10 ce matin : cette veille-là aurait été refusée à la
  # publication si elle avait suivi une tentative échouée. S10 exige ≤ 9, et le seuil est
  # descendu à 7. Les deux ensemble enferment TOURS_MINI dans [6, 9].
  essai "S9 arrêt précoce à 5 tours = FAUX SUCCÈS" 7 2 \
        "FAUX SUCCÈS|PAS DE PUBLICATION" "✅ Succès" \
        "1|$RESEAU" "0|$OK5"

  essai "S10 cas réel serafin-ph 09/09 (9 tours) = vrai succès" 0 2 \
        "Succès à la tentative 2 (régénération complète : 9 tours)" "FAUX SUCCÈS|PAS DE PUBLICATION" \
        "1|$RESEAU" "0|$OK9"
}

echo "▶ Témoins du runner — 10 scénarios de décision (faux claude, dépôt jetable)"
lancer_les_dix

# ---- MODE --mutations : QUI TESTE LE HARNAIS ? ----
# Un témoin peut devenir aveugle sans que rien ne le dise : il reste vert. La seule preuve
# qu'il sert est de CASSER le runner exprès et de vérifier qu'il tombe — et que ce sont
# exactement les bons qui tombent. Ces mutations étaient jouées à la main le 27/09/2026 ;
# elles vivent ici désormais.
# Chaque ligne : « étiquette ¤ expression sed appliquée à run_job.sh ¤ témoins qui DOIVENT tomber ».
# Un ensemble plus PETIT que prévu = un témoin devenu aveugle. Un ensemble plus GRAND = une
# mutation qui touche plus que ce qu'on croyait, ou un témoin trop large. Les deux sont des
# échecs : on veut l'égalité, pas l'inclusion.
if [ "$MUTATIONS" = 1 ]; then
  echo "▶ Mutations du runner — les témoins doivent tomber, et exactement ceux-là"
  MUTS=(
    "TOURS_MINI=5 (sous le plancher mesuré)¤s/^TOURS_MINI=.*/TOURS_MINI=5/¤S9"
    "TOURS_MINI=6 (borne basse admissible)¤s/^TOURS_MINI=.*/TOURS_MINI=6/¤"
    "TOURS_MINI=9 (borne haute admissible)¤s/^TOURS_MINI=.*/TOURS_MINI=9/¤"
    "TOURS_MINI=10 (la valeur fautive du matin)¤s/^TOURS_MINI=.*/TOURS_MINI=10/¤S10"
    "TOURS_MINI=13¤s/^TOURS_MINI=.*/TOURS_MINI=13/¤S8 S10"
    "TOURS_MINI=50¤s/^TOURS_MINI=.*/TOURS_MINI=50/¤S4 S8 S10"
    "fail-fast du plafond sans la forme JSON¤s/|error_max_budget_usd|max_budget_usd//¤S1"
    "detection du travail partiel desarmee¤s/^  ECHEC_ANTERIEUR=1$/  ECHEC_ANTERIEUR=0/¤S3 S4 S5 S8 S9 S10"
  )
  MUT_SRC="$H/mutant_source.sh"
  for M in "${MUTS[@]}"; do
    etiq="${M%%¤*}"; reste="${M#*¤}"; expr="${reste%%¤*}"; attendu="${reste#*¤}"
    sed "$expr" "$RUNNER" > "$MUT_SRC"
    if cmp -s "$MUT_SRC" "$RUNNER"; then
      printf '  ✗ %-44s la mutation N'"'"'A RIEN CHANGÉ — le sed ne mord plus sur run_job.sh\n' "$etiq"
      STATUT=1; continue
    fi
    if ! instrumenter "$MUT_SRC" "$COPIE" >/dev/null 2>&1; then
      printf '  ✗ %-44s la copie mutée n'"'"'a pas pu être instrumentée\n' "$etiq"; STATUT=1
      instrumenter "$RUNNER" "$COPIE" >/dev/null 2>&1; continue
    fi
    SILENCE=1; lancer_les_dix; SILENCE=0
    obtenu="$(echo $ECHECS | tr ' ' '\n' | sort -V | tr '\n' ' ' | sed 's/ *$//')"
    voulu="$(echo $attendu  | tr ' ' '\n' | sort -V | tr '\n' ' ' | sed 's/ *$//')"
    if [ "$obtenu" = "$voulu" ]; then
      printf '  ✓ %-44s tombent : %s\n' "$etiq" "${obtenu:-aucun (attendu)}"
    else
      printf '  ✗ %-44s tombent : %s   ATTENDU : %s\n' "$etiq" "${obtenu:-aucun}" "${voulu:-aucun}"
      STATUT=1
    fi
  done
  instrumenter "$RUNNER" "$COPIE" >/dev/null 2>&1   # on repart du runner réel
fi

if [ "$STATUT" = 0 ]; then
  if [ "$MUTATIONS" = 1 ]; then
    echo "  ✓ 10/10 témoins + 8/8 mutations — le runner publie ce qui a été fait, refuse ce qui ne l'a"
    echo "        pas été, et les témoins tombent quand on le casse exprès"
  else
    echo "  ✓ 10/10 — le runner publie ce qui a été fait, et refuse ce qui ne l'a pas été"
    echo "        (les mutations ne sont PAS jouées ici : --mutations pour prouver que ces témoins mordent)"
  fi
else
  echo "  ✗ AU MOINS UN TÉMOIN DU RUNNER A CHANGÉ DE COMPORTEMENT."
  echo "    Si le changement est voulu, mets à jour les attentes dans ce fichier — et dis pourquoi."
fi
# ⚠️ PAS « ▶ Terminé — exit N » : cette ligne est le sentinelle que le job controle-livrables
# lit sur la DERNIÈRE ligne de non_regression.sh, qui appelle ce harnais. Deux lignes identiques
# rendraient la lecture ambiguë (27/09/2026).
echo "▶ Témoins du runner — exit $STATUT"
exit $STATUT
