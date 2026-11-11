#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Les livrables PUBLIÉS sont-ils intacts sur le disque ?

POURQUOI — INCIDENT DU 10/11/2026, RENDU VISIBLE LE 11/11 PAR UN PUSH REFUSÉ.
kDrive a réécrit TROIS livrables publiés, tous à la même seconde (19:19:42) :
  · psychopathologie n°11 .md   : 4 393 o du contenu de a8285ab + 3 106 NUL contigus
  · psychopathologie n°11 .docx : zip VALIDE, CRC justes, horodatage interne INCHANGÉ,
                                  mais 19 058 caractères au lieu de 27 058 (−29,6 %)
  · appli-ia n°04 .docx         : idem, 26 525 au lieu de 37 840 (−29,9 %)
L'information était dans `git status` depuis cinq jours — trois lignes « M » — et
PERSONNE NE L'A LUE. Ce qui l'a dite, c'est le diff avec la référence du harnais,
qui a refusé un push en nommant « 0 → 1 bloquant(s) » : un contrôle écrit pour
autre chose, cinq jours trop tard. « Une alerte que personne ne lit n'existe pas. »

⛔ CE QUE CE CONTRÔLE N'EST PAS : un remplaçant de `git status`. git voit les trois
fichiers. Ce qu'il ne sait pas dire, c'est si un « M » est une CORRECTION EN COURS ou
une CORRUPTION — et c'est la seule question qui décide du geste. Ce contrôle classe.

🔴 ET LA MESURE A DÉMOLI L'HYPOTHÈSE ÉVIDENTE. « Le disque est revenu à une révision
passée » ne couvre QUE le .md : les deux .docx abîmés ne sont AUCUN blob de tout
l'historique (2 904 objets), ils s'ouvrent, leurs CRC sont justes, et leur
`dcterms:modified` est identique à celui du fichier publié. Une signature de
conteneur ne les voit pas. Ce qui les voit est la PERTE DE TEXTE.

BORNES, TOUTES MESURÉES SUR LE CORPUS LE 11/11/2026 :
  · NUL     — 0 fichier sur 360 du périmètre texte en porte un → 0 faux positif
  · ZIP     — 0 conteneur sur 395 refuse de s'ouvrir, CRC compris → 0 faux positif
  · AMPUTÉ  — 189 transitions .docx de l'historique : perte maximale LÉGITIME 15,58 %
              (une note controle-livrables réécrite), médiane +11,93 %, 0 transition
              au-delà de 20 %. L'incident est à 29,6 % et 29,9 %. Plancher à 20 % :
              BANDE VIDE DE 14 POINTS, et 0 faux positif sur les 189.
  · REVENU  — contenu du disque, NUL finaux rognés, égal à un blob PASSÉ de ce chemin
              (celui de HEAD exclu). Un éditeur ne rend jamais une révision passée.

⛔ `DIVERGENT` N'EST PAS BLOQUANT, ET C'EST LE POINT : un fichier qui diffère de HEAD
sans porter aucune signature ci-dessus est indiscernable d'une correction en cours.
Le contrôle le DIT et ne tranche pas. En production, un faux refus coûte un livrable
non publié (règle du 14/10).

⚠️ LES CINQ AUTRES CLASSES SONT BLOQUANTES DÈS LE PREMIER JOUR, et cela déroge en
apparence à la règle du 14/10 (« avertir sur des éditions neuves avant de bloquer ») :
ABSENT, NUL, ZIP et REVENU ne jugent pas un CONTENU, elles jugent si le fichier
publié est encore LISIBLE — même famille que le bloc `0 nonies` (26/10) et que
`corps_tronque.py` (04/11), rendus bloquants aussitôt pour cette raison. AMPUTÉ est
le cas limite : il lit un contenu. Ce qui le justifie n'est pas un argument mais la
bande de 14 points, et le fait qu'AUCUN ordre de la doctrine ne retire du texte —
« corrige X » AJOUTE un marqueur et une ligne de journal.

