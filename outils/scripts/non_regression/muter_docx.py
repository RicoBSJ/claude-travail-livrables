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
  nompropre — ⚠️ MOTIF D'UN AUTRE GENRE : il ne JOINT pas un paragraphe, il MODIFIE le premier
              paragraphe qui porte à la fois un lien et un marqueur de source, en y glissant un
              nom propre inventé (ajouté le 09/10/2026, en portant le correctif du motif ⑤ de
              controle_astrologie_karmique.py)
              → doit déclencher le motif ⑤ de controle_astrologie_karmique.py.
                Un paragraphe AJOUTÉ en fin de document n'aurait pas suffi : ⑤ ne regarde que les
                paragraphes qui portent un lien (« if not LIENS[i]: continue ») et dont la page
                répond 200 avec au moins 500 caractères. Une mutation doit tomber LÀ OÙ LE MOTIF
                REGARDE, sinon elle ne prouve rien.
  citation  — injecte « Le rapport cite « zorblax quantique indéterminé » sans page. »
              (ajouté le 10/10/2026, en portant norm4 dans controle_ai_act.py)
              → doit déclencher le motif (1) de controle_ai_act.py : une citation courte
                qui n'est sur aucune page de la note. C'est LUI qui garde le motif après
                l'élargissement du normaliseur : « alerte » n'exerce que le motif (6),
                qui ne compare aucune citation.
  typo      — ⚠️ MUTATION ATTENDUE EN EXIT 0, la seule du lot. Injecte
              « La CNIL titre « Quels sont mes droits? » sur sa page de questions-réponses. »
              (ajouté le 10/10/2026). La page cnil.fr que la note du 09/10 liste écrit
              « Quels sont mes droits ? » avec une espace fine AVANT le point
              d'interrogation — typographie française. Avant le portage de norm4, la note
              qui la citait sans cette espace était refusée DEUX FOIS : motif (1)
              « citation courte absente des pages » et motif ⑦ « ponctuation inventée ».
              → le contrôle doit l'ACCEPTER. C'est le sens « il ne mord pas à tort » du
                normaliseur, et sans lui l'élargissement n'est prouvé dans aucun sens.
  alerte    — injecte un paragraphe « 🟢 Niveau d'alerte : VERT … » dans une note qui
              annonce des faits marquants (ajouté le 09/10/2026, en sortant
              controle_ai_act.py de son prompt)
              → doit déclencher le motif (6) de controle_ai_act.py. Ce motif ne coûte
                AUCUN appel réseau : la mutation se juge sur le document seul, même si
                le reste du script, lui, rouvre les pages de la note.
"""
import re, sys, zipfile, html
import xml.etree.ElementTree as ET

TEXTES = {
    "ligature": "Le Noeud Nord est ici cité sans sa ligature, hors de toute adresse web.",
    "fraction": "Selon la HAS, un tiers des personnes concernées ne sont pas informées de leurs droits.",
    "alerte": "\U0001F7E2  Niveau d'alerte : VERT — paragraphe de mutation, injecté par le harnais.",
    # « zorblax quantique indéterminé » : trois mots, donc dans la fenêtre 2–5 du motif (1) ;
    # sur aucune page du web ; et la citation ne se termine PAS par une ponctuation forte, pour
    # que seul le motif (1) soit en cause et non ⑦. « Le rapport cite » n'est aucun des mots
    # (édition|note|cadrage|prompt|consigne|rubrique|section) qui exemptent une citation.
    "citation": "Le rapport cite « zorblax quantique indéterminé » sans page.",
    # ⚠️ ATTENDUE EN EXIT 0 : la page cnil.fr listée par la note du 09/10 écrit
    # « Quels sont mes droits ? » avec une espace avant le point d'interrogation.
    "typo": "La CNIL titre « Quels sont mes droits? » sur sa page de questions-réponses.",
}
# Mutations qui s'insèrent DANS un paragraphe existant, et non en fin de document.
DEDANS = {
    # « Zorblax » n'est sur aucune page du web consultée par le contrôle, n'est pas un mot de la prose
    # française de la leçon, n'est dans aucun domaine cité, et ne ressemble à aucun exonyme : il ne peut
    # être exempté par aucune des gardes du motif ⑤. Le marqueur « Selon » est là pour que la phrase
    # attribue, puisque c'est la condition d'examen du motif.
    "nompropre": " Selon Zorblax, ce relevé est confirmé.",
}

def main():
    if len(sys.argv) != 4:
        sys.exit("usage : muter_docx.py <source.docx> <destination.docx> <%s>" % "|".join(TEXTES))
    src, dst, motif = sys.argv[1:4]
    if motif not in TEXTES and motif not in DEDANS:
        sys.exit("motif inconnu : %s (connus : %s)" % (motif, ", ".join(list(TEXTES) + list(DEDANS))))
    z = zipfile.ZipFile(src)
    x = z.read("word/document.xml").decode("utf-8")
    if motif in DEDANS:
        # On cherche le premier paragraphe qui porte un lien ET un marqueur de source : c'est la seule
        # zone que le motif ⑤ examine. On y ajoute un run APRÈS le dernier, donc hors de l'hyperlien —
        # le motif lit le texte « hors lien » du paragraphe.
        rels_ = dict(re.findall(r'Id="([^"]+)"[^>]*Target="(https?://[^"]+)"',
                                z.read("word/_rels/document.xml.rels").decode("utf-8")))
        SRC_ = r"(?i)\bsource\s*:|\bétabli\b|page citée|\bd['’]après\b|\bselon\b"
        spans = [(m.start(), m.end()) for m in re.finditer(r"<w:p(?:\s[^>]*)?>.*?</w:p>", x, re.S)]
        jj = x.find("Journal des corrections")
        cible = None
        for a_, b_ in spans:
            if 0 <= jj < a_: break
            q_ = x[a_:b_]
            if not [r for r in re.findall(r'r:id="([^"]+)"', q_) if r in rels_]: continue
            txt_ = html.unescape("".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", q_)))
            if re.search(SRC_, txt_): cible = (a_, b_); break
        if cible is None:
            sys.exit("aucun paragraphe à la fois lié et porteur d'un marqueur de source dans %s" % src)
        a_, b_ = cible
        txt = (DEDANS[motif].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                            .replace("'", "&apos;"))
        run = ('<w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:cs="Times New Roman" '
               'w:hAnsi="Times New Roman"/><w:sz w:val="22"/></w:rPr><w:t xml:space="preserve">'
               + txt + '</w:t></w:r>')
        q_ = x[a_:b_]
        k_ = q_.rfind("</w:p>")
        x = x[:a_] + q_[:k_] + run + "</w:p>" + x[b_:]
        with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as out:
            for it in z.infolist():
                data = x.encode("utf-8") if it.filename == "word/document.xml" else z.read(it.filename)
                out.writestr(it, data)
        xm = zipfile.ZipFile(dst).read("word/document.xml").decode("utf-8")
        ET.fromstring(xm)
        if len(re.findall(r"<w:p(?:\s[^>]*)?>", xm)) != xm.count("</w:p>"):
            sys.exit("mutant déséquilibré")
        print("mutation « %s » insérée dans un paragraphe sourcé : %s" % (motif, dst))
        return
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
