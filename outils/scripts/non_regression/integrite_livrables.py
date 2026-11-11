#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Témoin figé de `controle_integrite_livrables.py` — un livrable PUBLIÉ est-il intact ?

⛔ IL NE PEUT PAS SE PÉRIMER : aucun réseau, aucun tiers, aucune date, aucun fichier
vivant du dépôt dans le verdict. Tout est fabriqué en `tempfile`, dépôt git compris.
Quatre témoins VIVANTS ont bloqué TOUS les pushs du dépôt les 15, 22, 23/10 et 04/11 ;
l'invariant gardé ici ne devient faux que si le contrôle cesse de distinguer une
corruption d'une correction en cours.

LE CLASSIFIEUR EST EXTRAIT DU CONTRÔLE, JAMAIS RECOPIÉ (règle du 15/10) : la tranche
entre les deux marqueurs `──8<──` est lue puis exécutée. Si elle disparaît, la borne ⑰
le dit au lieu de rester verte sur du vide.

🔴 ET LA BORNE QUI COMPTE LE PLUS EST ⑭, NÉE D'UN DÉFAUT À MOI AU PREMIER ESSAI :
`RACINE` pointait sur `outils/` (deux `parent` au lieu de trois), `git ls-files` rendait
ZÉRO fichier, et le verdict imprimait « 0 divergence(s) » avec exit 0 — UN VERT SUR UN
PÉRIMÈTRE JAMAIS REGARDÉ. Un classifieur juste ne garde rien si le périmètre est vide :
⑭ exige donc que le compte de suivis soit NON NUL sur un dépôt propre fabriqué.
"""
import io, os, pathlib, re, subprocess, sys, tempfile, zipfile
from contextlib import redirect_stdout

RACINE = pathlib.Path(__file__).resolve().parent.parent.parent.parent
# ⚠️ QUATRE parent : ce témoin vit dans outils/scripts/non_regression/, un cran
# plus bas que les contrôles. Trois donnaient outils/ — le bug de
# tolerance_page_morte.py (23/10) et coherence_skill.py (27/10), reproduit ICI
# au premier essai, et c'est l'assertion qui l'a dit, pas la relecture.
CONTROLE = RACINE / "outils" / "scripts" / "controle_integrite_livrables.py"
assert (RACINE / "jobs_config.json").exists(), "RACINE ne pointe pas sur la racine : %s" % RACINE

KO, JOUEES = [], []
def borne(nom, condition):
    JOUEES.append(nom)
    if not condition:
        KO.append(nom)

# ── ⑰ extraction du classifieur, jamais une copie
src = CONTROLE.read_text()
DEB = "# ──8<── CLASSIFICATION"
FIN_ = "# ──8<── FIN CLASSIFICATION"
borne("le classifieur est EXTRAIT du controle (les deux marqueurs sont la)",
      DEB in src and FIN_ in src and src.index(DEB) < src.index(FIN_))
tranche = src[src.index(DEB):src.index(FIN_)] if (DEB in src and FIN_ in src) else ""
G = {"hashlib": __import__("hashlib"), "io": io, "pathlib": pathlib, "re": re, "zipfile": zipfile}
exec(compile(tranche, str(CONTROLE), "exec"), G)
classe, sha1_blob, caracteres = G["classe"], G["sha1_blob"], G["caracteres"]

def code_tranche_findall():
    """La tranche, docstrings et commentaires retires : on ne teste que du CODE."""
    sans = re.sub(r'"""(?:.|\n)*?"""', '""', tranche)
    return re.sub(r"#[^\n]*", "", sans)

def docx(n, casse=False):
    b = io.BytesIO()
    with zipfile.ZipFile(b, "w") as z:
        z.writestr("word/document.xml",
                   "<w:document><w:tbl><w:tr><w:tc><w:t>%s</w:t></w:tc></w:tr></w:tbl></w:document>" % ("a" * n))
    return b"pas un zip du tout" if casse else b.getvalue()

# ──────── bornes du classifieur
borne("① un fichier identique a HEAD est intact",
      classe(b"x" * 100, b"x" * 100, "livrables/lecons/a/x.md", set())[0] is None)
borne("② un fichier suivi mais disparu du disque est ABSENT et bloquant",
      classe(None, b"x", "livrables/lecons/a/x.md", set())[:1] == ("ABSENT",) and
      classe(None, b"x", "livrables/lecons/a/x.md", set())[2])
borne("③ un .md porteur d'un octet NUL est NUL",
      classe(b"abc\0\0", b"abcd", "sources/veille/a/x.md", set())[0] == "NUL")
borne("④ un .pdf porteur d'un octet NUL n'est PAS NUL — binaire legitime (ACCEPTEE)",
      classe(b"abc\0\0", b"abcd", "livrables/documents/x.pdf", set())[0] != "NUL")
borne("⑤ le contenu NUL-rogne egal a un blob PASSE est REVENU",
      classe(b"ancien\0\0\0", b"nouveau", "livrables/documents/x.pdf",
             {sha1_blob(b"ancien")})[0] == "REVENU")
borne("⑥ un .docx qui perd 30 % de son texte est AMPUTE",
      classe(docx(700), docx(1000), "livrables/lecons/a/x.docx", set())[0] == "AMPUTÉ")
borne("⑦ un .docx qui perd 15 % reste DIVERGENT — plancher mesure, pas resserrable (ACCEPTEE)",
      classe(docx(850), docx(1000), "livrables/lecons/a/x.docx", set())[0] == "DIVERGENT")
borne("⑧ un .docx qui ne s'ouvre plus est ZIP",
      classe(docx(0, casse=True), docx(1000), "livrables/lecons/a/x.docx", set())[0] == "ZIP")
borne("⑨ DIVERGENT n'est PAS bloquant — indiscernable d'une correction (ACCEPTEE)",
      classe(docx(850), docx(1000), "livrables/lecons/a/x.docx", set())[2] is False)
borne("⑩ les cinq autres classes SONT bloquantes",
      all(classe(*a)[2] for a in (
          (None, b"x", "livrables/lecons/a/x.md", set()),
          (b"a\0", b"ab", "livrables/lecons/a/x.md", set()),
          (b"ancien", b"neuf", "livrables/documents/x.pdf", {sha1_blob(b"ancien")}),
          (docx(0, casse=True), docx(1000), "livrables/lecons/a/x.docx", set()),
          (docx(700), docx(1000), "livrables/lecons/a/x.docx", set()))))
borne("⑪ le plancher est au LITTERAL dans le controle (SEUIL_AMPUTE = 20.0)",
      re.search(r"^SEUIL_AMPUTE\s*=\s*20\.0\b", tranche, re.M) is not None)
# ⚠️ ON LIT LE MOTIF RÉELLEMENT PASSÉ À re.findall, pas le texte du fichier : le contrôle
# CITE le motif fautif dans l'avertissement qui en met en garde (et dans une docstring, que
# neutraliser les « # » ne touche pas), donc un test textuel accuserait sa propre
# documentation — même piège que la coquille citée qui s'immunisait elle-même (27/10).
_mf = re.search(r"re\.findall\(r\"([^\"]+)\"", code_tranche_findall())
borne("⑫ le motif de caracteres() est ancre : <w:t suivi d'une ESPACE ou de >, "
      "sans quoi il apparie AUSSI <w:tbl>, <w:tc>, <w:tr>",
      _mf is not None and _mf.group(1) == r"<w:t(?:\s[^>]*)?>(.*?)</w:t>")
borne("⑬ le compte de caracteres ignore les balises de tableau",
      caracteres(docx(1000)) == 1000)

# ──────── bornes de bout en bout, sur un depot git FABRIQUE
def depot(tmp):
    E = dict(os.environ, GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_SYSTEM="/dev/null",
             GIT_AUTHOR_NAME="T", GIT_AUTHOR_EMAIL="t@local",
             GIT_COMMITTER_NAME="T", GIT_COMMITTER_EMAIL="t@local")
    for v in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE","GIT_OBJECT_DIRECTORY",
              "GIT_COMMON_DIR","GIT_QUARANTINE_PATH","GIT_ALTERNATE_OBJECT_DIRECTORIES","GIT_PREFIX"):
        E.pop(v, None)
    def g(*a): subprocess.run(["git"] + list(a), cwd=tmp, env=E, capture_output=True, check=True)
    for d in ("livrables/lecons/x", "sources/veille/y", "outils/scripts"):
        (tmp / d).mkdir(parents=True, exist_ok=True)
    (tmp / "livrables/lecons/x/a.docx").write_bytes(docx(1000))
    (tmp / "livrables/lecons/x/b.md").write_bytes(b"# fiche\ntexte\n")
    (tmp / "sources/veille/y/c.docx").write_bytes(docx(2000))
    (tmp / "outils/scripts/hors-perimetre.md").write_bytes(b"# hors liste blanche\n")
    g("init", "-q", "."); g("add", "-A"); g("commit", "-qm", "etat publie")
    return g

with tempfile.TemporaryDirectory() as d:
    tmp = pathlib.Path(d); g = depot(tmp)
    # verdict() vit HORS de la tranche extraite : on importe le module et on lui
    # passe la racine fabriquée, donc c'est le VRAI parcours de dépôt qui est exercé.
    import importlib.util
    spec = importlib.util.spec_from_file_location("cil", CONTROLE)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

    s = io.StringIO()
    with redirect_stdout(s):
        exit_propre = m.verdict(racine=tmp)
    sortie = s.getvalue()
    suivis = re.search(r"(\d+) suivi\(s\)", sortie)
    borne("⑭ depot propre FABRIQUE : exit 0 ET le perimetre est NON VIDE (vert-sur-du-vide)",
          exit_propre == 0 and suivis is not None and int(suivis.group(1)) == 3)   # 3 dans la liste blanche, le 4e est sous outils/

    # on abime les trois, chacun d'une façon mesurée sur l'incident du 10/11
    (tmp / "livrables/lecons/x/a.docx").write_bytes(docx(700))                    # −30 %
    (tmp / "livrables/lecons/x/b.md").write_bytes(b"# fiche\ntexte\n" + b"\0" * 50)
    (tmp / "sources/veille/y/c.docx").write_bytes(docx(0, casse=True))
    (tmp / "outils/scripts/hors-perimetre.md").write_bytes(b"\0" * 20)            # hors perimetre
    s = io.StringIO()
    with redirect_stdout(s):
        exit_abime = m.verdict(racine=tmp)
    sortie = s.getvalue()
    borne("⑮ les trois classes sont nommees et le verdict refuse",
          exit_abime == 1 and "AMPUTÉ" in sortie and "NUL" in sortie and "ZIP" in sortie
          and "3 bloquante(s)" in sortie)
    borne("⑯ un fichier HORS liste blanche n'est pas accuse, meme bourre de NUL (ACCEPTEE)",
          "hors-perimetre.md" not in sortie)
    borne("⑰ le verdict dit ou restaurer", "git checkout --" in sortie)
    (tmp / "livrables/lecons/x/a.docx").unlink()
    s = io.StringIO()
    with redirect_stdout(s):
        m.verdict(racine=tmp)
    borne("⑱ un livrable suivi SUPPRIME du disque est ABSENT et bloquant",
          "ABSENT" in s.getvalue())

# ⚠️ ANCRE ASCII ET SANS ACCENT : le harnais lit ce dénominateur par `sed` sous `env -i`,
# donc sans locale. La dérive d'un libellé accentué a déjà fait lire un dénominateur VIDE
# et refuser TOUS les pushs (04/11). La borne ⑳ applique CE motif à CETTE ligne.
LIGNE = ("%d/%d bornes integrite livrables — un livrable publié abîmé sur le disque est "
         "nommé, et une correction en cours ne l'est pas" % (len(JOUEES) + 1 - len(KO), len(JOUEES) + 1))
import subprocess as _sp
_sed = r"s/^[[:space:]]*\([0-9]\{1,\}\)\/\([0-9]\{1,\}\) bornes integrite livrables.*/\2/p"
_lu = _sp.run(["sed", "-n", _sed], input=LIGNE, capture_output=True, text=True).stdout.strip()
borne("⑳ le sed DU HARNAIS lit le DENOMINATEUR sur la ligne reellement imprimee",
      _lu == str(len(JOUEES) + 1))
LIGNE = ("%d/%d bornes integrite livrables — un livrable publié abîmé sur le disque est "
         "nommé, et une correction en cours ne l'est pas" % (len(JOUEES) - len(KO), len(JOUEES)))
print(LIGNE)
for n in KO:
    print("  ✗ %s" % n)
sys.exit(1 if KO else 0)