⚠️ CE QU'IL NE VOIT PAS, ET C'EST DIT :
  · un livrable abîmé AVANT son commit : le disque et HEAD concordent, tout est vert.
    Ce contrôle compare au dépôt, pas à la vérité.
  · une amputation de moins de 20 %, ou de n'importe quelle taille dans un .pptx ou
    un .xlsx : le plancher n'a été mesuré que sur les .docx.
  · un script de correction surpris ENTRE sa troncature et sa reconstruction rendrait
    un AMPUTÉ légitime. La doctrine sauvegarde puis patche, elle ne tronque pas.
  · les .pdf et les fichiers sans extension sont binaires et hors du test NUL.

Usage :  controle_integrite_livrables.py            → verdict sur le dépôt, exit 0/1
         controle_integrite_livrables.py --autotest → bornes, aucun réseau
"""
import hashlib, io, os, pathlib, re, subprocess, sys, zipfile

RACINE = pathlib.Path(__file__).resolve().parent.parent.parent
# ⚠️ TROIS parent : ce script vit dans outils/scripts/. Deux donnaient outils/, où
# `git ls-files` rendait ZÉRO fichier — et le verdict imprimait « 0 divergence(s) »
# avec exit 0, c'est-à-dire UN VERT SUR UN PÉRIMÈTRE JAMAIS REGARDÉ. Défaut mesuré au
# premier essai le 11/11/2026 ; même bug que tolerance_page_morte.py (23/10) et
# coherence_skill.py (27/10). La borne ⑥ de l'auto-test le garde désormais.
assert (RACINE / "jobs_config.json").exists(), (
    "RACINE ne pointe pas sur la racine du dépôt : %s" % RACINE)

# ──8<── CLASSIFICATION — extraite telle quelle par non_regression/integrite_livrables.py ──8<──
BLANCHE = ("sources/veille/", "livrables/lecons/", "livrables/quiz/", "livrables/infographies/",
           "livrables/projets/", "livrables/controles/", "livrables/documents/")
TEXTE = (".md", ".txt", ".json", ".csv", ".js", ".ts", ".tsx", ".mts", ".css", ".html", ".example")
CONTENEUR = (".docx", ".pptx", ".xlsx")
SEUIL_AMPUTE = 20.0   # % de texte perdu ; bande mesurée : légitime <= 15,58, incident >= 29,6

def sha1_blob(b):
    """L'empreinte que git donne à un contenu."""
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()

def caracteres(brut):
    """Caractères de texte d'un .docx. None si on ne peut pas les lire.
    ⚠️ <w:t[^>]*> apparierait AUSSI <w:tbl>, <w:tc>, <w:tr> (défaut mesuré le 11/11)."""
    try:
        d = zipfile.ZipFile(io.BytesIO(brut)).read("word/document.xml").decode("utf-8", "replace")
    except Exception:
        return None
    return len("".join(re.findall(r"<w:t(?:\s[^>]*)?>(.*?)</w:t>", d, re.S)))

def zip_casse(brut):
    """Raison pour laquelle ce conteneur n'est pas lisible, ou None."""
    try:
        z = zipfile.ZipFile(io.BytesIO(brut))
        mauvais = z.testzip()
        if mauvais:
            return "CRC faux sur %s" % mauvais
        for i in z.infolist():
            z.read(i.filename)
    except Exception as e:
        return "%s : %s" % (type(e).__name__, str(e)[:60])
    return None

