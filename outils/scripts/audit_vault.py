#!/usr/bin/env python3
"""Audit du vault Obsidian : nommage, cohérence et intégrité des liens.

    python3 outils/scripts/audit_vault.py [--verbeux]

Neuf contrôles sur livrables/lecons/ et sources/veille/. Sortie concise par
défaut : une ligne par contrôle, le détail seulement en cas de problème.

Code de sortie 0 si tout est vert, 1 sinon — utilisable dans un enchaînement.

À lancer après un incident de synchronisation, avant une session de travail
dans Obsidian, ou quand un job a produit des fichiers inattendus.

CONVENTIONS VÉRIFIÉES
  livrables/lecons/  <doc>.docx  →  <doc>.md          type: fiche-document
  sources/veille/    <doc>.docx  →  <doc>.fiche.md    type: fiche-document
                     veille rédigée en markdown        type: veille
                     note de synthèse par sujet        type: note-dossier

Le suffixe « .fiche.md » distingue les fiches locales des veilles markdown,
qui sont des livrables publiés. C'est lui que run_job.sh exclut de
l'auto-push : un livrable mal nommé ne serait jamais publié (cas réel du
17/08/2026, note de veille HAS).
"""
import re
import subprocess
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
LECONS = RACINE / "livrables" / "lecons"
VEILLE = RACINE / "sources" / "veille"

VERT, ROUGE, JAUNE, GRAS, RAZ = "\033[32m", "\033[31m", "\033[33m", "\033[1m", "\033[0m"


def type_de(p):
    """Valeur du champ `type:` du frontmatter, ou None."""
    t = p.read_text(encoding="utf-8", errors="replace")
    if not t.lstrip().startswith("---"):
        return None
    m = re.search(r"^type:\s*(\S+)", t, re.M)
    return m.group(1) if m else None


def notes_md(base, motif="*.md"):
    return sorted(base.rglob(motif)) if base.is_dir() else []


