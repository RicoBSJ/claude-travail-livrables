#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""controle_astrologie_karmique.py — étape 5 bis du job astrologie-karmique-lecon.

SORTI DU PROMPT LE 08/10/2026. Le script était inliné dans le prompt du job
(12 398 octets sur 61 543, soit 20 %), donc réémis à chaque tour : il pesait sur le
cache de chaque exécution sans jamais changer. Il suit désormais la règle que
`CLAUDE.md` fixe déjà pour les contrôles communs — « appelés par les prompts, jamais
copiés ». Comportement inchangé, à la ligne près : validé dans les deux sens le
08/10/2026 contre la version inlinée, verdicts identiques sur les leçons n°09 et n°10.

Usage :  python3 outils/scripts/controle_astrologie_karmique.py <chemin du .docx>
Sortie : 0 si aucun des sept motifs, 1 si la leçon est refusée.

REFUSE SUR SEPT MOTIFS — ① « Noeud » sans ligature hors adresse web ; ② un ¶ qui annonce
l'entrée dans un signe avec une longitude sans la borne correcte (haute si rétrograde) ;
③ une valeur décimale en degrés absente de toutes les pages liées et non déclarée comme
constante standard ; ④ une citation de DEUX À CINQ MOTS, non française, dans un ¶ qui
porte un lien et absente des pages de ce ¶ (recherche INSENSIBLE À LA CASSE) ; ⑤ un nom
propre d'un énoncé qui désigne une page comme sa source, absent de cette page ; ⑥ une page
qui répond 200 en ne rendant que moins de 500 caractères alors qu'on lui attribue un
chiffre ou une citation ; ⑦ une page qui ne répond pas après trois essais sans être
déclarée non lue. Ignore les marqueurs de correction et tout ce qui suit
« 📝 Journal des corrections ».
"""
import sys
if len(sys.argv) < 2:
    sys.exit("usage : controle_astrologie_karmique.py <chemin du .docx>")

import zipfile, re, sys, html, subprocess, unicodedata
p = sys.argv[1]
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
SIGNES = {"Bélier":0, "Taureau":30, "Gémeaux":60, "Cancer":90, "Lion":120, "Vierge":150, "Balance":180,
          "Scorpion":210, "Sagittaire":240, "Capricorne":270, "Verseau":300, "Poissons":330}
z = zipfile.ZipFile(p); x = z.read("word/document.xml").decode("utf-8")
rels = {}
for m in re.finditer(r"<Relationship [^>]*>", z.read("word/_rels/document.xml.rels").decode("utf-8")):
    i_ = re.search(r'Id="([^"]+)"', m.group(0)); t_ = re.search(r'Target="(https?://[^"]+)"', m.group(0))
    if i_ and t_: rels[i_.group(1)] = html.unescape(t_.group(1))
ps = re.findall(r"<w:p(?:\s[^>]*)?>.*?</w:p>", x, re.S)
def brut(q): return html.unescape("".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", q)))
T = [re.sub(r"\[(?:Corrigé|Précisé|Ajouté) le \d\d/\d\d/\d{4}.*?\]", "", brut(q), flags=re.S) for q in ps]
fin = [i for i, t in enumerate(T) if "Journal des corrections" in t]; n_fin = fin[0] if fin else len(T)
LIENS = [[rels[r] for r in re.findall(r'r:id="([^"]+)"', ps[i]) if r in rels] for i in range(len(ps))]
URLS = sorted({u for i in range(n_fin) for u in LIENS[i]})
def hors_lien(q):
    return html.unescape("".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>",
           re.sub(r"(?s)<w:hyperlink\b.*?</w:hyperlink>", " ", q))))
TH = [re.sub(r"\[(?:Corrigé|Précisé|Ajouté) le \d\d/\d\d/\d{4}.*?\]", "", hors_lien(q), flags=re.S) for q in ps]

pb = []

# ① LA LIGATURE Œ, HORS ADRESSES (le parcours écrit « Nœud » depuis la leçon 03)
for i, t in enumerate(T[:n_fin]):
    # les adresses écrites SANS protocole comptent aussi : « astrologie-autrement.com/noeuds-… »
    # faisait crier le motif sur une ligne de ressources parfaitement correcte (24/09/2026)
    sans_url = re.sub(r"https?://\S+|\b[\w-]+\.(?:com|fr|org|net|eu|io)/\S*", " ", t)
    if re.search(r"\b[Nn]oeud", sans_url):
        print("① LIGATURE PERDUE (¶%d) : « %s… » — ce parcours écrit « Nœud » depuis la leçon 03"
              % (i, sans_url.strip()[:90]))
        pb.append("¶%d ligature" % i); break

# ② ENTRER DANS UN SIGNE QUAND ON EST RÉTROGRADE, C'EST FRANCHIR SA BORNE HAUTE
retro = bool(re.search(r"(?i)rétrograd", "\n".join(T[:n_fin])))
for i, t in enumerate(T[:n_fin]):
    m = re.search(r"(?i)entr(?:e|ée|é|ent|er)\s+en\s+(%s)" % "|".join(SIGNES), t)
    if not m: continue
    degres = [int(d) for d in re.findall(r"(\d{1,3})\s*°\s*(?:de\s+longitude|\))", t)]
    if not degres: continue
    bas = SIGNES[m.group(1).capitalize()]; haut = (bas + 30) % 360 or 360
    attendu = haut if retro else bas
    if attendu not in degres and (attendu % 360) not in degres:
        print("② BORNE D'ENTRÉE INCOHÉRENTE AVEC LE SENS DE PARCOURS (¶%d) : « entrée en %s » avec %s, "
              "alors qu'un astre %s entre dans ce signe en franchissant %d° (le signe occupe %d°-%d°)"
              % (i, m.group(1), "°, ".join(str(d) for d in degres) + "°",
                 "rétrograde" if retro else "direct", attendu, bas, bas + 30))
        pb.append("¶%d borne %s" % (i, m.group(1)))

# ③ UNE CONSTANTE CHIFFRÉE QUI N'EST SUR AUCUNE PAGE LIÉE SE DÉCLARE COMME TELLE
pages = {}; codes = {}
def page(u):
    if u in pages: return pages[u]
    for _ in range(3):
        r = subprocess.run(["curl", "-s", "-L", "--max-time", "40", "-A", UA, "-w", "\n%{http_code}", u],
                           capture_output=True)
        s_ = r.stdout.decode("utf-8", "ignore"); c_ = s_.rsplit("\n", 1)[-1].strip()
        t = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", s_.rsplit("\n", 1)[0])
        pages[u] = re.sub(r"\s+", " ", html.unescape(re.sub(r"(?s)<[^>]+>", " ", t)))
        codes[u] = c_
        if c_ not in ("", "000"): break
    return pages[u]
AVEU = r"(?i)ne figure sur aucune|constante astronomique standard|non relevée|valeur de référence|reprise comme telle"
CIBLE = [(i, m.group(1)) for i, t in enumerate(T[:n_fin])
         for m in re.finditer(r"(\d{1,3},\d{1,3})\s*°", t)]
if CIBLE:
    TOUTES = " ".join(page(u) for u in URLS)
    for i, val in CIBLE:
        if re.search(AVEU, T[i]): continue
        if val in TOUTES or val.replace(",", ".") in TOUTES: continue
        print("③ CONSTANTE ABSENTE DES PAGES LIÉES (¶%d) : « %s° » ne figure sur aucune des %d pages, et le "
              "paragraphe ne dit pas que c'est une constante standard" % (i, val, len(URLS)))
        pb.append("¶%d constante %s" % (i, val))

CORPS = "\n".join(T[:n_fin])
PROSE = re.sub(r"[«»][^«»]{0,200}[«»]", " ", CORPS)
MOTS_FR = set(re.findall(r"[a-zà-öø-ÿ]{2,}", PROSE.lower()))
FR_SUP = set("""jumeaux temporels nodal karmique""".split())
GRAM_FR = set("""de des du la le les un une ce ces cet cette et ou au aux en dans sur par pour avec sans qui que
quoi dont son sa ses leur leurs plus moins non ne pas est sont ete etre avoir se il elle nous vous ils elles
mon ma mes ton ta tes notre votre tout toute tous toutes meme comme vers chez sous entre apres avant depuis
issues secondaires synthese syntheses""".split())
MINUSCULES = set(re.findall(r"\b([a-zà-öø-ÿ]{3,})\b", CORPS))

# ─── ④ CITATION COURTE (2 À 5 MOTS) SUR UNE PAGE DU PARAGRAPHE ──────────────
CIT = re.compile(r"«\s*([^«»]{3,90}?)\s*»")
def norm4(s):
    # la notice AbeBooks écrit « Samuel Weiser Inc. , 1984 » : un espace AVANT la virgule faisait
    # échouer la recherche d'une citation pourtant littérale (constaté le 02/10/2026 sur la n°08).
    return re.sub(r"\s+([,.;:)])", r"\1", re.sub(r"['’]", "'", s.lower()))
T4 = []
for i, t in enumerate(T[:n_fin]):
    if not LIENS[i]: continue
    for m in CIT.finditer(t):
        ph = m.group(1).strip().rstrip(".,;:…")
        mots = re.findall(r"[A-Za-zÀ-ÿ'’\-]{2,}", ph)
        if not (2 <= len(ph.split()) <= 5) or len(mots) < 2: continue
        bas = [w.lower().strip("'’-") for w in mots]
        if all(w in MOTS_FR | FR_SUP for w in bas): continue      # phrase entièrement dans la prose française
        if any(w in GRAM_FR for w in bas): continue               # un mot grammatical français = phrase française
        # ⚠️ une page qui n'a pas répondu, ou qui ne rend qu'une façade, ne prouve l'absence de RIEN :
        # ⑥ et ⑦ s'en occupent. Sans ce garde-fou, ④ refuse une citation DU MUR lui-même — constaté le
        # 02/10/2026 sur la n°08, qui cite « Human Verification | Open Library » en le déclarant.
        for u in LIENS[i]: page(u)
        lus4 = [u for u in LIENS[i] if codes.get(u) == "200" and len(page(u)) >= 500]
        if not lus4: continue
        T4.append((i, ph))
        if norm4(ph) in norm4(" ".join(page(u) for u in lus4)): continue
        print("④ CITATION COURTE HORS PAGE (¶%d) : « %s »" % (i, ph)); pb.append("¶%d cit. %s" % (i, ph[:26]))

# ─── CORRECTIF DU MOTIF ⑤, PORTÉ DU PROMPT `stoicisme` LE 09/10/2026 ────────
# Le motif ⑤ comparait « nom.lower() in page.lower() » : ni pliage des accents, ni exonymes, et
# ses mots de structure vivaient dans un STOP sensible à la casse ET aux accents. SIX FAUX
# POSITIFS mesurés le 09/10/2026 sur la leçon n°10 du 08/10 — le correctif existait depuis le
# 01/10/2026 dans le prompt `stoicisme` (sa(), FREN_/formes_(), STRUCT_) et n'avait jamais été
# porté : trois parcours portaient trois états du même code. Un test qui accuse à tort fait
# retirer du vrai.
def sa(s_):
    return "".join(c for c in unicodedata.normalize("NFD", s_) if unicodedata.category(c) != "Mn").lower()
# Exonymes : la leçon écrit le nom en français, la page le porte en anglais. CHAQUE ENTRÉE PORTE LE
# FAUX POSITIF QUI L'A JUSTIFIÉE, mesuré le 09/10/2026 sur la n°10 :
EXO_ = {
    "alger":  "algiers",   # ¶73 « découvert le 11/02/1927 à Alger » ; la fiche du MPC écrit « Algiers »
    "centre": "center",    # ¶10 « la fiche officielle du Centre des planètes mineures » ; la page écrit
                           #     « Minor Planet Center » — c'est aussi l'orthographe du domaine
}
def formes_(w):
    b = sa(w).strip("'’"); b = re.sub(r"^[a-z]['’]", "", b)      # « L'Observatoire » → « observatoire »
    return {b, EXO_.get(b, b)}
# Mots de STRUCTURE du document : des intitulés de rubrique, pas des noms prêtés à une source.
# ¶18 « Citation directe : "The Moon's center-to-center…" » — « Citation » était accusé d'être absent
# d'une page de la NASA qui n'a aucune raison de porter ce mot français.
STRUCT_ = {"citation", "citations", "encadre", "tableau", "figure", "annexe", "legende", "rubrique",
           "intitule", "paragraphe", "colonne", "ligne", "etape", "partie", "chapitre", "extrait",
           "traduction", "edition", "consigne", "format", "duree", "journal", "pont", "bilan",
           "synthese", "rappel", "corrige", "methode", "exemple", "remarque", "reserve", "verdict"}
# ─── ⑤ NOM PROPRE D'UN ¶ QUI DÉSIGNE SA SOURCE ─────────────────────────────
SRC = r"(?i)\bsource\s*:|\bétabli\b|page citée|\bd['’]après\b|\bselon\b"
STOP = set("""Chiron Chiron's Centaure Centaures Régime Régimes Nœud Nœuds Leçon Objectif Source Sources
Ressources Pratique Exercice Note Notes Thème Signe Maison Terre Soleil Lune Zodiaque Verseau Bélier Taureau
Gémeaux Cancer Lion Vierge Balance Scorpion Sagittaire Capricorne Poissons Continuité Résultat Mode Dans Les
Elle Cette Avant Après Depuis Chez Pour Avec Sans Mais Donc Distant HTTP ISBN Attribution Système
Astronomie Astrologie Observatoire Statut Fait Lecture Retour Classification Présence Double Zone"""
           .split())
# STOP vivait en casse et accents bruts : on le plie une fois pour toutes, et STRUCT_ le complète.
# (⚠️ cette ligne doit rester APRÈS la définition de STOP : placée avant, elle lève un NameError —
#  constaté le 09/10/2026 en portant le correctif, sur les dix leçons du parcours d'un coup.)
STOP_ = {sa(w) for w in STOP} | STRUCT_
T5 = []
ABSENCE = (r"(?i)z[ée]ro occurrence|0 occurrence|ne porte ni|n['’]y figure|ne figure (?:pas|sur aucune)"
           r"|compt(?:e|ent) z[ée]ro|absent|impossible|n['’]a pas été consult|non consult|ne mentionne"
           r"|aucune mention|sans source consultée|lecture courante du corpus|non lu"
           r"|pas une citation|pas une attribution|ne provient pas|aucune citation")
for i, t in enumerate(T[:n_fin]):
    if not LIENS[i] or not re.search(SRC, t): continue
    if re.search(ABSENCE, t): continue      # le ¶ DÉCLARE qu'un mot manque : ne pas l'accuser de le dire
    # une page qui n'a pas répondu, ou qui ne rend qu'une façade, ne prouve l'absence de RIEN :
    # c'est ⑥ et ⑦ qui s'en occupent. Sans ce garde-fou, ⑤ accuse tous les noms d'un ¶ dès qu'un
    # lien est injoignable — constaté sur la n°07 le 01/10/2026 (six noms accusés sur une page à code 000).
    for u in LIENS[i]: page(u)
    lus = [u for u in LIENS[i] if codes.get(u) == "200" and len(page(u)) >= 500]
    if not lus: continue
    pg = " ".join(page(u) for u in lus).lower()
    dom = " ".join(lus).lower()
    for m in re.finditer(r"\b([A-ZÀ-Þ][a-zà-öø-ÿ]{2,})\b", TH[i]):
        nom = m.group(1)
        # MINUSCULES vient du texte NON mis en minuscules : un mot qui apparaît ailleurs en bas de casse
        # est un nom commun français capitalisé en tête de phrase. ⚠️ NE PAS utiliser MOTS_FR ici : il est
        # construit sur la prose .lower(), il contient donc TOUS les noms propres et exempterait tout
        # (constaté le 01/10/2026 : ⑤ est passé à 0 nom testé sur les neuf leçons).
        if sa(nom) in STOP_ or nom.lower() in MINUSCULES: continue
        if any(f in sa(dom) for f in formes_(nom)): continue             # le nom de la source elle-même
        # ⚠️ le ¶ DÉCLARE lui-même le décompte : « Schulman=0, Spiller=0, Greene=0 » (n°08 du 24/09/2026,
        # la leçon la mieux sourcée du parcours — ⑤ l'accusait de dire que ces noms manquent)
        if re.search(r"\b%s\s*=\s*0\b" % re.escape(nom), t): continue
        # ⚠️ le nom est SUIVI de son adresse : « Tristan Balguerie (astrologie-autrement.com/…) » (n°07)
        if re.search(r"\b%s\b.{0,60}?[\w.-]+\.(?:com|org|net|fr|gov|edu|uk)/" % re.escape(nom), t): continue
        T5.append((i, nom))
        if any(f in sa(pg) for f in formes_(nom)): continue
        print("⑤ NOM PROPRE HORS SOURCE (¶%d) : « %s »" % (i, nom)); pb.append("¶%d nom %s" % (i, nom))

# ─── ⑥ UNE FAÇADE QUI RÉPOND 200 NE PORTE RIEN ─────────────────────────────
# ─── ⑦ UNE PAGE QUI NE RÉPOND PAS DU TOUT SE DÉCLARE NON LUE ───────────────
def etiq(u):
    # ⚠️ NE PAS tronquer une adresse par le DÉBUT : « …/OL8111269M » et « …/OL8111269M.json » donnaient
    # tous deux « openlibrary.org/books/OL8111 », et j'ai mal diagnostiqué le refus (02/10/2026).
    s = u.split("//")[-1]
    return s if len(s) <= 34 else "…" + s[-33:]
DECL = (r"(?i)non lue|rend 0 caract|0 caractère|aucun caract|page vide|formulaire javascript|illisible"
        r"|non lisible|code 000|sans réponse|n['’](?:a|ont) pas répondu|erreur ssl|vérifié à la main"
        r"|lu au navigateur|certificat désactivé|ne répond(?:ent)? pas|mur de vérification")   # ⚠️ une DÉCLARATION HONNÊTE prend bien des formes :
# la n°07 écrivait « la page renvoie une erreur SSL en contrôle automatique, mais le contenu a été lu et
# vérifié à la main » — déclaration exacte, que la première version de ⑦ refusait quand même (01/10/2026).
# Un test qui n'accepte qu'une seule tournure de l'aveu punit celui qui avoue autrement.
T6 = []
for u in URLS:
    n = len(page(u)); c = codes.get(u, ""); T6.append((u, c, n))
    porteurs = [i for i in range(n_fin) if u in LIENS[i] and re.search(r"\d|«", T[i])]
    if not porteurs: continue
    if c == "200" and n < 500:
        print("⑥ FAÇADE QUI RÉPOND 200 (%s : %d caractères utiles) : rien ne peut lui être attribué — ¶%s"
              % (u, n, ", ¶".join(map(str, porteurs))))
        pb.append("façade %s" % etiq(u))
    elif c in ("", "000") and not any(u in LIENS[i] and re.search(DECL, T[i]) for i in range(n_fin)):
        print("⑦ PAGE SANS RÉPONSE, NON DÉCLARÉE (%s : code %s après 3 essais) : ¶%s"
              % (u, c or "aucun", ", ¶".join(map(str, porteurs))))
        pb.append("page sans réponse %s" % etiq(u))

print(("REFUSÉ — %d motif(s) : %s" % (len(pb), " | ".join(pb))) if pb else "OK — aucun des sept motifs")
sys.exit(1 if pb else 0)