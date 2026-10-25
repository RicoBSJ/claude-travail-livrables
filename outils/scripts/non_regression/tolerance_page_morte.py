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
ADRESSE = re.compile(r"https?://[^\s<>\"»,;)\]]+")


def nfc(s):
    return unicodedata.normalize("NFC", s)


def urls_du_docx(p):
    """Les adresses que le TÉMOIN porte vraiment — la sortie du contrôle ne fait pas foi (③)."""
    with zipfile.ZipFile(p) as z:
        rels = z.read("word/_rels/document.xml.rels").decode("utf-8", "ignore")
    return {m.group(1) for m in re.finditer(r'Target="(https?://[^"]+)"', rels)}


def motifs_annonces(texte):
    """(nombre de motifs, ligne de synthèse) ou (None, None) si la forme n'est pas connue (①)."""
    for ligne in texte.splitlines():
        l = ligne.strip()
        m = SYNTH_N.match(l)
        if m:
            return int(m.group(1)), ligne
        m = SYNTH_L.match(l)
        if m:
            return len([x for x in m.group(1).split(";") if x.strip()]), ligne
    return None, None


def chemin_faisceau():
    try:
        sys.path.insert(0, os.path.join(RACINE, "outils", "scripts"))
        import ca_bundle
        return ca_bundle.chemin()
    except Exception:
        return None


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


def verdict(sortie, docx, faisceau=None, sonde=None):
    """Rend (excusé, raison). Le sens d'échec du comptage est TOUJOURS le refus."""
    sonde = sonde or (lambda u: code_http(u, faisceau))
    try:
        texte = nfc(open(sortie, encoding="utf-8", errors="ignore").read())
    except OSError as e:
        return False, "sortie du contrôle illisible (%s)" % e
    try:
        doc = urls_du_docx(docx)
    except Exception as e:
        return False, "témoin illisible (%s) — on n'excuse pas ce qu'on ne peut pas vérifier" % e

    n, synth = motifs_annonces(texte)
    if n is None:
        return False, ("la sortie ne porte aucune synthèse de refus connue — on ne compte pas "
                       "ce qu'on ne sait pas lire")
    if n < 1:
        return False, "synthèse annonçant %d motif — rien à excuser" % n

    porteuses, urls = 0, []
    for ligne in texte.splitlines():
        if ligne == synth or not ligne.strip():
            continue
        vues = [a.rstrip(".,;:)»'\"") for a in ADRESSE.findall(ligne)]
        vues = [a for a in vues if a in doc]          # ③ l'adresse doit être DANS le témoin
        if vues:
            porteuses += 1
            urls += [a for a in vues if a not in urls]
    if porteuses != n:
        return False, ("%d motif(s) annoncé(s) mais %d ligne(s) nommant une page du témoin — "
                       "un refus qui n'est pas ENTIÈREMENT imputable à des pages ne s'excuse pas"
                       % (n, porteuses))

    vivantes = []
    for u in urls:                                    # ④ séquentiel, mesuré ici
        c = sonde(u)
        if c not in ("", "000"):
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

    class H(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Length", "2")
            self.end_headers()
            self.wfile.write(b"ok")
        def log_message(self, *a):
            pass

    srv = socketserver.TCPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    VIVE = "http://127.0.0.1:%d/p" % srv.server_address[1]
    tmp = tempfile.mkdtemp(prefix="tolpm.")
    ko = vus = 0

    def essai(nom, sortie, urls_doc, attendu, motif):
        nonlocal ko, vus
        vus += 1
        s = os.path.join(tmp, nom + ".txt")
        open(s, "w", encoding="utf-8").write(sortie)
        d = _docx(os.path.join(tmp, nom + ".docx"), urls_doc)
        exc, raison = verdict(s, d, faisceau=chemin_faisceau())
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
          [MORTE], False, "2 motif(s) annoncé(s) mais 1 ligne")
    # ④ un motif qui ne nomme AUCUNE page, alors qu'une page du témoin est morte
    essai("motif-sans-page",
          "① LIGATURE PERDUE (¶3) : « Noeud Nord… »\n"
          "REFUSÉ — 1 motif(s) : ¶3 ligature\n",
          [MORTE], False, "0 ligne(s)")
    # ⑤ ANTI-MENSONGE : la sortie nomme une page morte qui n'est PAS dans le témoin
    essai("page-hors-temoin",
          "⑦ PAGE SANS RÉPONSE, NON DÉCLARÉE (%s : code 000 après 3 essais) : ¶19\n"
          "REFUSÉ — 1 motif(s) : page sans réponse …\n" % MORTE,
          ["https://autre-chose.invalid/q"], False, "0 ligne(s)")
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
