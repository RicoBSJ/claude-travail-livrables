#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Relit une édition de veille à l'édition PRÉCÉDENTE et à la FICHE de celle-ci. (12/10/2026)

POURQUOI. Trois incidents mesurés, tous de la même forme : une correction datée, écrite noir sur
blanc dans l'édition N-1 ou dans sa fiche, revient dans l'édition N.
  · veille iMac du 11/10/2026 : l'entrée 7 du journal du 04/10 retirait « TSMC » du procédé du M6,
    « le fondeur n'étant pas nommé sur la page citée ». Le 11/10 écrit « 2 nm (TSMC N2) ».
  · veille HAS du 12/10/2026 : la fiche du 05/10 démontrait que « note de cadrage mise en ligne le
    11/03/2025 » est faux (11 mars = validation, mise en ligne = 19 mars). Le 12/10 l'écrit tel quel.
  · veille HAS du 12/10/2026 : « aucune entrée du secteur datée de la fenêtre », vraie le 02/09 et
    le 05/10, recopiée telle quelle la première semaine où le secteur a publié.
Aucun contrôle du dépôt ne regardait l'édition précédente : `--docs` ne voit que la passe A, et
`controle_attributions.py` ne connaît qu'un document à la fois.

CE QUE LE CONTRÔLE SAIT FAIRE, ET CE QU'IL NE SAIT PAS.
  ① BLOQUANT — un JETON que la correction de N-1 a RETIRÉ et qui revient en N. Un jeton est fautif
     s'il est cité entre guillemets par le journal ou un marqueur de N-1 ET s'il est absent du corps
     corrigé de N-1 : c'est la signature d'une correction défaite. « TSMC » : corps du 04/10 = 0,
     journal = 1, corps du 11/10 = 1 → refusé.
  ② BLOQUANT — une SUITE DE MOTS qu'une fiche de N-1 donne pour fautive et qui revient en N. La
     fiche est de la prose : on ne retient qu'une citation entre guillemets voisine d'un mot de faute
     (« à tort », « faux », « ne figure », « zéro occurrence »…), et on exige un recouvrement de
     MOTS_MINI mots consécutifs. « note de cadrage mise en ligne le 11/03/2025 » = 8 mots → refusé.
  ③ NON BLOQUANT — une phrase d'ABSENCE recopiée mot pour mot de N-1 sans mention d'héritage. Une
     absence vraie une semaine peut être fausse la suivante ; recopiée, elle n'est plus vérifiée.
  ⛔ CE QU'IL NE SAIT PAS FAIRE, et il faut le dire : l'APPARIEMENT fautif. Le 04/10 corrigeait un
     Lenovo à 1 349 € donné en Core Ultra 7 / 32 Go / 1 To chez Fnac ; le 11/10 le réécrit à
     1 349,99 € chez Darty. Aucun jeton n'avait été retiré — « 1 349 » reste dans le corps corrigé du
     04/10, légitimement, puisque la correction a RÉATTRIBUÉ le prix à une autre configuration. Un
     contrôle de texte ne distingue pas un prix réattribué d'un prix réinventé. Ce rejeu-là reste à
     la relecture humaine, et le contrôle ne prétend pas le voir.

NFC OBLIGATOIRE. Les marqueurs du dépôt sont écrits tantôt avec un « é » précomposé, tantôt avec
« e » + U+0301 (NFD) : `\\[Corrigé le` ne trouve alors RIEN. MARQUEUR de controle_attributions.py n'y
survit que parce qu'il liste aussi les variantes sans accent. Ici tout est normalisé en NFC d'abord.

