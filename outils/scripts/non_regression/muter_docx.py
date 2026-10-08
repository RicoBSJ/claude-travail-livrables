#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""muter_docx.py — fabrique une copie MUTÉE d'un .docx, pour prouver qu'un contrôle mord.

Écrit le 08/10/2026 en câblant `controle_astrologie_karmique.py` et
`controle_psychopathologie.py` dans `non_regression.sh`.

⚠️ POURQUOI UNE MUTATION ET PAS UN TÉMOIN FIGÉ DE REFUS. Un témoin d'avant correction
prouve qu'un contrôle refuse encore ce qu'il refusait. Mais pour ces deux étapes 5 bis,
les seuls documents du dépôt que l'une d'elles refuse aujourd'hui le font sur des FAUX
POSITIFS : `controle_astrologie_karmique.py` rend six motifs ⑤ sur la leçon n°10 pour des
exonymes français — « Cérès » là où la NASA écrit « Ceres », « Alger » pour « Algiers »,
« Centre » pour « Center » — plus l'étiquette de section « Citation ». Figer un de ces
refus comme témoin inscrirait le bug dans le harnais, et le harnais échouerait le jour
où on le corrige. La mutation ne prouve qu'une chose, et c'est la bonne : le test mord.

La copie mutée est écrite là où on la demande (un répertoire temporaire), jamais dans le
dépôt, et l'appelant la supprime. Aucune mutation n'est committée.

Usage : muter_docx.py <source.docx> <destination.docx> <motif>
Motifs :
  ligature  — injecte un paragraphe contenant « Noeud » sans ligature, hors adresse web
              → doit déclencher le motif ① de controle_astrologie_karmique.py
  fraction  — injecte « Selon la HAS, un tiers des personnes … » sans effectif ni %
              → doit déclencher le motif (2) de controle_psychopathologie.py
"""
import re, sys, zipfile

TEXTES = {
    "ligature": "Le Noeud Nord est ici cité sans sa ligature, hors de toute adresse web.",
    "fraction": "Selon la HAS, un tiers des personnes concernées ne sont pas informées de leurs droits.",
}

def main():
    if len(sys.argv) != 4:
        sys.exit("usage : muter_docx.py <source.docx> <destination.docx> <%s>" % "|".join(TEXTES))
    src, dst, motif = sys.argv[1:4]
    if motif not in TEXTES:
        sys.exit("motif inconnu : %s (connus : %s)" % (motif, ", ".join(TEXTES)))
    z = zipfile.ZipFile(src)
    x = z.read("word/document.xml").decode("utf-8")
    font = ('<w:rFonts w:ascii="Times New Roman" w:cs="Times New Roman" '
            'w:hAnsi="Times New Roman"/>')
    txt = (TEXTES[motif].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                        .replace("'", "&apos;"))
    para = ('<w:p><w:pPr><w:spacing w:after="120"/></w:pPr><w:r><w:rPr>' + font
            + '<w:sz w:val="22"/></w:rPr><w:t xml:space="preserve">' + txt
            + '</w:t></w:r></w:p>')
    # avant <w:sectPr> : le paragraphe est dans le corps, pas après le journal des
    # corrections — les deux contrôles ignorent ce qui suit « 📝 Journal des corrections »
    i = x.find("<w:sectPr")
    if i < 0:
        sys.exit("sectPr introuvable dans %s" % src)
    j = x.find("Journal des corrections")
    if 0 <= j < i:
        # le document porte un journal : on insère AVANT lui, sinon la mutation est ignorée
        k = x.rfind("<w:p", 0, j)
        if k < 0:
            sys.exit("impossible de placer la mutation avant le journal de %s" % src)
        i = k
    x = x[:i] + para + x[i:]
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as out:
        for it in z.infolist():
            data = x.encode("utf-8") if it.filename == "word/document.xml" else z.read(it.filename)
            out.writestr(it, data)
    bad = zipfile.ZipFile(dst).testzip()
    if bad:
        sys.exit("archive mutée invalide : %s" % bad)
    print("mutation « %s » injectée : %s" % (motif, dst))

main()
