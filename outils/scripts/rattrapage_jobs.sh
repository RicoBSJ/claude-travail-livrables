#!/bin/bash
# ============================================================
# rattrapage_jobs.sh — Relance manuelle des jobs manqués
#
# À exécuter SUR LE MAC (chemins /Users/utilisateur/kDrive/Claude_Travail).
# Rejoue une liste de jobs via la vraie chaîne run_job.sh :
#   - chaque job garde son contrôle anti-doublon → aucun livrable dupliqué
#     s'il a déjà été produit aujourd'hui ;
#   - bénéficie du budget par-job et du push durci (voir run_job.sh) ;
#   - produit un livrable daté du JOUR d'exécution (une veille est un
#     instantané : on ne « rétro-date » pas au 05/07, on produit une veille
#     à jour ; les leçons reprennent simplement la suite du parcours).
#
# Usage :
#   bash outils/scripts/rattrapage_jobs.sh              # rejoue la liste ci-dessous
#   bash outils/scripts/rattrapage_jobs.sh dzogchen-lecon  # rejoue un seul job
#   bash outils/scripts/rattrapage_jobs.sh --manques       # INVENTAIRE : quels créneaux ont été
#                                                          # manqués ces 7 derniers jours ?
#                                                          # exit 0 si aucun, 1 sinon. Ne rejoue RIEN.
# ============================================================

set -u
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUN_JOB="$SCRIPT_DIR/run_job.sh"

if [ ! -x "$RUN_JOB" ]; then
  echo "❌ run_job.sh introuvable ou non exécutable : $RUN_JOB"
  echo "   (chmod +x \"$RUN_JOB\" puis relancer)"
  exit 1
fi

# ---- Inventaire des créneaux manqués (--manques, 20/10/2026) ------------
# POURQUOI. Le mardi 20/10/2026, le créneau de hypnose-lecon (9h03) n'a pas tourné : la machine
# avait démarré à 19h43, donc elle était ÉTEINTE à l'heure dite, et launchd NE RATTRAPE PAS un
# StartCalendarInterval manqué machine éteinte — contrairement à une mise en veille, où il part au
# réveil. Mesuré : plist chargé, créneau correct (Hour 9, Minute 3, Weekday 2), et pourtant
# « runs = 0 · last exit code = (never exited) », aucun log du jour, launchd.out/err vides et
# datés du 21 juin.
# 🔴 ET RIEN DANS LE DÉPÔT NE VOYAIT CE TROU : un créneau manqué ne produit AUCUN log, donc aucune
#    trace, donc aucun contrôle ne peut le constater. C'est le même angle mort que les liens
#    écartés, un étage au-dessus — l'absence de sortie n'est pas une sortie.
# ⚠️ ET LA LISTE DEFAULT_JOBS CI-DESSOUS EST LA PREUVE DU PROBLÈME : elle est figée depuis
#    juillet 2026 et porte encore deux jobs supprimés en commentaire. Une liste écrite à la main
#    périme ; la comparaison cron ↔ logs, non.
# CE QUE --manques COMPARE : pour chacun des 7 derniers jours, les créneaux que `jobs_config.json`
# prescrit (champ `cron`, forme « M H * * D ») contre la présence d'un log
# `logs/<job>_<AAAAMMJJ>_*.log`. Un créneau encore À VENIR aujourd'hui n'est pas un manque.
# Sort en 0 si tout est tracé, en 1 s'il manque quelque chose — comme `refaire_classeur.py
# --verifier`, pour pouvoir servir de garde un jour.
if [ "${1:-}" = "--manques" ]; then
  /usr/bin/python3 - "$SCRIPT_DIR" <<'PYMANQUES'
import glob, json, os, sys, datetime, re
SCRIPT_DIR = sys.argv[1]
RACINE = os.path.dirname(os.path.dirname(SCRIPT_DIR))
LOGS = os.path.join(SCRIPT_DIR, "logs")
JOURS = 7
cfg = json.load(open(os.path.join(RACINE, "jobs_config.json"), encoding="utf-8"))["jobs"]
plan = {}
for j in cfg:
    c = (j.get("cron") or "").split()
    # on n'accepte QUE la forme utilisée par les neuf jobs : minute heure * * jour-de-semaine.
    # Toute autre forme est dite, pas devinée — un rattrapage silencieusement faux est pire que rien.
    if len(c) != 5 or c[2] != "*" or c[3] != "*" or not re.fullmatch(r"\d", c[4] or ""):
        print("  ⚠️ cron non reconnu pour %s : %r — créneau NON vérifié" % (j["id"], j.get("cron")))
        continue
    plan.setdefault(int(c[4]), []).append((int(c[1]), int(c[0]), j["id"]))
