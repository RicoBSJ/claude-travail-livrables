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
import html, os, re, subprocess, sys, tempfile, time, unicodedata, zipfile
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


# 🔴 05/11/2026 — « FAÇADE ? » : UN 200 NE PROUVE PAS QU'UNE PAGE EXISTE, ET LE BALAYAGE
#    LISAIT UN CODE SANS JAMAIS LIRE UN CONTENU. Piste consignée le 25/10, ouverte depuis.
#    Les deux cas qui la fondent, REMESURÉS le 05/11 avec le faisceau, un par un, espacés :
#      www.handicap.gouv.fr/     HTTP 200 ·  6 845 octets bruts ·    93 caractères utiles
#      www.observalys.fr/ (http) HTTP 200 · 32 079 octets bruts ·   927 caractères utiles
#                                           (« Parked Domain name on Hostinger »)
#    ⛔ ET CES DEUX MESURES INTERDISENT LE RACCOURCI QUI SEMBLAIT ÉVIDENT : la TAILLE BRUTE
#    ne discrimine rien — 6 845 et 32 079 octets sont tous deux AU-DESSUS du plancher de
#    3 000, alors que les deux pages sont muettes. Il faut APLATIR, donc lire le corps.
#    🟢 ET LIRE LE CORPS NE COÛTE AUCUNE REQUÊTE DE PLUS : `-o /dev/null` téléchargeait déjà
#    le corps entier pour le jeter. On change la DESTINATION, pas le trafic — donc la règle
#    du 12/10 (jamais en parallèle) et la durée du balayage sont intactes.
#
#    QUATRE BORNES, toutes mesurées, et chacune ferme une façon de MENTIR :
#      ① seul un 2xx peut être une façade — le corps d'une erreur n'est pas la page, règle
#         d'`aspirer.py` ; un 404 est déjà MORTE, un 403 déjà REFUS.
#      ② `rc != 0` ne mesure RIEN : un transfert coupé par `--max-time` rend un corps
#         TRONQUÉ avec un code 200, donc un compte faussement bas. Une mesure partielle
#         n'est pas une petite page.
#      ③ un PDF (ou tout corps non textuel) n'est pas aplatissable — `aspirer.py` l'exempte
#         explicitement depuis l'origine. 31 des 1 353 adresses du corpus sont des `.pdf`,
#         et le type est lu sur la RÉPONSE (`%{content_type}`), pas sur l'extension.
#      ④ `None` n'est JAMAIS une façade : c'est l'ABSENCE de mesure, et le dépôt tient
#         qu'une page non lue est indiscernable d'une page vide (règle du 12/10).
#
# ⛔ LE VERDICT PORTE UN POINT D'INTERROGATION, ET CE N'EST PAS UNE PRÉCAUTION DE STYLE :
#    une page rendue en JavaScript est muette pour `curl` et riche pour un lecteur. FAÇADE
#    ne condamne donc pas — seuls MORTE et DNS font sortir en 1, c'est inchangé.
#
# ⚠️ L'APLATISSEMENT EST IMPORTÉ D'`aspirer.py`, JAMAIS RECOPIÉ (règle du 15/10 : un test
#    qui teste une copie de la logique ne garde rien). Les deux outils comptent donc les
#    mêmes caractères utiles, et une divergence est impossible par construction. Sur une
#    machine où l'import échoue, `aplati` vaut None, le balayage le DIT, et aucune adresse
#    n'est jamais dite façade — on perd le motif, on n'invente pas de verdict.
PLANCHER_LISIBLE = 3000        # le plancher du dépôt, cf. ⚠️ la borne de concordance au témoin
TYPES_TEXTE = ("text/html", "text/plain", "application/xhtml", "text/xml", "application/xml")

try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from aspirer import aplati          # LA MÊME mesure qu'aspirer.py, pas une seconde copie
except Exception:
    aplati = None


