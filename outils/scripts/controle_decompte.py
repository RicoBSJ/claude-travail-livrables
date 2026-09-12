#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""controle_decompte.py — le décompte de sources annoncé par une veille est-il celui de sa liste ?

Usage : /usr/bin/python3 outils/scripts/controle_decompte.py <chemin du .docx>
        DEBUG=1 devant la commande imprime, sur stderr, la rubrique retenue, chaque entrée comptée et sa ligne.
Sort en 0 si chaque nombre annoncé correspond à la liste, en 1 si l'un ne correspond pas,
en 2 s'il n'y a rien à comparer (aucun décompte annoncé, ou liste non reconnue) — un 2
n'est PAS un succès : la note se relit à la main.

Réécrit le 12/09/2026 après la passe sur les 85 veilles du dépôt : la première version
(règle 3 du prompt ai-act-veille, écrite le matin même) ne lisait qu'une forme de décompte
et une forme de liste ; sur le corpus, elle aurait laissé passer 11 des 12 décomptes faux
et crié sur 4 notes justes. Les huit défauts corrigés (JOBS.md, 12/09/2026) :
  ① un code HTTP devant un symbole (« 403 ⛔ ») était lu comme un compte → nombres < 100 ;
  ② un nombre pris sur la ligne précédente (« Config 5 ⏎ ⛔ ») → même ligne obligatoire ;
  ③ « 5/9 ✅ » : c'est 9 qui était lu — et 9 = 9 ✅ par hasard acquittait imac 06/09 → X et Y lus ;
  ④ un sous-titre commençant par un symbole (« ✅ Sources exploitées : ») comptait pour une source ;
  ⑤ un décompte placé APRÈS la liste n'était pas lu (ai-act 04/09, cité comme validation) ;
  ⑥ aucun nombre annoncé → « COHÉRENT » (11 des 13 exit 0 étaient inertes) → exit 2 ;
  ⑦ les formes sans symbole (« Sources : 5/7 », « 4/9 sources exploitées ») n'étaient pas lues :
     9 des 12 vraies erreurs étaient dans cet angle mort ;
  ⑧ la reconnaissance exigeait le symbole seul sur sa ligne, alors que « ✅ texte » se compte.

Ce que le test LIT :
  la liste — les entrées d'une rubrique « Sources … » : lignes ouvrant sur ✅ / ⚠️ / ⛔
  (« ⛔/✅ » = accès de repli, compté comme ouvert), lignes portant le symbole en fin
  (tableaux « ✅ Accessible », « … ⛔ 403 »), lignes « Consultée… » sans symbole (comptées
  à part), et, sous un sous-titre qui porte le symbole (« ✅ Sources directement lues »),
  les lignes nues qui suivent ;
  les nombres — « X/Y » suivi de ✅ ou d'un mot de source ; « N ✅ », « N sources ✅ »,
  « N exploitées (✅) », « N bloquée anti-robot (⚠️) » sur la même ligne ; « N sources
  tentées / consultées / exploitées / accessibles / listées » ; « sur N sources » ;
  « N consultées sans nouveauté ». Partout dans la note, journal des corrections exclu.
Ce que le test ACCEPTE : X (ouvertes) = ✅, ou ✅ + repli, ou ✅ + repli + consultées sans
  symbole ; Y (tentées) = total des entrées ; un nombre devant ⛔ ou ⚠️ = ce symbole, ou
  ⛔+⚠️ quand la note écrit « ⛔/⚠️ », ou l'un de ceux-là + consultées sans symbole.
  Chaque acquittement exige une somme EXACTE : rien n'est arrondi, rien n'est « proche ».
Un lien posé au milieu d'une ligne la coupe en trois à l'extraction (« … (», « domaine », «) — … ») :
  le test recolle ces morceaux avant de lire — constaté le 12/09/2026 après l'ajout de douze liens.
Ce que le test NE LIT PAS : une source qui en cache deux (« A & B — non consultées » compte
  1 + le nombre de « & »), un décompte par domaine quand la liste est par page — lis la
  ligne « liste » qu'il imprime avant de croire son verdict.
