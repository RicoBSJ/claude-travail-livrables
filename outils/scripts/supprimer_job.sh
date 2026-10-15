#!/bin/bash
# supprimer_job.sh — supprime un job planifié en exécutant les SIX gestes, ou refuse.
#
# POURQUOI (15/10/2026). La suppression des trois jobs de parcours clos, le matin du
# 15/10/2026, a montré que la doctrine décrivait MAL ce geste : CLAUDE.md disait depuis le
# 11/09 que `setup_launchd.sh` « ne synchronise que les créneaux », ce qui est vrai et
# dangereusement incomplet — il porte sa PROPRE liste en dur, donc le lancer après avoir
# retiré un job de la config LE RÉINSTALLE, et il n'a jamais su retirer un .plist orphelin.
# Un job supprimé restait planifié indéfiniment, à appeler un id que run_job.sh ignore.
# Quatre autres emplacements ont été trouvés le même jour : le skill lancer-job (qui pointait
# encore `revenus` et `appli`, supprimés ONZE JOURS plus tôt), sa description de frontmatter,
# distincte de son corps, et le classeur de suivi, qui portait cinq jobs morts.
#
# ⚠️ ET LA RAISON D'ÊTRE DU GARDE-FOU : le dépôt a déjà perdu un parcours par oubli de date.
# La 11e leçon de `revenus-passifs` avait été PRÉDITE PAR ÉCRIT, avec sa date, dans JOBS.md
# le 27/09/2026 ; rien n'a été fait de la semaine et le livrable est sorti. Une note datée ne
# suffit pas. Ce script REFUSE donc de supprimer un job de leçon dont le parcours n'a pas
# atteint le compte qu'il annonce : il ne peut pas partir trop tôt, ni à moitié.
#
# Usage :  supprimer_job.sh <job_id>                  → PLAN seulement, ne touche à rien
#          supprimer_job.sh <job_id> --confirmer      → exécute les gestes ①→⑥
#          supprimer_job.sh <job_id> --config <chemin> → plan contre une config de test
#
set -u
RACINE="$(cd "$(dirname "$0")/../.." && pwd)"
JOB="${1:-}"; shift 2>/dev/null || true
CONFIRMER=0; CONFIG="$RACINE/jobs_config.json"
while [ "$#" -gt 0 ]; do
  case "$1" in
    --confirmer) CONFIRMER=1 ;;
    --config)    shift; CONFIG="$1" ;;
    *) echo "option inconnue : $1"; exit 2 ;;
  esac
  shift
done
[ -z "$JOB" ] && { sed -n '2,30p' "$0" | sed 's/^# \{0,1\}//'; exit 2; }
if [ "$CONFIRMER" = 1 ] && [ "$CONFIG" != "$RACINE/jobs_config.json" ]; then
  echo "⛔ --confirmer et --config ensemble : les gestes agissent sur le dépôt réel,"
  echo "   pas sur la config de test. Refusé pour éviter toute confusion."; exit 2
fi

python3 - "$CONFIG" "$JOB" <<'PY' || exit 3
import json, sys
cfg, jid = sys.argv[1], sys.argv[2]
ids = [x["id"] for x in json.load(open(cfg, encoding="utf-8"))["jobs"]]
if jid not in ids:
    sys.exit("⛔ job inconnu dans %s : %s\n   connus : %s" % (cfg, jid, ", ".join(ids)))
PY