def utiles(brut, ctype, code, rc):
    """-> caractères utiles de la page, ou None quand elle n'a PAS ÉTÉ MESURÉE.

    None et 0 sont deux choses différentes, et les confondre est la seule erreur
    vraiment coûteuse ici : None dit « on ne sait pas », 0 dirait « page vide »."""
    if aplati is None or rc != 0 or not brut or code[:1] != "2":
        return None                                      # bornes ① ② ④
    if brut[:4] == b"%PDF":
        return None                                      # borne ③ — un PDF n'est pas du texte
    if ctype and not any(ctype.strip().lower().startswith(t) for t in TYPES_TEXTE):
        return None                                      # borne ③ — ni une image, ni un zip
    return len(unicodedata.normalize("NFC", aplati(brut.decode("utf-8", "replace"))))


def classe(code, rc=0, car=None):
    """(code HTTP, code de sortie curl, caractères utiles ou None) → un verdict qui ne
    confond pas ces situations. `car=None` = page non mesurée : jamais une façade."""
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
        # ⚠️ `code[:1] == "2"` N'EST PAS REDONDANT avec la garde d'`utiles()` : un 3xx FINAL
        # (curl a cessé de suivre) rend le corps d'une page de redirection, légitimement
        # minuscule. `utiles()` le rend None de son côté ; ici on refuse de l'accuser même
        # si un appelant passait un compte à la main — une exigence trop lâche rend un garde
        # redondant sans le dire (leçon du 26/10/2026), donc chaque couche exige la sienne.
        if car is not None and code[:1] == "2" and car < PLANCHER_LISIBLE:
            return "FACADE"       # 200 et muette : gabarit de parking, mur, ou rendu en JS
        return "VIVANTE"
    return "AUTRE"


CONCLUANT = ("VIVANTE", "FACADE", "MORTE", "REFUS")   # on ne rejoue que ce qui peut être
# passager — une façade est un 2xx stable, la rejouer coûterait deux requêtes pour rien


def faisceau():
    try:
        sys.path.insert(0, os.path.join(RACINE, "outils", "scripts"))
        import ca_bundle
        return ca_bundle.chemin()
    except Exception:
        return None


