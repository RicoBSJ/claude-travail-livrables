#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""chercher.py — cherche une citation, un chiffre ou une date dans des pages aspirées,
et quand elle est ABSENTE, dit CE QUE LA PAGE ÉCRIT À LA PLACE.

POURQUOI (15/10/2026). Quatre fois les 13 et 14/10/2026 une conclusion « ABSENT » tirée
d'une lecture à l'œil était fausse, et à chaque fois pour la même raison : la page écrivait
la chose AUTREMENT. « left prefrontal » / « left side of the prefrontal cortex » · « neuf
facteurs » / « moins de 9 facteurs » · « Acceptation » / « outil d'acceptation » ·
« identify their type » / « able to accurately predict ». Un outil qui rend « ABSENT » tout
court reproduit l'erreur ; celui-ci est tenu de montrer la plus longue suite de mots de la
requête qu'il a trouvée, avec son contexte. C'est la règle de méthode du 14/10 — chercher
la variante de graphie AVANT de conclure à l'absence — rendue mécanique.

Usage :  chercher.py "<texte cherché>" <page.txt> [<page.txt>…]
         chercher.py --fichier requetes.txt <page.txt>…      (une requête par ligne)

Quatre degrés, du plus fort au plus faible, et la sortie NOMME celui qui a répondu :
  ① LITTÉRAL     — à l'identique, ponctuation et casse comprises (espaces normalisés, NFC)
  ② GRAPHIE      — identique une fois accents, casse, ponctuation et espaces pliés.
                   Suffit pour « la source le dit », PAS pour une citation entre guillemets.
  ③ LOCALE       — nombre français retrouvé sous sa graphie anglaise. Bornes de ㉟
                   (11/10/2026) reprises telles quelles : le point n'est JAMAIS essayé
                   comme séparateur de milliers — il fabriquait deux faux appariements en
                   trois documents, la pire direction possible.
  ④ ABSENT       — et alors on imprime la plus longue suite de mots trouvée, en contexte.
"""
import os, re, sys, unicodedata

def nfc(s):
    return re.sub(r"[ \u00a0\u202f\t\r\n]+", " ", unicodedata.normalize("NFC", s)).strip()

def cle(s):                                  # cle_texte() de controle_attributions.py
    s = unicodedata.normalize("NFKD", s.lower())
    return re.sub(r"[^a-z0-9]+", "", "".join(c for c in s if not unicodedata.combining(c)))

def mots(s):
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.findall(r"[a-z0-9]+", s)

def variantes_locale(n):
    """㉟ : espace → virgule anglaise ou forme collée ; virgule ↔ point SAUF à 3 chiffres."""
    v = set()
    if re.search(r"[ \u00a0\u202f]", n):
        v.add(re.sub(r"[ \u00a0\u202f]", ",", n))
        v.add(re.sub(r"[ \u00a0\u202f]", "", n))
    m = re.fullmatch(r"(\d+),(\d+)", n.strip())
    if m and len(m.group(2)) != 3:           # « 1,234 » reste ambigu : on n'y touche pas
        v.add(m.group(1) + "." + m.group(2))
    m = re.fullmatch(r"(\d+)\.(\d+)", n.strip())
    if m and len(m.group(2)) != 3:
        v.add(m.group(1) + "," + m.group(2))
    return {x for x in v if x and x != n}

VIDES = {"the","a","an","of","to","in","on","and","or","is","are","was","were","for",
         "le","la","les","de","des","du","un","une","et","ou","est","sont","en","au",
         "aux","ce","cette","par","pour","que","qui","dans","sur","leur","their","its"}

def pleins(q):
    """Mots qui portent le sens : on ne juge pas une absence sur « the » ou « de »."""
    p = [w for w in q if len(w) >= 4 and w not in VIDES] or [w for w in q if w not in VIDES]
    return p or q

def grappe(q, p, texte, fenetre=25):
    """⚠ 15/10/2026 — LA CONTIGUÏTÉ EST LE MAUVAIS CRITÈRE, mesuré à l'écriture de ce
    script : « left prefrontal » contre « left SIDE OF THE prefrontal cortex » ne donne
    AUCUN couple de mots contigus, donc l'ancienne version rendait « 1 mot de suite » et
    n'imprimait aucun contexte — soit exactement l'erreur que ce script existe pour
    empêcher. Idem « neuf facteurs » / « moins de 9 facteurs » et « identify their type »
    / « their own dominant type ». Ce qu'on cherche, ce sont les mots PLEINS de la requête
    DISPERSÉS dans une fenêtre courte. Rend (nb de mots distincts trouvés, nb attendu,
    contexte)."""
    pl = pleins(q)
    cibles = set(pl)
    pos = sorted((i, w) for i, w in enumerate(p) if w in cibles)
    if not pos:
        return 0, len(pl), None
    best = (0, None)
    for a in range(len(pos)):
        vus, b = set(), a
        while b < len(pos) and pos[b][0] - pos[a][0] <= fenetre:
            vus.add(pos[b][1]); b += 1
        if len(vus) > best[0]:
            best = (len(vus), (pos[a][0], pos[b - 1][0]))
    n, (d, f) = best[0], best[1]
    # on retrouve la zone dans le texte d'origine en s'appuyant sur les mots eux-mêmes
    suite = [w for w in p[d:f + 1]]
    c = contexte(texte, suite[:1]) if len(suite) > 12 else contexte(texte, suite)
    return n, len(pl), c

def plus_longue_suite(q, p, texte):
    """Plus longue suite CONTIGUË de mots de q présente dans p. Rend (début_q, longueur)."""
    idx = {}
    for i, w in enumerate(p):
        idx.setdefault(w, []).append(i)
    best = (0, 0)
    for i in range(len(q)):
        for d in idx.get(q[i], ())[:400]:
            k = 0
            while i + k < len(q) and d + k < len(p) and q[i + k] == p[d + k]:
                k += 1
            if k > best[1]:
                best = (i, k)
    return best

def contexte(texte, suite):
    """Retrouve la suite de mots dans le texte d'origine et rend ±90 caractères."""
    m = re.search(r"\W+".join(re.escape(w) for w in suite), texte,
                  re.I | re.UNICODE)
    if not m:
        return None
    a, b = max(0, m.start() - 90), min(len(texte), m.end() + 90)
    return "…" + re.sub(r"\s+", " ", texte[a:b]).strip() + "…"

