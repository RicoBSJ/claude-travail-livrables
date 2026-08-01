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
# ============================================================

set -u
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUN_JOB="$SCRIPT_DIR/run_job.sh"

if [ ! -x "$RUN_JOB" ]; then
  echo "❌ run_job.sh introuvable ou non exécutable : $RUN_JOB"
  echo "   (chmod +x \"$RUN_JOB\" puis relancer)"
  exit 1
fi

# ---- Liste des jobs à rattraper -----------------------------------------
# Confirmé manquant (trou dans une semaine par ailleurs complète) :
# À confirmer via les logs (aucun push depuis le 08/07) — laissés actifs car
# l'anti-doublon les protège s'ils ont finalement tourné :
#   stoicisme-lecon             (jeudi 09/07)
#   placement-financier-lecon   (samedi 11/07)
#   entretien-motivationnel-lecon (jours intensifs 09→11/07)
# Commente (#) les lignes que tu ne veux PAS rejouer.
DEFAULT_JOBS=(
  revenus-passifs-lecon
  stoicisme-lecon
  appli-ia-lecon
  placement-financier-lecon
  entretien-motivationnel-lecon
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
echo "  ls -t livrables/lecons/ | head"
echo "  ls -t livrables/lecons/ | head"
echo "Et l'état du push :"
echo "  git status -sb"
