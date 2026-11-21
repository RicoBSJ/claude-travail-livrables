#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""㊳ TER — LE RENDEMENT D'UN RUN EST-IL MESURÉ ET DIT ? — 21/11/2026.

POURQUOI. Le 13/11/2026 le job ai-act a dépensé 5,0444 $ en 78 tours pour 5 316 caracteres
utiles — la plus petite note de sa serie depuis le 17/10 — et ZERO hyperlien, ce qui rend son
propre controle d'etape 5 bis INERTE. Le run a reussi au sens de ses controles, le document a
ete publie, et RIEN dans le depot ne rapprochait le cout de ce qui avait ete produit : ㊳ juge
si le run a ECHOUE, ㊳ bis compte les liens que le recapitulatif ANNONCE, le [mesure] donne le
cout. Entre « le run a echoue » et « le run a produit peu », il existait un troisieme etat que
personne ne regardait — meme forme que « un log n'est pas un run » (23/10) et « un run n'est pas
une publication » (06/11).

⛔ LE MOTIF EST NON BLOQUANT (regle du 14/10 : il juge un CONTENU, et une semaine creuse rend
   legitimement une note breve), donc il se garde par des EXIGENCES DE LIGNE et par la borne ⑯,
   qui exige que le code de sortie du vrai controle reste 0.
⛔ RIEN DE VIVANT DANS LE VERDICT : la serie est FABRIQUEE en tempfile et datee 2099 (lecon du
   22/10). Le seul fait du depot employe est le nom de dossier « ai-act », et il est auto-
   reparant : s'il sortait de la config, la table de ㊳ le deduirait du log fabrique.
⛔ ET LES MOTIFS SONT IMPORTES DU CONTROLE, JAMAIS RECOPIES (regle du 15/10) : une copie ne
   garde rien, et une copie qui derive invente des defauts (25/10).

Aucun reseau. 24 bornes, 11 s mesurees (11,61 / 11,46 / 11,32) : le prix de
quatre series fabriquees et de huit lancements du VRAI controle en sous-processus.
"""
import hashlib, importlib.util, os, re, shutil, subprocess, sys, tempfile, zipfile

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # outils/scripts
NR_SH = os.path.join(RACINE, "non_regression.sh")
assert os.path.isfile(NR_SH), "RACINE fausse : %s n'existe pas" % NR_SH
CTRL = os.path.join(RACINE, "controle_livrable_du_job.py")
assert os.path.isfile(CTRL), "contrôle introuvable : %s" % CTRL

_sp = importlib.util.spec_from_file_location("clj", CTRL)
clj = importlib.util.module_from_spec(_sp)
_sp.loader.exec_module(clj)          # le VRAI contrôle, importé et non recopié

TMP = tempfile.mkdtemp(prefix="rendement_")

DOCX_CT = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
           '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
           '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.'
           'relationships+xml"/><Override PartName="/word/document.xml" ContentType='
           '"application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
           '</Types>')
RELS = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
        'relationships/officeDocument" Target="word/document.xml"/></Relationships>')
W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
RID = 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'


def docx(chemin, paras, rels_ext=(), servis=()):
    """Un .docx MINIMAL mais VRAI : c'est le vrai extract_docx.py qui le lira."""
    corps = ""
    for i, t in enumerate(paras):
        inner = '<w:r><w:t xml:space="preserve">%s</w:t></w:r>' % t
        if i < len(servis) and servis[i]:
            inner = '<w:hyperlink r:id="%s">%s</w:hyperlink>' % (servis[i], inner)
        corps += "<w:p>%s</w:p>" % inner
    xml = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document %s %s><w:body>%s'
           '</w:body></w:document>' % (W, RID, corps))
    rl = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns='
          '"http://schemas.openxmlformats.org/package/2006/relationships">'
          + "".join('<Relationship Id="%s" Type="http://schemas.openxmlformats.org/officeDocument'
                    '/2006/relationships/hyperlink" Target="%s" TargetMode="External"/>' % (i, u)
                    for i, u in rels_ext) + "</Relationships>")
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with zipfile.ZipFile(chemin, "w") as z:
        z.writestr("[Content_Types].xml", DOCX_CT)
        z.writestr("_rels/.rels", RELS)
        z.writestr("word/document.xml", xml)
        z.writestr("word/_rels/document.xml.rels", rl)
    return chemin


