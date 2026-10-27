#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""controle_psychopathologie.py — étape 5 bis du job psychopathologie-lecon.

SORTI DU PROMPT LE 08/10/2026. Le script était inliné (5 520 octets sur 71 057, le plus
gros prompt du dépôt), donc réémis à chaque tour sans jamais changer. Il suit désormais
la règle que `CLAUDE.md` fixe pour les contrôles communs — « appelés par les prompts,
jamais copiés ». Comportement inchangé à la ligne près : validé dans les deux sens le
08/10/2026 contre la version inlinée, verdicts identiques sur les leçons n°17 et n°19.

Usage :  python3 outils/scripts/controle_psychopathologie.py <chemin du .docx>
Sortie : 0 si aucun des quatre motifs, 1 si la leçon est refusée.

REFUSE SI — (1) une page has-sante.fr liée dans les ressources lie elle-même un PDF
has-sante.fr absent des ressources (règle B3 bis) ; (2) une fraction (« 1/3 », « un
tiers », « la moitié », « un sur cinq ») figure dans un ¶ qui nomme une source sans
donner d'effectif ni de pourcentage (règle A2 bis) ; (3) une ligne du tableau « Corrigé —
Challenge » contient un effet indésirable que la théorie ne décrit que sous une autre
classe (règle C2 ter) ; (4) une DCI d'un tableau de théorie est absente des pages ANSM
listées (règle A2 ter).

