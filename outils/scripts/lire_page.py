#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lire_page.py — lire une FENÊTRE d'une page aspirée, jamais la page entière. (19/10/2026)

POURQUOI, ET C'EST UNE ERREUR MESURÉE DE MA PART. Le 18/10/2026 le prompt de `rbpp-pipeline` a
reçu la consigne « lis ce `.txt` (`sed -n`, `grep -n`) au lieu de WebFetch ». CETTE CONSIGNE EST
INAPPLICABLE : `aspirer.py` écrase tous les blancs (`re.sub(r"\\s+", " ", …)`), donc une page
aspirée est UNE SEULE LIGNE. Mesuré le 19/10 sur les pages du jour : 0 saut de ligne, et la ligne
unique fait 46 869 caractères pour le flux HAS-Actualité, 48 839 pour le flux Recommandations,
9 775 pour le calendrier, 11 859 pour l'appel CVS. `sed -n '1,50p'` rend donc le fichier ENTIER et
`grep -n` imprime la ligne ENTIÈRE : la consigne garantissait exactement ce qu'elle voulait éviter.
Conséquence mesurée au créneau suivant : le job est passé de 2,3661 $ (59 % du plafond) à
3,7351 $ (93 %), de 47 à 72 tours, avec 2,4 fois plus de cache lu.

CE QUE CET OUTIL REND, ET SA BORNE EST STRUCTURELLE. Deux modes, et dans les deux la sortie est
bornée PAR CONSTRUCTION — au plus MAX_OCC fenêtres de 2×FENETRE caractères, plus une ligne de
total. Le reste de la page ne peut pas entrer en contexte, même par accident.

  lire_page.py --autour "<motif>" <page.txt>…        → les occurrences du motif, en contexte
  lire_page.py --items <flux.brut>… [--depuis JJ/MM/AAAA]  → date · titre · lien, un par ligne
  lire_page.py --autotest                           → les bornes, rejouées. Aucun réseau.

Options : --fenetre N (défaut 300) · --max N (défaut 6)

