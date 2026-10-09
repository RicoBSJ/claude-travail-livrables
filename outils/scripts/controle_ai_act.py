#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Étape 5 bis du job `ai-act-veille` — contrôle de la note de veille elle-même.

SORTI DU PROMPT LE 09/10/2026. Il y était inliné et réémis à chaque tour (12 303 octets) ;
le prompt l'appelle désormais par son chemin, comme controle_attributions.py et
controle_decompte.py. Même règle que controle_astrologie_karmique.py et
controle_psychopathologie.py, sortis le 08/10/2026 : appelé par le prompt, jamais recopié.

Le code est repris VERBATIM de la version inlinée (sha256 de la version inlinée :
0e4953566f02897f6893dcae743b7cf40de20a4e0e2a931e4c449ca1af19048b) ; seules deux lignes changent, le chemin qui devient sys.argv[1] et ce docstring.
Validé dans les deux sens le 09/10/2026, sous `env -i`, contre la version inlinée, sur cinq
documents — verdicts et codes de sortie identiques :
  09/10 corrigée  -> 0      09/10 telle que livrée -> 1 (huit signalements)
  02/10 -> 1        25/09 -> 1        18/09 -> 1   (motif (8) seul, à juste titre)

Onze motifs. Il ouvre, avec un agent de navigateur, toutes les pages que la note lie, et
REFUSE la note si :
  (1)  une citation de 2 à 5 mots n'est sur aucune de ces pages
  (2)  une citation ou un nom d'acte du résumé d'un article « Lu en entier » n'est pas sur
       la page de CET article  — ⚠️ ce motif était INERTE du 20/09 au 09/10/2026 : il
       cherchait l'adresse de l'article dans les deux paragraphes SUIVANT son en-tête,
       quand l'hyperlien est dans l'en-tête lui-même
  (3)  un discours du presscorner que l'API rend est déclaré « non lu », ou l'API n'est pas liée
  (4)  une page dite « non extractible » porte 5 000 caractères de texte ou plus
  (5)  une ligne « navette » / « DDADUE » n'a ni lien ni « non vérifié »
  (6)  le niveau d'alerte est 🟢 alors que la note annonce au moins un fait marquant
  (7)  une citation est refermée par une ponctuation que la page ne porte pas
  (8)  un identifiant d'acte dit « non vérifié » est porté par une page LISTÉE, dans son
       texte OU dans un de ses liens (forme du Journal officiel : OJ:L_<année><5 chiffres>)
  (9)  une page dite « sans élément nouveau » porte, dans la fenêtre, une date que la note
       ne cite nulle part
  (10) une taille de page annoncée s'écarte de plus de 2 % de la taille mesurée ici
  (11) un nom d'acte prêté à un article n'existe sur sa page que dans le dernier quart du
       texte, c'est-à-dire dans le mobilier de fin de page, sans que le CORPS le signale

Les motifs (6) et (7) ne coûtent aucun appel réseau. Le seuil du motif (11) est MESURÉ :
sur les huit pages lisibles de l'édition du 09/10/2026, la première occurrence légitime
d'un nom d'acte tombe entre 0,002 et 0,289 de la longueur du texte, et le défaut à 0,813.