def adresses(seulement=None, orphelines=None):
    """{adresse : [documents qui la citent]} — lues dans les rels, comme le font les contrôles.

    🔴 25/10/2026 — UN rel N'EST PAS UN LIEN CLIQUABLE. Une correction qui retire un
    <w:hyperlink> sans retirer sa relation laisse une cible que le lecteur ne peut plus
    atteindre : le balayage la condamnait quand même. Mesuré sur la leçon n°3 d'ennéagramme,
    dont la correction du 09/10/2026 avait retiré les deux liens morts et conservé les
    adresses en clair, exactement comme il fallait — et le balayage du 25/10 a rendu
    « DNS » pour psychologie-enneagramme.fr, accusant un document qui avait raison.
    Borne mesurée sur les 294 documents : 4 rels orphelins dans 3 documents sur 2 951.
    Un rel orphelin est désormais RECENSÉ À PART et jamais sondé : il ne peut donc plus
    condamner. `orphelines` reçoit {adresse : [documents]} quand l'appelant la fournit."""
    par = defaultdict(set)
    orph = defaultdict(set)
    for base in ("livrables/lecons", "sources/veille"):
        for r, _, f in os.walk(os.path.join(RACINE, base)):
            for n in sorted(f):
                if not n.endswith(".docx"):
                    continue
                try:
                    z = zipfile.ZipFile(os.path.join(r, n))
                    rels = z.read("word/_rels/document.xml.rels").decode("utf-8", "ignore")
                    corps = z.read("word/document.xml").decode("utf-8", "ignore")
                except Exception:
                    continue
                vus = set(re.findall(r'r:id="([^"]+)"', corps))
                # une adresse peut avoir PLUSIEURS rels dans le même document : elle n'est
                # orpheline que si AUCUN ne sert, d'où les deux ensembles puis la différence
                cliquables, mortes_nees = set(), set()
                for m in re.finditer(r'Id="([^"]+)"[^>]*Target="(https?://[^"]+)"', rels):
                    u = html.unescape(m.group(2))
                    (cliquables if m.group(1) in vus else mortes_nees).add(u)
                for u in cliquables:
                    par[u].add(n)
                for u in mortes_nees - cliquables:
                    orph[u].add(n)
    if seulement:
        garde = {l.strip() for l in open(seulement, encoding="utf-8") if l.strip()}
        absentes = garde - set(par)
        par = {u: v for u, v in par.items() if u in garde}
        if absentes:
            print("⚠️ %d adresse(s) de la liste ne sont plus citées par aucun document" % len(absentes))
    if orphelines is not None:
        orphelines.update({u: sorted(v) for u, v in orph.items()})
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
    """(code, code de sortie curl, caractères utiles ou None).

    UNE SEULE REQUÊTE, la même qu'avant : `-o /dev/null` téléchargeait déjà le corps
    entier pour le jeter — on change sa DESTINATION, pas le trafic. Le fichier est
    effacé aussitôt lu : rien n'est conservé sur le disque, et le balayage reste
    strictement séquentiel (règle du 12/10/2026).

    Mesuré localement le 05/11/2026 : `curl -L -o fichier` n'y concatène PAS le corps
    des réponses 3xx — seul le corps FINAL y atterrit, donc le compte n'est pas gonflé
    par les pages de redirection. Vérifié sur un serveur fabriqué, pas supposé."""
    # ⚠️ DANS LE DOSSIER TEMPORAIRE DU SYSTÈME, JAMAIS DANS LE DÉPÔT : l'arbre de travail
    # vit dans kDrive, et le 27/10/2026 kDrive a dématérialisé un objet de `.git` puis déposé
    # une copie de conflit dedans. On n'y fait pas transiter des centaines de mégaoctets.
    tmp = os.path.join(tempfile.gettempdir(), "balayage_corps_%d.bin" % os.getpid())
    cmd = ["curl", "-s", "-o", tmp, "-w", "%{http_code}\t%{content_type}", "-L",
           "--max-time", str(MAX_TIME), "-A", UA]
    if ca and os.path.exists(ca):
        cmd += ["--cacert", ca]
    r = subprocess.run(cmd + [u], capture_output=True)
    champs = r.stdout.decode("utf-8", "ignore").strip().split("\t")
    code = (champs[0].strip() or "000")[-3:]
    ctype = champs[1].strip() if len(champs) > 1 else ""
    try:
        brut = open(tmp, "rb").read()
    except OSError:
        brut = b""
    if os.path.exists(tmp):
        os.remove(tmp)
    return code, r.returncode, utiles(brut, ctype, code, r.returncode)


