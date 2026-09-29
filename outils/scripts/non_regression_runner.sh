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
GARDER=0; MUTATIONS=0; JUGE_SEUL=0
for a in "$@"; do
  case "$a" in
    --garder)    GARDER=1 ;;
    --mutations) MUTATIONS=1 ;;
    # --juge-seul : ne joue QUE les auto-tests du juge, puis sort. Sert aux mutations du juge
    # (mode --mutations), qui lancent des copies mutées de CE fichier et exigent qu'elles
    # échouent. Sans ce raccourci, chaque mutation du juge coûterait les quatorze témoins.
    --juge-seul) JUGE_SEUL=1 ;;
    *) echo "option inconnue : $a (attendu --mutations, --juge-seul et/ou --garder)"; exit 2 ;;
  esac
done
STATUT=0

[ -f "$RUNNER" ] || { echo "✗ runner introuvable : $RUNNER"; exit 1; }

H="$(mktemp -d -t nrrunner)"
nettoyer() { [ "$GARDER" -eq 1 ] && echo "  (dossier conservé : $H)" || rm -rf "$H"; }
trap nettoyer EXIT

# ⚠️ LE DÉPÔT JETABLE EST UN SOUS-DOSSIER, PAS $H (27/09/2026). Première version : le dépôt
# git occupait $H, où vivent aussi la copie instrumentée, le faux claude, le scénario et le
# compteur. La mutation « liste blanche élargie à tout le dépôt » les a donc COMMITTÉS, puis
# le « git reset --hard » du témoin suivant les a EFFACÉS — et la mutation d'après ne pouvait
# plus rien lancer : les quatorze témoins tombaient pour une raison qui n'avait rien à voir.
# Les outils du harnais vivent dans $H, le dépôt sous test dans $D. Rien ne se croise.
D="$H/depot"
mkdir -p "$D/outils/scripts/logs"
# Un dépôt distant LOCAL et NU : le push de l'auto-commit doit réussir du premier coup,
# sinon le runner dort 15 s puis 30 s entre ses trois tentatives (S14 coûterait 45 s).
# Chemin de fichier, donc aucun réseau, aucune clé SSH, aucun accès au vrai dépôt.
( cd "$D" && git init -q . && git config user.email t@local && git config user.name T \
  && git init -q --bare "$H/distant.git" && git remote add origin "$H/distant.git" \
  && echo x > .semence && git add -A && git commit -qm init && git push -q origin HEAD:main \
  && git branch -M main && git branch --set-upstream-to=origin/main main ) >/dev/null 2>&1