Sorties : 0 = rien à signaler · 1 = rejeu bloquant · 2 = pas d'édition précédente (inerte, et ce
n'est PAS une réussite).
"""
import sys, os, re, html, zipfile, unicodedata, glob

MOTS_MINI = 6          # ② recouvrement minimal, en mots consécutifs
MOTS_ABSENCE = 8       # ③ longueur minimale d'une phrase d'absence recopiée
JETON_MINI = 3         # ① longueur minimale d'un jeton

MARQUEUR = re.compile(r"\[(?:Corrigé|Corrige|Précisé|Precise|Ajouté|Ajoute|Note du|Vérifié|Verifie)\b"
                      r"[^\[\]]*(?:\[[^\]]*\][^\[\]]*)*\]", re.S)
# ① la BORNE. Première version le 12/10/2026, RESSERRÉE le 14/10/2026 après un faux refus EN
#    PRODUCTION : le contrôle a refusé trois fois le push du job serafin-ph-veille du 14/10 sur deux
#    jetons — « Inaccessible », tiré de « ⛔ Inaccessible (404) », et « Semaine », tiré de « Semaine
#    creuse ». Deux mots ordinaires de la langue, capitalisés seulement parce qu'ils ouvrent une
#    cellule de tableau, et qui reviennent parce que la série en parle chaque semaine. Le livrable
#    était juste ; le contrôle avait tort, et il a laissé un commit non poussé.
#    CE QUI AVAIT ÉTÉ MAL BORNÉ. La version du 12/10 retenait une citation si elle était COURTE
#    (≤ 4 mots) **OU** suivie d'une dénonciation. La prémisse du « court » était qu'un jeton tiré
#    d'une citation brève EST l'objet de la correction. C'est faux : une citation brève est le plus
#    souvent une ÉTIQUETTE — « ⛔ Inaccessible (404) », « Semaine creuse » — dont les mots sont le
#    vocabulaire ordinaire de la série. Ce qui distinguait « TSMC », ce n'était pas la brièveté de
#    « Procédé 2 nm TSMC », c'était que TSMC est un NOM PROPRE et que la citation est suivie d'une
#    dénonciation explicite (« le fondeur n'étant pas nommé sur la page citée »).
#    LA BORNE EST DONC UN ET, SUR DEUX AXES INDÉPENDANTS, mesurés le 14/10/2026 :
#      · la citation doit être suivie d'une DÉNONCIATION explicite (le 12/10 déjà : 0 faux positif
#        sur les 73 éditions, et « TSMC » retenu) ;
#      · le jeton ne doit pas OUVRIR la citation — un mot capitalisé en tête de citation ou juste
#        après un symbole n'est pas un nom propre, c'est un début de phrase ou de cellule.
#      Mesure : « Inaccessible » et « Semaine » sont tous deux en TÊTE et NON dénoncés ; « TSMC » est
#      au MILIEU et dénoncé. Les deux axes séparent, et on exige les deux.
#    CE QUE LA BORNE COÛTE, et il faut le dire : un jeton réellement retiré par une correction mais
#    dont la citation d'origine n'est pas suivie d'une explication échappe désormais au motif. Le
#    journal d'une veille corrigée liste souvent ses formulations d'origine sans les commenter une
#    par une — c'est le cas de huit des dix entrées du 04/10 sur la série iMac. Le motif ne voit donc
#    que les corrections EXPLIQUÉES. C'est le prix d'un contrôle bloquant qui ne doit jamais refuser
#    un livrable juste : en production, un faux refus coûte un livrable non publié, un vrai manqué ne
#    coûte qu'une relecture humaine.
MOTS_CITATION = 4
# ─────────────────────────────────────────────────────────────────────────────
# 🔴 TROISIÈME BORNE DU MOTIF ①, LE 19/10/2026 — UN JETON REVENU SEUL NE BLOQUE PLUS.
#    DEUXIÈME FAUX REFUS EN PRODUCTION, et le resserrement du 14/10 ne le voyait pas venir.
#    La veille has-actualite du 19/10 a été refusée trois fois sur le jeton « Commission »,
#    retiré du corps du 12/10 par une correction JUSTE : la note y attribuait trois validations
#    « à la Commission en charge du social et du médico-social (CSMS) », ce qu'aucune des trois
#    pages n'écrivait. Le 19/10 écrit « Commission de la transparence (21/10) — hors secteur
#    social & médico-social », et le calendrier HAS porte littéralement « 21/10/2026 Commission
#    Commission de la transparence - Réunion du 21 octobre 2026 ». Même mot, autre organisme,
#    page listée, fait exact — et la revendication corrigée, elle, ne revient nulle part.
#    LES DEUX AXES DU 14/10 NE SÉPARENT PAS CE CAS : la citation d'origine EST suivie d'une
#    dénonciation (« zéro occurrence ») et le jeton n'est PAS en tête de citation.
#    TROIS BORNES ESSAYÉES ET MESURÉES AVANT DE RETENIR CELLE-CI (19/10/2026) :
#      · recouvrement de 2 mots consécutifs avec la citation : « oct. 2031 » contre « octobre
#        2031 » ne se recouvrent pas — la borne perdait le VRAI rejeu du 18/10 ;
#      · fréquence du JETON dans la série : « Commission » 26 % des éditions has-actualite,
#        « Microsoft » 23 %, « 2031 » 35 %, « TSMC » 17 % des éditions imac — les distributions
#        sont entrelacées, aucun seuil ne sépare ;
#      · accompagnateur pris parmi les seuls JETONS de la citation : « Procédé 2 nm TSMC » n'en
#        a qu'un, « Procédé » ouvrant la citation — la borne perdait le rejeu FONDATEUR du
#        11/10, et son témoin au harnais passait de 1 à 0. Mesuré, puis abandonné ;
#      · ubiquité calculée sur les AUTRES éditions de la série : séparait (social 100 %,
#        medico 100 %, apple 100 %, windows 93 % contre nm 31 %, microsoft 25 %, tsmc 18 %),
#        mais un témoin gelé n'a pas de série autour de lui : le dossier ne contient que N et
#        N-1, le vocabulaire sortait vide et le faux refus revenait. Remplacée par la
#        fréquence dans le corps de N-1, qui est autonome et donne les mêmes verdicts ;
#      · nombre de jetons revenus de la même citation : 2 pour le 18/10, 1 pour le 19/10 — mais
#        1 aussi pour « TSMC » le 11/10, qui est le rejeu fondateur. La borne cassait le témoin.
#    CE QUI SÉPARE, MESURÉ : un VRAI rejeu ramène le jeton ACCOMPAGNÉ d'un autre jeton
#    distinctif de la même citation, tout près. Distances mesurées sur les deux cas gelés :
#    « Microsoft » à 47 caractères de « 2031 » (vrai rejeu du 18/10) ; pour « Commission », le
#    seul accompagnateur non calendaire est « CSMS », à 128 caractères. FENETRE = 80 sépare,
#    avec 33 caractères de marge d'un côté et 48 de l'autre — elle n'est pas ajustée sur un
#    point unique : toute valeur de 48 à 127 donne le même verdict sur les deux cas.
#    ⚠️ ET UNE ANNÉE NUE NE CORROBORE RIEN. « 2026 » était à 62 caractères de « Commission » et
#    aurait suffi à maintenir le faux refus : dans une veille hebdomadaire, un millésime est un
#    horodatage présent dans presque chaque phrase, pas un élément de la revendication.
#    CE QUE LA BORNE COÛTE, ET IL FAUT LE DIRE : un vrai rejeu dont la citation d'origine n'a
#    qu'UN seul jeton distinctif non calendaire ne bloque plus — il sort en AVERTISSEMENT, avec
#    sa ligne. C'est le compromis assumé du dépôt : en production un faux refus coûte un
#    livrable non publié, un vrai manqué ne coûte qu'une relecture humaine.
FENETRE = 80           # distance maximale, en caractères, entre le jeton revenu et son accompagnateur
ANNEE = re.compile(r"^(?:19|20)\d\d$")     # un millésime nu n'accompagne pas : il horodate
VOC_MIN = 5           # occurrences dans le corps de N-1 au-delà desquelles un mot est du VOCABULAIRE
DENONCE = re.compile(r"(?i)n['’]?(?:est|était|étant|e figure|e figurait)? ?(?:pas|plus)? ?nomm"
                     r"|pas sur la page|ne figure|absent|z[ée]ro occurrence|invent|fabriqu|non v[ée]rifi"
                     r"|aucune page|n['’]a pas [ée]t[ée]|sans source|non list")
FAUTE = re.compile(r"(?i)à tort|faux|fausse|erreur|inexact|n[e']? ?(?:est|sont) pas|ne figure|absent"
                   r"|z[ée]ro occurrence|confond|mal [ée]tiquet|rejou|invent|fabriqu|non littéral"
                   r"|aurait d[uû]|devient|au lieu de|alors que la page")
HERITAGE = re.compile(r"(?i)d['’]apr[èe]s l['’][ée]dition du|[ée]dition du \d\d/\d\d")
ABSENCE = re.compile(r"(?i)\baucun[e]?\b|\bpas de\b|\bn['’]a pas\b")
# une phrase qui parle de l'OUTIL et non du SUJET n'est pas un constat d'absence : « n'a été relu sur
# aucune page », « aucune source n'a pu être ouverte » décrivent l'exécution, pas le marché ni le secteur.
METHODE = re.compile(r"(?i)aucune? (?:page|source|adresse|url)|(?:relu|lu|ouvert|vérifi|consult|aspir)"
                     r"[^.]{0,40}aucune?|cette ex[ée]cution|agent de navigateur|cadrage du job|HTTP")

def nfc(s):
    return unicodedata.normalize("NFC", s)

def paragraphes(p):
    x = zipfile.ZipFile(p).read("word/document.xml").decode("utf-8")
    ps = re.findall(r"<w:p(?:\s[^>]*)?>.*?</w:p>", x, re.S)
    return [nfc(html.unescape("".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", q)))) for q in ps]

def para_sans_marqueur(T):
    """le texte des paragraphes de N-1 QUI NE PORTENT PAS de marqueur : ce que la fiche a dénoncé
    et que personne n'a corrigé. Un paragraphe marqué a été traité — sa formulation d'origine est
    dans le marqueur, et ce qui reste dans le corps est la version corrigée."""
    i = [k for k, t in enumerate(T) if "Journal des corrections" in t]
    fin = i[0] if i else len(T)
    return " ".join(t for t in T[:fin] if not MARQUEUR.search(t))

def decoupe(T):
    """(corps sans marqueurs, journal, marqueurs) — le journal commence à son titre"""
    i = [k for k, t in enumerate(T) if "Journal des corrections" in t]
    fin = i[0] if i else len(T)
    brut = " ".join(T[:fin])
    marqueurs = " ".join(m.group(0) for m in MARQUEUR.finditer(brut))
    corps = MARQUEUR.sub(" ", brut)
    return corps, " ".join(T[fin:]), marqueurs

def mots(s):
    return re.findall(r"[0-9A-Za-zÀ-ÿ]+(?:[.,/][0-9]+)*", s)

def cle(s):
    z = unicodedata.normalize("NFKD", s.lower())
    z = "".join(c for c in z if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", z).strip()

def plat(s):
    """espaces normalisés, ponctuation CONSERVÉE : sinon « 1 338,23 » contient « 1 338 ».
    Mesuré le 12/10/2026 : avec cle(), le motif ① accusait « 1 338 » sur la veille iMac du 11/10,
    où le prix réel est « 1 338,23 € » pour un AUTRE modèle Dell, déclaré comme extrait de recherche."""
    return re.sub(r"[ \u00a0\u202f\t]+", " ", unicodedata.normalize("NFC", s))

def motif(jeton):
    """le motif d'un jeton ENTIER : pas de chiffre ni de séparateur décimal accolé.
    UN SEUL endroit le construit — present() le teste, occurrences() le localise."""
    j = re.sub(r"[ \u00a0\u202f]+", "[ \u00a0\u202f]?", re.escape(plat(jeton).strip()))
    return re.compile(r"(?<![0-9A-Za-zÀ-ÿ.,])" + j + r"(?![0-9]|[.,][0-9])")


def present(jeton, texte):
    """le jeton est-il là, entier ? pas de chiffre ni de séparateur décimal accolé"""
    return motif(jeton).search(texte) is not None


def occurrences(jeton, texte):
    """les positions du jeton, par le MÊME motif que present()"""
    return [m.span() for m in motif(jeton).finditer(texte)]

def citations(s):
    return [re.sub(r"\s+", " ", c).strip() for c in re.findall(r"«\s*(.+?)\s*»", s, re.S)]

def citations_retenues(*sources):
    """les formulations d'origine dont un JETON peut servir de preuve : citation courte, ou citation
    suivie d'une dénonciation explicite. Voir la borne mesurée en tête de fichier."""
    gardees, vues = [], 0
    for src in sources:
        for m in re.finditer(r"«\s*(.+?)\s*»", src, re.S):
            c = re.sub(r"\s+", " ", m.group(1)).strip()
            vues += 1
            if DENONCE.search(src[m.end():m.end() + 140]):
                gardees.append((c, src[m.end():m.end() + 140]))
    return gardees, vues

