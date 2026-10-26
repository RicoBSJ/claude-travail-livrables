#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ca_bundle.py — rend le chemin d'un bundle de certificats complet, ou None.

POURQUOI (18/10/2026). Le `curl` d'Apple (`/usr/bin/curl`, LibreSSL/SecureTransport) lit
`/etc/ssl/cert.pem` : 128 certificats, daté du 16/08/2025, SANS la racine
« Sectigo Public Server Authentication Root R46 ». Et `has-sante.fr`, dont le certificat a
ete reemis le 08/10/2026, N'ENVOIE PAS sa chaine intermediaire. Il manquait donc les DEUX
morceaux, et `curl` rendait 60 sur les 57 documents du depot qui citent la HAS.

ET CE N'ETAIT PAS UN CAS ISOLE (26/10/2026). `cnsa.fr` a le MEME defaut : certificat reemis
le 14/10/2026, chaine intermediaire absente, `curl` 60 sur les 38 documents du depot qui
citent la CNSA. Autre emetteur — « Sectigo Qualified Website Authentication CA R39 » et non
« Public Server Authentication CA OV R36 » — donc un SECOND maillon, et la racine R46 suffit
aux deux. Le module charge desormais TOUS les .pem de `ca/` : voir `intermediaires()`.

Ce module reconstruit un bundle = racines a jour de `brew ca-certificates` + les intermediaires
que les extensions AIA des certificats designent elles-memes, et le met en cache dans
`logs/` (gitignore). Rien n'est desactive : la chaine est validee ENTIEREMENT, jusqu'a une
racine publique. Voir `outils/scripts/ca/README.md` pour la mesure complete.

