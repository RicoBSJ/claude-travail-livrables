#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""aspirer.py — aspire une page vers le DISQUE et ne rend qu'un compte-rendu de trois lignes.

POURQUOI (15/10/2026). Les contrôles du dépôt aspirent 394 hôtes sans qu'une seule page
n'entre dans le contexte de Claude : ils ne rendent que des verdicts. Mais quand Claude
vérifie une citation « mot pour mot » à la main, il réouvre la page et son texte entre,
lui, dans le contexte — 600 000 à 900 000 caractères pour une fiche du Minor Planet
Center, 744 580 octets pour growingself.com. Mesure : une seule de ces pages vaut plus de
tokens que tout le reste d'une session.

Et ce n'est pas seulement cher, c'est MOINS FIABLE : les quatre quasi-fausses accusations
du 13 et 14/10/2026 — « left prefrontal » contre « left side of the prefrontal cortex »,
« neuf facteurs » contre « moins de 9 facteurs », « Acceptation » contre « outil
d'acceptation », « identify their type » contre « able to accurately predict » — viennent
toutes d'une lecture humaine d'un dump. Un appariement exact ne rate pas une casse.

Usage :  aspirer.py <url> [<url>…] [--dossier D] [--frais]
Rend, par page : code HTTP, code de sortie curl, octets bruts, caractères utiles, et les
deux chemins (texte aplati, brut). Le texte se cherche ensuite avec chercher.py.

La logique réseau est celle de controle_attributions.py, volontairement à l'identique :
même UA, trois essais (0 s, 5 s, 15 s), hors 2xx = page NON LUE (⑰, ㉑), plancher de
façade à 3 000 caractères utiles, PDF non analysé.
"""
import hashlib, html, os, re, subprocess, sys, time, unicodedata
try:
    import ca_bundle
    CA = ca_bundle.args_curl()      # ⚠️ 18/10/2026, voir ca/README.md : chaîne complète, rien n'est désactivé
except Exception:
    CA = []

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
      " (KHTML, like Gecko) Chrome/126 Safari/537.36")

def dossier_defaut():
    # le scratchpad de la session si on le connaît, sinon un cache local gitignoré
    s = os.environ.get("CLAUDE_SCRATCHPAD") or os.environ.get("TMPDIR") or "/tmp"
    return os.path.join(s, "pages")

def aplati(raw):
    r = re.sub(r"<(script|style).*?</\1>", "", raw, flags=re.S)
    r = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", r)))
    return re.sub(r"\[\s*\d+\s*\]", " ", r)          # appels de note Wikipedia

def aspire(u, dest, frais=False):
    nom = hashlib.sha1(u.encode()).hexdigest()[:16]
    ftxt, fbrut = os.path.join(dest, nom + ".txt"), os.path.join(dest, nom + ".brut")
    if os.path.exists(ftxt) and not frais:
        n = len(open(ftxt, encoding="utf-8").read())
        print("  ♻ %s\n     déjà aspirée · %d car. utiles · %s" % (u, n, ftxt))
        return
    brut, essais, code, rc = b"", 0, "000", 0
    for attente in (0, 5, 15):
        if attente:
            time.sleep(attente)
        essais += 1
        tmp = os.path.join(dest, nom + ".tmp")
        rep = subprocess.run(["curl", "-s", "-L", "--max-time", "30", "-o", tmp,
                              "-w", "%{http_code}"] + CA + ["-A", UA, u],
                             capture_output=True, text=True)
        code, rc = rep.stdout.strip()[-3:], rep.returncode
        try:
            brut = open(tmp, "rb").read()
        except FileNotFoundError:
            brut = b""
        if not code.startswith("2"):
            brut = b""                               # un corps d'erreur n'est pas la page
        if brut:
            break
    for t in (os.path.join(dest, nom + ".tmp"),):
        if os.path.exists(t):
            os.remove(t)
    if not brut:
        print("  ✗ %s\n     HTTP %s · curl %d · %d essais · NON LUE : rien ne sera conclu "
              "d'elle (⑰, ㉑)" % (u, code, rc, essais))
        return
    if brut[:4] == b"%PDF" or u.lower().endswith(".pdf"):
        open(fbrut, "wb").write(brut)
        print("  ⚠ %s\n     PDF, %d octets · NON APLATI, vérification à la main · %s"
              % (u, len(brut), fbrut))
        return
    raw = brut.decode("utf-8", "replace")
    txt = unicodedata.normalize("NFC", aplati(raw))
    open(ftxt, "w", encoding="utf-8").write(txt)
    open(fbrut, "w", encoding="utf-8").write(raw)
    facade = "  ⚠ SOUS 3000 : façade, ou page rendue en JS ? regarde le brut" if len(txt) < 3000 else ""
    print("  ✓ %s\n     HTTP %s · %d octets bruts · %d car. utiles%s\n     %s"
          % (u, code, len(brut), len(txt), facade, ftxt))

if __name__ == "__main__":
    args = [a for a in sys.argv[1:]]
    frais = "--frais" in args
    args = [a for a in args if a != "--frais"]
    dest = dossier_defaut()
    if "--dossier" in args:
        i = args.index("--dossier")
        dest = args[i + 1]
        args = args[:i] + args[i + 2:]
    if not args:
        sys.exit(__doc__)
    os.makedirs(dest, exist_ok=True)
    for u in args:
        aspire(u, dest, frais)