def jetons(s):
    """ce qui, dans une formulation, est assez distinctif pour qu'un retour soit un retour.
    Un jeton qui OUVRE la citation (rien, ou seulement des symboles, devant lui) est écarté :
    « ⛔ Inaccessible (404) » et « Semaine creuse » ont fait refuser à tort un livrable juste
    le 14/10/2026, parce qu'un mot capitalisé en tête de cellule n'est pas un nom propre."""
    out = set()
    for m in re.finditer(r"\b\d{1,3}(?:[   ]\d{3})+(?:[.,]\d+)?\b|\b\d{3,}(?:[.,]\d+)?\b", s):
        out.add(m.group(0))
    for m in re.finditer(r"\b[A-Z]{3,}\d*\b", s):            # TSMC, QHD, N2 écrit NVME…
        out.add(m.group(0))
    for m in re.finditer(r"\b[A-Z][a-zà-ÿ]{3,}\b", s):        # Lenovo, Boulanger, Autodétermination
        out.add(m.group(0))
    gardes = set()
    for j in out:
        if len(j) < JETON_MINI: continue
        for m in re.finditer(r"(?<![0-9A-Za-zÀ-ÿ])" + re.escape(j) + r"(?![0-9A-Za-zÀ-ÿ])", s):
            avant = s[:m.start()].strip()
            if avant and not re.fullmatch(r"[^0-9A-Za-zÀ-ÿ]+", avant):
                gardes.add(j); break                      # vu au moins une fois en milieu de citation
    return gardes

