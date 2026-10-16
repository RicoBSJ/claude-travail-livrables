#!/bin/zsh
# non_regression.sh — rejoue les contrôles communs sur le corpus du dépôt et compare au dernier passage accepté.
#
#   outils/scripts/non_regression.sh            passes A/A2/A3/A4 des attributions (sans aspiration, ~2 min) sur toutes les
#                                               leçons et veilles + décompte sur les 85 veilles + les 14 témoins
#                                               d'avant correction (qui doivent sortir en 1) ; diff avec la référence.
#   outils/scripts/non_regression.sh --complet  ajoute le contrôle d'attributions COMPLET (avec aspiration) sur les
#                                               trois témoins à citations (doivent sortir en 0) et sur les témoins
#                                               d'avant correction de non_regression/temoins_attributions_avant_correction/
#                                               (doivent sortir en 1) — long, dépend du réseau : un exit 3 est
#                                               retenté une fois après NR_ATTENTE s (60), puis affiché, jamais refusé.
#   outils/scripts/non_regression.sh --accepter enregistre le passage courant comme nouvelle référence, APRÈS avoir
#                                               lu le diff et compris chaque changement de verdict.
#   outils/scripts/non_regression.sh --docs f…  mode DOCUMENTS (quelques secondes) : pour chaque .docx donné, passes
#                                               A/A2/A3/A4 et, pour une veille, décompte ; comparé à la référence du
#                                               document — un document ne doit pas régresser, un document nouveau doit
#                                               être à 0 bloquant. C'est ce que le hook lance quand un push touche des
#                                               livrables ou des veilles (les jobs publient par là).
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

# Effectif ATTENDU de chaque lot de témoins (23/09/2026). Les trois boucles de témoins contrôlaient ce
# qu'elles trouvaient et annonçaient un total ÉCRIT EN DUR : « ✓ 14/14 en exit 1 » s'imprimait quel que
# soit le nombre de fichiers réellement passés. Le 23/09, pendant un test du hook, un témoin avait quitté
# son dossier et le script annonçait toujours 14/14. Pire : zsh saute une boucle dont le motif ne matche
# rien (« no matches found »), donc un lot VIDÉ — dossier supprimé, fichiers renommés, glob d'un document
# vivant qui ne matche plus après un rangement — faisait passer le contrôle sans en exécuter une ligne.
# Désormais chaque lot déclare son effectif ici, le script compte ce qu'il a réellement contrôlé, et TOUT
# écart refuse. Ajouter ou retirer un témoin, c'est mettre à jour le nombre correspondant ci-dessous.
# Les trois boucles portent le qualificateur zsh (N) : sans lui, un lot VIDE fait mourir le script sur
# « no matches found » avant même le diff des verdicts — refus, mais sans message lisible. Avec (N), le
# motif vide rend zéro fichier, le compteur reste à 0 et le contrôle ci-dessous dit ce qui manque.
ATTENDU_DECOMPTE=15   # temoins_decompte_avant_correction/ — 15 depuis le 02/10/2026 :
                      #   + ai-act/2026-10-02 TELLE QUE LIVRÉE (en-tête 8 sources, corps 9)
ATTENDU_DEC_CONFORMES=3  # temoins_decompte_conformes/ — doivent sortir en 0.
                      # ⚠️ POURQUOI CE LOT EXISTE (02/10/2026). Un témoin « d'avant correction » ne
                      # prouve que la MORSURE, jamais la JUSTESSE : la veille ai-act du 02/10 telle que
                      # livrée sort en 1 avec le contrôle bogué COMME avec le contrôle corrigé — elle ne
                      # discrimine rien. Ce qui discrimine, c'est sa version CORRIGÉE : exit 1 avec
                      # l'ancien contrôle (qui perdait une entrée sur les listes mêlant « ✅ Nom » et
                      # « Consultée… : Nom »), exit 0 avec le contrôle corrigé. Sans ce lot, rien dans ce
                      # harnais n'empêche de ramener le décalage d'appariement.
                      # ⚠️ TROIS FORMES DE LISTE, TROIS TÉMOINS — matrice mesurée le 02/10/2026 contre
                      # trois mutations du contrôle (copies jetables, jamais commitées) :
                      #   m1 = « Consultée… » classée avant le test du deux-points (ma 1re tentative de
                      #        correctif, qui réparait le 02/10 et cassait trois autres notes)
                      #   m2 = fermeture de groupe retirée (le défaut réellement corrigé le 02/10)
                      #   m3 = marqueurs de correction en ligne non retirés
                      #   ┌──────────────────────────────┬──────┬──────┬──────┬──────┐
                      #   │ témoin (doit sortir en 0)    │ sain │  m1  │  m2  │  m3  │
                      #   ├──────────────────────────────┼──────┼──────┼──────┼──────┤
                      #   │ ai-act 2026-10-02            │  0   │  0   │  1   │  1   │
                      #   │ ai-act 2026-09-18            │  0   │  1   │  0   │  0   │
                      #   │ imac   2026-08-30            │  0   │  1   │  0   │  0   │
                      #   └──────────────────────────────┴──────┴──────┴──────┴──────┘
                      # Chaque mutation est attrapée par au moins un témoin, et AUCUN témoin ne les
                      # attrape toutes : retirer l'un des trois rend une des trois mutations invisible.
                      # ⚠️ Le témoin du 02/10 ne couvre m3 que parce que son marqueur de correction cite
                      # le décompte d'origine EN CHIFFRES. Il avait d'abord été écrit en lettres pour
                      # contourner le bug m3 ; ce contournement le rendait aveugle à sa propre correction.
                      # Un marqueur qui cite fidèlement est donc aussi ce qui rend le test possible.
ATTENDU_CONFORMES=11  # 3 documents vivants (stoïcisme 14, appli-ia 07, placement 14) + temoins_attributions_conformes/ (8 copies figées)
                      # 11 depuis le 15/10/2026 : 2026-06-25_lecon-stoicisme_04_courbes.docx entre pour ㊱,
                      # les guillemets COURBES “ ” — c'est le SEUL document des 283 dont des citations de
                      # six mots ou plus tombaient hors de toute capture. Recensement complet, pas échantillon.
                      # 10 depuis le 11/10/2026 : 2026-10-01_lecon-astrologie-karmique_09_locale.docx entre pour
                      # garder ㉟ (un nombre français écrit à l'anglaise sur la page citée). ⚠️ CE TÉMOIN SORT EN 3,
                      # durablement : deux de ses citations sont sur des pages que le contrôle ne peut pas lire. Ce
                      # n'est pas son code de sortie qui prouve quelque chose, c'est sa LIGNE — comme pour ㉜.
                      # 9 depuis le 11/10/2026 : 2026-06-10_lecon-enneagramme_02_declaree.docx entre pour garder
                      # l'EXEMPTION de ㉞ — un lien dont le document declare qu'il ne resout pas n'est pas une faute.
                      # 8 depuis le 10/10/2026 : 2026-10-10_lecon-placement-financier_18_passeD.docx entre
                      # pour garder la PASSE D, qui n'est pas dans la référence et qu'aucun verdict ne protège.
                      # 4e copie figée le 09/10/2026 : la leçon Ennéagramme n°06 APRÈS correction, témoin de
                      # l'exemption de ㉜ — ses quatre citations d'ouvrages y sont DÉCLARÉES reformulations,
                      # et elle doit donc sortir en 0 SANS aucune ligne « SOURCE NOMMÉE SANS PAGE ». C'est le
                      # seul témoin qui garde la déclaration : si la détection devenait aveugle aux mots
                      # « reformulation / non consulté / d'après », il refuserait un document juste.
                      # 3e copie figée le 27/09/2026 : appli-ia n°10, témoin de ㉛ — deux requêtes SQL de son
                      # exercice (« SELECT COUNT(*) as n FROM livrables WHERE slug LIKE @m ») étaient lues comme
                      # des citations anglaises et bloquaient un document juste. Elle doit sortir en 0.
#   5 depuis le 26/09/2026 : la leçon placement-financier n°03 AVEC SES MARQUEURS DE CORRECTION
#   GUILLEMETÉS est entrée dans le lot. C'est le seul témoin qui garde l'exemption des marqueurs
#   dans les passes B, B-FR et B-NOM : il DOIT sortir en 0, et il sortait en 1 avant le correctif
#   du 26/09 (mesuré dans les deux sens). Si une formulation citée pour mémoire redevient un jour
#   une attribution, c'est lui qui le dira — aucun autre témoin conforme ne porte de marqueur.
ATTENDU_AVANT=9       # temoins_attributions_avant_correction/ — 9 depuis le 11/10/2026 :
                      # 2026-06-10_lecon-enneagramme_02_avant.docx entre pour garder ㉞ (un nom de domaine
                      # qui ne resout pas est un lien mort). C'est le SEUL des 394 hotes du depot dans ce cas.