maintenant = datetime.datetime.now()
aujourdhui = maintenant.date()
manques, lignes = [], []
for d in range(JOURS - 1, -1, -1):
    jour = aujourdhui - datetime.timedelta(days=d)
    dow = (jour.weekday() + 1) % 7          # python : lundi=0 ; cron : dimanche=0
    for h, m, jid in sorted(plan.get(dow, [])):
        quand = datetime.datetime.combine(jour, datetime.time(h, m))
        logs = glob.glob(os.path.join(LOGS, "%s_%s_*.log" % (jid, jour.strftime("%Y%m%d"))))
        if logs:
            etat = "✓ tracé"
        elif quand > maintenant:
            etat = "· à venir"
        else:
            etat = "⛔ MANQUÉ"
            manques.append(jid)
        lignes.append("  %s %s  %02dh%02d  %-28s %s"
                      % (jour.strftime("%a %d/%m"), "", h, m, jid, etat))
print("Créneaux prescrits sur les %d derniers jours, contre les logs présents :" % JOURS)
for l in lignes:
    print(l)
if manques:
    print("\n⛔ %d créneau(x) MANQUÉ(S) : %s" % (len(manques), " ".join(sorted(set(manques)))))
    print("   launchd ne rattrape pas un créneau passé machine éteinte. Pour les rejouer :")
    print("     bash outils/scripts/rattrapage_jobs.sh %s" % " ".join(sorted(set(manques))))
    print("   (anti-doublon actif, budget par job, push durci — et le livrable portera la date du jour)")
    sys.exit(1)
print("\n✓ tous les créneaux prescrits des %d derniers jours ont leur log" % JOURS)
PYMANQUES
  exit $?
fi

# ---- Liste des jobs à rattraper -----------------------------------------
# ⚠️ CETTE LISTE EST FIGÉE DEPUIS JUILLET 2026 et ne vaut plus comme défaut : utilise
#    `--manques` pour savoir ce qui a réellement été manqué, puis passe les ids en argument.
# Confirmé manquant (trou dans une semaine par ailleurs complète) :
# À confirmer via les logs (aucun push depuis le 08/07) — laissés actifs car
# l'anti-doublon les protège s'ils ont finalement tourné :
#   stoicisme-lecon             (jeudi 09/07)
#   placement-financier-lecon   (samedi 11/07)
#   entretien-motivationnel-lecon (jours intensifs 09→11/07)
# Commente (#) les lignes que tu ne veux PAS rejouer.
DEFAULT_JOBS=(
  # revenus-passifs-lecon  ← SUPPRIMÉ le 04/10/2026 (parcours clos à 10 leçons)
  stoicisme-lecon
  # appli-ia-lecon  ← SUPPRIMÉ le 04/10/2026 (parcours fermé, 12 leçons livrées)
  placement-financier-lecon
  astrologie-karmique-lecon
)

# Si un id de job est passé en argument, on ne rejoue que celui-là.
if [ "$#" -ge 1 ]; then
  JOBS=("$@")
else
  JOBS=("${DEFAULT_JOBS[@]}")
fi

echo "========================================================="
echo " Rattrapage de ${#JOBS[@]} job(s) — $(date '+%Y-%m-%d %H:%M:%S')"
echo " (anti-doublon actif : un job déjà fait aujourd'hui sera sauté)"
echo "========================================================="

declare -a RESULTS
for JOB in "${JOBS[@]}"; do
  echo ""
  echo "▶️  $JOB — démarrage…"
  if "$RUN_JOB" "$JOB"; then
    echo "✅ $JOB — terminé (voir le log pour doublon éventuel ou livrable produit)."
    RESULTS+=("✅ $JOB")
  else
    CODE=$?
    echo "⛔ $JOB — échec (code $CODE). Voir outils/scripts/logs/${JOB}_*.log"
    RESULTS+=("⛔ $JOB (code $CODE)")
  fi
  # Petite pause pour éviter les rafales d'appels API/push consécutifs.
  sleep 5
done

echo ""
echo "========================================================="
echo " Récapitulatif du rattrapage"
echo "========================================================="
for R in "${RESULTS[@]}"; do echo "  $R"; done
echo ""
echo "Vérifie les livrables produits :"
echo "  ls -t livrables/lecons/*/*.docx | head"
echo "  ls -t sources/veille/*/*.docx | head"
echo "Et l'état du push :"
echo "  git status -sb"
