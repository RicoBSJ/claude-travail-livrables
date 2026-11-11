#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tout témoin du dépôt appartient-il à une catégorie du hook `pre-push` ?

POURQUOI — MESURÉ LE 11/11/2026, ET LE TROU ÉTAIT UN RÉPERTOIRE ENTIER.
NEUF des douze fichiers de `outils/scripts/non_regression/` n'appartenaient à AUCUNE
catégorie : bfr_journal, coherence_skill, corps_tronque, desarmement_git, etiquette_has,
faisceau_5bis, murs_lus, publication_run, tolerance_page_morte. Un push qui ne touchait
qu'eux ne déclenchait RIEN — le témoin pouvait être amputé ou saboté et partir sur le
dépôt sans qu'UNE SEULE de ses bornes soit jouée. Même défaut que `CLAUDE.md` sans
catégorie (27/10) et que `rattrapage_jobs.sh` (06/11), à l'échelle d'un répertoire.

⚠️ ET MA PROPRE DESCRIPTION DU TROU ÉTAIT FAUSSE LA VEILLE : j'avais écrit que
`publication_run.py` n'était pas câblé « alors que muter_docx.py et omission_axe2.py le
sont ». Deux éléments lus comme un recensement : il y en avait NEUF. « Un recensement
textuel n'est pas un recensement d'appels », par l'autre bout.

🔴 LE PRÉDICAT EST STRUCTUREL, JAMAIS UN COMPTE EN DUR. Un `12/12` figé se périme au
prochain témoin écrit, et une liste de fichiers dans le hook se périme de la même façon
— c'est le défaut que ce dépôt a payé TROIS fois (`setup_launchd.sh`,
`rattrapage_jobs.sh`, la table dossier → job de ㊳). On lit donc les catégories DANS le
hook, on énumère les témoins DEPUIS git, et la borne ⑤ exige qu'un nom de témoin
FABRIQUÉ, qui n'existe pas, soit déjà couvert : c'est elle, et elle seule, qui interdit
de revenir à une liste.

⛔ IL NE PEUT PAS SE PÉRIMER : aucun réseau, aucun tiers, aucune date. L'invariant ne
devient faux que si un témoin du dépôt cesse d'être déclenché par le hook.