def classe(brut_disque, brut_head, chemin, blobs_passes):
    """(classe, détail, bloquant) — (None, None, False) si le livrable est intact.
    brut_disque vaut None quand le fichier a disparu du disque.
    blobs_passes : sha1 des blobs PASSÉS de ce chemin, celui de HEAD EXCLU."""
    suffixe = pathlib.PurePath(chemin).suffix
    if brut_disque is None:
        return ("ABSENT", "suivi à HEAD (%d o), disparu du disque" % len(brut_head), True)
    if brut_disque == brut_head:
        return (None, None, False)
    # ① un livrable TEXTE ne contient jamais d'octet NUL — 0 sur 360 mesuré
    if suffixe in TEXTE and b"\0" in brut_disque:
        rogne = brut_disque.rstrip(b"\0")
        suite = ""
        if sha1_blob(rogne) in blobs_passes:
            suite = ", et le contenu rogné EST une révision passée (%s)" % sha1_blob(rogne)[:7]
        return ("NUL", "%d octet(s) NUL dont %d finaux contigus%s"
                % (brut_disque.count(b"\0"), len(brut_disque) - len(rogne), suite), True)
    # ② le disque est revenu à une révision passée de ce même chemin
    for libelle, contenu in (("tel quel", brut_disque), ("NUL finaux rognés", brut_disque.rstrip(b"\0"))):
        s = sha1_blob(contenu)
        if s in blobs_passes:
            return ("REVENU", "%s = blob passé %s de ce chemin" % (libelle, s[:7]), True)
    # ③ un conteneur qui ne s'ouvre plus — 0 sur 395 mesuré
    if suffixe in CONTENEUR:
        raison = zip_casse(brut_disque)
        if raison:
            return ("ZIP", raison, True)
    # ④ un .docx qui s'ouvre mais dont le texte a fondu — plancher mesuré, bande de 14 points
    if suffixe == ".docx":
        cd, ch = caracteres(brut_disque), caracteres(brut_head)
        if cd is not None and ch:
            perte = (ch - cd) / ch * 100.0
            if perte >= SEUIL_AMPUTE:
                return ("AMPUTÉ", "%d caractères sur disque contre %d à HEAD : −%.1f %%"
                        % (cd, ch, perte), True)
    # ⑤ divergent sans signature : correction en cours OU corruption. On ne tranche pas.
    return ("DIVERGENT", "%d o sur disque contre %d à HEAD — correction en cours ou corruption, "
            "ce contrôle ne tranche pas" % (len(brut_disque), len(brut_head)), False)
# ──8<── FIN CLASSIFICATION ──8<──

def _git(args, racine):
    return subprocess.run(["git"] + args, cwd=str(racine), capture_output=True).stdout

def blobs_du_chemin(chemin, racine, sha_head):
    """sha1 des blobs PASSÉS de ce chemin (renommages suivis), celui de HEAD exclu."""
    revs = _git(["log", "--follow", "--format=%H", "--", chemin], racine).decode().split()
    vus = set()
    base = pathlib.PurePath(chemin).name
    for r in revs:
        for ligne in _git(["ls-tree", "-r", r], racine).decode("utf-8", "replace").splitlines():
            _, sep, reste = ligne.partition(" blob ")
            if not sep:
                continue
            sha, _, p = reste.partition("\t")
            if pathlib.PurePath(p).name == base:
                vus.add(sha)
    vus.discard(sha_head)
    return vus

def verdict(racine=RACINE):
    suivis = [p.decode() for p in _git(["ls-files", "-z"], racine).split(b"\0")
              if p and p.decode().startswith(BLANCHE)]
    # ne lire l'historique que des fichiers qui diffèrent : le reste est intact par égalité
    differents = set(p.decode() for p in
                     _git(["diff", "--name-only", "-z", "HEAD", "--"] + list(BLANCHE), racine).split(b"\0") if p)
    non_suivis = [p.decode() for p in
                  _git(["ls-files", "-z", "--others", "--exclude-standard"] + list(BLANCHE), racine).split(b"\0") if p]
    # un SEUL ls-tree au lieu de 758 rev-parse : 12,3 s → moins d'une seconde.
    # Un hook long tue la connexion SSH du push (mesuré les 26/10 et 31/10).
    shas = {}
    for ligne in _git(["ls-tree", "-r", "HEAD"], racine).decode("utf-8", "replace").splitlines():
        _, sep, reste = ligne.partition(" blob ")
        if sep:
            sha, _, chem = reste.partition("\t")
            shas[chem] = sha
    trouves, bloquants = [], 0
    for chemin in sorted(suivis):
        f = pathlib.Path(racine, chemin)
        if chemin not in differents and f.exists():
            continue
        sha_head = shas.get(chemin)
        if not sha_head:
            continue
        brut_head = _git(["cat-file", "blob", sha_head], racine)
        brut_disque = f.read_bytes() if f.exists() else None
        c, detail, bloq = classe(brut_disque, brut_head, chemin, blobs_du_chemin(chemin, racine, sha_head))
        if c:
            trouves.append((c, chemin, detail, bloq))
            bloquants += bloq
    print("INTÉGRITÉ DES LIVRABLES PUBLIÉS : %d suivi(s) dans la liste blanche · "
          "%d divergence(s) · %d bloquante(s) · %d non suivi(s)"
          % (len(suivis), len(trouves), bloquants, len(non_suivis)))
    for c, chemin, detail, bloq in sorted(trouves, key=lambda t: (not t[3], t[0])):
        print("  %s %-9s %s — %s" % ("⛔" if bloq else "⚠️ ", c, chemin, detail))
    if non_suivis:
        print("  ⓘ  %d fichier(s) de la liste blanche non suivi(s) — NON accusés, "
              "ce contrôle juge l'intégrité du PUBLIÉ :" % len(non_suivis))
        for p in non_suivis[:10]:
            print("       %s" % p)
    if bloquants:
        print("  ⛔ RESTAURER DEPUIS LE DÉPÔT : git checkout -- <chemin>   "
              "(le contenu de git est celui qui a été publié)")
    return 1 if bloquants else 0

