#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UN MARQUEUR QUI NOMME LE « JOURNAL DES CORRECTIONS » TRONQUE LE CORPS LU — 04/11/2026.

controle_attributions.py coupe le corps a la PREMIERE occurrence de « Journal des corrections »
(`jrn = corps.find(...)` puis `corps = corps[:jrn]`). Un marqueur de correction qui NOMME cette
section place donc la sentinelle AVANT la vraie section, et toutes les passes qui lisent « corps »
s'arretent au marqueur. MESURE de l'incident (veille SERAFIN-PH du 04/11/2026, defaut introduit par
moi en corrigeant son bloquant A4) : corps lu 2 886 caracteres au lieu de 9 854, SPANS = [] — le
marqueur, coupe avant son « ] », n'etait plus reconnu comme marqueur —, et A4 repondait « (aucune) »
SANS AVOIR LU la ligne fautive : un VERT sur 70 % du document.

⚠️ ET LA DOCTRINE ELLE-MEME INVITE A ECRIRE CE MARQUEUR : la ligne « corrige X » de CLAUDE.md
prescrit de conserver le libelle d'origine dans cette section, et il est naturel de l'y renvoyer.

📊 PORTEE MESUREE SUR LES 328 DOCUMENTS, PAS SUPPOSEE : 116 portent au moins un marqueur, 196 un
journal, et 0 a sa premiere occurrence DANS un marqueur — donc zero faux refus, zero verdict change.
Le defaut etait le mien seul, attrape avant publication.

⛔ CE QUE CETTE BORNE NE PEUT PAS VOIR, ET C'EST DIT : la chaine posee dans du TEXTE ORDINAIRE du
corps (ni marqueur, ni titre) tronque tout autant, et la garde ne l'attrape pas — la borne ⑫ fixe
cette limite au lieu de la laisser derivér en silence. Et la garde est TEXTUELLE : elle ne prouve pas
qu'un corps non tronque soit complet, seulement qu'aucun marqueur ne le coupe.