SEMENCE="$(cd "$D" && git rev-parse HEAD 2>/dev/null)"
[ -n "$SEMENCE" ] || { echo "✗ dépôt jetable non initialisable"; exit 1; }
ecrire_config () {
  mkdir -p "$D/outils/scripts/logs"
  cat > "$D/jobs_config.json" <<'JSON'
{ "_derniere_mise_a_jour": "2026-09-27",
  "jobs": [ { "id": "test-job", "cron": "0 0 * * 0", "livrable": "aucun", "prompt": "prompt de test" } ] }
JSON
}
ecrire_config

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
  sed -e "s|^PROJECT=.*|PROJECT=\"$D\"|" \
      -e "s|/usr/local/bin/claude|$H/faux_claude|" \
      -e "s|^RETRY_DELAYS=.*|RETRY_DELAYS=(0 0)   # neutralisé par le harnais|" \
      "$src" > "$dest"
  local v
  for v in "PROJECT=\"$D\"" "$H/faux_claude" "RETRY_DELAYS=(0 0)"; do
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
# Auth : le libellé réel du CLI. Panne du 09→15/07/2026, jeton Keychain expiré en launchd.
AUTH='{"is_error":true,"subtype":"error_during_execution","result":"API Error: Failed to authenticate. Please run /login","total_cost_usd":0.01,"num_turns":1,"usage":{}}'
# Limite d'usage : le libellé RÉELLEMENT renvoyé le 27/08/2026, qui ne contient ni
# « usage limit » ni « quota exceeded » — c'est lui qui a motivé l'élargissement du motif.
LIMITE='{"is_error":true,"subtype":"error_during_execution","result":"You are out of extra usage · resets 1pm (Europe/Paris)","total_cost_usd":0.02,"num_turns":1,"usage":{}}'
# Un 403 de source bloquée : NORMAL et géré par les prompts (ATIH, Fnac, Darty…).
# Il ne doit déclencher AUCUN fail-fast — sinon les trois tentatives sont perdues à tort.
BLOQUEE='{"is_error":true,"subtype":"error_during_execution","result":"WebFetch: 403 Forbidden sur atih.sante.fr — source bloquee, repli prevu","total_cost_usd":0.3,"num_turns":6,"usage":{}}'
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
# ---- LE JUGE, isolé pour pouvoir être jugé lui-même (27/09/2026) ----
# juger() est PURE : elle ne lit aucun fichier, ne lance rien, et se contente de comparer.
# Elle a été extraite d'essai() pour une raison précise : c'est elle qui décide de tout, et
# si elle se casse — un IFS qui ne découpe plus, un grep qui devient permissif — TOUS les
# témoins passent au vert en ne comparant plus rien. Le mode d'auto-test ci-dessous la met à
# l'épreuve sur des cas synthétiques, avant que le moindre témoin ne tourne.
# Rend 0 si tout concorde, 1 sinon, et dépose l'explication dans JUGE_MOTIFS.
# ⚠️ LIMITE ASSUMÉE : « | » sépare les motifs, un motif ne peut donc pas en contenir.
# La comparaison est LITTÉRALE (grep -F) : un motif n'est jamais une expression régulière.
JUGE_MOTIFS=""
juger () {
  local code="$1" tent="$2" log="$3" att_exit="$4" att_tent="$5" doit="$6" interdit="$7"
  local ok=1 m
  JUGE_MOTIFS=""
  [ "$code" = "$att_exit" ] || { ok=0; JUGE_MOTIFS="exit $code au lieu de $att_exit"; }
  [ "$tent" = "$att_tent" ] || { ok=0; JUGE_MOTIFS="$JUGE_MOTIFS; $tent tentative(s) au lieu de $att_tent"; }
  local IFS='|'
  for m in $doit;     do [ -n "$m" ] && { grep -qF -- "$m" <<<"$log" || { ok=0; JUGE_MOTIFS="$JUGE_MOTIFS; « $m » ABSENT du log"; }; }; done
  for m in $interdit; do [ -n "$m" ] && { grep -qF -- "$m" <<<"$log" && { ok=0; JUGE_MOTIFS="$JUGE_MOTIFS; « $m » PRÉSENT alors qu'il ne devrait pas"; }; }; done
  unset IFS
  JUGE_MOTIFS="${JUGE_MOTIFS#; }"
  [ "$ok" = 1 ]
}

