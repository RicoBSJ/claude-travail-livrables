#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""balayer_adresses.py — LES ADRESSES CITÉES PAR LES LIVRABLES RÉPONDENT-ELLES ENCORE ?

Écrit le 25/10/2026, après la panne de `promenade.imcce.fr` : un lien cité par un livrable publié
peut mourir sans que rien ne le dise. Les contrôles du dépôt n'ouvrent les pages QUE du document
qu'on leur donne, et le harnais ne regarde que les documents d'un push — donc **personne ne relit
un livrable que personne n'a touché**. Ce script comble ce trou, et lui seul.

    balayer_adresses.py [--sortie <tsv>] [--limite N] [--essais N]
    balayer_adresses.py --autotest        # la classification, aucun réseau

⛔ JAMAIS EN PARALLÈLE — règle du 12/10/2026, payée deux fois : `has-sante.fr`, `wikipedia.org` et
`classics.mit.edu` limitent le débit, et 11 contrôles simultanés ont fait basculer 4 documents sains
en « bloquant ». Le balayage est donc **strictement séquentiel**, et il ordonne les adresses en
TOURNIQUET PAR HÔTE : deux requêtes consécutives ne touchent jamais le même serveur, ce qui espace
les 106 adresses de `has-sante.fr` sans allonger le total.

⛔ ET UN SEUL ESSAI NE CONDAMNE PAS UNE PAGE — même règle : tout code non concluant est rejoué,
seul, après un délai. Les essais 2 et 3 sont groupés à la fin pour que l'intervalle soit réel.

Le faisceau de certificats est obligatoire : sans lui, toute page `has-sante.fr` rend 000 (18/10).
Jamais `-k`, jamais `--insecure`.

LA CLASSIFICATION EST LE CŒUR, et elle refuse de confondre quatre choses :
  🔴 MORTE      404, 410       — le lien est cassé : c'est le seul verdict qui demande une correction
  🟠 INJOIGNABLE 000           — DNS, TLS ou délai dépassé : le cas de l'IMCCE
  🟡 PANNE      5xx            — le serveur est en peine, souvent passagère
  🔵 REFUS      401, 403, 429  — un automate est écarté ; la page existe pour un humain
  🟢 VIVANTE    2xx            — après redirections