Aucun reseau. Aucun fichier du depot dans le verdict : les corpus et les .docx sont FABRIQUES.
"""
import os, re, subprocess, sys, tempfile, zipfile

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # outils/scripts
# 23/10/2026 — le bug de tolerance_page_morte.py : ce script vit UN CRAN plus bas que les controles,
# donc un dirname de trop (ou de moins) et tout ce qui suit mesure a cote. On l'assied sur un fait.
CTRL = os.path.join(RACINE, "controle_attributions.py")
assert os.path.isfile(CTRL), "RACINE fausse : %s n'existe pas" % CTRL

SRC = open(CTRL, encoding="utf-8").read()
SENTINELLE = "CORPS TRONQUE PAR UN MARQUEUR DE CORRECTION"
PHRASE = "Journal des corrections"
MARQ_OK = "[Corrigé le 04/11/2026 : libellé d'origine conservé en fin de document.]"
MARQ_KO = "[Corrigé le 04/11/2026 : libellé d'origine conservé au 📝 " + PHRASE + ".]"

LIGNE = "  %d/%d bornes du corps tronque"   # format PARTAGÉ avec la borne ⑮
jouees, ko = [], []
def borne(nom, cond, detail=""):
    jouees.append(nom)
    if not cond:
        ko.append(nom)
        print("  ✗ %s%s" % (nom, (" — " + detail) if detail else ""))

# ── le bloc est EXTRAIT du controle et EXECUTE, jamais recopie (regle du 15/10/2026)
m_marq = re.search(r"^MARQUEUR = re\.compile\(.*?\n(?=\w|def )", SRC, re.S | re.M)
m_span = re.search(r"^def spans_de\(z\):.*?\n    return \[.*?\]\n", SRC, re.S | re.M)
m_cond = re.search(r"^if (jrn != -1 and any\(.*?\)):\n", SRC, re.M)
borne("① le controle porte la garde : MARQUEUR, spans_de et la condition sont extractibles",
      bool(m_marq and m_span and m_cond),
      "marqueur=%s spans=%s cond=%s" % (bool(m_marq), bool(m_span), bool(m_cond)))
if not (m_marq and m_span and m_cond):
    print("  ✗ extraction impossible — le reste du lot ne prouverait rien")
    print("%d/%d bornes du corps tronque" % (len(jouees) - len(ko), len(jouees)))
    sys.exit(1)

NS = {"re": re}
exec(m_marq.group(0) + m_span.group(0), NS)
assert NS["spans_de"](MARQ_KO), "bloc extrait inoperant : il ne voit pas un marqueur entier"
COND = compile(m_cond.group(1), "<garde>", "eval")

def mord(corps_plein):
    """la garde EXTRAITE, jouee exactement comme le controle la joue"""
    j = corps_plein.find(PHRASE)
    g = dict(NS); g.update({"jrn": j, "corps_plein": corps_plein})
    return bool(eval(COND, g))   # un SEUL espace de noms : une genexpr ne voit pas les locaux d'eval

def mord_sur_tronque(corps_plein):
    """la version NAIVE : spans calcules sur le corps DEJA tronque (ce que ferait dans_marqueur)"""
    j = corps_plein.find(PHRASE)
    tronque = corps_plein[:j] if j != -1 else corps_plein
    g = dict(NS); g.update({"jrn": j, "corps_plein": tronque})
    return bool(eval(COND, g))

# ── ② et ③ : l'ORDRE et la SOURCE sont la moitie de la garde
i_plein = SRC.find("corps_plein = corps")
i_coupe = SRC.find("corps = corps[:jrn]")
borne("② « corps_plein = corps » PRECEDE la coupe (sinon il est deja tronque, et la garde est inerte)",
      0 < i_plein < i_coupe, "plein @%d · coupe @%d" % (i_plein, i_coupe))
borne("③ la garde teste spans_de(corps_plein), PAS SPANS ni dans_marqueur (calcules apres la coupe)",
      "spans_de(corps_plein)" in m_cond.group(1)
      and "SPANS" not in m_cond.group(1) and "dans_marqueur" not in m_cond.group(1),
      m_cond.group(1)[:90])
i_garde = SRC.find("sys.exit(\"" + SENTINELLE)
i_print = SRC.find("print(")
borne("④ la garde precede le PREMIER print du controle : aucun verdict sur un corps tronque",
      0 < i_garde < i_print, "garde @%d · premier print @%d" % (i_garde, i_print))
borne("⑤ le message porte la sentinelle, et dit les deux longueurs", i_garde > 0
      and "caracteres sur" in SRC[i_garde:i_garde + 700], "sentinelle @%d" % i_garde)

# ── ⑥ a ⑫ : la garde extraite, jouee sur des corpus FABRIQUES
CORPS = "=== TEXTE COMPLET (120 caracteres) ===\nSource primaire : CNSA, publie le 16/10/2026\n"
VRAI_JRN = "\n📝 " + PHRASE + " — 4 novembre 2026\nLibelle d'origine : « ... ».\n"
borne("⑥ coupe DANS un marqueur, vraie section plus bas → MORD",
      mord(CORPS + MARQ_KO + "\ncorps qui suit\n" + VRAI_JRN))
borne("⑦ aucun journal, aucun marqueur nommant la phrase → ACCEPTE",
      not mord(CORPS + MARQ_OK + "\ncorps qui suit\n"))
borne("⑧ vraie section de journal, marqueur qui ne la nomme pas → ACCEPTE",
      not mord(CORPS + MARQ_OK + "\ncorps qui suit\n" + VRAI_JRN))
borne("⑨ vraie section D'ABORD, un marqueur la nommant APRES → ACCEPTE (rien n'est tronque a tort)",
      not mord(CORPS + VRAI_JRN + MARQ_KO + "\n"))
borne("⑩ marqueur nommant la phrase SANS aucune vraie section → MORD",
      mord(CORPS + MARQ_KO + "\ncorps qui suit\n"))
borne("⑪ la version NAIVE (spans sur le corps tronque) NE MORD PAS sur le cas ⑥ — "
      "c'est elle, et elle seule, qui rend la borne ③ necessaire",
      not mord_sur_tronque(CORPS + MARQ_KO + "\ncorps qui suit\n" + VRAI_JRN))
borne("⑫ LIMITE DITE : la phrase dans du texte ORDINAIRE n'est PAS attrapee (elle tronque pourtant)",
      not mord(CORPS + "on parle ici du " + PHRASE + " en passant\n" + VRAI_JRN))

# ── ⑬ et ⑭ : le VRAI controle, de bout en bout, sur des .docx FABRIQUES (aucun reseau atteint,
#    la garde sortant avant la premiere requete)
def docx(chemin, textes):
    ps = "".join('<w:p><w:r><w:t xml:space="preserve">%s</w:t></w:r></w:p>' % t for t in textes)
    with zipfile.ZipFile(chemin, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml",
                   '<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"/>')
        z.writestr("_rels/.rels",
                   '<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>')
        z.writestr("word/_rels/document.xml.rels",
                   '<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>')
        z.writestr("word/document.xml",
                   '<?xml version="1.0"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                   '<w:body>' + ps + '</w:body></w:document>')

with tempfile.TemporaryDirectory() as d:
    f_ko, f_ok = os.path.join(d, "fautif.docx"), os.path.join(d, "conforme.docx")
    docx(f_ko, ["Source primaire : CNSA (cnsa.fr), publie le 16/10/2026", MARQ_KO,
                "corps qui suit", "📝 " + PHRASE + " — 4 novembre 2026", "Libelle d'origine : « ... »."])
    docx(f_ok, ["Source primaire : CNSA (cnsa.fr), publie le 16/10/2026", MARQ_OK,
                "corps qui suit", "📝 " + PHRASE + " — 4 novembre 2026", "Libelle d'origine : « ... »."])
    def lance(f):
        r = subprocess.run(["/usr/bin/python3", CTRL, f], capture_output=True, text=True, timeout=120)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    c_ko, s_ko = lance(f_ko)
    c_ok, s_ok = lance(f_ok)
    borne("⑬ bout en bout : le VRAI controle REFUSE le .docx fautif, exit 1, avec la sentinelle",
          c_ko == 1 and SENTINELLE in s_ko, "exit=%d · sentinelle=%s" % (c_ko, SENTINELLE in s_ko))
    borne("⑭ bout en bout : le .docx conforme n'est PAS refuse pour ce motif (ACCEPTE)",
          SENTINELLE not in s_ok, "sortie=%r" % s_ok[:120])

# ── ⑮ LE GARDE DU HARNAIS LIT-IL VRAIMENT CETTE LIGNE ? (04/11/2026, défaut à moi)
#    Mon premier motif exigeait un caractère PUIS une espace avant le numérateur ; la ligne
#    commençant en colonne 1, « LU_CT » était VIDE et le harnais REFUSAIT TOUS LES PUSHS. La même
#    faute avec une comparaison inversée aurait produit l'inverse : un garde qui ACCEPTE tout.
#    On applique donc le motif DU HARNAIS à la ligne que ce témoin imprime REELLEMENT.
NR_SH = os.path.join(RACINE, "non_regression.sh")
m_sed = re.search(r'LU_CT=\$\(sed -n "([^"]+)" "\$CT_OUT"\)', open(NR_SH, encoding="utf-8").read())
lu = ""
if m_sed:
    lu = subprocess.run(["sed", "-n", m_sed.group(1)], input=LIGNE % (13, 14),
                        capture_output=True, text=True).stdout.strip()
borne("⑮ le motif du harnais, appliqué à la ligne que ce témoin imprime, rend le DÉNOMINATEUR",
      bool(m_sed) and lu == "14", "motif=%s · lu=%r (14 attendu)" % (bool(m_sed), lu))

print(LIGNE % (len(jouees) - len(ko), len(jouees)))
sys.exit(1 if ko else 0)