def suites(s, n):
    w = mots(s)
    return {" ".join(cle(" ".join(w[i:i+n])).split()) for i in range(len(w)-n+1)} if len(w) >= n else set()

def precedente(p):
    d, b = os.path.dirname(p) or ".", os.path.basename(p)
    m = re.match(r"(\d{4}-\d\d-\d\d)_(veille_.+)\.docx$", b)
    if not m: return None
    date, suite = m.groups()
    cands = []
    for f in glob.glob(os.path.join(d, "*_%s.docx" % suite)):
        mm = re.match(r"(\d{4}-\d\d-\d\d)_", os.path.basename(f))
        if mm and mm.group(1) < date: cands.append((mm.group(1), f))
    return max(cands)[1] if cands else None

def fiche_de(p):
    base = p[:-5]
    for c in (base + ".fiche.md", base + ".md"):
        if os.path.exists(c): return c
    return None

# ─────────────────────────────────────────────────────────────────────────────
if len(sys.argv) != 2:
    sys.exit("usage : controle_edition_precedente.py <chemin du .docx>")
COUR = sys.argv[1]
if not os.path.exists(COUR):
    sys.exit("fichier introuvable : " + COUR)
PREC = precedente(COUR)
print("Édition relue    : %s" % os.path.basename(COUR))
if not PREC:
    print("Édition précédente : AUCUNE — contrôle INERTE, et ce n'est PAS une réussite")
    sys.exit(2)
