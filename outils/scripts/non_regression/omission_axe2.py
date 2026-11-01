# -*- coding: utf-8 -*-
"""L'axe ② de `controle_edition_precedente.py` était TOTALEMENT INERTE dès que N-1 portait un
marqueur. Mesuré le 01/11/2026 : cela le rendait muet sur **27 des 300 documents** du dépôt, et le
fondeur « TSMC » a traversé ainsi le maillon 18/10 → 25/10 de la série imac — présent le 04/10
(corrigé), rejoué le 11/10, absent du 18/10 après une correction qui ne l'a pas cité, rejoué le
25/10, pour un verdict « aucune correction rejouée ».

⚠️ CE QUE LE CORRECTIF FERME, ET CE QU'IL NE FERME PAS — à ne pas confondre.
  · FERMÉ : une formulation que la fiche de N-1 donne pour fautive, que N-1 n'a PAS corrigée, sur
    une édition corrigée AILLEURS. ① ne la suit pas (rien ne la cite dans le journal) et ② se
    taisait. C'est la classe des 9 signalements neufs, dont le conteneur du défaut TSMC et le
    rejeu du tarif Mac mini.
  · PAS FERMÉ : une formulation ENTIÈREMENT retirée de N-1 — la vraie correction par omission.
    Le filtre `ecartees` l'exclut par construction, et c'est voulu : sur un N-1 non corrigé, c'est
    ce filtre qui empêche d'accuser une version corrigée. La borne ③ ci-dessous l'épingle, et elle
    doit être ACCEPTÉE — sans elle, rien n'empêche de croire le trou refermé.

Aucun réseau, aucun document du dépôt dans le verdict : les éditions, leur fiche et leur journal
sont FABRIQUÉS en tempfile (leçon du 22/10/2026 — un témoin vivant périme tout seul et bloque
alors TOUS les pushs du dépôt).
"""
import os, re, sys, zipfile, tempfile, subprocess, shutil

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
assert os.path.isfile(os.path.join(RACINE, "controle_edition_precedente.py")), \
    "RACINE mal calculée : ce script vit un cran SOUS outils/scripts (bug du 23/10/2026)"
CTRL = os.path.join(RACINE, "controle_edition_precedente.py")

