#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tolerance_page_morte.py — LE HARNAIS REFUSE DE CONCLURE QUAND LA PAGE D'UN TÉMOIN NE RÉPOND PLUS.

Écrit le 25/10/2026, après le quatrième incident de la même classe : un témoin VIVANT dont le
verdict dépend d'une propriété volatile. Le 23 et le 25/10/2026, `promenade.imcce.fr` est tombé
— DNS résolu, aucune réponse TCP, `curl` exit 28 avec ET sans le faisceau, donc ni TLS ni nous —
et le bloc des étapes 5 bis a déclaré FAUX POSITIF son témoin conforme d'astrologie n°10 :

    ⑦ PAGE SANS RÉPONSE, NON DÉCLARÉE (https://promenade.imcce.fr/fr/pages2/221.html : code 000
      après 3 essais) : ¶19, ¶115
    REFUSÉ — 1 motif(s) : page sans réponse …enade.imcce.fr/fr/pages2/221.html

Le document n'avait pas changé d'un octet. Le refus était EXACT (le ¶ attribue un chiffre à une
page qui ne répond pas, sans le déclarer) et le harnais sortait en 1, donc **le hook refusait TOUS
les pushs du dépôt** — exactement l'effet du motif ⑩ le 15/10 et du témoin de `supprimer_job.sh`
le 22/10. `controle_attributions.py` a son `exit 3` « pages non lues » depuis des semaines ; les
trois contrôles 5 bis n'ont rien d'équivalent, et c'est ce trou qu'on ferme ICI, au harnais, et
non dans les contrôles : en PRODUCTION, ⑦ doit continuer à refuser une page muette non déclarée.

⚠️ CE QU'ON NE FAIT PAS, ET POURQUOI : on ne touche pas aux contrôles. Un job qui attribue un
chiffre à une page morte sans le dire doit toujours être refusé — c'est le sens même de ⑦. Ce qui
est faux, c'est de lire ce refus comme la RÉGRESSION D'UN DÉPÔT : le document est figé, la page
non. Le harnais ne doit donc pas conclure, ni dans un sens ni dans l'autre : le duo n'est PAS JOUÉ,
et il le dit.

CONTRAT
    tolerance_page_morte.py <sortie_du_contrôle.txt> <témoin.docx>
      exit 0 → refus EXCUSÉ : le duo n'est pas joué (et le harnais l'imprime, il ne le tait pas)
      exit 1 → refus À PRENDRE AU SÉRIEUX : le bloc 5 bis sort en 1 comme avant
    tolerance_page_morte.py --autotest   → bornes, serveur local, AUCUN tiers

QUATRE CONDITIONS, TOUTES NÉCESSAIRES — l'excuse est l'exception, le refus est le défaut :
  ① la sortie porte une ligne de synthèse de refus d'une forme CONNUE, qui dit combien de motifs ;
  ② autant de lignes de motif nomment une adresse QUE de motifs annoncés — un refus qui n'est pas
     ENTIÈREMENT imputable à des pages ne s'excuse pas, même en partie ;
  ③ chaque adresse figure dans `word/_rels` DU TÉMOIN, et non seulement dans la sortie : un
     contrôle saboté qui IMPRIMERAIT une excuse ne s'excuse pas lui-même ;
  ④ le harnais MESURE lui-même, à la seconde, que l'adresse ne répond pas — avec le faisceau de
     certificats, donc une page qui tomberait par défaut de TLS n'est PAS excusée mais DÉNONCÉE.
Le sens d'échec du comptage est le REFUS : mal compter fait bloquer, jamais excuser.