"""
import html, os, re, subprocess, sys, time, zipfile
from collections import defaultdict

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126 Safari/537.36")
PAUSE, MAX_TIME, ENTRE_ESSAIS = 0.25, 20, 20


# 🔴 25/10/2026 — UN « 000 » CACHE QUATRE SITUATIONS, ET DEUX PEUVENT ÊTRE DE NOTRE CÔTÉ.
#    Mesuré sur quatre des vingt injoignables du premier balayage, faisceau compris :
#      www.entretienmotivationnel.org  exit 60  — certificat non authentifiable (7 documents)
#      www.service-public.gouv.fr      exit 35  — erreur de connexion TLS
#      media4.obspm.fr                 exit 28  — délai dépassé (la panne de l'Observatoire)
#      www.davidstamile.com            exit  6  — hôte non résolu : le site a disparu
#    Les classer tous « INJOIGNABLE » revenait à écrire en face d'une page vivante qu'elle est morte
#    — le piège du 18/10, où `has-sante.fr` rendait 000 PAR DÉFAUT DE FAISCEAU. Le code de sortie de
#    curl est donc relevé, et « TLS » ne dit JAMAIS qu'une page est morte.
SORTIES_TLS = (35, 51, 58, 59, 60, 77, 83)


def classe(code, rc=0):
    """(code HTTP, code de sortie curl) → un verdict qui ne confond pas ces situations."""
    if code in ("404", "410"):
        return "MORTE"
    if code in ("", "000"):
        if rc == 6:
            return "DNS"          # l'hôte ne résout plus : le site a disparu
        if rc in SORTIES_TLS:
            return "TLS"          # peut être NOTRE pile : n'en jamais conclure que la page est morte
        if rc == 28:
            return "DELAI"        # le serveur ne répond pas — panne, souvent passagère
        if rc == 7:
            return "CONNEXION"
        return "INJOIGNABLE"
    if code in ("401", "403", "429"):
        return "REFUS"
    if code[:1] == "5":
        return "PANNE"
    if code[:1] in ("2", "3"):
        return "VIVANTE"
    return "AUTRE"


CONCLUANT = ("VIVANTE", "MORTE", "REFUS")   # on ne rejoue que ce qui peut être passager


def faisceau():
    try:
        sys.path.insert(0, os.path.join(RACINE, "outils", "scripts"))
        import ca_bundle
        return ca_bundle.chemin()
    except Exception:
        return None


def adresses(seulement=None):
    """{adresse : [documents qui la citent]} — lues dans les rels, comme le font les contrôles."""
    par = defaultdict(set)
    for base in ("livrables/lecons", "sources/veille"):
        for r, _, f in os.walk(os.path.join(RACINE, base)):
            for n in sorted(f):
                if not n.endswith(".docx"):
                    continue
                try:
                    rels = zipfile.ZipFile(os.path.join(r, n)).read(
                        "word/_rels/document.xml.rels").decode("utf-8", "ignore")
                except Exception:
                    continue
                for m in re.finditer(r'Target="(https?://[^"]+)"', rels):
                    par[html.unescape(m.group(1))].add(n)
    if seulement:
        garde = {l.strip() for l in open(seulement, encoding="utf-8") if l.strip()}
        absentes = garde - set(par)
        par = {u: v for u, v in par.items() if u in garde}
        if absentes:
            print("⚠️ %d adresse(s) de la liste ne sont plus citées par aucun document" % len(absentes))
    return {u: sorted(v) for u, v in par.items()}


def tourniquet(urls):
    """Ordonne pour que deux requêtes voisines ne touchent pas le même hôte."""
    par_hote = defaultdict(list)
    for u in sorted(urls):
        par_hote[u.split("/")[2].lower()].append(u)
    files = sorted(par_hote.values(), key=len, reverse=True)
    sortie = []
    while any(files):
        for f in files:
            if f:
                sortie.append(f.pop(0))
    return sortie


def sonde(u, ca):
    cmd = ["curl", "-s", "-o", os.devnull, "-w", "%{http_code}", "-L",
           "--max-time", str(MAX_TIME), "-A", UA]
    if ca and os.path.exists(ca):
        cmd += ["--cacert", ca]
    r = subprocess.run(cmd + [u], capture_output=True)
    return (r.stdout.decode("utf-8", "ignore").strip() or "000"), r.returncode


def balaye(limite=0, essais=3, sortie=None, seulement=None):
    par_doc = adresses(seulement)
    ca = faisceau()
    print("faisceau : %s" % ("utilisé" if ca and os.path.exists(ca) else "⚠️ ABSENT"))
    liste = tourniquet(par_doc)
    if limite:
        liste = liste[:limite]
    print("%d adresse(s) distincte(s) · %d hôte(s) · %d document(s) citants"
          % (len(liste), len({u.split("/")[2].lower() for u in liste}),
             len({d for u in liste for d in par_doc[u]})))
    codes, t0 = {}, time.time()
    for i, u in enumerate(liste, 1):
        codes[u] = sonde(u, ca)
        if i % 50 == 0 or i == len(liste):
            print("  … %d/%d · %.0f s écoulées" % (i, len(liste), time.time() - t0), flush=True)
        time.sleep(PAUSE)
    # essais 2 et 3 : groupés, donc réellement espacés, et SEULEMENT sur le non concluant
    for n in range(2, essais + 1):
        douteux = [u for u in liste if classe(*codes[u]) not in CONCLUANT]
        if not douteux:
            break
        print("  essai %d sur %d adresse(s) non concluante(s) après %d s d'attente"
              % (n, len(douteux), ENTRE_ESSAIS), flush=True)
        time.sleep(ENTRE_ESSAIS)
        for u in douteux:
            codes[u] = sonde(u, ca)
            time.sleep(PAUSE)
    lignes = [(classe(c, rc), "%s/%d" % (c, rc), u, ",".join(par_doc[u]))
              for u, (c, rc) in codes.items()]
    if sortie:
        with open(sortie, "w", encoding="utf-8") as f:
            for v, c, u, d in sorted(lignes):
                f.write("%s\t%s\t%s\t%s\n" % (v, c, u, d))
        print("écrit : %s" % sortie)
    tot = defaultdict(int)
    for v, _, _, _ in lignes:
        tot[v] += 1
    print("\n── verdict du balayage, %.0f s ──" % (time.time() - t0))
    for v in ("VIVANTE", "REFUS", "PANNE", "DELAI", "TLS", "CONNEXION",
              "INJOIGNABLE", "DNS", "MORTE", "AUTRE"):
        if tot[v]:
            print("  %-12s %4d" % (v, tot[v]))
    for v in ("MORTE", "DNS", "TLS", "DELAI", "CONNEXION", "INJOIGNABLE", "PANNE"):
        pour = [(c, u, par_doc[u]) for vv, c, u, _ in sorted(lignes) if vv == v
                for pass_ in (0,) if (c, u) == (c, u)]
        if not pour:
            continue
        print("\n%s — %d adresse(s) :" % (v, len(pour)))
        for c, u, docs in pour:
            print("  [%s] %s" % (c, u))
            print("        %d document(s) : %s" % (len(docs), ", ".join(docs[:3])
                                                   + (" …" if len(docs) > 3 else "")))
    return 1 if tot["MORTE"] or tot["DNS"] else 0   # les deux seuls verdicts qui CONDAMNENT


def autotest():
    cas = [("200", 0, "VIVANTE"), ("301", 0, "VIVANTE"), ("404", 0, "MORTE"), ("410", 0, "MORTE"),
           ("403", 0, "REFUS"), ("401", 0, "REFUS"), ("429", 0, "REFUS"), ("500", 0, "PANNE"),
           ("503", 0, "PANNE"), ("418", 0, "AUTRE"),
           # les quatre causes MESURÉES le 25/10/2026 derrière un même « 000 »
           ("000", 6, "DNS"), ("000", 60, "TLS"), ("000", 35, "TLS"), ("000", 28, "DELAI"),
           ("000", 7, "CONNEXION"), ("000", 0, "INJOIGNABLE"), ("", 0, "INJOIGNABLE")]
    ko = 0
    for code, rc, attendu in cas:
        if classe(code, rc) != attendu:
            print("  ✗ code %r/%d → %s, attendu %s" % (code, rc, classe(code, rc), attendu)); ko += 1
    # ⛔ UN DÉFAUT DE TLS NE CONDAMNE JAMAIS UNE PAGE — le piège du 18/10 (has-sante.fr)
    for rc in SORTIES_TLS:
        if classe("000", rc) != "TLS":
            print("  ✗ exit TLS %d classé %s — le piège du 18/10 est rouvert" % (rc, classe("000", rc))); ko += 1
    # le tourniquet ne doit JAMAIS mettre deux adresses du même hôte côte à côte quand on peut l'éviter
    u = ["https://a.fr/1", "https://a.fr/2", "https://a.fr/3", "https://b.fr/1", "https://c.fr/1"]
    t = tourniquet(u)
    colles = sum(1 for i in range(1, len(t)) if t[i].split("/")[2] == t[i - 1].split("/")[2])
    if sorted(t) != sorted(u):
        print("  ✗ le tourniquet perd ou duplique des adresses"); ko += 1
    if colles != 1:          # a1,b1,c1,a2,a3 : un seul voisinage de même hôte, (a2,a3) — DÉROULÉ,
                             # pas deviné : mon premier attendu disait 2 et c'est la borne qui m'a corrigé
        print("  ✗ le tourniquet colle %d fois au lieu de 1 — l'espacement par hôte est cassé" % colles); ko += 1
    # un 403 ne doit pas être rejoué (la page existe), un 000 et un 5xx doivent l'être
    rejeux = (("403", 0, False), ("000", 0, True), ("503", 0, True), ("404", 0, False),
              ("200", 0, False), ("000", 60, True), ("000", 6, True), ("000", 28, True))
    for code, rc, rejoue in rejeux:
        if (classe(code, rc) not in CONCLUANT) != rejoue:
            print("  ✗ code %s/%d : rejeu=%s, attendu %s"
                  % (code, rc, not rejoue, rejoue)); ko += 1
    total = len(cas) + len(SORTIES_TLS) + 2 + len(rejeux)
    if ko:
        print("  ✗ %d/%d borne(s) de balayer_adresses.py en échec" % (ko, total)); return 1
    print("  ✓ %d/%d bornes de balayer_adresses.py — un 403 n'est pas un lien mort, un défaut de TLS"
          " non plus" % (total, total))
    return 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["--autotest"]:
        sys.exit(autotest())
    def opt(nom, defaut):
        return type(defaut)(a[a.index(nom) + 1]) if nom in a else defaut
    sys.exit(balaye(limite=opt("--limite", 0), essais=opt("--essais", 3),
                    sortie=opt("--sortie", ""), seulement=opt("--adresses", "")))
