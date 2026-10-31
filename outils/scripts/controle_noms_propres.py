#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
㊵ — UN NOM PROPRE PRÊTÉ À UNE PAGE EST-IL SUR CETTE PAGE ?

NÉ DE DEUX INCIDENTS MESURÉS, À CINQ JOURS D'ÉCART, DANS LA MÊME SÉRIE :
  · 24/10/2026, veille ai-act — « Poitiers Métropole » donné comme troisième organisateur
    de la Journée RGPD de la CNIL. « Métropole » : ZÉRO occurrence sur la page citée, qui
    écrit « la Communauté urbaine du Grand Poitiers ». Le journal de cette correction
    concluait lui-même : « Aucun contrôle du dépôt ne pouvait voir ce défaut ».
  · 30/10/2026, veille ai-act — « Lara Comi » et « Leonardo Benifei » là où la newsletter
    source écrit « Alex Agius Saliba » et « Brando Benifei ». « Lara Comi » : ZÉRO
    occurrence sur les SEPT pages lisibles du document. Et la substitution changeait de
    camp politique : Lara Comi siège au PPE, que la phrase suivante oppose à ces députés.

POURQUOI AUCUNE PASSE EXISTANTE NE LES VOIT, ET CE N'EST PAS UNE FAILLE :
  B et B-FR cherchent des CITATIONS entre guillemets, B-NOM des AFFIRMATIONS prêtées à une
  source nommée (« selon X », « X indique »), D des VALEURS CHIFFRÉES. Un nom propre dans
  une parenthèse n'est aucun des trois. Sur la veille du 30/10, cinq des dix passes sont
  INERTES — 0 citation anglaise, 0 citation française, 0 valeur chiffrée attribuée — et la
  seule sortie est un B-NOM « À RELIRE » non bloquant. La surface de contrôle d'un document
  est proportionnelle à ce qu'il CITE : une veille écrite entièrement au style indirect
  désarme presque tout l'appareil.

⛔ NON BLOQUANT, ET C'EST UNE DÉCISION MESURÉE, PAS UNE PRUDENCE.
  Un nom propre peut légitimement ne figurer sur aucune page listée : il peut venir d'une
  recherche par moteur, d'une édition antérieure, ou être un nom que le document apporte
  lui-même (un auteur cité, une institution nommée en passant). Le motif ne distingue pas
  « inventé » de « sourcé ailleurs » — il ne peut pas. En production un faux refus coûte un
  livrable non publié, un vrai manqué coûte une relecture : règle du 14/10/2026.

