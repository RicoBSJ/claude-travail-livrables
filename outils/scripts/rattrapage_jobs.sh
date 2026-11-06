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
  # 🔴 23/10/2026 — SIGNAL DE VIVACITÉ EXACT, et il ne peut pas être le mtime du log.
  #    Pendant l'appel `claude -p`, run_job.sh n'écrit RIEN dans le log : le run du 16/10 a
  #    démarré à 09:03 et sa ligne suivante est de 09:32. Un log « frais » ne prouve donc pas
  #    qu'un run vit, et un log « vieux » ne prouve pas qu'il est mort. Le seul fait sûr est
  #    le PID que launchd tient pour le label du job.
  EN_COURS="$(launchctl list 2>/dev/null | awk '$1 ~ /^[0-9]+$/ && $3 ~ /claudetravail/ {print $3}' | sed 's/^com\.claudetravail\.//' | tr '\n' ',')"
  /usr/bin/python3 - "$SCRIPT_DIR" "$EN_COURS" <<'PYMANQUES'
import glob, json, os, sys, datetime, re
SCRIPT_DIR = sys.argv[1]
EN_COURS = {x for x in (sys.argv[2] if len(sys.argv) > 2 else "").split(",") if x}
RACINE = os.path.dirname(os.path.dirname(SCRIPT_DIR))
LOGS = os.path.join(SCRIPT_DIR, "logs")
JOURS = 7
# 🔴 23/10/2026 — UN LOG N'EST PAS UN RUN : IL FAUT SA LIGNE DE FIN.
#    Le 23/10, `ai-act-veille` a démarré à 09:03:01, la machine a été éteinte à 09:08, et le
#    log s'est arrêté à « Tentative 1/3 » — 438 octets, ni [diagnostic], ni [mesure], ni ligne
#    de fin, aucun livrable, aucun commit. `--manques` répondait « ✓ tracé » et sortait en 0 :
#    il vérifiait la PRÉSENCE d'un fichier, pas qu'un run soit allé au bout. L'outil écrit le
#    20/10 pour rendre visibles les créneaux manqués déclarait sain le seul créneau perdu de
#    la semaine. Il exige désormais l'épilogue de run_job.sh.
#    BORNE MESURÉE SUR LES 59 LOGS DU DOSSIER : un seul n'a pas de ligne de fin, celui du
#    23/10 — donc ZÉRO faux positif sur tout le corpus. Et la durée maximale observée d'un
#    run est de 1 967 s (32,8 min, appli-ia du 27/09), médiane 694 s : le délai au-delà
#    duquel un run sans épilogue est tenu pour interrompu est fixé à 3 600 s, soit 1,8 fois
#    le maximum observé. Un run encore vivant est reconnu par son PID chez launchd, pas par
#    ce délai — le délai ne sert qu'aux runs lancés à la main, hors launchd.
FIN = re.compile(r"^<<< .* — Fin du job .* \(code de sortie : (-?\d+)", re.M)
# 🔴 06/11/2026 — UN RUN N'EST PAS UNE PUBLICATION, et c'est la suite exacte du « un log
#    n'est pas un run » du 23/10. Le créneau imac du 25/10 a produit son livrable, l'a
#    committé, et son push a été REFUSÉ TROIS FOIS : `[git] ⛔ push ÉCHEC après 3 tentatives
#    — 2 commit(s) en avance sur origin/main`. L'épilogue portait pourtant `(code de sortie :
#    0, tentatives : 1)`, donc `--manques` répondait « ✓ tracé » : il lisait la PRÉSENCE de
#    l'épilogue sans jamais lire ce que run_job.sh écrit APRÈS lui. Et ㊳ ne pouvait rien
#    dire non plus : il juge l'EXÉCUTION, qui a bel et bien réussi.
#    📊 BORNE MESURÉE SUR LES 39 LOGS PRÉSENTS, PAS SUPPOSÉE : 19 portent `✅ push OK`,
#    5 portent `Rien de nouveau à committer`, 2 `Job en erreur`, 0 `PAS DE PUBLICATION` —
#    et **12, soit 31 %, portent la ligne d'échec**, tous avec un code de sortie 0, sur
#    SEPT jobs différents du 07/10 au 04/11. Les douze portent `pre-push : ✗ PUSH REFUSÉ`
#    trois fois : la cause dominante est le HOOK, pas le transport (deux seulement portent
#    aussi « Connection to github.com closed by remote host. »).
#    🔴 ET LE MÉCANISME EST UNE CASCADE : un document bloquant refuse le push du job qui
#    l'a produit, puis celui de TOUS les jobs suivants, qui héritent du même backlog —
#    d'où les « 2, 3, 5 commit(s) en avance ». `2026-10-07_veille_SERAFIN-PH.docx : 1
#    bloquant` a ainsi refusé serafin 07/10, enneagramme 07/10 et stoicisme 08/10.
#    ⛔ DÉTECTION POSITIVE, jamais par absence : on apparie la ligne que run_job.sh
#    n'écrit QUE dans cette branche (ligne 488). Un garde satisfait par un état cassé est
#    le défaut qui revient le plus dans ce dépôt — `$SEMENCE` non vide, les deux photos
#    vides, le `✅` sur un mur. Ici, pas de log = pas d'accusation.
#    ⛔ ET LA PORTÉE S'ARRÊTE AU RUN, PAS AU TRAVAIL : le backlog est presque toujours
#    poussé par le push du job SUIVANT (mesuré : le local n'est en avance que des commits
#    du jour). L'état dit donc « CE run n'a pas publié », ce que le log affirme, et non
#    « ce livrable est absent du distant », qui demanderait le réseau.
PUB_OK = re.compile(r"^\[git\] ✅ push OK", re.M)
PUB_ECHEC = re.compile(r"^\[git\] ⛔ push ÉCHEC après 3 tentatives — ([0-9?]+) commit\(s\) en avance", re.M)
PUB_HOOK = re.compile(r"^pre-push : ✗ PUSH REFUSÉ", re.M)
PUB_RESEAU = re.compile(r"Connection to github\.com closed by remote host\.")
SEUIL_EN_COURS = 3600
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
manques, interrompus, nonpublies, lignes = [], [], [], []

