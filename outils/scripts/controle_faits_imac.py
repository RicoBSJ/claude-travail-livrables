#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LES FAITS ACQUIS DE LA SÉRIE iMac SONT-ILS RECOPIÉS JUSTES DANS LE LIVRABLE ? — 22/11/2026.

    outils/scripts/controle_faits_imac.py <document.docx>…

⛔ NON BLOQUANT : il imprime, le lecteur tranche, et il sort toujours en 0. Il juge un CONTENU, et
un balayage rétrospectif ne valide pas un motif bloquant (14/10). Surtout : les DEUX éditions qu'il
signale aujourd'hui sont PUBLIÉES et non corrigées — bloquant, il refuserait tout push qui les
touche.

POURQUOI IL EXISTE. Le 22/11/2026, `non_regression/faits_imac.py` a été écrit pour garder que les
faits mesurés sont VERSÉS AU PROMPT. Il ne peut pas garder qu'ils soient RECOPIÉS : c'est écrit noir
sur blanc dans sa consignation (« il garde que les faits sont présents, placés et appariés dans le
prompt ; il ne garde pas que le job les recopie »). Ce contrôle-ci ferme l'autre moitié, du côté du
livrable, et le balayage du corpus montre que ce n'était pas une précaution :

  · 15/11/2026 : « M6 · 12c CPU/GPU · 16 Go · 512 Go + nano-texturé → 2 219 € »   ✗ FAUX
  · 15/11/2026 : « Prix US au lancement : 1 299 $ » ×2, attribué à 9to5Mac, marqué ✅ HTTP 200  ✗ FAUX
  · 22/11/2026 : « la configuration intermédiaire M6 12c · 16 Go · 512 Go à 2 219 € » ×2   ✗ FAUX

🔴 ET CE QUE LE BALAYAGE A CORRIGÉ DANS MA PROPRE CONSIGNATION DE LA VEILLE : j'avais écrit que ces
deux faits étaient « JUSTES puis défaits dans la même journée ». Mesuré : les DEUX vivaient déjà
FAUX dans l'édition PUBLIÉE du 15/11. Le document de 8h03 du 22/11 ne les a pas défaits, il en a
RECONDUIT un (« 1 299 $ ») et CORRIGÉ l'autre (2 219 € = 256 Go) ; c'est le rattrapage de 14h10 qui
est revenu au 512 Go de N-1 et y a perdu « nano-texturé ». La justesse qui s'est défaite n'a donc
vécu que dans un document JAMAIS PUBLIÉ, et l'origine des deux défauts est le 15/11.
⛔ Et c'est pour cela qu'aucun axe de controle_edition_precedente.py ne pouvait parler : ses trois
axes partent du JOURNAL DES CORRECTIONS de N-1, et le 15/11 n'a jamais été corrigé — il n'y avait
aucune correction à voir se défaire.

📊 LA GRILLE EST MESURÉE AU DEGRÉ ① LE 22/11/2026 sur consomac.fr/comparateur/mac/imac-m6, qui
écrit 34 fois `iMac 24" Retina 4,5K 2026, M6 12 coeurs, 16 Go, SSD 256 Go, 4 ports USB, Argent,
Mat … 2 219,00 €`, et sur MacRumors du 06/11/2026 pour les prix US (`$1,499` / `$1,699` / `$1,449`).

⛔ LE DISCRIMINANT EST « M6 DANS LE LIBELLÉ », ET IL EST MESURÉ NÉCESSAIRE : la grille M4 porte
LÉGITIMEMENT `M4 · 10c CPU/GPU · 16 Go · 512 Go · 4 ports USB → 2 219 €` — c'est la même somme pour
une autre machine, et l'édition du 15/11 l'écrit juste. Un motif qui ne regarderait que le prix
accuserait cette ligne. C'est la borne qui doit être ACCEPTÉE.
⛔ ET LE PRIX DOIT APPARTENIR À LA GRILLE : sans cela, « Mac mini M6 lancé à 1 049 € (16 Go/256 Go) »
serait confronté à une grille d'iMac. 6 lignes du corpus parlent de M6 avec un stockage et un prix
HORS grille (Mac mini, iMac M4 à 1 499,99 €) : elles ne sont pas accusées.
⛔ LE STOCKAGE EST LU DANS LE LIBELLÉ SEUL, LE PRIX DANS LE LIBELLÉ OU LES DEUX RUNS SUIVANTS :
`extract_docx.py` joint chaque `<w:t>` par un saut de ligne, donc une LIGNE de tableau est plusieurs
runs — l'ambiguïté d'aplatissement qui coûte huit faux positifs à controle_decompte.py et son
séparateur à controle_noms_propres.py. Élargir la fenêtre du stockage recollerait deux lignes.
⛔ AUCUNE EXEMPTION NON MESURÉE : un libellé portant DEUX stockages (« 256 Go, 512 Go en option »)
serait accusé, et c'est assumé — il a ZÉRO occurrence sur les 15 lignes de grille du corpus, donc
l'exempter serait une exemption que rien ne mesure, dans la direction d'erreur la plus coûteuse (le
silence). Le jour où le cas existe, il se verra.
⛔ DÉTECTION POSITIVE : un document sans aucune ligne de grille M6 ne produit AUCUNE accusation, et
le dénominateur est IMPRIMÉ — un décompte de défauts sans le décompte de ce qui a été lu ne veut
rien dire (règle de ㉜).