#   la leçon Ennéagramme n°06 d'AVANT sa correction est entrée dans le lot ce jour-là. C'est le SEUL
#   témoin qui exerce la passe ㉜ : elle citait QUATRE ouvrages entre guillemets, en français, sans
#   qu'aucun texte ait été ouvert, et le contrôle n'en signalait qu'UN comme bloquant — le seul à côté
#   duquel un domaine était nommé. Les trois autres désignaient un LIVRE, et ㉖ ne déclenche que sur un
#   domaine. Ce témoin doit sortir en 1 (pour la citation de Palmer, via ㉖) ET porter au moins une
#   ligne « SOURCE NOMMÉE SANS PAGE » (via ㉜). Le code de sortie seul ne prouverait rien : il sortirait
#   en 1 sur la seule citation de Palmer même si ㉜ perdait toute sa dent.
#   7 depuis le 25/09/2026 :
#   la leçon appli-ia n°05 d'avant le 11/09 (commit 4ed6de0) est entrée dans le lot ce jour-là.
#   C'est le SEUL témoin qui exerce la passe C2 : « Vite v8.2.2 — vérifiée sur vite.dev/guide/
#   le 28/08/2026 » alors que la page ne l'a jamais portée. Les six autres témoins exercent B,
#   B-NOM et A6 ; le sens REFUS de C2 n'avait aucun témoin permanent, et la branche a été
#   retouchée deux fois le 25/09/2026 (acquittement de la dérive déclarée, et retrait du repli
#   qui cherchait le numéro de remplacement dans toute la fenêtre).

# ── 0 bis. AUTO-TESTS DE chercher.py — DANS TOUS LES MODES, --docs COMPRIS (15/10/2026)
# `chercher.py` n'est pas un contrôle de publication : c'est l'outil par lequel Claude vérifie
# qu'une citation, un chiffre ou une date figure bien sur une page aspirée, SANS que la page
# entre dans son contexte. Il ne peut donc pas être gardé par un témoin .docx ni par la
# référence. Mais ses bornes sont exactement celles que le dépôt a déjà payées cher :
#   • le « \? » devant la classe d'espaces — bug de la passe D réparé le 10/10/2026, reproduit
#     à l'identique à l'écriture de chercher.py le 15/10 (nombres présents donnés pour absents) ;
#   • le point JAMAIS séparateur de milliers — borne de ㉟ du 11/10, deux faux appariements
#     mesurés (« 7 918 » dans le « 7.918 » de doi.org, « 1 049 » dans le « 1.049 » d'apple.com) ;
#   • un jeton se cherche ponctuation CONSERVÉE — borne du 12/10 ;
#   • et le degré ④ doit MONTRER ce que la page écrit à la place, règle du 14/10 née de quatre
#     quasi-fausses accusations en deux jours.
# 21 auto-tests, 0,1 s, AUCUN appel réseau — donc il tourne même à la porte des pushs de job.
# Les neuf mutations qui les prennent en défaut sont dans le docstring de chercher.py.
if [ -x "$ROOT/outils/scripts/chercher.py" ]; then
  echo "▶ Auto-tests de chercher.py (appariement exact, aucun réseau)"
  # ⚠ PAS de pipe ici. La première écriture était « ... --autotest | tail -1 », qui teste le
  # code de sortie de TAIL : le sabotage s'affichait et le harnais sortait en 0 quand même.
  # Mesuré le 15/10/2026 à la pose du garde. Un garde qui ne fait pas sortir en 1 est décoratif.
  CH_OUT="$CUR/chercher_autotest.txt"
  if env -i $PY "$ROOT/outils/scripts/chercher.py" --autotest > "$CH_OUT" 2>&1; then
    tail -1 "$CH_OUT"
  else
    grep '✗' "$CH_OUT" | head -5
    echo "  ✗ chercher.py A PERDU UNE BORNE — un « ABSENT » de cet outil ne vaut plus rien"
    exit 1
  fi
fi