def log(dossier, job, jour, cout=None, plafond="6.00", pct=97, tours=68, extra=""):
    os.makedirs(dossier, exist_ok=True)
    p = os.path.join(dossier, "%s_%s_090300.log" % (job, jour.replace("-", "")))
    t = ">>> Démarrage du job : %s\n[auth] ok\n%s" % (job, extra)
    if cout is not None:
        t += ("[mesure] coût réel %s $ / plafond %s $ (%d %% du plafond) | %d tours | 836718 ms"
              " | in 75 · out 37035 · cache-read 9268406 · cache-write 289537\n"
              % (cout, plafond, pct, tours))
    t += "[diagnostic] is_error=False | subtype=success | stop_reason=end_turn\n"
    t += "<<< Fin du job %s (code de sortie : 0, tentatives : 1)\n" % job
    open(p, "w", encoding="utf-8").write(t)
    return p


LIGNE = "  %d/%d bornes du rendement d un run"
jouees, ko = [], []
def borne(nom, cond, detail=""):
    jouees.append(nom)
    if not cond:
        ko.append(nom)
        print("  ✗ %s%s" % (nom, (" — " + detail) if detail else ""))


# ── ① ② le motif [mesure], IMPORTÉ du contrôle ──────────────────────────────────────────────
reel = ("[mesure] coût réel 5.8261 $ / plafond 6.00 $ (97 % du plafond) | 68 tours | 836718 ms"
        " | in 75 · out 37035 · cache-read 9268406 · cache-write 289537")
m = clj.MESURE.search(reel)
borne("① le motif [mesure] lit coût, plafond, taux et tours sur la ligne RÉELLE du 20/11",
      bool(m) and m.group(1) == "5.8261" and m.group(3) == "97" and m.group(4) == "68",
      "groupes=%r" % ((m.groups() if m else None),))
borne("② ACCEPTÉE : une ligne sans « coût réel » n'est pas lue — un log muet n'accuse rien",
      clj.MESURE.search("[diagnostic] is_error=False | subtype=success") is None)

# ── ③ ④ le compte de caractères, ANNONCÉ par extract_docx et non recalculé ──────────────────
d3 = docx(os.path.join(TMP, "s", "d3.docx"), ["Alpha beta gamma.", "Delta epsilon."])
t3 = clj.texte(d3)
borne("③ le compte de caractères est celui qu'ANNONCE extract_docx.py (vrai .docx, vrai script)",
      clj.utiles(t3) is not None and clj.utiles(t3) > 0, "utiles=%r" % clj.utiles(t3))
borne("④ ACCEPTÉE : sans la ligne de compte, utiles() rend None et non 0 — un 0 rendrait un "
      "rendement infini", clj.utiles("une sortie quelconque sans compte") is None)

# ── ⑤ ⑥ ⑦ les liens SERVIS ──────────────────────────────────────────────────────────────────
d5 = docx(os.path.join(TMP, "s", "d5.docx"), ["Un lien.", "Du texte."],
          rels_ext=[("rId9", "https://example.invalid/a"), ("rId8", "https://example.invalid/b")],
          servis=["rId9", None])
borne("⑤ liens_servis() compte les relations externes RÉELLEMENT servies dans le corps",
      clj.liens_servis(d5) == 1, "compte=%r" % clj.liens_servis(d5))
borne("⑥ ACCEPTÉE : un rel ORPHELIN n'est pas un lien cliquable (règle du 25/10) — 2 rels, "
      "1 servi, le compte dit 1", clj.liens_servis(d5) == 1)
