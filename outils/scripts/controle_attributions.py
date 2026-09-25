#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""controle_attributions.py — test d'attribution des pages, commun à tous les parcours.

Usage : /usr/bin/python3 outils/scripts/controle_attributions.py <chemin du .docx>
Sort en 0 si aucun problème bloquant, en 1 sinon, en 2 si le fichier est illisible, en 3 si rien
ne bloque mais qu'une vérification a été IMPOSSIBLE (page non lue, 0 octet) — un 3 n'est pas un 0.

Copie CANONIQUE, extraite verbatim du bloc embarqué dans le prompt appli-ia-lecon
(jobs_config.json) le 12/09/2026 — même contenu, même validation : dix-sept cas
connus, dans les deux sens, sous env -i. Historique des treize défauts du test
et de leurs corrections : outils/scripts/JOBS.md (journée du 11/09/2026) ; ⑭ le
12/09/2026, la passe A cesse d'ignorer un site nu cité comme source sans aucune page listée ;
⑮ le même jour, un guillemet droit collé à un chiffre (27") n'ouvre plus une citation ;
⑯ A4 ignore les lignes de décompte (« Sources : 6 ✅ … ») et lit « LDLC.com » comme un domaine ;
⑰ une page non lue (0 octet) ne prouve pas une absence : NON VERIFIABLE, exit 3, jamais INTERDIT ;
⑲ A4 lit les libellés des liens imprimés par extract_docx (« Nexem → nexem.fr/… ») : un lien sans domaine
   dans son libellé est quand même une adresse donnée au lecteur ;
⑳ A4 APPARIE la source nommée à l'adresse voisine (« Nexem » ↔ nexem.fr, alias d'institutions) : sur la
   même ligne la proximité suffit, sur les lignes suivantes le nom doit répondre à l'adresse ;
⑱ une page vide est retentée deux fois (5 s, 15 s) avant d'être déclarée non lue ;
㉑ un code HTTP hors 2xx (429, 503, 403) vaut page non lue : le corps d'une page d'erreur n'est pas la page ;
㉒ passe A5 : un hyperlien sans cible (relation sans Target), signalé par extract_docx, bloque ;
㉓ (13/09/2026) B APPARIE la citation à la source NOMMÉE à côté d'elle : « … » (selon consomac.fr) doit être
   sur une page de consomac.fr — trouvée sur une autre page listée, elle est MAL ATTRIBUÉE et bloque.
   Avant ㉓, une citation trouvée sur n'importe quelle page listée était OK, quelle que soit la source
   que la note lui prêtait (veille iMac du 13/09/2026 : deux phrases de Gurman prêtées à consomac.fr,
   qui n'en porte aucune — elles étaient sur 9to5mac.com et macrumors.com, et B disait OK).
㉔ (13/09/2026) B descend de huit à six mots : « Before the end of the year » (six mots) passait sous le seuil
   dans la même note. Inventaire préalable sur les 223 documents : cinq citations de six ou sept mots, toutes
   trouvées sur leur page (Enneagram Institute, react.dev, lyckowbackman.se, aapel.org, 9to5mac) — aucun faux
   positif à trier ; le plancher de 25 caractères ne cache aucune citation de six mots (vérifié à 18).
㉕ (14/09/2026) D acceptait « 1 689 » mais pas « 1 689,00 » : la borne « (?![0-9.,]) » refusait les décimales nulles
   d'une page française (consomac : « 1 689,00 € »), et l'espace insécable n'était pas neutralisée (re.escape
   n'échappe plus l'espace depuis Python 3.7 : le remplacement était du code mort). Faux positif dans la note de
   contrôle du 13/09.