📊 BALAYAGE DES 24 ÉDITIONS DE LA SÉRIE : 15 lignes de grille M6 lues, 3 signalées, 0 faux positif ;
2 prix en dollars examinés, 2 signalés, 0 faux positif. Les 5 signalements sont des défauts RÉELS.
"""
import io
import os
import re
import unicodedata
import subprocess
import sys

EXTRACT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "extract_docx.py")
_DEC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "controle_decompte.py")

# ── MARQUEURS ET JOURNAL : LE CORPS LU PAR CE CONTRÔLE EST CELUI DES AUTRES PASSES ───────────
# Sans cette borne, un marqueur de correction qui CITE le libellé fautif rouvre le motif qu'on
# vient de fermer (leçons des 23 et 25/10, passe A), et les chiffres du journal des corrections
# sont lus comme ceux d'une ligne de grille — mesuré le 22/11/2026 au soir sur les deux éditions
# corrigées le jour même : 4 accusations, toutes portées par mes propres marqueurs et journaux.
# `_hors_marqueur` est EXTRAIT de controle_decompte.py, jamais recopié (règle du 15/10) : une
# seconde implémentation du pliage NFC dériverait en silence, et c'est elle qui fait qu'un « é »
# DÉCOMPOSÉ n'échappe pas au motif.
_SRC = io.open(_DEC, encoding="utf-8").read()
_G = {"re": re, "unicodedata": unicodedata}
exec(_SRC[_SRC.index("R_MARQ_LARGE = re.compile"):_SRC.index("def _nombre_car")]
     + _SRC[_SRC.index("def _hors_marqueur"):_SRC.index('    return " ".join(garde)')
            + len('    return " ".join(garde)')], _G)
hors_marqueur = _G["_hors_marqueur"]
# ⛔ LA SENTINELLE EST LE TITRE, JAMAIS LA PHRASE NUE, et c'est mesuré sur 343 documents : la
# phrase nue y est dans 204 documents, la forme TITRE dans 202, et les DEUX seuls où la phrase nue
# précède sont des notes controle-livrables qui PARLENT du journal d'un autre document sans en
# avoir un — tronquer dessus coupait la note du 08/11 à son run 76 au lieu du 99, et le contrôle
# rendait « 0 ligne lue » sur un document qui en porte trois. C'est le défaut du 04/11/2026 refait
# de ma main, et le cas que CLAUDE.md disait à zéro occurrence : il en a deux.
# ⚠️ controle_attributions.py:98 tronque, lui, sur la PHRASE NUE — ces deux notes y seraient
# coupées de même ; son gate ne couvre ni livrables/controles/ ni ce cas. Mesuré, non corrigé.
SENTINELLE = "📝 Journal des corrections"


def corps_runs(runs):
    """Les runs du CORPS : marqueurs retirés, et rien à partir du journal des corrections."""
    out = []
    for r in runs:
        if SENTINELLE in r:
            break
        out.append(hors_marqueur(r))
    return out

# ── les faits mesurés au degré ① le 22/11/2026, REMESURÉS le 22/11/2026 au soir ───────────────
# prix France (€) → variantes admissibles (SSD en Go, verre). Mesure par extraction des 14
# références Apple du comparateur consomac, une par une : 2 219 € désigne DEUX configurations,
# 16 Go/256 Go à verre nano-texturé (MH2U4FN/A) et 16 Go/512 Go à verre standard (MH154FN/A,
# MH1J4FN/A, MH1Q4FN/A, MH1F4FN/A) — chaque option valant +220 € sur la base de 1 999 €, et
# AUCUNE référence ne les cumulant. Une grille par capacité SEULE accusait donc une ligne juste.
GRILLE_M6 = {"1 799": [("256", "standard")],
             "1 999": [("256", "standard")],
             "2 219": [("256", "nano"), ("512", "standard")],
             "2 439": [("512", "standard")]}
# prix US de lancement (MacRumors 06/11/2026) → ce qu'ils désignent.
PRIX_US = {"1 499": "10 cœurs", "1 699": "12 cœurs", "1 449": "éducation"}

PRIX_EUR = re.compile(r"\b([12] [0-9]{3})\s*(?:,00)?\s*€")
STOCKAGE = re.compile(r"\b(256|512)\s*Go")
# le verre est le SEUL discriminant à 2 219 €, où capacité et nano-texturé sont les deux
# alternatives : « 512 Go + nano-texturé » cumule ce que ce prix n'additionne pas.
NANO = re.compile(r"nano[\s\-]?text", re.I)
# ⛔ LE PRIX DOIT APPARTENIR À LA MÊME LIGNE, et c'est MESURÉ sur 342 documents, pas raisonné :
# une fenêtre de deux runs franchit la frontière de paragraphe. Deux faux positifs relevés le
# 22/11/2026 au soir — une prose de la veille du 18/10 qui emprunte le « 2 219 € » du paragraphe
# SUIVANT, et trois lignes de puces de la note controle-livrables du 08/11 dont chacune porte SON
# prix et se voyait confrontée à celui des deux autres. Règle : si le libellé porte un prix de la
# grille, c'est LE SIEN et on ne regarde pas plus loin ; sinon seule une cellule qui n'est RIEN
# D'AUTRE qu'un prix est acceptée — ce qu'est une cellule de prix de tableau, et ce que n'est ni
# une prose, ni une ligne de puces, ni un marqueur.
PRIX_SEUL = re.compile(r"^\s*([12] [0-9]{3})\s*(?:,00)?\s*€\s*$")
DOLLAR = re.compile(r"(?:\$\s?([0-9],[0-9]{3})|\b([0-9] [0-9]{3})\s*\$)")
LANCEMENT = re.compile(r"lancement|prix US|US au|États-Unis|Etats-Unis", re.I)
# ⛔ ET LE RUN DOIT AUSSI NOMMER LA MACHINE, mesuré sur 343 documents : « lancement » seul
# faisait lire « données de lancement … <1 000 $/mois » d'une leçon revenus-passifs comme un
# prix US de lancement d'iMac — troisième faux positif du 22/11/2026 au soir. Des DEUX
# resserrements possibles, le corpus rend des verdicts IDENTIQUES (4 runs appariés, 1 retiré
# par chacun) : ce n'est donc PAS la mesure qui tranche, et il faut le dire. La conjonction
# est retenue plutôt que le retrait de « lancement » parce qu'elle garde ce mot comme
# déclencheur — « Au lancement, l'iMac M6 était à 1 299 $ » resterait attrapé, ce que le
# retrait perdrait — et parce qu'elle emploie le MÊME ancrage que la moitié « grille », où il
# est mesuré nécessaire. Une borne FABRIQUÉE l'épingle, le corpus n'en portant aucun cas.
MACHINE = re.compile(r"iMac|M6|Mac")


def runs_de(docx):
    """Le texte par le VRAI extracteur du dépôt, jamais une relecture du zip à la main."""
    r = subprocess.run(["/usr/bin/python3", EXTRACT, docx], capture_output=True, text=True)
    return r.stdout.split("\n")


def signale(runs):
    """Rend (signalements, lignes de grille lues, prix en dollars lus)."""
    out, lignes, dollars = [], 0, 0
    for i, r in enumerate(runs):
        if "M6" not in r:
            continue
        stos = sorted(set(STOCKAGE.findall(r)))          # le stockage est dans le LIBELLÉ
        propres = sorted(set(PRIX_EUR.findall(r)) & set(GRILLE_M6))
        if propres:
            prix = propres                              # la ligne porte SON prix : on s'arrête là
        else:                                           # sinon : une CELLULE qui n'est qu'un prix
            prix = []
            for suiv in runs[i + 1:i + 3]:
                m = PRIX_SEUL.match(suiv)
                if m and m.group(1) in GRILLE_M6:
                    prix = [m.group(1)]
                    break
        if not (stos and prix):
            continue
        lignes += 1
        verre = "nano" if NANO.search(r) else "standard"
        for p in prix:
            for s in stos:
                if (s, verre) not in GRILLE_M6[p]:
                    adm = " ou ".join("%s Go/%s" % v for v in GRILLE_M6[p])
                    out.append("%s € donné pour %s Go en verre %s — la grille M6 mesurée dit %s : « %s »"
                               % (p, s, verre, adm, r.strip()[:90]))
    for r in runs:
        if not (LANCEMENT.search(r) and MACHINE.search(r)):
            continue
        for m in DOLLAR.finditer(r):
            v = (m.group(1) or m.group(2) or "").replace(",", " ")
            if not v:
                continue
            dollars += 1
            if v not in PRIX_US:
                out.append("%s $ donné pour un prix US de lancement — les trois mesurés sont "
                           "1 499 (10 cœurs), 1 699 (12 cœurs) et 1 449 (éducation) : « %s »"
                           % (v, r.strip()[:90]))
    return out, lignes, dollars


def verdict(docs):
    tot = li = do = 0
    for d in docs:
        out, lignes, dollars = signale(corps_runs(runs_de(d)))
        li += lignes
        do += dollars
        tot += len(out)
        for x in out:
            print("  FAIT ACQUIS CONTREDIT — %s : %s" % (os.path.basename(d), x))
    print("  FAITS ACQUIS DANS LE LIVRABLE : %d ligne(s) de grille M6 lue(s) · %d prix en dollars "
          "lu(s) · %d contradiction(s)" % (li, do, tot))
    if not li and not do:
        print("  ⓘ aucune ligne de grille M6 ni prix US dans ce ou ces document(s) : motif inerte, "
              "et il le dit")
    return 0          # NON BLOQUANT, toujours : voir l'en-tête


if __name__ == "__main__":
    sys.exit(verdict(sys.argv[1:]))