LES BORNES SONT MESURÉES SUR LE CORPUS, PAS DEVINÉES — voir --mesure.
"""
import sys, re, os, subprocess, unicodedata

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RACINE = os.path.dirname(RACINE) if os.path.basename(RACINE) == "outils" else RACINE
assert os.path.isdir(os.path.join(RACINE, "outils", "scripts")), "RACINE mal calculée : %s" % RACINE
sys.path.insert(0, os.path.join(RACINE, "outils", "scripts"))

# ── BORNE ① : un nom est une suite de DEUX jetons capitalisés OU PLUS.
#    Mesuré : les trois noms des deux incidents en ont exactement deux (« Lara Comi »,
#    « Leonardo Benifei », « Poitiers Métropole »). À UN jeton, le motif ramasse chaque
#    début de phrase, chaque intitulé de tableau et chaque sigle : inexploitable.
MIN_JETONS = 2
# ── BORNE ② : chaque jeton fait au moins 3 lettres. Écarte « M. Dupont », « n° 179 »,
#    les initiales et les particules isolées, sans écarter aucun nom des incidents.
MIN_LETTRES = 3

PARTICULES_NOM = {"de", "du", "des", "la", "le", "van", "von", "der", "di", "al"}
MAJ = "A-ZÀÂÄÇÉÈÊËÎÏÔÖÙÛÜŸÆŒ"
MIN = "a-zà-öø-ÿ"
# un jeton capitalisé : majuscule puis minuscules, trait d'union et apostrophe internes admis
JETON = r"[%s][%s%s'’\-]{%d,}" % (MAJ, MAJ, MIN, MIN_LETTRES - 1)
# ── BORNE ⑤ : LE SÉPARATEUR EST UN ESPACE DE LA MÊME LIGNE, JAMAIS UN SAUT DE LIGNE.
#    Deux défauts MESURÉS le 31/10/2026, tous deux dans la mécanique du motif, pas dans ses seuils :
#    ① `\s*` autorisait ZÉRO espace, donc un mot tout en capitales se coupait en deux pseudo-jetons
#       — « ORANGE » = « ORA » + « NGE » —, et le niveau d'alerte d'une veille devenait un nom propre
#       absent de toutes les pages, c'est-à-dire un faux refus ;
#    ② `extract_docx.py` joint CHAQUE `<w:t>` par un saut de ligne — il n'y a pas de paragraphes dans
#       sa sortie, il y a des RUNS. Un `\s+` qui franchit le saut recolle donc deux cellules de tableau
#       ou un titre et le mot suivant : « Marchand Écart », « Los Angeles Calendrier »,
#       « WebSearch Lenovo IdeaCentre AIO ». C'est l'ambiguïté d'aplatissement déjà consignée en
#       en-tête de `controle_decompte.py`, qui lui coûte huit faux positifs.
#    ⚠️ CE QUE LE RESSERREMENT COÛTE, ET C'EST MESURÉ, PAS ARGUMENTÉ : un nom coupé en deux runs par
#       la typographie (une moitié en gras) est hors de portée. Balayage des 299 documents :
#       8,6 → 7,1 noms retenus par document, 448 clés perdues, et les 448 sont du bruit de cellules
#       recollées — « Acteur Rôle », « Activité Type Durée », « ARS Déclinaison ». Zéro nom de
#       personne ou d'organisme dans les perdus.
SEP = r"[ \u00a0\u202f]+"      # espace, espace insécable, espace fine insécable — jamais `\n`
NOM = re.compile(r"(?<![%s%s'’\-])((?:%s)(?:%s(?:%s)%s)?(?:%s(?:%s)){%d,})"
                 % (MAJ, MIN, JETON, SEP, "|".join(sorted(PARTICULES_NOM)), SEP, SEP, JETON,
                    MIN_JETONS - 1))

# ── BORNE ③ : le VOCABULAIRE est écarté, et il est LU SUR LE CORPUS, jamais écrit en dur.
#    Un nom qui apparaît dans au moins SEUIL_UBIQUITE documents distincts du dossier de la
#    série est un nom de la série : institutions, textes, organismes récurrents. Les noms
#    des deux incidents apparaissent dans UN document chacun.
SEUIL_UBIQUITE = 3
# ── BORNE ⑥ : plancher du dépôt — sous 3 000 caractères utiles, une page n'est PAS lue
#    (façade ou rendu JavaScript). Sans elle, le mur anti-automate de `handicap.gouv.fr`
#    (HTTP 200 · 93 caractères, mesuré le 28/10 ET le 31/10) aurait fait accuser
#    « Camille Galliard-Minier », qui est une personne réelle : une page muette rend
#    indiscernables une mention absente et une mention NON LUE — et c'est la direction
#    d'erreur la plus coûteuse, celle du faux refus.
PLANCHER_PAGE = 3000

def sans_accent(t):
    return "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn")

def cle(t):
    """la clé d'appariement : accents, casse et blancs pliés. Un nom propre ne se décline pas,
    mais une page peut l'écrire avec une espace insécable ou un accent de plus."""
    return re.sub(r"[^a-z0-9]", "", sans_accent(t).lower())