def balaye(limite=0, essais=3, sortie=None, seulement=None):
    orphelines = {}
    par_doc = adresses(seulement, orphelines)
    ca = faisceau()
    print("faisceau : %s · aplatissement : %s"
          % ("utilisé" if ca and os.path.exists(ca) else "⚠️ ABSENT",
             "aspirer.aplati" if aplati is not None
             else "⚠️ INDISPONIBLE — aucune adresse ne sera dite FACADE"))
    liste = tourniquet(par_doc)
    if limite:
        liste = liste[:limite]
    print("%d adresse(s) distincte(s) · %d hôte(s) · %d document(s) citants"
          % (len(liste), len({u.split("/")[2].lower() for u in liste}),
             len({d for u in liste for d in par_doc[u]})))
    if orphelines:
        print("↯ %d adresse(s) dans %d document(s) ne sont PLUS cliquables — leur relation "
              "survit, aucun <w:hyperlink> ne la nomme : non sondées, non condamnées"
              % (len(orphelines), len({d for v in orphelines.values() for d in v})))
        for u in sorted(orphelines):
            print("    %s  [%s]" % (u, ", ".join(orphelines[u])))
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
    lignes = [(classe(c, rc, car), "%s/%d" % (c, rc), u, ",".join(par_doc[u]),
               "" if car is None else str(car))
              for u, (c, rc, car) in codes.items()]
    if sortie:
        with open(sortie, "w", encoding="utf-8") as f:
            for v, c, u, d, car in sorted(lignes):
                # la 5e colonne est AJOUTÉE : les quatre premières gardent leur ordre, pour
                # qu'un balayage du 25/10 et un du 05/11 se relisent côte à côte
                f.write("%s\t%s\t%s\t%s\t%s\n" % (v, c, u, d, car))
        print("écrit : %s" % sortie)
    tot = defaultdict(int)
    for v, _, _, _, _ in lignes:
        tot[v] += 1
    print("\n── verdict du balayage, %.0f s ──" % (time.time() - t0))
    for v in ("VIVANTE", "FACADE", "REFUS", "PANNE", "DELAI", "TLS", "CONNEXION",
              "INJOIGNABLE", "DNS", "MORTE", "AUTRE"):
        if tot[v]:
            print("  %-12s %4d" % (v, tot[v]))
    for v in ("MORTE", "DNS", "TLS", "DELAI", "CONNEXION", "INJOIGNABLE", "PANNE", "FACADE"):
        pour = [(c, u, par_doc[u], car) for vv, c, u, _, car in sorted(lignes) if vv == v]
        if not pour:
            continue
        if v == "FACADE":
            print("\n%s ? — %d adresse(s) : un 2xx SOUS %d caractères utiles. Ni morte ni"
                  " vivante : gabarit de parking, mur anti-automate, ou page rendue en"
                  " JavaScript — et une page rendue en JS est muette pour curl et riche pour"
                  " un lecteur. À LIRE, pas à corriger." % (v, len(pour), PLANCHER_LISIBLE))
        else:
            print("\n%s — %d adresse(s) :" % (v, len(pour)))
        for c, u, docs, car in pour:
            print("  [%s%s] %s" % (c, "" if not car else " · %s car." % car, u))
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
    # ── un rel N'EST PAS un lien cliquable (25/10/2026) ───────────────────────────────
    # Arborescence FABRIQUÉE : rien de vivant dans le verdict (leçon du 22/10/2026, où un
    # témoin ancré sur l'avancement réel d'un parcours a bloqué tous les pushs du dépôt).
    # On exerce le VRAI chemin, adresses(), en déplaçant RACINE — pas une copie de sa logique
    # (leçon du 15/10/2026 : un test qui teste une copie de la logique ne garde rien).
    import tempfile
    U = "https://exemple-temoin-orphelin.invalid/p"
    def docx(chemin, paires):
        """paires : [(Id, sert_dans_le_corps)] — toutes pointent U."""
        rels = ('<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org'
                '/package/2006/relationships">' + "".join(
                '<Relationship Id="%s" Type="http://schemas.openxmlformats.org/officeDocument'
                '/2006/relationships/hyperlink" Target="%s" TargetMode="External"/>' % (i, U)
                for i, _ in paires) + '</Relationships>')
        corps = ('<?xml version="1.0"?><w:document xmlns:w="http://schemas.openxmlformats.org'
                 '/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org'
                 '/officeDocument/2006/relationships"><w:body>' + "".join(
                 '<w:p><w:hyperlink r:id="%s"><w:r><w:t>lien</w:t></w:r></w:hyperlink></w:p>' % i
                 for i, sert in paires if sert) + '</w:body></w:document>')
        with zipfile.ZipFile(chemin, "w") as o:
            o.writestr("word/_rels/document.xml.rels", rels)
            o.writestr("word/document.xml", corps)
    orphelins_attendus = [
        # (nom, [(Id, sert)], l'adresse est-elle CLIQUABLE ?, est-elle ORPHELINE ?)
        ("tout_orphelin.docx", [("rId1", False)], False, True),
        ("vivant_et_orphelin.docx", [("rId1", True), ("rIdcorr", False)], True, False),
        ("tout_vivant.docx", [("rId1", True)], True, False)]
    vieille_racine = globals()["RACINE"]
    for nom, paires, cliquable, orpheline in orphelins_attendus:
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "livrables", "lecons"))
            os.makedirs(os.path.join(d, "sources", "veille"))
            docx(os.path.join(d, "livrables", "lecons", nom), paires)
            globals()["RACINE"] = d
            try:
                orph = {}
                par = adresses(None, orph)
            finally:
                globals()["RACINE"] = vieille_racine
            if (U in par) != cliquable:
                print("  ✗ %s : cliquable=%s, attendu %s" % (nom, U in par, cliquable)); ko += 1
            if (U in orph) != orpheline:
                print("  ✗ %s : orpheline=%s, attendu %s — un rel que le corps ne nomme plus "
                      "ne doit PAS être condamné" % (nom, U in orph, orpheline)); ko += 1
    if globals()["RACINE"] != vieille_racine:
        print("  ✗ RACINE n'a pas été rendue — le balayage réel sondrait l'arborescence du témoin")
        ko += 1

    # ── « FAÇADE ? » : un 2xx muet n'est ni mort ni vivant (05/11/2026) ──────────────
    # ⚠️ SEPT de ces bornes doivent être ACCEPTÉES : ce motif RESSERRE le verdict VIVANTE,
    # donc sans elles rien n'empêche de le réélargir demain (convention du dépôt).
    facade_cas = [
        ("200", 0, 2999, "FACADE"),     # le plancher mord à 2 999…
        ("200", 0, 0, "FACADE"),        # …et une page qui répond 200 sans un mot est le cas pur
        ("200", 0, 3000, "VIVANTE"),    # ACCEPTÉE : 3 000 n'est pas SOUS le plancher
        ("200", 0, 99999, "VIVANTE"),   # ACCEPTÉE
        ("200", 0, None, "VIVANTE"),    # ACCEPTÉE : non mesurée ≠ façade (règle du 12/10)
        ("301", 0, 10, "VIVANTE"),      # ACCEPTÉE : un 3xx FINAL rend une page de redirection
        ("404", 0, 12, "MORTE"),        # ACCEPTÉE : un corps d'erreur n'est pas la page
        ("403", 0, 12, "REFUS"),        # ACCEPTÉE : un automate écarté n'est pas une façade
        ("500", 0, 12, "PANNE"),        # ACCEPTÉE
        ("000", 60, 12, "TLS"),         # ACCEPTÉE : le piège du 18/10 reste fermé
    ]
    for code, rc, car, attendu in facade_cas:
        if classe(code, rc, car) != attendu:
            print("  ✗ %s/%d · %r car. → %s, attendu %s"
                  % (code, rc, car, classe(code, rc, car), attendu)); ko += 1

    # ── utiles() exercée POUR DE VRAI : c'est elle qui décide si l'on a MESURÉ ────────
    HTM = b"<html><body>" + b"mot " * 10 + b"</body></html>"        # bien sous le plancher
    GROS = b"<html><body>" + b"mot " * 2000 + b"</body></html>"     # bien au-dessus
    utiles_cas = [
        # (corps, content-type, code, rc, attendu : None, "sous" ou "au-dessus")
        (HTM, "text/html", "200", 0, "sous"),
        (GROS, "text/html", "200", 0, "au-dessus"),
        (HTM, "text/html; charset=utf-8", "200", 0, "sous"),   # un paramètre ne gêne pas
        (HTM, "", "200", 0, "sous"),                           # serveur sans Content-Type
        (HTM, "text/html", "200", 28, None),   # ② coupé par --max-time : mesure PARTIELLE
        (HTM, "text/html", "404", 0, None),    # ① le corps d'une erreur n'est pas la page
        (b"%PDF-1.7 trailer", "application/pdf", "200", 0, None),   # ③ reconnu aux octets
        (HTM, "application/pdf", "200", 0, None),                   # ③ reconnu au type seul
        (b"\x89PNG\r\n\x1a\n", "image/png", "200", 0, None),      # ③ ni texte ni page
        (b"", "text/html", "200", 0, None),    # ④ rien reçu n'est PAS une page vide
    ]
    for brut, ctype, code, rc, attendu in utiles_cas:
        n = utiles(brut, ctype, code, rc)
        bon = (n is None if attendu is None else
               isinstance(n, int) and ((n < PLANCHER_LISIBLE) == (attendu == "sous")))
        if not bon:
            print("  ✗ utiles(%d octets, %r, %s/%d) → %r, attendu %s"
                  % (len(brut), ctype, code, rc, n, attendu)); ko += 1

    # ── le plancher est à QUATRE endroits du dépôt : ils doivent concorder ───────────
    # Aucun n'importe celui d'un autre, donc une divergence serait SILENCIEUSE : un même
    # « sous le plancher » voudrait dire deux choses selon l'outil qui le dit.
    SCR = os.path.dirname(os.path.abspath(__file__))
    planchers = [("aspirer.py", r"len\(txt\) < (\d+)"),
                 ("controle_attributions.py", r"utile < (\d+)"),
                 ("controle_noms_propres.py", r"PLANCHER_PAGE = (\d+)"),
                 ("controle_decompte.py", r"PLANCHER_LISIBLE = (\d+)")]
    for nom, motif in planchers:
        try:
            t = open(os.path.join(SCR, nom), encoding="utf-8").read()
        except OSError:
            t = ""
        m = re.search(motif, t)
        if not m or int(m.group(1)) != PLANCHER_LISIBLE:
            print("  ✗ %s : plancher %s, %d ici — les deux outils ne mesurent plus la même "
                  "chose" % (nom, m.group(1) if m else "INTROUVABLE", PLANCHER_LISIBLE)); ko += 1

    # ── et le motif est exercé DE BOUT EN BOUT, sur un serveur LOCAL ─────────────────
    # Aucun tiers : 127.0.0.1 et une arborescence fabriquée. Un témoin ancré sur un site
    # tiers périme tout seul et bloque alors TOUS les pushs du dépôt (15, 22 et 23/10/2026).
    # On exerce le VRAI chemin — sonde → utiles → classe → impression → code de sortie —
    # parce qu'une fonction juste mais jamais appelée n'écrit dans aucun log (27/10/2026).
    import contextlib, http.server, io, threading
    CORPS = {"/facade": b"<html><body>Parked Domain name</body></html>",
             "/riche": b"<html><body>" + b"phrase " * 900 + b"</body></html>"}

    class Main(http.server.BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.0"
        def log_message(self, *a):
            pass
        def do_GET(self):
            c = CORPS.get(self.path)
            self.send_response(200 if c else 404)
            c = c or b"<html>rien</html>"
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(len(c)))
            self.end_headers()
            self.wfile.write(c)

    srv = http.server.HTTPServer(("127.0.0.1", 0), Main)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = "http://127.0.0.1:%d" % srv.server_port

    def balaye_sur(chemins):
        """fabrique un .docx qui cite ces chemins, puis lance le VRAI balaye()."""
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "livrables", "lecons"))
            os.makedirs(os.path.join(d, "sources", "veille"))
            paires = [("rId%d" % (i + 1), base + c) for i, c in enumerate(chemins)]
            rels = ('<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats'
                    '.org/package/2006/relationships">' + "".join(
                    '<Relationship Id="%s" Type="http://schemas.openxmlformats.org/office'
                    'Document/2006/relationships/hyperlink" Target="%s" TargetMode='
                    '"External"/>' % p for p in paires) + '</Relationships>')
            corps = ('<?xml version="1.0"?><w:document xmlns:w="http://schemas.openxml'
                     'formats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.open'
                     'xmlformats.org/officeDocument/2006/relationships"><w:body>' + "".join(
                     '<w:p><w:hyperlink r:id="%s"><w:r><w:t>l</w:t></w:r></w:hyperlink>'
                     '</w:p>' % i for i, _ in paires) + '</w:body></w:document>')
            with zipfile.ZipFile(os.path.join(d, "livrables", "lecons", "t.docx"), "w") as o:
                o.writestr("word/_rels/document.xml.rels", rels)
                o.writestr("word/document.xml", corps)
            vieille = globals()["RACINE"]
            globals()["RACINE"] = d
            tampon = io.StringIO()
            try:
                with contextlib.redirect_stdout(tampon):
                    rc = balaye(essais=1)
            finally:
                globals()["RACINE"] = vieille
            return rc, tampon.getvalue()

    rc_vf, sortie_vf = balaye_sur(["/facade", "/riche"])
    rc_m, _ = balaye_sur(["/mort"])
    srv.shutdown()
    lignes_f = [l for l in sortie_vf.splitlines() if "/facade" in l]
    # le récapitulatif s'imprime "  %-12s %4d" : deux jetons par ligne, verdict puis compte
    recap = dict(tuple(l.split()) for l in sortie_vf.splitlines()
                 if len(l.split()) == 2 and l.split()[1].isdigit())
    bout = [
        ("une façade ne CONDAMNE pas : seuls MORTE et DNS font sortir en 1", rc_vf == 0),
        ("le récapitulatif COMPTE la façade", recap.get("FACADE") == "1"),
        ("le détail NOMME l'adresse : une alerte que personne ne lit n'existe pas",
         bool(lignes_f) and any("car." in l for l in lignes_f)),
        ("la page riche reste VIVANTE", recap.get("VIVANTE") == "1"),
        ("un 404 CONDAMNE toujours — le code de sortie n'a pas été affaibli", rc_m == 1),
    ]
    for libelle, ok in bout:
        if not ok:
            print("  ✗ bout en bout : %s" % libelle); ko += 1

    # ── deux bornes de structure ─────────────────────────────────────────────────────
    structure = [
        ("l'aplatissement est IMPORTÉ d'aspirer.py, pas recopié",
         aplati is not None and getattr(aplati, "__module__", "") == "aspirer"),
        ("FACADE est CONCLUANT : un 2xx stable ne se rejoue pas, cela coûterait 2 requêtes",
         "FACADE" in CONCLUANT),
    ]
    for libelle, ok in structure:
        if not ok:
            print("  ✗ %s" % libelle); ko += 1

    total = (len(cas) + len(SORTIES_TLS) + 2 + len(rejeux)
             + 2 * len(orphelins_attendus) + 1
             + len(facade_cas) + len(utiles_cas) + len(planchers)
             + len(bout) + len(structure))
    if ko:
        print("  ✗ %d/%d borne(s) de balayer_adresses.py en échec" % (ko, total)); return 1
    print("  ✓ %d/%d bornes de balayer_adresses.py — un 403 n'est pas un lien mort, un défaut de"
          " TLS non plus, un rel orphelin n'est pas une adresse cliquable, et un 200 muet"
          " n'est pas une page vivante" % (total, total))
    return 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["--autotest"]:
        sys.exit(autotest())
    def opt(nom, defaut):
        return type(defaut)(a[a.index(nom) + 1]) if nom in a else defaut
    sys.exit(balaye(limite=opt("--limite", 0), essais=opt("--essais", 3),
                    sortie=opt("--sortie", ""), seulement=opt("--adresses", "")))