"""
import sys, re, os, subprocess
DEBUG = bool(os.environ.get("DEBUG"))

DOCX = sys.argv[1]
EXTRACT = "/Users/utilisateur/kDrive/Claude_Travail/outils/scripts/extract_docx.py"
t = subprocess.run(["/usr/bin/python3", EXTRACT, DOCX], capture_output=True, text=True).stdout
if "=== TEXTE COMPLET" not in t:
    sys.exit("EXTRACTION IMPOSSIBLE (fichier introuvable ou illisible) : " + DOCX)
t = t[t.index("=== TEXTE COMPLET"):]
t = t.split("Journal des corrections")[0]        # le journal cite volontairement les anciens comptes
t = t.replace("\ufe0f", "")   # ⚠ = U+26A0 + sélecteur U+FE0F : sans ce retrait, une classe [⚠] coupe le symbole en deux
lignes = []
for l in t.split("\n"):
    # un lien posé au milieu d'une phrase la coupe en trois lignes à l'extraction : on recolle
    if lignes and (lignes[-1].rstrip().endswith("(") or l.lstrip().startswith(")")):
        lignes[-1] = lignes[-1].rstrip() + l.lstrip()
    else:
        lignes.append(l)

SYM = "✅⚠⛔"
R_START = re.compile(r"^[•\-–·\d.)\s]*([✅⚠⛔])(?:\s*/\s*([✅⚠⛔]))?\s*(.*)$")
R_END = re.compile(r"\S.*\s([✅⚠⛔])\s*[^✅⚠⛔\n]{0,40}$")
R_CONS = re.compile(r"^\s*(?:◻️|Consult[ée]e?s?\b|Non consult)")
R_HEAD = re.compile(r"^[^\w]{0,6}Sources?\b[^\n]{0,80}$")
R_END_SEC = re.compile(r"^\s*(?:\d+\.\s*)?(?:🔜|🔵|─{5,}|(?:Produit|Généré|Document|Note|Compte-rendu|CR|Veille)\b.{0,40}(?:généré|produit|automatiquement)|.*[Ss]urveiller)")
R_META = re.compile(r"(?i)^(?:Affirmations|Légende|Legende|Décompte|Decompte|Bilan|Total|NB\b|Note\b)")
R_NUM_SYM = re.compile(r"(?<![\d/.])(?<![Ss]ource )(\d{1,2})[^\S\n]*(?:sources?[^\S\n]*)?(?:[a-zéèêàçô'’ -]{0,30}?\()?[^\S\n]*([✅⚠⛔])(?:\s*/\s*([✅⚠⛔]))?")

def norm(s):
    return s.replace(" ", " ").strip()

# ── 1. la liste
R_VOCAB = re.compile(r"(?i)^(?:\(|non\b|accessible|consult|dispo|publi|termin|clôtur|cloture|lanc|réuni|en\b|mise|ok\b|nouveau|"
                     r"\d{3}\b|timeout|js\b|rendu|via\b|bto|source\s*\d+\s*—?\s*$|erreur|http|lecture|page\b|atteinte|"
                     r"contenu|données|prix|jamais|aucun|bloqu|inaccessible|exploit)")
R_DOM = re.compile(r"\w\.(?:fr|eu|org|com|int|gouv|net|co|io|uk)\b")
R_URL = re.compile(r"^https?://")

R_XY_NU = re.compile(r"(?<![\d/,.])(\d{1,2})\s*/\s*(\d{1,2})(?![\d/])")
R_XY_MOT = re.compile(r"(?i)✅|sources?\b|accessibles|exploit|consult|\btent[ée]|directes|WebSearch|fallback|extraits")
R_REPLI = re.compile(r"(?i)(?:fallback|websearch|repli)[^\n]{0,25}(?:✅|OK\b)|✅[^\n]{0,15}(?:fallback|websearch)")
def xy(n):
    """les « X/Y » d'une ligne qui parlent de sources : un mot-clé dans les 30 caractères avant ou après"""
    for m in R_XY_NU.finditer(n):
        if R_XY_MOT.search(n[m.end():m.end() + 30]) or R_XY_MOT.search(n[max(0, m.start() - 30):m.start()]):
            yield m