def corps_utile(txt):
    """le corps SEUL : sans les marqueurs de correction, sans le journal, sans la rubrique
    des sources. Un marqueur CITE le libellé fautif — le compter serait accuser la correction
    elle-même (règle du 23/10/2026, passe A), et le journal fait de même."""
    t = txt.split("📝 Journal des corrections")[0]
    t = re.sub(r"\[(?:Corrigé|Corrige|Précisé|Precise|Ajouté|Ajoute)\s+le[^\]]*\]", " ", t)
    return t

def noms(txt):
    """les noms propres du corps, dans l'ordre, dédoublonnés sur la clé."""
    vus, sortie = set(), []
    for m in NOM.finditer(corps_utile(txt)):
        n = re.sub(r"\s+", " ", m.group(1)).strip(" -–—")
        k = cle(n)
        if len(k) < 2 * MIN_LETTRES or k in vus:
            continue
        vus.add(k)
        sortie.append(n)
    return sortie

# ── BORNE ④ : LE DISCRIMINANT QUI PORTE LE MOTIF — un jeton que le corpus écrit AUSSI en
#    minuscules n'est pas un nom propre, c'est un mot commun capitalisé par sa POSITION
#    (en-tête de tableau, titre, début de ligne) ou par la typographie d'un intitulé.
#    Mesuré sur la veille du 30/10 : 18 candidats → 9 retenus, et les 9 écartés sont tous
#    des artefacts — « Date Obligation », « Jalon Statut » (deux cellules d'en-tête mises
#    bout à bout par l'aplatissement), « Human Rights », « Law Impact Assessment » (morceaux
#    d'un sigle développé), « Chaque État ». C'est la mécanique de `controle_orthographe.py`
#    du 27/10 — le corpus pour dictionnaire — appliquée à la casse.
#    Le lexique est LOCAL : le document lui-même et les pages qu'il liste. Rien n'est écrit
#    en dur, rien n'est lu ailleurs que dans ce que le document donne à lire.
PARTICULES = {"de", "du", "des", "la", "le", "van", "von", "der", "di", "al", "d", "l"}

def sous_jetons(nom):
    """les morceaux alphabétiques d'un nom : « Kim van Sparrentak » → kim, van, sparrentak ;
    « L'agent Sol » → l, agent, sol. Un nom dont un morceau est un mot commun n'est pas un nom."""
    return [x for x in re.split(r"[^A-Za-zÀ-ÿ]+", sans_accent(nom).lower()) if x]

def minuscules(txt):
    """les mots que ce texte écrit en minuscules, DÉCOMPOSÉS comme les noms le sont.
    ⚠️ Mesuré le 31/10/2026 : sans la décomposition, « d'alerte » entre au lexique comme
    « dalerte » et « alerte » n'y figure JAMAIS — donc « ALERTE CRITIQUE », le niveau d'alerte
    d'une veille, survivait à la borne ④. L'apostrophe et le trait d'union doivent se traiter
    des DEUX côtés de la comparaison, sans quoi la borne ④ compare deux découpages différents."""
    out = set()
    for w in re.findall(r"[A-Za-zÀ-ÿ'’\-]{3,}", txt):
        if w[:1].islower():
            out.update(j for j in sous_jetons(w) if len(j) >= MIN_LETTRES)
    return out


# ── BORNE ⑧ : L'INSTRUMENTATION D'UN DOCUMENT N'EST PAS SON CONTENU — c'est ㊲ (16/10/2026),
#    appliqué aux noms. « Légifrance HTTP » vient de « Légifrance (HTTP 200 testé le…) », « WebSearch
#    CNIL » et « WebFetch PMC » du nom de l'outil qui a lu la page. Mesuré sur les 299 documents :
#    16 occurrences, 12 formes, zéro nom véritable.
#    ⚠️ La liste est VOLONTAIREMENT COURTE, et la mesure dit pourquoi : « mozilla » en faisait partie
#    (l'en-tête `-A "Mozilla/5.0"` prescrit par les neuf prompts) et l'exclure perdait
#    « Mozilla Developer Network », qui est un nom légitime. On n'écarte que des jetons qui
#    n'appartiennent à AUCUN nom propre.
INSTRUMENTATION = {"http", "https", "url", "websearch", "webfetch", "curl"}