print("Édition précédente : %s" % os.path.basename(PREC))
FICHE = fiche_de(PREC)
print("Fiche de la précédente : %s" % (os.path.basename(FICHE) if FICHE else "ABSENTE"))

P_COUR, P_PREC = paragraphes(COUR), paragraphes(PREC)
corps_c, journal_c, marq_c = decoupe(P_COUR)
corps_p, journal_p, marq_p = decoupe(P_PREC)
nu_p = " " + " ".join(cle(para_sans_marqueur(P_PREC)).split()) + " "   # N-1, paragraphes non corrigés
cle_c = " " + " ".join(cle(corps_c).split()) + " "
pb = []

# ① un jeton que la correction de N-1 a retiré et qui revient
print("\n① JETONS RETIRÉS PAR UNE CORRECTION DE L'ÉDITION PRÉCÉDENTE ET REVENUS (bloquant)")
cites_p, n_vues = citations_retenues(journal_p, marq_p)
cands = set()
porteuses = {}                      # jeton -> [(citation, tous ses jetons)] : il faut l'ACCOMPAGNATEUR
for c, _ctx in cites_p:
    js = jetons(c)
    cands |= js
    for j in js:
        porteuses.setdefault(j, []).append((c, js))
plat_p, plat_c = plat(corps_p), plat(corps_c)
retires = sorted(j for j in cands if not present(j, plat_p))
revenus = [j for j in retires if present(j, plat_c)]


_VOC = None