faux = os.path.join(TMP, "s", "pas_un_zip.docx")
open(faux, "w").write("ceci n'est pas un zip")
borne("⑦ un fichier illisible rend None et non 0 — « je ne sais pas » n'est pas « zéro lien »",
      clj.liens_servis(faux) is None, "compte=%r" % clj.liens_servis(faux))

# ── ⑧ ⑨ ⑩ le document corrigé ───────────────────────────────────────────────────────────────
borne("⑧ CORRIGE voit un 📝 Journal des corrections",
      bool(clj.CORRIGE.search("… 📝 Journal des corrections — 21 novembre 2026 …")))
borne("⑨ CORRIGE voit un marqueur [Corrigé le …]",
      bool(clj.CORRIGE.search("… texte [Corrigé le 21/11/2026 : libellé] …")))
borne("⑩ ACCEPTÉE : un document neuf n'est pas dit corrigé",
      not clj.CORRIGE.search("Une note de veille ordinaire, avec ses sources et ses tableaux."))

# ── ⑪ à ⑮ : le VRAI rendement() et le VRAI comparables(), RACINE et LOGS déplacés ───────────
SERIE = os.path.join(TMP, "sources", "veille", "ai-act")
LOGS = os.path.join(TMP, "logs")
clj.LOGS = LOGS
clj._MEMO.clear()
d11 = docx(os.path.join(SERIE, "2099-01-01_veille_ai-act.docx"), ["Texte de la note."] * 20,
           rels_ext=[("rId9", "https://example.invalid/a")], servis=[None] * 19 + ["rId9"])
log(LOGS, "ai-act-veille", "2099-01-01", cout="5.0000")
r11 = clj.rendement(d11)
attendu = 5.0 * 1000.0 / r11["car"] if r11 and r11.get("car") else None
borne("⑪ bout en bout : rendement() rend coût × 1 000 / caractères, exactement",
      bool(r11) and "par_mille" in r11 and abs(r11["par_mille"] - attendu) < 1e-9,
      "r=%r" % r11)
d12 = docx(os.path.join(SERIE, "2099-02-02_veille_ai-act.docx"), ["Sans log."])
r12 = clj.rendement(d12)
borne("⑫ DÉTECTION POSITIVE : sans log (la purge à 30 jours), il DIT « sans_log » et ne rend "
      "AUCUN rendement", bool(r12) and r12["sans_log"] and "par_mille" not in r12, "r=%r" % r12)
d13 = docx(os.path.join(SERIE, "2099-03-03_veille_ai-act.docx"), ["Log sans mesure."])
log(LOGS, "ai-act-veille", "2099-03-03", cout=None)
r13 = clj.rendement(d13)
borne("⑬ un log SANS ligne [mesure] ne rend pas de rendement non plus, et le document est lu",
      bool(r13) and not r13["sans_log"] and "par_mille" not in r13 and r13["car"] > 0,
      "r=%r" % r13)
base = clj.comparables(d11)
borne("⑭ comparables() ne retient que les runs MESURABLES de la série (1 sur 3 ici)",
      len(base) == 1 and base[0]["doc"].startswith("2099-01-01"),
      "base=%r" % [c["doc"] for c in base])
d15 = docx(os.path.join(SERIE, "2099-04-04_veille_ai-act.docx"), ["Autre note."] * 10)
log(LOGS, "ai-act-veille", "2099-04-04", cout="2.0000")
borne("⑮ la base est DÉRIVÉE DU DISQUE, jamais écrite en dur : un run mesurable de plus et elle "
      "passe de 1 à 2", len(clj.comparables(d11)) == 2,
      "base=%r" % [c["doc"] for c in clj.comparables(d11)])