# ── BORNE ⑨ : UN NOM DE PLUSIEURS MOTS TOUT EN CAPITALES N'EST PAS UN NOM PROPRE, c'est du
#    vocabulaire d'intitulé — « ALERTE CRITIQUE », « NIVEAU D'ALERTE », « RBPP HAS », « SO-DIMM DDR »,
#    « INSERT INTO ». Mesuré sur les 299 documents : 74 occurrences, 54 formes.
#    ⚠️ Coût assumé et mesuré : « FREE MOBILE » et « VEILLE HAS », écrits ainsi dans des cellules de
#    tableau, sortent de portée. Un SIGLE SEUL n'est pas concerné — il ne franchit pas MIN_JETONS.
def tout_capitales(nom):
    mots = [j for j in re.findall(r"[A-Za-zÀ-ÿ]{%d,}" % MIN_LETTRES, nom)]
    return len(mots) >= 2 and all(j.isupper() for j in mots)

def retenus(nom, lexique):
    """vrai si le nom franchit les bornes ④, ⑧ et ⑨."""
    js = [j for j in sous_jetons(nom) if j not in PARTICULES and len(j) >= MIN_LETTRES]
    if any(j in INSTRUMENTATION for j in js):   return False    # ⑧
    if tout_capitales(nom):                     return False    # ⑨
    return not any(j in lexique for j in js)                    # ④

# ── la recherche sur les pages : au degré ② (accents, casse, ponctuation pliés), parce qu'un
#    nom propre NE SE DÉCLINE PAS — c'est le seul cas où ② suffit (règle du 15/10 : ② est
#    interdit aux chiffres, pas aux noms). Une page peut écrire « Galliard Minier » là où le
#    document écrit « Galliard-Minier », et c'est le même nom.
def sur_page(nom, textes):
    k = cle(nom)
    return [u for u, t in textes.items() if t and k in cle(t)]

def pages_du_document(urls, dest=None, frais=False):
    """aspire les pages listées EN LES RÉUTILISANT si elles sont déjà au cache (aspirer.py
    les met en cache sur la clé de l'adresse) et rend {url: texte utile}. Le contrôle est
    APPELÉ, jamais recopié : c'est aspirer.aspire() qui lit le réseau, avec son faisceau de
    certificats, ses trois essais et son plancher."""
    import aspirer, hashlib, io, contextlib
    dest = dest or aspirer.dossier_defaut()
    os.makedirs(dest, exist_ok=True)
    textes = {}
    for u in urls:
        with contextlib.redirect_stdout(io.StringIO()):
            try:
                aspirer.aspire(u, dest, frais=frais)
            except Exception:
                pass
        f = os.path.join(dest, hashlib.sha1(u.encode()).hexdigest()[:16] + ".txt")
        t = open(f, encoding="utf-8").read() if os.path.exists(f) else ""
        textes[u] = t if len(t) >= PLANCHER_PAGE else ""   # borne ⑥
    return textes

def serie(chemin):
    """les jetons du NOM DE LA SÉRIE, lus sur le chemin du document — « SERAFIN-PH », « ai-act »,
    « imac ». BORNE ⑦ : une veille qui porte son propre titre (« Veille SERAFIN-PH ») n'attribue
    rien à personne, et ses pages n'ont aucune raison de l'écrire. Lu sur le chemin, jamais en dur."""
    b = os.path.basename(chemin)
    b = re.sub(r"^\d{4}-\d{2}-\d{2}[_-]", "", b).rsplit(".", 1)[0]
    return set(j for j in sous_jetons(b.replace("veille", " ").replace("lecon", " "))
               if len(j) >= MIN_LETTRES)