def juge(logs, quand):
    """-> (etat, id_du_motif). La question est « ce créneau a-t-il eu UN run complet ? », donc
       il suffit qu'UN des logs du jour porte l'épilogue — un run mort suivi d'un rattrapage
       réussi est servi, et un run réussi suivi d'un rattrapage mort l'est aussi.
       ⚠️ 23/10/2026 — la première version ne jugeait que le log le PLUS RÉCENT : elle aurait
       crié « INTERROMPU » sur un créneau servi à 08h03 dont un rattrapage manuel de 10h20
       était mort. Mesuré par deux logs fabriqués le même jour. Si AUCUN n'a d'épilogue, c'est
       le plus récent qui décide entre « en cours » et « interrompu »."""
    if any(FIN.search(open(f, encoding="utf-8", errors="replace").read()) for f in logs):
        return "✓ tracé", None
    dernier = max(logs)
    jid_ = os.path.basename(dernier).split("_")[0]
    if jid_ in EN_COURS:
        return "· en cours (launchd tient son PID)", None
    # ⚠️ 23/10/2026 — L'ÂGE SE COMPTE DEPUIS LE DÉMARRAGE DU LOG, PAS DEPUIS LE CRÉNEAU.
    #    Première version : age = maintenant − créneau prescrit. Un rattrapage lancé à la main
    #    quinze minutes plus tôt pour un créneau de 08h03 était donc déclaré INTERROMPU à
    #    10h20 — mesuré par un log fabriqué, et c'est la seule branche que les trois autres
    #    sens ne touchaient pas. Le nom du fichier porte l'heure réelle : <jid>_AAAAMMJJ_HHMMSS.
    depart = quand
    m_ = re.search(r"_(\d{8})_(\d{6})\.log$", dernier)
    if m_:
        depart = datetime.datetime.strptime(m_.group(1) + m_.group(2), "%Y%m%d%H%M%S")
    age = (maintenant - depart).total_seconds()
    if age < SEUIL_EN_COURS:
        return "· en cours ? démarré il y a %d min, pas d'épilogue" % (age // 60), None
    return "✗ INTERROMPU — aucune ligne de fin (%d o)" % os.path.getsize(dernier), "interrompu"
def publication(logs):
    """-> (suffixe, motif) pour un créneau DÉJÀ jugé « ✓ tracé ».
       Même règle de jour que juge() : il suffit qu'UN des logs du jour ait publié — un run
       refusé suivi d'un rattrapage qui passe est publié. Les quatre autres états terminaux
       de run_job.sh (`✅ push OK`, `Rien de nouveau à committer`, `PAS DE PUBLICATION`
       après un exit 7, `Job en erreur`) sont des SILENCES : les deux derniers n'ont rien à
       publier, et accuser un job en échec contredirait la borne du 23/10 — cet outil
       détecte un créneau perdu, pas un job raté."""
    textes = [open(f, encoding="utf-8", errors="replace").read() for f in logs]
    if any(PUB_OK.search(x) for x in textes):
        return "", None
    echecs = [m for m in (PUB_ECHEC.search(x) for x in textes) if m]
    if not echecs:
        return "", None
    causes = []
    if any(PUB_HOOK.search(x) for x in textes):
        causes.append("hook")
    if any(PUB_RESEAU.search(x) for x in textes):
        causes.append("transport")
    return ("  ✗ NON PUBLIÉ — %s commit(s) en avance%s" % (
        echecs[0].group(1), (" (" + " + ".join(causes) + ")") if causes else ""), "nonpublie")
for d in range(JOURS - 1, -1, -1):
    jour = aujourdhui - datetime.timedelta(days=d)
    dow = (jour.weekday() + 1) % 7          # python : lundi=0 ; cron : dimanche=0
    for h, m, jid in sorted(plan.get(dow, [])):
        quand = datetime.datetime.combine(jour, datetime.time(h, m))
        logs = glob.glob(os.path.join(LOGS, "%s_%s_*.log" % (jid, jour.strftime("%Y%m%d"))))
        if logs:
            etat, motif = juge(logs, quand)
            if motif == "interrompu":
                interrompus.append(jid)
            elif etat.startswith("✓ tracé"):
                suffixe, motif_pub = publication(logs)
                etat += suffixe
                if motif_pub == "nonpublie":
                    nonpublies.append(jid)
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
if interrompus:
    print("\n✗ %d run(s) INTERROMPU(S) : %s" % (len(interrompus), " ".join(sorted(set(interrompus)))))
    print("   Le créneau a bien démarré, et le log n'a pas de ligne de fin : le processus a été")
    print("   tué avant l'épilogue de run_job.sh — extinction, veille forcée, ou plantage.")
    print("   AUCUN livrable n'a été vérifié ni publié. Pour rejouer :")
    print("     bash outils/scripts/rattrapage_jobs.sh %s" % " ".join(sorted(set(interrompus))))
if manques:
    print("\n⛔ %d créneau(x) MANQUÉ(S) : %s" % (len(manques), " ".join(sorted(set(manques)))))
    print("   launchd ne rattrape pas un créneau passé machine éteinte. Pour les rejouer :")
    print("     bash outils/scripts/rattrapage_jobs.sh %s" % " ".join(sorted(set(manques))))
    print("   (anti-doublon actif, budget par job, push durci — et le livrable portera la date du jour)")
if nonpublies:
    print("\n✗ %d run(s) NON PUBLIÉ(S) : %s" % (len(nonpublies), " ".join(sorted(set(nonpublies)))))
    print("   Le run est allé au bout et a committé, et les 3 tentatives de push ont échoué.")
    print("   Les deux causes demandent des gestes OPPOSÉS, et le détail ci-dessus les nomme :")
    print("     · hook       → un document du push est refusé par un contrôle. Lis le log,")
    print("                    corrige le document, puis repousse. Relancer le job ne sert à rien :")
    print("                    tant que le bloquant est là, le push de CHAQUE job suivant est refusé.")
    print("     · transport  → la connexion a été coupée pendant le hook. Un simple `git push`")
    print("                    relancé à la main suffit (règle du 31/10).")
    print("   Pour voir ce qui reste en local :  git rev-parse HEAD  puis  git ls-remote origin main")
# Les logs HORS fenêtre ne sont pas accusés — le créneau est trop vieux pour être rejoué — mais
# les taire reviendrait à cacher la mesure qui a fait écrire ce bloc (12 logs sur 39 le 06/11).
hors = 0
for f in glob.glob(os.path.join(LOGS, "*.log")):
    m_ = re.search(r"_(\d{8})_\d{6}\.log$", f)
    if not m_:
        continue
    jour_ = datetime.datetime.strptime(m_.group(1), "%Y%m%d").date()
    if jour_ > aujourdhui - datetime.timedelta(days=JOURS - 1):
        continue
    x = open(f, encoding="utf-8", errors="replace").read()
    if PUB_ECHEC.search(x) and not PUB_OK.search(x):
        hors += 1
if hors:
    print("\nℹ %d run(s) NON PUBLIÉ(S) plus ancien(s) que la fenêtre de %d jours — non comptés."
          % (hors, JOURS))
    print("   La purge de run_job.sh efface les logs à 30 jours : cette mesure se perd d'elle-même.")
if manques or interrompus or nonpublies:
    sys.exit(1)
print("\n✓ tous les créneaux prescrits des %d derniers jours ont leur log ET sa ligne de fin" % JOURS)
PYMANQUES
  exit $?
fi

# ---- Liste des jobs à rattraper -----------------------------------------
# ⚠️ CETTE LISTE EST FIGÉE DEPUIS JUILLET 2026 et ne vaut plus comme défaut : utilise
#    `--manques` pour savoir ce qui a réellement été manqué, puis passe les ids en argument.
# (Trace : elle portait les créneaux de juillet 2026 de stoicisme-lecon, de
#  placement-financier-lecon et d'entretien-motivationnel-lecon. Les trois jobs sont
#  supprimés — les deux premiers le 27/10/2026 — et aucun n'existait plus quand la liste
#  a été vidée. Son ancien mode d'emploi, « commente les lignes que tu ne veux pas
#  rejouer », supposait une liste tenue à jour : c'est ce qu'elle n'a jamais été.)
# 🔴 27/10/2026 — CETTE LISTE EST DÉSORMAIS VIDE, ET ELLE L'EST PAR MESURE. C'est le SEPTIÈME
#    emplacement qui nomme un job, et le seul que `supprimer_job.sh` ne touche pas : il était
#    donc PÉRIMÉ depuis le 22/10, où il nommait encore `astrologie-karmique-lecon`, supprimé.
#    Les trois derniers parcours de leçons ont été fermés le 27/10 ; les trois ids qu'elle
#    portait ne désignent plus aucun job, et `run_job.sh` aurait répondu « job inconnu » sur
#    chacun. Une liste figée de jobs morts est pire qu'une liste vide : elle a l'air d'un
#    défaut raisonnable. Le lancement sans argument REFUSE maintenant et renvoie à --manques,
#    qui, lui, lit les créneaux prescrits dans jobs_config.json et ne peut pas se périmer.
DEFAULT_JOBS=(
  # (vide — voir ci-dessus. N'y remets un id que pour un rattrapage ponctuel, et retire-le.)
)

# Si un id de job est passé en argument, on ne rejoue que celui-là.
if [ "$#" -ge 1 ]; then
  JOBS=("$@")
elif [ "${#DEFAULT_JOBS[@]}" -eq 0 ]; then
  # ⚠️ `set -u` est actif : développer un tableau vide sort en erreur sur le bash 3.2 du
  #    système. On refuse donc explicitement, avec le geste à faire — jamais en silence.
  echo "⛔ Aucun job à rattraper : la liste par défaut est vide (et c'est voulu, 27/10/2026)."
  echo "   Passe les ids en argument, ou demande d'abord l'inventaire :"
  echo "     bash outils/scripts/rattrapage_jobs.sh --manques"
  exit 2
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
