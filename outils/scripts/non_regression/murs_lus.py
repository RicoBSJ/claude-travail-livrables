#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""murs_lus.py — une source donnée pour LUE peut-elle s'avouer sous le plancher de lisibilité ?

Usage : /usr/bin/python3 outils/scripts/non_regression/murs_lus.py
Sort en 0 si les bornes passent, en 1 sinon. AUCUN RÉSEAU, aucun tiers, rien de vivant dans le
verdict : les jetons et le .docx de bout en bout sont FABRIQUÉS en tempfile (leçon du 22/10).

Né le 05/11/2026. Le dépôt tient qu'au-dessous de 3 000 caractères utiles une page est une
façade, et qu'une mention absente y est INDISCERNABLE d'une mention non lue (règle du 12/10).
Deux éditions en six jours ont pourtant porté « ✅ » sur une ligne dont la remarque annonçait
elle-même un compte sous ce plancher — ai-act 30/10 (2 758 car., quand les éditions des 17/10
et 24/10 marquaient ⚠ LA MÊME page, l'une écrivant « sous le seuil … Rien n'en est tiré ») et
SERAFIN-PH 04/11 (93 car. pour un mur anti-automate). AUCUN motif du dépôt ne regardait la
conjonction des deux cellules, et c'était structurel : controle_decompte.py comptait les
symboles sans lire les remarques, controle_attributions.py lit les citations sans voir les
statuts, et ㊳ bis ne relève que les décomptes de liens écrits dans le LOG.

Ce que ce témoin garde, et pourquoi aucune borne n'est redondante :
  · le motif signale la ligne fautive et rend le bon compte (③⑭) ;
  · il n'accuse PAS ⚠, ⛔ ni le repli ⛔/✅ (④⑤⑥) : ce sont les marques HONNÊTES d'une façade,
    et des lignes légitimes du dépôt le prouvent (ai-act 17/10 et 24/10, SERAFIN-PH 21/10) ;
  · il n'accuse PAS une cellule qui dit la façade ET le compte du contenu lu ailleurs (⑦) :
    c'est la forme CORRIGÉE du 04/11 — sans cette borne, rien n'empêche de la réélargir demain ;
  · la portée de cette exemption est la CELLULE et non la ligne (⑧) — borne FABRIQUÉE, et dite
    telle : les deux formes rendent des verdicts identiques sur les 47 documents du dépôt qui
    annoncent un compte sous le plancher, donc le choix est préventif et il faut qu'il soit
    épinglé, sans quoi il se réélargirait sans que rien ne le dise ;
  · le plancher mord à 2 999 et pas à 3 000 (⑨⑩) ;
  · un compte de la PROSE ne remonte pas à la dernière ligne du tableau (⑪) : distances
    mesurées entre un ✅ et un compte hors tableau — 9 · 12 · 15 · 21 · 47 · 48 · 95 · 107 · 108 ;
  · un compte cité dans un MARQUEUR de correction n'est pas relu (⑫⑬), « é » décomposé compris :
    un marqueur CONSERVE par doctrine le libellé fautif, le relire rouvrirait le motif qu'on
    vient de fermer (leçons des 23 et 25/10) ;
  · « octets » n'est pas « caractères » (⑮), et un sous-titre porteur de ✅ n'ouvre pas une ligne
    qui avalerait tout son groupe (⑯) ;
  · le contrôle APPELLE la fonction et IMPRIME sa ligne (⑰⑱) — une fonction juste jamais appelée
    n'écrit dans aucun log (leçon du 27/10) ;
  · le motif ne change AUCUN code de sortie (⑲) : il est NON BLOQUANT ;
  · le garde de compte du harnais lit la ligne que ce témoin imprime RÉELLEMENT (⑳) ;
  · et le gate --docs REMONTE cette ligne au lieu de la laisser dans son fichier
    temporaire (㉑) — une alerte que personne ne lit n'existe pas (27/10).
