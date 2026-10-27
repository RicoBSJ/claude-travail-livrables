#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""etiquette_has.py — le motif (1) de psychopathologie reste-t-il borné aux pages de RBPP ?

POURQUOI (26/10/2026). Le portage du faisceau, le matin même, a rendu ACTIF un motif qui était
inerte depuis le 18/10 : `if pdfs and not any(…)` ne peut rien dire d'une page vide. Devenu
actif, il a mordu sur `p_3590541/la-has-adopte-son-nouveau-programme-sante-mentale-et-
psychiatrie-2025-2030`, qui est un COMMUNIQUÉ DE PRESSE — il exigeait des ressources de la
leçon l'annexe thématique d'une page d'actualité. La lettre de la règle B3 bis était
respectée ; son esprit visait la page de présentation d'une RECOMMANDATION.

LE DISCRIMINANT EST STRUCTUREL, ET IL EST MESURÉ sur les 17 pages jcms du corpus
psychopathologie : chaque page HAS déclare son type dans UNE seule étiquette, celle de sa zone
`sub-title` — `Recommandation de bonne pratique` (9 pages, 1 à 21 PDF chacune),
`Communiqué de presse` (1), `Flash sécurité patient` (1), `Article HAS` (2), et aucune
étiquette pour les 4 portails thématiques. Exactement une occurrence de `titleLabelCaps` par
page, zéro pour les portails.

⚠️ CE QUE CE TÉMOIN EMPÊCHE SURTOUT, C'EST DE REVENIR À UN TEST NAÏF. Un simple
`"Recommandation de bonne pratique" in page` donnerait le MÊME verdict sur les cas simples et
se tromperait sur les pages qui portent cette chaîne dans leur colonne « Voir aussi » sans en
être une (mesuré : 2 occurrences sur p_3953998 et sur p_3741239). La borne ⑤ est précisément
ce cas, et c'est la seule qui sépare les deux implémentations.

⚠️ IL N'EST PAS UNE COPIE DE LA LOGIQUE : la regex et la constante sont EXTRAITES de
`controle_psychopathologie.py` puis exécutées. Si l'une disparaît du contrôle, la borne ⑥
le dit — sans elle, ce témoin resterait vert sur du vide.

⚠️ RISQUE RÉSIDUEL, ET IL EST DIT : si le gabarit de la HAS renommait sa classe CSS, TOUTES
les pages deviendraient exemptes et le motif redeviendrait inerte — le défaut même corrigé le
26/10 au matin. Aucun témoin figé ne peut voir le changement d'un gabarit tiers. Ce qui le
rend visible est la ligne « PAGE HAS NON-RBPP, MOTIF (1) NON APPLIQUÉ » que le contrôle
imprime à chaque exemption : une inertie silencieuse devient une exemption énoncée.

🆕 27/10/2026 — IL GARDE AUSSI LE DÉCOMPTE DES EXEMPTIONS ET SON ALERTE (bornes ⑪ à ⑮).
L'angle mort est symétrique de celui que le bornage ferme : un renommage du gabarit HAS
rendrait TOUTES les pages exemptes et le motif inerte. ⛔ Mais « 100 % d'exemptions » seul est
un état LÉGITIME — mesuré, la leçon 17 ne cite qu'une page à PDF, un Flash sécurité patient,
donc 1 sur 1. C'est la borne ⑬, et elle doit être ACCEPTÉE : sans elle, rien n'empêche de
faire crier l'alerte sur un document conforme.