⚠️ CE N'EST PAS `chercher.py`, ET LES DEUX NE SE REMPLACENT PAS. `chercher.py` répond « cette
citation est-elle sur la page, et à quel degré » : il VÉRIFIE une chaîne connue. Celui-ci répond
« que dit la page autour de cet endroit » : il DÉCOUVRE. Un « 0 occurrence » ici ne prouve pas une
absence — la page peut l'écrire autrement, et c'est `chercher.py` qui tranche (règle du 14/10 :
chercher la variante de graphie AVANT de conclure à l'absence). La sortie le dit.

⚠️ ET LE MODE --items LIT LE `.brut`, PAS LE `.txt` : un flux RSS a sa structure dans ses balises,
et l'aspiration les retire. Mesuré le 19/10 : sur le flux Recommandations, les 50 `<item>` rendent
4 entrées d'octobre 2026 — soit quelques centaines de caractères au lieu de 48 839.
"""
import html
import os
import re
import sys
import unicodedata

FENETRE = 300          # caractères de contexte de chaque côté
MAX_OCC = 6            # occurrences imprimées au plus — le total, lui, est toujours dit
MAX_ITEMS = 40         # entrées de flux imprimées au plus


def plie(s):
    """casse et accents pliés, blancs normalisés — pour LOCALISER, pas pour afficher"""
    z = unicodedata.normalize("NFKD", s.lower())
    z = "".join(c for c in z if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", z)


def autour(motif, chemins, fenetre=FENETRE, maxi=MAX_OCC):
    """les occurrences du motif, en contexte, BORNÉES. Rend le nombre d'occurrences trouvées."""
    total = 0
    for p in chemins:
        if not os.path.exists(p):
            print("  ✗ %s : fichier introuvable" % p)
            continue
        brut = open(p, encoding="utf-8", errors="replace").read()
        plat = re.sub(r"\s+", " ", brut)
        cible = plie(plat)
        m = plie(motif)
        if not m:
            print("  ✗ motif vide")
            continue
        pos = [i for i in range(len(cible)) if cible.startswith(m, i)]
        print("» %s — %d occurrence(s) de « %s » sur %d caractères"
              % (os.path.basename(p), len(pos), motif, len(plat)))
        if not pos:
            print("   AUCUNE — la page peut l'écrire autrement : c'est chercher.py qui tranche"
                  " (variante de graphie, règle du 14/10/2026)")
        for i in pos[:maxi]:
            a, b = max(0, i - fenetre), min(len(plat), i + len(m) + fenetre)
            print("   …%s…" % plat[a:b].strip())
        if len(pos) > maxi:
            print("   (%d occurrence(s) de plus, non imprimée(s) — resserre le motif)"
                  % (len(pos) - maxi))
        total += len(pos)
    return total


def items(chemins, depuis=None, maxi=MAX_ITEMS):
    """les entrées d'un flux, lues dans le `.brut` : date · titre · lien. Rend le nombre imprimé."""
    from email.utils import parsedate_to_datetime
    imprimes = 0
    for p in chemins:
        if not os.path.exists(p):
            print("  ✗ %s : fichier introuvable" % p)
            continue
        brut = open(p, encoding="utf-8", errors="replace").read()
        entrees = re.findall(r"<item>(.*?)</item>", brut, re.S)
        gardees = []
        for it in entrees:
            def champ(nom):
                mm = re.search(r"<%s>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</%s>" % (nom, nom), it, re.S)
                return re.sub(r"\s+", " ", html.unescape(mm.group(1))).strip() if mm else ""
            d_, t_, l_ = champ("pubDate"), champ("title"), champ("link")
            dt = None
            if d_:
                try:
                    dt = parsedate_to_datetime(d_)
                except Exception:
                    dt = None
            if depuis and dt and dt.date() < depuis:
                continue
            gardees.append((dt.strftime("%d/%m/%Y") if dt else (d_[:16] or "?"), t_, l_))
        print("» %s — %d entrée(s)%s sur %d dans le flux"
              % (os.path.basename(p), len(gardees),
                 (" depuis le %s" % depuis.strftime("%d/%m/%Y")) if depuis else "", len(entrees)))
        for d_, t_, l_ in gardees[:maxi]:
            print("   %s · %s%s" % (d_, t_[:120], ("\n              " + l_) if l_ else ""))
            imprimes += 1
        if len(gardees) > maxi:
            print("   (%d entrée(s) de plus — resserre --depuis)" % (len(gardees) - maxi))
    return imprimes


# ── les bornes, rejouées sur le vrai chemin ──────────────────────────────────
PAGE = ("Veille HAS. " + "remplissage " * 400
        + "Date de clôture de l'appel à candidatures : 26/10/2026 (inclus). "
        + "bourrage " * 400 + "Date de clôture de l'appel à candidatures : 13/11/2026 (inclus). "
        + "queue " * 400)
FLUX = ("<rss><channel>"
        "<item><title><![CDATA[Note de cadrage — SAAD Familles]]></title>"
        "<pubDate>Thu, 8 Oct 2026 10:00:00 +0200</pubDate>"
        "<link>https://exemple.fr/a</link></item>"
        "<item><title>Guide pharmaceutique</title>"
        "<pubDate>Mon, 12 Oct 2026 09:00:00 +0200</pubDate>"
        "<link>https://exemple.fr/b</link></item>"
        "<item><title>Vieux document</title>"
        "<pubDate>Tue, 2 Jun 2026 09:00:00 +0200</pubDate>"
        "<link>https://exemple.fr/c</link></item>"
        "</channel></rss>")


def autotest():
    """Les bornes mesurées, rejouées sur le vrai chemin. Aucun appel réseau."""
    import datetime
    import io
    import tempfile
    ko = 0

    def capture(fn, *a, **k):
        vieux, tampon = sys.stdout, io.StringIO()
        sys.stdout = tampon
        try:
            r = fn(*a, **k)
        finally:
            sys.stdout = vieux
        return r, tampon.getvalue()

    def ecrire(txt, suf):
        with tempfile.NamedTemporaryFile("w", suffix=suf, encoding="utf-8", delete=False) as fh:
            fh.write(txt)
            return fh.name

    ptxt, pflux = ecrire(PAGE, ".txt"), ecrire(FLUX, ".brut")
    try:
        # ① LA BORNE QUI JUSTIFIE L'OUTIL : la sortie est STRICTEMENT plus petite que la page.
        n, out = capture(autour, "Date de clôture", [ptxt])
        if n == 2 and len(out) < len(PAGE) / 3:
            print("  ✓ 2 occurrences trouvées, sortie de %d caractères pour une page de %d"
                  % (len(out), len(PAGE)))
        else:
            ko += 1
            print("  ✗ borne de taille perdue : %d occurrence(s), sortie %d / page %d"
                  % (n, len(out), len(PAGE)))
        # ② le contexte contient bien la valeur cherchée, pas seulement le motif
        if "26/10/2026" in out and "13/11/2026" in out:
            print("  ✓ les deux dates de clôture sont dans les fenêtres rendues")
        else:
            ko += 1
            print("  ✗ une fenêtre ne porte pas sa valeur — FENETRE trop courte ?")
        # ③ casse et accents pliés pour localiser
        n3, _ = capture(autour, "DATE DE CLOTURE", [ptxt])
        if n3 == 2:
            print("  ✓ casse et accents pliés : « DATE DE CLOTURE » trouve « Date de clôture »")
        else:
            ko += 1
            print("  ✗ pliage perdu : %d occurrence(s) au lieu de 2" % n3)
        # ④ une absence ne se conclut pas ici, et la sortie le DIT
        n4, out4 = capture(autour, "surdicécité", [ptxt])
        if n4 == 0 and "chercher.py" in out4:
            print("  ✓ 0 occurrence renvoie à chercher.py — une absence ne se conclut pas ici")
        else:
            ko += 1
            print("  ✗ un « 0 occurrence » muet laisserait conclure à une absence")
        # ⑤ LE PLAFOND D'OCCURRENCES TIENT, ET IL ANNONCE SON RESTE.
        #    ⚠️ Première version de cette borne, le 19/10 : elle ne vérifiait que « de plus »
        #    dans la sortie. SABOTAGE MESURÉ LE MÊME JOUR — remplacer `pos[:maxi]` par `pos`
        #    imprimait les 400 fenêtres et l'auto-test restait VERT, parce que la mention
        #    « de plus » dépend de len(pos) > maxi, pas du nombre réellement imprimé, et que
        #    la borne ① se jouait sur un motif à 2 occurrences où le plafond n'engageait pas.
        #    On compte donc les FENÊTRES IMPRIMÉES. Un mutant qui ne mord pas ne prouve rien.
        n5, out5 = capture(autour, "remplissage", [ptxt], maxi=2)
        fenetres = sum(1 for l in out5.splitlines() if l.lstrip().startswith("…"))
        if n5 == 400 and fenetres == 2 and "de plus" in out5:
            print("  ✓ 400 occurrences, EXACTEMENT 2 fenêtres imprimées, et le reste est ANNONCÉ")
        else:
            ko += 1
            print("  ✗ plafond d'occurrences perdu : %d trouvée(s), %d fenêtre(s) imprimée(s)"
                  " pour 2 attendues, reste annoncé : %s" % (n5, fenetres, "de plus" in out5))
        # ⑥ --items lit les balises : CDATA, dates, liens
        n6, out6 = capture(items, [pflux])
        if n6 == 3 and "SAAD Familles" in out6 and "08/10/2026" in out6:
            print("  ✓ 3 entrées lues dans le .brut, CDATA et pubDate comprises")
        else:
            ko += 1
            print("  ✗ lecture du flux perdue : %d entrée(s)" % n6)
        # ⑦ --depuis filtre, et c'est lui qui remplace la lecture du flux entier
        n7, out7 = capture(items, [pflux], depuis=datetime.date(2026, 10, 1))
        if n7 == 2 and "Vieux document" not in out7:
            print("  ✓ --depuis 01/10/2026 garde 2 entrées sur 3 et écarte la plus ancienne")
        else:
            ko += 1
            print("  ✗ --depuis ne filtre plus : %d entrée(s)" % n7)
    finally:
        for f in (ptxt, pflux):
            os.remove(f)
    print("  %s %d/7 bornes de lire_page.py — une page aspirée n'entre jamais entière"
          % ("✓" if not ko else "✗", 7 - ko))
    return 1 if ko else 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    if a[0] == "--autotest":
        sys.exit(autotest())
    fen, mx, depuis = FENETRE, MAX_OCC, None
    for opt, conv in (("--fenetre", int), ("--max", int), ("--depuis", str)):
        if opt in a:
            i = a.index(opt)
            v = conv(a[i + 1])
            a = a[:i] + a[i + 2:]
            if opt == "--fenetre":
                fen = v
            elif opt == "--max":
                mx = v
            else:
                import datetime
                j, m_, an = (int(x) for x in v.split("/"))
                depuis = datetime.date(an, m_, j)
    if a[0] == "--items":
        sys.exit(0 if items(a[1:], depuis) is not None else 1)
    if a[0] == "--autour":
        if len(a) < 3:
            sys.exit("usage : lire_page.py --autour \"<motif>\" <page.txt>…")
        autour(a[1], a[2:], fen, mx)
        sys.exit(0)
    sys.exit(__doc__)
