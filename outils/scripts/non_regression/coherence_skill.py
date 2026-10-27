#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cohérence du skill `lancer-job` avec `jobs_config.json` — aucun réseau, 0,1 s.

🔴 27/10/2026 — POURQUOI CE CONTRÔLE EXISTE. `supprimer_job.sh` vérifie déjà, en fin de
   course, que « les ids du skill égalent les ids de la config ». Mesuré ce jour-là : cette
   vérification n'apparie que `job id "…"`, et le skill porte l'alias à DEUX AUTRES endroits
   que cette ligne — la ligne d'aide `  /lancer-job <alias>` et le `description:` du
   frontmatter. La suppression d'`astrologie-karmique-lecon` du 22/10 a donc laissé
   `/lancer-job astro` et le jeton `astro,` dans la description, et la vérification finale a
   répondu « ✓ ids du skill = ids de la config (8) » en toute bonne foi : le skill annonçait
   un job qui n'existe plus, et RIEN dans le dépôt ne pouvait le dire.
⛔ Et ce n'est pas un témoin qui peut se périmer sur une propriété volatile : l'invariant
   gardé est « le skill décrit exactement les jobs de la config », qui ne devient faux que si
   le dépôt est réellement incohérent. Aucun tiers, aucun réseau, aucune date.
"""
import json, os, re, sys

# ⚠️ QUATRE `dirname`, PAS TROIS : ce script vit dans `outils/scripts/non_regression/`,
#    un cran plus bas que les contrôles. Copier l'arithmétique des trois `dirname` d'un
#    contrôle de `outils/scripts/` est exactement le bug de `tolerance_page_morte.py` du
#    23/10 — on copie une CONSTANTE, jamais l'arithmétique qu'on teste.
RACINE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
assert os.path.isdir(os.path.join(RACINE, "outils", "scripts")), \
    "RACINE mal calculée : %s" % RACINE
SKILL = ".claude/skills/lancer-job/SKILL.md"
CONFIG = "jobs_config.json"

RE_CORRESP = re.compile(r'^- "([^"]*)"[^\n]*job id "([\w-]+)"', re.M)
RE_AIDE = re.compile(r"^  /lancer-job (\S+)", re.M)
RE_DESCR = re.compile(r"^description:[^\n]*où nom est\s*:\s*([^\n]*)$", re.M)


def lire(skill_src):
    """Les TROIS endroits où le skill nomme un job. L'alias est celui de la ligne de
    correspondance — il n'est PAS dérivable de l'id : `finance` → `placement-financier-lecon`,
    `astro` → `astrologie-karmique-lecon`."""
    corresp = [(a, j) for a, j in RE_CORRESP.findall(skill_src)]
    aides = RE_AIDE.findall(skill_src)
    m = RE_DESCR.search(skill_src)
    descr = [x.strip() for x in m.group(1).split(",") if x.strip()] if m else []
    return corresp, aides, descr


def ecarts(skill_src, ids):
    corresp, aides, descr = lire(skill_src)
    alias = {a for a, _ in corresp}
    out = []
    for a, j in corresp:
        if j not in ids:
            out.append("correspondance « %s » → job id « %s » ABSENT de la config" % (a, j))
    for j in sorted(ids - {j for _, j in corresp}):
        out.append("job « %s » de la config SANS ligne de correspondance dans le skill" % j)
    for a in aides:
        if a not in alias:
            out.append("ligne d'aide « /lancer-job %s » SANS correspondance — alias orphelin" % a)
    for a in sorted(alias - set(aides)):
        out.append("alias « %s » sans ligne d'aide /lancer-job" % a)
    for a in descr:
        if a not in alias:
            out.append("description du frontmatter : alias « %s » SANS correspondance" % a)
    for a in sorted(alias - set(descr)):
        out.append("alias « %s » absent de la description du frontmatter" % a)
    return out


# ── CAS FABRIQUÉS. Rien de vivant dans ces verdicts : ni le dépôt, ni un tiers, ni une date.
CONFORME = """---
name: lancer-job
description: Usage : /lancer-job [nom] où nom est : imac, finance
---
- "imac" ou "mac"                → job id "imac-veille"
- "finance" ou "placement"       → job id "placement-financier-lecon"
```
  /lancer-job imac        — Veille
  /lancer-job finance     — Leçon
```
"""


def autotest():
    ids = {"imac-veille", "placement-financier-lecon"}
    jouees, ko = [], []

    def borne(nom, src, ids_, attendu_n, motif=None):
        jouees.append(nom)
        e = ecarts(src, ids_)
        if len(e) != attendu_n or (motif and not any(motif in x for x in e)):
            ko.append("%s : %d écart(s) %s" % (nom, len(e), e))

    # ① ACCEPTÉE — un skill conforme ne doit RIEN produire.
    borne("① conforme", CONFORME, ids, 0)
    # ② ACCEPTÉE, ET C'EST ELLE QUI INTERDIT DE REDÉRIVER L'ALIAS DE L'ID : `finance` n'est
    #    pas un préfixe de `placement-financier-lecon`, et pourtant c'est l'alias juste.
    borne("② l'alias est celui de la ligne, pas le slug de l'id", CONFORME, ids, 0)
    # ③ le cas RÉEL du 22/10 : correspondance retirée, ligne d'aide et description laissées.
    astro = CONFORME.replace('- "finance" ou "placement"       → job id "placement-financier-lecon"\n', "")
    borne("③ correspondance retirée, aide et description laissées", astro,
          {"imac-veille"}, 2, "alias orphelin")
    # ④ un job de la config que le skill ne nomme pas.
    borne("④ job de la config sans correspondance", CONFORME,
          ids | {"serafin-ph-veille"}, 1, "SANS ligne de correspondance")
    # ⑤ une correspondance vers un job qui n'existe plus.
    borne("⑤ correspondance vers un job absent de la config", CONFORME,
          {"imac-veille"}, 1, "ABSENT de la config")
    # ⑥ correspondance présente, ligne d'aide manquante.
    borne("⑥ alias sans ligne d'aide", CONFORME.replace("  /lancer-job finance     — Leçon\n", ""),
          ids, 1, "sans ligne d'aide")
    # ⑦ correspondance présente, absente de la description.
    borne("⑦ alias absent de la description", CONFORME.replace("imac, finance", "imac"),
          ids, 1, "absent de la description")

    for x in ko:
        print("  ✗ " + x)
    print("  %d/%d bornes de la cohérence du skill" % (len(jouees) - len(ko), len(jouees)))
    return 1 if ko else 0


def reel():
    src = open(os.path.join(RACINE, SKILL), encoding="utf-8").read()
    ids = {x["id"] for x in json.load(open(os.path.join(RACINE, CONFIG), encoding="utf-8"))["jobs"]}
    e = ecarts(src, ids)
    for x in e:
        print("  ✗ " + x)
    print("  COHÉRENCE DU SKILL : %d job(s) de la config · %d écart(s)" % (len(ids), len(e)))
    return 1 if e else 0


if __name__ == "__main__":
    if "--racine" in sys.argv:
        print(RACINE)
        sys.exit(0)
    sys.exit(autotest() if "--autotest" in sys.argv else reel())