def analyse(corps, urls, textes, chemin=""):
    """rend (interrogés, absents, ecartes_lexique, non_lues)."""
    lexique = minuscules(corps) | serie(chemin)
    for t in textes.values():
        lexique |= minuscules(t)
    cands = noms(corps)
    gardes = [n for n in cands if retenus(n, lexique)]
    absents = [n for n in gardes if not sur_page(n, textes)]
    non_lues = [u for u, t in textes.items() if not t]
    return gardes, absents, len(cands) - len(gardes), non_lues

# ─────────────────────────────────────────────────────────────────────────────────────────────
#  VERDICT
# ─────────────────────────────────────────────────────────────────────────────────────────────
def extrait(chemin):
    out = subprocess.run([sys.executable, os.path.join(RACINE, "outils", "scripts", "extract_docx.py"),
                          chemin], capture_output=True, text=True).stdout
    if "=== TEXTE COMPLET" not in out:
        sys.exit("EXTRACTION IMPOSSIBLE (fichier introuvable, illisible ou non zip) : %s" % chemin)
    urls = re.findall(r"^https?://\S+$", out.split("=== LIENS", 1)[0], re.M)
    return out.split("=== TEXTE COMPLET", 1)[-1], urls

def verdict(chemin, dest=None, frais=False):
    corps, urls = extrait(chemin)
    textes = pages_du_document(urls, dest=dest, frais=frais)
    gardes, absents, ecartes, non_lues = analyse(corps, urls, textes, chemin)
    nom = os.path.basename(chemin)
    if not gardes:
        print("  · %s : aucun nom propre interrogeable (%d écarté(s) aux bornes)" % (nom, ecartes))
        return 0
    print("  · %s : %d nom(s) interrogé(s) · %d écarté(s) aux bornes · %d/%d page(s) NON LUE(s)"
          % (nom, len(gardes), ecartes, len(non_lues), len(urls)))
    if not absents:
        print("    ✓ chaque nom figure sur au moins une page lue du document")
        return 0
    for n in absents:
        print("    ⚠️  NOM NON RETROUVÉ : « %s » ne figure sur AUCUNE des %d page(s) LUE(s)"
              % (n, len(urls) - len(non_lues)))
    if non_lues:
        # ⚠️ LE DÉCOMPTE DES PAGES NON LUES N'EST PAS DÉCORATIF : c'est la règle de ㉜ — une page
        #    non lue gonfle le motif, et un décompte d'absences sans le décompte des pages lues ne
        #    veut rien dire. Mesuré sur la veille SERAFIN-PH du 28/10 : 2 pages sur 4 sous le
        #    plancher, dont le mur anti-automate de `handicap.gouv.fr`, et quatre des noms
        #    « non retrouvés » de la série sont des parlementaires réels.
        print("    ⚠️  et %d page(s) n'a/ont PAS été lue(s) — une absence n'y est pas vérifiable :"
              % len(non_lues))
        for u in non_lues:
            print("         %s" % u)
    print("    ⛔ NON BLOQUANT — un nom propre faux ne se distingue d'une page non lue que par la\n"
          "       lecture ; en production un faux refus coûte un livrable non publié (règle du 14/10).")
    return 0