# ── 0. mode documents : quelques .docx, comparés un à un à la référence
if [ "$MODE" = "--docs" ]; then
  shift; STATUT=0
  [ $# -eq 0 ] && { echo "  (aucun document)"; exit 0; }
  # ㊳ (16/10/2026) UN LIVRABLE POUSSÉ VIENT-IL D'UNE EXÉCUTION RÉUSSIE ?
  # Avertissement pur, JAMAIS bloquant — la règle du 14/10/2026 l'exige d'un motif neuf à la
  # porte des pushs : avant de le rendre bloquant, le faire tourner en avertissement sur
  # quelques éditions fraîches, parce qu'un balayage rétrospectif ne mesure pas la
  # variabilité de ce qui vient. Incident fondateur : la veille ai-act du 16/10, écrite par
  # un job mort sur son plafond (3,2339 $ pour 3,00 $, 34 tours) SANS avoir lancé un seul
  # contrôle, puis publiée après une vérification manuelle.
  if [ -x "$ROOT/outils/scripts/controle_livrable_du_job.py" ]; then
    LJ="$CUR/livrable_du_job.txt"
    env -i $PY "$ROOT/outils/scripts/controle_livrable_du_job.py" "$@" > "$LJ" 2>&1 || true
    [ -s "$LJ" ] && cat "$LJ"
  fi
  env -i $PY - "$ROOT/outils/scripts/controle_attributions.py" "$@" > "$CUR/docs_A.tsv" <<'PYH'
import sys, io, contextlib
src = open(sys.argv[1], encoding="utf-8").read()
code = src[src.index("import sys, re, html, subprocess"):src.index("# ── aspiration des pages")]
for f in sys.argv[2:]:
    sys.argv = ["x", f]; out = io.StringIO(); g = {"__name__": "__main__"}
    with contextlib.redirect_stdout(out):
        try: exec(code, g)
        except SystemExit as e: print("EXIT", e)
    orph = sorted(g.get("orphelines", set())); snl = sorted(g.get("sites_non_listes", set()))
    a2 = sorted(g.get("sans_adresse", set())); a3 = sorted(g.get("mal_formes", set())); a4 = list(g.get("src_sans_adresse", [])) + list(g.get("sans_cible", []))
    print("%s\t%d\t%s" % (f.split("/")[-1], len(orph) + len(snl) + len(a2) + len(a3) + len(a4), " ; ".join(orph + snl + a2 + a3 + a4)[:300]))
PYH
  while IFS=$'\t' read -r nom n detail; do
    ref=$(awk -F'\t' -v n="$nom" '$1==n{print $2}' "$REF/passe_A.tsv" 2>/dev/null)
    if [ -z "$ref" ]; then etat="nouveau"; ref=0; else etat="référence $ref"; fi
    if [ "$n" -gt "$ref" ]; then echo "  ✗ $nom : $n bloquant(s) ($etat) — $detail"; STATUT=1
    else echo "  ✓ $nom : $n bloquant(s) ($etat)"; fi
  done < "$CUR/docs_A.tsv"
  for f in "$@"; do
    case "$f" in */sources/veille/*|sources/veille/*)
      env -i $PY "$ROOT/outils/scripts/controle_decompte.py" "$f" > "$CUR/doc_dec.txt" 2>&1; rc=$?
      nom="${f#*sources/veille/}"; ref=$(awk -F'\t' -v n="$nom" '$2==n{print $1}' "$REF/decompte.tsv" 2>/dev/null)
      if [ "$rc" = "1" ] && [ "${ref:-0}" != "1" ]; then echo "  ✗ $nom : décompte INCOHÉRENT (exit 1) — $(tail -1 "$CUR/doc_dec.txt")"; STATUT=1
      else echo "  ✓ $nom : décompte exit $rc"; fi
      # 12/10/2026 — relecture à l'édition PRÉCÉDENTE et à sa fiche. Aucun appel réseau, 0,3 s :
      # ce contrôle a sa place ici, dans la porte des pushs de job, et c'est le seul motif de
      # cette porte qui regarde AILLEURS que dans le document poussé.
      if [ -f "$ROOT/outils/scripts/controle_edition_precedente.py" ]; then
        env -i $PY "$ROOT/outils/scripts/controle_edition_precedente.py" "$f" > "$CUR/doc_edprec.txt" 2>&1; rce=$?
        case "$rce" in
          1) echo "  ✗ $nom : REJEU d'une correction de l'édition précédente — $(tail -1 "$CUR/doc_edprec.txt")"; STATUT=1;;
          2) echo "  ○ $nom : pas d'édition précédente — relecture INERTE";;
          *) RL=$(grep -c "^   A RELIRE" "$CUR/doc_edprec.txt")
             echo "  ✓ $nom : aucun rejeu de l'édition précédente$([ "$RL" != "0" ] && echo " ($RL point(s) à relire)")";;
        esac
      fi;;
    esac
  done
  exit $STATUT
fi

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
    a2 = sorted(g.get("sans_adresse", set())); a3 = sorted(g.get("mal_formes", set())); a4 = list(g.get("src_sans_adresse", [])) + list(g.get("sans_cible", []))
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
TEM_KO=0; TEM_N=0
for f in "$NR"/temoins_decompte_avant_correction/*.docx(N); do
  TEM_N=$((TEM_N+1))
  env -i $PY "$ROOT/outils/scripts/controle_decompte.py" "$f" > /dev/null 2>&1; rc=$?
  if [ "$rc" != "1" ]; then echo "  ✗ $(basename "$f") sort en $rc au lieu de 1"; TEM_KO=$((TEM_KO+1)); fi
done
if [ "$TEM_N" != "$ATTENDU_DECOMPTE" ]; then
  echo "  ✗ $TEM_N témoin(s) contrôlé(s), $ATTENDU_DECOMPTE attendu(s) — un lot incomplet ne prouve rien :"
  echo "    rétablis le ou les témoins manquants, ou mets ATTENDU_DECOMPTE à jour dans ce script."
  TEM_KO=$((TEM_KO+1))
fi
[ "$TEM_KO" = "0" ] && echo "  ✓ $TEM_N/$ATTENDU_DECOMPTE en exit 1"

# ── 3 bis. les témoins CONFORMES du décompte : tous doivent sortir en 0 (02/10/2026)
echo "▶ Témoins conformes du décompte (doivent sortir en 0)…"
DEC_KO=0; DEC_N=0
for f in "$NR"/temoins_decompte_conformes/*.docx(N); do
  DEC_N=$((DEC_N+1))
  env -i $PY "$ROOT/outils/scripts/controle_decompte.py" "$f" > /dev/null 2>&1; rc=$?
  if [ "$rc" != "0" ]; then echo "  ✗ $(basename "$f") sort en $rc au lieu de 0"; DEC_KO=$((DEC_KO+1)); fi
done
if [ "$DEC_N" != "$ATTENDU_DEC_CONFORMES" ]; then
  echo "  ✗ $DEC_N témoin(s) conforme(s) contrôlé(s), $ATTENDU_DEC_CONFORMES attendu(s) — un lot incomplet"
  echo "    ne prouve rien : rétablis le témoin manquant, ou mets ATTENDU_DEC_CONFORMES à jour."
  DEC_KO=$((DEC_KO+1))
fi
[ "$DEC_KO" = "0" ] && echo "  ✓ $DEC_N/$ATTENDU_DEC_CONFORMES en exit 0"
[ "$DEC_KO" != "0" ] && TEM_KO=$((TEM_KO+DEC_KO))

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
# RETRY (13/09/2026) : un exit 3 (page non lue — réseau, mur, délai) ne prouve rien sur la passe B ; comme le
# hook ne refuse pas sur un 3, un témoin qui sort en 3 laissait passer un push sans l'avoir testé. On retente
# UNE fois après NR_ATTENTE secondes (60 par défaut) ; un 3 qui persiste est affiché « deux essais » — toujours
# pas un refus (un site qui tombe n'est pas une régression du contrôle), mais on sait que ce passage n'a rien
# prouvé sur B, et il faut relancer --complet à la main.
ATTENTE="${NR_ATTENTE:-60}"
controle_complet() {   # $1 docx, $2 fichier de sortie → rc ; ESSAIS=1|2
  env -i $PY "$ROOT/outils/scripts/controle_attributions.py" "$1" > "$2" 2>&1; local rc=$?; ESSAIS=1
  if [ "$rc" = "3" ]; then
    sleep "$ATTENTE"
    env -i $PY "$ROOT/outils/scripts/controle_attributions.py" "$1" > "$2" 2>&1; rc=$?; ESSAIS=2
  fi
  return $rc
}
if [ "$MODE" = "--complet" ]; then
  # témoins CONFORMES : ils doivent sortir en 0. Les trois premiers sont les documents vivants (stoïcisme 14 :
  # citations anglaises appariées ; appli-ia 07 ; placement 14). S'y ajoutent les copies figées de
  # non_regression/temoins_attributions_conformes/ — chacune protège une passe contre un FAUX POSITIF :
  #   · 2026-09-15_lecon-dzogchen_16 (20/09/2026) : une phrase française prêtée à une page ANGLAISE (Lotsawa House,
  #     Tricycle) ne doit pas bloquer en B-NOM (㉙) — ses chiffres sont sur la page, ses mots français n'y sont pas.
  #     La passe l'a bloqué pendant deux heures le 20/09 et la note de contrôle a prescrit de supprimer des chiffres
  #     exacts. Un témoin qui sort en 1 = le contrôle a poussé une dent de trop.
  echo "▶ Contrôle d'attributions complet (avec aspiration) sur les témoins conformes (doivent sortir en 0)…"
  CONF_N=0
  for f in "$ROOT"/livrables/lecons/**/*stoicisme_14*.docx(N) "$ROOT"/livrables/lecons/**/*appli-ia_07*.docx(N) "$ROOT"/livrables/lecons/**/*placement-financier_14*.docx(N) "$ROOT"/outils/scripts/non_regression/temoins_attributions_conformes/*.docx(N); do
    [ -e "$f" ] || continue
    CONF_N=$((CONF_N+1))
    controle_complet "$f" "$CUR/$(basename "$f" .docx).txt"; rc=$?
    case $rc in 0) l="✓ exit 0";; 3) l="⟳ exit 3 après $ESSAIS essais — pages non lues, rien prouvé sur B : relancer --complet";; *) l="✗ exit $rc — un témoin conforme bloque : faux positif du contrôle"; STATUT=1;; esac
    [ "$ESSAIS" = "2" ] && [ "$rc" != "3" ] && l="$l (au 2e essai)"
    echo "  $l  $(basename "$f")  ($(grep -m1 '^VERDICT' "$CUR/$(basename "$f" .docx).txt" | cut -c1-80))"
    # ⚠️ LA PASSE D N'EST PAS DANS LA RÉFÉRENCE (10/10/2026). passe_A.tsv ne stocke que le NOMBRE de
    #    problèmes bloquants des passes A/A2/A3/A4 : une passe non bloquante est invisible au diff —
    #    même piège que ㉜ le 09/10 et que le motif ② d'ai-act, inerte trois semaines. On exige donc
    #    la LIGNE, dans les DEUX sens, sur ce témoin : il reprend littéralement « 1 782 € » de
    #    lafinancepourtous.com et « 38 400 € x 45 % x (158 / 170) = 16 060,24 € » de service-public.fr,
    #    trois nombres à SÉPARATEUR DE MILLIERS qui sont tous sur leurs pages. Le bug corrigé le
    #    10/10/2026 les rendait tous les trois « A VERIFIER … absente des pages citees », et un nombre
    #    réellement absent sortait avec le même libellé qu'un nombre réellement présent.
    # ⚠️ ㉟ (11/10/2026) : « 50,4 » et « 50,6 » — la période orbitale de Chiron — sont écrits
    #    « 50.4 » et « 50.6 » par le Minor Planet Center. Avant ㉟ la passe D les donnait pour
    #    ABSENTS. Ce témoin ne prouve rien par son code de sortie (il sort en 3, deux de ses
    #    citations étant sur des pages illisibles) : c'est la LIGNE qui est exigée.
    if [[ "$(basename "$f")" == "2026-10-01_lecon-astrologie-karmique_09_locale.docx" ]]; then
      TL="$CUR/$(basename "$f" .docx).txt"
      N_LOC=$(grep -cE "^ +OK +50,[46] +-> .*ecrit « 50\.[46] »" "$TL")
      if [ "$N_LOC" -ge 2 ]; then
        echo "        ↳ ✓ ㉟ tient : $N_LOC nombre(s) français retrouvé(s) sous leur graphie anglaise"
      else
        echo "        ↳ ✗ ㉟ A PERDU SA DENT : « 50,4 » et « 50,6 » ne sont plus appariés à « 50.4 » et"
        echo "          « 50.6 » du Minor Planet Center ($N_LOC/2) — la passe D a reperdu la locale."
        STATUT=1
      fi
    fi
    # ⚠️ ㊱ (15/10/2026) LES GUILLEMETS COURBES. La demande portait sur les guillemets DROITS :
    #    ils étaient déjà appariés depuis l'origine de la boucle de B/B-FR, et la mesure sur la
    #    leçon astrologie-karmique n°11 l'a prouvé — ses trois citations anglaises entre " ont été
    #    vues, deux OK et une en ㉚. Le vrai manque était les COURBES, celles que Word substitue
    #    au ". Sur les 283 documents, UN SEUL perdait des citations de six mots ou plus : celui-ci,
    #    le Manuel d'Épictète, pour cinq d'entre elles.
    #    ⚠️ CE TÉMOIN NE PROUVE RIEN PAR SON CODE DE SORTIE — il sort en 0 AVANT comme APRÈS le
    #    portage, les cinq citations gagnées étant des traductions, donc non appariables et rendues
    #    en « A RELIRE » non bloquant. C'est la LIGNE qui est exigée, comme pour ㉜, D, ㉞ et ㉟.
    #    ⚠️ Et le portage lui-même a d'abord été une RÉGRESSION, mesurée avant commit : ajouter
    #    “ ” à l'alternance fait de “ un délimiteur et TRONQUE les spans « … » qui en contiennent
    #    — 21 documents raccourcis, et une capture tronquée est introuvable sur sa page, donc
    #    « ABSENTE » faux sur une passe BLOQUANTE. D'où un balayage COMPLÉMENTAIRE, qui n'ajoute
    #    que les citations courbes ne chevauchant aucune capture déjà faite : 1 document gagne,
    #    0 ne perd rien, 0 code de sortie ne change.
    if [[ "$(basename "$f")" == "2026-06-25_lecon-stoicisme_04_courbes.docx" ]]; then
      TL="$CUR/$(basename "$f" .docx).txt"
      N_CB=$(grep -cE "A RELIRE (Ce ne sont pas les événements qui troublent|Toute chose a deux anses)" "$TL")
      if [ "$N_CB" -ge 2 ]; then
        echo "        ↳ ✓ ㊱ tient : $N_CB citation(s) entre guillemets courbes “ ” vue(s) par B-FR"
      else
        echo "        ↳ ✗ ㊱ A PERDU SA DENT : les citations d'Épictète entre “ ” sont redevenues"
        echo "          invisibles à B-FR ($N_CB/2) — le balayage complémentaire ne mord plus."
        STATUT=1
      fi
    fi
    # ⚠️ L'EXEMPTION DE ㉞ SE GARDE AUSSI (11/10/2026) : ce témoin est la même leçon, dont le lien
    #    mort est DÉCLARÉ. S'il se mettait à bloquer, ㉞ refuserait un document honnête.
    if [[ "$(basename "$f")" == "2026-06-10_lecon-enneagramme_02_declaree.docx" ]]; then
      if grep -q "LE NOM DE DOMAINE NE RESOUT PAS" "$CUR/$(basename "$f" .docx).txt"; then
        echo "        ↳ ✗ ㉞ MORD À TORT : le lien est déclaré « ⛔ LIEN MORT … NE RESOUT PAS » dans le"
        echo "          document, et A6 le signale quand même — l'exemption de déclaration est cassée."
        STATUT=1
      else
        echo "        ↳ ✓ l'exemption de ㉞ tient : un lien mort déclaré ne bloque pas"
      fi
    fi
    if [[ "$(basename "$f")" == "2026-10-10_lecon-placement-financier_18_passeD.docx" ]]; then
      TD="$CUR/$(basename "$f" .docx).txt"
      # le séparateur est l'une des trois espaces que le contrôle neutralise (normale, insécable, fine) :
      # une virgule ne doit PAS compter, sinon « OK 0,625 » serait pris pour un nombre à séparateur.
      D_OK=$(grep -cE '^ +OK +[0-9]{1,3}[   ][0-9]{3}' "$TD")
      D_KO=$(grep -cE '^ +A VERIFIER [0-9]{1,3}[   ][0-9]{3}' "$TD")
      # ⚠️ SEUIL RAMENÉ DE 3 À 1 LE 11/10/2026, et ce n'est pas un affaiblissement : c'est la
      #    découverte que ce témoin reposait sur du CONTENU DE MARQUEUR. « 38 400 » et
      #    « 16 060,24 » ne figurent, dans ce document, que dans le marqueur du ¶110, qui cite
      #    l'exemple de service-public.fr. Depuis que la passe D écarte les marqueurs comme B et
      #    B-FR le font, elle ne les voit plus — à juste titre. Le seul nombre à séparateur du
      #    CORPS en contexte d'attribution est « 1 782 » (¶26). Exiger 3 reviendrait à exiger que
      #    la passe D relise les marqueurs.
      # 🧪 LA FORCE PERDUE EST REPRISE PAR UNE SECONDE EXIGENCE DE LIGNE : la ligne d'exemption
      #    doit être là ET nommer au moins deux nombres à séparateur. Ce témoin prouve donc
      #    maintenant les DEUX correctifs du même coup — le séparateur de milliers (10/10) et
      #    l'exclusion des marqueurs (11/10).
      D_EXEMPT=$(grep -cE 'valeur\(s\) ecartee\(s\) : elles ne figurent que dans un marqueur' "$TD")
      D_EXSEP=$(grep -oE 'un chiffre cite POUR MEMOIRE.*' "$TD" | grep -oE '[0-9]{1,3}[   ][0-9]{3}' | wc -l | tr -d ' ')
      if [ "$D_OK" -ge 1 ] && [ "$D_KO" = "0" ] && [ "$D_EXEMPT" -ge 1 ] && [ "$D_EXSEP" -ge 2 ]; then
        echo "        ↳ ✓ passe D tient : $D_OK nombre(s) à séparateur apparié(s), 0 donné pour absent,"
        echo "          et $D_EXSEP nombre(s) à séparateur écarté(s) parce qu'ils ne vivent que dans un marqueur"
      else
        echo "        ↳ ✗ PASSE D A PERDU SA DENT : $D_OK apparié(s) (1 au minimum), $D_KO donné(s) pour"
        echo "          absent(s) — « 1 782 » est sur sa page —, ligne d'exemption des marqueurs : $D_EXEMPT,"
        echo "          dont $D_EXSEP nombre(s) à séparateur (2 au minimum : « 38 400 » et « 16 060,24 »,"
        echo "          qui ne vivent que dans le marqueur du ¶110)."
        echo "          Ce témoin sort en 0 de toute façon : la passe D n'est pas bloquante. Lis sa section D."
        STATUT=1
      fi
    fi
  done
  if [ "$CONF_N" != "$ATTENDU_CONFORMES" ]; then
    echo "  ✗ $CONF_N témoin(s) conforme(s) contrôlé(s), $ATTENDU_CONFORMES attendu(s) — un document vivant a changé"
    echo "    de nom ou de dossier, ou une copie figée manque : rétablis-le, ou mets ATTENDU_CONFORMES à jour."
    STATUT=1
  else
    echo "  ✓ $CONF_N/$ATTENDU_CONFORMES témoin(s) conforme(s) contrôlé(s)"
  fi
  # témoins d'AVANT correction pour le contrôle complet : ils doivent sortir en 1 (une citation prêtée à la
  # mauvaise page, ㉓ — veille iMac du 13/09/2026). Un témoin qui sort en 0 = le contrôle a perdu une dent.
  echo "▶ Témoins d'attributions d'avant correction (doivent sortir en 1)…"
  AVANT_N=0
  for f in "$ROOT"/outils/scripts/non_regression/temoins_attributions_avant_correction/*.docx(N); do
    [ -e "$f" ] || continue
    AVANT_N=$((AVANT_N+1))
    controle_complet "$f" "$CUR/temoin_attr_$(basename "$f" .docx).txt"; rc=$?
    case $rc in 1) l="✓ exit 1";; 3) l="⟳ exit 3 après $ESSAIS essais — la page de la source nommée n'a pas été lue, rien prouvé : relancer --complet";; *) l="✗ exit $rc — le témoin ne bloque plus"; STATUT=1;; esac
    [ "$ESSAIS" = "2" ] && [ "$rc" != "3" ] && l="$l (au 2e essai)"
    echo "  $l  $(basename "$f")  ($(grep -m1 'MAL ATTRIBUEE\|^ *INTERDIT\|^ *ABSENTE ' "$CUR/temoin_attr_$(basename "$f" .docx).txt" | cut -c1-90))"
    # ⚠️ UN TÉMOIN QUI SORT EN 1 NE DIT PAS POURQUOI (25/09/2026). Celui de la leçon
    #    appli-ia n°05 a plusieurs défauts : il sortirait en 1 sur sa seule citation
    #    anglaise absente, même si la passe C2 perdait toute sa dent. Or c'est LUI qui
    #    garde C2, la seule passe dont le sens REFUS n'avait aucun témoin permanent.
    #    On exige donc la LIGNE, pas seulement le code de sortie — même exigence que
    #    « lis la sortie, ne te contente pas du code de retour » (JOBS.md, 12/09/2026).
    # ⚠️ MÊME EXIGENCE POUR ㉜ (09/10/2026) : ce témoin sortirait en 1 sur la seule citation de Palmer,
    #    que ㉖ attrape. Ce qui prouve ㉜, c'est la LIGNE qui nomme l'ouvrage.
    if [[ "$(basename "$f")" == "2026-07-08_lecon-enneagramme_06_avant.docx" ]]; then
      if grep -q "SOURCE NOMMÉE SANS PAGE" "$CUR/temoin_attr_$(basename "$f" .docx).txt"; then
        echo "        ↳ ✓ ㉜ tient : $(grep -c "SOURCE NOMMÉE SANS PAGE" "$CUR/temoin_attr_$(basename "$f" .docx).txt") citation(s) prêtée(s) à un ouvrage toujours nommée(s)"
      else
        echo "        ↳ ✗ ㉜ A PERDU SA DENT : aucune citation prêtée à un ouvrage n'est plus signalée."
        echo "          Ce témoin sort en 1 pour la citation de Palmer (㉖) — lis sa sortie complète."
        STATUT=1
      fi
    fi
    # ⚠️ MÊME EXIGENCE POUR ㉞ (11/10/2026) : ce témoin n'a qu'UN défaut, et c'est le lien mort.
    #    S'il sortait en 1 pour autre chose, on ne saurait pas que A6 a perdu le HTTP 000 — d'où la LIGNE.
    if [[ "$(basename "$f")" == "2026-06-10_lecon-enneagramme_02_avant.docx" ]]; then
      if grep -q "LE NOM DE DOMAINE NE RESOUT PAS" "$CUR/temoin_attr_$(basename "$f" .docx).txt"; then
        echo "        ↳ ✓ ㉞ tient : le nom de domaine qui ne résout pas est toujours un lien mort"
      else
        echo "        ↳ ✗ ㉞ A PERDU SA DENT : www.davidstamile.com ne résout pas (HTTP 000, curl 6) et"
        echo "          n'est plus signalé. A6 est redevenue aveugle au 000 — lis sa section A6."
        STATUT=1
      fi
    fi
    if [[ "$(basename "$f")" == "2026-08-28_lecon-appli-ia_05.docx" ]]; then
      if grep -q "INTERDIT   8.2.2" "$CUR/temoin_attr_$(basename "$f" .docx).txt"; then
        echo "        ↳ ✓ C2 tient : « 8.2.2 près de vite.dev/guide » toujours INTERDIT"
      else
        echo "        ↳ ✗ C2 A PERDU SA DENT : « 8.2.2 près de vite.dev/guide » n'est plus refusé."
        echo "          Ce témoin sort peut-être en 1 pour une autre raison — lis sa sortie complète."
        STATUT=1
      fi
    fi
  done
  if [ "$AVANT_N" != "$ATTENDU_AVANT" ]; then
    echo "  ✗ $AVANT_N témoin(s) contrôlé(s), $ATTENDU_AVANT attendu(s) — un lot incomplet ne prouve rien :"
    echo "    rétablis le ou les témoins manquants, ou mets ATTENDU_AVANT à jour dans ce script."
    STATUT=1
  else
    echo "  ✓ $AVANT_N/$ATTENDU_AVANT témoin(s) d'avant correction contrôlé(s)"
  fi

  # ── 5 ter. LES TROIS ÉTAPES 5 BIS SORTIES DES PROMPTS — QUATRE DUOS ─────────
  # `controle_astrologie_karmique.py` (7 motifs) et `controle_psychopathologie.py`
  # (4 motifs) étaient inlinés dans leurs prompts — 12 398 et 5 520 octets réémis à
  # chaque tour. Sortis le 08/10/2026, ils sont devenus des scripts du dépôt que
  # PLUS AUCUN HARNAIS NE TESTAIT : une retouche de l'un des deux ne se serait vue
  # nulle part. Chacun se prouve ici DANS LES DEUX SENS.
  #   • un témoin CONFORME doit sortir en 0 (le contrôle laisse passer ce qui est juste) ;
  #   • une MUTATION du même document, fabriquée par muter_docx.py et détruite après,
  #     doit sortir en 1 (le contrôle mord encore).
  # ⚠️ POURQUOI UNE MUTATION ET PAS UN TÉMOIN FIGÉ DE REFUS. Au 08/10/2026, les seuls
  # documents que controle_astrologie_karmique.py refusait le faisaient sur SIX FAUX POSITIFS
  # du motif ⑤ — des exonymes français (« Cérès » pour « Ceres », « Alger » pour « Algiers »,
  # « Centre » pour « Center ») et l'étiquette de section « Citation » ; figer un de ces refus
  # aurait inscrit le bug dans le harnais, qui aurait échoué le jour de sa correction. 🟢 CE
  # JOUR EST ARRIVÉ LE 09/10/2026 : le correctif du prompt `stoicisme` a été porté, les six
  # faux positifs ont disparu, et la leçon n°10 sort désormais en 0. Le raisonnement ci-dessus
  # est donc HISTORIQUE — mais la mutation reste le bon instrument, pour une autre raison : un
  # témoin figé de refus prouve qu'un contrôle refuse encore un document DONNÉ, la mutation
  # prouve qu'il refuse encore une FAUTE, et c'est elle qui survit à une correction du document.
  # ⚠️ ET LA MUTATION DOIT TOMBER LÀ OÙ LE MOTIF REGARDE. Le motif ⑤ n'examine que les
  # paragraphes qui portent un lien dont la page répond 200 : un paragraphe AJOUTÉ en fin de
  # document ne l'atteint jamais. D'où le motif « nompropre », qui MODIFIE le premier paragraphe
  # à la fois lié et porteur d'un marqueur de source. Mesuré le 09/10/2026 : il sort en 1 sur le
  # seul motif ⑤.
  # ⚠️ EN --complet SEULEMENT : ces scripts rouvrent CHAQUE page listée du document (dix
  # pour la leçon d'astrologie, dont quatre fiches du MPC de 600 000 à 900 000 caractères ;
  # douze pour la veille ai-act, en 5 s). En --docs, qui est la porte des pushs de job et
  # doit rester en secondes, ils n'ont rien à faire.
  # 🆕 09/10/2026 — TROISIÈME DUO : controle_ai_act.py (11 motifs, 12 303 octets), sorti du
  # prompt d'ai-act-veille le même jour. Sa mutation est « alerte » : un paragraphe
  # « 🟢 Niveau d'alerte : VERT » injecté dans une note qui annonce des faits marquants,
  # ce qui déclenche son motif (6) — le seul des onze qui ne coûte AUCUN appel réseau.
  # ⚠️ ET CE CÂBLAGE A RÉVÉLÉ UN BUG DE muter_docx.py, resté invisible depuis le 08/10 :
  # sa branche « document portant un journal des corrections » insérait la mutation entre
  # <w:p> et <w:pPr> du paragraphe du titre, qui n'était alors plus un <w:p>…</w:p>
  # complet ; plus aucun paragraphe ne contenait « Journal des corrections », et le
  # contrôle lisait tout le journal. Le mutant restait un XML valide, donc rien ne le
  # disait, et le témoin d'astrologie n°09 — qui porte un journal — passait depuis deux
  # jours sur un document malformé. Corrigé : on repère le SPAN du paragraphe, et
  # muter_docx.py vérifie désormais l'XML, l'équilibre des <w:p> et la position de la
  # mutation avant le journal.
  echo "▶ Étapes 5 bis du dépôt (témoin conforme en 0, mutation en 1)…"
  # Quatre duos pour trois scripts : l'astrologie en a DEUX, et SUR DEUX DOCUMENTS DIFFÉRENTS.
  #   • n°09 + « ligature » → prouve que le motif ① mord ;
  #   • n°10 + « nompropre » → prouve que le motif ⑤ mord.
  # ⚠️ LE CHOIX DE LA n°10 N'EST PAS INDIFFÉRENT, c'est lui qui garde le correctif des exonymes
  # dans L'AUTRE SENS. La n°10 est le document qui portait les six faux positifs du motif ⑤ ;
  # elle sort en 0 depuis le portage du 09/10/2026, et elle est la SEULE chose du dépôt qui
  # retomberait en 1 si quelqu'un défaisait sa (sa(), EXO_, STRUCT_). Une mutation prouve qu'un
  # contrôle MORD ; un témoin conforme bien choisi prouve qu'il NE MORD PAS À TORT — il fallait
  # les deux, et c'est pourquoi ce duo-là ne réutilise pas le témoin de « ligature ».
  # Coût : 11 s par passage du contrôle astro, mesuré — négligeable sur un --complet de 7 min.
  # 6 depuis le 10/10/2026 : deux duos ajoutés sur controle_ai_act.py en portant norm4 — « citation »
  # (le motif (1) doit continuer à refuser une citation fabriquée) et « 0:typo » (il ne doit PAS
  # refuser une citation que la page écrit avec une espace avant sa ponctuation).
  ATTENDU_5BIS=7
  CB_N=0
  MUTDIR=$(mktemp -d "${TMPDIR:-/tmp}/nr5bis.XXXXXX")
  # Le chemin du témoin est relatif à la racine du dépôt : le troisième duo est une VEILLE,
  # pas une leçon, et l'ancien préfixe livrables/lecons/ était codé en dur (09/10/2026).
  for duo in \
    "controle_astrologie_karmique.py|livrables/lecons/astrologie-karmique/2026-10-01_lecon-astrologie-karmique_09_chiron-corps-reel-blessure-symbolique.docx|ligature" \
    "controle_psychopathologie.py|livrables/lecons/psychopathologie/2026-10-05_lecon-psychopathologie_19_ethique-consentement-contrainte-sante-mentale.docx|fraction" \
    "controle_ai_act.py|sources/veille/ai-act/2026-10-09_veille_ai-act.docx|alerte" \
    "controle_astrologie_karmique.py|livrables/lecons/astrologie-karmique/2026-10-08_lecon-astrologie-karmique_10_lilith-points-fictifs-statut-objets.docx|nompropre" \
    "controle_ai_act.py|sources/veille/ai-act/2026-10-09_veille_ai-act.docx|citation" \
    "controle_ai_act.py|sources/veille/ai-act/2026-10-09_veille_ai-act.docx|0:typo" \
    "controle_ai_act.py|sources/veille/ai-act/2026-10-09_veille_ai-act.docx|taille"; do
    SC="${duo%%|*}"; RESTE="${duo#*|}"; REL="${RESTE%%|*}"; MOTIF="${RESTE##*|}"
    # ⚠️ CONVENTION « 0:motif » (10/10/2026) : le mutant doit être ACCEPTÉ, pas refusé. Un
    #    normaliseur qu'on ÉLARGIT doit se prouver DANS LES DEUX SENS — une mutation qui doit
    #    sortir en 1 garde sa dent, une mutation qui doit sortir en 0 garde l'élargissement.
    #    Sans la seconde, rien n'empêche de resserrer le normaliseur demain : les quatre autres
    #    duos continueraient de passer.
    ATTENDU_MUT=1
    case "$MOTIF" in 0:*) ATTENDU_MUT=0; MOTIF="${MOTIF#0:}";; esac
    DOC="$ROOT/$REL"
    if [ ! -f "$DOC" ] || [ ! -f "$ROOT/outils/scripts/$SC" ]; then
      echo "  ✗ $SC : témoin ou script introuvable ($REL) — rétablis-le, ou mets ce bloc à jour."
      STATUT=1; continue
    fi
    CB_N=$((CB_N + 1))
    env -i /usr/bin/python3 "$ROOT/outils/scripts/$SC" "$DOC" > "$CUR/5bis_$MOTIF.txt" 2>&1; rc=$?
    if [ "$rc" != "0" ]; then
      echo "  ✗ $SC : le témoin conforme sort en $rc — faux positif du contrôle : $(tail -1 "$CUR/5bis_$MOTIF.txt")"
      STATUT=1
    else
      MUT="$MUTDIR/mutant_$MOTIF.docx"
      if ! /usr/bin/python3 "$NR/muter_docx.py" "$DOC" "$MUT" "$MOTIF" > /dev/null 2>&1; then
        echo "  ✗ $SC : la mutation « $MOTIF » n'a pas pu être fabriquée — rien n'est prouvé."
        STATUT=1
      else
        env -i /usr/bin/python3 "$ROOT/outils/scripts/$SC" "$MUT" > "$CUR/5bis_mut_$MOTIF.txt" 2>&1; rcm=$?
        if [ "$rcm" = "$ATTENDU_MUT" ]; then
          echo "  ✓ $SC : témoin conforme exit 0, mutation « $MOTIF » exit $ATTENDU_MUT$([ "$ATTENDU_MUT" = "0" ] && echo " (acceptation attendue)")"
        elif [ "$ATTENDU_MUT" = "0" ]; then
          echo "  ✗ $SC : la mutation « $MOTIF » sort en $rcm au lieu de 0 — LE CONTRÔLE MORD À TORT"
          echo "    (une citation que la page écrit avec une espace avant sa ponctuation est refusée :"
          echo "     le portage de norm4 a été défait, ou resserré)"
          echo "    $(tail -1 "$CUR/5bis_mut_$MOTIF.txt")"
          STATUT=1
        else
          echo "  ✗ $SC : la mutation « $MOTIF » sort en $rcm au lieu de 1 — LE CONTRÔLE NE MORD PLUS"
          echo "    $(tail -1 "$CUR/5bis_mut_$MOTIF.txt")"
          STATUT=1
        fi
      fi
      rm -f "$MUT"
    fi
  done
  rmdir "$MUTDIR" 2>/dev/null
  if [ "$CB_N" != "$ATTENDU_5BIS" ]; then
    echo "  ✗ $CB_N étape(s) 5 bis contrôlée(s), $ATTENDU_5BIS attendue(s) — un lot incomplet ne"
    echo "    prouve rien : rétablis le script ou le témoin manquant, ou mets ATTENDU_5BIS à jour."
    STATUT=1
  fi

  # ── 5 ter bis. DÉLIMITATION DES BLOCS D'ARTICLE DE controle_ai_act.py (16/10/2026) ──
  # Le motif (2) confrontait au lien de SON bloc des noms d'actes et des citations
  # appartenant aux blocs SUIVANTS : le corps d'un bloc s'arrêtait à la première ligne vide,
  # or la veille du 16/10 n'en met aucune entre ses articles. Le corps de l'« Article 1 »
  # courait sur 10 569 caractères au lieu de 1 392, et la note recevait DEUX refus bloquants
  # pour des chaînes qui ne sont pas les siennes — dont « Publication 09 October 2026 », que
  # la passe B-FR appariait en OK au même moment sur la bonne page. Les deux contrôles se
  # contredisaient, et c'était celui-ci qui avait tort.
  # ⚠️ CE TÉMOIN NE PEUT PAS ÊTRE JUGÉ SUR SON SEUL CODE DE SORTIE : il sort en 1 AVANT comme
  #    APRÈS le correctif, puisqu'il garde un refus légitime — « EU AI Act » prêté à un
  #    article qui parle de l'« EU AI Office ». C'est la LIGNE qui est exigée, et dans LES
  #    DEUX SENS : une ligne INTERDITE (le lien de l'Article 1, qui ne doit plus apparaître
  #    dans aucun refus) et une ligne REQUISE (le refus légitime, qui doit subsister).
  #    Sans la ligne interdite, on ne saurait pas que le saignement de bloc est revenu ;
  #    sans la ligne requise, un motif entièrement mort passerait pour corrigé.
  echo "▶ Délimitation des blocs d'article de controle_ai_act.py (16/10/2026)"
  BL_D="$ROOT/outils/scripts/non_regression/temoins_ai_act_blocs"
  BL_F="$BL_D/2026-10-16_veille_ai-act_blocs.docx"
  if [ -f "$BL_F" ]; then
    BL_OUT="$CUR/ai_act_blocs.txt"
    env -i $PY "$ROOT/outils/scripts/controle_ai_act.py" "$BL_F" > "$BL_OUT" 2>&1
    BL_RC=$?
    # ⚠️ DEUX LIGNES INTERDITES — une par saignement, car il y en avait DEUX :
    #    ① le lien de l'« Article 1 », quand le corps courait jusqu'à la première ligne vide ;
    #    ② tout « ACTE NOMMÉ ABSENT », car l'acte « EU AI Act » venait du titre d'une AUTRE
    #       source avalée par le dernier bloc. Cette copie figée n'a aucun refus d'acte juste.
    # ET UNE LIGNE REQUISE : le refus d'héritage, qui est le VRAI défaut que cette copie
    #    conserve — le paragraphe DDADUE sans lien ni « non vérifié ». Sans elle, un motif
    #    entièrement mort passerait pour corrigé.
    BL_SAIGNE=$(grep -c "special-meeting-ai-scientific-panel" "$BL_OUT")
    BL_ACTE=$(grep -c "ACTE NOMMÉ ABSENT" "$BL_OUT")
    BL_VRAI=$(grep -c "HÉRITAGE SANS SOURCE NI RÉSERVE" "$BL_OUT")
    if [ "$BL_RC" = 1 ] && [ "$BL_SAIGNE" = 0 ] && [ "$BL_ACTE" = 0 ] && [ "$BL_VRAI" -ge 1 ]; then
      echo "  ✓ les blocs tiennent : aucun refus prêté à un autre bloc, et le vrai défaut subsiste"
    else
      [ "$BL_SAIGNE" != 0 ] && echo "  ✗ LE SAIGNEMENT DE BLOC EST REVENU : $BL_SAIGNE refus prêté(s) au lien de"
      [ "$BL_SAIGNE" != 0 ] && echo "    l'Article 1 pour des chaînes qui appartiennent aux blocs suivants."
      [ "$BL_ACTE" != 0 ] && echo "  ✗ $BL_ACTE refus d'ACTE : le dernier bloc avale de nouveau le titre d'une"
      [ "$BL_ACTE" != 0 ] && echo "    autre source (« Timeline for the Implementation of the EU AI Act »)."
      [ "$BL_VRAI" = 0 ] && echo "  ✗ le vrai défaut a disparu : le paragraphe DDADUE sans lien ni « non vérifié »"
      [ "$BL_VRAI" = 0 ] && echo "    n'est plus refusé — le motif (5) ne mord plus du tout."
      [ "$BL_RC" != 1 ] && echo "  ✗ code de sortie $BL_RC, 1 attendu"
      STATUT=1
    fi
  else
    echo "  ✗ témoin absent : $BL_F"
    STATUT=1
  fi

  # ── 5 quater. RELECTURE À L'ÉDITION PRÉCÉDENTE ET À SA FICHE (12/10/2026) ────
  # `controle_edition_precedente.py` est le premier contrôle du dépôt qui regarde AILLEURS que
  # dans le document qu'on lui donne. Il n'est donc PAS dans la référence (passe_A.tsv ne stocke
  # que les passes A/A2/A3/A4 d'un document isolé) : comme ㉜, la passe D, ㉞ et ㉟, il lui faut
  # son témoin et une EXIGENCE DE LIGNE.
  # LE DUO EST UN VRAI INCIDENT, FIGÉ DANS LES DEUX ÉTATS. L'entrée 7 du journal de la veille
  # iMac du 04/10/2026 retirait « TSMC » du procédé du M6, « le fondeur n'étant pas nommé sur la
  # page citée ». L'édition du 11/10 l'a réécrit « 2 nm (TSMC N2) » — correction défaite, sept
  # jours plus tard, dans le document même que la note avait relu pour sa continuité.
  #   • temoins_edition_precedente/rejeu/      : le 11/10 AVANT correction → doit sortir en 1
  #     ET porter la ligne « INTERDIT « TSMC » ». Sans la ligne, n'importe quel autre jeton
  #     ferait passer le témoin : le code de sortie seul ne prouve pas QUEL rejeu est vu.
  #   • temoins_edition_precedente/conforme/   : le 11/10 APRÈS correction → doit sortir en 0.
  # Chaque dossier porte sa propre copie de l'édition N-1 et de la FICHE de celle-ci, puisque le
  # contrôle les cherche à côté du document : deux fichiers de même nom ne peuvent pas cohabiter.
  echo "▶ Relecture à l'édition précédente (rejeu en 1 avec sa ligne, conforme en 0)…"
  # 🔴 TROISIÈME TÉMOIN AJOUTÉ LE 14/10/2026, APRÈS UN FAUX REFUS EN PRODUCTION. Le contrôle a
  # refusé trois fois le push du job serafin-ph-veille du 14/10 sur deux jetons — « Inaccessible »
  # (de « ⛔ Inaccessible (404) ») et « Semaine » (de « Semaine creuse ») : deux mots ordinaires,
  # capitalisés parce qu'ils ouvrent une cellule, et que la série emploie chaque semaine. La borne a
  # été resserrée (dénonciation EXIGÉE, et jeton hors tête de citation). ⚠️ ET LES DEUX TÉMOINS
  # EXISTANTS NE GARDENT PAS CE RESSERREMENT : sabotage vérifié le 14/10/2026 — en retirant
  # l'exigence de dénonciation, « rejeu » sort toujours en 1 AVEC sa ligne TSMC et « conforme »
  # toujours en 0, tandis que la paire SERAFIN rebascule en 1. C'est la même leçon que la convention
  # « 0: » du 10/10 : un motif qu'on RESSERRE a besoin d'un témoin qui doit être ACCEPTÉ, sinon rien
  # n'empêche de le réélargir demain et de refuser à nouveau un livrable juste.
  ATTENDU_EDPREC=3
  EP_N=0; EPD="$NR/temoins_edition_precedente"
  for cas in "rejeu|1|INTERDIT « TSMC »|2026-10-11_veille_imac.docx|2026-10-04_veille_imac" \
             "conforme|0||2026-10-11_veille_imac.docx|2026-10-04_veille_imac" \
             "faux_refus|0||2026-10-14_veille_SERAFIN-PH.docx|2026-10-07_veille_SERAFIN-PH"; do
    NOM="${cas%%|*}"; RST="${cas#*|}"; ATT="${RST%%|*}"; RST2="${RST#*|}"
    LIGNE="${RST2%%|*}"; RST3="${RST2#*|}"; FICH="${RST3%%|*}"; PREC="${RST3##*|}"
    DOC="$EPD/$NOM/$FICH"
    if [ ! -f "$DOC" ] || [ ! -f "$EPD/$NOM/$PREC.docx" ] \
       || [ ! -f "$EPD/$NOM/$PREC.fiche.md" ]; then
      echo "  ✗ témoin « $NOM » incomplet — il lui faut l'édition N, l'édition N-1 et la fiche de N-1."
      STATUT=1; continue
    fi
    EP_N=$((EP_N + 1))
    env -i /usr/bin/python3 "$ROOT/outils/scripts/controle_edition_precedente.py" "$DOC" \
        > "$CUR/edprec_$NOM.txt" 2>&1; rc=$?
    if [ "$rc" != "$ATT" ]; then
      echo "  ✗ témoin « $NOM » sort en $rc au lieu de $ATT — $(tail -1 "$CUR/edprec_$NOM.txt")"
      [ "$ATT" = "1" ] && echo "    LA RELECTURE NE MORD PLUS : une correction défaite ne serait plus vue."
      [ "$ATT" = "0" ] && echo "    LA RELECTURE MORD À TORT : une édition honnête serait refusée$([ "$NOM" = "faux_refus" ] && echo " — c'est le faux refus du 14/10/2026 qui revient")."
      STATUT=1
    elif [ -n "$LIGNE" ] && ! grep -q "$LIGNE" "$CUR/edprec_$NOM.txt"; then
      echo "  ✗ témoin « $NOM » sort bien en 1, mais SANS la ligne « $LIGNE » :"
      echo "    le code de sortie ne dit pas QUEL rejeu est vu — le jeton attendu n'est plus détecté."
      STATUT=1
    else
      echo "  ✓ témoin « $NOM » exit $ATT$([ -n "$LIGNE" ] && echo " avec sa ligne « $LIGNE »")"
    fi
  done
  if [ "$EP_N" != "$ATTENDU_EDPREC" ]; then
    echo "  ✗ $EP_N témoin(s) de relecture contrôlé(s), $ATTENDU_EDPREC attendu(s) — rétablis le"
    echo "    dossier manquant, ou mets ATTENDU_EDPREC à jour."
    STATUT=1
  fi
fi
# ---- Témoins de supprimer_job.sh (15/10/2026) ----
# supprimer_job.sh exécute les SIX gestes d'une suppression de job, et son GARDE-FOU est la
# seule chose qui l'empêche de partir trop tôt : il appelle controle_clauses_parcours.py et
# refuse tant que les leçons réelles sont sous le compte annoncé. Sans témoin, personne ne
# saurait que ce garde-fou a cessé de mordre — et le prix d'un garde-fou muet est un BILAN
# de parcours jamais produit, comme l'inverse a déjà coûté une 11e leçon à revenus-passifs.
# ⚠️ CES TÉMOINS N'EXERCENT QUE LES DIRECTIONS LISIBLES SEULES, et c'est délibéré : le chemin
#    --confirmer écrit dans jobs_config.json, relance setup_launchd.sh et retire un .plist du
#    HOME. Le jouer ici endommagerait launchd pour de vrai. CE QUI RESTE DONC NON COUVERT :
#    que les six gestes soient tous accomplis. Cela a été validé à la main le 15/10/2026 sur
#    les trois suppressions du jour, et l'est à chaque usage par les vérifications finales du
#    script (config, .plist et launchctl doivent concorder ; ids du skill = ids de la config).
# Sans réseau, sans jeton, moins d'une seconde. Pas en --docs : c'est la porte des documents.
if [ "$MODE" != "--docs" ] && [ -x "$ROOT/outils/scripts/supprimer_job.sh" ]; then
  echo "▶ Témoins de supprimer_job.sh (le garde-fou doit refuser avant le bilan)"
  SJ="$ROOT/outils/scripts/supprimer_job.sh"
  SJ_KO=0
  # La config de test déclare pour astrologie-karmique le nombre de leçons RÉELLEMENT sur le
  # disque : le parcours y est donc complet, et le garde-fou doit laisser passer. Fabriquée
  # ici puis détruite, comme une mutation — un témoin figé se périmerait à chaque leçon.
  SJ_CFG="$CUR/cfg_parcours_complet.json"
  env -i $PY - "$ROOT" "$SJ_CFG" <<'PYSJ'
import glob, json, re, sys
racine, dst = sys.argv[1], sys.argv[2]
d = json.load(open(racine + "/jobs_config.json", encoding="utf-8"))
n = len(glob.glob(racine + "/livrables/lecons/astrologie-karmique/*.docx"))
for x in d["jobs"]:
    if x["id"] == "astrologie-karmique-lecon":
        x["prompt"] = re.sub(r"\b12 LEÇONS", "%d LEÇONS" % n, x["prompt"])
        x["prompt"] = re.sub(r"limite de 12", "limite de %d" % n, x["prompt"])
json.dump(d, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
PYSJ
  # scénario | code attendu | motif exigé dans la sortie (vide = aucun)
  for cas in "refus_avant_bilan|1|il manque|astrologie-karmique-lecon|" \
             "parcours_complet|0|le parcours a atteint|astrologie-karmique-lecon|--config $SJ_CFG" \
             "job_inconnu|3|job inconnu|job-qui-nexiste-pas|" \
             "usage_sans_argument|2|Usage|  |" \
             "confirmer_avec_config|2|agissent sur le dépôt réel|astrologie-karmique-lecon|--confirmer --config $SJ_CFG"; do
    IFS='|' read -r SJ_NOM SJ_ATT SJ_MOT SJ_JOB SJ_OPT <<< "$cas"
    SJ_OUT="$CUR/supprimer_job_$SJ_NOM.txt"
    # ⚠️ 15/10/2026 — « ${=SJ_OPT} » ET PAS « ${SJ_OPT} » : ce harnais est en ZSH, qui ne
    #    découpe PAS une expansion non quotée, contrairement à bash. Écrit sans le « = »,
    #    « --config /chemin » partait comme UN SEUL argument et supprimer_job.sh rendait
    #    « option inconnue » — exit 2 au lieu de 0, sur deux des cinq scénarios. Le témoin
    #    a donc commencé par accuser le script d'un défaut qui était dans le témoin.
    SJ_ARGS=(${=SJ_OPT})
    if [ "$SJ_JOB" = "  " ]; then
      "$SJ" > "$SJ_OUT" 2>&1; SJ_RC=$?
    else
      "$SJ" "$SJ_JOB" "${SJ_ARGS[@]}" > "$SJ_OUT" 2>&1; SJ_RC=$?
    fi
    if [ "$SJ_RC" != "$SJ_ATT" ]; then
      echo "  ✗ $SJ_NOM : exit $SJ_RC, $SJ_ATT attendu"
      SJ_KO=1
    elif [ -n "$SJ_MOT" ] && ! grep -qF "$SJ_MOT" "$SJ_OUT"; then
      echo "  ✗ $SJ_NOM : exit $SJ_ATT mais la sortie ne porte pas « $SJ_MOT »"
      echo "    Un code de sortie seul ne dit pas POURQUOI le script a refusé."
      SJ_KO=1
    fi
  done
  # ⚠️ ET LA VÉRIFICATION QUI COMPTE AUTANT QUE LES CINQ : aucun de ces appels ne doit avoir
  #    touché quoi que ce soit. Un garde-fou qui refuse APRÈS avoir écrit ne garde rien.
  SJ_SALE=$(cd "$ROOT" && git status --porcelain jobs_config.json outils/scripts/run_job.sh \
            outils/scripts/setup_launchd.sh .claude/skills/lancer-job/SKILL.md 2>/dev/null | wc -l | tr -d ' ')
  SJ_PLIST=$(ls "$HOME/Library/LaunchAgents"/com.claudetravail.*.plist 2>/dev/null | wc -l | tr -d ' ')
  SJ_JOBS=$(env -i $PY -c "import json;print(len(json.load(open('$ROOT/jobs_config.json'))['jobs']))")
  if [ "$SJ_SALE" != "0" ]; then
    echo "  ✗ les appels de plan ont MODIFIÉ $SJ_SALE fichier(s) suivi(s) — ils doivent être inertes"
    SJ_KO=1
  elif [ "$SJ_PLIST" != "$SJ_JOBS" ]; then
    echo "  ✗ $SJ_PLIST .plist pour $SJ_JOBS job(s) — un agent a été touché par un appel de plan"
    SJ_KO=1
  fi
  rm -f "$SJ_CFG"
  if [ "$SJ_KO" = 0 ]; then
    echo "  ✓ 5/5 scénarios — le garde-fou refuse avant le bilan, accepte un parcours complet,"
    echo "        et les appels de plan n'ont rien touché ($SJ_JOBS jobs, $SJ_PLIST .plist)"
  else
    STATUT=1
  fi
fi

# ---- Le classeur de suivi contre jobs_config.json (15/10/2026) ----
# Le classeur `livrables/documents/*_Les N Jobs.xlsx` est le SEUL endroit où un humain lit la
# liste des jobs, et c'était le seul que RIEN ne vérifiait : controle_clauses_parcours.py
# compare le prompt aux .docx, audit_vault.py les fiches aux documents, et personne ne
# comparait le classeur à la config. Résultat mesuré le 15/10/2026 : l'ancien classeur
# portait CINQ jobs supprimés et s'intitulait « Tes 14 jobs » pour 9 réels — parce que
# maj_xlsx_jobs.py, qui y écrit après chaque job réussi, ne met à jour QU'UNE COLONNE et ne
# touche jamais au jeu de lignes. Il est structurellement incapable de suivre une suppression.
# Sans réseau, instantané. Pas en --docs : c'est la porte des documents.
if [ "$MODE" != "--docs" ] && [ -x "$ROOT/outils/scripts/refaire_classeur.py" ]; then
  CL_OUT="$CUR/refaire_classeur.txt"
  if env -i $PY "$ROOT/outils/scripts/refaire_classeur.py" --verifier > "$CL_OUT" 2>&1; then
    grep -E "^ +✓" "$CL_OUT" | sed 's/^ */  /'
  else
    echo "▶ Classeur de suivi — DISCORDANCE avec jobs_config.json"
    grep -E "^ +✗|^ +→" "$CL_OUT" | sed 's/^ */  /'
    STATUT=1
  fi
fi

# ---- Témoins du runner (27/09/2026) ----
# run_job.sh décide ce qui est retenté et ce qui est PUBLIÉ pour les 14 jobs, et rien ne le
# testait : le fail-fast du plafond était mort depuis 19 jours sans qu'aucun contrôle puisse
# le dire. Sept scénarios de décision, quelques secondes, sans réseau ni jeton.
# Pas en mode --docs : celui-là est la porte des pushs de job, il reste focalisé sur les
# documents. Le job controle-livrables passe en --complet, donc la couverture est hebdomadaire.
# En --complet (le mode du job controle-livrables, qui accepte déjà 4-5 min de réseau) on
# joue AUSSI les mutations : 30 s au lieu de 4, et c'est la seule passe automatique qui
# vérifie que ces témoins mordent encore. En mode normal, les dix témoins seuls.
if [ "$MODE" != "--docs" ] && [ -x "$ROOT/outils/scripts/non_regression_runner.sh" ]; then
  RUNNER_ARGS=()
  [ "$MODE" = "--complet" ] && RUNNER_ARGS=(--mutations)
  if ! "$ROOT/outils/scripts/non_regression_runner.sh" "${RUNNER_ARGS[@]}"; then
    echo "  ✗ les témoins du runner ont changé de comportement (voir ci-dessus)"
    STATUT=1
  fi
fi

# dernière ligne, toujours : ce qui lit la sortie en arrière-plan (job controle-livrables) attend celle-ci —
# l'en-tête « Témoins d'attributions » s'imprime AVANT le dernier contrôle, il ne prouve pas la fin
echo "▶ Terminé — exit $STATUT"
exit $STATUT