# ── ⑯ à ⑱ quater : le VRAI contrôle lancé en sous-processus, avec --logs ────────────────────
#    TROIS séries FABRIQUÉES, parce que le drapeau tient sur une CONJONCTION de trois conditions
#    et qu'une seule série ne peut pas les séparer :
#      A (serafin-ph)   : 4 runs mesurables, le PLUS RÉCENT est le PIRE  → le drapeau se lève
#      B (has-actualite): 4 runs mesurables, le pire est le PLUS ANCIEN  → il NE se lève PAS
#      C (imac)         : 3 runs mesurables, le plus récent est le pire  → il NE se lève PAS
#    Chacune dans un dossier VIERGE : le dossier « ai-act » sert déjà aux bornes ⑪–⑮, et son
#    dénominateur n'est donc pas celui qu'on borne ici (mesuré : 6 et non 4, au premier essai).
#    🔴 LES DEUX BORNES ACCEPTÉES SONT MESURÉES, PAS SUPPOSÉES : sans « le plus récent », le
#    drapeau se levait sur 6 documents du dépôt — un par série, PAR CONSTRUCTION, puisque le pire
#    d'une série existe toujours ; sans le plancher de 3 autres, sur 3, dont un rang 2/2 (le bilan
#    d'hypnose, parcours CLOS). Après bornage : 2, et les deux ont un sens.
def lance(doc):
    r = subprocess.run(["/usr/bin/env", "-i", sys.executable, CTRL, "--logs", LOGS, doc],
                       capture_output=True, text=True)
    return r.returncode, r.stdout


def serie(dossier, runs):
    """runs = [(jour, coût, nb_paras)] — le rendement est COÛT×1000/car, donc peu de ¶ et un
    coût élevé font un mauvais rendement. On ne devine rien : on mesure après coup."""
    base = os.path.join(TMP, "sources", "veille", dossier)
    job = {"ai-act": "ai-act-veille", "has-actualite": "rbpp-pipeline",
           "serafin-ph": "serafin-ph-veille", "imac": "imac-veille"}[dossier]
    chemins = {}
    for jour, cout, n in runs:
        chemins[jour] = docx(os.path.join(base, "%s_veille_%s.docx" % (jour, dossier)),
                             ["Texte de la note."] * n)
        log(LOGS, job, jour, cout=cout)
    return chemins


# A : le plus récent (2099-12-12, 9 $ pour 2 ¶) est le pire des quatre
A = serie("serafin-ph", [("2099-07-07", "1.0000", 40), ("2099-08-08", "1.2000", 40),
                     ("2099-09-09", "1.4000", 40), ("2099-12-12", "9.0000", 2)])
cA, sA = lance(A["2099-12-12"])
rA = {c["jour"]: c["par_mille"] for c in clj.comparables(A["2099-12-12"])}
pireA = max(rA, key=rA.get)
borne("⑯ ACCEPTÉE : le rendement NE TOUCHE PAS le code de sortie — exit 0 même quand il alerte, "
      "motif NON BLOQUANT", cA == 0 and "📐" in sA, "exit=%d · %r" % (cA, sA[:110]))
borne("⑰ le drapeau se lève quand le PLUS RÉCENT est le PIRE sur ≥ 3 autres (mesuré : le pire "
      "est bien %s)" % pireA,
      "PIRE RENDEMENT" in sA and pireA == "2099-12-12" and len(rA) == 4,
      "pire=%s · mesurables=%d · drapeau=%s" % (pireA, len(rA), "PIRE RENDEMENT" in sA))
borne("⑰ bis le rang est IMPRIMÉ avec son dénominateur : c'est l'ALERTE qui est bornée, pas "
      "l'information", "rang 4/4" in sA, "sortie=%r" % sA)

# B : le pire est le PLUS ANCIEN — il ne doit PAS être signalé
B = serie("has-actualite", [("2099-07-07", "9.0000", 2), ("2099-08-08", "1.2000", 40),
                            ("2099-09-09", "1.4000", 40), ("2099-12-12", "1.6000", 40)])
