#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""controle_livrable_du_job.py — un livrable poussé vient-il d'une exécution RÉUSSIE ?

POURQUOI (16/10/2026). Le `TOURS_MINI` et le fail-fast du plafond existent pour empêcher
qu'un document sorte sans que personne l'ait vérifié : un job qui meurt laisse son travail
sur le disque, sans commit ni push, et c'est délibéré. Mais rien ne dit, au moment d'un
push MANUEL, que le document poussé vient d'une exécution morte.

Incident fondateur : la veille `ai-act` du 16/10/2026. Le job meurt sur
`error_max_budget_usd` — 3,2339 $ pour 3,00 $, 108 %, 34 tours, `stop_reason=tool_use` —
après avoir écrit un `.docx` de 17 159 octets, et sans lancer AUCUN contrôle : ni
`controle_attributions.py`, ni son étape 5 bis, ni `non_regression.sh`. Le document a été
publié le jour même après une vérification MANUELLE. C'est défendable — tout avait été
rejoué — mais cela contourne à la main le garde-fou qui existe pour ça, et « personne »,
dans « publier ce que personne n'a vérifié », c'était moi.

⚠️ CE CONTRÔLE N'EST PAS BLOQUANT, ET C'EST VOLONTAIRE. La règle du 14/10/2026, payée par
un faux refus en production : avant de rendre un motif bloquant dans `--docs`, le faire
tourner en AVERTISSEMENT sur quelques éditions neuves. Un balayage rétrospectif ne mesure
pas la variabilité de ce qui vient — les 73 éditions du 12/10 précédaient toutes le
contrôle, et la 74e l'a cassé en moins de quarante-huit heures. Il avertit donc, il ne
refuse pas. Le passer en bloquant demandera sa propre décision, et quelques semaines.

Usage : controle_livrable_du_job.py <doc.docx> [...]
Rend toujours 0 : c'est un avertisseur. Sortie vide si tous les documents viennent d'un run
réussi, ou si aucun log ne correspond (un document écrit à la main n'est pas en cause).
"""
import glob, json, os, re, sys

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOGS = os.path.join(RACINE, "outils", "scripts", "logs")


def jobs_par_dossier():
    """Le lien dossier → job vient de jobs_config.json, source de vérité unique."""
    m = {}
    try:
        cfg = json.load(open(os.path.join(RACINE, "jobs_config.json"), encoding="utf-8"))["jobs"]
    except OSError:
        return m
    for j in cfg:
        liv = j.get("livrable", "")
        p = re.search(r"livrables/lecons/([a-z0-9-]+)/", liv) or \
            re.search(r"sources/veille/([a-z0-9-]+)/", liv)
        if p:
            m[p.group(1)] = j["id"]
        p2 = re.search(r"lecon-([a-z0-9-]+)_NN", liv)
        if p2:
            m[p2.group(1)] = j["id"]
    return m


def job_du_document(chemin):
    d = chemin.replace(os.sep, "/")
    p = re.search(r"(?:livrables/lecons|sources/veille)/([a-z0-9-]+)/", d)
    if not p:
        return None
    return jobs_par_dossier().get(p.group(1))


def run_du_jour(job, jour):
    """Le log du run qui a produit un document daté YYYY-MM-DD, s'il existe."""
    motif = os.path.join(LOGS, "%s_%s_*.log" % (job, jour.replace("-", "")))
    return sorted(glob.glob(motif))


def verdict(f):
    base = os.path.basename(f)
    m = re.match(r"(\d{4}-\d{2}-\d{2})_", base)
    job = job_du_document(f)
    if not m or not job:
        return None
    logs = run_du_jour(job, m.group(1))
    if not logs:
        return None                      # aucun run ce jour-là : document écrit autrement
    txt = open(logs[-1], encoding="utf-8", errors="replace").read()
    err = re.search(r"is_error=(\w+).*?subtype=(\S+)", txt)
    mes = re.search(r"co[ûu]t r[ée]el ([\d.,]+) \$ / plafond ([\d.,]+) \$ \((\d+) %[^|]*\| (\d+) tours", txt)
    ctrl = len(re.findall(r"controle_attributions|controle_decompte|VERDICT|non_regression", txt))
    if not err or err.group(1) != "True":
        return None                      # run réussi : rien à dire
    d = {"doc": base, "job": job, "log": os.path.basename(logs[-1]),
         "subtype": err.group(2), "controles": ctrl}
    if mes:
        d.update(cout=mes.group(1), plafond=mes.group(2), pct=mes.group(3), tours=mes.group(4))
    return d


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    alertes = [v for v in (verdict(f) for f in sys.argv[1:]) if v]
    for a in alertes:
        print("  ⚠ %s vient d'une exécution ÉCHOUÉE de %s" % (a["doc"], a["job"]))
        if "cout" in a:
            print("      %s $ / %s $ (%s %%) · %s tours · %s"
                  % (a["cout"], a["plafond"], a["pct"], a["tours"], a["subtype"]))
        else:
            print("      %s" % a["subtype"])
        print("      contrôles tracés dans le log : %d%s"
              % (a["controles"], " — AUCUN : ce document n'a été vérifié par personne"
                 if a["controles"] == 0 else ""))
        print("      (avertissement, non bloquant : relancer le job est la voie sûre ;")
        print("       une vérification manuelle contourne le garde-fou qui existe pour ça)")
    sys.exit(0)