VALIDATION D'ORIGINE (21/09/2026, dans les deux sens) : n°17 telle que livrée → refusée
(PDF du Flash non lié ; « 1/3 » sans effectif en théorie et en pont pro ; « agitation »
ligne Antidépresseur et « rigidité » ligne Thymorégulateur ; « Lévopromazine ») ;
corrigée → OK. n°14 → OK. n°13, 15 et 16 → refusées pour le seul contrôle 1 (notice HAS
liée, PDF non lié) : même pratique, laissée telle quelle.
"""
import sys
if len(sys.argv) < 2:
    sys.exit("usage : controle_psychopathologie.py <chemin du .docx>")

import zipfile, re, sys, html, subprocess, unicodedata
try:
    import ca_bundle
    CA = ca_bundle.args_curl()      # ⚠️ 26/10/2026, voir ca/README.md : chaîne complète, rien n'est désactivé
except Exception:
    CA = []
p = sys.argv[1]
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
z = zipfile.ZipFile(p); x = z.read("word/document.xml").decode("utf-8")
rels = z.read("word/_rels/document.xml.rels").decode("utf-8")
urls = sorted({html.unescape(t) for t in re.findall(r'Target="(https?://[^"]+)"', rels)})
ps = re.findall(r"<w:p(?:\s[^>]*)?>.*?</w:p>", x, re.S)
T = [re.sub(r"\[Corrigé le \d\d/\d\d/\d{4} :.*?\]", "", html.unescape("".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", q))), flags=re.S) for q in ps]
fin = [i for i, t in enumerate(T) if "Journal des corrections" in t]
if fin: T = T[:fin[0]]
pb = []
# 1. UNE PAGE HAS DE PRÉSENTATION N'EST PAS LE DOCUMENT — si la page jcms lie un PDF has-sante.fr, ce PDF est dans les ressources
# 🔴 BORNÉ AUX PAGES DE RBPP LE 26/10/2026. Le motif a mordu sur `p_3590541/la-has-adopte-son-nouveau-programme-sante-mentale-et-psychiatrie-2025-2030`, qui est
# un COMMUNIQUÉ DE PRESSE : il exigeait des ressources de la leçon l'annexe thématique d'une
# page d'actualité. La lettre de la règle B3 bis était respectée, son esprit visait la page de
# présentation d'une RECOMMANDATION. La largeur n'est devenue visible qu'au portage du
# faisceau, le même jour : avant, une page vide rendait le motif inerte et il ne s'exerçait
# jamais.
# LE DISCRIMINANT EST STRUCTUREL, PAS LEXICAL, et c'est mesuré sur les 17 pages jcms du
# corpus : chaque page HAS déclare son propre type dans UNE seule étiquette, celle de sa zone
# sub-title — `Recommandation de bonne pratique` (9 pages), `Communiqué de presse` (1),
# `Flash sécurité patient` (1), `Article HAS` (2), aucune pour les 4 portails thématiques.
# ⚠️ UN SIMPLE `"Recommandation de bonne pratique" in page` NE MARCHE PAS : la chaîne
# apparaît aussi dans la colonne « Voir aussi » de pages qui n'en sont pas une (mesuré sur
# p_3953998 et p_3741239, 2 occurrences chacune). C'est l'ÉTIQUETTE qui tranche, pas la page.
# ⚠️ ET L'EXEMPTION EST DITE, JAMAIS SILENCIEUSE : si le gabarit de la HAS changeait de
# classe, toutes les pages deviendraient exemptes et le motif redeviendrait inerte — le défaut
# même corrigé le 26/10 au matin. La ligne imprimée rend ce cas visible dans le log.
# 🆕 27/10/2026 — LE DÉCOMPTE DES EXEMPTIONS, ET L'ALERTE QUAND ELLES PASSENT À 100 %.
# POURQUOI : le bornage du 26/10 ouvre un angle mort symétrique de celui qu'il ferme. Si le
# gabarit de la HAS renommait `titleLabelCaps` ou sa zone `sub-title`, AUCUNE page ne rendrait
# plus d'étiquette, toutes seraient exemptées, et le motif (1) redeviendrait INERTE — le défaut
# même corrigé le 26/10 au matin, par l'autre bout.
# ⛔ ET « 100 % D'EXEMPTIONS » SEUL NE PEUT PAS ÊTRE L'ALERTE : c'est un état LÉGITIME du
# corpus. Mesuré sur les 20 leçons et leurs 11 visites de page jcms à PDF : 8 documents ont au
# moins une page à PDF, et la leçon 17 n'en cite qu'UNE, le Flash sécurité patient p_3381939,
# donc 1 exemptée sur 1 — 100 %. Une alerte sur le seul taux accuserait un document conforme.
# 🟢 LE DISCRIMINANT MESURÉ EST L'ÉTIQUETTE LUE : sur ces 11 visites, une étiquette a été lue
# 11 fois sur 11 (9 « Recommandation de bonne pratique », 1 « Communiqué de presse », 1 « Flash
# sécurité patient »). Un renommage de gabarit les fait TOUTES tomber à zéro. L'alerte est donc
# « 100 % d'exemptions ET aucune étiquette lue » : zéro occurrence sur le corpus, donc zéro
# fausse alerte mesurée.
# ⚠️ CE QUE LA BORNE COÛTE, ET C'EST DIT : un renommage PARTIEL — une seule page devenue
# illisible — ne déclenche pas l'alerte, il n'est visible que dans les nombres du décompte.
# ⚠️ LES 4 PORTAILS THÉMATIQUES, SANS AUCUNE ÉTIQUETTE, NE SONT PAS CONCERNÉS : ils n'ont aucun
# PDF, donc le motif les écarte avant d'en arriver là. Le décompte ne compte que les pages à PDF.
# ⚠️ NON BLOQUANT. La cause serait le gabarit d'un TIERS, pas le document : un refus couperait la
# publication d'une leçon conforme. Règle du 14/10 — un vrai manqué coûte une relecture humaine,
# un faux refus coûte un livrable non publié.
def bilan_etiquettes(n_pdf, n_exempt, n_etiq):
    """Les lignes a imprimer : decompte des exemptions, puis l'alerte d'inertie. [] si rien."""
    if not n_pdf:
        return []
    L = ["ÉTIQUETTES HAS : %d page(s) jcms à PDF · %d exemptée(s) · %d étiquette(s) lue(s)"
         % (n_pdf, n_exempt, n_etiq)]
    if n_exempt == n_pdf:
        if n_etiq:
            L.append("   100 %% d'exemptions, mais %d étiquette(s) LUE(S) : le gabarit de la HAS "
                     "répond, aucune alerte (cas mesuré — la leçon 17 ne cite qu'un flash)" % n_etiq)
        else:
            L.append("🔴 ALERTE ÉTIQUETTE HAS — 100 % D'EXEMPTIONS ET AUCUNE ÉTIQUETTE LUE : le "
                     "motif (1) est INERTE, plus aucun PDF n'est confronté aux ressources. Cause "
                     "probable : `titleLabelCaps` ou la zone `sub-title` a changé de nom.")
    return L
ETIQ_HAS = re.compile(r'<div class="sub-title">\s*<span class="titleLabelCaps">([^<]{2,60})</span>')
RBPP_HAS = "Recommandation de bonne pratique"
_n_pdf = _n_exempt = _n_etiq = 0
for u in [u for u in urls if "has-sante.fr/jcms/" in u]:
    r = subprocess.run(["curl", "-s", "-L", "--max-time", "30"] + CA + ["-A", UA, u], capture_output=True); page = r.stdout.decode("utf-8", "ignore")
    pdfs = sorted(set(re.findall(r'https?://www\.has-sante\.fr/upload/docs/application/pdf/[^"\']+\.pdf', page)))
    pdfs = [d for d in pdfs if not re.search(r"(?i)focus_on|_en\.pdf|english", d)]
    if not pdfs:
        continue
    _n_pdf += 1
    _m = ETIQ_HAS.search(page)
    _et = _m.group(1).strip() if _m else ""
    if _et:
        _n_etiq += 1
    if _et != RBPP_HAS:
        _n_exempt += 1
        print("PAGE HAS NON-RBPP, MOTIF (1) NON APPLIQUÉ :", u,
              "\n   type déclaré par la page :", _et or "⟨aucune étiquette titleLabelCaps⟩",
              "—", len(pdfs), "PDF non confronté(s) aux ressources")
        continue
    if not any(d in urls for d in pdfs):
        print("PAGE HAS DE PRÉSENTATION SANS SON DOCUMENT :", u, "\n   PDF lié(s) sur la page, absent(s) des ressources :", " ; ".join(pdfs)); pb.append("PDF HAS non lié (%s)" % u.split("/")[-1][:50])
for _L in bilan_etiquettes(_n_pdf, _n_exempt, _n_etiq):
    print(_L)
# 2. UNE FRACTION PORTE SON EFFECTIF (A2 bis) — « 1/3 », « un tiers », « la moitié », « un sur cinq » dans un paragraphe qui nomme une source et ne donne aucun % : l'effectif compté est dans le paragraphe
for i, t in enumerate(T):
    if not re.search(r"(?i)\b(HAS|ANSM|INSERM|OMS|Merck|Psycom|selon|d'après|source|étude|enquête|base)\b", t): continue
    props = re.findall(r"(?i)\b(?:\d/\d|un tiers|deux tiers|un quart|trois quarts|la moitié|une? \w+ sur (?:deux|trois|quatre|cinq|dix))\b", t)
    if props and "%" not in t and not re.search(r"(?i)\b\d[\d\s]*\s?(?:événements?|évènements?|cas|patients?|personnes?|sujets?|adultes?|enfants?|participants?|études?|signalements?|décès|résidents?)\b|\bsur\s+(?:\d|un échantillon|une population|l'ensemble)|\bn\s?=\s?\d|\b(?:parmi|des)\s+\d[\d\s]*\b", t):
        print("PROPORTION SANS DÉNOMINATEUR (¶%d) :" % i, ", ".join(props), "—", t[:110]); pb.append("¶%d proportion sans effectif" % i)
# 3. UN CORRIGÉ EN TABLEAU NE MÉLANGE PAS LES CLASSES DE LA THÉORIE (C2) — un mot distinctif d'une section de théorie ne va pas dans la ligne d'une autre classe
def norm(s): return unicodedata.normalize("NFD", s.lower()).encode("ascii", "ignore").decode()
i_th = [i for i, t in enumerate(T) if re.match(r"^\s*\d\. [A-ZÉ]", t)]
i_ex = [i for i, t in enumerate(T) if re.search(r"(?i)^(🛠️|Pratique \()|Exercice 1", t)]
sections = {}
if i_th and i_ex:
    bornes = [i for i in i_th if i < i_ex[0]] + [i_ex[0]]
    zones = {}
    for a, b in zip(bornes, bornes[1:]):
        nom = norm(re.sub(r"^\s*\d\. (Les |Le |La |L')?", "", T[a])).split()[0].rstrip("s")
        sections[nom] = norm(" ".join(T[a:b]))
        ei = [j for j in range(a, b) if re.match(r"(?i)\s*effets ind[ée]sirables", T[j])]
        zones[nom] = norm(" ".join(T[ei[0]:b])) if ei else ""
i_cor = [i for i, t in enumerate(T) if re.match(r"(?i)Corrigé — Challenge", t)]
if sections and i_cor:
    k = x.find(ps[i_cor[0]]); m = re.search(r"<w:tbl>.*?</w:tbl>", x[k:], re.S)
    rows = re.findall(r"<w:tr\b.*?</w:tr>", m.group(0), re.S) if m else []
    for r in rows:
        cells = [html.unescape("".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", c))) for c in re.findall(r"<w:tc>.*?</w:tc>", r, re.S)]
        if len(cells) < 2: continue
        cls = [k for k in sections if k in norm(cells[0])]
        if len(cls) != 1: continue
        for w in set(re.findall(r"[a-z]{8,}", norm(" ".join(cells[1:])))):
            ailleurs = [k for k, s in zones.items() if k != cls[0] and re.search(r"\b" + w, s)]
            if ailleurs and not re.search(r"\b" + w, sections[cls[0]]):
                print("SIGNE D'UNE AUTRE CLASSE DANS LA LIGNE « %s » : « %s » est un effet indésirable de la théorie sous %s, absent de la section %s" % (cells[0], w, ailleurs[0], cls[0])); pb.append("ligne %s : %s" % (cells[0], w))
# 4. UNE DCI SE RECOPIE DE LA PAGE — tout nom de molécule des tableaux de théorie est sur une page ANSM listée
ansm = [u for u in urls if "ansm.sante.fr" in u]
if ansm and i_ex:
    corpus = ""
    for u in ansm:
        r = subprocess.run(["curl", "-s", "-L", "--max-time", "30"] + CA + ["-A", UA, u], capture_output=True); h = r.stdout.decode("utf-8", "ignore")
        corpus += " " + norm(html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", h, flags=re.S | re.I))))
    k_ex = x.find(ps[i_ex[0]])
    cellules = " ".join(html.unescape("".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", c))) for c in re.findall(r"<w:tc>.*?</w:tc>", x[:k_ex], re.S))
    for dci in sorted(set(re.findall(r"\b[A-ZÉ][a-zéèï]{6,}(?:ine|ate|ol|one|am|ide|azole|pine|idone|azine|azépine|xétine|pram|zone|ium)\b", cellules))):
        if norm(dci) not in corpus: print("DCI ABSENTE DES PAGES ANSM :", dci); pb.append("DCI « %s »" % dci)
if pb: sys.exit("LEÇON REFUSÉE — " + " ; ".join(pb))
print("OK — documents HAS liés, fractions avec effectif, tableau du corrigé cohérent avec la théorie, DCI sur les pages ANSM")