# ─────────────────────────────────────────────────────────────────────────────────────────────
#  AUTO-TESTS — aucun réseau, aucun tiers, rien de vivant dans le verdict
# ─────────────────────────────────────────────────────────────────────────────────────────────
def autotest():
    jouees, ko = [], []
    def borne(num, lib, cond):
        jouees.append(num)
        print("  %s %s" % ("✓" if cond else "✗", lib))
        if not cond:
            ko.append(num)

    INCIDENT = ("Les rapporteurs du Parlement européen, dont Lara Comi, Leonardo Benifei, "
                "Kim van Sparrentak et Sergey Lagodinsky, ont demandé le retrait.")
    n1 = noms(INCIDENT)
    borne(1, "l'incident du 30/10 est vu : « Lara Comi » ET « Leonardo Benifei » sont extraits",
          "Lara Comi" in n1 and "Leonardo Benifei" in n1)

    lex = minuscules(INCIDENT + " le texte van der visa de la de du des")
    borne(2, "ACCEPTÉE — « Kim van Sparrentak » est RETENU malgré « van » en minuscules au lexique",
          "van" in lex and retenus("Kim van Sparrentak", lex))

    borne(3, "un mot SEUL tout en capitales n'est jamais un nom — « ORANGE » ≠ « ORA » + « NGE »",
          noms("Niveau d'alerte : ORANGE — trois faits marquants.") == [])

    borne(4, "un nom ne se recolle pas par-dessus un saut de ligne (runs de `extract_docx.py`)",
          noms("Los Angeles\nCalendrier") == ["Los Angeles"])

    borne(5, "le lexique écarte deux cellules d'en-tête recollées — « Date Obligation »",
          not retenus("Date Obligation", minuscules("la date de l'obligation est fixée")))

    borne(6, "lexique DÉCOMPOSÉ : « d'alerte » met « alerte » au lexique, pas « dalerte »",
          "alerte" in minuscules("le niveau d'alerte est relevé")
          and not retenus("Alerte Critique", minuscules("le niveau d'alerte est critique")))

    borne(7, "⑨ un intitulé tout en capitales est écarté — « ALERTE CRITIQUE »",
          tout_capitales("ALERTE CRITIQUE") and not retenus("ALERTE CRITIQUE", set()))

    borne(8, "⑧ l'instrumentation est écartée — « Légifrance HTTP », « WebSearch CNIL »",
          not retenus("Légifrance HTTP", set()) and not retenus("WebSearch CNIL", set()))

    borne(9, "ACCEPTÉE — « Mozilla Developer Network » survit : la liste ⑧ n'écarte aucun vrai nom",
          retenus("Mozilla Developer Network", set()))

    borne(10, "un nom DANS un marqueur de correction ne rouvre pas le motif (leçon de la passe A, 25/10)",
           noms("Le rapporteur est Brando Benifei. [Corrigé le 31/10/2026 : « Leonardo Benifei » "
                "remplacé, la source écrit « Brando Benifei ».]") == ["Brando Benifei"])

    borne(11, "le 📝 Journal des corrections est hors du corps — il CONSERVE les libellés fautifs",
           noms("Le texte.\n📝 Journal des corrections\nLara Comi remplacé par Alex Agius Saliba.") == [])

    borne(12, "⑥ une page sous le plancher est NON LUE — elle n'accuse ni ne disculpe",
           sur_page("Camille Galliard-Minier", {"u": "x" * (PLANCHER_PAGE - 1)}) == []
           and PLANCHER_PAGE == 3000)

    borne(13, "degré ② : la page qui écrit « Galliard Minier » apparie « Galliard-Minier » du document",
           sur_page("Galliard-Minier", {"u": "la députée Galliard Minier a déposé"}) == ["u"])

    borne(14, "⑦ le nom de la SÉRIE est exempté — une veille qui porte son titre n'attribue rien",
           "serafin" in serie("sources/veille/serafin-ph/2026-10-28_veille_SERAFIN-PH.docx"))

    borne(15, "ACCEPTÉE — le sens conforme : un nom que la page écrit n'est PAS signalé",
           sur_page("Alex Agius Saliba", {"u": "a" * PLANCHER_PAGE + " Alex Agius Saliba"}) == ["u"])

    borne(16, "RACINE est la racine du dépôt, pas le dossier des scripts (bug du 23/10, reproduit)",
           os.path.isfile(os.path.join(RACINE, "outils", "scripts", "extract_docx.py")))

    # ── BORNES ⑰ et ⑱ : le VRAI `verdict()` joué de bout en bout — extraction, bornes, appariement,
    #    ligne imprimée — sur un `.docx` FABRIQUÉ en `tempfile` et une page FABRIQUÉE au cache.
    #    Rien de vivant dans le verdict (leçon du 22/10 : un témoin vivant périme tout seul et
    #    bloque alors TOUS les pushs du dépôt), aucun réseau : l'adresse est en `.invalid`, qui ne
    #    résout jamais PAR NORME (RFC 2606), et la page est déjà au cache, donc `aspirer.aspire()`
    #    rend sans sortir. Le motif étant NON BLOQUANT, c'est la LIGNE qui le garde, jamais le code
    #    de sortie — règle du dépôt.
    import tempfile, zipfile, hashlib, io, contextlib
    URL = "https://temoin.invalid/page"
    def docx_fabrique(d, texte):
        f = os.path.join(d, "temoin.docx")
        W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
        R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
        with zipfile.ZipFile(f, "w") as z:
            z.writestr("[Content_Types].xml",
                '<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/'
                'content-types"><Default Extension="xml" ContentType="application/xml"/>'
                '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats'
                '-officedocument.wordprocessingml.document.main+xml"/></Types>')
            z.writestr("word/document.xml",
                '<?xml version="1.0"?><w:document xmlns:w="%s" xmlns:r="%s"><w:body><w:p><w:r>'
                '<w:t>%s</w:t></w:r></w:p></w:body></w:document>' % (W, R, texte))
            z.writestr("word/_rels/document.xml.rels",
                '<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/'
                'package/2006/relationships"><Relationship Id="rId1" Type="%s/hyperlink" '
                'Target="%s" TargetMode="External"/></Relationships>' % (R, URL))
        return f
    def joue(texte_page):
        with tempfile.TemporaryDirectory() as d:
            pg = os.path.join(d, "pages"); os.makedirs(pg)
            open(os.path.join(pg, hashlib.sha1(URL.encode()).hexdigest()[:16] + ".txt"),
                 "w", encoding="utf-8").write(texte_page)
            f = docx_fabrique(d, "Le rapporteur Lara Comi a saisi la commission.")
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                verdict(f, dest=pg)
            return buf.getvalue()
    # la page parle d'autre chose, en restant AU-DESSUS du plancher : le nom doit être signalé
    s17 = joue("rapport parlementaire " * 400)
    borne(17, "⑰ `verdict()` de bout en bout : la ligne « NOM NON RETROUVÉ » est IMPRIMÉE",
          "NOM NON RETROUVÉ : « Lara Comi »" in s17)
    # la MÊME fabrication, la page portant le nom : ACCEPTÉE, rien ne doit être signalé
    s18 = joue("rapport parlementaire " * 400 + " signé Lara Comi ")
    borne(18, "⑱ ACCEPTÉE — même document, page qui PORTE le nom : aucune ligne de signalement",
          "NOM NON RETROUVÉ" not in s18 and "figure sur au moins une page lue" in s18)

    # ⚠️ LE DÉNOMINATEUR EST COMPTÉ, JAMAIS ÉCRIT EN DUR : un lot amputé doit faire bouger le
    #    nombre que le harnais lit (26/10 — « ATTENDU_CB5 » et « ATTENDU_CA » laissaient tous
    #    deux passer un lot amputé parce que leur dénominateur ne bougeait pas).
    print("  %d/%d bornes du contrôle des noms propres" % (len(jouees) - len(ko), len(jouees)))
    return 1 if ko else 0

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--autotest" in sys.argv:
        sys.exit(autotest())
    if not args:
        sys.exit("usage : controle_noms_propres.py <document.docx>… [--frais] [--autotest]\n"
                 "        --frais : réaspire les pages au lieu de réutiliser le cache")
    s = 0
    for d in args:
        s |= verdict(d, frais="--frais" in sys.argv)
    sys.exit(s)