cB, sB = lance(B["2099-07-07"])
rB = {c["jour"]: c["par_mille"] for c in clj.comparables(B["2099-07-07"])}
borne("⑱ ACCEPTÉE : le pire d'une série n'est PAS signalé s'il n'est pas le plus récent — sans "
      "cette borne le drapeau se levait sur 6 documents du dépôt, un par série",
      "PIRE RENDEMENT" not in sB and max(rB, key=rB.get) == "2099-07-07" and "rang 4/4" in sB,
      "drapeau=%s · pire=%s" % ("PIRE RENDEMENT" in sB, max(rB, key=rB.get)))

# C : trois runs seulement — « pire de 3 » ne vaut pas une alerte
C = serie("imac", [("2099-07-07", "1.0000", 40), ("2099-08-08", "1.2000", 40),
                         ("2099-12-12", "9.0000", 2)])
cC, sC = lance(C["2099-12-12"])
rC = {c["jour"]: c["par_mille"] for c in clj.comparables(C["2099-12-12"])}
borne("⑱ bis ACCEPTÉE : le plancher du dénominateur — pire ET plus récent, mais sur 2 autres "
      "seulement, n'alerte pas (« pire de 2 » est vrai une fois sur deux par hasard)",
      "PIRE RENDEMENT" not in sC and max(rC, key=rC.get) == "2099-12-12" and "rang 3/3" in sC,
      "drapeau=%s · mesurables=%d" % ("PIRE RENDEMENT" in sC, len(rC)))

# ⑱ ter : zéro hyperlien servi → l'étape 5 bis du job est INERTE
sans = docx(os.path.join(TMP, "sources", "veille", "ai-act", "2099-11-11_veille_ai-act.docx"),
            ["Sans aucun lien."] * 5)
log(LOGS, "ai-act-veille", "2099-11-11", cout="4.0000")
borne("⑱ ter zéro hyperlien servi fait DIRE que l'étape 5 bis du job est INERTE — l'état mesuré "
      "du 13/11/2026", "INERTE" in lance(sans)[1])

# ⑱ quater : un document CORRIGÉ voit son rendement déclaré non comparable
corr = docx(os.path.join(TMP, "sources", "veille", "ai-act", "2099-10-10_veille_ai-act.docx"),
            ["Du texte."] * 20 + ["📝 Journal des corrections — 21 novembre 2026"])
log(LOGS, "ai-act-veille", "2099-10-10", cout="3.0000")
borne("⑱ quater un document CORRIGÉ depuis son run le DIT : son rendement n'est pas celui du run",
      "CORRIGÉ depuis" in lance(corr)[1], "sortie=%r" % lance(corr)[1][-200:])

# ── ⑲ le garde du harnais lit-il la ligne que ce témoin imprime RÉELLEMENT ? (défaut du 04/11)
#     Ancre ASCII SANS ACCENT, et le sed est LU dans le harnais, jamais recopié.
m_sed = re.search(r'LU_REND=\$\(sed -n "([^"]+)"', open(NR_SH, encoding="utf-8").read())
lu = ""
if m_sed:
    lu = subprocess.run(["sed", "-n", m_sed.group(1)], input=LIGNE % (23, 24),
                        capture_output=True, text=True).stdout.strip()
borne("⑲ le motif du harnais, appliqué à la ligne que ce témoin imprime, rend le DÉNOMINATEUR",
      bool(m_sed) and lu == "24", "motif=%s · lu=%r (24 attendu)" % (bool(m_sed), lu))

shutil.rmtree(TMP, ignore_errors=True)
borne("⑳ le témoin ne laisse RIEN derrière lui (la fuite de 330 dossiers du 17/11)",
      not os.path.isdir(TMP), "reste : %s" % TMP)

print(LIGNE % (len(jouees) - len(ko), len(jouees)))
sys.exit(1 if ko else 0)