R_SUB_VOCAB = re.compile(r"(?i)sources?|consult|inaccessible|exploit|accessible|bloqu|repli|fallback")

def est_annonce(l):
    return bool(R_NUM_SYM.search(l)) or any(True for _ in xy(l))

def classe(n):
    """-> (type, symbole, texte) : SUB sous-titre · STAT statut seul · ENTRY symbole + nom ·
       CONS « consultée… » · CONT continuation · NAME ligne nue · SKIP"""
    if not n or n in ("Source", "URL", "Statut", "Remarque", "St.", "/", "Sources"):
        return ("SKIP", None, n)
    if est_annonce(n) and not R_START.match(n):
        return ("SKIP", None, n)
    if R_META.match(n):
        return ("SKIP", None, n)
    m = R_START.match(n)
    if m:
        sym = "repli" if m.group(2) else m.group(1)
        reste = m.group(3).strip()
        if R_META.match(reste):
            return ("SKIP", None, n)
        if re.match(r"/?\s*(?:Sources?|Exploit|Inaccessibles?|Non accessible|Note\b)", reste) or reste.endswith(":"):
            return ("SUB", sym, n)
        if est_annonce(reste):
            return ("SKIP", None, n)
        if reste == "" or (not R_DOM.search(reste) and (R_VOCAB.match(reste) or (len(reste) <= 30 and not re.search(r"[A-Z]", reste[1:])))):
            return ("STAT", sym, n)
        return ("ENTRY", sym, n)
    if n.endswith(":"):
        sym = re.search(r"[✅⚠⛔]", n)
        return ("SUB", sym.group() if sym else None, n)
    m = R_END.match(n)
    if m and not re.match(r"[).]", n[m.end(1):m.end(1) + 1]) and n[:m.start(1)].count("(") <= n[:m.start(1)].count(")"):
        # (un symbole entre parenthèses est de la prose — « statut ⛔ retiré le 12/09 » — pas un statut)
        # symbole en fin de ligne : statut d'un nom porté par la ligne (ENTRY) ou par la ligne d'avant (STAT)
        avant = n[:m.start(1)].strip()
        if re.match(r"^[—\-–/]", avant) or not re.search(r"[A-Za-zÀ-ÿ]{3}", avant):
            return ("STAT", m.group(1), n)
        return ("ENTRY", m.group(1), n)
    if R_CONS.match(n):
        return ("CONS", None, n)
    if R_URL.match(n) or re.match(r"^[—\-–/]", n) or len(n) < 6:
        return ("CONT", None, n)
    return ("NAME", None, n)

R_CANON = re.compile(r"^(?:📚|📋)?\s*Sources\s*(?:du jour|consultées|documentaires|—|$)")
candidats = []
for k, l in enumerate(lignes):
    n = norm(l)
    m = R_START.match(n)
    if m and re.match(r"\s*/?\s*Sources?\b[^:]{0,90}:?$", m.group(3)) and not R_DOM.search(m.group(3)):
        candidats.append((k, True, 2)); continue         # « ✅ Sources directement lues » ouvre la liste
    tete = R_HEAD.match(n) and (not est_annonce(n) or n.endswith(":")) \
        and not re.match(r"^[^\w]{0,6}Sources?\s*(?:\w+\s*)?:\s*\S", n) and not n.startswith("→")   # « Source : AMF, … » est une ligne du corps
    if tete:
        types = [classe(norm(x)) for x in lignes[k + 1:k + 13]]
        score = sum(1 for t in types if t[0] in ("STAT", "ENTRY") or (t[0] == "SUB" and t[1]))
        if score or any(t[0] == "CONS" for t in types[:8]):
            candidats.append((k, bool(R_CANON.match(n)), score))