# ---- AUTO-TESTS DU JUGE : est-il capable de dire non ? ----
# Joués à CHAQUE invocation, avant les témoins : ils ne coûtent aucun sous-processus.
# Les douze mutations mordent sur run_job.sh ; celles-ci mordent sur le juge.
autotests_du_juge () {
  local LOG_T="premiere ligne
[retry] ✅ Succès à la tentative 2 (régénération complète : 40 tours)
[git] ✅ push OK (tentative 1)"
  local n=0 ko=0
  cas () {
    local att="$1" lib="$2"; shift 2
    local obt=0; juger "$@" || obt=1
    n=$((n + 1))
    if [ "$obt" = "$att" ]; then
      [ "${VERBEUX:-0}" = 1 ] && printf '    ✓ %s\n' "$lib"
    else
      printf '  ✗ AUTO-TEST DU JUGE : %s — verdict %s au lieu de %s (motifs : %s)\n' \
             "$lib" "$obt" "$att" "${JUGE_MOTIFS:-aucun}"
      ko=1
    fi
  }
  #    attendu  libellé                                     code tent log        att_exit att_tent doit interdit
  cas 0 "tout concorde"                                     0 2 "$LOG_T" 0 2 "push OK" "FAUX SUCCÈS"
  cas 1 "exit différent"                                    7 2 "$LOG_T" 0 2 "push OK" ""
  cas 1 "nombre de tentatives différent"                    0 3 "$LOG_T" 0 2 "push OK" ""
  cas 1 "un « doit contenir » absent"                       0 2 "$LOG_T" 0 2 "ABSENT_XYZ" ""
  cas 0 "deux « doit contenir » présents"                   0 2 "$LOG_T" 0 2 "push OK|régénération complète" ""
  cas 1 "deux « doit contenir », le second absent"          0 2 "$LOG_T" 0 2 "push OK|ABSENT_XYZ" ""
  cas 1 "deux « doit contenir », le premier absent"         0 2 "$LOG_T" 0 2 "ABSENT_XYZ|push OK" ""
  cas 1 "un « interdit » présent"                           0 2 "$LOG_T" 0 2 "" "push OK"
  cas 0 "un « interdit » absent"                            0 2 "$LOG_T" 0 2 "" "FAUX SUCCÈS"
  cas 1 "deux « interdits », le second présent"             0 2 "$LOG_T" 0 2 "" "ABSENT_XYZ|push OK"
  cas 0 "motifs vides : ignorés, pas cherchés"              0 2 "$LOG_T" 0 2 "" ""
  cas 0 "comparaison LITTÉRALE : parenthèses et deux-points" 0 2 "$LOG_T" 0 2 "(régénération complète : 40 tours)" ""
  cas 1 "comparaison LITTÉRALE : le point n'est pas un joker" 0 2 "$LOG_T" 0 2 "push.OK" ""
  cas 1 "comparaison LITTÉRALE : pas d'ancre regex"         0 2 "$LOG_T" 0 2 "^premiere" ""
  cas 1 "log vide et un motif attendu"                      0 2 ""        0 2 "push OK" ""
  cas 0 "log vide, rien d'attendu, rien d'interdit"         0 2 ""        0 2 "" ""
  cas 1 "accent dans le motif, absent du log"               0 2 "$LOG_T" 0 2 "régénération partielle" ""
  cas 0 "accent dans le motif, présent dans le log"         0 2 "$LOG_T" 0 2 "régénération complète" ""
  if [ "$ko" = 0 ]; then
    echo "  ✓ $n/$n auto-tests du juge — essai() sait dire non"
  else
    echo "  ✗ LE JUGE EST CASSÉ : tant qu'il l'est, un témoin vert ne prouve RIEN."
    STATUT=1
  fi
}

if [ "$JUGE_SEUL" = 1 ]; then
  autotests_du_juge
  exit $STATUT
fi