def borne_nombre(n, t):
    """⚠ Borne de controle_edition_precedente.py (12/10/2026), à ne JAMAIS perdre :
    « 1 338 » ne doit pas s'apparier à « 1 338,23 », ni « 447 » à « 447 812 ». Un
    simple `in` le fait, et c'est un faux appariement qui déclare présent un nombre
    absent — la pire direction. On exige donc que le nombre ne soit ni précédé ni
    suivi d'un chiffre ou d'une décimale."""
    # ⚠ LE « \\? » N'EST PAS DÉCORATIF. re.escape ÉCHAPPE L'ESPACE en Python 3.9.6
    # (l'interpréteur du dépôt) : re.escape("1 338,23") rend « 1\\ 338,23 ». Sans ce
    # \\?, la substitution insère la classe APRÈS l'antislash et produit « 1\\[ ]?338 »,
    # où \\[ est un crochet LITTÉRAL — on cherche alors une chaîne qui n'existe nulle
    # part. C'est mot pour mot le bug de la passe D réparé le 10/10/2026, reproduit ici
    # à l'écriture le 15/10/2026 : nombres réellement présents donnés pour absents.
    j = re.sub(r"\\?[ \u00a0\u202f]+", "[ \u00a0\u202f]?", re.escape(n))
    # et le lookahead doit refuser aussi un GROUPE DE MILLIERS qui suit : sans cela
    # « 447 » s'appariait à « 447 812 », mesuré le 15/10/2026 — le vrai nombre est 447 812.
    # ⚠ et une borne gauche de GROUPE DE MILLIERS, trouvée par l'auto-test le 15/10/2026 :
    # sans elle « 812 » s'appariait dans « 447 812 » et « 338 » dans « 1 338 ». Python
    # exige un lookbehind de largeur fixe, d'où « un chiffre + une espace » plutôt que
    # « un à trois chiffres ». Elle refuse aussi « 812 » dans « en 2026 812 cas » : c'est
    # une non-confirmation, pas une fausse accusation — la bonne direction d'erreur.
    return re.search(r"(?<![0-9A-Za-zÀ-ÿ.,])(?<![0-9][ \u00a0\u202f])" + j
                     + r"(?![0-9]|[.,][0-9]|[ \u00a0\u202f][0-9]{3}(?![0-9]))", t) is not None

