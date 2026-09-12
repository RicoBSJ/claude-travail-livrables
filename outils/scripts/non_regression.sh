#!/bin/zsh
# non_regression.sh — rejoue les contrôles communs sur le corpus du dépôt et compare au dernier passage accepté.
#
#   outils/scripts/non_regression.sh            passes A/A2/A3/A4 des attributions (sans aspiration, ~2 min) sur toutes les
#                                               leçons et veilles + décompte sur les 85 veilles + les 14 témoins
#                                               d'avant correction (qui doivent sortir en 1) ; diff avec la référence.
#   outils/scripts/non_regression.sh --complet  ajoute le contrôle d'attributions COMPLET (avec aspiration) sur les
#                                               trois témoins à citations — long, dépend du réseau (exit 3 = relancer).
#   outils/scripts/non_regression.sh --accepter enregistre le passage courant comme nouvelle référence, APRÈS avoir
#                                               lu le diff et compris chaque changement de verdict.
#
# Sort en 0 si aucun verdict n'a changé, en 1 sinon (ou si un témoin ne sort plus en 1). Les documents nouveaux
# depuis la référence sont signalés, pas comparés : un job qui publie ne crée pas une régression.
# Hook : outils/scripts/hooks/pre-push lance ce script avant tout push qui touche un contrôle commun
# (installation : git config core.hooksPath outils/scripts/hooks).
# Règle (JOBS.md, 12/09/2026) : toute retouche de controle_attributions.py ou controle_decompte.py se rejoue ici,
# dans les deux sens, et le diff des verdicts se lit — pas seulement le décompte. Dix-huit défauts ont été trouvés
# en rejouant, aucun en relisant.
set -u
ROOT="/Users/utilisateur/kDrive/Claude_Travail"
NR="$ROOT/outils/scripts/non_regression"
REF="$NR/reference"
CUR="$NR/courant"
PY=/usr/bin/python3
mkdir -p "$CUR"
MODE="${1:-}"

# ── 1. passes A, A2, A3, A4 des attributions, sans aspiration : le fichier est exécuté jusqu'au marqueur « # ── aspiration »
echo "▶ Passes A/A2/A3/A4 (attributions, sans aspiration) sur leçons + veilles…"
find "$ROOT/livrables/lecons" "$ROOT/sources/veille" -name "*.docx" | sort > "$CUR/corpus.txt"
env -i $PY - "$ROOT/outils/scripts/controle_attributions.py" $(cat "$CUR/corpus.txt") > "$CUR/passe_A.tsv" <<'PYH'
import sys, io, contextlib
src = open(sys.argv[1], encoding="utf-8").read()
code = src[src.index("import sys, re, html, subprocess"):src.index("# ── aspiration des pages")]
for f in sys.argv[2:]:
    sys.argv = ["x", f]; out = io.StringIO(); g = {"__name__": "__main__"}
    with contextlib.redirect_stdout(out):
        try: exec(code, g)
        except SystemExit as e: print("EXIT", e)
    orph = sorted(g.get("orphelines", set())); snl = sorted(g.get("sites_non_listes", set()))
    a2 = sorted(g.get("sans_adresse", set())); a3 = sorted(g.get("mal_formes", set())); a4 = list(g.get("src_sans_adresse", []))
    print("%s\t%d\t%s\t%s\t%s" % (f.split("/")[-1], len(orph) + len(snl) + len(a2) + len(a3) + len(a4), ";".join(orph), ";".join(snl), ";".join(a2 + a3 + a4)[:200]))
PYH
N_A=$(wc -l < "$CUR/passe_A.tsv" | tr -d ' '); B_A=$(awk -F'\t' '$2>0' "$CUR/passe_A.tsv" | wc -l | tr -d ' ')
echo "  $N_A documents · $B_A bloquant(s)"

# ── 2. décompte sur les veilles
echo "▶ Décompte sur les veilles…"
: > "$CUR/decompte.tsv"
for f in $(find "$ROOT/sources/veille" -name "*.docx" | sort); do
  env -i $PY "$ROOT/outils/scripts/controle_decompte.py" "$f" > /dev/null 2>&1; rc=$?
  printf "%s\t%s\n" "$rc" "${f#$ROOT/sources/veille/}" >> "$CUR/decompte.tsv"
done
echo "  $(cut -f1 "$CUR/decompte.tsv" | sort | uniq -c | awk '{printf "exit %s : %s · ", $2, $1}')"