SILENCE=0; ECHECS=""
# Compteurs CALCULÉS : la première version annonçait « 10/10 témoins + 8/8 mutations » alors
# qu'il y en avait 14 et 12. Un verdict qui compte à la main finit par mentir (27/09/2026).
N_TEMOINS=0; N_MUT=0; N_MUT_OK=0
essai () {
  local nom="$1" att_exit="$2" att_tent="$3" doit="$4" interdit="$5"; shift 5
  local id="${nom%% *}"
  [ "$SILENCE" = 0 ] && N_TEMOINS=$((N_TEMOINS + 1))
  # La marque d'échec de run_job.sh (logs/.echec_<job>, 29/09/2026) SURVIT au processus :
  # c'est son rôle. Chaque témoin déclare sa propre prémisse — « sans échec avant » pour
  # S6 — donc on repart d'un monde propre. S15, lui, la conserve VOLONTAIREMENT.
  rm -f "$H/compteur" "$D"/outils/scripts/logs/test-job_*.log "$D/outils/scripts/logs/.echec_test-job"
  printf '%s\n' "$@" > "$H/scenario"
  ( cd "$D" && HARN="$H" bash "$COPIE" test-job ) >/dev/null 2>&1
  local code=$? tent log ok=1
  tent="$(cat "$H/compteur" 2>/dev/null || echo 0)"
  log="$(cat "$D"/outils/scripts/logs/test-job_*.log 2>/dev/null)"
  juger "$code" "$tent" "$log" "$att_exit" "$att_tent" "$doit" "$interdit" || ok=0
  local motifs="$JUGE_MOTIFS"
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

# ---- S14 : la LISTE BLANCHE de l'auto-push ----
# Les treize premiers témoins lisent le LOG. Celui-ci lit le COMMIT : c'est le seul moyen
# de savoir ce qui part vraiment sur le dépôt public. La règle de CLAUDE.md est « jamais
# git add -A » — contexte/, sources/rbpp, sources/tnmp, sources/qvct, en_cours/, ressources/,
# outils/ et NotebookLM/ restent hors publication automatique, et les fiches Obsidian des
# leçons comme les .fiche.md des veilles sont exclues par pathspec. Rien ne le vérifiait.
# L'assertion est une ÉGALITÉ d'ensembles, pas une inclusion : elle attrape autant un
# élargissement (un dossier personnel publié) qu'un rétrécissement (un livrable oublié).
PERMIS=(
  "livrables/lecons/parcours-test/2026-09-27_lecon-test_01_theme.docx"
  "livrables/quiz/quiz_test_2026-09-27.pptx"
  "livrables/infographies/infographie_test_2026-09-27.pptx"
  "livrables/projets/appli-ia/PROJET.md"
  "livrables/controles/2026-09-27_controle.docx"
  "livrables/documents/note-de-cadrage.docx"
  "sources/veille/serie-test/2026-09-27_veille_test.docx"
  "sources/veille/serie-test/2026-09-27_veille_markdown.md"
)
# Exclus par pathspec — des livrables voisins qui ne doivent PAS partir seuls.
EXCLUS=(
  "livrables/lecons/parcours-test/2026-09-27_lecon-test_01_theme.md"
  "sources/veille/serie-test/2026-09-27_veille_test.fiche.md"
  "sources/veille/2026-09-27_veille_racine.fiche.md"
)
# Dossiers personnels : jamais publiés automatiquement.
INTERDITS=(
  "contexte/emails/note.md" "sources/rbpp/recommandation.txt" "sources/tnmp/grille.txt"
  "sources/qvct/document.txt" "en_cours/script-jetable.js" "ressources/memo.md"
  "outils/scripts/outil.sh" "NotebookLM/RBPP/guide.md"
)
essai_liste_blanche () {
  local nom="S14 liste blanche de l'auto-push (lit le COMMIT)"
  [ "$SILENCE" = 0 ] && N_TEMOINS=$((N_TEMOINS + 1))
  local f
  # ⚠️ REPARTIR DE LA SEMENCE, PAS DE HEAD (27/09/2026). Première version : reset sur HEAD.
  # Au premier appel S14 publiait ses huit fichiers ; à l'appel suivant — chaque mutation
  # rejoue le lot — ils étaient déjà dans HEAD, « Rien de nouveau à committer », aucun push,
  # et S14 tombait dans les douze mutations. Un témoin non idempotent accuse tout le monde.
  # Le distant est remis au même point, sinon le pull --rebase du runner les ramène.
  ( cd "$D" && git reset -q --hard "$SEMENCE" && git push -q --force origin main \
      && git clean -qfdx ) >/dev/null 2>&1
  ecrire_config
  for f in "${PERMIS[@]}" "${EXCLUS[@]}" "${INTERDITS[@]}"; do
    mkdir -p "$D/$(dirname "$f")"; echo "contenu de $f" > "$D/$f"
  done
  rm -f "$H/compteur" "$D"/outils/scripts/logs/test-job_*.log
  printf '%s\n' "0|$OK40" > "$H/scenario"
  ( cd "$D" && HARN="$H" bash "$COPIE" test-job ) >/dev/null 2>&1
  local code=$? log obtenu voulu ok=1 motifs=""
  log="$(cat "$D"/outils/scripts/logs/test-job_*.log 2>/dev/null)"
  obtenu="$(cd "$D" && git show --pretty=format: --name-only HEAD 2>/dev/null | grep -v '^$' | sort | tr '\n' ' ' | sed 's/ *$//')"
  voulu="$(printf '%s\n' "${PERMIS[@]}" | sort | tr '\n' ' ' | sed 's/ *$//')"
  [ "$code" = 0 ] || { ok=0; motifs="exit $code au lieu de 0"; }
  grep -qF "push OK" <<<"$log" || { ok=0; motifs="$motifs; le push n'a pas abouti dans le dépôt jetable"; }
  [ "$obtenu" = "$voulu" ] || { ok=0; motifs="$motifs; l'ensemble publié diffère"; }
  if [ "$ok" = 1 ]; then
    ECHECS_LB=""
    [ "$SILENCE" = 0 ] && printf '  ✓ %-58s %s fichier(s) publié(s), %s exclu(s), %s interdit(s) écarté(s)\n' \
        "$nom" "${#PERMIS[@]}" "${#EXCLUS[@]}" "${#INTERDITS[@]}"
  else
    ECHECS="$ECHECS S14"; ECHECS_LB="S14"
    if [ "$SILENCE" = 0 ]; then
      printf '  ✗ %-58s %s\n' "$nom" "${motifs#; }"
      echo "      publié : $obtenu"
      echo "      attendu: $voulu"
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

  # S15 — LA MÉMOIRE D'ÉCHEC TRAVERSE LES PROCESSUS (29/09/2026).
  # S3, S5 et S9 couvrent le faux succès À L'INTÉRIEUR d'une exécution. Rien ne couvrait le
  # cas réel : hypnose-lecon meurt sur la limite d'usage à 09h03 (exit 1 ; la leçon reste sur
  # le disque, non contrôlée), rattrapage_jobs.sh le relance à 19h18 — NOUVEAU PROCESSUS —
  # l'étape 1 s'arrête sur le doublon en 2 tours, rend exit 0, et le runner a publié un .docx
  # que personne n'avait vérifié (2da03a1). ECHEC_ANTERIEUR était une variable de shell :
  # elle ne pouvait pas le savoir.
  # Ce témoin lance DEUX fois le runner sans effacer la marque entre les deux, et exige que
  # la seconde exécution refuse de publier. Il tombe si la marque n'est pas écrite, pas relue,
  # considérée comme périmée, ou levée à tort par une sortie non nulle.
  temoin_deux_processus () {
    local nom="S15 échec, PUIS nouveau processus à 3 tours = FAUX SUCCÈS"
    local marque="$D/outils/scripts/logs/.echec_test-job" ok=1 motifs=""
    [ "$SILENCE" = 0 ] && N_TEMOINS=$((N_TEMOINS + 1))
    rm -f "$H/compteur" "$D"/outils/scripts/logs/test-job_*.log "$marque"
    printf '%s\n' "1|$RESEAU" "1|$RESEAU" "1|$RESEAU" > "$H/scenario"
    ( cd "$D" && HARN="$H" bash "$COPIE" test-job ) >/dev/null 2>&1     # 1er processus : il échoue
    [ -f "$marque" ] || { ok=0; motifs="$motifs; la marque d'échec n'a pas été écrite"; }
    rm -f "$H/compteur" "$D"/outils/scripts/logs/test-job_*.log        # les logs partent, PAS la marque
    printf '%s\n' "0|$OK3" > "$H/scenario"
    ( cd "$D" && HARN="$H" bash "$COPIE" test-job ) >/dev/null 2>&1     # 2e processus : doublon, 3 tours
    local code=$? tent log
    tent="$(cat "$H/compteur" 2>/dev/null || echo 0)"
    log="$(cat "$D"/outils/scripts/logs/test-job_*.log 2>/dev/null)"
    juger "$code" "$tent" "$log" 7 1 "ÉCHEC ANTÉRIEUR SUR DISQUE|FAUX SUCCÈS|RIEN N'EST PUBLIÉ" "✅ Succès|push OK" || ok=0
    [ -n "$JUGE_MOTIFS" ] && motifs="$motifs$JUGE_MOTIFS"
    [ -f "$marque" ] || { ok=0; motifs="$motifs; la marque a été levée par un exit 7"; }
    if [ "$ok" = 1 ]; then
      [ "$SILENCE" = 0 ] && printf '  ✓ %-58s exit %s · %s tentative(s)\n' "$nom" "$code" "$tent"
    else
      ECHECS="$ECHECS S15"
      if [ "$SILENCE" = 0 ]; then
        printf '  ✗ %-58s %s\n' "$nom" "${motifs#; }"
        echo "$log" | grep -aE "retry|Fin du job" | sed 's/^/      /' | head -6
        STATUT=1
      fi
    fi
    rm -f "$marque"
  }
  temoin_deux_processus

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

  # S11 à S13 couvrent les deux AUTRES fail-fast, jamais testés jusqu'ici (27/09/2026).
  # Leur enjeu est le même que celui du plafond : une erreur non transitoire retentée trois
  # fois brûle le créneau hebdomadaire. Panne du 09→15/07/2026 pour l'auth (jeton Keychain
  # expiré en launchd), 27/08/2026 pour la limite d'usage — ce jour-là le motif ne couvrait
  # pas le libellé réel et les tentatives 2 et 3 d'astrologie-karmique ont été brûlées en
  # 18 minutes face à un quota qui se rétablissait 3 heures plus tard.
  essai "S11 erreur d'AUTHENTIFICATION = arrêt immédiat" 1 1 \
        "Échec d'AUTHENTIFICATION détecté|setup-token|pas de commit" "Nouvelle tentative|Succès" \
        "1|$AUTH" "0|$OK40"

  essai "S12 LIMITE D'USAGE (libellé réel du 27/08) = arrêt immédiat" 1 1 \
        "LIMITE D'USAGE atteinte|rattrapage_jobs.sh|pas de commit" "Nouvelle tentative|Succès" \
        "1|$LIMITE" "0|$OK40"

  # S13 est un témoin de FAUX POSITIF : un 403 de source bloquée n'est pas une limite d'usage.
  # Les commentaires de run_job.sh l'exigent en capitales ; rien ne le vérifiait.
  essai "S13 403 de source bloquée : AUCUN fail-fast, on retente" 1 3 \
        "Tentative 3 échouée" "LIMITE D'USAGE|AUTHENTIFICATION détecté" \
        "1|$BLOQUEE" "1|$BLOQUEE" "1|$BLOQUEE"

  essai_liste_blanche
}

echo "▶ Auto-tests du juge (aucun sous-processus)"
autotests_du_juge

echo "▶ Témoins du runner — scénarios de décision (faux claude, dépôt jetable)"
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
    "fail-fast d'authentification neutralise¤s#grep -qiE 'Failed to authenticate[^']*'#grep -qiE 'ZZ_AUCUNE_CORRESPONDANCE_ZZ'#¤S11"
    "fail-fast de limite d'usage neutralise¤s#^  LIMIT_RE=.*#  LIMIT_RE=\"ZZ_AUCUNE_CORRESPONDANCE_ZZ\"#¤S12"
    "liste blanche elargie a tout le depot¤s#^          ':(exclude)livrables/lecons/[*].md'.*#          '.' 2>/dev/null#¤S14"
    "exclusion des fiches Obsidian retiree¤s#':(exclude)livrables/lecons/[*].md' ##¤S14"
    # --- la mémoire d'échec entre processus (29/09/2026) : trois façons de la désarmer ---
    'marque d echec jamais ECRITE¤s#> "$MARQUE_ECHEC" 2>/dev/null#> /dev/null#¤S15'
    'marque d echec jamais RELUE¤s#^if \[ -f "\$MARQUE_ECHEC" \]; then#if false; then#¤S15'
    'fraicheur de la marque a 0 (toujours perimee)¤s#^ECHEC_FRAICHEUR=.*#ECHEC_FRAICHEUR=0#¤S15'
  )
  MUT_SRC="$H/mutant_source.sh"
  for M in "${MUTS[@]}"; do
    etiq="${M%%¤*}"; reste="${M#*¤}"; expr="${reste%%¤*}"; attendu="${reste#*¤}"
    sed "$expr" "$RUNNER" > "$MUT_SRC"
    if cmp -s "$MUT_SRC" "$RUNNER"; then
      printf '  ✗ %-44s la mutation N'"'"'A RIEN CHANGÉ — le sed ne mord plus sur run_job.sh\n' "$etiq"
      N_MUT=$((N_MUT + 1)); STATUT=1; continue
    fi
    if ! instrumenter "$MUT_SRC" "$COPIE" >/dev/null 2>&1; then
      printf '  ✗ %-44s la copie mutée n'"'"'a pas pu être instrumentée\n' "$etiq"; N_MUT=$((N_MUT + 1)); STATUT=1
      instrumenter "$RUNNER" "$COPIE" >/dev/null 2>&1; continue
    fi
    SILENCE=1; lancer_les_dix; SILENCE=0
    obtenu="$(echo $ECHECS | tr ' ' '\n' | sort -V | tr '\n' ' ' | sed 's/ *$//')"
    voulu="$(echo $attendu  | tr ' ' '\n' | sort -V | tr '\n' ' ' | sed 's/ *$//')"
    N_MUT=$((N_MUT + 1))
    if [ "$obtenu" = "$voulu" ]; then
      N_MUT_OK=$((N_MUT_OK + 1))
      printf '  ✓ %-44s tombent : %s\n' "$etiq" "${obtenu:-aucun (attendu)}"
    else
      printf '  ✗ %-44s tombent : %s   ATTENDU : %s\n' "$etiq" "${obtenu:-aucun}" "${voulu:-aucun}"
      STATUT=1
    fi
  done
  instrumenter "$RUNNER" "$COPIE" >/dev/null 2>&1   # on repart du runner réel

  # ---- MUTATIONS DU JUGE : et si c'était lui qui se cassait ? ----
  # Les douze mutations ci-dessus cassent run_job.sh. Celles-ci cassent juger(), la fonction
  # qui décide de tout. Un juge permissif rend les quatorze témoins verts sans rien comparer :
  # c'est la panne la plus dangereuse du harnais, et la seule qui ne se voit pas.
  # Chaque mutation produit une copie de CE fichier, lancée avec --juge-seul : elle DOIT sortir
  # en échec. Une mutation du juge que les auto-tests laissent passer est un trou de couverture.
  echo "▶ Mutations du juge — ses auto-tests doivent le prendre en défaut"
  MUTS_JUGE=(
    "comparaison rendue REGEX (grep -qF → grep -q)¤s/grep -qF -- /grep -q -- /g"
    "separateur de motifs neutralise (IFS)¤s/  local IFS='|'/  local IFS=\$'\\002'/"
    "boucle des motifs INTERDITS supprimee¤/for m in \$interdit;/d"
    "verdict toujours favorable¤s/^  \[ \"\$ok\" = 1 \]$/  true/"
    "comparaison du code de sortie supprimee¤s/^  \[ \"\$code\" = \"\$att_exit\" \].*$//"
    "comparaison du nombre de tentatives supprimee¤s/^  \[ \"\$tent\" = \"\$att_tent\" \].*$//"
  )
  MUTE="$H/harnais_mute.sh"
  for M in "${MUTS_JUGE[@]}"; do
    etiq="${M%%¤*}"; expr="${M#*¤}"
    sed "$expr" "$0" > "$MUTE"
    N_MUT=$((N_MUT + 1))
    if cmp -s "$MUTE" "$0"; then
      printf '  ✗ %-44s la mutation N'"'"'A RIEN CHANGÉ — le sed ne mord plus sur le juge\n' "$etiq"
      STATUT=1; continue
    fi
    if ! bash -n "$MUTE" 2>/dev/null; then
      printf '  ✗ %-44s la copie mutée du harnais ne passe pas bash -n\n' "$etiq"
      STATUT=1; continue
    fi
    if RUNNER_SOUS_TEST="$RUNNER" bash "$MUTE" --juge-seul >/dev/null 2>&1; then
      printf '  ✗ %-44s les auto-tests ne l'"'"'ont PAS vu — trou de couverture du juge\n' "$etiq"
      STATUT=1
    else
      N_MUT_OK=$((N_MUT_OK + 1))
      printf '  ✓ %-44s pris en défaut\n' "$etiq"
    fi
  done
fi

if [ "$STATUT" = 0 ]; then
  if [ "$MUTATIONS" = 1 ]; then
    echo "  ✓ $N_TEMOINS/$N_TEMOINS témoins + $N_MUT_OK/$N_MUT mutations (runner ET juge) — le runner publie ce"
    echo "        qui a été fait, refuse ce qui ne l'a pas été, les témoins tombent quand on casse le runner,"
    echo "        et les auto-tests tombent quand on casse le juge"
  else
    echo "  ✓ $N_TEMOINS/$N_TEMOINS — le runner publie ce qui a été fait, et refuse ce qui ne l'a pas été"
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