def cherche(req, fichiers, muet=False):
    """Rend le DEGRÉ atteint (1 à 4). ⚠ 15/10/2026 : l'auto-test appelle CETTE fonction
    et non une copie de sa cascade — la première version en réimplémentait la logique,
    de sorte qu'un sabotage du vrai chemin n'était pas pris en défaut. Un test qui teste
    une copie ne garde rien. Défaut trouvé par le sabotage lui-même."""
    dis = (lambda *a: None) if muet else print
    req = nfc(req)
    qm, qk = mots(req), cle(req)
    dis("» %s" % req)
    meilleur = (-1, 0, None, None)
    for f in fichiers:
        try:
            t = nfc(open(f, encoding="utf-8").read())
        except OSError as e:
            dis("  ✗ %s : %s" % (f, e)); continue
        nom = os.path.basename(f)
        chiffre = bool(re.fullmatch(r"[\d ,.\u00a0\u202f%€$]+", req))
        if borne_nombre(req, t) if chiffre else (req in t):
            dis("  ① LITTÉRAL  %s" % nom); return 1
        # ⚠ 15/10/2026 : le degré ② est INTERDIT dès que la requête porte un chiffre.
        # Mesuré à l'écriture : « 1 338 » était déclaré présent par une page portant
        # « 1,338 », parce que cle() écrase la ponctuation — exactement le faux
        # appariement que ㉟ avait refusé le 11/10 (« 1 049 » trouvé dans le « 1.049 »
        # d'apple.com), et exactement la borne de CLAUDE.md « un jeton se cherche
        # ponctuation CONSERVÉE ». Pire : cle() concatène la page entière, donc un
        # nombre peut s'apparier à cheval sur deux nombres sans rapport. Un chiffre ne
        # passe donc que par ① (littéral) ou ③ (locale, aux bornes mesurées).
        if qk and not re.search(r"\d", req) and qk in cle(t):
            dis("  ② GRAPHIE   %s — présente aux accents/casse/ponctuation près" % nom)
            c = contexte(t, qm)
            if c: dis("     %s" % c)
            return 2
        for v in variantes_locale(req):
            if borne_nombre(v, t):
                dis("  ③ LOCALE    %s — la page écrit « %s »" % (nom, v)); return 3
        pm = mots(t)
        n, att, c = grappe(qm, pm, t)
        if n > meilleur[0] or meilleur[0] < 0:
            meilleur = (n, att, nom, c)
    n, att, nom, c = meilleur
    if n > 0 and c and (n >= 2 or att <= 2):
        dis("  ④ ABSENT LITTÉRALEMENT — mais %s porte %d de ses %d mot(s) pleins :"
            % (nom, n, att))
        dis("     %s" % c)
        dis("     ⚠ VARIANTE DE GRAPHIE PROBABLE : relis CE TEXTE avant de conclure"
            " à l'absence (règle du 14/10/2026)")
    else:
        dis("  ④ ABSENT    — aucune page ne porte plus de %d de ses %d mot(s) pleins"
            % (n, att))
    return 4

CAS = [
    # (requête, texte, degré attendu, pourquoi cette borne existe)
    ("left prefrontal", "activity in the left side of the prefrontal cortex fell", 4,
     "incident 13/10 : l'absence littérale doit MONTRER la variante"),
    ("neuf facteurs", "a model with moins de 9 facteurs fits best", 4,
     "incident 14/10 : mots dispersés, contiguïté inopérante"),
    ("identify their type", "not able to accurately predict their own dominant type", 4,
     "incident 14/10 : trois mots, aucun couple contigu"),
    ("Acceptation", "est avant tout un outil d'acceptation de soi", 2,
     "incident 14/10 : la casse seule ne fait pas une absence"),
    ("1 338", "le montant est de 1 338,23 euros", 4,
     "borne 12/10 : un jeton se cherche ponctuation CONSERVÉE"),
    ("447", "et 447 812 tests au total", 4,
     "borne 15/10 : un groupe de milliers qui suit interdit l'appariement"),
    ("1 338,23", "le montant est de 1 338,23 euros", 1,
     "SENS ACCEPTANT du bug re.escape : un nombre présent doit passer"),
    ("447 812", "et 447 812 tests au total", 1,
     "SENS ACCEPTANT : idem, c'est le \\? qui le rend possible"),
    ("50,4", "la periode est de 50.4 ans", 3,
     "㉟ 11/10 : decimale virgule <-> point hors trois chiffres"),
    ("54 000", "Total: 54,000 units", 3,
     "㉟ : espace -> virgule anglaise, forme francaise sans ambiguite"),
    ("1 049", "prix de 1.049 euros", 4,
     "㉟ : LE POINT N'EST JAMAIS UN SEPARATEUR DE MILLIERS - faux appariement refuse"),
    ("7 918", "la valeur doi 7.918 du journal", 4,
     "㉟ : second faux appariement mesure le 11/10 (doi.org)"),
    ("1,234", "le total de 1.234 unites", 4,
     "㉟ : trois chiffres = seul cas reellement ambigu, on n'y touche pas"),
    ("338", "le montant est de 1 338,23 euros", 4,
     "borne GAUCHE, trou révélé par le sabotage du 15/10 : « 338 » n'est pas « 1 338 »"),
    ("812", "et 447 812 tests au total", 4,
     "borne GAUCHE : « 812 » n'est pas le nombre « 447 812 »"),
    ("338", "le code article est A1338 du catalogue", 4,
     "borne gauche collée, trou révélé par le sabotage : « 338 » n'est pas dans « A1338 »"),
    ("049", "le prix affiche 1.049 euros", 4,
     "borne gauche décimale : « 049 » n'est pas la décimale de « 1.049 »"),
    ("left prefrontal", "the left hemisphere was imaged. " + "filler word here. " * 60
     + "the prefrontal cortex showed no change", 4,
     "fenêtre de grappe : deux mots à 180 mots d'écart ne font pas une variante"),
    ("La publication du guide est prevue", "La publication du guide est prevue au troisieme trimestre", 1,
     "cas de ma propre fiche du 05/10 : le litteral doit etre vu"),
]