CRON=$(python3 -c "
import json,sys
j=[x for x in json.load(open('$CONFIG',encoding='utf-8'))['jobs'] if x['id']=='$JOB'][0]
print(j.get('cron','?'))")
BUDGET=$(grep -oE "^\s*$JOB\)\s*BUDGET=\"[0-9.]+\"" "$RACINE/outils/scripts/run_job.sh" \
         | grep -oE '[0-9]+\.[0-9]+' | head -1)
BUDGET="${BUDGET:-aucun}"

# ── LE GARDE-FOU. On n'imite pas controle_clauses_parcours.py, on l'APPELLE : les contrôles
#    du dépôt sont appelés, jamais copiés.
LIGNE=$(env -i python3 "$RACINE/outils/scripts/controle_clauses_parcours.py" "$CONFIG" 2>/dev/null \
        | grep -E "^\s+$JOB\s") || true
if [ -n "$LIGNE" ]; then
  ANN=$(echo "$LIGNE" | grep -oE 'annoncé +[0-9]+' | grep -oE '[0-9]+')
  REE=$(echo "$LIGNE" | grep -oE 'réels +[0-9]+'  | grep -oE '[0-9]+')
  echo "▶ Garde-fou — parcours de leçons : annoncé $ANN · réels $REE"
  if [ -n "${ANN:-}" ] && [ -n "${REE:-}" ] && [ "$REE" -lt "$ANN" ]; then
    echo "⛔ REFUSÉ : il manque $((ANN - REE)) leçon(s) à ce parcours."
    echo "   Le supprimer maintenant perdrait $((ANN - REE)) livrable(s), dont le BILAN s'il"
    echo "   est le dernier. Laisse passer les créneaux restants, puis relance ce script."
    echo "   (Précédent : la 11e leçon de revenus-passifs, prédite par écrit le 27/09/2026"
    echo "    et sortie quand même faute d'action — l'inverse du risque, même cause.)"
    exit 1
  fi
  echo "  ✓ le parcours a atteint le compte qu'il annonce"
else
  echo "▶ Garde-fou : ce job n'est pas un parcours de leçons — aucun compte à vérifier"
fi

echo ""
echo "▶ PLAN pour « $JOB »  (créneau $CRON · plafond $BUDGET \$)"
echo "   ① jobs_config.json                       — retirer l'objet du job"
echo "   ② outils/scripts/run_job.sh              — retirer son « case ... BUDGET= »"
echo "   ③ outils/scripts/setup_launchd.sh        — retirer sa ligne JOBS, puis relancer"
echo "   ④ launchctl unload + rm                  — ~/Library/LaunchAgents/com.claudetravail.$JOB.plist"
echo "   ⑤ .claude/skills/lancer-job/SKILL.md     — corps ET description du frontmatter"
echo "   ⑥ refaire_classeur.py --refaire           — classeur reconstruit, ancien archivé, CLASSEUR repointé"
echo "   ⑦ à faire ensuite, à la main              — consigner, git add, commit, push"
if [ "$CONFIRMER" != 1 ]; then
  echo ""
  echo "   (plan seulement — rien n'a été touché. Ajoute --confirmer pour exécuter.)"
  exit 0
fi

SAUVE="${TMPDIR:-/tmp}/supprimer_job_$JOB_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$SAUVE"
cp "$RACINE/jobs_config.json" "$RACINE/outils/scripts/run_job.sh" \
   "$RACINE/outils/scripts/setup_launchd.sh" \
   "$RACINE/.claude/skills/lancer-job/SKILL.md" "$SAUVE/" 2>/dev/null
echo ""
echo "▶ Sauvegardes dans $SAUVE"

python3 - "$RACINE" "$JOB" <<'PY' || exit 4
import json, re, sys
racine, jid = sys.argv[1], sys.argv[2]
# ① la config
p = racine + "/jobs_config.json"
d = json.load(open(p, encoding="utf-8"))
n0 = len(d["jobs"])
d["jobs"] = [x for x in d["jobs"] if x["id"] != jid]
assert len(d["jobs"]) == n0 - 1
import datetime
d["_derniere_mise_a_jour"] = datetime.date.today().isoformat()
open(p, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
print("  ① jobs_config.json : %d → %d jobs" % (n0, len(d["jobs"])))
# ② le plafond
p = racine + "/outils/scripts/run_job.sh"
s = open(p, encoding="utf-8").read()
m = re.search(r"^\s+" + re.escape(jid) + r"\)\s+BUDGET=\"[^\"]+\" ;;.*$\n", s, re.M)
if m:
    open(p, "w", encoding="utf-8").write(s[:m.start()] + s[m.end():])
    print("  ② run_job.sh : case BUDGET retiré (%d octets)" % len(m.group(0)))
else:
    print("  ② run_job.sh : aucun case BUDGET (le job était au défaut)")
# ③ la liste des créneaux
p = racine + "/outils/scripts/setup_launchd.sh"
s = open(p, encoding="utf-8").read()
m = re.search(r"^" + re.escape(jid) + r"\|[^\n]*\n", s, re.M)
if m:
    open(p, "w", encoding="utf-8").write(s[:m.start()] + s[m.end():])
    print("  ③ setup_launchd.sh : ligne JOBS retirée")
else:
    sys.exit("  ③ ✗ ligne JOBS introuvable pour %s — ARRÊT, rien d'autre ne sera touché" % jid)
# ⑤ le skill, CORPS et DESCRIPTION
p = racine + "/.claude/skills/lancer-job/SKILL.md"
s = open(p, encoding="utf-8").read()
court = re.sub(r"-(?:lecon|veille|pipeline|livrables)$", "", jid)
n = len(s)
s = re.sub(r'^- "[^"]*"[^\n]*job id "' + re.escape(jid) + r'"\n', "", s, flags=re.M)
s = re.sub(r"^  /lancer-job \S+ +— [^\n]*\n(?=(?:  /lancer-job|```))" if False else
           r"^  /lancer-job " + re.escape(court) + r"\b[^\n]*\n", "", s, flags=re.M)
s = re.sub(r"(description:[^\n]*)\b" + re.escape(court) + r", ", r"\1", s)
s = re.sub(r"(description:[^\n]*), " + re.escape(court) + r"\b", r"\1", s)
open(p, "w", encoding="utf-8").write(s)
print("  ⑤ SKILL.md : %d → %d octets" % (n, len(s)))
PY

echo "  ③ relance de setup_launchd.sh…"
"$RACINE/outils/scripts/setup_launchd.sh" 2>&1 | grep -E "agents installés|ORPHELIN" | sed 's/^/     /'
P="$HOME/Library/LaunchAgents/com.claudetravail.$JOB.plist"
if [ -e "$P" ]; then
  launchctl unload "$P" 2>/dev/null; rm -f "$P" && echo "  ④ .plist déchargé et retiré"
else
  echo "  ④ aucun .plist à retirer"
fi

echo ""
echo "▶ Vérifications finales"
NJ=$(python3 -c "import json;print(len(json.load(open('$RACINE/jobs_config.json'))['jobs']))")
NP=$(ls "$HOME/Library/LaunchAgents"/com.claudetravail.*.plist 2>/dev/null | wc -l | tr -d ' ')
NC=$(launchctl list | grep -c claudetravail)
NB=$(grep -oE 'BUDGET="[0-9.]+"' "$RACINE/outils/scripts/run_job.sh" | grep -oE '[0-9.]+' | paste -sd+ - | bc)
echo "   jobs $NJ · .plist $NP · chargés $NC · plafonds $NB \$"
[ "$NJ" = "$NP" ] && [ "$NJ" = "$NC" ] && echo "   ✓ config, .plist et launchctl concordent" \
  || { echo "   ✗ DISCORDANCE — vérifie à la main"; exit 5; }
python3 -c "
import json,re
reels={x['id'] for x in json.load(open('$RACINE/jobs_config.json'))['jobs']}
skill=set(re.findall(r'job id \"([\w-]+)\"', open('$RACINE/.claude/skills/lancer-job/SKILL.md',encoding='utf-8').read()))
print('   ✓ ids du skill = ids de la config (%d)' % len(reels) if skill==reels
      else '   ✗ skill ≠ config — écart : %s' % sorted(skill^reels))"
# ── ⑥ LE CLASSEUR DE SUIVI, DÉSORMAIS AUTOMATIQUE (15/10/2026).
#    Il était « à faire à la main », et c'est précisément le geste qui avait été oublié cinq
#    fois : l'ancien classeur portait cinq jobs supprimés et un titre faux. `maj_xlsx_jobs.py`
#    ne met à jour qu'UNE colonne et ne touche jamais au jeu de lignes — il ne peut donc pas
#    suivre une suppression. `refaire_classeur.py --refaire` reconstruit depuis la config,
#    archive l'ancien et REPOINTE `CLASSEUR`, sans quoi le nouveau classeur se figerait.
echo ""
echo "▶ ⑥ Classeur de suivi"
if env -i python3 "$RACINE/outils/scripts/refaire_classeur.py" --refaire 2>&1 | sed 's/^/   /'; then
  env -i python3 "$RACINE/outils/scripts/refaire_classeur.py" --verifier 2>&1 \
    | grep -E "✓|✗" | sed 's/^ */   /'
else
  echo "   ⚠ le classeur n'a pas pu être refait — à traiter à la main avant de commiter"
fi
echo ""
echo "⑦ RESTE À FAIRE À LA MAIN :"
echo "   • consigner dans CLAUDE.md et outils/scripts/JOBS.md"
echo "   • git add explicite (dont l'ANCIEN et le NOUVEAU chemin du classeur), commit, push"
