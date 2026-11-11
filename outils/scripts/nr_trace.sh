#!/bin/sh
# ─────────────────────────────────────────────────────────────────────────────────────────────
# nr_trace.sh — SHIM D'INTERPRÉTEUR : il JOURNALISE le script lancé, puis s'effface.
#
# 🔴 POURQUOI — 11/11/2026. Le garde `non_regression/categories_hook.py` recensait les scripts
#    lancés par le harnais en LISANT SON TEXTE. Deux défauts mesurés le même jour :
#      ① il ne connaissait qu'UNE forme d'appel (`$ROOT/…`) et ratait la forme Python
#        `racine + "/outils/…"` d'un heredoc — donc un script RÉELLEMENT exécuté
#        (`controle_clauses_parcours.py`) n'était ni compté, ni accusé ;
#      ② sur ses 59 sites appariés, 14 étaient des `if [ -x … ]` — des TESTS D'EXISTENCE,
#        pas des lancements. Il comptait donc aussi des non-lancements.
#    Un prédicat textuel ne peut pas fermer cette classe : il faut que le harnais DÉCLARE ce
#    qu'il lance, au moment où il le lance.
#
# 🟢 CE QU'IL FAIT. Le harnais définit `PY` sur ce shim (une seule ligne, qui instrumente ses
#    37 lancements Python d'un coup). Le shim écrit dans le journal le chemin, relatif à la
#    racine, de chaque argument qui est un script du dépôt, puis `exec` le vrai interpréteur.
#
# ⛔ IL SURVIT À `env -i`, ET C'EST LA CONTRAINTE QUI DICTE SA FORME. Le harnais lance presque
#    tout sous `env -i`, qui efface l'environnement : le chemin du journal ne peut donc PAS
#    être transmis par une variable. Il est déduit de l'emplacement du shim lui-même ($0).
#    Pour la même raison tout est appelé en ABSOLU : aucun PATH n'est garanti.
#
# ⛔ IL NE DOIT JAMAIS FAIRE ÉCHOUER UN RUN. Un journal impossible à écrire est silencieux :
#    l'instrumentation est un observateur, pas un garde. Le garde, c'est l'épilogue du harnais.
# ─────────────────────────────────────────────────────────────────────────────────────────────
PY_REEL=/usr/bin/python3
D=$(dirname "$0")                       # …/outils/scripts
R=$(cd "$D/../.." 2>/dev/null && pwd)   # racine du dépôt
J="$D/logs/.nr_journal"

if [ -n "$R" ] && [ -d "$D/logs" ]; then
  for a in "$@"; do
    case "$a" in
      "$R"/outils/scripts/*.py) printf '%s\n' "${a#"$R"/}" >> "$J" 2>/dev/null ;;
      outils/scripts/*.py)      printf '%s\n' "$a"         >> "$J" 2>/dev/null ;;
    esac
  done
fi
exec "$PY_REEL" "$@"
