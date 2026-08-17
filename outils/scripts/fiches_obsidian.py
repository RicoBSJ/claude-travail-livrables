#!/usr/bin/env python3
"""Crée une fiche Obsidian pour chaque leçon qui n'en a pas encore.

Appelé automatiquement par run_job.sh après un job réussi, et lançable à la
main : python3 outils/scripts/fiches_obsidian.py [--dry-run]

Ce qui est déductible du nom de fichier est pré-rempli (parcours, numéro,
date). Ce qui demande la lecture du document reste à faire : les tags
thématiques portent « a-classer », et les deux sections sont vides.

Garanties : aucun .docx n'est lu, modifié ni déplacé · aucune fiche
existante n'est écrasée · le script est idempotent.
"""
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
LECONS = RACINE / "livrables" / "lecons"
CONFIG = RACINE / "jobs_config.json"

GABARIT = """---
type: fiche-document
source: {source}
date_creation: {date_creation}
date_lecon: {date_lecon}
parcours: {parcours}
numero: {numero}
statut: {statut}
tags:
  - parcours/{parcours}
  - a-classer
---

# {titre}

Document source : [[{source}]]

## Résumé

## Notes liées

"""


def parcours_actifs():
    """Identifiants de parcours ayant encore un job planifié."""
    try:
        data = json.loads(CONFIG.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return set()
    jobs = data["jobs"] if isinstance(data, dict) and "jobs" in data else data
    return {j["id"][:-6] for j in jobs if isinstance(j, dict)
            and j.get("id", "").endswith("-lecon")}


def analyser(nom):
    """(parcours, numero) d'après le nom de fichier, ou valeurs de repli."""
    m = re.match(r"^\d{4}-\d{2}-\d{2}_lecon-([a-z0-9-]+?)_(\d{2})_", nom)
    if m:
        return m.group(1), int(m.group(2))
    # Format historique des premières leçons : 2026-04-10_lecon01_slug
    m = re.match(r"^\d{4}-\d{2}-\d{2}_lecon(\d{2})_", nom)
    if m:
        return "claude-code", int(m.group(1))
    return "a-classer", 0


def fiches_distantes(prefixe):
    """Noms des .md déjà présents sur origin/main sous ce préfixe.

    Une fiche peut avoir été remplie et poussée depuis une autre machine.
    La recréer vide ici produirait un fichier non suivi qui BLOQUE le
    prochain `git pull` (« seraient effacés par la fusion »). On s'abstient
    donc, et le pull apportera la version renseignée.

    Aucun accès réseau : on lit la dernière référence connue localement.
    En cas d'échec (pas de dépôt, pas de remote, git absent), on renvoie un
    ensemble vide et le script se comporte comme avant.
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
    if not LECONS.is_dir():
        print(f"ERREUR : dossier introuvable — {LECONS}", file=sys.stderr)
        return 1

    actifs = parcours_actifs()
    distantes = fiches_distantes("livrables/lecons")
    aujourdhui = date.today().isoformat()
    crees, differees = [], []

    for docx in sorted(LECONS.rglob("*.docx")):
        if docx.name.startswith("~$"):
            continue
        note = docx.with_suffix(".md")
        if note.exists():
            continue
        if note.name in distantes:
            differees.append(note.name)
            continue

        parcours, numero = analyser(docx.name)
        statut = "parcours-actif" if parcours in actifs else "parcours-archive"
        contenu = GABARIT.format(
            source=docx.name, date_creation=aujourdhui,
            date_lecon=docx.name[:10], parcours=parcours,
            numero=numero, statut=statut, titre=docx.stem,
        )
        if not essai:
            note.write_text(contenu, encoding="utf-8")
        crees.append(note.name)

    prefixe = "[essai] " if essai else ""
    if crees:
        for n in crees:
            print(f"  {prefixe}+ fiche Obsidian : {n}")
        print(f"  {prefixe}{len(crees)} fiche(s) créée(s) — à compléter (résumé, tags, liens)")
    if differees:
        for n in differees:
            print(f"  {prefixe}⏭️  déjà sur origin/main, non recréée : {n}")
        print(f"  {prefixe}→ un `git pull` apportera la version renseignée")
    return 0


if __name__ == "__main__":
    sys.exit(main())