⚠️ LE MAGASIN DE CONFIANCE DU SYSTEME N'EST PAS TOUCHE. Ajouter une racine a une machine est
une decision de securite qui revient a son proprietaire. Si le bundle de brew est absent, ce
module rend None et l'appelant ne passe aucun --cacert : comportement d'avant, a l'identique.
"""
import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BREW = ("/usr/local/etc/ca-certificates/cert.pem",
        "/opt/homebrew/etc/ca-certificates/cert.pem")
CA_DIR = os.path.join(RACINE, "outils", "scripts", "ca")
CACHE = os.path.join(RACINE, "outils", "scripts", "logs", ".ca_bundle.pem")


def intermediaires():
    """Tous les .pem versionnes dans ca/, tries. Liste vide si le dossier manque.

    ⚠️ 26/10/2026 — CETTE FONCTION REMPLACE UN CHEMIN EN DUR. Jusqu'a ce jour le module
    ne connaissait QU'UN intermediaire, celui de la HAS ; deposer un second .pem dans ca/
    n'avait aucun effet et rien ne le disait. `cnsa.fr` a eu le meme defaut de chaine que
    `has-sante.fr`, avec un AUTRE emetteur (Sectigo Qualified Website Authentication CA R39,
    contre Public Server Authentication CA OV R36) : il a donc fallu un second maillon.
    """
    try:
        return sorted(os.path.join(CA_DIR, f) for f in os.listdir(CA_DIR)
                      if f.endswith(".pem"))
    except OSError:
        return []


def chemin():
    """Le bundle complet, reconstruit si besoin. None si on ne peut pas le batir."""
    base = next((b for b in BREW if os.path.exists(b)), None)
    inters = intermediaires()
    if not base or not inters:
        return None
    try:
        frais = (os.path.exists(CACHE)
                 and os.path.getmtime(CACHE) >= max(os.path.getmtime(f)
                                                    for f in [base] + inters))
        if not frais:
            os.makedirs(os.path.dirname(CACHE), exist_ok=True)
            with open(CACHE, "w", encoding="utf-8") as out:
                for f in [base] + inters:
                    out.write(open(f, encoding="utf-8", errors="replace").read())
                    out.write("\n")
        return CACHE
    except OSError:
        return None


def args_curl():
    """Les arguments a inserer dans une commande curl : ['--cacert', chemin] ou []."""
    c = chemin()
    return ["--cacert", c] if c else []


def _compte(f):
    return open(f, encoding="utf-8", errors="replace").read().count("BEGIN CERTIFICATE")


def _autotest():
    """Bornes HORS RESEAU. Le defaut qu'elles gardent : un .pem depose dans ca/ et jamais
    charge — c'est ce que faisait le chemin en dur d'avant le 26/10/2026."""
    import tempfile
    # ⚠️ 26/10/2026 — LE DENOMINATEUR ETAIT EN DUR, DONC LE GARDE DU HARNAIS ETAIT DECORATIF.
    #    Un numerateur « bornes moins echecs » sur un denominateur fixe ne bouge pas quand on
    #    RETIRE une borne : le lot pouvait etre ampute et ATTENDU_CA restait satisfait. Mesure
    #    du 26/10 : sabotage pose, harnais en exit 0. Le denominateur est desormais le nombre de
    #    bornes jouees, et le harnais le lit. Meme correctif que non_regression/faisceau_5bis.py.
    ko, jouees = [], []

    def borne(nom, ok, detail=""):
        print("  %s %s%s" % ("✓" if ok else "✗", nom, (" — " + detail) if detail else ""))
        jouees.append(nom)
        if not ok:
            ko.append(nom)

    c = chemin()
    borne("① chemin() rend un fichier existant", bool(c) and os.path.exists(c), str(c))

    inters = intermediaires()
    borne("② ca/ porte au moins un intermediaire", len(inters) >= 1,
          "%d : %s" % (len(inters), ", ".join(os.path.basename(i) for i in inters)))

    base = next((b for b in BREW if os.path.exists(b)), None)
    if c and base:
        attendu = _compte(base) + sum(_compte(i) for i in inters)
        borne("③ le compte du faisceau = brew + TOUS les .pem de ca/", _compte(c) == attendu,
              "%d mesure, %d attendu" % (_compte(c), attendu))
        blob = open(c, encoding="utf-8", errors="replace").read()
        manquants = [os.path.basename(i) for i in inters
                     if not all(b.strip() in blob for b in
                                open(i, encoding="utf-8", errors="replace").read()
                                .split("-----END CERTIFICATE-----")[:-1])]
        borne("④ chaque .pem de ca/ est DANS le faisceau", not manquants,
              "absents : %s" % ", ".join(manquants) if manquants else "aucun absent")

    # ⑤ et ⑥ exercent le VRAI intermediaires() en deplacant CA_DIR (pas une copie de sa logique)
    global CA_DIR
    vrai = CA_DIR
    try:
        d = tempfile.mkdtemp()
        open(os.path.join(d, "b.pem"), "w").write("x")
        open(os.path.join(d, "a.pem"), "w").write("x")
        open(os.path.join(d, "note.txt"), "w").write("x")
        CA_DIR = d
        vus = [os.path.basename(p) for p in intermediaires()]
        borne("⑤ seuls les .pem sont pris, et tries", vus == ["a.pem", "b.pem"], str(vus))
        CA_DIR = os.path.join(d, "absent")
        borne("⑥ dossier ca/ absent -> aucun intermediaire (repli d'avant le faisceau)",
              intermediaires() == [], str(intermediaires()))
    finally:
        CA_DIR = vrai

    print("  %d/%d bornes du faisceau de certificats"
          % (len(jouees) - len(ko), len(jouees)))
    return 1 if ko else 0


if __name__ == "__main__":
    if "--autotest" in sys.argv:
        raise SystemExit(_autotest())
    c = chemin()
    if not c:
        raise SystemExit("aucun bundle reconstructible (brew ca-certificates absent ?)")
    print("%s — %d certificats" % (c, _compte(c)))
    for i in intermediaires():
        print("  + %s (%d)" % (os.path.basename(i), _compte(i)))