def autotest():
    ko, jouees = [], []
    def borne(nom, condition):
        jouees.append(nom)
        if not condition:
            ko.append(nom)
    b_head = b"x" * 100
    borne("un fichier identique a HEAD est intact",
          classe(b_head, b_head, "livrables/lecons/a/x.md", set())[0] is None)
    borne("un fichier absent du disque est ABSENT",
          classe(None, b_head, "livrables/lecons/a/x.md", set())[0] == "ABSENT")
    borne("un .md avec un octet NUL est NUL",
          classe(b"abc\0\0", b"abcd", "livrables/lecons/a/x.md", set())[0] == "NUL")
    borne("un .pdf avec un octet NUL n'est PAS NUL (binaire legitime)",
          classe(b"abc\0\0", b"abcd", "livrables/documents/x.pdf", set())[0] != "NUL")
    borne("le contenu rogne egal a un blob passe est REVENU",
          classe(b"ancien\0\0", b"nouveau", "livrables/documents/x.pdf",
                 {sha1_blob(b"ancien")})[0] == "REVENU")
    borne("un .docx qui perd 30 % de son texte est AMPUTE", True)   # exercée ci-dessous
    jouees.pop(); ko[:] = [k for k in ko if k != "un .docx qui perd 30 % de son texte est AMPUTE"]
    def docx(n):
        import io as _io, zipfile as _z
        b = _io.BytesIO()
        with _z.ZipFile(b, "w") as z:
            z.writestr("word/document.xml", "<w:document><w:t>" + "a" * n + "</w:t></w:document>")
        return b.getvalue()
    borne("un .docx qui perd 30 %% de son texte est AMPUTE",
          classe(docx(700), docx(1000), "livrables/lecons/a/x.docx", set())[0] == "AMPUTÉ")
    borne("un .docx qui perd 15 %% est DIVERGENT, pas AMPUTE (borne a ACCEPTER)",
          classe(docx(850), docx(1000), "livrables/lecons/a/x.docx", set())[0] == "DIVERGENT")
    borne("un .docx qui ne s'ouvre plus est ZIP",
          classe(b"pas un zip", docx(1000), "livrables/lecons/a/x.docx", set())[0] == "ZIP")
    borne("DIVERGENT n'est PAS bloquant",
          classe(docx(850), docx(1000), "livrables/lecons/a/x.docx", set())[2] is False)
    borne("les cinq autres classes SONT bloquantes",
          all(classe(*a)[2] for a in (
              (None, b"x", "livrables/lecons/a/x.md", set()),
              (b"a\0", b"ab", "livrables/lecons/a/x.md", set()),
              (b"ancien", b"neuf", "livrables/documents/x.pdf", {sha1_blob(b"ancien")}),
              (b"pas un zip", docx(1000), "livrables/lecons/a/x.docx", set()),
              (docx(700), docx(1000), "livrables/lecons/a/x.docx", set()))))
    borne("RACINE est la racine du depot, pas outils/ — un perimetre VIDE n'est pas un depot propre",
          (RACINE / "jobs_config.json").exists() and (RACINE / "livrables").is_dir())
    print("%d/%d borne(s) jouée(s) de l'intégrité des livrables" % (len(jouees) - len(ko), len(jouees)))
    for n in ko:
        print("  ✗ %s" % n)
    return 1 if ko else 0

if __name__ == "__main__":
    sys.exit(autotest() if "--autotest" in sys.argv else verdict())