def docx(chemin, paras):
    xml = ('<?xml version="1.0" encoding="UTF-8"?><w:document xmlns:w="http://schemas.openxml'
           'formats.org/wordprocessingml/2006/main"><w:body>')
    for p in paras:
        xml += '<w:p><w:r><w:t xml:space="preserve">%s</w:t></w:r></w:p>' % (
            p.replace('&', '&amp;').replace('<', '&lt;'))
    xml += '<w:sectPr/></w:body></w:document>'
    with zipfile.ZipFile(chemin, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('word/document.xml', xml)

MARQ = ("[Corrigé le 08/01/2026 : la version initiale écrivait "
        "« gravée en 2 nm chez Fonderie Bidule », absente des pages.]")

def arbre(d, avec_marqueur=True):
    """N-1 (8 janvier) et N (15 janvier) + la fiche de N-1. Tout est inventé."""
    p3 = "La puce Qwerty est gravée en 2 nm chez Fonderie Bidule."
    prec = [
        "Veille témoin du 8 janvier 2026",
        "Le tarif Zorglub est de 1 049 € depuis le 22 septembre 2026.",
        (p3 + " " + MARQ) if avec_marqueur else p3,
        # ce ¶ n'est PAS marqué et porte le MÊME libellé que le journal cite : il rend la
        # formulation signalable, donc le bornage par ① est le seul à l'en empêcher. Sans ce ¶,
        # retirer le bornage ne changeait rien au témoin — borne qui ne peut pas échouer (26/10).
        "Rappel du cadrage : gravée en 2 nm chez Fonderie Bidule, non relu sur page.",
        "📝 Journal des corrections — 8 janvier 2026",
        "① Fiche technique — « gravée en 2 nm chez Fonderie Bidule » : absente des pages citées.",
    ]
    cour = [
        "Veille témoin du 15 janvier 2026",
        "Le tarif Zorglub est de 1 049 € depuis le 22 septembre 2026, inchangé cette semaine.",
        "La puce Qwerty est gravée en 2 nm chez Fonderie Bidule.",
        "une formulation entièrement retirée de cette édition par omission",
    ]
    docx(os.path.join(d, "2026-01-08_veille_temoin.docx"), prec)
    docx(os.path.join(d, "2026-01-15_veille_temoin.docx"), cour)
    fiche = """# fiche témoin

- Le tarif est **faux** : « Le tarif Zorglub est de 1 049 € depuis le 22 septembre 2026 » ne figure
  sur aucune page, et il est repris du cadrage du job.
- Doublon volontaire, même suite de six mots : « Le tarif Zorglub est de 1 049 € depuis le 22
  septembre 2026 selon le marchand » est également faux.
- Le fondeur est inexact : « gravée en 2 nm chez Fonderie Bidule » est absente des pages.
- Retirée en silence : « une formulation entièrement retirée de cette édition par omission » est
  fausse elle aussi.
"""
    open(os.path.join(d, "2026-01-08_veille_temoin.fiche.md"), "w", encoding="utf-8").write(fiche)
    return os.path.join(d, "2026-01-15_veille_temoin.docx")

def axe2(sortie):
    bloc = re.search(r"^② .*?(?=^③ )", sortie, re.S | re.M)
    return bloc.group(0) if bloc else ""

def lance(cible):
    r = subprocess.run([sys.executable, CTRL, cible], capture_output=True, text=True,
                       env={"PATH": "/usr/bin:/bin", "LC_ALL": "fr_FR.UTF-8"})
    return r.stdout + r.stderr

def autotest():
    ko, jouees = [], []
    def borne(nom, cond, detail=""):
        jouees.append(nom)
        if not cond:
            ko.append(nom); print("  ✗ %s %s" % (nom, detail))

    d = tempfile.mkdtemp(prefix="omission_axe2_")
    try:
        # ── N-1 CORRIGÉE : le motif doit PARLER, et dire ce qu'il ne dit pas
        cible = arbre(d, avec_marqueur=True)
        b = axe2(lance(cible))
        borne("① la formulation non citée au journal est SIGNALÉE",
              "A RELIRE" in b and "Zorglub" in b, "— bloc : %r" % b[:220])
        borne("② le fondeur, CITÉ au journal, est couvert par ① (doit être ACCEPTÉE)",
              re.search(r"1 couverte\(s\) par ①", b) is not None
              and "Fonderie" not in b.split("A RELIRE")[-1],
              "— bloc : %r" % b[:220])
        # ⚠️ `ecartees` compte les SUITES rejetées, pas les citations : ma première version de
        #    cette borne exigeait « 1 écartée(s) » et accusait un contrôle juste (01/11/2026).
        borne("③ la formulation ABSENTE de N-1 reste ÉCARTÉE (doit être ACCEPTÉE)",
              re.search(r"[1-9]\d* écartée\(s\)", b) is not None and "par omission" not in b,
              "— bloc : %r" % b[:220])
        borne("④ le mot INERTE a disparu pour un N-1 corrigé",
              "INERTE" not in b, "— bloc : %r" % b[:220])
        borne("⑤ la ligne de décompte nomme les marqueurs de N-1",
              re.search(r"N-1 est CORRIGÉE \(\d+ marqueur\(s\)\)", b) is not None,
              "— bloc : %r" % b[:220])
        borne("⑥ déduplication : deux citations, une seule suite, UN signalement",
              b.count("A RELIRE") == 1, "— %d signalement(s)" % b.count("A RELIRE"))

        # ── N-1 NON corrigée : comportement d'origine, et c'est `n_marq_p` qui commande
        shutil.rmtree(d); d = tempfile.mkdtemp(prefix="omission_axe2_")
        cible = arbre(d, avec_marqueur=False)
        b2 = axe2(lance(cible))
        borne("⑦ sans marqueur dans N-1, aucune couverture par ① n'est annoncée",
              "couverte(s) par ①" not in b2, "— bloc : %r" % b2[:220])
        borne("⑧ sans marqueur, le fondeur redevient signalable",
              b2.count("A RELIRE") >= 1 and "Fonderie" in b2, "— bloc : %r" % b2[:220])

        # ── fiche absente : comportement d'origine intact
        os.remove(os.path.join(d, "2026-01-08_veille_temoin.fiche.md"))
        b3 = axe2(lance(cible))
        borne("⑨ fiche absente : motif INERTE, et ce n'est PAS une réussite",
              "fiche absente" in b3 and "INERTE" in b3, "— bloc : %r" % b3[:220])

        # ── le trou ne peut pas être rétabli en silence
        src = open(CTRL, encoding="utf-8").read()
        borne("⑩ la branche totalement inerte n'est pas rétablie",
              "motif ② hors sujet" not in src)
        borne("⑪ la rectification de la prémisse du 12/10 est écrite dans le contrôle",
              "ÉTAIT FAUSSE" in src and "SANS MARQUEUR" in src)
        borne("⑫ le bornage lit l'ensemble que ① suit, il ne le recopie pas",
              "jetons(c) & cands" in src)
    finally:
        shutil.rmtree(d, ignore_errors=True)

    # une EXIGENCE DE LIGNE pour le harnais : le motif est NON BLOQUANT, donc un code de
    # sortie seul ne prouve pas qu'il a dit quelque chose (règle du dépôt).
    if not ko:
        print("  ② sur N-1 CORRIGÉE : 1 signalement · 1 couverte par ① · absente de N-1 NON signalée")
    print("  %d/%d bornes de l'omission à l'axe ②" % (len(jouees) - len(ko), len(jouees)))
    return 1 if ko else 0

if __name__ == "__main__":
    sys.exit(autotest())
