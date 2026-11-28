#!/usr/bin/env python3
"""Convention des fiches .md — la forme d'un amendement est-elle tenue ? (28/11/2026)

Une fiche publiée qu'on amende doit garder VISIBLE l'affirmation d'origine : git
tient l'histoire, mais ce que le propriétaire lit dans Obsidian est le fichier.
Le corpus avait déjà une convention, mesurée sur ses 329 fiches et ses 5 ratures,
et elle n'est PAS celle du .docx — ni marqueur entre crochets, ni journal final.

Deux motifs, les deux NON BLOQUANTS (ils jugent un contenu — règle du 14/10) :

  ① RATURE SANS MARQUE DATÉE — une rature `~~…~~` doit être suivie d'une marque
     en gras qui porte une date. Bornes mesurées sur les 5 ratures du corpus :
     le gras ouvre à **+3 caractères dans 5 cas sur 5** (` → ` ou ` — `), d'où la
     fenêtre de 6 ; et la date doit vivre DANS le gras, parce que la seule rature
     du corpus dont la date est au-delà (`**suivi**` puis « au 04/09/2026 » à
     +65) est justement celle qui n'est PAS datée — un test « une date dans les
     80 caractères qui suivent » l'aurait acceptée à tort.

  ② JOURNAL DANS UNE FICHE — une fiche ne porte pas de section « Journal des
     corrections ». ⚠️ PRÉVENTIF, et c'est dit : 0 occurrence sur les 329 fiches.
     Un .docx de 27 000 caractères a besoin d'un journal, une fiche de 120 lignes
     se lit en entier, donc la correction doit vivre OÙ elle corrige. ⛔ On
     apparie un TITRE (`#…`), jamais la phrase nue : `Journal des corrections`
     est cité par 24 fiches qui RAPPORTENT le journal de leur .docx, et
     `[Corrigé le …]` par 13 qui citent le marqueur du .docx — un recensement
     textuel n'est pas un recensement d'usages (27/10).

⛔ CE QUE CE CONTRÔLE NE FAIT PAS, ET POURQUOI : il ne dit pas qu'un amendement
   AURAIT DÛ être marqué. Mesuré : 50 révisions de fiche suppriment de la prose,
   dont 31 à J+0 ou J+1 (la fiche est encore en train d'être écrite — bande vide
   mesurée à J+2 : 22 révisions à J+0, 9 à J+1, ZÉRO à J+2, la suivante à J+3) ;
   des 19 restantes, les non marquées relèvent de quatre formes légitimes — le
   compte cumulatif d'un `_dossier`, une référence prospective résolue en
   wikilien, un suffixe ajouté à la même ligne, et le passage du verbe à
   l'imparfait (03/11 : l'imparfait est le temps de la conservation). Séparer ces
   quatre formes demanderait quatre exemptions calibrées sur 19 cas, dont deux
   que la mesure ne sépare pas : ce serait un motif qui crie (règle du 21/11).

Usage : controle_convention_fiches.py <fiche.md>…   |   --corpus   |   --autotest
Sortie : 0 toujours sur les motifs (non bloquants) ; 1 seulement si l'auto-test
         échoue ou si un fichier n'est pas lisible.
"""
import re, sys, pathlib

# ⚠️ TROIS parent : ce script vit dans outils/scripts/. Deux seulement rendaient
# un corpus VIDE et un vert sur rien — le bug de RACINE du dépôt, cinquième
# occurrence (23/10, 27/10, 11/11 deux fois). La borne ⑰ l'a dit, pas la relecture.
RACINE = pathlib.Path(__file__).resolve().parent.parent.parent

# ── prédicat STRUCTUREL : le frontmatter, jamais une liste de chemins ni
# ── d'extensions (règle du 11/11). 329 fiches aujourd'hui, et la ligne change
# ── d'elle-même à la prochaine série.
TYPES_FICHE = ("fiche-document", "note-dossier")
TITRE_JOURNAL = re.compile(r"^#{1,6}[^\S\n]+.{0,40}Journal des corrections", re.M)
RATURE = re.compile(r"~~(.{3,600}?)~~", re.S)
FENETRE_GRAS = 6          # mesuré : 5/5 des ratures du corpus ouvrent le gras à +3
DATE = re.compile(r"\b\d{2}/\d{2}(?:/\d{4})?\b")
# ──8<── extrait par le témoin : ne pas déplacer sans relancer convention_fiches.py
def type_de(texte):
    """Le `type:` du frontmatter, ou None si la fiche n'en a pas."""
    if not texte.startswith("---"):
        return None
    fin = texte.find("\n---", 3)
    for l in texte[:fin if fin > 0 else 2000].splitlines():
        if l.startswith("type:"):
            return l[5:].strip()
    return None