# un titre canonique (« Sources du jour », « 📚 Sources »…) suivi d'au moins deux statuts l'emporte ;
# sinon le candidat le mieux fourni (le premier à égalité)
start = next((k for k, canon, sc in candidats if canon and sc >= 2), None)
if start is None and candidats:
    start = max(candidats, key=lambda c: c[2])[0]

c = {s: 0 for s in SYM}
c["repli"] = 0
c["autres"] = 0
if start is not None:
    if DEBUG: print("   rubrique : %s" % norm(lignes[start])[:90], file=sys.stderr)
    toks = []
    fin_sur_titre = False
    tiret_ouvre = False
    m0 = R_START.match(norm(lignes[start]))
    if m0:
        toks.append(["SUB", "repli" if m0.group(2) else m0.group(1), norm(lignes[start]), False])   # le titre porte lui-même le symbole du groupe
    for l in lignes[start + 1:]:
        n = norm(l)
        if R_END_SEC.match(n):
            if DEBUG: print("   fin     : %s" % n[:90], file=sys.stderr)
            break
        typ, sym, txt = classe(n)
        if typ == "SKIP":
            continue
        if typ == "SUB" and sym is None and not R_SUB_VOCAB.search(n):
            if DEBUG: print("   fin     : %s" % n[:90], file=sys.stderr)
            fin_sur_titre = True
            break                   # un sous-titre sans symbole ni vocabulaire de source : on a quitté la liste
        if typ == "CONT" and re.match(r"^[—\-–]", n) and toks and (toks[-1][0] == "SUB" or (tiret_ouvre and toks[-1][0] == "NAME" and toks[-1][2][0] in "—-–")):
            typ = "NAME"            # un tiret juste sous un sous-titre ouvre une entrée, et les tirets suivants du même groupe aussi
        if typ == "SUB":
            tiret_ouvre = False
        elif typ == "NAME" and toks and toks[-1][0] == "SUB" and n[0] in "—-–":
            tiret_ouvre = True
        if typ == "CONS":
            # « Consultée… : plare.fr » nomme sa source ; « Consultée, sans élément » + nom dessous est un statut ;
            # « Consultée — données hors fenêtre » sous un nom est une remarque
            if R_DOM.search(n) or re.search(r" — [A-ZÀ-Ý]", n):
                typ, sym = "ENTRY", "autres"
            else:
                typ, sym = "STAT", "autres"
        toks.append([typ, sym, txt, False])       # [type, symbole, texte, consommé]
    if fin_sur_titre and toks and toks[-1][0] == "STAT" and R_START.match(toks[-1][2]) and not R_START.match(toks[-1][2]).group(3).strip():
        toks.pop()                                # un symbole NU juste avant le titre qui ferme la liste est l'emoji de ce titre
    # orientation : le statut précède-t-il le nom (« ✅ » puis « CNIL — … ») ou le suit-il (tableau nom · URL · « ✅ Accessible ») ?
    #   calculée PAR GROUPE (sous-titre) : un groupe « ✅ Exploitées : » fait de noms nus ne dit rien de l'ordre du groupe suivant
    def orientation(deb, fin):
        i_stat = next((i for i in range(deb, fin) if toks[i][0] == "STAT" and toks[i][1] != "autres"), None)
        i_name = next((i for i in range(deb, fin) if toks[i][0] == "NAME"), None)
        return i_stat is not None and i_name is not None and i_name < i_stat
    bornes = [i for i, tk in enumerate(toks) if tk[0] == "SUB"] + [len(toks)]
    apres_de = {}
    deb = 0
    for fin in bornes + ([len(toks)] if not bornes or bornes[-1] != len(toks) else []):
        ap = orientation(deb, fin)
        for i in range(deb, fin):
            apres_de[i] = ap
            if ap and toks[i][0] == "STAT" and toks[i][1] == "autres":
                toks[i][0] = "SKIP"     # dans un tableau, « Consultée — … » est la remarque d'une ligne, pas un statut
        deb = fin
    # appariement nom ↔ statut, par sous-titre
    groupe = None
    grp = {}     # sous-titre -> {"stat": bool, "entry": bool}
    for i, tk in enumerate(toks):
        if tk[0] == "SUB":
            groupe = i; grp[groupe] = {"stat": False, "entry": False}; continue
        if tk[0] == "STAT": grp.setdefault(groupe, {"stat": False, "entry": False})["stat"] = True
        if tk[0] == "ENTRY": grp.setdefault(groupe, {"stat": False, "entry": False})["entry"] = True
    groupe = None
    for i, tk in enumerate(toks):
        typ, sym = tk[0], tk[1]
        if typ == "SUB":
            groupe = i; continue
        if typ == "ENTRY":
            n_src = 1 + tk[2].split(" — ")[0].count(" & ")
            c[sym] += n_src; tk[3] = True
            if DEBUG: print("   %-5s %s  %s" % (sym, "·", tk[2][:80]), file=sys.stderr)
            continue
        if typ == "NAME":
            # statut juste avant (non consommé) ? sinon juste après (une continuation peut s'intercaler) ?
            st = None
            j = i + 1
            while j < len(toks) and toks[j][0] == "CONT": j += 1
            suivant = j if j < len(toks) and toks[j][0] == "STAT" and not toks[j][3] else None
            precedent = i - 1 if i >= 1 and toks[i - 1][0] == "STAT" and not toks[i - 1][3] else None
            apres = apres_de.get(i, False)
            st = (suivant if suivant is not None else precedent) if apres else (precedent if precedent is not None else suivant)
            g = grp.get(groupe, {"stat": False, "entry": False})
            if st is not None:
                toks[st][3] = True; tk[3] = True
                s_st = toks[st][1]
                if s_st == "⛔" and R_REPLI.search(tk[2]):
                    s_st = "repli"        # « ⛔ » + « … (403 — WebSearch fallback ✅) » : la source a été lue par un autre chemin
                c[s_st] += 1 + tk[2].split(" — ")[0].count(" & ")
                if DEBUG: print("   %-5s %s  %s" % (s_st, "↔", tk[2][:80]), file=sys.stderr)
            elif g["stat"]:
                if DEBUG: print("   remarque   %s" % tk[2][:80], file=sys.stderr)   # nom sans statut dans un groupe à statuts : remarque
            else:
                s_g = toks[groupe][1] if groupe is not None and toks[groupe][1] else "autres"
                c[s_g] += 1 + tk[2].split(" — ")[0].count(" & ")
                if DEBUG: print("   %-5s %s  %s" % (s_g, "nue", tk[2][:80]), file=sys.stderr)
    seuls = [tk for tk in toks if tk[0] == "STAT" and tk[1] != "autres" and not tk[3]]
    if seuls:
        # un statut sans nom n'est pas compté : on le signale, le lecteur tranche
        print("statuts sans nom (non comptés) : %d — %s" % (len(seuls), " · ".join(tk[2][:40] for tk in seuls[:4])))