Le bloc testé est EXTRAIT du contrôle et exécuté, jamais recopié (règle du 15/10/2026) : si la
fonction ou le plancher en disparaissent, le témoin le dit au lieu de rester vert sur du vide.
"""
import os, re, sys, subprocess, tempfile, zipfile, unicodedata

# 23/10/2026 — le bug de tolerance_page_morte.py : ce script vit UN CRAN plus bas que les
# contrôles, donc un dirname de trop (ou de moins) et tout ce qui suit mesure à côté.
RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CTRL = os.path.join(RACINE, "controle_decompte.py")
assert os.path.isfile(CTRL), "RACINE fausse : %s n'existe pas" % CTRL
NR_SH = os.path.join(RACINE, "non_regression.sh")
SENTINELLE = "SOURCE DONNÉE POUR LUE SOUS LE PLANCHER"

LIGNE = "  %d/%d bornes de la source donnee pour lue"   # format PARTAGÉ avec la borne ⑳
jouees, ko = [], []
def borne(nom, cond, detail=""):
    jouees.append(nom)
    if not cond:
        ko.append(nom)
        print("  ✗ %s%s" % (nom, (" — " + detail) if detail else ""))

SRC = open(CTRL, encoding="utf-8").read()

# ── ① le bloc est EXTRAIT du contrôle, jamais recopié
deb = SRC.find("PLANCHER_LISIBLE = ")
fin = SRC.find("\ndef norm(s):")
borne("① le contrôle porte le motif : PLANCHER_LISIBLE et murs_donnes_pour_lus extractibles",
      deb != -1 and fin != -1 and deb < fin, "deb=%d fin=%d" % (deb, fin))
if ko:
    print("  ✗ extraction impossible — le reste du lot ne prouverait rien")
    print(LIGNE % (len(jouees) - len(ko), len(jouees)))
    sys.exit(1)
G = {"re": re, "unicodedata": unicodedata}
exec(compile(SRC[deb:fin], CTRL, "exec"), G)
murs, PLANCHER = G["murs_donnes_pour_lus"], G["PLANCHER_LISIBLE"]
borne("② plancher de lisibilité à 3 000 caractères", PLANCHER == 3000, "lu=%r" % PLANCHER)

def T(*cellules):
    """fabrique une ligne de jetons du contrôle : [type, symbole, texte, consommé]"""
    return [list(c) + [False] for c in cellules]

# ── ③ la ligne fautive est signalée, et avec le bon compte
l = T(("STAT", "✅", "✅"), ("NAME", None, "Handicap.gouv.fr — 14e comité stratégique"),
      ("NAME", None, "Source primaire lue (rendu JS, 93 car. utiles)"))
r = murs(l)
borne("③ ✅ + « 93 car. utiles » → signalé, compte 93", len(r) == 1 and r[0][0] == 93, "rendu=%r" % r)

# ── ④⑤⑥ les autres symboles sont la marque HONNÊTE d'une façade : ACCEPTÉS
for nom, sym in (("④ ACCEPTÉE : ⚠ + 93 car. n'est pas accusé", "⚠"),
                 ("⑤ ACCEPTÉE : ⛔ + 93 car. n'est pas accusé", "⛔"),
                 ("⑥ ACCEPTÉE : le repli ⛔/✅ n'est pas accusé", "repli")):
    l = T(("STAT", sym, sym), ("NAME", None, "Mur JavaScript : 93 caractères servis"))
    borne(nom, murs(l) == [], "rendu=%r" % murs(l))

# ── ⑦ ACCEPTÉE : la façade DITE et le contenu lu ailleurs (forme CORRIGÉE du 04/11/2026)
l = T(("STAT", "✅", "✅"),
      ("NAME", None, "Page murée : HTTP 200 mais 93 caractères utiles (mur anti-automate). "
                     "Contenu lu sur un instantané d'archive du 18/05/2026 (5 761 caractères)"))
borne("⑦ ACCEPTÉE : 93 car. ET 5 761 car. dans la MÊME cellule", murs(l) == [], "rendu=%r" % murs(l))

# ── ⑧ la portée de l'exemption est la CELLULE, pas la ligne. BORNE FABRIQUÉE, et dite telle :
#    aucune ligne du dépôt ne sépare les deux comptes en deux cellules, donc le choix est
#    PRÉVENTIF — retenu parce que le motif est non bloquant et que son erreur chère est le
#    silence, pas le bruit. Sans cette borne, la portée se réélargirait sans que rien ne le dise.
l = T(("STAT", "✅", "✅"), ("NAME", None, "Page murée : 93 caractères utiles"),
      ("NAME", None, "Contenu lu sur une archive (5 761 caractères)"))
borne("⑧ exemption bornée à la CELLULE : deux cellules séparées → signalé",
      len(murs(l)) == 1 and murs(l)[0][0] == 93, "rendu=%r" % murs(l))

# ── ⑨⑩ le plancher mord juste au-dessous, pas à sa valeur
l = T(("STAT", "✅", "✅"), ("NAME", None, "Consultée (2 999 car.)"))
borne("⑨ 2 999 car. → signalé", len(murs(l)) == 1, "rendu=%r" % murs(l))
l = T(("STAT", "✅", "✅"), ("NAME", None, "Consultée (3 000 car.)"))
borne("⑩ ACCEPTÉE : 3 000 car. n'est pas sous le plancher", murs(l) == [], "rendu=%r" % murs(l))

# ── ⑪ ACCEPTÉE : un compte de la PROSE ne remonte pas à la dernière ligne du tableau
l = T(("STAT", "✅", "✅"), ("NAME", None, "ATIH — Recueil national PH 2025"),
      ("NAME", None, "Source primaire lue (8 903 car.)"),
      ("SUB", None, "🔵 En bref — Tableau de bord"),
      ("NAME", None, "La page du Conseil est un vrai mur (130 caractères)."))
borne("⑪ ACCEPTÉE : un compte hors de la ligne ne lui est pas imputé", murs(l) == [], "rendu=%r" % murs(l))

# ── ⑫⑬ ACCEPTÉES : un compte cité dans un MARQUEUR de correction n'est pas relu
#    ⚠️ CES DEUX BORNES NE DISCRIMINAIENT PAS AU PREMIER JET, ET C'EST LE SABOTAGE QUI L'A DIT.
#    Le libellé portait « Consultée (8 903 car.) » HORS du marqueur : sans l'exemption des
#    marqueurs, la cellule contenait alors un compte BAS (93, dans le marqueur) ET un compte
#    HAUT (8 903), donc la borne ⑦ l'exemptait de toute façon et le témoin passait pour la
#    MAUVAISE raison. Le libellé ne porte donc plus AUCUN autre compte : le seul nombre de la
#    cellule est dans le marqueur, et l'exemption des marqueurs est la seule chose qui l'écarte.
MARQ = ("Consultée, sans élément nouveau [Corrigé le 04/11/2026 : la remarque disait « lue » "
        "une page qui ne rend que 93 caractères utiles]")
l = T(("STAT", "✅", "✅"), ("NAME", None, unicodedata.normalize("NFC", MARQ)))
borne("⑫ ACCEPTÉE : 93 car. cité dans un marqueur de correction", murs(l) == [], "rendu=%r" % murs(l))
l = T(("STAT", "✅", "✅"), ("NAME", None, unicodedata.normalize("NFD", MARQ)))
borne("⑬ ACCEPTÉE : marqueur à « é » DÉCOMPOSÉ", murs(l) == [], "rendu=%r" % murs(l))

# ── ⑭ les séparateurs de milliers sont lus pour ce qu'ils valent
l = T(("STAT", "✅", "✅"), ("NAME", None, "— Consultée (2 758 car.), dates d'échéances vérifiées"))
r = murs(l)
borne("⑭ « 2 758 car. » vaut 2758, pas 2", len(r) == 1 and r[0][0] == 2758, "rendu=%r" % r)

# ── ⑮ « octets » n'est pas « caractères »
l = T(("STAT", "✅", "✅"), ("NAME", None, "Page lue (6 078 octets bruts)"))
borne("⑮ ACCEPTÉE : « octets » n'est pas un compte de caractères", murs(l) == [], "rendu=%r" % murs(l))

# ── ⑯ un sous-titre porteur de ✅ n'ouvre pas une ligne qui avalerait son groupe
l = T(("SUB", "✅", "✅ Sources directement lues :"),
      ("NAME", None, "Index MIT — page de 538 caractères, citée pour le nom du traducteur"))
borne("⑯ ACCEPTÉE : un SUB porteur de ✅ n'est pas une ligne", murs(l) == [], "rendu=%r" % murs(l))

# ── ⑰⑱ le contrôle APPELLE la fonction et IMPRIME sa ligne
borne("⑰ le contrôle appelle murs_donnes_pour_lus(toks)",
      re.search(r"in murs_donnes_pour_lus\(toks\)", SRC) is not None)
borne("⑱ le contrôle imprime la sentinelle du motif", SENTINELLE in SRC)

# ── ⑲ de bout en bout sur un .docx FABRIQUÉ, et le motif ne change aucun code de sortie
def docx(chemin, lignes):
    ps = "".join('<w:p><w:r><w:t xml:space="preserve">%s</w:t></w:r></w:p>' % l for l in lignes)
    z = zipfile.ZipFile(chemin, "w", zipfile.ZIP_DEFLATED)
    z.writestr("[Content_Types].xml",
               '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
               '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
               '<Default Extension="xml" ContentType="application/xml"/>'
               '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.'
               'relationships+xml"/><Override PartName="/word/document.xml" ContentType='
               '"application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
               '</Types>')
    z.writestr("_rels/.rels",
               '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns='
               '"http://schemas.openxmlformats.org/package/2006/relationships"><Relationship '
               'Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships'
               '/officeDocument" Target="word/document.xml"/></Relationships>')
    z.writestr("word/document.xml",
               '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w='
               '"http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>%s'
               '</w:body></w:document>' % ps)
    z.writestr("word/_rels/document.xml.rels",
               '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns='
               '"http://schemas.openxmlformats.org/package/2006/relationships"/>')
    z.close()

LIGNES = ["Veille fabriquée — témoin murs_lus", "📚 Sources du jour",
          "✅", "Site A — page institutionnelle", "https://exemple.invalid/a",
          "Source primaire lue (rendu JS, 93 car. utiles)",
          "✅", "Site B — page institutionnelle", "https://exemple.invalid/b",
          "Source primaire lue (8 903 car.)",
          "⛔", "Site C — page institutionnelle", "https://exemple.invalid/c",
          "Anti-robot (403)",
          "Sources : 2/3 consultées"]
with tempfile.TemporaryDirectory() as d:
    p = os.path.join(d, "temoin_murs.docx")
    docx(p, LIGNES)
    res = subprocess.run(["/usr/bin/python3", CTRL, p], capture_output=True, text=True,
                         env={"PATH": "/usr/bin:/bin"})
    out = res.stdout + res.stderr
    borne("⑲ de bout en bout : le motif mord sur un .docx fabriqué, SANS changer le code de sortie",
          SENTINELLE in out and "93 caractères annoncés" in out and "liste :" in out
          and res.returncode in (0, 1, 2),
          "exit=%s sortie=%r" % (res.returncode, out[-220:]))

# ── ⑳ LE GARDE DE COMPTE DU HARNAIS LIT-IL VRAIMENT CETTE LIGNE ? (défaut à moi, 04/11/2026)
#    Un motif qui exige un caractère PUIS une espace avant le numérateur rend « vide » sur une
#    ligne commençant en colonne 1 : le harnais REFUSE alors tous les pushs, et avec une
#    comparaison inversée il les ACCEPTERAIT tous. On applique le motif DU HARNAIS à la ligne
#    que ce témoin imprime RÉELLEMENT.
m_sed = re.search(r'LU_MUR=\$\(sed -n "([^"]+)" "\$MUR_OUT"\)', open(NR_SH, encoding="utf-8").read())
lu = ""
if m_sed:
    lu = subprocess.run(["sed", "-n", m_sed.group(1)], input=LIGNE % (20, 21),
                        capture_output=True, text=True).stdout.strip()
borne("⑳ le motif du harnais, appliqué à la ligne imprimée, rend le DÉNOMINATEUR",
      bool(m_sed) and lu == "21", "motif=%s · lu=%r (21 attendu)" % (bool(m_sed), lu))

# ── ㉑ LE GATE REMONTE-T-IL LA LIGNE ? (27/10/2026 : une alerte que personne ne lit n'existe pas)
#    Le bloc « --docs » CAPTURE la sortie du contrôle dans $CUR/doc_dec.txt et n'imprime qu'un
#    ✓/✗ : sans remontée explicite, le motif mourrait dans un fichier temporaire. C'est le trou
#    exact comblé le 27/10 pour l'alerte d'étiquette HAS, et il s'est reproduit ici au PREMIER
#    essai du gate — mesuré, pas relu.
SH = open(NR_SH, encoding="utf-8").read()
borne("㉑ le gate --docs remonte la ligne du motif depuis doc_dec.txt",
      re.search(r'grep -h "' + re.escape(SENTINELLE) + r'" "\$CUR/doc_dec\.txt"', SH) is not None)

print(LIGNE % (len(jouees) - len(ko), len(jouees)))
sys.exit(1 if ko else 0)
