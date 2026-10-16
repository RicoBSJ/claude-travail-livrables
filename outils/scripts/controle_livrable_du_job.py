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

🔴 BLOQUANT DEPUIS LE 16/10/2026, SUR DÉCISION EXPLICITE — ET AVEC UNE EXEMPTION PAR
DÉCLARATION, SANS LAQUELLE IL SERAIT UN PIÈGE. Il s'appuie sur le run qui a produit le
fichier, un fait qui ne change JAMAIS : sans exemption, le livrable du 16/10 et chacune de
ses corrections futures seraient refusés indéfiniment, et le push de correction mené le jour
même aurait été bloqué. Le document doit donc DIRE LUI-MÊME les deux choses — ① que son
exécution a échoué ou crevé son plafond, ET ② qu'il a été relu hors du job. Une phrase dans
son journal des corrections suffit, et elle reste lisible par qui le relira, ce qu'un
avertissement de harnais n'est pas.

⚠️ CE QUE CE PASSAGE EN BLOQUANT ENFREINT, ET IL FAUT LE DIRE : la règle du 14/10/2026 veut
qu'un motif tourne en AVERTISSEMENT sur quelques éditions neuves avant de bloquer, parce
qu'un balayage rétrospectif ne mesure pas la variabilité de ce qui vient — les 73 éditions
du 12/10 précédaient toutes leur contrôle, et la 74e l'a cassé en moins de 48 h. Ici, le
motif a tourné en avertissement UNE journée, sur UN cas. Ce qui borne le risque n'est donc
pas l'observation mais l'exemption : un faux refus se lève en écrivant une phrase dans le
livrable, pas en modifiant un contrôle.

Usage : controle_livrable_du_job.py <doc.docx> [...]
Rend 1 s'il reste un document issu d'un run échoué SANS déclaration, 0 sinon. Sortie vide si
tous viennent d'un run réussi, ou si aucun log ne correspond (un document écrit à la main
n'est pas en cause).
"""
import glob, json, os, re, subprocess, sys, unicodedata

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


# ⚠️ EXEMPTION PAR DÉCLARATION — AJOUTÉE LE 16/10/2026, QUAND ㊳ EST DEVENU BLOQUANT.
#    Sans elle, ㊳ bloquant serait un PIÈGE et non un garde : il s'appuie sur le run qui a
#    produit le fichier, un fait qui ne change JAMAIS. Le livrable du 16/10 — et CHACUNE de
#    ses corrections futures — seraient refusés indéfiniment ; le push de correction mené le
#    jour même aurait été bloqué. C'est l'idiome du dépôt qui donne la sortie : ㉜ et ㉞ ne
#    refusent pas ce qui est DÉCLARÉ, « ce qui est attendu, c'est une déclaration ».
#    BORNE EN « ET », PAS EN « OU » : la leçon du 14/10/2026, où une borne « ≤4 mots OU
#    dénoncée » a refusé un livrable juste et où le « ET » a tenu. Le document doit dire
#    LES DEUX : ① que l'exécution a échoué ou crevé son plafond, ET ② qu'il a été relu
#    hors du job. Un seul des deux ne suffit pas — « plafond » seul est un mot que n'importe
#    quelle note sur les budgets peut porter.
#    NFC D'ABORD : les marqueurs du dépôt s'écrivent tantôt « é » précomposé, tantôt
#    « e » + U+0301, et les variantes sans accent ne sont pas de la redondance.
ECHEC_DIT = re.compile(r"plafond de co[uû]t|d[ée]passement de (?:budget|plafond)"
                       r"|error_max_budget|mort(?:e)? sur son plafond"
                       r"|ex[ée]cution [ée]chou[ée]+|job .{0,30}est mort", re.I)
RELU_DIT = re.compile(r"relue? (?:puis|et) publi|v[ée]rifi[ée]e?s? [àa] la main"
                      r"|audit men[ée] [àa] la main|contr[ôo]les? rejou[ée]"
                      r"|relue? [àa] la main|publi[ée]e? s[ée]par[ée]ment", re.I)


def declaration(f):
    """Le document dit-il LUI-MÊME que son job a échoué ET qu'il a été relu hors du job ?"""
    try:
        t = subprocess.run([sys.executable, os.path.join(RACINE, "outils", "scripts",
                                                         "extract_docx.py"), f],
                           capture_output=True, text=True, env={}).stdout
    except OSError:
        return False, False
    t = unicodedata.normalize("NFC", re.sub(r"[ \t\u00a0\u202f]+", " ", t))
    return bool(ECHEC_DIT.search(t)), bool(RELU_DIT.search(t))


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
    dit_echec, dit_relu = declaration(f)
    d = {"doc": base, "job": job, "log": os.path.basename(logs[-1]),
         "subtype": err.group(2), "controles": ctrl,
         "declare": dit_echec and dit_relu, "dit_echec": dit_echec, "dit_relu": dit_relu}
    if mes:
        d.update(cout=mes.group(1), plafond=mes.group(2), pct=mes.group(3), tours=mes.group(4))
    return d


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    alertes = [v for v in (verdict(f) for f in sys.argv[1:]) if v]
    refuses = 0
    for a in alertes:
        marque = "✓" if a["declare"] else "⛔"
        print("  %s %s vient d'une exécution ÉCHOUÉE de %s" % (marque, a["doc"], a["job"]))
        if "cout" in a:
            print("      %s $ / %s $ (%s %%) · %s tours · %s"
                  % (a["cout"], a["plafond"], a["pct"], a["tours"], a["subtype"]))
        else:
            print("      %s" % a["subtype"])
        print("      contrôles tracés dans le log : %d%s"
              % (a["controles"], " — AUCUN : ce document n'a été vérifié par personne"
                 if a["controles"] == 0 else ""))
        if a["declare"]:
            print("      DÉCLARÉ par le document : il dit l'échec de son exécution ET sa relecture")
            print("      hors du job. Accepté — la trace est dans le livrable, pas seulement ici.")
        else:
            refuses += 1
            manque = []
            if not a["dit_echec"]: manque.append("l'échec de son exécution")
            if not a["dit_relu"]:  manque.append("sa relecture hors du job")
            print("      ⛔ REFUSÉ : le document ne DÉCLARE pas %s." % " ni ".join(manque))
            print("      Relancer le job est la voie sûre. Si le travail doit être repris à la")
            print("      main, le livrable doit le DIRE — une phrase dans son journal des")
            print("      corrections suffit, et elle restera lisible par qui le relira.")
    sys.exit(1 if refuses else 0)
