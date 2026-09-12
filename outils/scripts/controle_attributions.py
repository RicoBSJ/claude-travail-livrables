#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""controle_attributions.py — test d'attribution des pages, commun à tous les parcours.

Usage : /usr/bin/python3 outils/scripts/controle_attributions.py <chemin du .docx>
Sort en 0 si aucun problème bloquant, en 1 sinon (et en 2 si le fichier est illisible).

Copie CANONIQUE, extraite verbatim du bloc embarqué dans le prompt appli-ia-lecon
(jobs_config.json) le 12/09/2026 — même contenu, même validation : dix-sept cas
connus, dans les deux sens, sous env -i. Historique des treize défauts du test
et de leurs corrections : outils/scripts/JOBS.md (journée du 11/09/2026) ; ⑭ le
12/09/2026, la passe A cesse d'ignorer un site nu cité comme source sans aucune page listée ;
⑮ le même jour, un guillemet droit collé à un chiffre (27") n'ouvre plus une citation ;
⑯ A4 ignore les lignes de décompte (« Sources : 6 ✅ … ») et lit « LDLC.com » comme un domaine.

Cinq passes : A pages nommées non listées et sites nus · A2 noms d'autorité sans
adresse · A3 identifiants (forme vérifiée, clé ISBN) · B citations anglaises de
huit mots ou plus cherchées dans les pages · C/C2 numéros de version (C2 bloquant
à moins de 80 caractères d'un domaine cité) · D valeurs chiffrées, à relire.
Lis toujours la ligne « PASSES INERTES » : une passe inerte n'a rien cherché.
"""
import sys, re, html, subprocess

DOCX = sys.argv[1]
EXTRACT = "/Users/utilisateur/kDrive/Claude_Travail/outils/scripts/extract_docx.py"
t = subprocess.run(["/usr/bin/python3", EXTRACT, DOCX],
                   capture_output=True, text=True).stdout
if "=== TEXTE COMPLET" not in t:
    sys.exit("EXTRACTION IMPOSSIBLE (fichier introuvable ou illisible) : " + DOCX)
sep = t.index("=== TEXTE COMPLET")
entete, corps = t[:sep], t[sep:]
# le journal des corrections cite VOLONTAIREMENT les formulations d'origine : on l'exclut
jrn = corps.find("Journal des corrections")
if jrn != -1:
    corps = corps[:jrn]
urls = sorted(set(re.findall(r"https?://[^\s)]+", entete)))
# ⑭ une adresse ecrite EN CLAIR dans le corps (cellule « URL » d'un tableau, ligne « Source : https://… »)
#    est une adresse donnee au lecteur, meme sans lien cliquable : elle compte comme listee
urls_texte = sorted(set(re.findall(r"https?://[^\s)>\]»]+", corps)))
urls = sorted(set(urls) | set(urls_texte))

# ── A. une page nommee dans le CORPS doit etre listee en Ressources
#    (on s'arrete avant la section Ressources : apres, tout est un libelle de lien)
#    ⚠️ ancre sur le TITRE (emoji compris) et non sur le mot « Ressources » : ce mot
#    apparait dans les notes de correction du corps, et un find() naif tronquait la
#    lecon avant ses numeros de version (bug attrape le 11/09/2026 sur la lecon 01).
res = corps.find("\U0001F4DA Ressources")
if res == -1:
    res = corps.rfind("Ressources")
avant_res = corps[:res] if res != -1 else corps
# ⚠️ PERIMETRE DEDUIT, PAS CODE EN DUR. Une liste de domaines ecrite a la main
#    perime en silence — c'est l'incident iMac et celui de l'etape 2 de serafin-ph.
#    On accepte tout nom de domaine plausible, et on EXCLUT les noms de fichiers
#    (serveur.js, package.json, index.css...) par une liste de TLD reels.
TLD = (r"com|org|net|fr|dev|io|gov|edu|uk|au|ca|ch|be|de|es|it|eu|info|int|co"
       r"|ai|app|me|tv|us|nl|se|no|jp|cn|in|ru|br|za|nz|at|dk|fi|pl|pt|gr|il|tsadra")
# ⑭ (12/09/2026) borne de mot des deux cotes et casse ignoree : sans elles, « Amazon.fr »
#    donnait « mazon.fr », « err.message » donnait « err.me », « path.setAttribute » « path.se » —
#    tous invisibles tant que les sites nus non listes etaient ignores. Et « www. » est neutralise.
DOM = r"(?<![A-Za-z0-9-])(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+(?:" + TLD + r")(?![A-Za-z0-9-])"
def sans_www(d):
    return re.sub(r"^www\.", "", d.lower())
doms_res = set(sans_www(d) for d in re.findall(r"^(?:https?://)?(" + DOM + r")",
                                               "\n".join(urls), re.M | re.I))
CODE = re.compile(r"curl|wget|\bPOST\b|\bGET\b|fetch\s*\(|\bbash\b|endpoint"
                  r"|x-api-key|Authorization|Content-Type|cl\u00e9 API|api[_ ]?key"
                  r"|URL\s*:|RSS|header|requests\.|axios|npm |npx ", re.I)
SOURCE = re.compile(r"source|consult|v\u00e9rifi|d'apr\u00e8s|selon|documentation"
                    r"|r\u00e9f\u00e9rence|cit\u00e9e?s?\b", re.I)
# ⑭ un site nu est « cite comme source » s'il est ATTRIBUE — un mot d'attribution juste AVANT
#    (« source : », « selon », « d'apres », « issu de », « via », « consulte sur »), sans point entre
#    les deux, ou juste APRES (« X, consultes », « X (sources secondaires) ») — et non s'il est donne
#    en CONSIGNE au lecteur (« verifiez sur », « va la verifier », « releve la position sur astro.com »)
#    ni declare NON consulte (« decret non consulte sur legifrance ») : une consigne n'attribue rien.
#    « sans point entre les deux » = sans FIN DE PHRASE (« . » suivi d'un blanc) : les points d'un
#    domaine voisin (« Sources : handicap.gouv.fr ✅ | cnsa.fr ») ne coupent pas la liste.
ATTRIB_AVANT = re.compile(r"(?:sources?\s*(?:primaires?|secondaires?|officielles?)?\s*:|\bsources?\s+\d+\s*[—:-]"
                          r"|\bselon\b|d['’]apr[eè]s|\bissus?\s+de|\bcit[ée]e?s?\s+(?:via|sur|dans)"
                          r"|\brelev[ée]e?s?\s+(?:sur|chez)|\bconsult[ée]e?s?\b)(?:(?!\.\s).){0,60}$", re.I | re.S)
ATTRIB_APRES = re.compile(r"(?:(?!\.\s).){0,40}?\b(?:consult[ée]e?s?\b|cit[ée]e?s?\b|sources?\s+secondaires?)", re.I | re.S)
NON_CONSULT = re.compile(r"\b(?:non|pas|jamais)\s+(?:été\s+)?consult", re.I)   # « n'a pas ete consulte » aussi
IMPER = re.compile(r"\b(?:vérifie[rz]?|consultez|relève[rz]?|cherche[rz]?|va\s+(?:la\s+|le\s+)?vérifier"
                   r"|à\s+vérifier|utilise[rz]?|ouvre[rz]?|teste[rz]?|rends-toi)\b", re.I)
def attribue(avant, apres):
    av = avant[-80:]
    if ATTRIB_AVANT.search(av) and not NON_CONSULT.search(av[-60:]) and not IMPER.search(av[-60:]):
        return True
    return bool(ATTRIB_APRES.match(apres[:40])) and not NON_CONSULT.search(apres[:40])
def liste(dom):
    """le domaine, ou l'un de ses sous-domaines, a une page listee"""
    return dom in doms_res or any(d.endswith("." + dom) for d in doms_res)
nues, orphelines, sites_non_listes = set(), set(), set()
for m in re.finditer(r"(" + DOM + r")((?:/[A-Za-z0-9._~:/#@!$&*+,;=%-]*)?)", avant_res, re.I):
    dom, chemin = sans_www(m.group(1)), m.group(2).rstrip("./,;:)")
    ctx = avant_res[max(0, m.start() - 120): m.end() + 120]
    if not liste(dom) and not chemin:
        # ⑭ (12/09/2026) un domaine nu cite COMME SOURCE dont AUCUNE page n'est listee etait
        #    ignore en silence, alors que la meme source nommee avec un chemin bloquait :
        #    nommer moins precisement faisait passer le test. Meme exigence pour les deux.
        if not CODE.search(ctx) and attribue(avant_res[max(0, m.start() - 80):m.start()], avant_res[m.end():m.end() + 40]):
            sites_non_listes.add(dom)
        continue          # sinon : domaine simplement mentionne, jamais cite comme source
    if (dom.startswith("api.") or re.search(r"\.(sh|ps1|bat)$", chemin)
            or CODE.search(ctx)) and not SOURCE.search(ctx):
        continue          # valeur de configuration, pas une source (regle 11)
    if not chemin:
        nues.add(dom)
    else:
        nus = [re.sub(r"^https?://(?:www\.)?", "", u.lower()) for u in urls]
        court = (dom + chemin).lower()
        seg = [x for x in chemin.split("/") if x][-1:] or [""]
        seg = [seg[0].lower()]
        meme_dom = [u for u in nus if u.startswith(dom)]
        if not any(court in u for u in nus) and not any(seg[0] and seg[0] in u
                                                        for u in meme_dom):
            orphelines.add(dom + chemin)
print("A. RESSOURCES LISTEES : %d" % len(urls))
for u in urls:
    print("     ", u)
print("   pages citees dans le corps et ABSENTES des Ressources :")
for o in sorted(orphelines):
    print("      INTERDIT", o)
print("      (aucune)" if not orphelines else "")
print("   sites cites comme source dont AUCUNE page n'est listee (meme exigence qu'une page) :")
for o in sorted(sites_non_listes):
    print("      INTERDIT", o)
print("      (aucun)" if not sites_non_listes else "")
print("   attributions au SITE NU, a preciser en page (une page du site est listee) :",
      sorted(nues) if nues else "(aucune)")

# ── A2. AUTORITE NOMMEE SANS ADRESSE : une norme citee est une source citee
#    (defaut du 06/09 sur la lecon 01 : « Cloud Security Alliance », « OX Security »
#     nommes sans aucune URL ; meme forme que RFC/ECMA/W3C/ISO cites sans lien)
#    ⑬ deux familles distinctes : les NOMS (a adresser) et les IDENTIFIANTS
#    (qui resolvent seuls, mais dont la forme se verifie).

def cle_isbn(s):
    """True/False si la cle de controle est valide, None si ce n'est pas un ISBN."""
    d = [ch for ch in s if ch.isdigit() or ch in "Xx"]
    if len(d) == 13 and all(ch.isdigit() for ch in d):
        t = sum((1 if i % 2 == 0 else 3) * int(ch) for i, ch in enumerate(d[:12]))
        return (10 - t % 10) % 10 == int(d[12])
    if len(d) == 10:
        t = sum((10 - i) * (10 if ch in "Xx" else int(ch)) for i, ch in enumerate(d[:9]))
        return (t + (10 if d[9] in "Xx" else int(d[9]))) % 11 == 0
    return None

# noms sans identifiant : il faut une adresse
NOMS = re.compile(r"\b(DSM-5(?:-TR)?|CIM-1[01]|ICD-1[01]|W3C|IETF|ECMAScript)\b", re.I)
# identifiants qui resolvent d'eux-memes : pas d'adresse exigee, mais forme verifiee
IDENT = re.compile(r"\b(ISBN[\s:]?[\d-]{10,17}[\dXx]?|doi[\s:]?10\.\d{4,9}/[^\s,;)]+"
                   r"|PMID[\s:]?\d{6,9}|PMC\d{6,9}|arXiv[:\s]?\d{4}\.\d{4,5}"
                   r"|RFC\s?\d{3,5}|ECMA-\d{3,4}|ISO[\s/]?\d{4,5})\b", re.I)

sans_adresse = set()
section_res = corps[res:] if res != -1 else ""
couverture = re.sub(r"[^A-Za-z0-9]", "", (section_res + " " + " ".join(urls))).lower()
for m in NOMS.finditer(avant_res):
    nom = re.sub(r"\s+", " ", m.group(1))
    if re.sub(r"[^A-Za-z0-9]", "", nom).lower() not in couverture:
        sans_adresse.add(nom)
identifiants, mal_formes = set(), set()
for m in IDENT.finditer(avant_res):
    ident = re.sub(r"\s+", " ", m.group(1)).strip()
    ok = cle_isbn(ident) if ident.lower().startswith("isbn") else None
    if ok is False:
        mal_formes.add(ident)
    else:
        identifiants.add(ident + ("  [cle valide]" if ok else ""))
# ── A4. « Source : … » sans adresse — une source qu'on nomme et qu'on date sans la lier
#    (placement-financier n°14, 12/09/2026 : « Source : AMF, annonce…, 31/05/2026 », sans
#     lien ; la page existait, la date etait un horodatage d'impression, un dimanche).
#    Une ligne « Source : » qui nomme quelque chose doit porter un domaine, sur elle-meme
#    ou sur les deux lignes qui la suivent (le lien est souvent a la ligne).
lignes = avant_res.split("\n")
src_sans_adresse = []
for idx, l in enumerate(lignes):
    # « Sources de données : … » (nocode-ia n°16) n'est pas une reference : seuls les
    # qualificatifs bibliographiques sont admis entre « Source » et les deux-points.
    m = re.match(r"\s*Sources?(?:\s+(?:primaires?|secondaires?|consult[ée]e?s?|utilis[ée]e?s?"
                 r"|officielles?|mobilis[ée]e?s?))*\s*:\s*(.*)$", l)
    if not m or not m.group(1).strip():
        continue                          # en-tete nu : le lien vient dessous
    # ⑯ (12/09/2026) une ligne de DECOMPTE (« Sources : 6 ✅ exploitées · 9 ⛔ ») ne nomme rien
    if re.match(r"\s*\d{1,2}\s*(?:/\s*\d{1,2})?\s*(?:[✅⚠️⛔]|sources?|exploit|tent|consult|accessibl|list[ée])", m.group(1)):
        continue
    fenetre = " ".join(lignes[idx: idx + 3])
    # ⑯ casse ignoree : « Source : LDLC.com » portait bien son domaine
    if re.search(DOM, fenetre, re.I) or re.search(r"https?://", fenetre):
        continue
    src_sans_adresse.append(l.strip()[:120])
print("A2. NOMS D'AUTORITE SANS AUCUNE ADRESSE :")
for a in sorted(sans_adresse):
    print("      INTERDIT", a, "- nommee comme source, sans adresse dans les Ressources")
print("      (aucun)" if not sans_adresse else "")
print("A4. LIGNES « Source : » QUI NOMMENT SANS LIER (aucun domaine sur la ligne ni les deux suivantes) :")
for l in src_sans_adresse:
    print("      INTERDIT", l)
print("      (aucune)" if not src_sans_adresse else "")
print("A3. IDENTIFIANTS (resolvent d'eux-memes ; on verifie la FORME, pas l'adresse) :")
for a in sorted(mal_formes):
    print("      INTERDIT", a, "- CLE DE CONTROLE INVALIDE : identifiant inexistant ou mal recopie")
for a in sorted(identifiants):
    print("      ok      ", a)
print("      (aucun)" if not (identifiants or mal_formes) else "")

# ── aspiration des pages : texte utile ET html brut
#    le brut est indispensable : nodejs.org/en/download n'expose ses numeros de
#    version que dans sa charge JavaScript (mesure du 11/09/2026).
pages, textes, bruts = {}, {}, {}
non_textuels = []
for u in urls:
    # ⚠️ PAS de text=True : une ressource peut etre un PDF, et le decodage utf-8
    #    d'un binaire leve UnicodeDecodeError — le controle mourait alors en cours de
    #    route et rendait exit 1 SANS verdict, ce qui se lisait comme un defaut trouve.
    #    Une exception deguisee en resultat est le pire etat possible d'un test.
    #    (crash attrape le 11/09/2026 sur la lecon psychopathologie n°15, qui cite un
    #     PDF de la HAS en troisieme ressource.)
    brut = subprocess.run(["curl", "-s", "-L", "--max-time", "30", "-A",
                           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
                           " (KHTML, like Gecko) Chrome/126 Safari/537.36", u],
                          capture_output=True).stdout
    if brut[:4] == b"%PDF" or u.lower().endswith(".pdf"):
        non_textuels.append(u)
        print("     %s : PDF (%d octets) — NON ANALYSE par ce test, verification a la main"
              % (u, len(brut)))
        continue
    raw = brut.decode("utf-8", "replace")
    r = re.sub(r"<(script|style).*?</\1>", "", raw, flags=re.S)
    r = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", r)))
    r = re.sub(r"\[\s*\d+\s*\]", " ", r)   # appels de note Wikipedia
    utile = len(r)
    pages[u] = re.sub(r"[^a-z0-9]+", "", r.lower())
    textes[u] = r
    bruts[u] = raw
    note = "  <-- SOUS 3000 : facade, ou page rendue en JS ? regarde le brut" if utile < 3000 else ""
    print("     %s : %d car. utiles / %d octets bruts%s" % (u, utile, len(raw), note))

def ou_trouve(aiguille):
    """Citations : ponctuation et espaces neutralises des deux cotes."""
    n = re.sub(r"[^a-z0-9]+", "", aiguille.lower())
    for u, p in pages.items():
        if n and n in p:
            return u, "texte"
    return None, None

def ou_trouve_nombre(n):
    """Nombres : recherche BORNEE. Sans bornes, 0.1.0 est 'trouve' dans 10.1.0 et
    un nombre a deux chiffres est trouve dans n'importe quelle page. Le brut est
    consulte en second : nodejs.org/en/download n'expose ses numeros de version
    que dans sa charge JavaScript (mesure du 11/09/2026)."""
    corps_n = re.escape(n).replace("\\ ", "[  ]?").replace("\\ ", "[  ]?")
    motif = re.compile(r"(?<![\d.,])" + corps_n + r"(?![\d.,])")
    motif_v = re.compile(r"(?<![\d.])v" + re.escape(n) + r"(?![\d.])")
    for u, r in textes.items():
        if motif.search(r):
            return u, "texte"
    for u, raw in bruts.items():
        if motif.search(raw) or motif_v.search(raw):
            return u, "brut (rendu JS)"
    return None, None

# ── B. citations anglaises de 8 mots ou plus
#    ⚠️ La passe B ne peut PAS verifier une TRADUCTION : une citation rendue en
#    francais n'est pas une sous-chaine de la page anglaise. Le filtre doit donc etre
#    large, sinon toute traduction est declaree ABSENTE a tort — c'est arrive le
#    11/09/2026 sur la lecon stoicisme n°14 (« Tu es responsable de tes jugements... »).
FR = re.compile(r"\b(de|tes|mes|ses|ma|ta|sa|nos|vos|leurs|ces|cet|quand|dont|lui|on"
                r"|toi|moi|soi|rien|tout|etre|meme|plus|moins|peu|tres|bien|mal"
                r"|le|la|les|des|du|un|une|dans|pour|qui|que|est|sont|ne|pas|avec"
                r"|sur|cette|ce|sa|son|ses|aux|par|plus|tout|nous|vous|en|mais|aussi"
                r"|alors|donc|etait|avait|etre|leur|elle|ils|si|comme|sans|sous|entre"
                r"|chaque|autre|meme|deja|à|être|même|déjà"
                r"|était)\b", re.I)
OUTILS = re.compile(r"\b(the|of|a|an|is|are|was|were|to|in|on|that|this|with|not|and"
                    r"|or|be|been|from|for|by|at|as|it|its|you|your|we|their|have|has|do"
                    r"|does|can|will|would|should|more|than|when|which|who|but|if|no|all"
                    r"|any|each|other|such|only|also|into|inside|without|before|after"
                    r"|between|during|while|about|there|these|those|them|he|she|they)\b",
                    re.I)
cits = set()
# ⑮ (12/09/2026) un guillemet droit colle a un chiffre est un POUCE (« 27" QHD »), pas une citation :
#    sur la veille iMac du 05/07, deux tailles d'ecran encadraient une ligne de tableau, lue comme
#    une citation anglaise de 8 mots « absente des pages ». Ouverture et fermeture non precedees d'un chiffre.
for m in re.finditer(r"(?:«|(?<!\d)\")\s*([^»\"]{25,300}?)\s*(?:»|(?<!\d)\")", corps):
    c = re.sub(r"\s+", " ", m.group(1)).strip()
    if len(c.split()) < 8:                      continue
    if re.search(r"[<>{}=;]|//|…", c):     continue
    if not c[:1].isalpha():                     continue
    if FR.search(c):                            continue
    # ⚠️ une citation est une PHRASE, pas un NOM. Un nom propre ou un intitule de
    #    produit entre guillemets n'a aucun mot-outil anglais — et n'a pas a etre
    #    cherche sur une page. Sans ce filtre, la lecon placement-financier n°13
    #    voyait signaler « Tracker CAC 40 (DR) UCITS ETF - Dist », un nom que la
    #    lecon declare elle-meme FICTIF deux lignes plus haut (11/09/2026).
    if not OUTILS.search(c):                    continue
    # l'attribution « — Auteur » finale n'est pas la citation : on la retire avant de
    # chercher, sinon une citation EXACTE est declaree absente (11/09/2026).
    c = re.split(r"\s+[\u2014-]\s+(?=[A-Z\u00c0-\u00dd][^.]{2,60}$)", c)[0].strip()
    if len(c.split()) >= 8:
        cits.add(c)
print("\nB. CITATIONS ANGLAISES DE 8 MOTS OU PLUS : %d" % len(cits))
ko_b = 0
for c in sorted(cits):
    u, how = ou_trouve(c)
    if u:
        print("   OK      %s\n             -> %s (%s)" % (c[:76], u, how))
    else:
        ko_b += 1
        print("   ABSENTE %s\n             -> sur AUCUNE page listee" % c[:76])

# ── C. numeros de version
#    un numero releve a npm show est legitime et ne vient PAS de la doc :
#    on le classe NPM au lieu de le signaler.
#    ⚠️ NON BLOQUANTE, et c'est voulu : trouver un numero quelque part parmi les
#    pages citees ne prouve NI que la lecon l'y a pris, NI qu'il s'agit du meme
#    paquet. Mesure du 11/09/2026 : « 7.0.2 » (TypeScript) et « 26.2.0 »
#    (@types/node) sont « trouves » dans la charge de nodejs.org/previous-releases,
#    qui liste des centaines de versions de Node. C est un INVENTAIRE ; c'est C2,
#    la proximite, qui juge. Une mesure locale (npm show, node -v) est legitime.
LOCAL = re.compile(r"npm\s+(show|view|list|ls|install)|package\.json|node_modules"
                   r"|node\s+-v|node\s+--version", re.I)
NPM = LOCAL
SECTION = re.compile(r"(section|RFC|§|chapitre|art\.|annexe)\s*[\d.]*$", re.I)
vers = {}
for m in re.finditer(r"\bv?(\d+\.\d+\.\d+)\b", avant_res):
    if SECTION.search(avant_res[max(0, m.start() - 40): m.start()]):
        continue        # « RFC 3986 section 5.2.4 » n'est pas un numero de version
    ctx = avant_res[max(0, m.start() - 260): m.end() + 260]
    vers.setdefault(m.group(1), LOCAL.search(ctx) is not None)
    if LOCAL.search(ctx):
        vers[m.group(1)] = True
print("\nC. INVENTAIRE DES NUMEROS DE VERSION (non bloquant) : %d" % len(vers))
for v in sorted(vers):
    u, how = ou_trouve_nombre(v)
    if u:
        print("   presente  %-12s -> %s (%s)" % (v, u, how))
    elif vers[v]:
        print("   locale    %-12s -> mesure locale annoncee (npm show / node -v) : "
              "legitime, ne vient pas de la doc" % v)
    else:
        print("   A RELIRE  %-12s -> sur aucune page citee et aucune mesure locale "
              "annoncee : dis d'ou il vient" % v)
ko_c = 0

# ── C2. version ACCOLEE a un domaine : la page de ce domaine doit la porter
#    C'est la forme exacte du defaut du 28/08 : « Vite v8.2.2 — verifiee sur
#    vite.dev/guide/ » et le libelle « vite.dev/guide/ — Getting Started (v8.2.2) ».
#    On travaille LIGNE PAR LIGNE (extract_docx met un paragraphe par ligne) et on
#    inclut la section Ressources, dont les libelles sont des affirmations.
#    ⚠️ PROXIMITE de 80 caracteres, PAS « meme ligne » : extract_docx met un
#    paragraphe entier sur une ligne, et un paragraphe de la lecon 05 contient
#    « React 19.2.8 » (test local) ET « react.dev » (citation) sans rapport entre
#    eux — le critere « meme ligne » produisait un faux positif (11/09/2026).
PROX = 80
print("\nC2. VERSIONS ACCOLEES A UN DOMAINE (a moins de %d caracteres) :" % PROX)
ko_c2 = 0
vus = set()
mentions = [(m.start(), m.end(), m.group(1), m.group(2).rstrip("./,;:)"))
            for m in re.finditer(r"(" + DOM + r")((?:/[A-Za-z0-9._~:/#@!$&*+,;=%-]*)?)",
                                 corps)]
for mv in re.finditer(r"\bv?(\d+\.\d+\.\d+)\b", corps):
    v = mv.group(1)
    if SECTION.search(corps[max(0, mv.start() - 40): mv.start()]):
        continue
    # ⚠️ SEULE la mention de domaine la PLUS PROCHE est testee. Tester toutes celles
    #    de la fenetre produisait un faux positif : dans la section Ressources, un
    #    « (v8.2.2) » collé a vite.dev/guide/ se retrouvait aussi impute au
    #    « react.dev » du libelle suivant (11/09/2026).
    proches = [(min(abs(mv.start() - e), abs(s - mv.end())), s, e, d, c)
               for (s, e, d, c) in mentions
               if abs(mv.start() - e) <= PROX or abs(s - mv.end()) <= PROX]
    if not proches:
        continue
    _, s, e, dom, chemin = min(proches)
    zone = corps[max(0, min(s, mv.start()) - 20): max(e, mv.end()) + 20]
    if LOCAL.search(zone):
        continue
    cibles = [u for u in urls
              if dom + chemin.rstrip("/") in re.sub(r"^https?://", "", u)]
    if not cibles or (dom, chemin, v) in vus:
        continue
    vus.add((dom, chemin, v))
    motif = re.compile(r"(?<![\d.,])" + re.escape(v) + r"(?![\d.,])")
    motif_v = re.compile(r"(?<![\d.])v" + re.escape(v) + r"(?![\d.])")
    porte = [u for u in cibles
             if motif.search(textes[u]) or motif.search(bruts[u])
             or motif_v.search(bruts[u])]
    if porte:
        print("   OK         %-10s pres de %-38s -> la page la porte" % (v, dom + chemin))
    else:
        # ⚠️ UN SEUL ACQUITTEMENT POSSIBLE, ET IL EST EXIGEANT : la DERIVE DOCUMENTEE.
        #    La zone doit porter un marqueur de REVERIFICATION *et* un autre numero que
        #    la page, elle, porte reellement. Les deux conditions ensemble.
        #    ⚠️ N'ACQUITTE JAMAIS SUR LA SEULE PRESENCE D'UNE DATE : une premiere version
        #    le faisait, et requalifiait en note benigne le defaut meme qui a motive la
        #    regle 19 — la ligne fautive de la lecon 05 etait datee du 28/08/2026, et
        #    vite.dev/guide/ n'a JAMAIS porte le 8.2.2 qu'on lui pretait (11/09/2026).
        #    Un test qu'on ne peut pas ramener au vert finit ignore ; un test qui se laisse
        #    acquitter par une date ne sert a rien. La derive documentee tient les deux.
        large = corps[max(0, mv.start() - 400): mv.end() + 400]
        releve = re.search(r"rev[ée]rifi[ée]e?s?\s+le|remesur[ée]e?s?\s+le"
                           r"|affiche d[ée]sormais|ne (?:l[ae] |y )?(?:figure|porte) plus",
                           large, re.I)
        neuf = None
        if releve:
            # on lit d'abord APRES le marqueur : « affiche desormais v26.8.2 ». Sans cela
            #    le premier numero de la fenetre est retenu, et le message vert annonce un
            #    numero sans rapport (mesure du 11/09/2026 : 24.0.0 au lieu de 26.8.2).
            candidats = (re.findall(r"\bv?(\d+\.\d+\.\d+)\b", large[releve.end():])
                         + re.findall(r"\bv?(\d+\.\d+\.\d+)\b", large))
            for autre in candidats:
                if autre == v:
                    continue
                mo = re.compile(r"(?<![\d.,])" + re.escape(autre) + r"(?![\d.,])")
                if any(mo.search(textes[u]) or mo.search(bruts[u]) for u in cibles):
                    neuf = autre
                    break
        if neuf:
            print("   DERIVE     %-10s pres de %-38s -> la page porte maintenant %s, et la "
                  "lecon le DIT : derive documentee, pas defaut" % (v, dom + chemin, neuf))
        else:
            ko_c2 += 1
            date = re.search(r"\d{2}/\d{2}/\d{4}", zone)
            print("   INTERDIT   %-10s pres de %-38s -> cette page NE la porte PAS%s"
                  % (v, dom + chemin,
                     "  [releve date du %s : verifie si la page le portait alors, "
                     "ou jamais]" % date.group(0) if date else ""))
            print("              contexte : %s" % re.sub(r"\s+", " ", zone).strip()[:120])
if not vus:
    print("   (aucune version a proximite d'un domaine cite)")

# ── D. valeurs chiffrees presentees comme venant d'une source
ATTRIB = re.compile(r"(" + DOM + r")|\b(v[ée]rifi[ée]e?s?|selon|d'apr[eè]s|la doc|"
                    r"documentation|source|annonce|indique|pr[ée]cise)\b", re.I)
IGNORE = re.compile(r"^(19|20)\d\d$")          # annees
chiffres = {}
for phrase in re.split(r"(?<=[.!?:])\s+|\n", avant_res):
    if not ATTRIB.search(phrase):
        continue
    if re.search(r"\bv?\d+\.\d+\.\d+\b", phrase):
        phrase = re.sub(r"\bv?\d+\.\d+\.\d+\b", " ", phrase)   # deja traite en C
    for m in re.finditer(r"\b\d{1,3}(?:[  ]\d{3})+\b|\b\d+[,.]\d+\b|\b\d{3,6}\b", phrase):
        n = m.group(0)
        if IGNORE.match(n):                     continue
        if n in ("3000", "5173", "1024", "1000"):  continue   # ports et conversions du projet
        chiffres.setdefault(n, phrase.strip()[:110])
print("\nD. VALEURS CHIFFREES EN CONTEXTE D'ATTRIBUTION : %d" % len(chiffres))
ko_d = 0
for n in sorted(chiffres, key=lambda s: (len(s), s)):
    u, how = ou_trouve_nombre(n)
    if u:
        print("   OK      %-10s -> %s (%s)" % (n, u, how))
    else:
        ko_d += 1
        print("   A VERIFIER %-7s -> absente des pages citees | %s" % (n, chiffres[n]))

inertes = []
if not cits:    inertes.append("B (aucune citation anglaise de 8 mots ou plus)")
if not vers:    inertes.append("C (aucun numero de version)")
if not vus:     inertes.append("C2 (aucune version pres d'un domaine cite)")
if not chiffres: inertes.append("D (aucune valeur chiffree en contexte d'attribution)")
if non_textuels:
    print("\n>>> RESSOURCES NON ANALYSABLES (PDF) : %d — %s"
          % (len(non_textuels), "; ".join(non_textuels)))
    print(">>> Aucune citation ne peut etre confirmee sur ces pages par ce test.")
print("\n>>> PASSES INERTES SUR CE DOCUMENT : %s"
      % ("; ".join(inertes) if inertes else "aucune — les quatre ont mordu"))
print(">>> Une passe inerte n'est PAS une passe reussie : elle n'a rien cherche.")
pb = len(orphelines) + len(sites_non_listes) + len(sans_adresse) + len(mal_formes) + len(src_sans_adresse) + ko_b + ko_c2
print("\nVERDICT : %d probleme(s) bloquant(s) (A + A2 + A3 + A4 + B + C2)" % pb)
print("          %d valeur(s) chiffree(s) a relire en D — a la main, D n'est pas bloquant"
      % ko_d)
sys.exit(1 if pb else 0)