def autotest():
    """Les bornes mesurées, rejouées sur le vrai chemin. Aucun appel réseau, 0,1 s."""
    import tempfile
    ko = 0
    for req, txt, attendu, pourquoi in CAS:
        with tempfile.NamedTemporaryFile("w", suffix=".txt", encoding="utf-8",
                                         delete=False) as fh:
            fh.write(txt); p = fh.name
        obtenu = cherche(req, [p], muet=True)
        os.remove(p)
        if obtenu == attendu:
            print("  ✓ degré %d  « %s »" % (obtenu, req))
        else:
            ko += 1
            print("  ✗ « %s » : degré %d attendu, %d obtenu — %s"
                  % (req, attendu, obtenu, pourquoi))
    manquants = 0
    for req, txt, attendu, _ in CAS:
        if attendu != 4 or re.search(r"\d", req):
            continue
        n, att, c = grappe(mots(nfc(req)), mots(nfc(txt)), nfc(txt))
        if not (n > 0 and c):
            manquants += 1
            print("  ✗ « %s » : ABSENT sans montrer la variante" % req)
    # ⚠ la FENÊTRE de la grappe ne se prouve pas par un degré : deux mots de la requête
    # à 180 mots d'écart donnent « ABSENT » dans les deux cas. Ce qui change, c'est le
    # NOMBRE de mots trouvés. Assertion ajoutée le 15/10/2026 parce que le sabotage
    # « fenêtre portée à toute la page » passait les vingt autres tests.
    loin = ("the left hemisphere was imaged. " + "filler word here. " * 60
            + "the prefrontal cortex showed no change")
    n, att, _ = grappe(mots("left prefrontal"), mots(loin), nfc(loin))
    if n == 1:
        print("  \u2713 la fenêtre de grappe tient : 2 mots à 180 mots d'écart"
              " ne comptent pas pour une variante")
    else:
        ko += 1
        print("  \u2717 FENÊTRE DE GRAPPE PERDUE : %d mots appariés à 180 mots d'écart" % n)
    ko += manquants
    if not manquants:
        print("  ✓ les absences littérales montrent toutes leur variante")
    print("  %s %d/%d auto-tests de chercher.py — « ABSENT » sait dire pourquoi"
          % ("✓" if not ko else "✗", len(CAS) + 2 - ko, len(CAS) + 2))
    return 1 if ko else 0

if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "--autotest":
        sys.exit(autotest())
    if len(a) < 2:
        sys.exit(__doc__)
    if a[0] == "--fichier":
        reqs = [l for l in open(a[1], encoding="utf-8").read().splitlines() if l.strip()]
        pages = a[2:]
    else:
        reqs, pages = [a[0]], a[1:]
    ko = 0
    for r in reqs:
        ko += 1 if cherche(r, pages) == 4 else 0
    if len(reqs) > 1:
        print("— %d requête(s) · %d absente(s)" % (len(reqs), ko))
    sys.exit(1 if ko else 0)
