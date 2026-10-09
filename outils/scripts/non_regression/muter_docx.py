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
  alerte    — injecte un paragraphe « 🟢 Niveau d'alerte : VERT … » dans une note qui
              annonce des faits marquants (ajouté le 09/10/2026, en sortant
              controle_ai_act.py de son prompt)
              → doit déclencher le motif (6) de controle_ai_act.py. Ce motif ne coûte
                AUCUN appel réseau : la mutation se juge sur le document seul, même si
                le reste du script, lui, rouvre les pages de la note.
"""
import re, sys, zipfile
import xml.etree.ElementTree as ET

TEXTES = {
    "ligature": "Le Noeud Nord est ici cité sans sa ligature, hors de toute adresse web.",
    "fraction": "Selon la HAS, un tiers des personnes concernées ne sont pas informées de leurs droits.",
    "alerte": "\U0001F7E2  Niveau d'alerte : VERT — paragraphe de mutation, injecté par le harnais.",
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
        # Le document porte un journal : on insère AVANT lui, sinon la mutation est ignorée
        # (les contrôles coupent à « Journal des corrections »).
        # ⚠️ CORRIGÉ LE 09/10/2026. La première version faisait x.rfind("<w:p", 0, j), ce qui
        # tombait sur le <w:pPr> DU paragraphe du journal : la mutation s'insérait ENTRE <w:p>
        # et <w:pPr>, le paragraphe du titre n'était plus un <w:p>…</w:p> complet, aucun
        # paragraphe ne contenait plus « Journal des corrections » — et le contrôle lisait
        # tout le journal. Le mutant restait un XML valide, donc rien ne le signalait. La
        # branche tournait depuis le 08/10 sur le témoin d'astrologie n°09, qui porte un
        # journal ; son exit 1 venait du bon motif, mais le document était malformé.
        # On repère désormais le SPAN du paragraphe qui contient le texte, et on insère à son
        # début.
        spans = [(m.start(), m.end()) for m in re.finditer(r"<w:p(?:\s[^>]*)?>.*?</w:p>", x, re.S)]
        debut = [a for a, b in spans if a <= j < b]
        if not debut:
            sys.exit("impossible de placer la mutation avant le journal de %s" % src)
        i = debut[0]
    x = x[:i] + para + x[i:]
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as out:
        for it in z.infolist():
            data = x.encode("utf-8") if it.filename == "word/document.xml" else z.read(it.filename)
            out.writestr(it, data)
    bad = zipfile.ZipFile(dst).testzip()
    if bad:
        sys.exit("archive mutée invalide : %s" % bad)
    # Le mutant doit rester un document VALIDE : un refus obtenu sur un XML cassé ne prouve
    # pas que le contrôle mord, il prouve qu'il trébuche. (Ajouté le 09/10/2026, après le
    # bug ci-dessus, qui produisait un <w:p> imbriqué sans que rien ne le dise.)
    xm = zipfile.ZipFile(dst).read("word/document.xml").decode("utf-8")
    try:
        ET.fromstring(xm)
    except Exception as e:
        sys.exit("XML du mutant non conforme : %s" % e)
    ouvre = len(re.findall(r"<w:p(?:\s[^>]*)?>", xm))
    ferme = xm.count("</w:p>")
    if ouvre != ferme:
        sys.exit("mutant déséquilibré : %d <w:p> pour %d </w:p>" % (ouvre, ferme))
    jj = xm.find("Journal des corrections")
    if jj >= 0 and xm.find(txt) > jj:
        sys.exit("la mutation est tombée APRÈS le journal des corrections : elle serait ignorée")
    print("mutation « %s » injectée : %s" % (motif, dst))

main()