⚠️ CE QUE L'EXCUSE COÛTE, ET IL FAUT LE DIRE : pendant la panne d'un tiers, les motifs de ce duo
ne sont plus gardés du tout. C'est assumé, et c'est la doctrine du dépôt — « un faux refus coûte
un livrable non publié ; un vrai manqué ne coûte qu'une relecture humaine » — mais le harnais
compte les duos non joués et le dit à chaque passage.
"""
import os, re, subprocess, sys, time, unicodedata, zipfile

# ⚠️ QUATRE dirname, pas trois : ce script vit dans outils/scripts/non_regression/, un cran
# plus bas que les contrôles. Avec les trois dirname copiés de controle_*.py, RACINE valait
# « …/Claude_Travail/outils », l'import de ca_bundle échouait, et les sondes partaient SANS
# faisceau — en silence, puisque l'except rend None. C'est l'annotation « [faisceau : … ] »
# ajoutée dans le message qui l'a dit, au premier sabotage (25/10/2026).
RACINE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126 Safari/537.36")
ESSAIS, ATTENTE, MAX_TIME = 2, 2, 20

# les trois formes de synthèse des trois contrôles 5 bis, mesurées sur leur source le 25/10/2026 :
#   controle_astrologie_karmique.py : print  « REFUSÉ — N motif(s) : a | b »      puis sys.exit(1)
#   controle_psychopathologie.py    : sys.exit(« LEÇON REFUSÉE — a ; b »)  → stderr, exit 1
#   controle_ai_act.py              : sys.exit(« NOTE REFUSÉE — a ; b »)   → stderr, exit 1
# Le harnais capture 2>&1, donc les trois arrivent dans le même fichier.
SYNTH_N = re.compile(r"^REFUSÉ\s+—\s+(\d+)\s+motif")
SYNTH_L = re.compile(r"^(?:LEÇON|NOTE)\s+REFUSÉE\s+—\s+(.+)$")
# ⚠️ 28/11/2026 — LA TROISIÈME FORME, celle de `controle_attributions.py`, ET ELLE N'ÉNUMÈRE RIEN.
#    Son `VERDICT : N probleme(s) bloquant(s) (A + A2 + …)` donne le COMPTE et pas les motifs : le
#    profil d'appariement ci-dessous ne peut donc pas s'y appliquer, et on compte les LIGNES
#    BLOQUANTES. Les trois marqueurs sont relevés sur ses `print` (28/11/2026, `grep -oE` sur la
#    source) — « INTERDIT » (liens morts ㉞ et passe C), « ABSENTE » (B, ㉖), « MAL ATTRIBUEE »
#    (㉓, ㉚ reprise nue).
#    ⛔ BORNE DITE : son `pb` additionne DIX catégories (orphelines, sites non listés, sans
#    adresse, mal formés, source sans adresse, sans cible, liens morts, B, B-NOM, C2). Les trois
#    marqueurs ne les couvrent donc pas toutes — et c'est SANS DANGER, parce que le sens d'échec
#    du comptage est le REFUS : un motif hors marqueur fait rater le compte, donc bloquer.
SYNTH_V = re.compile(r"^VERDICT\s*:\s*(\d+)\s+probleme\(s\)\s+bloquant")
BLOQUANTS = ("INTERDIT", "ABSENTE", "MAL ATTRIBUEE")
ADRESSE = re.compile(r"https?://[^\s<>\"»,;)\]]+")


def nfc(s):
    return unicodedata.normalize("NFC", s)


def urls_du_docx(p):
    """Les adresses que le TÉMOIN porte vraiment — la sortie du contrôle ne fait pas foi (③)."""
    with zipfile.ZipFile(p) as z:
        rels = z.read("word/_rels/document.xml.rels").decode("utf-8", "ignore")
    return {m.group(1) for m in re.finditer(r'Target="(https?://[^"]+)"', rels)}


JETON = re.compile(r"[a-z0-9][a-z0-9./_-]{3,}")


def plie(s):
    """Casse et accents pliés — pour comparer une entrée de synthèse à une ligne de motif."""
    d = unicodedata.normalize("NFD", nfc(s).lower())
    return "".join(c for c in d if unicodedata.category(c) != "Mn")


def jetons(s):
    return set(JETON.findall(plie(s).replace("…", " ")))


def apparie(entrees, lignes_adr):
    """Chaque motif ÉNUMÉRÉ par la synthèse a-t-il SA ligne nommant une page du témoin ?

    Rend ({indice de ligne: entrée}, [entrées non appariées]).

    ⚠️ 28/11/2026 — C'EST LA CORRECTION D'UN DÉFAUT MESURÉ DE LA CONDITION ②, et ce défaut faisait
    REFUSER une excuse que la tolérance devait accorder. L'ancienne règle comptait les LIGNES qui
    nomment une page du témoin et exigeait l'égalité au nombre de motifs. Or les contrôles 5 bis
    impriment aussi des lignes d'EXEMPTION, qui nomment une page sans accuser personne — mesuré sur
    le témoin ai-act du 16/10 :

        TAILLE NON COMPARÉE (¶81) : https://iapp.org/news/ est une page d'index — …

    Cette ligne portait le compte à 3 pour une synthèse annonçant 2 motifs, et l'excuse était
    refusée au motif que le refus « n'est pas entièrement imputable à des pages » — alors qu'il
    l'était. On apparie donc chaque motif à une ligne, et les lignes que personne ne réclame sont
    ignorées : UNE EXEMPTION N'EST PAS UN MOTIF.

    ⛔ ET C'EST L'APPARIEMENT QUI PORTE TOUT, PAS LA PRÉSENCE : l'ancienne forme était satisfaite
    par n'importe quelles N lignes. Ici une entrée doit partager un jeton avec SA ligne, et une
    ligne ne sert qu'une entrée — appariement injectif, glouton par nombre de jetons partagés.
    C'est ce glouton qui sépare la ligne d'exemption « TAILLE NON COMPARÉE » de la ligne de motif
    « TAILLE ANNONCÉE FAUSSE » : la première ne partage que « taille » avec la synthèse, la
    seconde partage « taille », « 18111 » ET « 16369 ».

    ⚠️ Et seules les URL des lignes APPARIÉES sont sondées — sans quoi `iapp.org/news/`, qui
    répond, ferait refuser l'excuse par la condition ④ : le comptage et le sondage doivent porter
    sur le MÊME ensemble de lignes.
    """
    pris, manque = {}, []
    for e in entrees:
        je = jetons(e)
        best, bn = None, 0
        for i, (ligne, _urls) in enumerate(lignes_adr):
            if i in pris:
                continue
            n = len(je & jetons(ligne))
            if n > bn:
                best, bn = i, n
        if best is None:
            manque.append(e)
        else:
            pris[best] = e
    return pris, manque


def motifs_annonces(texte):
    """(n, ligne de synthèse, entrées|None), ou (None, None, None) si la forme est inconnue (①).

    `entrées` est la liste des motifs que la synthèse ÉNUMÈRE ; None signifie « cette forme ne les
    énumère pas » — profil « lignes bloquantes », voir SYNTH_V.
    """
    for ligne in texte.splitlines():
        l = ligne.strip()
        m = SYNTH_N.match(l)
        if m:
            q = l.split(":", 1)
            ent = [x.strip() for x in q[1].split("|") if x.strip()] if len(q) > 1 else []
            return int(m.group(1)), ligne, ent
        m = SYNTH_L.match(l)
        if m:
            ent = [x.strip() for x in m.group(1).split(";") if x.strip()]
            return len(ent), ligne, ent
        m = SYNTH_V.match(l)
        if m:
            return int(m.group(1)), ligne, None
    return None, None, None


def chemin_faisceau():
    try:
        sys.path.insert(0, os.path.join(RACINE, "outils", "scripts"))
        import ca_bundle
        return ca_bundle.chemin()
    except Exception:
        return None


# ⚠️ 28/11/2026 — LE PLANCHER ET SA MESURE SONT IMPORTÉS DE `balayer_adresses.py`, PAS RECOPIÉS.
#    Ce module compte déjà les caractères utiles d'un corps (`utiles`, qui réutilise lui-même
#    `aspirer.aplati`) et porte le plancher de 3 000 du dépôt. Une seconde implémentation
#    dériverait en silence — règle du 15/10 (« un test qui teste une COPIE de la logique ne garde
#    rien »), et le dépôt porte déjà une borne de concordance de ce plancher sur CINQ fichiers.
#    ⛔ Et le `sys.path.insert` est obligatoire : sous `python3 -I` le dossier du script quitte
#    `sys.path` et cet import échouerait EN SILENCE (le défaut du 28/11/2026, corrigé ce jour).
try:
    sys.path.insert(0, os.path.join(RACINE, "outils", "scripts"))
    from balayer_adresses import utiles as _utiles, PLANCHER_LISIBLE
except Exception as _e:
    print("⚠️ tolerance_page_morte.py : balayer_adresses non importé (%s) — aucune page ne sera "
          "dite MUETTE" % type(_e).__name__, file=sys.stderr)
    _utiles, PLANCHER_LISIBLE = None, 3000


def car_utiles(u, faisceau):
    """Caractères utiles de la page, ou None quand elle n'a PAS ÉTÉ MESURÉE.

    None et 0 sont deux choses différentes : None dit « on ne sait pas », 0 dirait « page vide ».
    Les confondre ferait excuser une page riche, c'est-à-dire exactement le contraire du but.
    """
    if _utiles is None:
        return None
    cmd = ["curl", "-sL", "--max-time", str(MAX_TIME), "-A", UA,
           "-w", "\n%{http_code}\t%{content_type}"]
    if faisceau and os.path.exists(faisceau):
        cmd += ["--cacert", faisceau]
    r = subprocess.run(cmd + [u], capture_output=True)
    i = r.stdout.rfind(b"\n")
    if i < 0:
        return None
    q = r.stdout[i + 1:].decode("utf-8", "ignore").split("\t")
    code = q[0].strip() or "000"
    ctype = (q[1] if len(q) > 1 else "").strip()
    return _utiles(r.stdout[:i], ctype, code, r.returncode)


def code_http(u, faisceau):
    """Le code de la page, MESURÉ ICI (④). Séquentiel : jamais deux sondes en parallèle."""
    cmd = ["curl", "-s", "-o", os.devnull, "-w", "%{http_code}", "-L",
           "--max-time", str(MAX_TIME), "-A", UA]
    if faisceau and os.path.exists(faisceau):
        cmd += ["--cacert", faisceau]
    for n in range(ESSAIS):
        r = subprocess.run(cmd + [u], capture_output=True)
        c = r.stdout.decode("utf-8", "ignore").strip() or "000"
        if c not in ("", "000"):
            return c
        if n + 1 < ESSAIS:
            time.sleep(ATTENTE)
    return "000"


def verdict(sortie, docx, faisceau=None, sonde=None, mesure=None):
    """Rend (excusé, raison). Le sens d'échec du comptage est TOUJOURS le refus."""
    sonde = sonde or (lambda u: code_http(u, faisceau))
    mesure = mesure or (lambda u: car_utiles(u, faisceau))
    try:
        texte = nfc(open(sortie, encoding="utf-8", errors="ignore").read())
    except OSError as e:
        return False, "sortie du contrôle illisible (%s)" % e
    try:
        doc = urls_du_docx(docx)
    except Exception as e:
        return False, "témoin illisible (%s) — on n'excuse pas ce qu'on ne peut pas vérifier" % e

    n, synth, entrees = motifs_annonces(texte)
    if n is None:
        return False, ("la sortie ne porte aucune synthèse de refus connue — on ne compte pas "
                       "ce qu'on ne sait pas lire")
    if n < 1:
        return False, "synthèse annonçant %d motif — rien à excuser" % n

    lignes_adr = []
    for ligne in texte.splitlines():
        if ligne == synth or not ligne.strip():
            continue
        vues = [a.rstrip(".,;:)»'\"") for a in ADRESSE.findall(ligne)]
        vues = [a for a in vues if a in doc]          # ③ l'adresse doit être DANS le témoin
        if vues:
            lignes_adr.append((ligne, vues))

    urls = []
    if entrees is None:
        # ── profil « lignes bloquantes » : la synthèse donne un COMPTE et n'énumère rien.
        bloq = [(l, v) for (l, v) in lignes_adr if any(b in l for b in BLOQUANTS)]
        if len(bloq) != n:
            return False, ("%d motif(s) bloquant(s) annoncé(s) mais %d ligne(s) bloquante(s) "
                           "nommant une page du témoin — un refus qui n'est pas ENTIÈREMENT "
                           "imputable à des pages ne s'excuse pas (marqueurs lus : %s)"
                           % (n, len(bloq), ", ".join(BLOQUANTS)))
        for _l, v in bloq:
            urls += [a for a in v if a not in urls]
    else:
        # ── profil « appariement » : chaque motif énuméré doit avoir SA ligne.
        if len(entrees) != n:
            return False, ("synthèse annonçant %d motif(s) mais en énumérant %d — on ne compte "
                           "pas ce qu'on ne sait pas lire" % (n, len(entrees)))
        pris, manque = apparie(entrees, lignes_adr)
        if manque:
            return False, ("%d motif(s) annoncé(s), %d apparié(s) à une ligne nommant une page du "
                           "témoin — un refus qui n'est pas ENTIÈREMENT imputable à des pages ne "
                           "s'excuse pas ; sans page : %s"
                           % (n, len(pris), " | ".join(manque)[:160]))
        for i in sorted(pris):
            urls += [a for a in lignes_adr[i][1] if a not in urls]

    vivantes, muettes = [], []
    for u in urls:                                    # ④ séquentiel, mesuré ici
        c = sonde(u)
        if c in ("", "000"):
            continue
        # ⚠️ 28/11/2026 — UNE PAGE QUI RÉPOND MAIS NE DIT RIEN EST INDISCERNABLE D'UNE PAGE NON
        #    LUE, et c'est la règle du 12/10 du dépôt : au-dessous de 3 000 caractères utiles une
        #    page est une façade ou un mur, donc « la citation n'y est pas » et « personne n'a pu
        #    la lire » rendent le MÊME verdict. Les contrôles disent précisément « pages non lues » ;
        #    l'excuser est donc la MÊME excuse qu'un 000, et non une seconde, plus large.
        #    ⛔ Et `None` n'est JAMAIS une façade : c'est l'ABSENCE de mesure (PDF, corps vide,
        #    transfert coupé). Une page non mesurée est traitée comme VIVANTE, donc REFUSÉE — le
        #    défaut va vers le refus, jamais vers l'excuse.
        car = mesure(u)
        if car is not None and car < PLANCHER_LISIBLE:
            muettes.append((u, c, car))
        else:
            vivantes.append((u, c))
    av = ("faisceau de certificats : utilisé" if faisceau and os.path.exists(faisceau)
          else "⚠️ SANS faisceau de certificats — une page tombée par défaut de TLS serait excusée à tort")
    if vivantes:
        # ⚠️ 25/10/2026 — ET LE CONTRÔLE, LUI, SONDE SANS FAISCEAU : les trois scripts 5 bis
        #    appellent curl sans --cacert (mesuré sur leur source). Une page que le harnais lit
        #    en 200 et que le contrôle n'a pas lue peut donc être un défaut de PILE TLS du
        #    contrôle, pas du document. On ne tranche pas à sa place : on nomme les deux.
        return False, ("%s répond (HTTP %s) quand le contrôle ne l'a pas lue — le refus n'est PAS "
                       "une panne de la page : document, ou pile TLS du contrôle (faisceau, "
                       "18/10/2026) [%s]" % (vivantes[0][0], vivantes[0][1], av))
    if muettes:
        return True, ("page(s) MUETTE(S) mesurée(s) ici — elles répondent et ne disent rien, donc "
                      "« citation absente » et « page non lue » sont indiscernables (plancher du "
                      "dépôt : %d caractères utiles) : %s ; injoignable(s) : %s — rien n'est "
                      "conclu, le duo n'est pas joué [%s]"
                      % (PLANCHER_LISIBLE,
                         ", ".join("%s (HTTP %s, %d car.)" % m for m in muettes),
                         ", ".join(u for u in urls if u not in [m[0] for m in muettes]) or "aucune",
                         av))
    return True, ("page(s) injoignable(s) mesurée(s) ici : %s — le témoin n'a pas changé, la page "
                  "si : rien n'est conclu, le duo n'est pas joué [%s]" % (", ".join(urls), av))