Usage : controle_ai_act.py <chemin du .docx>    (exit 0 = conforme, 1 = refusée)
Témoin de non-régression : section 5 ter de outils/scripts/non_regression.sh.
"""
import zipfile, re, sys, html, json, subprocess
p = sys.argv[1]
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
z = zipfile.ZipFile(p); x = z.read("word/document.xml").decode("utf-8")
rels = dict(re.findall(r'Id="([^"]+)"[^>]*Target="([^"]+)"', z.read("word/_rels/document.xml.rels").decode("utf-8")))
rels.update({m.group(2): m.group(1) for m in re.finditer(r'Target="([^"]+)"[^>]*Id="([^"]+)"', z.read("word/_rels/document.xml.rels").decode("utf-8"))})
ps = re.findall(r"<w:p(?:\s[^>]*)?>.*?</w:p>", x, re.S)
def t_of(q): return re.sub(r"\[Corrigé le \d\d/\d\d/\d{4} :.*?\]", "", html.unescape("".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", q))), flags=re.S)
def liens(q): return [html.unescape(rels[r]) for r in re.findall(r'r:id="([^"]+)"', q) if r in rels and rels[r].startswith("http")]
fin = [i for i, q in enumerate(ps) if "Journal des corrections" in t_of(q)]
if fin: ps = ps[:fin[0]]
T = [t_of(q) for q in ps]; L = [liens(q) for q in ps]
urls = sorted({u for l in L for u in l})
def norm(s): return re.sub(r"\s+", " ", s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace(" ", " ")).strip().lower()
cache, cbrut = {}, {}
def brut(u):
    if u not in cbrut:
        r = subprocess.run(["curl", "-s", "-L", "--max-time", "30", "-A", UA, u], capture_output=True)
        cbrut[u] = r.stdout.decode("utf-8", "ignore")
    return cbrut[u]
def page(u):
    if u in cache: return cache[u]
    raw = brut(u)
    try:
        j = json.loads(raw); parts = []
        def walk(o):
            if isinstance(o, dict): [walk(v) for v in o.values()]
            elif isinstance(o, list): [walk(v) for v in o]
            elif isinstance(o, str): parts.append(o)
        walk(j); raw = " ".join(parts)
    except Exception: pass
    raw = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", raw, flags=re.S | re.I)
    cache[u] = norm(html.unescape(re.sub(r"<[^>]+>", " ", raw))); return cache[u]
pb = []
# 1. CITATIONS COURTES (2 à 5 mots) — le contrôle commun commence à 6 : en dessous, on cherche ici, sur les pages de la note
courtes = [(i, m.group(1)) for i, t in enumerate(T) for m in re.finditer(r"«\s?([^»]{2,120}?)\s?»", t)
           if 2 <= len(re.findall(r"[A-Za-zÀ-ÿ0-9]+", m.group(1))) <= 5 and not re.search(r"(?i)(édition|note|cadrage|prompt|consigne|rubrique|section)[^«]{0,80}$", t[:m.start()])]
for i, q in courtes:
    ou = [u for u in urls if norm(q) in page(u)]
    if not ou:
        vides = [u for u in urls if len(page(u)) < 200]
        print("CITATION COURTE ABSENTE DES PAGES DE LA NOTE : «", q, "» (¶%d)" % i + (" — pages non lues : " + ", ".join(vides) if vides else "")); pb.append("citation courte « %s »" % q)
# 2. NOMS D'ACTES DANS LE RÉSUMÉ D'UN ARTICLE « LU EN ENTIER » — sur la page de CET article
for i, t in enumerate(T):
    if not re.match(r"Article \d+ — Lu", t): continue
    lien = [u for j in (i, i + 1, i + 2) if j < len(L) for u in L[j]]
    if not lien: continue
    corps = ""
    for j in range(i + 2, len(T)):
        if not T[j].strip(): break
        corps += " " + T[j]
    for n in set(re.findall(r"\b(?:[A-Z][A-Za-z-]+ ){1,4}(?:Act|Strategy)\b|\bDigital Omnibus\b(?: on AI| IA| AI)?", corps)):
        if norm(n) not in page(lien[0]): print("ACTE NOMMÉ ABSENT DE L'ARTICLE :", n, "->", lien[0]); pb.append("« %s » prêté à %s" % (n, lien[0]))
    for q in re.findall(r"«\s?([^»]{2,200}?)\s?»", corps):
        if len(re.findall(r"[A-Za-zÀ-ÿ0-9]+", q)) >= 2 and norm(q) not in page(lien[0]): print("CITATION ABSENTE DE L'ARTICLE RÉSUMÉ : «", q, "» ->", lien[0]); pb.append("« %s » prêtée à l'article" % q)
# 3. DISCOURS DU PRESSCORNER — l'API rend le texte : « non lu » ne s'écrit pas, et le lien de l'API se cite
for ref in set(re.findall(r"presscorner/detail/\w+/([A-Z]+_\d+_\d+)", " ".join(urls))):
    api = "https://ec.europa.eu/commission/presscorner/api/documents?reference=%s&language=en" % ref.replace("_", "/", 1).replace("_", "/")
    if len(page(api)) < 5000: continue
    nonlu = [i for i, t in enumerate(T) if re.search(r"(?i)(presscorner|discours).{0,250}non (lu|consult)|non (lu|consult).{0,250}(presscorner|discours)", t)]
    if nonlu: print("DISCOURS DÉCLARÉ NON LU (¶%s) ALORS QUE L'API LE REND : %s (%d caractères)" % (nonlu, api, len(page(api)))); pb.append("discours %s déclaré non lu" % ref)
    if not any("api/documents?reference=" in u for u in urls): print("LIEN DE L'API DU PRESSCORNER ABSENT DE LA NOTE :", api); pb.append("lien API %s absent" % ref)
# 4. PAGE DÉCLARÉE NON EXTRACTIBLE — on la lit : au-delà de 5 000 caractères de texte, elle était lisible
for i, t in enumerate(T):
    if not re.search(r"(?i)non extractible|HTML brut|rendu en JavaScript|JS-only|non lisible", t): continue
    for u in urls:
        dom = re.sub(r"^https?://(www\.)?", "", u).split("/")[0]
        if dom in t or u in L[i]:
            n = len(page(u))
            if n >= 5000: print("PAGE DÉCLARÉE NON EXTRACTIBLE MAIS LISIBLE : %s — %d caractères de texte (¶%d)" % (u, n, i)); pb.append("%s dite non extractible" % dom)
# 5. RÉFÉRENCE HÉRITÉE SANS SOURCE — une ligne « en navette » / DDADUE porte un lien ou se dit non vérifiée
for i, t in enumerate(T):
    if re.search(r"(?i)navette|DDADUE", t) and not L[i] and not re.search(r"(?i)non vérifié", t):
        print("HÉRITAGE SANS SOURCE NI RÉSERVE (¶%d) :" % i, t[:110]); pb.append("¶%d hérité sans source" % i)
# ⑥ NIVEAU D'ALERTE — le 🟢 est réservé aux semaines sans fait marquant (étape 3bis)
nb = [int(m.group(1)) for t in T for m in re.finditer(r"(?i)faits? marquants? de la semaine\s*:\s*(\d+)", t)]
niv = [i for i, t in enumerate(T) if re.search(r"(?i)niveau d'alerte", t)]
if nb and niv and nb[0] >= 1:
    for i in niv:
        if "🟢" in T[i] or re.search(r"(?i)\bVERT\b", T[i]):
            print("NIVEAU VERT AVEC %d FAIT(S) MARQUANT(S) (¶%d) :" % (nb[0], i), T[i][:120]); pb.append("niveau 🟢 avec %d fait(s) marquant(s)" % nb[0])

# ⑦ CITATION REFERMÉE PAR UNE PONCTUATION QUI N'EST PAS CELLE DE LA PAGE
for i, t in enumerate(T):
    for m in re.finditer(r"«\s?([^»]{12,400}?)\s?»", t):
        q = m.group(1)
        if not re.search(r"[.?!]$", q): continue
        if len(re.findall(r"[A-Za-zÀ-ÿ0-9]+", q)) < 4: continue
        if norm(q) in ("",): continue
        entier = any(norm(q) in page(u) for u in urls)
        tronque = any(norm(q[:-1]) in page(u) for u in urls)
        if tronque and not entier:
            print("CITATION REFERMÉE PAR UNE PONCTUATION INVENTÉE (¶%d) : «" % i, q[-70:], "» — la page continue la phrase"); pb.append("ponctuation inventée « …%s »" % q[-40:])

# ⑧ IDENTIFIANT DÉCLARÉ NON VÉRIFIÉ ALORS QU'UNE PAGE LISTÉE LE PORTE (texte OU lien)
for i, t in enumerate(T):
    if not re.search(r"(?i)non vérifi|non revérifi|hérité", t): continue
    if re.search(r"(?i)vérifiée?s? le \d\d/\d\d/\d{4}", t): continue
    for ident in set(re.findall(r"\b(?:20\d\d/\d{3,5}|L_20\d{8}|3\d{4}R\d{4})\b", t)):
        formes = {ident, ident.lower()}
        m_ = re.match(r"(20\d\d)/(\d{3,5})$", ident)
        if m_: formes |= {"L_%s%05d" % (m_.group(1), int(m_.group(2))), "%s%05d" % (m_.group(1), int(m_.group(2)))}
        ou = [u for u in urls if any(f in page(u) or f in brut(u) for f in formes)]
        if ou:
            print("IDENTIFIANT DÉCLARÉ NON VÉRIFIÉ MAIS PORTÉ PAR UNE PAGE LISTÉE (¶%d) : %s -> %s" % (i, ident, ou[0])); pb.append("%s dit non vérifié" % ident)

# ⑨ « SANS ÉLÉMENT NOUVEAU » ALORS QUE LA PAGE PORTE UNE DATE DANS LA FENÊTRE
MOIS = {"janvier":1,"février":2,"mars":3,"avril":4,"mai":5,"juin":6,"juillet":7,"août":8,"septembre":9,"octobre":10,"novembre":11,"décembre":12,
        "january":1,"february":2,"march":3,"april":4,"may":5,"june":6,"july":7,"august":8,"september":9,"october":10,"november":11,"december":12,
        "jan":1,"feb":2,"mar":3,"apr":4,"jun":5,"jul":7,"aug":8,"sep":9,"sept":9,"oct":10,"nov":11,"dec":12}
fen = None
for t in T:
    m = re.search(r"(?i)fenêtre couverte\s*:\s*(\d{1,2})\s+(\w+)\s+(\d{4})\s*(?:→|->|au)\s*(\d{1,2})\s+(\w+)\s+(\d{4})", t)
    if m:
        a = (int(m.group(3)), MOIS.get(m.group(2).lower(), 0), int(m.group(1)))
        b = (int(m.group(6)), MOIS.get(m.group(5).lower(), 0), int(m.group(4)))
        fen = (a, b); break
def dates(txt):
    out = set()
    for m in re.finditer(r"\b(\d{1,2})\s+([A-Za-zÀ-ÿ]{3,9})\.?,?\s+(20\d\d)\b", txt):
        mo = MOIS.get(m.group(2).lower().rstrip("."), 0)
        if mo: out.add((int(m.group(3)), mo, int(m.group(1))))
    for m in re.finditer(r"\b([A-Za-zÀ-ÿ]{3,9})\.?\s+(\d{1,2}),\s*(20\d\d)\b", txt):
        mo = MOIS.get(m.group(1).lower().rstrip("."), 0)
        if mo: out.add((int(m.group(3)), mo, int(m.group(2))))
    for m in re.finditer(r"\b(\d{1,2})/(\d{1,2})/(20\d\d)\b", txt):
        out.add((int(m.group(3)), int(m.group(2)), int(m.group(1))))
    return out
if fen:
    for i, t in enumerate(T):
        if not re.search(r"(?i)sans élément nouveau|aucune? (?:publication|nouveauté)|semaine (?:creuse|institutionnelle creuse)", t): continue
        for u in [v for j in (i, i - 1) if 0 <= j < len(L) for v in L[j]][:1]:
            # une date que la note CITE est traitée, même sans son année (« (01/10, 30/09, 29/09) », note du 02/10)
            tn = " ".join(T); vues = dates(tn)
            for mm_ in re.finditer(r"\b(\d{1,2})/(\d{1,2})\b(?!/)", tn):
                for an_ in {fen[0][0], fen[1][0]}: vues.add((an_, int(mm_.group(2)), int(mm_.group(1))))
            dd = sorted(d for d in dates(page(u)) if fen[0] <= d <= fen[1] and d not in vues)
            if dd:
                print("DATE DANS LA FENÊTRE, JAMAIS CITÉE PAR LA NOTE, SUR UNE PAGE DITE SANS ÉLÉMENT NOUVEAU (¶%d) : %s -> %s" % (i, u, ", ".join("%04d-%02d-%02d" % d for d in dd[:4]))); pb.append("%s : date non citée dans la fenêtre" % re.sub(r"^https?://(www\.)?", "", u).split("/")[0])

# ⑩ TAILLE DE PAGE ANNONCÉE CONTRE TAILLE MESURÉE (±2 %) — la mesure de référence est celle de ce script
for i, t in enumerate(T):
    annonces = [int(re.sub(r"\D", "", m.group(1))) for m in re.finditer(r"([0-9][0-9  ]{2,12})\s*(?:car\.|caractères)", t)]
    annonces = [a_ for a_ in annonces if a_ >= 500]
    if len(annonces) != 1: continue        # deux tailles dans un paragraphe : on ne sait pas laquelle va à quel lien
    ann = annonces[0]
    for u in [v for j in (i, i - 1, i + 1) if 0 <= j < len(L) for v in L[j]][:1]:
        vu = len(page(u))
        if vu < 500: continue              # page qui ne rend rien : non lue, on ne conclut pas
        if abs(vu - ann) > 0.02 * vu:
            print("TAILLE ANNONCÉE FAUSSE (¶%d) : %d annoncés contre %d mesurés pour %s" % (i, ann, vu, u)); pb.append("taille %d vs %d" % (ann, vu))

# ⑪ NOM D'ACTE TROUVÉ SEULEMENT DANS LE MOBILIER DE FIN DE PAGE (dernier quart)
for i, t in enumerate(T):
    if not re.match(r"Article \d+ — Lu", t): continue
    lien = [u for j in (i, i + 1, i + 2) if j < len(L) for u in L[j]]
    if not lien: continue
    corps = ""
    for j in range(i + 2, len(T)):
        if not T[j].strip(): break
        corps += " " + T[j]
    pg = page(lien[0]); n = len(pg)
    for nom in set(re.findall(r"\b(?:[A-Z][A-Za-z-]+ ){1,4}(?:Act|Strategy)\b|\bDigital Omnibus\b(?: on AI| IA| AI)?", corps)):
        pos = [mm.start() for mm in re.finditer(re.escape(norm(nom)), pg)]
        if pos and n and min(pos) / n > 0.75 and not re.search(r"(?i)ne mentionne (?:pas|jamais)|hors du corps|mobilier de", corps):
            print("ACTE TROUVÉ SEULEMENT DANS LE MOBILIER DE FIN DE PAGE (¶%d) : %s -> %s (position %.3f, %d occurrence(s))"
                  % (i, nom, lien[0], min(pos) / n, len(pos))); pb.append("« %s » dans le mobilier de %s" % (nom, lien[0]))

if pb: sys.exit("NOTE REFUSÉE — " + " ; ".join(pb))
print("OK — citations courtes, actes sur leur article et hors mobilier, discours lu par l'API, pages reçues lues, héritages sourcés, niveau cohérent avec les faits marquants, ponctuation des citations fidèle, identifiants cherchés jusque dans les liens, dates des pages dites sans nouveauté relues, tailles de page mesurées")