def vocabulaire():
    """le VOCABULAIRE de la série, lu dans le corps corrigé de N-1 lui-même : un mot qui y
    revient VOC_MIN fois ou plus ne peut pas servir d'accompagnateur. Autonome — aucune autre
    édition n'est ouverte, donc le verdict ne dérive pas quand la série s'allonge, et un témoin
    gelé se comporte exactement comme la production.
    MESURE DU 19/10/2026, qui fixe le seuil à 5. Écartés : « social » 12 et « medico » 7 dans la
    veille has-actualite du 12/10, « csms » 8, « windows » 17 et « annonce » 7 dans la veille
    imac du 11/10, « apple » 27 dans celle du 04/10. Conservés : « nm » 3, « toutes » 3,
    « commission » 3, « support » 2, « oct » 2, « procede » 1, « validees » 1, « charge » 1,
    « jusqu » 0, « microsoft » 0, « tsmc » 0. Le vide entre 3 et 7 est large : tout seuil de 4 à
    7 rend les mêmes verdicts sur les trois cas gelés."""
    global _VOC
    if _VOC is None:
        from collections import Counter
        k_ = Counter(cle(corps_p).split())
        _VOC = {w for w, n_ in k_.items() if n_ >= VOC_MIN}
    return _VOC


def accompagne(j):
    """(citation, accompagnateur, distance) si le jeton revient ACCOMPAGNÉ — voir la borne du
    19/10/2026 en tête de fichier. Sinon (None, None, None) : le retour n'est pas un rejeu
    prouvé, et il sort en avertissement."""
    ubi = vocabulaire()
    jmots = set(cle(j).split())
    for c, js in porteuses.get(j, []):
        # les mots de la CITATION, pas ses seuls jetons : « Procédé 2 nm TSMC » n'a qu'un jeton
        # distinctif — « Procédé » ouvre la citation, donc le garde du 14/10 l'écarte — et le
        # rejeu fondateur du 11/10 serait passé sans ces mots-là. Écartés : le jeton lui-même,
        # les mots de moins de 3 lettres, le vocabulaire ubiquitaire de la série, et un millésime
        # nu qui n'a pas été retiré (il horodate ; « 2031 », retiré, reste un accompagnateur).
        retires_cle = {w for r in retires for w in cle(r).split()}
        autres = [w for w in sorted(set(cle(c).split()))
                  if len(w) >= 3 and w not in jmots and w not in ubi
                  and (w in retires_cle or not ANNEE.match(w))]
        for d, f_ in occurrences(j, plat_c):
            fen = " " + " ".join(cle(plat_c[max(0, d - FENETRE):f_ + FENETRE]).split()) + " "
            for a in autres:
                if (" " + a + " ") in fen:
                    pos = [p for p in occurrences(a, plat_c)] or [(d, d)]
                    dist = min(abs(p[0] - d) for p in pos)
                    return c, a, dist
    return None, None, None


print("   %d citation(s) d'origine dans le journal et les marqueurs de N-1, dont %d retenue(s)"
      " (suivie d'une dénonciation explicite) · %d jeton(s) distinctif(s), hors tête de citation"
      " · %d retiré(s) du corps corrigé"
      % (n_vues, len(cites_p), len(cands), len(retires)))
if revenus:
    for j in revenus:
        ou = [c for c, _ in cites_p if j in c]
        c_, acc, dist = accompagne(j)
        if acc:
            print("   INTERDIT « %s » — retiré du corps de %s par une correction, présent dans celui-ci"
                  % (j, os.path.basename(PREC)[:10]))
            print("             accompagné de « %s » à %d caractère(s) : la revendication revient,"
                  " pas seulement le mot" % (acc, dist))
            if ou: print("             formulation d'origine : « %s »" % ou[0][:150])
            pb.append("jeton « %s » revenu" % j)
        else:
            autres = sorted(set().union(*[js for _, js in porteuses.get(j, [])]) - {j}) or ["(aucun)"]
            print("   À RELIRE « %s » — retiré du corps de %s, présent ici, mais SEUL : aucun autre"
                  " jeton de sa citation à moins de %d caractères (non bloquant)"
                  % (j, os.path.basename(PREC)[:10], FENETRE))
            print("             autres jetons de la citation : %s — millésimes exclus, ils horodatent"
                  % ", ".join(autres[:6]))
            if ou: print("             formulation d'origine : « %s »" % ou[0][:150])
            print("             le mot revient, la revendication corrigée peut ne pas revenir :"
                  " relis ce passage à la main")
else:
    print("      (aucun)")