total = sum(c.values())
print("liste : ✅ %d · ⚠ %d · ⛔ %d · repli(⛔/✅) %d · consultées sans symbole %d · total %d"
      % (c["✅"], c["⚠"], c["⛔"], c["repli"], c["autres"], total))
if total == 0:
    print("LISTE NON RECONNUE : aucune rubrique « Sources » suivie d'entrées ✅ / ⚠ / ⛔ — relis la note à la main", file=sys.stderr)
    sys.exit(2)

# ── 2. les nombres annoncés, partout dans la note
ouvertes = {c["✅"], c["✅"] + c["repli"], c["✅"] + c["repli"] + c["autres"]}
def ok_sym(n, s, double):
    acc = {c[s], c[s] + c["autres"]}
    if s == "✅":
        acc |= ouvertes
    if double or s in "⚠⛔":
        acc |= {c["⚠"] + c["⛔"], c["⚠"] + c["⛔"] + c["autres"]} if double else set()
    return n in acc
annonces, pb = [], []
for l in lignes:
    n = norm(l)
    if est_annonce(n) and (R_START.match(n) and not re.search(r"\d", R_START.match(n).group(3) or "")):
        continue
    for m in xy(n):
        x, y = int(m.group(1)), int(m.group(2))
        if y < x: continue
        suite = n[m.end():m.end() + 30]
        avant = n[max(0, m.start() - 30):m.start()]
        if re.match(r"\s*(?:WebSearch|fallback|extraits)", suite) or re.search(r"(?i)(?:WebSearch|fallback|extraits)\s*:?\s*$", avant):
            annonces.append("%d/%d (repli)" % (x, y))
            if x not in {c["⛔"] + c["⚠"], c["repli"] + c["⛔"] + c["⚠"]}: pb.append("%d en repli annoncées, liste ⛔+⚠ %d" % (x, c["⛔"] + c["⚠"]))
        else:
            annonces.append("%d/%d" % (x, y))
            if x not in ouvertes: pb.append("%d ouvertes annoncées, liste ✅ %d" % (x, c["✅"]))
        if y != total: pb.append("%d au total annoncées, liste %d" % (y, total))
    for m in R_NUM_SYM.finditer(n):
        n1, s, s2 = int(m.group(1)), m.group(2), m.group(3)
        if re.search(r"(?:HTTP|erreur|code)\s*$", n[:m.start()]): continue
        annonces.append("%d %s%s" % (n1, s, "/" + s2 if s2 else ""))
        if not ok_sym(n1, s, bool(s2)): pb.append("%d annoncé pour %s, liste %d" % (n1, s + ("/" + s2 if s2 else ""), c[s] if not s2 else c["⚠"] + c["⛔"]))
    for m in re.finditer(r"(?<![\d/.])(\d{1,2})\s+(?:sources?\s+)?(?:documentaires\s+|officielles\s+|institutionnelles\s+)?(tent[ée]es?|consult[ée]es?|exploit[ée]es?|accessibles?|list[ée]es?|ouvertes?)\b", n):
        n1, mot = int(m.group(1)), m.group(2)
        mot = {"tent": "tentées", "cons": "consultées", "expl": "exploitées", "acce": "accessibles", "list": "listées", "ouve": "ouvertes"}[mot[:4].lower()]
        if re.search(r"[✅⚠⛔]", n[m.end():m.end() + 3]): continue      # déjà lu par la forme symbole
        if "sans" in n[m.end():m.end() + 12]:
            annonces.append("%d consultées sans nouveauté" % n1)
            if n1 != c["autres"]: pb.append("%d consultées sans nouveauté annoncées, liste %d" % (n1, c["autres"]))
            continue
        annonces.append("%d %s" % (n1, mot))
        if mot in ("tentées", "listées"):
            if n1 != total: pb.append("%d %s annoncées, liste %d" % (n1, mot, total))
        elif mot == "exploitées":
            if n1 not in ouvertes: pb.append("%d exploitées annoncées, liste ✅ %d" % (n1, c["✅"]))
        else:
            if n1 not in ouvertes | {total}: pb.append("%d %s annoncées, liste ✅ %d (total %d)" % (n1, mot, c["✅"], total))
    for m in re.finditer(r"\bsur\s+(\d{1,2})\s+sources", n):
        n1 = int(m.group(1)); annonces.append("sur %d" % n1)
        if n1 != total: pb.append("sur %d annoncé, liste %d" % (n1, total))
print("annoncé :", " ; ".join(dict.fromkeys(annonces)) if annonces else "(rien)")
if not annonces:
    print("AUCUN DÉCOMPTE ANNONCÉ — rien à comparer ; si la note en porte un, le test ne le lit pas", file=sys.stderr)
    sys.exit(2)
pb = list(dict.fromkeys(pb))
print("COHÉRENT" if not pb else "INCOHÉRENT — " + " ; ".join(pb))
sys.exit(1 if pb else 0)
