#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""L'AXE ① NE REGARDAIT QU'UN SEUL MAILLON — 12/11/2026.

INCIDENT. La veille imac du 08/11/2026 ecrivait « Windows 11 : jusque 2031 ». Ce chiffre est FAUX
(mesure du 18/10 : zero occurrence sur quatre pages de cycle de vie Microsoft) et la correction du
11/10 l'avait deja retire. Les editions du 25/10 et du 01/11 n'en portent AUCUNE occurrence : la
chaine de continuite avait donc perdu le jeton, et controle_edition_precedente.py, qui ne comparait
N qu'a N-1, a rendu « OK sur ses trois axes » trois semaines plus tard. Il avait raison au regard de
ce qu'il surveillait ; ce qui manquait est une memoire plus longue qu'UN maillon.

PROFONDEUR MESUREE SUR LES 120 EDITIONS, le .docx du 08/11 pris dans son etat d'AVANT correction :
K=3 perd l'incident (il est retire par l'edition du 11/10, soit N-4) · K=4 rend 2 signalements,
2 VRAIS, 0 faux · K=5, 6, 7 : verdicts IDENTIQUES · K=8 : premier faux positif. Bande vide de trois
rangs, d'ou PROFONDEUR = 4.

DEUX BORNES, et la mesure dit laquelle porte : la CHAINE (le jeton absent du corps de toute edition
entre E et N) et le JOURNAL DE N (le jeton n'y est pas discute — l'edition l'a traite). La seconde
retire les DEUX faux positifs de K=4, dont « 170 » dans la veille imac du 18/10, que son propre
journal re-source en disant « les 170 Go/s desormais litteraux sur la page Apple ».

NON BLOQUANT : un balayage retrospectif ne valide pas un motif bloquant (14/10), et ce controle a
deja produit deux faux refus en production, les 14/10 et 19/10, qui ont bloque TOUS les pushs.
D'ou des EXIGENCES DE LIGNE ici, et pas seulement un code de sortie.

Aucun reseau. Aucun fichier du depot dans le verdict : la serie est FABRIQUEE en tempfile — le
signalement unique du corpus reel disparaitra a la prochaine edition ou a la prochaine correction
(il a deja disparu une fois, le 12/11, en corrigeant le document de l'incident), et un temoin
ancre dessus perirait tout seul : c'est arrive quatre fois au depot, les 15, 22 et 23/10 et le 04/11.
"""
import os, re, subprocess, sys, tempfile, zipfile

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # outils/scripts
CTRL = os.path.join(RACINE, "controle_edition_precedente.py")
assert os.path.isfile(CTRL), "RACINE fausse : %s n'existe pas" % CTRL
SRC = open(CTRL, encoding="utf-8").read()
LIGNE = "  %d/%d bornes de la profondeur de l'axe 1 — une correction vieille de plusieurs editions est suivie"

jouees, ko = [], []
def borne(nom, cond, detail=""):
    jouees.append(nom)
    if not cond:
        ko.append(nom); print("  ✗ %s%s" % (nom, (" — " + detail) if detail else ""))

# ── le bloc de fonctions est EXTRAIT du controle et execute, jamais recopie (regle du 15/10)
G = {"__name__": "extrait"}
exec(compile(SRC[:SRC.index("if len(sys.argv) != 2:")], CTRL, "exec"), G)

# ── ① ② ③ ④ ⑤ la forme : profondeur au litteral, une seule enumeration, logique appelee
borne("① PROFONDEUR = 4 au litteral dans le controle",
      re.search(r"(?m)^PROFONDEUR = 4\b", SRC) is not None)
borne("② precedentes() enumere, et precedente() en DELEGUE — une seule enumeration",
      "def precedentes(" in SRC and re.search(r"def precedente\(p\):\s*\n\s*c = precedentes\(p, 1\)", SRC)
      is not None and SRC.count("glob.glob(os.path.join(d,") == 1,
      "globs=%d" % SRC.count("glob.glob(os.path.join(d,"))
borne("④ candidats_de() est APPELEE au moins deux fois — par ① et par ①bis",
      len(re.findall(r"(?<!def )candidats_de\(", SRC)) >= 2,
      "%d appel(s)" % len(re.findall(r"(?<!def )candidats_de\(", SRC)))
borne("⑤ vocabulaire() prend le corps en argument — un vocabulaire PAR edition",
      re.search(r"def vocabulaire\(corps\)", SRC) is not None and "vocabulaire(corps_p)" in SRC)

# ── la serie FABRIQUEE
DOC = ('<?xml version="1.0"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
       '<w:body>%s</w:body></w:document>')
def p(t):
    return "<w:p><w:r><w:t xml:space=\"preserve\">%s</w:t></w:r></w:p>" % (
        t.replace("&", "&amp;").replace("<", "&lt;"))
def docx(chemin, paras):
    with zipfile.ZipFile(chemin, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("word/document.xml", DOC % "".join(p(t) for t in paras))

def journal(entrees):
    return [p_ for p_ in ["Journal des corrections"] + entrees]

def edition(corps, entrees):
    return corps + journal(entrees)

def pose(d, nom, corps, entrees=()):
    docx(os.path.join(d, nom), edition(corps, list(entrees)))

# un jeton est RETIRE par E si sa citation est denoncee dans le journal de E et absente du corps de E
def retire(jeton, reste, pourquoi="ce nom ne figure sur aucune page citee."):
    return "¶9 — libelle d'origine : « %s %s » — %s" % (reste[0], jeton, pourquoi) if False else \
           "¶9 — libelle d'origine : « %s » — %s" % (reste, pourquoi)

T = tempfile.mkdtemp(prefix="axe1_")
A = os.path.join(T, "A"); B = os.path.join(T, "B"); C = os.path.join(T, "C")
for d in (A, B, C): os.makedirs(d)

# ─── ARBRE A : le scenario complet, exit 0 attendu
pose(A, "2026-01-04_veille_temoin.docx", ["Marche calme cette semaine."],
     [retire("XANADU", "le site XANADU recense les prix")])
pose(A, "2026-01-11_veille_temoin.docx", ["Rien de neuf sur les tarifs."],
     [retire("ZORGLUB", "procede ZORGLUB avance")])
pose(A, "2026-01-18_veille_temoin.docx", ["Semaine creuse, aucun fait nouveau."],
     [retire("MAGMA", "le moteur MAGMA equipe la gamme"),
      retire("GLOUBI", "la puce GLOUBI sort en mars")])
pose(A, "2026-01-25_veille_temoin.docx", ["Le moteur MAGMA equipe la gamme, source lue ce jour."],
     [retire("PLOUTOS", "le fonds PLOUTOS detient la marque"),
      retire("GLOUBI", "la puce GLOUBI sort en mars"),
      retire("SOLITUDE", "la SOLITUDE mesuree par Trucmuche")])
pose(A, "2026-02-01_veille_temoin.docx", ["Aucun element nouveau cette semaine."], [])
pose(A, "2026-02-01_veille_temoin.fiche.md", [])
open(os.path.join(A, "2026-02-01_veille_temoin.fiche.md"), "w").write("# fiche\nRien a signaler.\n")
pose(A, "2026-02-08_veille_temoin.docx",
     ["Le site XANADU recense les prix, releve du jour.",
      "Procede ZORGLUB avance, confirme par la page.",
      "Le moteur MAGMA equipe la gamme.",
      "La puce GLOUBI sort en mars.",
      "Le fonds PLOUTOS detient la marque.",
      "Rien d'autre. SOLITUDE. Fin de la rubrique."],
     ["Note du 08/02/2026 : le fonds PLOUTOS a ete re-source sur la page de l'autorite."])

# ─── ARBRE B : un rejeu de N-1 — le motif BLOQUANT doit mordre, ①bis se taire
pose(B, "2026-01-25_veille_temoin.docx", ["Rien de neuf."],
     [retire("ZORGLUB", "procede ZORGLUB avance")])
pose(B, "2026-02-01_veille_temoin.docx", ["Semaine calme."],
     [retire("TSMCBIS", "procede TSMCBIS avance")])
open(os.path.join(B, "2026-02-01_veille_temoin.fiche.md"), "w").write("# fiche\nRien a signaler.\n")
pose(B, "2026-02-08_veille_temoin.docx",
     ["Procede TSMCBIS avance, repris tel quel.", "Procede ZORGLUB avance, repris tel quel."], [])

# ─── ARBRE C : aucune edition avant N-1
pose(C, "2026-02-01_veille_temoin.docx", ["Semaine calme."], [])
open(os.path.join(C, "2026-02-01_veille_temoin.fiche.md"), "w").write("# fiche\nRien a signaler.\n")
pose(C, "2026-02-08_veille_temoin.docx", ["Semaine calme aussi."], [])

borne("③ precedentes() rend %d edition(s), la plus recente d'abord" % G["PROFONDEUR"],
      [os.path.basename(f)[:10] for _, f in
       G["precedentes"](os.path.join(A, "2026-02-08_veille_temoin.docx"), G["PROFONDEUR"])]
      == ["2026-02-01", "2026-01-25", "2026-01-18", "2026-01-11"])

def lance(chemin):
    r = subprocess.run([sys.executable, CTRL, chemin], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr

def bis(sortie):
    """la seule tranche ①bis de la sortie — on ne confond pas avec le motif ① de N-1"""
    i = sortie.index("①bis")
    j = sortie.index("\n② ", i)
    return sortie[i:j]

code_a, out_a = lance(os.path.join(A, "2026-02-08_veille_temoin.docx"))
z_a = bis(out_a)
borne("⑥ ZORGLUB, retire par N-4, est SIGNALE", "« ZORGLUB »" in z_a and "(N-4)" in z_a,
      z_a.replace("\n", " | ")[:300])
borne("⑦ GLOUBI est signale UNE SEULE fois, en nommant N-2 — deduplication",
      z_a.count("« GLOUBI »") == 1 and re.search(r"« GLOUBI » — retiré du corps de \S+ \(N-2\)", z_a)
      is not None, "%d occurrence(s)" % z_a.count("« GLOUBI »"))
borne("⑧ XANADU, retire par N-5, n'est PAS signale — hors profondeur (ACCEPTEE)",
      "XANADU" not in z_a)
borne("⑨ MAGMA, deja revenu en N-2, n'est PAS signale — borne de CHAINE (ACCEPTEE)",
      "MAGMA" not in z_a)
borne("⑩ PLOUTOS, dont le journal de N parle, n'est PAS signale mais est COMPTE (ACCEPTEE)",
      "PLOUTOS" not in z_a and "1 jeton(s) écarté(s)" in z_a, z_a.replace("\n", " | ")[-180:])
borne("⑪ SOLITUDE, revenue SEULE, n'est PAS signalee — borne du 19/10 preservee (ACCEPTEE)",
      "SOLITUDE" not in z_a)
borne("⑫ la ligne de decompte est imprimee, avec ses deux nombres",
      re.search(r"2 signalement\(s\) · 1 jeton\(s\) écarté\(s\)", z_a) is not None,
      z_a.replace("\n", " | ")[-180:])
borne("⑬ exit 0 : ①bis n'ajoute RIEN au code de sortie (ACCEPTEE)", code_a == 0,
      "exit=%d" % code_a)

code_b, out_b = lance(os.path.join(B, "2026-02-08_veille_temoin.docx"))
z_b = bis(out_b)
borne("⑭ un rejeu de N-1 reste BLOQUANT (exit 1) et ①bis ne s'en melange pas",
      code_b == 1 and "INTERDIT « TSMCBIS »" in out_b and "TSMCBIS" not in z_b,
      "exit=%d · interdit=%s" % (code_b, "INTERDIT « TSMCBIS »" in out_b))
borne("⑮ et le jeton retire par N-2 du MEME arbre est bien vu par ①bis",
      "« ZORGLUB »" in z_b and "(N-2)" in z_b, z_b.replace("\n", " | ")[:260])

code_c, out_c = lance(os.path.join(C, "2026-02-08_veille_temoin.docx"))
borne("⑯ sans edition avant N-1, ①bis se declare INERTE et ne se tait pas",
      "aucune édition avant" in bis(out_c) and "INERTE" in bis(out_c),
      bis(out_c).replace("\n", " | ")[:200])

# ── ⑰ LE GARDE DU HARNAIS LIT-IL VRAIMENT CETTE LIGNE ? (defaut du 04/11, non repaye)
NR_SH = os.path.join(RACINE, "non_regression.sh")
m_sed = re.search(r'LU_EP=\$\(sed -n "([^"]+)" "\$EP_OUT"\)', open(NR_SH, encoding="utf-8").read())
lu = ""
if m_sed:
    lu = subprocess.run(["sed", "-n", m_sed.group(1)], input=LIGNE % (16, 17),
                        capture_output=True, text=True).stdout.strip()
borne("⑰ le motif du harnais, applique a la ligne reellement imprimee, rend le DENOMINATEUR",
      bool(m_sed) and lu == "17", "motif=%s · lu=%r (17 attendu)" % (bool(m_sed), lu))

import shutil; shutil.rmtree(T, ignore_errors=True)

# ── EXIGENCES DE LIGNE : le motif est NON BLOQUANT, un exit 0 ne prouve pas qu'il a parle.
print("  ①bis portee : ZORGLUB vu a N-4 · GLOUBI dedupe a N-2 · XANADU hors profondeur ·"
      " MAGMA couvert par la chaine · PLOUTOS traite par le journal de N · SOLITUDE seule")
print("  ①bis cadre : N-1 reste bloquant (exit 1) · exit 0 quand seul ①bis parle ·"
      " INERTE sans edition avant N-1")
print(LIGNE % (len(jouees) - len(ko), len(jouees)))
sys.exit(1 if ko else 0)