㉖ (14/09/2026) passe B-FR : une citation FRANÇAISE entre guillemets, prêtée à une source nommée à côté d'elle
   (domaine, ou nom apparié aux pages listées : « par l'INSERM 2016 », « (ANESM, 2015) », « selon Unafam »),
   doit être sur une page de cette source quand cette page est en français — sinon ABSENTE DE LA SOURCE NOMMÉE,
   bloquant. Page non lue ou PDF → NON VERIFIABLE ; page en anglais → traduction possible, non tranché ; sans
   source nommée → cherchée partout, « à relire » si absente, jamais bloquant. Une citation entre crochets de
   correction (« [Corrigé le … : la première version prêtait … « mot » …] ») est exemptée : elle cite l'erreur.
   Incident : psychopathologie n°16 du 14/09/2026, « contradictoires » prêté à l'INSERM, mot absent du chapitre ;
   l'anglais avait un test depuis le 11/09, le français aucun.
㉗ (15/09/2026) trois angles morts vus sur dzogchen n°16 : une adresse à parenthèses (Wikipedia « Terma_(religion) »)
   était coupée à la parenthèse et déclarée non lue ; les diacritiques (« ḍākinīs ») rendaient une citation exacte
   introuvable ; une citation de plus de 300 caractères, ou coupée par « [...] », n'était pas lue du tout — elle
   se cherche désormais segment par segment (tous sur la même page), jusqu'à 700 caractères.
㉘ (17/09/2026) passe A6 : un lien en 404/410 est un LIEN MORT, bloquant — sauf si le document le déclare mort à
   côté de son libellé (« ⛔ 404 »). Avant, un 404 était « une page non lue » comme un 429 : astrologie n°07 a
   publié un lien mort avec un verdict à 0.
㉘ bis (20/09/2026) un ⛔ seul ne déclare pas un lien mort : la déclaration nomme le code (404/410) ou le fait
   (« lien mort », « introuvable », « n'existe plus ») — revenus-passifs n°09 marquait un 404 « ⛔ page JS-only ».
㉚ (20/09/2026) présence n'est pas parole : une citation TROUVÉE sur la page nommée peut y être dans la voix de
   l'auteur, sans guillemets — « All signs point to the M6 models being close to launch » est une phrase de
   9to5Mac, que MacRumors cite entre guillemets en la prêtant à Gurman ; la veille iMac du 20/09 l'a remise sous
   9to5Mac une semaine après la correction du 13/09, et ㉓ disait OK. B cherche désormais la phrase AVEC ses
   guillemets sur la page nommée : trouvée nue là et entre guillemets ailleurs → MAL ATTRIBUEE (reprise nue) ;
   nue partout → A RELIRE, « qui parle ? ».
㉙ (19/09/2026) passe B-NOM : une affirmation SANS guillemets prêtée à une source nommée — « selon l'IEFP »,
   « (AMF) », « d'après la CNIL », « l'INSEE indique que » — se cherche mot par mot (mots pleins de 7 lettres
   ou plus) sur les pages listées de cette source. Placement n°15 : « les biais les plus courants en France,
   selon la littérature (IEFP), sont … l'effet moutonnier » — la page de l'IEFP ne dit jamais « moutonnier » ;
   ai-act 18/09 : trois chantiers législatifs prêtés à un article qui n'en nomme aucun. B et B-FR ne cherchent
   que ce qui est entre guillemets ; un nom entre parenthèses est une attribution comme une autre.

Cinq passes : A pages nommées non listées et sites nus · A2 noms d'autorité sans
adresse · A3 identifiants (forme vérifiée, clé ISBN) · B citations anglaises de
six mots ou plus (㉔) cherchées dans les pages · B-FR citations françaises · B-NOM affirmations
prêtées à un nom sans guillemets (㉙) · C/C2 numéros de version (C2 bloquant
à moins de 80 caractères d'un domaine cité) · D valeurs chiffrées, à relire.
Lis toujours la ligne « PASSES INERTES » : une passe inerte n'a rien cherché.
"""
import sys, re, html, subprocess, time, os, unicodedata

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
def urls_de(z, fin=r"\s"):
    """㉗ (15/09/2026) une adresse Wikipedia porte des parentheses (« Terma_(religion) ») : on ne coupe une
    parenthese fermante finale que si elle n'a pas d'ouvrante dans l'adresse."""
    out = []
    for u in re.findall(r"https?://[^" + fin + r"]+", z):
        while u and u[-1] in ")>]»" and (u[-1] != ")" or u.count("(") < u.count(")")):
            u = u[:-1]
        out.append(u)
    return out
urls = sorted(set(urls_de(entete)))
# ⑲ (12/09/2026) les LIBELLÉS des liens : extract_docx imprime « libellé → cible » ; un libellé sans
#    domaine (« Nexem ») est quand meme une adresse donnee au lecteur — A4 doit le savoir
libelles_lies = set()
lib_hote = {}      # ㉚ libelle de lien -> hote de sa cible (« 9to5Mac (23/08/2026) » -> 9to5mac.com)
for l in entete.split("\n"):
    if " → http" in l:
        lib = l.rsplit(" → ", 1)[0].strip()
        # un libelle generique (« ici », « lien », « source ») acquitterait n'importe quelle fenetre
        if len(lib) >= 4 and lib.lower() not in ("lien", "voir", "page", "site", "source", "sources", "cliquer", "ici"):
            libelles_lies.add(lib)
            lib_hote[lib] = re.sub(r"^www\.", "", re.sub(r"^https?://", "", l.rsplit(" → ", 1)[1].strip()).split("/")[0].lower())
# ⑭ une adresse ecrite EN CLAIR dans le corps (cellule « URL » d'un tableau, ligne « Source : https://… »)
#    est une adresse donnee au lecteur, meme sans lien cliquable : elle compte comme listee
urls_texte = sorted(set(urls_de(corps, r"\s>\]«»\"")))
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
def cle_texte(z):
    """㉗ (15/09/2026) ponctuation, espaces ET diacritiques neutralises : « ḍākinīs » (leçon) et « dakinis »
    (Wikipedia) sont le meme mot — avant, ḍ et ā disparaissaient et la citation exacte etait NON VERIFIABLE."""
    z = unicodedata.normalize("NFKD", z)
    z = "".join(ch for ch in z if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+", "", z.lower())
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
# ⑳ (12/09/2026) APPARIEMENT : une adresse dans la fenetre ne suffit plus, il faut qu'elle soit CELLE
#    de la source nommee. Sur la meme ligne, la proximite vaut appariement (l'auteur a mis l'adresse
#    a cote du nom). Sur les deux lignes suivantes, le lien ou le domaine doit repondre au nom :
#    « Nexem » ↔ nexem.fr, « Le Media Social » ↔ lemediasocial.fr, « CNSA » ↔ cnsa.fr — ou par un
#    alias d'institution (ANESM et HAS publient sur has-sante.fr, l'OMS sur who.int, le CEPD sur
#    edpb.europa.eu). Avant ⑳, « Source : Nexem » suivie d'un lien vers lemediasocial.fr passait.
ALIAS = {"anesm": ("hassante",), "has": ("hassante",), "hautautoritedesante": ("hassante",),
         "oms": ("whoint", "icdwhoint"), "who": ("whoint",), "apa": ("psychiatryorg",),
         "cepd": ("edpbeuropaeu",), "edpb": ("edpbeuropaeu",), "cnil": ("cnilfr",),
         "commissioneuropeenne": ("europaeu",), "commission": ("europaeu",), "conseildelue": ("consiliumeuropaeu",),
         "cjue": ("curiaeuropaeu",), "legifrance": ("legifrancegouvfr",), "cnsa": ("cnsafr",),
         "dgcs": ("socialgouvfr", "handicapgouvfr"), "ministere": ("gouvfr",), "atih": ("atihsantefr",),
         "amf": ("amffranceorg",), "insee": ("inseefr",), "bloomberg": ("bloombergcom",), "gurman": ("bloombergcom",),
         "serafin": ("handicapgouvfr", "cnsafr"), "serafinph": ("handicapgouvfr", "cnsafr"),
         "pubmed": ("ncbinlmnihgov",), "pubmedcentral": ("ncbinlmnihgov",), "pmc": ("ncbinlmnihgov",),
         "iefp": ("lafinancepourtouscom",), "iapp": ("iapporg",), "servicepublic": ("servicepublicgouvfr", "servicepublicfr"),
         "banquedefrance": ("banquefrancefr",), "acpr": ("acprbanquefrancefr",), "urssaf": ("urssaffr",), "dgfip": ("impotsgouvfr",)}
def cle(t):
    t = t.lower()
    for a_, b_ in (("é", "e"), ("è", "e"), ("ê", "e"), ("à", "a"), ("ô", "o"), ("î", "i"), ("ç", "c"), ("ù", "u"), ("û", "u")):
        t = t.replace(a_, b_)
    return re.sub(r"[^a-z0-9]", "", t)
def nom_source(reste):
    """le premier segment de ce qui suit « Source : » : « HAS (Haute Autorité…) — Validé… » -> « HAS »"""
    seg = re.split(r"\s[—–]\s|\s-\s|[,;·(:\[]|\s\d{1,2}/\d{1,2}/\d{2,4}", reste.strip(), 1)[0].strip()
    return seg
# mots qui ne designent pas une source : « page principale CNSA » repond a cnsa.fr par « cnsa », pas par « page »
VIDES = {"page", "principale", "comite", "strategique", "publication", "reunion", "communique", "rapport", "note",
         "guide", "source", "sources", "via", "resume", "article", "decret", "loi", "journal", "officiel", "annonce",
         "site", "dossier", "fiche", "les", "des", "une", "sur", "pour", "dans", "avec", "par", "primaire", "secondaire",
         "officielle", "consultee", "consulte", "cadrage", "recommandation", "actualites", "actualite", "news", "blog",
         "espace", "portail", "plateforme", "presse", "service", "direction", "agence", "ministere"}
def apparie(nom, adresse):
    """le nom repond-il a l'adresse (domaine ou libelle de lien) ? Par la cle entiere, par un de ses mots
    (« ARS Bretagne » ↔ bretagne.ars.sante.fr), ou par un alias d'institution."""
    est_url = "://" in adresse or re.match(DOM, adresse, re.I)
    a_ = cle(re.sub(r"^https?://(?:www\.)?", "", adresse).split("/")[0] if est_url else adresse)
    n = cle(nom)
    if len(n) < 3 or len(a_) < 3:
        return True                      # trop court pour trancher : on ne bloque pas sur un sigle d'une lettre
    a_sans_tld = re.sub(r"(com|org|net|fr|eu|gouv|io|int)$", "", a_) or a_
    if n in a_ or (len(a_sans_tld) >= 4 and a_sans_tld in n):
        return True
    mots = [cle(w) for w in re.findall(r"[A-Za-zÀ-ÿ0-9]{3,}", nom)]
    mots = [w for w in mots if w and w not in VIDES]
    if any(w in a_ for w in mots):
        return True
    return any(al in a_ for al in ALIAS.get(n, ()) + sum((ALIAS.get(w, ()) for w in mots), ()))
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
    # la LIGNE LOGIQUE : un lien pose au milieu d'une ligne la coupe en trois a l'extraction
    #    (« Source : CNSA, » / « cnsa.fr » / « — publication… ») ; on recolle les libelles de liens et
    #    les morceaux qui s'ouvrent par une ponctuation de continuation
    logique, j = l, idx + 1
    while j < len(lignes) and (lignes[j].strip() in libelles_lies
                               or (lignes[j].strip()[:1] in ("—", "–", ")", ",", "(", "·", ";") and lignes[j].strip())):
        logique += " " + lignes[j].strip(); j += 1
    nom = nom_source(m.group(1))
    def adresses(z, sans=""):
        c_ = re.findall(DOM, z, re.I) + re.findall(r"https?://[^\s)]+", z)
        c_ += [lib for lib in libelles_lies if lib not in sans and re.search(r"(?<![A-Za-zÀ-ÿ])" + re.escape(lib) + r"(?![A-Za-zÀ-ÿ])", z)]
        return c_
    # 1. les adresses SUR LA LIGNE LOGIQUE, puis 2. celles des deux lignes suivantes : dans les deux cas
    #    l'une d'elles doit REPONDRE AU NOM (⑳). « Source : page principale CNSA … à verifier sur
    #    legifrance.gouv.fr » porte un domaine, mais pas celui de la source nommee.
    sur_ligne = adresses(logique, sans=nom)
    suite = " ".join(lignes[j: j + 2])
    candidats = sur_ligne if sur_ligne else adresses(suite)
    if not candidats:
        src_sans_adresse.append(l.strip()[:120])
        continue
    # l'appariement ne s'applique qu'a une source NOMMEE : une description (« classification adaptee
    # d'un guide generaliste »), une reference d'article (« Hyndych A, Koval K (2025) » — le DOI est
    # verifie en A3) ou une source declaree NON consultee (« newsletter Gurman — non consultee, reprise
    # d'apres macrumors.com ») se contentent d'une adresse voisine
    nommee = bool(re.search(r"(?<![\w])[A-ZÀ-Ý][\wÀ-ÿ-]+", nom))
    article = bool(re.match(r"[A-ZÀ-Ý][a-zà-ÿ-]+\s+[A-Z]{1,2}\b", nom))
    #    (la mention « non consultee » doit porter sur LA source nommee : avant le premier « ; »,
    #     sinon « CNSA … ; source primaire (legifrance) non consultee » exempterait la CNSA)
    if not nommee or article or NON_CONSULT.search(m.group(1).split(";")[0][:160]):
        continue
    if any(apparie(nom, c_) for c_ in candidats):
        continue
    src_sans_adresse.append("%s   [nomme « %s », mais les adresses voisines sont : %s]" % (l.strip()[:90], nom[:40], ", ".join(candidats)[:80]))
print("A2. NOMS D'AUTORITE SANS AUCUNE ADRESSE :")
for a in sorted(sans_adresse):
    print("      INTERDIT", a, "- nommee comme source, sans adresse dans les Ressources")
print("      (aucun)" if not sans_adresse else "")
print("A4. LIGNES « Source : » QUI NOMMENT SANS LIER (aucune adresse sur la ligne, ni adresse APPARIEE au nom sur les deux suivantes) :")
for l in src_sans_adresse:
    print("      INTERDIT", l)
print("      (aucune)" if not src_sans_adresse else "")
print("A3. IDENTIFIANTS (resolvent d'eux-memes ; on verifie la FORME, pas l'adresse) :")
for a in sorted(mal_formes):
    print("      INTERDIT", a, "- CLE DE CONTROLE INVALIDE : identifiant inexistant ou mal recopie")
for a in sorted(identifiants):
    print("      ok      ", a)
print("      (aucun)" if not (identifiants or mal_formes) else "")

# ── A5. hyperliens SANS CIBLE : extract_docx les liste (㉒, 13/09/2026). Un lien qui ne mene
#    nulle part est une source nommee sans adresse — trois lecons n°01 en ont porte quatre
#    chacune pendant trois mois, lues « 0 URL » par tous les controles.
sans_cible = []
if "HYPERLIENS SANS CIBLE" in entete:
    bloc = entete.split("HYPERLIENS SANS CIBLE", 1)[1]
    sans_cible = [l.strip() for l in bloc.split("\n")[1:] if " → " in l]
print("A5. HYPERLIENS SANS CIBLE (le lecteur clique dans le vide) :")
for l in sans_cible:
    print("      INTERDIT", l[:120])
print("      (aucun)" if not sans_cible else "")

# ── aspiration des pages : texte utile ET html brut
#    le brut est indispensable : nodejs.org/en/download n'expose ses numeros de
#    version que dans sa charge JavaScript (mesure du 11/09/2026).
pages, textes, bruts = {}, {}, {}
non_textuels = []
codes = {}                                  # ㉘ dernier code HTTP de chaque adresse
for u in urls:
    # ⚠️ PAS de text=True : une ressource peut etre un PDF, et le decodage utf-8
    #    d'un binaire leve UnicodeDecodeError — le controle mourait alors en cours de
    #    route et rendait exit 1 SANS verdict, ce qui se lisait comme un defaut trouve.
    #    Une exception deguisee en resultat est le pire etat possible d'un test.
    #    (crash attrape le 11/09/2026 sur la lecon psychopathologie n°15, qui cite un
    #     PDF de la HAS en troisieme ressource.)
    # ⑱ (12/09/2026) RETRY : une page a 0 octet est retentee, deux fois, apres 5 puis 15 s —
    #    reseau qui flanche, delai depasse, mur qui cede a la deuxieme demande. Le 12/09 au soir,
    #    nodejs.org, MDN, code.claude.com puis neuf pages d'imac 06/09 sont revenues vides
    #    en une seule passe alors qu'elles repondaient le matin. Un retry qui rend une page
    #    est un retry ; un retry qui rend encore du vide reste NON VERIFIABLE (⑰) — jamais
    #    un « la page ne porte pas ». Le nombre d'essais est imprime avec la page.
    brut, essais = b"", 0
    for attente in (0, 5, 15):
        if attente:
            time.sleep(attente)
        essais += 1
        # ㉑ (13/09/2026) le CODE HTTP compte : une page d'erreur (429, 503, 403…) a un corps, mais ce
        #    corps n'est pas la page — la citation y est forcement « absente », et le verdict est faux.
        #    Sur hypnose n°13, deux citations exactes ont ete declarees absentes de PMC pendant une
        #    salve de 429 ; la meme commande dix minutes plus tard les trouvait. Hors 2xx : page non lue.
        rep = subprocess.run(["curl", "-s", "-L", "--max-time", "30", "-o", "/tmp/.controle_page", "-w", "%{http_code}", "-A",
                              "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
                              " (KHTML, like Gecko) Chrome/126 Safari/537.36", u],
                             capture_output=True, text=True)
        code = rep.stdout.strip()[-3:]
        codes[u] = code
        try:
            brut = open("/tmp/.controle_page", "rb").read()
        except FileNotFoundError:
            brut = b""
        if not code.startswith("2"):
            brut = b""                 # corps d'erreur : on ne lit rien dedans
        if brut or re.search(r"://(?:localhost|127\.0\.0\.1)", u):
            break
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
    pages[u] = cle_texte(r)
    textes[u] = r
    bruts[u] = raw
    locale = bool(re.search(r"://(?:localhost|127\.0\.0\.1)", u))
    if not raw:
        note = "  <-- adresse locale du projet, non aspiree" if locale else "  <-- VIDE ou HTTP %s apres %d essais : NON LUE, rien ne sera conclu sur elle (⑰, ㉑)" % (code if not locale else "-", essais)
    else:
        note = ("  <-- SOUS 3000 : facade, ou page rendue en JS ? regarde le brut" if utile < 3000 else "") \
               + ("  [obtenue au %de essai]" % essais if essais > 1 else "")
    print("     %s : %d car. utiles / %d octets bruts%s" % (u, utile, len(raw), note))

# ── A6. LIENS MORTS (㉘, 17/09/2026). Un 404 ou un 410 n'est pas un mur ni un delai : la page n'existe pas.
#    Avant ㉘, le controle le rangeait avec les 429 et les 000 (« page non lue », exit 3 au mieux), et la lecon
#    astrologie n°07 a publie imprint.co.uk/jcs/JCS10_6-7.html en 404 avec un verdict a 0 bloquant. Regle 6 de
#    tous les prompts : « 404 = ne cite pas ». Exemption : un lien que le document DECLARE mort a cote de son
#    libelle (« ⛔ 404 », « lien mort », « inaccessible ») — enneagramme n°15 declare psychologytoday en 404 —
#    est une information donnee au lecteur, pas une adresse pretendue vivante.
liens_morts = []
for u in urls:
    if codes.get(u) not in ("404", "410"):
        continue
    libs = [l.rsplit(" → ", 1)[0].strip() for l in entete.split("\n") if l.strip().endswith(u)]
    chemin_u = re.sub(r"^https?://(?:www\.)?", "", u).rstrip("/")
    declare = False
    for cle_u in libs + [chemin_u, chemin_u.split("/")[0]]:
        for m_ in re.finditer(re.escape(cle_u), corps):
            fen = corps[max(0, m_.start() - 200): m_.end() + 200]
            # ㉘ bis (20/09/2026) : un ⛔ seul ne declare pas un lien mort — revenus-passifs n°09 marquait plausible.io/pricing
            #   « ⛔ page JS-only » alors que l'adresse repond 404 : la raison ecrite etait fausse et le lecteur renvoye vers une
            #   erreur. La declaration doit nommer le fait : le code, ou « lien mort / introuvable / n'existe plus / supprimee ».
            if re.search(r"404|410|lien mort|introuvable|n['’]existe plus|page supprim", fen, re.I):
                declare = True
                break
        if declare:
            break
    if declare:
        print("     (lien mort DECLARE dans le document, non bloquant : %s)" % u)
    else:
        liens_morts.append(u)
print("A6. LIENS MORTS (HTTP 404/410, non declares dans le document) :")
for u in liens_morts:
    print("      INTERDIT", u, "- HTTP", codes.get(u), ": la page n'existe pas, le document la cite comme vivante (㉘)")
print("      (aucun)" if not liens_morts else "")

def ou_trouve(aiguille):
    """Citations : ponctuation et espaces neutralises des deux cotes ; une citation coupee par « […] » ou « [...] »
    se cherche segment par segment (㉗), et n'est trouvee que si TOUS ses segments le sont sur une meme page."""
    segs = [sg for sg in re.split(r"\[\s*(?:\.\.\.|…)\s*\]|…", aiguille) if len(sg.split()) >= 3]
    if len(segs) > 1:
        for u, p in pages.items():
            if all(cle_texte(sg) in p for sg in segs):
                return u, "texte, %d segments" % len(segs)
        return None, None
    n = cle_texte(aiguille)
    for u, p in pages.items():
        if n and n in p:
            return u, "texte"
    return None, None

def ou_trouve_toutes(aiguille):
    """㉓ toutes les pages qui portent la citation, pas la premiere : l'appariement a besoin de savoir
    si la page NOMMEE est parmi elles."""
    segs = [sg for sg in re.split(r"\[\s*(?:\.\.\.|…)\s*\]|…", aiguille) if len(sg.split()) >= 3]
    if len(segs) > 1:
        return [u for u, p in pages.items() if all(cle_texte(sg) in p for sg in segs)]
    n = cle_texte(aiguille)
    return [u for u, p in pages.items() if n and n in p]

def hote(u):
    return sans_www(re.sub(r"^https?://", "", u).split("/")[0])

def pages_de(dom):
    """les pages listees du domaine nomme (ou de ses sous-domaines)"""
    return [u for u in urls if hote(u) == dom or hote(u).endswith("." + dom)]

def ou_trouve_nombre(n):
    """Nombres : recherche BORNEE. Sans bornes, 0.1.0 est 'trouve' dans 10.1.0 et
    un nombre a deux chiffres est trouve dans n'importe quelle page. Le brut est
    consulte en second : nodejs.org/en/download n'expose ses numeros de version
    que dans sa charge JavaScript (mesure du 11/09/2026)."""
    # ㉕ (14/09/2026) l'espace du nombre (normale, insecable, fine) est neutralisee ici — re.escape ne l'echappe
    #    plus depuis Python 3.7 — et « ,00 » / « .00 » apres le nombre ne le rendent pas absent : « 1 689,00 € »
    #    porte bien 1 689 (consomac, note de controle du 13/09 : faux positif).
    corps_n = re.sub(r"[ \u00a0\u202f]", "[ \u00a0\u202f]?", re.escape(n))
    motif = re.compile(r"(?<![\d.,])" + corps_n + r"(?:[.,]0+)?(?![\d.,])")
    motif_v = re.compile(r"(?<![\d.])v" + re.escape(n) + r"(?![\d.])")
    for u, r in textes.items():
        if motif.search(r):
            return u, "texte"
    for u, raw in bruts.items():
        if motif.search(raw) or motif_v.search(raw):
            return u, "brut (rendu JS)"
    return None, None

# ── B. citations anglaises de 6 mots ou plus (㉔, 13/09/2026 : huit auparavant)
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
# ㉓ (13/09/2026) la source NOMMEE a cote de la citation : un domaine ecrit juste apres la fermeture
#    (« (Gurman, selon consomac.fr du 26/08) »), jusqu'a la fin de la phrase ou de la ligne ; ou, juste
#    avant l'ouverture, un domaine ou un nom qui « titre », « ecrit », « rapporte » la citation
#    (« MacRumors (25/08) titre "…" »). Le nom est apparie aux domaines listes comme en A4 (⑳).
#    Un nom sans page listee ne donne rien : c'est la passe A (site nu) qui le voit.
attrib = {}
dit_par = {}    # ㉚ la note fait-elle DIRE la phrase a quelqu'un via la page (« Gurman, cité par 9to5Mac ») — ou cite-t-elle la prose de la page ?
cits_fr = {}
NOMME = re.compile(r"(?<![\wÀ-ÿ])([A-ZÀ-Ý][\wÀ-ÿ-]{2,}(?:\s+[A-ZÀ-Ý][\wÀ-ÿ-]+)?)\s*(?:\([^)]{0,40}\))?\s*"
                   r"(?:titre|écrit|rapporte|publie|annonce|indique|précise|cite)\s*:?\s*$", re.I)
CONT = ("—", "–", ")", ",", "(", "·", ";", ":")
def ligne_logique_apres(z):
    """un lien pose dans la phrase la coupe a l'extraction : on recolle les libelles de liens et les
    morceaux qui s'ouvrent par une ponctuation de continuation (meme regle qu'en A4)"""
    segs = z.split("\n")
    out = segs[0]
    for sg in segs[1:]:
        if sg.strip() in libelles_lies or (sg.strip()[:1] in CONT and sg.strip()):
            out += " " + sg.strip()
        else:
            break
    return out
def ligne_logique_avant(z):
    segs = z.split("\n")
    out = segs[-1]
    for sg in reversed(segs[:-1]):
        if sg.strip() in libelles_lies or (out.strip()[:1] in CONT and out.strip()):
            out = sg.strip() + " " + out
        else:
            break
    return out
def source_nommee(avant, apres):
    apres = re.split(r"\.\s", ligne_logique_apres(apres[:200]), 1)[0]
    doms = [sans_www(d) for d in re.findall(DOM, apres, re.I)]
    doms = [d for d in doms if pages_de(d)]
    if doms:
        return set(doms)
    avant = re.split(r"\.\s", ligne_logique_avant(avant[-140:]))[-1]
    doms = [sans_www(d) for d in re.findall(DOM, avant, re.I)]
    doms = [d for d in doms if pages_de(d)]
    if doms:
        return set(doms[-1:])            # le plus proche de l'ouverture
    # ㉚ un LIBELLE de lien dans la phrase (« Gurman, cité par 9to5Mac (23/08/2026) : "…" et "…" ») nomme la page
    #    de sa cible — meme quand une premiere citation le separe de la seconde. Le plus proche de l'ouverture.
    pos_ = [(avant.rfind(lib), lib) for lib in lib_hote if lib in avant]
    if pos_:
        return {lib_hote[max(pos_)[1]]}
    m_ = NOMME.search(avant)
    if m_:
        nom_ = m_.group(1)
        return set(hote(u) for u in urls if apparie(nom_, hote(u)) and len(cle(nom_)) >= 4)
    return set()
NOM_ATTR = re.compile(r"(?:\bselon|\bpar|d[’']apr[eè]s|\bde|\bpour|[—–(:;,])\s*(?:l[’']|la\s|le\s|les\s|du\s|des\s|un\s|une\s)?"
                      r"(?:guide\s|expertise\s|page\s|rapport\s|site\s|note\s)?([A-ZÀ-Ý][\wÀ-ÿ-]{2,}(?:\s+[A-ZÀ-Ý][\wÀ-ÿ-]+){0,2})")
def source_nommee_fr(avant, apres):
    """㉖ la source nommee d'une citation francaise : celle de ㉓ (domaines, « X titre »), plus un NOM attribue
    dans la phrase, avant ou apres (« par l'INSERM 2016 », « (ANESM, 18 décembre 2015 » , « selon Unafam »),
    apparie aux pages listees comme en A4 (⑳). Un nom sans page listee ne donne rien."""
    doms = set(source_nommee(avant, apres))
    apres_l = re.split(r"\.\s", ligne_logique_apres(apres[:200]), 1)[0]
    avant_l = re.split(r"\.\s", ligne_logique_avant(avant[-160:]))[-1]
    for z in (apres_l, avant_l):
        for m_ in NOM_ATTR.finditer(z):
            nom_ = m_.group(1)
            if len(cle(nom_)) < 3 or cle(nom_.split()[0]) in VIDES:
                continue
            doms |= set(hote(u) for u in urls if apparie(nom_, hote(u)))
    return doms
# ⑮ (12/09/2026) un guillemet droit colle a un chiffre est un POUCE (« 27" QHD »), pas une citation :
#    sur la veille iMac du 05/07, deux tailles d'ecran encadraient une ligne de tableau, lue comme
#    une citation anglaise de 8 mots « absente des pages ». Ouverture et fermeture non precedees d'un chiffre.
#    un guillemet droit OUVRANT n'est pas colle a une lettre (la fermeture de "induire" suivie de l'ouverture de
#    "covert" fabriquait la « citation » « un état hypnotique chez une tierce personne… » — hypnose n°14, 15/09/2026)
for m in re.finditer(r"(?:«|(?<![\wÀ-ÿ])\")\s*([^»\"]{9,700}?)\s*(?:»|\"(?![\wÀ-ÿ]))", corps):   # 700 : une citation hagiographique tient sur 500 caracteres (㉗)
    c = re.sub(r"\s+", " ", m.group(1)).strip()
    if re.search(r"[<>{}=]|//|\w\(\)", c):   continue      # code, pas prose ; « ; » n'exclut plus (« in his heart; a stream of tears » — Thondup, dzogchen 16, ㉗), ni « … »
    if not re.search(r"[A-Za-zÀ-ÿ]", c):       continue
    # une citation entre crochets de correction (« [Corrigé le … : la première version citait « … »] ») cite
    # l'erreur, elle ne l'affirme pas : exemptee dans les deux langues (17/09/2026 — astrologie n°07)
    av_ = corps[max(0, m.start() - 300):m.start()]
    if "[" in av_.rsplit("]", 1)[-1] and "]" in corps[m.end():m.end() + 400]:
        continue
    if FR.search(c) or not OUTILS.search(c):
        # ㉖ citation FRANCAISE — un mot-outil francais, ou aucun mot-outil anglais (« contradictoires », un seul
        #    mot, n'a ni l'un ni l'autre : le document est francais, la citation l'est) : neuf lettres au moins,
        #    hors crochets de correction, avec sa source nommee
        lettres = len(re.findall(r"[A-Za-zÀ-ÿ]", c))
        if lettres >= 9:
            nommes_ = source_nommee_fr(corps[max(0, m.start() - 160):m.start()], corps[m.end():m.end() + 200])
            # la parole d'une vignette (« il répète « j'en peux plus » »), la question que la lecon propose de se
            # poser, la formulation qu'elle discute : ce sont ses propres mots, pas une citation — sans source
            # nommee, on ne les cherche pas
            parole = re.search(r"\b(?:dit|disent|répète|pense|crie|murmure|verbalis\w*|propos|phrase|question|formul\w*|"
                               r"écrit|note[sz]?|intitul\w*|appel\w*|terme|mot|expression)\b[^«»\n]{0,40}$", av_[-80:], re.I)
            if nommes_ or not parole:
                cits_fr[c] = cits_fr.get(c, set()) | nommes_
        continue
    if len(c.split()) < 6:                      continue      # anglais : six mots ou plus (㉔)
    if not c[:1].isalpha():                     continue      # (un titre francais peut commencer par un chiffre : « 6e cycle… » — B-FR l'a deja pris)
    # ⚠️ une citation est une PHRASE, pas un NOM. Un nom propre ou un intitule de
    #    produit entre guillemets n'a aucun mot-outil anglais — et n'a pas a etre
    #    cherche sur une page. Sans ce filtre, la lecon placement-financier n°13
    #    voyait signaler « Tracker CAC 40 (DR) UCITS ETF - Dist », un nom que la
    #    lecon declare elle-meme FICTIF deux lignes plus haut (11/09/2026).
    # l'attribution « — Auteur » finale n'est pas la citation : on la retire avant de
    # chercher, sinon une citation EXACTE est declaree absente (11/09/2026).
    c = re.split(r"\s+[\u2014-]\s+(?=[A-Z\u00c0-\u00dd][^.]{2,60}$)", c)[0].strip()
    if len(c.split()) >= 6:
        cits.add(c)
        attrib[c] = attrib.get(c, set()) | source_nommee(corps[max(0, m.start() - 140):m.start()], corps[m.end():m.end() + 200])
        av_c = corps[max(0, m.start() - 140):m.start()]
        dit_par[c] = dit_par.get(c, False) or bool(
            re.search(r"cit[ée]e?s?\s+(?:par|dans)|rapport[ée]e?s?\s+par|\bselon\b|d[’']apr[eè]s|\bsays?\b|\bsaid\b|\bdit\b|d[ée]clar|affirm", av_c, re.I)
            and not re.search(r"titre|headline|intitul", av_c[-60:], re.I))
# ⑰ (12/09/2026) une page qui n'a PAS PU ETRE LUE (0 octet : reseau, mur, delai) n'est pas une
#    page qui ne porte pas la phrase. nodejs.org/en/download repondait 0 octet, et C2 concluait
#    « cette page NE la porte PAS » sur le vide. Sur une page non lue on ne conclut rien :
#    NON VERIFIABLE, compte a part, exit 3 s'il ne reste que cela.
non_lues = [u for u in urls if u not in non_textuels and not bruts.get(u)
            and not re.search(r"://(?:localhost|127\.0\.0\.1)", u)]      # les adresses locales du projet ne sont pas des pages
print("\nB. CITATIONS ANGLAISES DE 6 MOTS OU PLUS : %d" % len(cits))
ko_b = 0
non_verif = 0
def entre_guillemets(c, u):
    """㉚ la phrase est-elle ENTRE GUILLEMETS sur la page u (“…”, "…", «…», „…“) ? On cherche ses mots, dans l'ordre,
    precedes d'un guillemet ouvrant a moins de trois caracteres. None si la phrase n'y est pas du tout."""
    t_ = textes.get(u, "")
    mots_ = re.findall(r"[A-Za-z0-9]+", c)
    if len(mots_) < 3 or not t_:
        return None
    corps_ = r"[^A-Za-z0-9]+".join(re.escape(w) for w in mots_)
    if not re.search(corps_, t_, re.I):
        return None
    return bool(re.search(r"[“\"«„‘']\s?[^A-Za-z0-9]{0,2}" + corps_, t_, re.I))
a_relire_b = 0
for c in sorted(cits):
    u, how = ou_trouve(c)
    nommes = attrib.get(c, set())
    if os.environ.get("DEBUG"):
        print("   [debug B] %r -> trouvee %s, nommes %s, dit_par %s" % (c[:50], u, sorted(nommes), dit_par.get(c)))
    if u and nommes:
        # ㉓ la citation est trouvee : est-ce sur une page de la source que la note lui prete ?
        trouvees = ou_trouve_toutes(c)
        chez = [t_ for t_ in trouvees if any(hote(t_) == d or hote(t_).endswith("." + d) for d in nommes)]
        if chez:
            u = chez[0]
            # ㉚ presence n'est pas parole : sur la page nommee, la phrase est-elle entre guillemets ?
            g_chez = [entre_guillemets(c, t_) for t_ in chez] if dit_par.get(c) else []
            if os.environ.get("DEBUG"):
                print("   [debug ㉚] %r -> nommes %s, dit_par %s, guillemets %s" % (c[:50], sorted(nommes), dit_par.get(c), g_chez))
            if any(g_chez):
                pass
            elif g_chez and all(g is False for g in g_chez):
                ailleurs = [t_ for t_ in trouvees if t_ not in chez and entre_guillemets(c, t_)]
                if ailleurs:
                    ko_b += 1
                    print("   MAL ATTRIBUEE %s\n             -> prêtée à %s, où elle est dans la voix de l'auteur, SANS guillemets ; elle est entre guillemets sur %s (㉚ reprise nue)"
                          % (c[:76], "/".join(sorted(nommes)), ailleurs[0]))
                    continue
                a_relire_b += 1
                print("   A RELIRE %s\n             -> prêtée à %s : la phrase y est SANS guillemets, dans la voix de l'auteur — qui parle ? (㉚, non bloquant)"
                      % (c[:76], "/".join(sorted(nommes))))
                continue
        else:
            attendues = sum((pages_de(d) for d in nommes), [])
            if any(a_ in non_lues for a_ in attendues):
                non_verif += 1
                print("   NON VERIFIABLE %s\n             -> prêtée à %s, dont une page n'a pas été lue ; trouvée sur %s"
                      % (c[:76], "/".join(sorted(nommes)), trouvees[0]))
            else:
                ko_b += 1
                print("   MAL ATTRIBUEE %s\n             -> prêtée à %s (%d page(s) lue(s), aucune ne la porte) ; elle est sur %s (㉓)"
                      % (c[:76], "/".join(sorted(nommes)), len(attendues), ", ".join(trouvees)))
            continue
    if u:
        print("   OK      %s\n             -> %s (%s)%s" % (c[:76], u, how, " — prêtée à " + "/".join(sorted(nommes)) + ", appariée (㉓)" if nommes else ""))
    elif non_lues or non_textuels:
        non_verif += 1
        print("   NON VERIFIABLE %s\n             -> sur aucune page LUE ; %d page(s) non lue(s), %d PDF non analyse(s)" % (c[:76], len(non_lues), len(non_textuels)))
    else:
        ko_b += 1
        print("   ABSENTE %s\n             -> sur AUCUNE page listee" % c[:76])

# ── B-FR (㉖). Les pages francaises se reconnaissent a leurs mots-outils ; une citation francaise pretee a une
#    page anglaise peut etre une traduction : on ne tranche pas.
def page_fr(u):
    t_ = textes.get(u, "")
    return len(FR.findall(t_)) / max(1, len(t_.split())) >= 0.08
a_relire_fr = 0
print("\nB-FR. CITATIONS FRANCAISES ENTRE GUILLEMETS (9 lettres ou plus ; sans source nommee, 4 mots ou plus) : %d" % len(cits_fr))
if os.environ.get("DEBUG"):
    for c in sorted(cits_fr): print("   [debug] %r -> nommes %s" % (c[:60], sorted(cits_fr[c])))
for c in sorted(cits_fr):
    nommes = cits_fr[c]
    trouvees = ou_trouve_toutes(c)
    if not nommes:
        if len(c.split()) < 4:
            continue                     # un terme entre guillemets sans source nommee (« saupoudrage ») n'est pas une citation a chercher
        if trouvees:
            print("   OK      %s\n             -> %s (sans source nommée à côté)" % (c[:76], trouvees[0]))
        else:
            a_relire_fr += 1
            print("   A RELIRE %s\n             -> sur aucune page lue, et aucune source nommée à côté : traduction ou reformulation ? (non bloquant)" % c[:76])
        continue
    attendues = sum((pages_de(d) for d in nommes), [])
    chez = [t_ for t_ in trouvees if t_ in attendues]
    if chez:
        print("   OK      %s\n             -> %s — prêtée à %s, appariée (㉖)" % (c[:76], chez[0], "/".join(sorted(nommes))))
    elif any(a_ in non_lues or a_ in non_textuels or len(textes.get(a_, "")) < 500 for a_ in attendues):
        # une FACADE (moins de 500 caracteres utiles : mur, page d'attente, 2xx vide) n'est pas une page lue —
        # ipubli.inserm.fr a rendu 94 caracteres a un passage du harnais le 14/09, 89 984 au suivant
        non_verif += 1
        print("   NON VERIFIABLE %s\n             -> prêtée à %s : page non lue, façade (< 500 car.) ou PDF non analysé — à vérifier à la main%s"
              % (c[:76], "/".join(sorted(nommes)), (" ; trouvée sur " + trouvees[0]) if trouvees else ""))
    elif not any(page_fr(a_) for a_ in attendues):
        a_relire_fr += 1
        print("   A RELIRE %s\n             -> prêtée à %s, page(s) en anglais : traduction possible, non tranché (non bloquant)" % (c[:76], "/".join(sorted(nommes))))
    else:
        ko_b += 1
        print("   ABSENTE DE LA SOURCE NOMMEE %s\n             -> prêtée à %s (%d page(s) française(s) lue(s), aucune ne la porte)%s (㉖)"
              % (c[:76], "/".join(sorted(nommes)), len(attendues), (" ; elle est sur " + trouvees[0]) if trouvees else ""))

# ── B-NOM (㉙, 19/09/2026). Une affirmation sans guillemets pretee a un nom : « selon l'IEFP », « (AMF) »,
#    « d'apres la CNIL », « l'INSEE indique que ». B et B-FR ne cherchent que ce qui est entre guillemets ;
#    placement n°15 pretait a l'IEFP une hierarchie des biais que sa page ne pose pas (« moutonnier » absent),
#    ai-act 18/09 pretait a un article trois chantiers legislatifs qu'il ne nomme pas. Ici, pas de phrase exacte
#    a chercher : on prend les MOTS PLEINS de la phrase (7 lettres ou plus, hors nom de la source et mots
#    de liaison) et on regarde combien la source nommee les porte sur ses pages listees. En dessous d'un tiers,
#    la phrase n'est pas de cette page : bloquant. Entre un tiers et deux tiers : a relire. Une source sans page
#    listee n'est pas jugee ici (c'est A2 / A4).
LIAISON = {"corrige", "courant", "courants", "notamment", "egalement", "cependant", "toutefois", "principaux", "principal", "principale", "suivant", "suivante",
           "suivants", "certains", "certaines", "plusieurs", "toujours", "souvent", "pendant", "comment", "pourquoi",
           "lorsque", "environ", "ensemble", "generalement", "particulierement", "essentiellement", "notamment", "litterature",
           "exemple", "exemples", "c'est-a-dire", "cestadire", "concernant", "seulement", "actuellement", "desormais",
           "aujourdhui", "maintenant", "surtout", "davantage", "vraiment", "reellement", "directement", "immediatement",
           "rapidement", "simplement", "clairement", "necessairement", "precisement", "consulte", "consultee", "consultes",
           "verifie", "verifiee", "verifiees", "verifies", "source", "sources", "secondaire", "primaire", "officiel", "officielle"}
MARQUEUR_NOM = re.compile(
    r"(?:\b(?:selon|d[’']apr[eè]s)\s+(?:l[’']|la\s|le\s|les\s|une?\s|du\s|des\s)?(?:litt[ée]rature\s(?:de\s|sur\s)?[^,;(]{0,60}?\(?)?"
    r"([A-ZÀ-Ý][\wÀ-ÿ.-]{1,}(?:\s+[A-ZÀ-Ý][\wÀ-ÿ-]+){0,3})"
    r"|\(([A-Z][A-Z0-9-]{1,}[a-z]?)\)"
    r"|(?<![\wÀ-ÿ])([A-ZÀ-Ý][\wÀ-ÿ-]{2,}(?:\s+[A-ZÀ-Ý][\wÀ-ÿ-]+){0,2})(?:\s*\([^)]{0,60}\))?\s+(?:a\s+)?(?:indique|pr[ée]cise|rapporte|[ée]crit|souligne|estime|recense|signale|rappelle|explique|affirme|constate|observe|montre|recommande|publi[ée]|alerte|met\s+en\s+garde)\b)")
def mots_pleins(z, nom):
    exclus = set(cle(w) for w in re.findall(r"[\wÀ-ÿ-]+", nom))
    z = re.sub(DOM, " ", z, flags=re.I)                                    # un domaine n'est pas un mot de la phrase
    z = re.sub(re.escape(nom) + r"\s*\([^)]{0,60}\)", nom, z)             # « AMF (Autorité des marchés financiers) » : le developpe n'est pas un mot a chercher
    out = []
    for w in re.findall(r"[A-Za-zÀ-ÿ][\wÀ-ÿ-]{6,}", z):
        k = cle(w)
        if len(k) >= 7 and k not in LIAISON and k not in exclus and k not in out:
            out.append(k)
    return out
ko_nom = 0
a_relire_nom = 0
phrases_nom = []
for ph in re.split(r"(?<=[.!?])\s+|\n+", corps):
    ph = ph.strip()
    if len(ph) < 40 or "«" in ph or "\"" in ph or "[Corrigé le" in ph or "Journal des corrections" in ph:
        continue
    for m_ in MARQUEUR_NOM.finditer(ph):
        nom_ = m_.group(1) or m_.group(2) or m_.group(3)
        if not nom_ or len(cle(nom_)) < 3 or cle(nom_.split()[0]) in VIDES or cle(nom_) in LIAISON:
            continue
        # « American Psychiatric Association (APA) », « CIM-10 (OMS) » : la parenthese developpe ou situe le NOM qui
        # la precede, elle n'attribue pas la phrase. Une attribution suit un mot ordinaire : « des épargnants (IEFP) ».
        if m_.group(2) and re.search(r"(?:[A-ZÀ-Ý][\wÀ-ÿ-]*|\d[\w-]*)\s*$", ph[:m_.start()]):
            continue
        if re.match(r"(?:Source|Sources|Lien|Page|Voir|Note|Figure|Tableau|Exercice|Situation|Scénario|Leçon|Corrigé)\b", nom_):
            continue
        attendues = [u for u in urls if apparie(nom_, hote(u)) and not re.search(r"://(?:localhost|127\.0\.0\.1)", u)]
        if not attendues:
            continue
        mots = mots_pleins(ph, nom_)
        if len(mots) < 4:
            continue
        phrases_nom.append((ph, nom_, attendues, mots))
        break                                     # une phrase, une attribution : la premiere
print("\nB-NOM. AFFIRMATIONS SANS GUILLEMETS PRETEES A UNE SOURCE NOMMEE (« selon X », « (X) », « X indique ») : %d" % len(phrases_nom))
for ph, nom_, attendues, mots in phrases_nom:
    lues = [u for u in attendues if u not in non_lues and u not in non_textuels and len(textes.get(u, "")) >= 500]
    if not lues:
        non_verif += 1
        print("   NON VERIFIABLE %s\n             -> prêtée à %s : page(s) non lue(s), façade ou PDF" % (ph[:76], nom_))
        continue
    corpus_ = " ".join(pages[u] for u in lues)
    absents = [k for k in mots if k not in corpus_]
    part = 1 - len(absents) / len(mots)
    if part < 0.66 and not any(page_fr(u) for u in lues):
        # une phrase francaise pretee a une page ANGLAISE (Lotsawa House, Tricycle — dzogchen n°16) : ses mots
        # n'y sont pas parce que la page est dans une autre langue, pas parce qu'elle ne le dit pas. A relire.
        a_relire_nom += 1
        print("   A RELIRE %s\n             -> prêtée à %s : page(s) en anglais, %d mots pleins sur %d — traduction, non tranché (non bloquant)"
              % (ph[:76], nom_, len(mots) - len(absents), len(mots)))
        continue
    if part >= 0.66:
        print("   OK      %s\n             -> %s : %d mots pleins sur %d sur ses pages (%s)" % (ph[:76], nom_, len(mots) - len(absents), len(mots), lues[0]))
    elif part >= 0.34 or len(mots) < 6:
        # sous six mots pleins, la phrase est trop courte pour trancher (« TER < 0,5 % typique des ETF selon l'AMF » :
        # quatre mots, tous du redacteur — le chiffre, lui, releve de D) : a relire, jamais bloquant
        a_relire_nom += 1
        print("   A RELIRE %s\n             -> prêtée à %s : %d mots pleins sur %d sur ses pages — absents : %s (non bloquant)"
              % (ph[:76], nom_, len(mots) - len(absents), len(mots), ", ".join(absents)))
    else:
        ko_nom += 1
        print("   PAS SUR LA SOURCE NOMMEE %s\n             -> prêtée à %s : %d mots pleins sur %d seulement — absents : %s (㉙)"
              % (ph[:76], nom_, len(mots) - len(absents), len(mots), ", ".join(absents)))
if not phrases_nom:
    print("      (aucune)")

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
    if all(not bruts.get(u) for u in cibles):
        non_verif += 1          # ⑰ : toutes les pages de ce domaine sont restees vides
        print("   NON VERIFIABLE %-10s pres de %-38s -> page(s) non lue(s) (0 octet) : on ne conclut rien" % (v, dom + chemin))
        continue
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
        # ⚠️ SECOND ACQUITTEMENT, AJOUTE LE 25/09/2026 — LA DERIVE DECLAREE.
        #    Le premier acquittement (ci-dessous, `neuf`) exige que le numero de
        #    REMPLACEMENT annonce par la lecon soit encore celui de la page. Il PERIME :
        #    la lecon appli-ia n°04 ecrit, depuis le 11/09/2026, « REVERIFIEE LE
        #    11/09/2026 : la page affiche desormais v26.8.2 et le v26.7.0 n'y figure
        #    plus » — impeccable — mais nodejs.org/api/fs.html publie la doc de la
        #    version COURANTE : mesure le 25/09/2026, la page porte 26.10.0 et plus
        #    aucune trace de 26.8.2. L'acquittement est tombe, et le controle a
        #    re-accuse pendant deux semaines une ligne qui disait deja la verite.
        #    Un test qu'on ne peut pas ramener au vert finit ignore : c'est ecrit
        #    six lignes plus bas, et c'est arrive au test lui-meme.
        #    Le discriminant qui ne perime pas : la lecon DECLARE que la page ne le
        #    porte plus — ce que le controle vient precisement de mesurer, donc les
        #    deux sont D'ACCORD — ET elle porte DEUX dates distinctes, celle du releve
        #    et celle de la reverification. Le defaut du 28/08/2026 qui a motive la
        #    regle n'a ni l'un ni l'autre : « Vite v8.2.2 — verifiee sur vite.dev/guide/
        #    le 28/08/2026 » affirme que la page LA PORTE, a une seule date, et
        #    vite.dev/guide/ ne l'a jamais portee. Une date seule n'acquitte toujours pas.
        absence = re.search(r"n[’']?(?:y |e l[ae] |e )?(?:figure|porte|apparai[ts]|est)\s+plus"
                            r"|en a disparu|a disparu de|ne s[’']y trouve plus",
                            large, re.I)
        dates = set(re.findall(r"\d{2}/\d{2}/\d{4}", large))
        neuf = None
        if releve:
            # on lit d'abord APRES le marqueur : « affiche desormais v26.8.2 ». Sans cela
            #    le premier numero de la fenetre est retenu, et le message vert annonce un
            #    numero sans rapport (mesure du 11/09/2026 : 24.0.0 au lieu de 26.8.2).
            # ⚠️ APRES LE MARQUEUR, ET NULLE PART AILLEURS (resserre le 25/09/2026).
            #    Le repli « + re.findall(..., large) » cherchait dans TOUTE la fenetre de
            #    800 caracteres : sur la lecon appli-ia n°04, il acquittait la ligne
            #    url.html en annoncant « la page porte maintenant 24.0.0 » — un numero pris
            #    dans une phrase VOISINE et sans rapport (l'historique de depreciation
            #    d'url.parse(), « RÉVOCATION … v24.0.0 »), que nodejs.org/api/url.html
            #    porte effectivement dans son tableau History. La ligne etait juste, mais
            #    acquittee pour une raison fausse — et n'importe quelle ligne fautive
            #    voisine d'un numero que la page porte l'etait aussi. C'est un FAUX NEGATIF,
            #    plus grave que le faux positif corrige le meme jour : le numero de
            #    remplacement doit etre celui que la lecon ANNONCE, donc apres son marqueur.
            candidats = re.findall(r"\bv?(\d+\.\d+\.\d+)\b", large[releve.end():])
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
        elif releve and absence and len(dates) >= 2:
            print("   DERIVE     %-10s pres de %-38s -> la lecon DECLARE que la page ne la "
                  "porte plus, la mesure le confirme, et deux dates l'attestent (%s) : "
                  "derive declaree, pas defaut" % (v, dom + chemin, ", ".join(sorted(dates))))
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
if not cits:    inertes.append("B (aucune citation anglaise de 6 mots ou plus)")
if not cits_fr: inertes.append("B-FR (aucune citation française de 9 lettres ou plus)")
if not phrases_nom: inertes.append("B-NOM (aucune affirmation prêtée à un nom sans guillemets)")
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
if non_lues:
    print(">>> PAGES NON LUES (0 octet) : %d — %s" % (len(non_lues), "; ".join(non_lues)))
    print(">>> Rien n'a pu etre verifie sur elles : relance plus tard, ou verifie a la main.")
pb = len(orphelines) + len(sites_non_listes) + len(sans_adresse) + len(mal_formes) + len(src_sans_adresse) + len(sans_cible) + len(liens_morts) + ko_b + ko_nom + ko_c2
print("\nVERDICT : %d probleme(s) bloquant(s) (A + A2 + A3 + A4 + A5 + A6 + B + B-FR + B-NOM + C2)%s%s%s%s"
      % (pb, " — et %d verification(s) IMPOSSIBLE(S), pages non lues ou PDF" % non_verif if non_verif else "",
         " — et %d citation(s) francaise(s) A RELIRE (non bloquant)" % a_relire_fr if a_relire_fr else "",
         " — et %d attribution(s) sans guillemets A RELIRE (non bloquant)" % a_relire_nom if a_relire_nom else "",
         " — et %d citation(s) reprise(s) nue(s) A RELIRE (㉚, non bloquant)" % a_relire_b if a_relire_b else ""))
print("          %d valeur(s) chiffree(s) a relire en D — a la main, D n'est pas bloquant"
      % ko_d)
sys.exit(1 if pb else (3 if non_verif else 0))
