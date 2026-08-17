#!/usr/bin/env python3
"""Crée une fiche Obsidian pour chaque veille .docx qui n'en a pas encore.

Appelé automatiquement par run_job.sh après un job réussi, et lançable à la
main : python3 outils/scripts/fiches_veille.py [--dry-run]

Différence avec fiches_obsidian.py (dossier lecons/) : sources/veille/
contient aussi des veilles rédigées DIRECTEMENT en markdown, qui sont des
livrables publiés. Les fiches portent donc le suffixe « .fiche.md » pour
qu'aucune confusion ne soit possible — ni pour un lecteur, ni pour le
pathspec d'exclusion de l'auto-push.

Garanties : aucun .docx n'est lu, modifié ni déplacé · aucune fiche
existante n'est écrasée · les sous-dossiers sont parcourus.
"""
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
VEILLE = RACINE / "sources" / "veille"
CONFIG = RACINE / "jobs_config.json"

GABARIT = """---
type: fiche-document
source: {source}
date_creation: {date_creation}
date_veille: {date_veille}
veille: {sujet}
statut: {statut}
tags:
  - veille/{sujet}
  - a-classer
---

# {titre}

Document source : [[{source}]]

## Résumé

## Notes liées

"""

# Sujet de veille → identifiant du job qui le produit
JOBS = {
    "imac": "imac-veille",
    "serafin-ph": "serafin-ph-veille",
    "rbpp": "rbpp-pipeline",
    "has-actualite": "rbpp-pipeline",
    "has": "rbpp-pipeline",
}


def jobs_existants():
    try:
        data = json.loads(CONFIG.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return set()
    jobs = data["jobs"] if isinstance(data, dict) and "jobs" in data else data
    return {j["id"] for j in jobs if isinstance(j, dict)}


def sujet_de(chemin):
    """Sujet de veille : le sous-dossier s'il y en a un, sinon le nom du fichier."""
    rel = chemin.relative_to(VEILLE)
    if len(rel.parts) > 1:
        return rel.parts[0].lower()
    m = re.match(r"^\d{4}-\d{2}-\d{2}_veille_(.+)$", chemin.stem, re.I)
    if m:
        # « rbpp_tsa-enfant-adolescent » → « rbpp »
        return m.group(1).lower().split("_")[0]
    # Nommage historique : « veille-essms-2026-05-20-2026-05-26 »
    m = re.match(r"^veille-([a-z0-9-]+?)-\d{4}-\d{2}-\d{2}", chemin.stem, re.I)
    if m:
        return m.group(1).lower()
    return "a-classer"


def fiches_distantes(prefixe):
    """Noms des .fiche.md déjà présents sur origin/main sous ce préfixe.

    Une fiche peut avoir été remplie et poussée depuis une autre machine.
    La recréer vide ici produirait un fichier non suivi qui BLOQUE le
    prochain `git pull`. On s'abstient donc, et le pull apportera la version
    renseignée. Aucun accès réseau : dernière référence connue localement.
    """
    try:
        out = subprocess.run(
            ["git", "-C", str(RACINE), "ls-tree", "-r", "--name-only",
             "origin/main", "--", prefixe],
            capture_output=True, text=True, timeout=15)
        if out.returncode != 0:
            return set()
        return {Path(l).name for l in out.stdout.splitlines() if l.endswith(".md")}
    except (OSError, subprocess.SubprocessError):
        return set()


def main():
    essai = "--dry-run" in sys.argv
    if not VEILLE.is_dir():
        print(f"ERREUR : dossier introuvable — {VEILLE}", file=sys.stderr)
        return 1

    actifs = jobs_existants()
    distantes = fiches_distantes("sources/veille")
    aujourdhui = date.today().isoformat()
    crees, differees = [], []

    for docx in sorted(VEILLE.rglob("*.docx")):
        if docx.name.startswith("~$"):
            continue
        note = docx.with_suffix(".fiche.md")
        if note.exists():
            continue
        # La veille existe déjà en markdown (même nom, sans suffixe) : ce .md EST
        # la note Obsidian, une fiche d'accompagnement ferait doublon. Cas des
        # veilles HAS, que le pipeline produit en Word ET en markdown.
        if docx.with_suffix(".md").exists():
            continue
        if note.name in distantes:
            differees.append(note.name)
            continue

        sujet = sujet_de(docx)
        job = JOBS.get(sujet)
        statut = "veille-active" if job in actifs else "veille-archive"
        # Date en tête du nom, ou première date rencontrée (nommage historique)
        m = re.search(r"(\d{4}-\d{2}-\d{2})", docx.name)
        contenu = GABARIT.format(
            source=docx.name, date_creation=aujourdhui,
            date_veille=m.group(1) if m else "inconnue",
            sujet=sujet, statut=statut, titre=docx.stem,
        )
        if not essai:
            note.write_text(contenu, encoding="utf-8")
        crees.append(note.relative_to(VEILLE))

    prefixe = "[essai] " if essai else ""
    if crees:
        for n in crees:
            print(f"  {prefixe}+ fiche veille : {n}")
        print(f"  {prefixe}{len(crees)} fiche(s) créée(s) — à compléter (résumé, tags, liens)")
    if differees:
        for n in differees:
            print(f"  {prefixe}⏭️  déjà sur origin/main, non recréée : {n}")
        print(f"  {prefixe}→ un `git pull` apportera la version renseignée")
    return 0


if __name__ == "__main__":
    sys.exit(main())