class Audit:
    def __init__(self, verbeux=False):
        self.verbeux = verbeux
        self.echecs = 0
        self.lecons = notes_md(LECONS)
        self.fiches_v = notes_md(VEILLE, "*.fiche.md")
        self.veilles_md = [p for p in notes_md(VEILLE) if not p.name.endswith(".fiche.md")]
        self.noms = {}
        for p in self.lecons + notes_md(VEILLE):
            self.noms.setdefault(p.stem, []).append(p)

    def resultat(self, titre, problemes, note=""):
        if problemes:
            self.echecs += 1
            print(f"  {ROUGE}✗{RAZ} {titre} — {len(problemes)} problème(s)")
            for x in problemes[: (None if self.verbeux else 8)]:
                print(f"      {x}")
            if not self.verbeux and len(problemes) > 8:
                print(f"      … {len(problemes) - 8} autres (--verbeux)")
        else:
            print(f"  {VERT}✓{RAZ} {titre}{note}")

    # ---- 1 · suffixe cohérent avec le type déclaré -------------------------
    def c1(self):
        pb = []
        for p in notes_md(VEILLE):
            t = type_de(p)
            est_fiche = p.name.endswith(".fiche.md")
            if est_fiche and t not in ("fiche-document", "note-dossier"):
                pb.append(f"{p.relative_to(VEILLE)} — suffixe .fiche mais type={t!r} "
                          f"(livrable mal nommé : il ne sera JAMAIS publié)")
            if not est_fiche and t != "veille":
                pb.append(f"{p.relative_to(VEILLE)} — sans suffixe mais type={t!r} "
                          f"(fiche mal nommée : elle serait publiée)")
        self.resultat("Suffixe cohérent avec le type (sources/veille)", pb)

    # ---- 2 · type des fiches de leçons ------------------------------------
    def c2(self):
        pb = [f"{p.name} — type={type_de(p)!r}" for p in self.lecons
              if type_de(p) != "fiche-document"]
        self.resultat("Type des fiches de leçons", pb, f" ({len(self.lecons)} fiches)")

    # ---- 3 · fiches orphelines --------------------------------------------
    def c3(self):
        pb = []
        for p in self.fiches_v + self.lecons:
            if "_dossier" in p.name:
                continue
            m = re.search(r"^source:\s*(.+)$", p.read_text(encoding="utf-8"), re.M)
            if not m:
                pb.append(f"{p.name} — pas de champ `source`")
            elif not (p.parent / m.group(1).strip()).exists():
                pb.append(f"{p.name} → {m.group(1).strip()} introuvable")
        self.resultat("Chaque fiche pointe vers un document existant", pb)

    # ---- 4 · documents sans note ------------------------------------------
    def c4(self):
        pb = []
        for d in sorted(VEILLE.rglob("*.docx")):
            if d.name.startswith("~$"):
                continue
            if not d.with_suffix(".fiche.md").exists() and not d.with_suffix(".md").exists():
                pb.append(f"veille/{d.relative_to(VEILLE)}")
        for d in sorted(LECONS.glob("*.docx")):
            if not d.name.startswith("~$") and not d.with_suffix(".md").exists():
                pb.append(f"lecons/{d.name}")
        self.resultat("Chaque document a sa note", pb)

    # ---- 5 · doublons fiche + veille markdown -----------------------------
    def c5(self):
        pb = [f"{d.relative_to(VEILLE)} a une fiche ET une veille markdown"
              for d in VEILLE.rglob("*.docx")
              if d.with_suffix(".fiche.md").exists() and d.with_suffix(".md").exists()]
        self.resultat("Pas de doublon fiche / veille markdown", pb)

    # ---- 6 · noms de note ambigus -----------------------------------------
    def c6(self):
        pb = [f"« {k} » : {', '.join(str(x.relative_to(RACINE)) for x in v)}"
              for k, v in self.noms.items() if len(v) > 1]
        self.resultat("Aucun nom de note ambigu", pb)

    # ---- 7 · liens wiki ----------------------------------------------------
    def c7(self):
        pb, total = [], 0
        for p in self.lecons + notes_md(VEILLE):
            for c in re.findall(r"\[\[([^\]]+)\]\]", p.read_text(encoding="utf-8")):
                total += 1
                ok = (p.parent / c).exists() if c.endswith(".docx") else c in self.noms
                if not ok:
                    pb.append(f"{p.name} → [[{c}]]")
        self.resultat("Liens wiki résolus (règle Obsidian)", pb, f" ({total} liens)")

    # ---- 8 · fiches non renseignées ---------------------------------------
    def c8(self):
        pb = [p.name for p in self.lecons + notes_md(VEILLE)
              if "a-classer" in p.read_text(encoding="utf-8")]
        if pb:
            self.echecs -= 1  # information, pas une anomalie
            print(f"  {JAUNE}○{RAZ} Fiches restant à renseigner — {len(pb)}")
            for x in pb[: (None if self.verbeux else 8)]:
                print(f"      {x}")
            if not self.verbeux and len(pb) > 8:
                print(f"      … {len(pb) - 8} autres (--verbeux)")
            self.echecs += 1
        else:
            print(f"  {VERT}✓{RAZ} Toutes les fiches sont renseignées")

    # ---- 9 · portée de l'auto-push ----------------------------------------
    def c9(self):
        cmd = ["git", "-C", str(RACINE), "add", "--dry-run",
               "sources/veille", "livrables/lecons", "livrables/quiz",
               "livrables/infographies", "livrables/projets",
               "livrables/controles", "livrables/documents",
               ":(exclude)livrables/lecons/*.md",
               ":(exclude)sources/veille/*.fiche.md"]
        try:
            out = subprocess.run(cmd, capture_output=True, text=True, timeout=30).stdout
        except (OSError, subprocess.SubprocessError) as e:
            print(f"  {JAUNE}○{RAZ} Portée de l'auto-push — non vérifiable ({e})")
            return
        pb = [l.strip() for l in out.splitlines()
              if ".fiche.md" in l or re.search(r"lecons/.*\.md'", l)]
        attente = len([l for l in out.splitlines() if l.strip()])
        self.resultat("Aucune fiche ne partirait à l'auto-push", pb,
                      f" ({attente} fichier(s) en attente de publication)")

    def run(self):
        print(f"\n{GRAS}Audit du vault — {RACINE.name}{RAZ}\n")
        for c in (self.c1, self.c2, self.c3, self.c4, self.c5,
                  self.c6, self.c7, self.c8, self.c9):
            c()
        print()
        if self.echecs:
            print(f"  {ROUGE}{self.echecs} contrôle(s) en échec{RAZ}\n")
            return 1
        print(f"  {VERT}Les 9 contrôles sont au vert{RAZ}\n")
        return 0


if __name__ == "__main__":
    sys.exit(Audit(verbeux="--verbeux" in sys.argv).run())