⚠️ CE QU'IL NE FAIT PAS, ET C'EST DIT : les scripts de PREMIER niveau
(`outils/scripts/*.py|sh`) ne sont pas exigés — leur rattachement est une décision par
script, pas un invariant. Ils sont RECENSÉS et IMPRIMÉS, non bloquants, pour que ce
reste soit visible au lieu d'être silencieux (même parti que `--table` de
`controle_livrable_du_job.py`). Mesure du 11/11 : 8 orphelins de premier niveau.
"""
import pathlib, re, subprocess, sys

RACINE = pathlib.Path(__file__).resolve().parent.parent.parent.parent
# ⚠️ QUATRE parent : ce témoin vit dans outils/scripts/non_regression/. Trois donnaient
# outils/ — bug de tolerance_page_morte.py (23/10), coherence_skill.py (27/10) et
# integrite_livrables.py (11/11, le jour même).
assert (RACINE / "jobs_config.json").exists(), "RACINE ne pointe pas sur la racine : %s" % RACINE
HOOK = RACINE / "outils" / "scripts" / "hooks" / "pre-push"

KO, JOUEES = [], []
def borne(nom, condition):
    JOUEES.append(nom)
    if not condition:
        KO.append(nom)

# ── les catégories sont LUES dans le hook, par motif de déclaration et non par une liste
#    de noms : renommer une catégorie ne doit pas la faire disparaître du recensement.
src = HOOK.read_text()
CATS = {}
for m in re.finditer(r"^([A-Z][A-Z0-9_]*)='(\^[^']+)'$", src, re.M):
    CATS[m.group(1)] = m.group(2)
borne("① les catégories sont lues DANS le hook (au moins six déclarations)", len(CATS) >= 6)

def categories(chemin):
    return [n for n, r in CATS.items() if re.match(r, chemin)]

suivis = [p.decode() for p in
          subprocess.run(["git", "ls-files", "-z"], cwd=str(RACINE), capture_output=True).stdout.split(b"\0") if p]
temoins = sorted(p for p in suivis
                 if p.startswith("outils/scripts/non_regression/") and p.endswith(".py"))
orphelins = [p for p in temoins if not categories(p)]

borne("② le dépôt a bien des témoins à vérifier (un périmètre VIDE n'est pas un dépôt sain)",
      len(temoins) >= 10)
borne("③ AUCUN témoin n'est orphelin de catégorie", not orphelins)
borne("④ le hook se surveille lui-même — sinon l'éditer ne déclenche rien",
      bool(categories("outils/scripts/hooks/pre-push")))
# ⑤ LA BORNE QUI INTERDIT DE REVENIR À UNE LISTE : un nom FABRIQUÉ, absent du dépôt,
#    doit déjà être couvert. Avec une liste de fichiers en dur, elle tombe.
FABRIQUE = "outils/scripts/non_regression/temoin_fabrique_qui_nexiste_pas.py"
assert FABRIQUE not in suivis, "le nom fabriqué existe pour de vrai : en changer"
borne("⑤ un témoin FUTUR est déjà couvert — donc c'est un MOTIF, pas une liste (ACCEPTEE)",
      bool(categories(FABRIQUE)))
# ⚠️ MA PREMIÈRE ⑥ S'ÉCRIVAIT `True if X == [] else X != []` : elle ne pouvait PAS échouer,
#    donc ce n'était pas une borne (règle du 26/10). Forme juste : le motif de répertoire est
#    ANCRÉ, donc un .py quelconque hors de ce répertoire n'est PAS attrapé par lui. Un motif
#    élargi en `.*\.py` ferait tomber cette borne — c'est ce qu'elle garde.
borne("⑥ le motif est ANCRÉ au répertoire : un .py jetable n'est pas attrapé (ACCEPTEE)",
      "SURVEILLES" not in categories("en_cours/jetable.py")
      and "SURVEILLES" not in categories("outils/scripts/non_regression/sous/profond.py"))
borne("⑦ les catégories spécifiques SURVIVENT au motif de répertoire — muter_docx garde CINQBIS",
      "CINQBIS" in categories("outils/scripts/non_regression/muter_docx.py")
      and "EDPREC" in categories("outils/scripts/non_regression/omission_axe2.py"))
borne("⑧ le motif de répertoire est dans SURVEILLES, la catégorie qui lance le mode normal",
      "SURVEILLES" in categories("outils/scripts/non_regression/publication_run.py"))

# ── recensement NON BLOQUANT des scripts de premier niveau, pour qu'il ne soit pas silencieux
niv1 = sorted(p for p in suivis if re.match(r"outils/scripts/[^/]+\.(py|sh)$", p))
orph1 = [p for p in niv1 if not categories(p)]
borne("⑨ le recensement de premier niveau est fait (il est imprimé, non bloquant)",
      len(niv1) >= 20)

print("CATÉGORIES DU HOOK : %d · témoins : %d · orphelins : %d · "
      "scripts de premier niveau : %d dont %d sans catégorie (NON bloquant)"
      % (len(CATS), len(temoins), len(orphelins), len(niv1), len(orph1)))
for p in orphelins:
    print("  ⛔ TÉMOIN ORPHELIN : %s — un push qui ne touche que lui ne déclenche RIEN" % p)
for p in orph1:
    print("  ⓘ  premier niveau sans catégorie : %s" % p)

# ⑩ LE sed DU HARNAIS, APPLIQUÉ À LA LIGNE RÉELLEMENT IMPRIMÉE. L'ancre est ASCII sans
#    accent : la dérive d'un libellé accentué a déjà fait lire un dénominateur VIDE et
#    refuser TOUS les pushs (04/11). Un garde de compte doit être essayé sur la ligne
#    qu'il va vraiment lire — faux, il bloque tout ; inversé, il accepte tout.
# 🔴 LE sed EST LU DANS LE HARNAIS, PAS RECOPIÉ ICI. Mon premier jet le recopiait : un
#    sabotage qui faisait dériver le libellé dans les DEUX fichiers du témoin laissait la
#    borne verte, puisque la copie dérivait avec. « Un test qui teste une COPIE de la
#    logique ne garde rien » (15/10) — c'est le sabotage qui l'a dit, pas la relecture.
_h = (RACINE / "outils" / "scripts" / "non_regression.sh").read_text()
_seds = re.findall(r"sed -n '([^']*categories hook[^']*)'", _h)
borne("⑩ le harnais porte UN seul sed pour cette ligne", len(_seds) == 1)
_sed = _seds[0] if _seds else "s/ZZZ/\\1/p"
_ligne = ("%d/%d bornes categories hook — tout temoin du depot est declenche par le hook"
          % (len(JOUEES) + 1 - len(KO), len(JOUEES) + 1))
_lu = subprocess.run(["sed", "-n", _sed], input=_ligne, capture_output=True, text=True).stdout.strip()
borne("⑪ le sed DU HARNAIS lit le DENOMINATEUR sur la ligne reellement imprimee",
      _lu == str(len(JOUEES) + 1))

print("%d/%d bornes categories hook — tout temoin du depot est declenche par le hook"
      % (len(JOUEES) - len(KO), len(JOUEES)))
for n in KO:
    print("  ✗ %s" % n)
sys.exit(1 if KO else 0)