# ─────────────────────────── bornes (serveur local, aucun tiers) ───────────────────────────
MORTE = "https://temoin-harnais-page-morte.invalid/p"   # RFC 2606 : ne résout jamais, par norme


def _docx(chemin, urls):
    rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships '
            'xmlns="http://schemas.openxmlformats.org/package/2006/relationships">']
    for i, u in enumerate(urls, 1):
        rels.append('<Relationship Id="rId%d" Type="http://schemas.openxmlformats.org/'
                    'officeDocument/2006/relationships/hyperlink" Target="%s" '
                    'TargetMode="External"/>' % (i, u))
    rels.append("</Relationships>")
    with zipfile.ZipFile(chemin, "w") as z:
        z.writestr("word/_rels/document.xml.rels", "".join(rels))
        z.writestr("word/document.xml", "<w:document><w:body/></w:document>")
    return chemin


def autotest():
    import http.server, socketserver, tempfile, threading

    # ⚠️ 28/11/2026 — DEUX PAGES, et la riche est devenue NÉCESSAIRE. Le serveur ne servait
    #    qu'un corps de deux octets : depuis que la condition ④ distingue une page MUETTE d'une
    #    page vivante, cette page de deux caractères était excusée, et la borne ② — « une page
    #    qui répond accuse » — tombait. Elle ne testait donc plus ce qu'elle annonce. `/p` sert
    #    désormais ~6 000 caractères utiles (au-dessus du plancher de 3 000) et `/mur` les deux
    #    octets d'origine, qui exercent la page muette.
    class H(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            corps = b"ok" if self.path.startswith("/mur") else (b"<p>" + b"mot " * 1500 + b"</p>")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(corps)))
            self.end_headers()
            self.wfile.write(corps)
        def log_message(self, *a):
            pass

    srv = socketserver.TCPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    VIVE = "http://127.0.0.1:%d/p" % srv.server_address[1]       # répond ET dit quelque chose
    MUR = "http://127.0.0.1:%d/mur" % srv.server_address[1]      # répond et ne dit rien
    tmp = tempfile.mkdtemp(prefix="tolpm.")
    ko = vus = 0

    def essai(nom, sortie, urls_doc, attendu, motif, mesure=None):
        nonlocal ko, vus
        vus += 1
        s = os.path.join(tmp, nom + ".txt")
        open(s, "w", encoding="utf-8").write(sortie)
        d = _docx(os.path.join(tmp, nom + ".docx"), urls_doc)
        exc, raison = verdict(s, d, faisceau=chemin_faisceau(), mesure=mesure)
        if exc != attendu or (motif and motif not in raison):
            print("  ✗ %s : excusé=%s (attendu %s) — %s" % (nom, exc, attendu, raison))
            ko += 1

    # ① le cas réel du 23 et du 25/10/2026, forme d'astrologie, page morte PAR NORME
    essai("astro-page-morte",
          "⑦ PAGE SANS RÉPONSE, NON DÉCLARÉE (%s : code 000 après 3 essais) : ¶19, ¶115\n"
          "REFUSÉ — 1 motif(s) : page sans réponse …oin-harnais-page-morte.invalid/p\n" % MORTE,
          [MORTE], True, "injoignable")
    # ② LA MÊME SORTIE sur une page QUI RÉPOND : le refus est dans le document → on bloque
    essai("page-vivante",
          "⑦ PAGE SANS RÉPONSE, NON DÉCLARÉE (%s : code 000 après 3 essais) : ¶19\n"
          "REFUSÉ — 1 motif(s) : page sans réponse …\n" % VIVE,
          [VIVE], False, "répond (HTTP 200) quand le contrôle ne l'a pas lue")
    # ③ deux motifs, une seule ligne imputable à une page : l'autre défaut est réel
    essai("deux-motifs-une-page",
          "① LIGATURE PERDUE (¶3) : « Noeud Nord… »\n"
          "⑦ PAGE SANS RÉPONSE, NON DÉCLARÉE (%s : code 000 après 3 essais) : ¶19\n"
          "REFUSÉ — 2 motif(s) : ¶3 ligature | page sans réponse …\n" % MORTE,
          [MORTE], False, "2 motif(s) annoncé(s), 1 apparié(s)")
    # ④ un motif qui ne nomme AUCUNE page, alors qu'une page du témoin est morte
    essai("motif-sans-page",
          "① LIGATURE PERDUE (¶3) : « Noeud Nord… »\n"
          "REFUSÉ — 1 motif(s) : ¶3 ligature\n",
          [MORTE], False, "sans page : ¶3 ligature")
    # ⑤ ANTI-MENSONGE : la sortie nomme une page morte qui n'est PAS dans le témoin
    essai("page-hors-temoin",
          "⑦ PAGE SANS RÉPONSE, NON DÉCLARÉE (%s : code 000 après 3 essais) : ¶19\n"
          "REFUSÉ — 1 motif(s) : page sans réponse …\n" % MORTE,
          ["https://autre-chose.invalid/q"], False, "sans page : page sans réponse")
    # ⑥ la forme de controle_ai_act.py — sortie sur stderr, synthèse SANS compteur
    essai("ai-act-citation-courte",
          "CITATION COURTE ABSENTE DES PAGES DE LA NOTE : « acte délégué » (¶4) — "
          "pages non lues : %s\nNOTE REFUSÉE — citation courte « acte délégué »\n" % MORTE,
          [MORTE], True, "injoignable")
    # ⑦ la forme de controle_psychopathologie.py, DEUX motifs séparés par « ; »
    essai("psycho-deux-points-virgules",
          "PAGE HAS DE PRÉSENTATION SANS SON DOCUMENT : %s\n"
          "PAGE HAS DE PRÉSENTATION SANS SON DOCUMENT : %s\n"
          "LEÇON REFUSÉE — page %s ; page %s\n" % (MORTE, MORTE + "2", MORTE, MORTE + "2"),
          [MORTE, MORTE + "2"], True, "injoignable")
    # ⑧ une forme de synthèse inconnue ne s'excuse pas : on ne compte pas ce qu'on ne lit pas
    essai("forme-inconnue",
          "Traceback (most recent call last):\n  File \"x\", line 1\nKeyError: 'word/document.xml'\n",
          [MORTE], False, "aucune synthèse de refus connue")
    # ⑨ une sortie VIDE (contrôle tué, plafond, signal) ne s'excuse pas non plus
    essai("sortie-vide", "", [MORTE], False, "aucune synthèse de refus connue")

    # ⑪ UNE PAGE QUI RÉPOND ET NE DIT RIEN EXCUSE (28/11/2026). Règle du 12/10 du dépôt : sous
    #    3 000 caractères utiles, « la citation n'y est pas » et « personne n'a pu la lire » sont
    #    le MÊME verdict. Les contrôles écrivent précisément « pages non lues ».
    essai("page-muette",
          "CITATION COURTE ABSENTE DES PAGES DE LA NOTE : « acte délégué » (¶4) — "
          "pages non lues : %s\nNOTE REFUSÉE — citation courte « acte délégué »\n" % MUR,
          [MUR], True, "MUETTE")
    # ⑫ ACCEPTÉE ET DÉCISIVE : `None` N'EST PAS UNE FAÇADE, c'est l'ABSENCE de mesure (PDF, corps
    #    vide, transfert coupé). Une page non mesurée est traitée comme VIVANTE, donc REFUSÉE : le
    #    défaut va vers le refus. Sans cette borne, rien n'empêche de confondre None et 0 — et à
    #    0 caractère l'excuse serait la plus sûre d'elle-même (les 11 adresses à 202 et corps vide
    #    du balayage du 05/11).
    essai("non-mesurable-accuse",
          "⑦ PAGE SANS RÉPONSE, NON DÉCLARÉE (%s : code 000 après 3 essais) : ¶19\n"
          "REFUSÉ — 1 motif(s) : page sans réponse …\n" % VIVE,
          [VIVE], False, "répond (HTTP 200)", lambda u: None)
    # ⑬ LA FORME DE `controle_attributions.py` — elle n'énumère RIEN, donc profil « lignes
    #    bloquantes ». C'est le cas réel du 22/11 : `capsurvous.com` ne résout plus, et le témoin
    #    conforme d'ennéagramme n°6 bloquait TOUS les pushs du dépôt.
    essai("attributions-lien-mort",
          "      INTERDIT %s - HTTP 000, curl 6 : LE NOM DE DOMAINE NE RESOUT PAS, le document "
          "le cite comme vivant (㉞)\n"
          "VERDICT : 1 probleme(s) bloquant(s) (A + A2 + A3 + A4 + A5 + A6 + B + B-FR + B-N)\n"
          % MORTE, [MORTE], True, "injoignable")
    # ⑭ et le comptage de ce profil mord : 2 annoncés, 1 seule ligne bloquante nommant une page.
    essai("attributions-compte-faux",
          "      INTERDIT %s - HTTP 000, curl 6 : LE NOM DE DOMAINE NE RESOUT PAS (㉞)\n"
          "VERDICT : 2 probleme(s) bloquant(s) (A + A2 + A3)\n" % MORTE,
          [MORTE], False, "2 motif(s) bloquant(s) annoncé(s) mais 1 ligne")
    # ⑮ ACCEPTÉE — UNE LIGNE D'EXEMPTION N'EST PAS UN MOTIF. C'est le défaut mesuré du 28/11 sur
    #    le témoin ai-act du 16/10 : `TAILLE NON COMPARÉE` nomme une page du témoin sans accuser
    #    personne, portait le compte à 3 pour 2 motifs annoncés, et l'excuse était refusée.
    #    Ici les trois pages sont mortes : SEUL le comptage est en jeu.
    essai("exemption-nest-pas-motif",
          "CITATION COURTE ABSENTE DES PAGES DE LA NOTE : « 05 October 2026 » (¶25) — "
          "pages non lues : %s\n"
          "TAILLE ANNONCÉE FAUSSE (¶80) : 18111 annoncés contre 16369 mesurés pour %s\n"
          "TAILLE NON COMPARÉE (¶81) : %s est une page d'index — exemptée de ⑩\n"
          "NOTE REFUSÉE — citation courte « 05 October 2026 » ; taille 18111 vs 16369\n"
          % (MORTE, MORTE + "2", MORTE + "3"),
          [MORTE, MORTE + "2", MORTE + "3"], True, "injoignable")
    # ⑯ ACCEPTÉE — ET SEULES LES LIGNES APPARIÉES SONT SONDÉES. Même sortie, mais la page de la
    #    ligne d'EXEMPTION répond et dit quelque chose : si l'ensemble sondé était « toutes les
    #    lignes nommant une page », la condition ④ refuserait. Cette borne tombe SEULE quand on
    #    recollecte les URL sur `lignes_adr` au lieu des lignes appariées — sa contribution est
    #    donc séparable de celle de ⑮ (règle du 12/11/2026).
    essai("exemption-nest-pas-sondee",
          "CITATION COURTE ABSENTE DES PAGES DE LA NOTE : « 05 October 2026 » (¶25) — "
          "pages non lues : %s\n"
          "TAILLE ANNONCÉE FAUSSE (¶80) : 18111 annoncés contre 16369 mesurés pour %s\n"
          "TAILLE NON COMPARÉE (¶81) : %s est une page d'index — exemptée de ⑩\n"
          "NOTE REFUSÉE — citation courte « 05 October 2026 » ; taille 18111 vs 16369\n"
          % (MORTE, MORTE + "2", VIVE),
          [MORTE, MORTE + "2", VIVE], True, "injoignable")
    # ⑰ L'ANTI-MENSONGE ③ VAUT AUSSI POUR LE PROFIL « LIGNES BLOQUANTES » : une ligne bloquante
    #    qui nomme une page ABSENTE du témoin ne compte pas, donc le compte rate, donc on refuse.
    essai("attributions-page-hors-temoin",
          "      INTERDIT https://autre-chose.invalid/q - HTTP 000, curl 6 : NE RESOUT PAS (㉞)\n"
          "VERDICT : 1 probleme(s) bloquant(s) (A + A2)\n",
          [MORTE], False, "1 motif(s) bloquant(s) annoncé(s) mais 0 ligne")

    # ⑱ LE HARNAIS APPELLE-T-IL CETTE TOLÉRANCE DANS LE BLOC DES TÉMOINS CONFORMES ? (28/11/2026)
    #    Elle gardait le bloc des étapes 5 bis depuis le 25/10 et le bloc des conformes n'en avait
    #    AUCUNE : il concluait « faux positif du contrôle » sans jamais demander si la page n'avait
    #    pas disparu. *Une alerte que personne ne lit n'existe pas* (27/10) — ici c'était un outil
    #    que personne n'appelait.
    #    ⛔ FENÊTRE STRUCTURELLE, jamais un nombre de caractères : du `CONF_N=0` qui ouvre la boucle
    #    des conformes au `ATTENDU_CONFORMES` qui la referme. Une fenêtre en dur est tombée le
    #    17/11 sur deux lignes de commentaire ajoutées.
    #    ⚠️ BORNE LITTÉRALE, et c'est dit : prouver l'EFFET demanderait un --complet (~25 min de
    #    réseau sur des tiers), même parti que le garde ② de l'assertion de tableau (18/10) et
    #    que desarmement_git.py (27/10).
    vus += 1
    HARN = os.path.join(RACINE, "outils", "scripts", "non_regression.sh")
    try:
        h = open(HARN, encoding="utf-8").read()
        # ⚠️ la borne de FIN se cherche APRÈS le début : `ATTENDU_CONFORMES` est aussi défini
        #    en tête du harnais, et `find` depuis 0 y tombait — fenêtre VIDE, borne qui accuse un
        #    câblage juste. Elle l'a DIT (« 0 octets ») au lieu de passer en silence.
        i = h.find("CONF_N=0")
        j = h.find("ATTENDU_CONFORMES", i) if i >= 0 else -1
        fen = h[i:j] if 0 <= i < j else ""
    except OSError:
        fen = ""
    if "tolerance_page_morte.py" not in fen:
        print("  ✗ câblage : le bloc des témoins conformes de non_regression.sh n'appelle PAS "
              "tolerance_page_morte.py (fenêtre CONF_N=0 → ATTENDU_CONFORMES, %d octets) — un "
              "témoin dont la page est morte y conclurait « faux positif du contrôle » et "
              "refuserait TOUS les pushs, comme le 22/11/2026" % len(fen))
        ko += 1

    # ⑩ LA SONDE DOIT TROUVER LE FAISCEAU QUAND IL EXISTE — c'est le bug ① ci-dessus, et il
    #    était SILENCIEUX : sans faisceau, une page qui tombe par défaut de TLS est excusée à tort,
    #    donc l'excuse s'élargirait toute seule. Sur une machine SANS brew ca-certificates, le
    #    faisceau est légitimement absent (le dépôt retombe sur le magasin système) : la prémisse
    #    est alors fausse et la borne passe — elle le dit.
    # 🔴 ET LA PREMIÈRE VERSION DE CETTE BORNE NE MORDAIT PAS : elle cherchait le faisceau à
    #    os.path.join(RACINE, …), donc avec le MÊME RACINE faux que le code testé — le fichier
    #    n'existait pas, la prémisse était fausse, la borne passait. Le sabotage ⑥ sortait en 0.
    #    Elle part désormais des deux chemins ABSOLUS de brew, qui sont des faits de la machine :
    #    on copie une CONSTANTE, jamais l'arithmétique de chemin, qui est ce qu'on teste.
    vus += 1
    BREW_ = ("/usr/local/etc/ca-certificates/cert.pem",
             "/opt/homebrew/etc/ca-certificates/cert.pem")
    if any(os.path.exists(b) for b in BREW_):
        f = chemin_faisceau()
        if not (f and os.path.exists(f)):
            print("  ✗ faisceau : brew porte ses racines sur cette machine, mais chemin_faisceau() "
                  "rend %r — RACINE est faux ou l'import échoue, et les sondes partiraient sans "
                  "--cacert EN SILENCE : une page tombée par TLS serait EXCUSÉE au lieu d'être "
                  "dénoncée" % (f,))
            ko += 1
    else:
        print("  ○ faisceau : brew ca-certificates absent de cette machine — borne inerte, le dépôt "
              "retombe sur le magasin système (prévu par ca_bundle.py)")

    srv.shutdown()
    for f in sorted(os.listdir(tmp)):
        os.remove(os.path.join(tmp, f))
    os.rmdir(tmp)
    if ko:
        print("  ✗ %d/%d borne(s) de tolerance_page_morte.py en échec" % (ko, vus))
        return 1
    print("  ✓ %d/%d bornes de tolerance_page_morte.py — une page morte excuse, une page vivante"
          " accuse" % (vus, vus))
    return 0


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--autotest":
        sys.exit(autotest())
    if len(sys.argv) != 3:
        sys.exit("usage : tolerance_page_morte.py <sortie.txt> <témoin.docx>  |  --autotest")
    ok, pourquoi = verdict(sys.argv[1], sys.argv[2], faisceau=chemin_faisceau())
    print(pourquoi)
    sys.exit(0 if ok else 1)
