#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ca_bundle.py — rend le chemin d'un bundle de certificats complet, ou None.

POURQUOI (18/10/2026). Le `curl` d'Apple (`/usr/bin/curl`, LibreSSL/SecureTransport) lit
`/etc/ssl/cert.pem` : 128 certificats, daté du 16/08/2025, SANS la racine
« Sectigo Public Server Authentication Root R46 ». Et `has-sante.fr`, dont le certificat a
ete reemis le 08/10/2026, N'ENVOIE PAS sa chaine intermediaire. Il manquait donc les DEUX
morceaux, et `curl` rendait 60 sur les 57 documents du depot qui citent la HAS.

Ce module reconstruit un bundle = racines a jour de `brew ca-certificates` + l'intermediaire
que l'extension AIA du certificat de la HAS designe elle-meme, et le met en cache dans
`logs/` (gitignore). Rien n'est desactive : la chaine est validee ENTIEREMENT, jusqu'a une
racine publique. Voir `outils/scripts/ca/README.md` pour la mesure complete.

⚠️ LE MAGASIN DE CONFIANCE DU SYSTEME N'EST PAS TOUCHE. Ajouter une racine a une machine est
une decision de securite qui revient a son proprietaire. Si le bundle de brew est absent, ce
module rend None et l'appelant ne passe aucun --cacert : comportement d'avant, a l'identique.
"""
import os

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BREW = ("/usr/local/etc/ca-certificates/cert.pem",
        "/opt/homebrew/etc/ca-certificates/cert.pem")
INTER = os.path.join(RACINE, "outils", "scripts", "ca",
                     "sectigo-public-server-auth-ca-ov-r36.pem")
CACHE = os.path.join(RACINE, "outils", "scripts", "logs", ".ca_bundle.pem")


def chemin():
    """Le bundle complet, reconstruit si besoin. None si on ne peut pas le batir."""
    base = next((b for b in BREW if os.path.exists(b)), None)
    if not base or not os.path.exists(INTER):
        return None
    try:
        frais = (os.path.exists(CACHE)
                 and os.path.getmtime(CACHE) >= max(os.path.getmtime(base),
                                                    os.path.getmtime(INTER)))
        if not frais:
            os.makedirs(os.path.dirname(CACHE), exist_ok=True)
            with open(CACHE, "w", encoding="utf-8") as out:
                for f in (base, INTER):
                    out.write(open(f, encoding="utf-8", errors="replace").read())
                    out.write("\n")
        return CACHE
    except OSError:
        return None


def args_curl():
    """Les arguments a inserer dans une commande curl : ['--cacert', chemin] ou []."""
    c = chemin()
    return ["--cacert", c] if c else []


if __name__ == "__main__":
    c = chemin()
    if not c:
        raise SystemExit("aucun bundle reconstructible (brew ca-certificates absent ?)")
    n = open(c, encoding="utf-8", errors="replace").read().count("BEGIN CERTIFICATE")
    print("%s — %d certificats" % (c, n))