Aucun réseau. Usage : python3 outils/scripts/non_regression/etiquette_has.py
Sortie : 0 si toutes les bornes tiennent, 1 sinon.
"""
import os, re, sys

# ⚠️ QUATRE dirname — ce script vit dans outils/scripts/non_regression/, un cran plus bas que
#    les contrôles. Le piège du 23/10, et la borne ⑦ vérifie que RACINE est rendue.
RACINE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
CTL = os.path.join(RACINE, "outils", "scripts", "controle_psychopathologie.py")

SOUS = '<div class="sub-title"> <span class="titleLabelCaps">%s</span> - Mis en ligne le 08 nov. 2017'
# Témoins FIGÉS, réduits à ce que le motif regarde. Chacun porte un PDF has-sante.fr, sans quoi
# le motif ne s'exercerait pas du tout.
PDF = '<a href="https://www.has-sante.fr/upload/docs/application/pdf/2017-10/doc.pdf">doc</a>'
CAS = [
 ("① une page de RBPP : le motif MORD (il ne doit pas être resserré à rien)",
  SOUS % "Recommandation de bonne pratique" + PDF, True),
 ("② un COMMUNIQUÉ DE PRESSE est exempté (p_3590541, l'incident du 26/10)",
  SOUS % "Communiqué de presse" + PDF, False),
 ("③ un FLASH SÉCURITÉ PATIENT est exempté (p_3381939)",
  SOUS % "Flash sécurité patient" + PDF, False),
 ("④ un portail sans étiquette est exempté (4 pages du corpus)",
  '<div class="title"><h1>Dépression</h1></div>' + PDF, False),
 ("⑤ la chaîne dans le CORPS seule ne suffit pas — garde contre `RBPP in page`"
  " (mesuré : 3 portails du corpus mordraient avec ce test)",
  SOUS % "Article HAS" + PDF
  + '<aside class="voir-aussi"><span class="titleLabelCaps">Recommandation de bonne pratique'
    '</span> 21/07/2025 Repérage et prise en charge</aside>', False),
 ("⑥ le gabarit réel, avec ses blancs entre les balises, est bien lu",
  '<div class="sub-title">\n   <span class="titleLabelCaps">Recommandation de bonne pratique'
  '</span> - Mis en ligne le 21 avr. 2026' + PDF, True),
 # ⑩ ⚠️ TÉMOIN FABRIQUÉ, ET IL FAUT LE DIRE : aucune page du corpus n'a cette forme — la
 #    colonne « Voir aussi » de la HAS vient TOUJOURS après la zone sub-title. C'est pourquoi
 #    l'ancrage à `<div class="sub-title">` est un durcissement PRÉVENTIF : mesuré sur les
 #    17 pages, « première étiquette où qu'elle soit » donne 0 verdict différent. Ma première
 #    version de la borne ⑤ prétendait garder ce cas et ne le gardait PAS : un sabotage qui
 #    retirait l'ancrage laissait le lot vert. C'est cette borne-là, et elle seule, qui mord.
 ("⑩ une étiquette de barre latérale AVANT la zone sub-title ne détourne pas le verdict"
  " (témoin FABRIQUÉ : forme absente du corpus, durcissement préventif)",
  '<aside><span class="titleLabelCaps">Recommandation de bonne pratique</span> 21/07/2025</aside>'
  + SOUS % "Communiqué de presse" + PDF, False),
]


def extrait():
    """La regex ET la constante, prises DANS le contrôle. (None, None) si absentes."""
    s = open(CTL, encoding="utf-8").read()
    a = re.search(r"^ETIQ_HAS = re\.compile\(.*\)$", s, re.M)
    b = re.search(r'^RBPP_HAS = ".*"$', s, re.M)
    return (a.group(0) if a else None), (b.group(0) if b else None)


def extrait_bilan():
    """Le CORPS de bilan_etiquettes(), pris DANS le contrôle. None si absent.

    ⚠️ Pas une copie : la fonction est extraite puis exécutée. La borne ⑮ vérifie en plus que
    le contrôle l'APPELLE et imprime ses lignes — une fonction juste mais jamais appelée
    laisserait le lot vert, et le décompte n'apparaîtrait dans aucun log.
    """
    s = open(CTL, encoding="utf-8").read()
    m = re.search(r"^def bilan_etiquettes\(.*?\n    return L$", s, re.S | re.M)
    return m.group(0) if m else None


def controler():
    ko, jouees = [], []

    def borne(nom, ok, detail=""):
        print("  %s %s%s" % ("✓" if ok else "✗", nom, (" — " + detail) if detail else ""))
        jouees.append(nom)
        if not ok:
            ko.append(nom)

    def fin():
        print("  %d/%d bornes de l'étiquette HAS" % (len(jouees) - len(ko), len(jouees)))
        return 1 if ko else 0

    borne("⑦ RACINE est rendue — le contrôle est là où ce script le cherche",
          os.path.isfile(CTL), CTL)
    if not os.path.isfile(CTL):
        return fin()

    ligne_re, ligne_cst = extrait()
    borne("⑧ la regex et la constante sont bien DANS le contrôle (sinon ce témoin est vide)",
          bool(ligne_re) and bool(ligne_cst),
          "regex %s · constante %s" % ("OK" if ligne_re else "ABSENTE",
                                        "OK" if ligne_cst else "ABSENTE"))
    if not (ligne_re and ligne_cst):
        return fin()

    # ⑨ SANS CETTE BORNE, UN SABOTAGE POURRAIT RENDRE L'EXEMPTION SILENCIEUSE et le reste du
    #    lot resterait vert — or une inertie muette est exactement le défaut fermé le 26/10 au
    #    matin. Le contrôle doit DIRE qu'il n'a pas appliqué le motif, et nommer le type lu.
    src = open(CTL, encoding="utf-8").read()
    borne("⑨ l'exemption est IMPRIMÉE, pas silencieuse (une inertie muette est le défaut du matin)",
          "PAGE HAS NON-RBPP, MOTIF (1) NON APPLIQUÉ" in src
          and "type déclaré par la page" in src)

    g = {"re": re}
    exec(ligne_re + "\n" + ligne_cst, g)          # le VRAI code du contrôle, pas une copie
    etiq, rbpp = g["ETIQ_HAS"], g["RBPP_HAS"]

    for nom, page, doit_mordre in CAS:
        m = etiq.search(page)
        lu = m.group(1).strip() if m else ""
        borne(nom, (lu == rbpp) == doit_mordre,
              "étiquette lue : %s" % (("« %s »" % lu) if lu else "⟨aucune⟩"))

    # ── le décompte des exemptions et son alerte (27/10/2026) ───────────────────────────
    corps = extrait_bilan()
    borne("⑪ bilan_etiquettes() est bien DANS le contrôle (sinon les bornes qui suivent sont vides)",
          bool(corps), "extrait" if corps else "ABSENTE")
    if not corps:
        return fin()
    gb = {}
    exec(corps, gb)                               # le VRAI code du contrôle, pas une copie
    bilan = gb["bilan_etiquettes"]

    r = bilan(0, 0, 0)
    borne("⑫ aucune page jcms à PDF -> AUCUNE ligne (12 des 20 leçons sont dans ce cas)",
          r == [], repr(r))

    r = bilan(11, 2, 11)
    ok = (len(r) == 1 and "11 page(s) jcms à PDF" in r[0] and "2 exemptée(s)" in r[0]
          and "11 étiquette(s) lue(s)" in r[0])
    borne("⑬ le cas nominal du corpus (11 pages, 2 exemptées, 11 étiquettes) : décompte, zéro alerte",
          ok, r[0] if r else "⟨rien⟩")

    r = bilan(1, 1, 1)
    ok = (len(r) == 2 and "aucune alerte" in r[1] and "ALERTE ÉTIQUETTE HAS" not in r[1])
    borne("⑭ 100 % D'EXEMPTIONS MAIS L'ÉTIQUETTE EST LUE -> PAS d'alerte"
          " (cas RÉEL de la leçon 17 : ce témoin doit être ACCEPTÉ)",
          ok and "🔴" not in " ".join(r), " / ".join(x.strip()[:70] for x in r))

    r = bilan(3, 3, 0)
    borne("⑮ 100 % d'exemptions ET aucune étiquette lue -> ALERTE, et elle dit INERTE"
          " (le renommage du gabarit HAS)",
          len(r) == 2 and "ALERTE ÉTIQUETTE HAS" in r[1] and "INERTE" in r[1],
          r[1].strip()[:90] if len(r) == 2 else repr(r))

    # ⚠️ QUATRE exigences en une borne : elle NOMME celle qui manque, sinon deux sabotages
    #    différents (l'appel retiré, le compteur mort) rendraient le même message.
    attelage = [("l'appel", "for _L in bilan_etiquettes(_n_pdf, _n_exempt, _n_etiq):"),
                ("l'impression", "print(_L)"),
                ("le compteur d'exemptions", "_n_exempt += 1"),
                ("le compteur d'étiquettes", "_n_etiq += 1")]
    absents = [nom for nom, frag in attelage if frag not in src]
    borne("⑯ le contrôle APPELLE le bilan et imprime ses lignes, et il compte l'exemption"
          " (une fonction jamais appelée n'écrit dans aucun log)",
          not absents, "manque : " + ", ".join(absents) if absents else "les quatre y sont")
    # ⑰ UNE ALERTE QUE RIEN NE REMONTE EST DÉCORATIVE. Le bloc des 5 bis du harnais capture la
    #    sortie des contrôles dans un fichier et n'imprime qu'un ✓/✗, et le job psychopathologie
    #    est supprimé depuis le 15/10 : sans cette remontée, l'alerte s'écrirait dans un fichier
    #    que personne n'ouvre. C'est le seul endroit du dépôt où ce contrôle tourne encore sur
    #    un document réel, donc le seul où l'alerte peut être vue.
    nr = os.path.join(RACINE, "outils", "scripts", "non_regression.sh")
    try:
        hs = open(nr, encoding="utf-8").read()
    except OSError:
        hs = ""
    borne("⑰ le harnais REMONTE l'alerte du bloc 5 bis (sinon elle s'écrit dans un fichier"
          " que personne n'ouvre)",
          "ALERTE ÉTIQUETTE HAS" in hs and '5bis_$MOTIF.txt' in hs,
          "non_regression.sh lu : %d caractères" % len(hs))
    return fin()


if __name__ == "__main__":
    raise SystemExit(controler())