def est_fiche(texte):
    return type_de(texte) in TYPES_FICHE

def marque_datee(suite):
    """Un gras ouvrant dans les 6 premiers caractères, et une date DEDANS."""
    g = re.match(r".{0,%d}?\*\*(.{0,200}?)\*\*" % FENETRE_GRAS, suite, re.S)
    return bool(g and DATE.search(g.group(1)))

def anomalies(texte):
    """Les écarts à la convention, sans réseau et sans git. Détection POSITIVE :
    une fiche sans rature et sans titre de journal ne rend RIEN."""
    out = []
    for m in RATURE.finditer(texte):
        if not marque_datee(texte[m.end():m.end() + 220]):
            out.append(("RATURE SANS MARQUE DATÉE",
                        re.sub(r"\s+", " ", m.group(1))[:90]))
    for m in TITRE_JOURNAL.finditer(texte):
        out.append(("JOURNAL DANS UNE FICHE", m.group(0).strip()[:90]))
    return out
# ──8<── fin de la tranche extraite

def fiches_du_depot():
    for d in ("sources/veille", "livrables/lecons", "livrables/controles",
              "livrables/documents", "outils/scripts/non_regression"):
        for f in sorted((RACINE / d).rglob("*.md")):
            try:
                t = f.read_text(encoding="utf-8")
            except OSError:
                continue
            if est_fiche(t):
                yield f, t

def verdict(chemins):
    lus = rat = pb = 0
    for c in chemins:
        p = pathlib.Path(c)
        try:
            t = p.read_text(encoding="utf-8")
        except OSError as e:
            print("⛔ FICHE ILLISIBLE : %s (%s)" % (c, e))
            return 1
        if not est_fiche(t):
            print("· %s — type « %s », hors convention des fiches" % (p.name, type_de(t)))
            continue
        lus += 1
        n = len(RATURE.findall(t))
        rat += n
        for quoi, extrait in anomalies(t):
            pb += 1
            print("⚠ CONVENTION DES FICHES — %s : %s — « %s »" % (quoi, p.name, extrait))
    # le dénominateur est imprimé : un décompte d'écarts sans le décompte de ce
    # qui a été lu ne veut rien dire (règle de ㉜)
    print("CONVENTION DES FICHES : %d fiche(s) lue(s) · %d rature(s) · %d écart(s)"
          % (lus, rat, pb))
    return 0