# ── 3. les quatorze témoins d'avant correction : tous doivent sortir en 1
echo "▶ Témoins d'avant correction (doivent sortir en 1)…"
TEM_KO=0
for f in "$NR"/temoins_decompte_avant_correction/*.docx; do
  env -i $PY "$ROOT/outils/scripts/controle_decompte.py" "$f" > /dev/null 2>&1; rc=$?
  if [ "$rc" != "1" ]; then echo "  ✗ $(basename "$f") sort en $rc au lieu de 1"; TEM_KO=$((TEM_KO+1)); fi
done
[ "$TEM_KO" = "0" ] && echo "  ✓ 14/14 en exit 1"

# ── 4. diff avec la référence
STATUT=0
if [ "$MODE" = "--accepter" ]; then
  mkdir -p "$REF"; cp "$CUR/passe_A.tsv" "$CUR/decompte.tsv" "$REF/"; date "+%d/%m/%Y %H:%M" > "$REF/date.txt"
  echo "▶ Référence enregistrée ($(cat "$REF/date.txt"))."
elif [ -f "$REF/passe_A.tsv" ]; then
  echo "▶ Diff avec la référence du $(cat "$REF/date.txt") :"
  # seuls les documents présents dans LES DEUX passages sont comparés : un document nouveau (un job vient
  # de publier) ou disparu n'est pas une régression — il est listé à part
  D1=$(join -t$'\t' -j1 <(cut -f1,2 "$REF/passe_A.tsv" | sort) <(cut -f1,2 "$CUR/passe_A.tsv" | sort) | awk -F'\t' '$2!=$3{printf "    %s : %s → %s bloquant(s)\n",$1,$2,$3}')
  D2=$(join -t$'\t' -j1 <(awk -F'\t' '{print $2"\t"$1}' "$REF/decompte.tsv" | sort) <(awk -F'\t' '{print $2"\t"$1}' "$CUR/decompte.tsv" | sort) | awk -F'\t' '$2!=$3{printf "    %s : exit %s → %s\n",$1,$2,$3}')
  NOUV=$(comm -13 <(cut -f1 "$REF/passe_A.tsv" | sort) <(cut -f1 "$CUR/passe_A.tsv" | sort) | wc -l | tr -d ' ')
  DISP=$(comm -23 <(cut -f1 "$REF/passe_A.tsv" | sort) <(cut -f1 "$CUR/passe_A.tsv" | sort) | wc -l | tr -d ' ')
  [ "$NOUV" != "0" ] && echo "  ($NOUV document(s) nouveau(x) depuis la référence — non comparés, --accepter pour les y inscrire)"
  [ "$DISP" != "0" ] && echo "  ($DISP document(s) de la référence absent(s) du corpus)"
  if [ -z "$D1" ] && [ -z "$D2" ]; then echo "  ✓ aucun verdict n'a changé"; else
    [ -n "$D1" ] && { echo "  passes A/A2/A3/A4 :"; echo "$D1"; }
    [ -n "$D2" ] && { echo "  décompte :"; echo "$D2"; }
    echo "  → lis chaque ligne ; si le changement est voulu et compris : non_regression.sh --accepter"
    STATUT=1
  fi
else
  echo "▶ Pas encore de référence : non_regression.sh --accepter pour enregistrer ce passage."
fi
[ "$TEM_KO" != "0" ] && STATUT=1

# ── 5. contrôle complet sur les témoins à citations
if [ "$MODE" = "--complet" ]; then
  echo "▶ Contrôle d'attributions complet (avec aspiration) sur trois témoins…"
  for f in "$ROOT"/livrables/lecons/*stoicisme_14*.docx "$ROOT"/livrables/lecons/*appli-ia_07*.docx "$ROOT"/livrables/lecons/*placement-financier_14*.docx; do
    env -i $PY "$ROOT/outils/scripts/controle_attributions.py" "$f" > "$CUR/$(basename "$f" .docx).txt" 2>&1; rc=$?
    case $rc in 0) l="✓ exit 0";; 3) l="⟳ exit 3 — pages non lues, à relancer";; *) l="✗ exit $rc"; STATUT=1;; esac
    echo "  $l  $(basename "$f")  ($(grep -m1 '^VERDICT' "$CUR/$(basename "$f" .docx).txt" | cut -c1-80))"
  done
fi
exit $STATUT