# ② une suite de mots que la fiche de N-1 donne pour fautive
print("\n② FORMULATIONS QUE LA FICHE DE L'ÉDITION PRÉCÉDENTE DONNE POUR FAUTIVES ET QUI REVIENNENT (non bloquant)")
n_marq_p = len(MARQUEUR.findall(" ".join(P_PREC)))
if not FICHE:
    print("   fiche absente — motif INERTE, et ce n'est PAS une réussite")
elif n_marq_p:
    # N-1 PORTE des marqueurs : ses défauts ont été traités, et sa fiche cite alors les deux
    # versions — la fautive ET la corrigée. Une suite de mots commune aux deux ne prouve rien.
    # Mesuré le 12/10/2026 : sur la veille iMac du 04/10 (7 marqueurs), ce motif accusait
    # « Mac mini M6 : 1 049 € depuis le 22/09/2026 », qui est le DÉBUT de la formulation corrigée.
    # C'est la passe ① qui répond pour une édition corrigée : elle part du journal, pas de la fiche.
    print("   édition précédente CORRIGÉE (%d marqueur(s)) — motif ② hors sujet : ses défauts sont"
          " tracés dans son journal, et c'est ① qui les suit. INERTE ici." % n_marq_p)
else:
    txt = nfc(open(FICHE, encoding="utf-8").read())
    fautives, n_cit = [], 0
    for m in re.finditer(r"«\s*(.+?)\s*»", txt, re.S):
        c = re.sub(r"\s+", " ", m.group(1)).strip()
        if len(mots(c)) < MOTS_MINI: continue
        n_cit += 1
        fen = txt[max(0, m.start()-220): m.end()+220]
        if FAUTE.search(fen): fautives.append(c)
    trouves, ecartees = [], 0
    for c in fautives:
        for s in suites(c, MOTS_MINI):
            if not s or (" %s " % s) not in cle_c: continue
            # la formulation doit encore vivre dans un paragraphe NON CORRIGÉ de N-1 : sinon la
            # fiche dénonçait une formulation déjà traitée, et ce qui revient est la version corrigée
            if (" %s " % s) not in nu_p: ecartees += 1; continue
            trouves.append((c, s)); break
    print("   %d citation(s) de %d mots ou plus dans la fiche · %d voisine(s) d'un mot de faute"
          " · %d écartée(s) : la formulation avait été corrigée dans N-1"
          % (n_cit, MOTS_MINI, len(fautives), ecartees))
    if trouves:
        for c, s in trouves:
            print("   A RELIRE la fiche de N-1 donne pour fautif « %s »" % c[:150])
            print("             et cette édition en reprend %d mots : « %s »" % (MOTS_MINI, s))
            print("             non bloquant : une citation de fiche voisine d'un mot de faute n'est pas"
                  " toujours la formulation fautive — relis le passage de la fiche")
    else:
        print("      (aucune)")

# ③ une phrase d'absence recopiée telle quelle
print("\n③ PHRASES D'ABSENCE RECOPIÉES DE L'ÉDITION PRÉCÉDENTE SANS MENTION D'HÉRITAGE (non bloquant)")
ph_p = [p_ for p_ in re.split(r"(?<=[.!?:])\s+|\n", corps_p)
        if ABSENCE.search(p_) and not METHODE.search(p_) and len(mots(p_)) >= MOTS_ABSENCE]
rec = []
for p_ in ph_p:
    k = " ".join(cle(p_).split())
    if not k: continue
    if (" %s " % k) in (" " + " ".join(cle(corps_c).split()) + " "):
        ph_c = [q for q in re.split(r"(?<=[.!?:])\s+|\n", corps_c)
                if k in " ".join(cle(q).split())]
        if ph_c and HERITAGE.search(ph_c[0]): continue
        rec.append((p_, k))
print("   %d phrase(s) d'absence de %d mots ou plus dans N-1 · %d recopiée(s) MOT POUR MOT sans"
      " mention d'héritage" % (len(ph_p), MOTS_ABSENCE, len(rec)))
for p_, s in rec[:8]:
    print("   A RELIRE « %s »" % re.sub(r"\s+", " ", p_)[:150])
    print("             une absence vraie la semaine passée peut être fausse celle-ci : revérifie-la")

print()
if pb:
    sys.exit("ÉDITION REFUSÉE — %d rejeu(x) : %s" % (len(pb), " ; ".join(pb)))
print("OK — aucune correction de l'édition précédente ni de sa fiche n'est rejouée"
      "%s" % (" (et %d absence(s) recopiée(s) à revérifier)" % len(rec) if rec else ""))