def autotest():
    jouees, ko = [], []
    def borne(nom, cond):
        jouees.append(nom)
        if not cond:
            ko.append(nom)
            print("  ✗ %s" % nom)
    F = "---\ntype: fiche-document\n---\n# n\n\n"
    D = "---\ntype: note-dossier\n---\n# n\n\n"
    # ① les trois formes conformes du corpus, au littéral
    borne("① rature + ** MESURE ET CORRIGE le JJ/MM/AAAA **",
          anomalies(F + "~~le 2031 est un heritage~~ → **MESURÉ ET CORRIGÉ le 12/11/2026** : zero occurrence.") == [])
    borne("② rature + ** FAIT le JJ/MM ** (date courte)",
          anomalies(F + "~~lire les deux URL du log~~ → **FAIT le 20/11** : archive de 2017.") == [])
    borne("③ rature + ** tranche le JJ/MM/AAAA ** avec tiret cadratin",
          anomalies(D + "~~Le perimetre adultes~~ — **tranché le 19/08/2026** : voir ci-dessous.") == [])
    # ② ce que la convention refuse
    borne("④ rature + marque NON datee → 1 ecart",
          [q for q, _ in anomalies(F + "~~l'article 50~~ — **tranché** : en application.")] == ["RATURE SANS MARQUE DATÉE"])
    borne("⑤ rature sans aucune marque → 1 ecart",
          len(anomalies(F + "~~une affirmation renversee~~ et la suite de la phrase.")) == 1)
    # ③ la borne qui a DÉCIDÉ la forme du test : la date hors du gras ne compte pas
    borne("⑥ date APRES le gras (le cas AI-Act a +65) → refuse",
          len(anomalies(F + "~~la transposition~~ — **suivi** : autorites non designees au 04/09/2026.")) == 1)
    # ④ le gras trop loin de la rature n'est pas sa marque
    borne("⑦ gras date mais a +40 de la rature → refuse",
          len(anomalies(F + "~~une affirmation~~ suivie de quarante caracteres de prose puis **le 12/11/2026**.")) == 1)
    # ⑤ DÉTECTION POSITIVE — doivent être ACCEPTÉES
    borne("⑧ ACCEPTÉE : une fiche sans rature ne rend RIEN",
          anomalies(F + "Un resume dense, aucune rature, aucun journal.") == [])
    borne("⑨ ACCEPTÉE : la fiche qui RAPPORTE le journal de son .docx",
          anomalies(F + "**Corrigé le 17/09/2026, journal dans le document** : huit corrections.") == [])
    borne("⑩ ACCEPTÉE : la fiche qui CITE le marqueur du .docx entre crochets",
          anomalies(F + "`controle_attributions` lit a l'interieur des marqueurs `[Corrigé le …]`.") == [])
    borne("⑪ ACCEPTÉE : la phrase nue « Journal des corrections » hors titre",
          anomalies(F + "Le libelle d'origine est au Journal des corrections du document.") == [])
    # ⑥ le titre, lui, est un écart
    borne("⑫ un TITRE de journal dans la fiche → 1 ecart",
          [q for q, _ in anomalies(F + "## \U0001f4dd Journal des corrections\n\nune entree.")] == ["JOURNAL DANS UNE FICHE"])
    # ⑦ prédicat structurel
    borne("⑬ ACCEPTÉE : `type: veille` est hors convention",
          est_fiche("---\ntype: veille\n---\n") is False)
    borne("⑭ ACCEPTÉE : un .md sans frontmatter est hors convention",
          est_fiche("# CLAUDE.md\n\ndes consignes.\n") is False)
    borne("⑮ les deux types de fiche sont dans le predicat",
          est_fiche(F) and est_fiche(D))
    # ⑧ le prédicat n'est pas une liste de chemins : un nom FABRIQUÉ est couvert
    borne("⑯ ACCEPTÉE : une fiche d'une serie qui n'existe pas est couverte",
          est_fiche("---\ntype: fiche-document\nserie: serie-inventee-2099\n---\n"))
    # ⑨ le corpus réel : la mesure du jour, et elle doit rester lisible
    reel = list(fiches_du_depot())
    borne("⑰ le predicat trouve un corpus NON VIDE sur le depot",
          len(reel) >= 300)
    # ⚠️ ON N'ÉPINGLE PAS LE COMPTE D'ÉCARTS DU DÉPÔT RÉEL, et c'est une leçon payée cinq
    #    fois : une borne dont le spécimen est une propriété VIVANTE périme toute seule
    #    (15, 22, 23/10, 04/11, 17/11) — et ici la convention INVITE à corriger les 2 ratures
    #    non datées d'AI-Act_dossier, donc la borne tomberait le jour où le dépôt progresse.
    #    Le compte réel est IMPRIMÉ par le verdict, et le harnais EXIGE cette ligne ; ce qui est
    #    gardé ici est le verdict de BOUT EN BOUT sur une fiche FABRIQUÉE en tempfile.
    import tempfile, io, contextlib
    with tempfile.TemporaryDirectory() as d:
        bonne = pathlib.Path(d) / "a.fiche.md"
        bonne.write_text(F + "~~une affirmation~~ \u2192 **FAIT le 20/11** : mesure.", encoding="utf-8")
        mauvaise = pathlib.Path(d) / "b.fiche.md"
        mauvaise.write_text(F + "~~une affirmation~~ \u2014 **tranch\u00e9** : sans date.", encoding="utf-8")
        hors = pathlib.Path(d) / "c.md"
        hors.write_text("# sans frontmatter\n", encoding="utf-8")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = verdict([str(bonne), str(mauvaise), str(hors)])
        sortie = buf.getvalue()
    borne("⑱ le VRAI verdict, de bout en bout sur des fiches fabriquees : 2 lues, 1 ecart",
          "CONVENTION DES FICHES : 2 fiche(s) lue(s) · 2 rature(s) · 1 écart(s)" in sortie)
    borne("⑲ ACCEPTÉE : le verdict sort en 0 MÊME quand il alerte (non bloquant)",
          code == 0)
    borne("⑳ le verdict NOMME le fichier en écart et DIT lequel des deux motifs",
          "b.fiche.md" in sortie and "RATURE SANS MARQUE DATÉE" in sortie
          and "a.fiche.md" not in sortie)
    borne("㉑ le verdict DIT qu'un .md hors predicat est hors convention, au lieu de se taire",
          "c.md" in sortie and "hors convention" in sortie)
    print("%d/%d bornes de la convention des fiches .md — l'affirmation d'origine reste visible, datee, la ou elle est amendee"
          % (len(jouees) - len(ko), len(jouees)))
    return 1 if ko else 0

if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "--autotest":
        sys.exit(autotest())
    if a and a[0] == "--corpus":
        sys.exit(verdict([str(f) for f, _ in fiches_du_depot()]))
    if not a:
        sys.exit(__doc__.strip().splitlines()[-3])
    sys.exit(verdict(a))
