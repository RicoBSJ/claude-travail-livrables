#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Temoin de controle_faits_imac.py — LES FAITS ACQUIS SONT-ILS RECOPIES JUSTES DANS LE LIVRABLE ?

Aucun reseau, aucun tiers, aucun document vivant dans le verdict : les `.docx` sont FABRIQUES en
tempfile (lecon du 22/10). Les 5 signalements du corpus reel disparaitraient a la premiere
correction des deux editions concernees, donc un compte attendu sur le depot perimerait tout seul
et bloquerait tous les pushs — ce qui est arrive les 15, 22 et 23/10, puis le 04/11.

Le fabricateur de `.docx` est EXTRAIT de non_regression/murs_lus.py et execute, jamais recopie
(regle du 15/10) : une derive du fabricateur ne peut donc pas rendre ce lot vert sur du vide.
Et `signale()` est EXTRAIT du controle, jamais reimplemente.
"""
import io, json, os, re, subprocess, sys, tempfile, unicodedata

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))        # outils/scripts
NR_SH = os.path.join(RACINE, "non_regression.sh")
CTRL = os.path.join(RACINE, "controle_faits_imac.py")
CONFIG = os.path.join(os.path.dirname(RACINE), "..", "jobs_config.json")
assert os.path.isfile(NR_SH) and os.path.isfile(CTRL), "RACINE fausse : %s" % RACINE

# ── le fabricateur de .docx, EXTRAIT de murs_lus.py ──────────────────────────────────────────
_src = io.open(os.path.join(RACINE, "non_regression", "murs_lus.py"), encoding="utf-8").read()
_a = _src.index("def docx(")
_b = _src.index("    z.close()", _a) + len("    z.close()")
_g = {"zipfile": __import__("zipfile")}
exec(_src[_a:_b], _g)
docx = _g["docx"]

# ── le contrôle lui-même, EXTRAIT et exécuté (jamais réimplémenté) ───────────────────────────
_c = io.open(CTRL, encoding="utf-8").read()
_h = {"io": io, "os": os, "re": re, "subprocess": subprocess, "sys": sys,
      "unicodedata": unicodedata, "__file__": CTRL}
exec(_c[_c.index("EXTRACT = "):_c.index('if __name__ == "__main__":')], _h)
signale, GRILLE_M6, PRIX_US = _h["signale"], _h["GRILLE_M6"], _h["PRIX_US"]
corps_runs, SENTINELLE = _h["corps_runs"], _h["SENTINELLE"]

LIGNE = "  %d/%d bornes des faits acquis dans le livrable imac"
jouees, ko = [], []
def borne(nom, cond, detail=""):
    jouees.append(nom)
    if not cond:
        ko.append(nom)
        print("  ✗ %s%s" % (nom, (" — " + detail) if detail else ""))


def sig(lignes):
    return signale(lignes)


# ① le defaut REEL du 15/11 et du 22/11 : 2 219 € donne pour 512 Go.
o, li, do = sig(["M6 · 12c CPU/GPU · 16 Go · 512 Go + nano-texturé", "2 219 €"])
borne("① 512 Go CUMULÉ au nano-texturé à 2 219 € → signalé, et le VERRE est nommé",
      len(o) == 1 and "verre nano" in o[0] and "256 Go/nano" in o[0] and "512 Go/standard" in o[0]
      and li == 1, "o=%r li=%d" % (o, li))
# ② ACCEPTEE : la grille M4 porte LEGITIMEMENT 512 Go a 2 219 € — c'est le discriminant « M6 ».
o2, _, _ = sig(["M4 · 10c CPU/GPU · 16 Go · 512 Go · 4 ports USB", "2 219 €"])
borne("② la ligne M4 à 2 219 € / 512 Go n'est PAS accusée (ACCEPTÉE)", o2 == [], "o=%r" % (o2,))
# ③ ACCEPTEE : 2 439 € EST la reference M6 a 512 Go, avec 24 Go.
o3, l3, _ = sig(["M6 · 12c CPU/GPU · 24 Go · 512 Go · 4 ports USB", "2 439 €"])
borne("③ 2 439 € avec 512 Go accepté (ACCEPTÉE)", o3 == [] and l3 == 1, "o=%r l=%d" % (o3, l3))
# ④ ACCEPTEE : un prix HORS grille n'est pas confronte a la grille (Mac mini M6, iMac M4).
o4, l4, _ = sig(["Mac mini M6 lancé à 1 049 € (16 Go/256 Go) — hors gamme iMac"])
borne("④ prix hors grille non confronté (ACCEPTÉE)", o4 == [] and l4 == 0, "o=%r l=%d" % (o4, l4))
# ⑤ le prix peut etre dans le run SUIVANT : une ligne de tableau est PLUSIEURS runs.
o5, l5, _ = sig(["M6 · 12c CPU/GPU · 16 Go · 512 Go nano-texturé", "Apple", "2 219 €"])
borne("⑤ prix lu jusqu'au 2ᵉ run suivant", len(o5) == 1 and l5 == 1, "o=%r" % (o5,))
# ⑥ ACCEPTEE : le stockage N'EST PAS lu dans les runs suivants, sinon deux lignes se recollent.
o6, l6, _ = sig(["M6 · 12c CPU/GPU · 16 Go nano-texturé", "512 Go", "2 219 €"])
borne("⑥ stockage lu dans le libellé SEUL (ACCEPTÉE)", o6 == [] and l6 == 0, "o=%r l=%d" % (o6, l6))
# ⑦ le defaut REEL du 15/11 : « Prix US au lancement : 1 299 $ ».
o7, _, d7 = sig(["Prix US au lancement : 1 299 $ pour l'entrée de gamme (source 9to5Mac)"])
borne("⑦ 1 299 $ au lancement → signalé", len(o7) == 1 and "1 499" in o7[0] and d7 == 1,
      "o=%r d=%d" % (o7, d7))
# ⑧ ACCEPTEE : les trois prix US mesures passent, dans les deux graphies.
o8, _, d8 = sig(["iMac M6, prix US au lancement : $1,499 / $1,699, et $1,449 en éducation"])
borne("⑧ les trois prix US mesurés passent (ACCEPTÉE)", o8 == [] and d8 == 3,
      "o=%r d=%d" % (o8, d8))
# ⑨ ACCEPTEE : un dollar HORS contexte de lancement n'est ni accuse ni compte.
o9, _, d9 = sig(["Un écran externe à 1 299 $ chez un revendeur américain"])
borne("⑨ dollar hors contexte de lancement ignoré (ACCEPTÉE)", o9 == [] and d9 == 0,
      "o=%r d=%d" % (o9, d9))
# ⑩ DETECTION POSITIVE : un document muet n'accuse rien, et le DIT.
o10, l10, d10 = sig(["Veille sans grille de prix ni mention de lancement."])
borne("⑩ document muet → aucune accusation", o10 == [] and l10 == 0 and d10 == 0)
# ⑪ 2 219 € porte DEUX variantes et le VERRE les separe : invariant mesure au ① le 22/11/2026
#    par extraction des 14 references Apple du comparateur. Une grille par CAPACITE seule
#    accusait la ligne juste du 22/11 : c'est le defaut que cette borne interdit de refaire.
borne("⑪ 2 219 € = 256 Go/nano OU 512 Go/standard, et 2 439 € = 512 Go/standard",
      sorted(GRILLE_M6) == ["1 799", "1 999", "2 219", "2 439"]
      and sorted(GRILLE_M6["2 219"]) == [("256", "nano"), ("512", "standard")]
      and GRILLE_M6["2 439"] == [("512", "standard")]
      and GRILLE_M6["1 999"] == [("256", "standard")],
      "grille=%r" % (GRILLE_M6,))
# ⑫ les trois prix US mesures sont bien les trois, et 1 299 n'en est pas.
borne("⑫ PRIX_US = 1 499 · 1 699 · 1 449", sorted(PRIX_US) == ["1 449", "1 499", "1 699"],
      "us=%r" % (sorted(PRIX_US),))

# ── le VRAI verdict(), de bout en bout, sur des .docx FABRIQUÉS ──────────────────────────────
tmp = tempfile.mkdtemp(prefix="faits_livrable_")
FAUX = os.path.join(tmp, "faux.docx")
BON = os.path.join(tmp, "bon.docx")
docx(FAUX, ["M6 · 12c CPU/GPU · 16 Go · 512 Go + nano-texturé", "2 219 €",
            "iMac M6 — prix US au lancement : 1 299 $"])
docx(BON, ["M6 · 12c CPU/GPU · 16 Go · 256 Go · verre nano-texturé", "2 219 €",
           "iMac M6 — prix US au lancement : $1,499"])


def joue(*docs):
    r = subprocess.run(["/usr/bin/python3", CTRL] + list(docs), capture_output=True, text=True,
                       env={"PATH": "/usr/bin:/bin"})
    return r.returncode, r.stdout


rc, out = joue(FAUX)
# ⑬ le verdict reel NOMME le document et les deux contradictions.
borne("⑬ verdict réel : document nommé, 2 contradictions", "faux.docx" in out
      and out.count("FAIT ACQUIS CONTREDIT") == 2 and "2 contradiction(s)" in out,
      "out=%r" % (out[-240:],))
# ⑭ ACCEPTEE, ET C'EST LA MOITIE QUI COMPTE : NON BLOQUANT, exit 0 meme quand il signale.
borne("⑭ exit 0 même quand il signale (ACCEPTÉE)", rc == 0, "rc=%d" % rc)
rc2, out2 = joue(BON)
# ⑮ ACCEPTEE : le document juste ne produit AUCUNE contradiction, et les denominateurs sont lus.
borne("⑮ document juste → 0 contradiction, dénominateurs imprimés (ACCEPTÉE)",
      rc2 == 0 and "0 contradiction(s)" in out2 and "1 ligne(s) de grille M6 lue(s)" in out2
      and "1 prix en dollars lu(s)" in out2, "out=%r" % (out2[-240:],))

# ── LE VERRE, LA LIGNE, LE MARQUEUR : les bornes nées du 22/11/2026 au soir ──────────────────
# ⑯ ACCEPTEE, ET C'EST LA BORNE DECISIVE : 512 Go a 2 219 € en verre STANDARD est une variante
#    LEGITIME (4 references Apple). Une grille par CAPACITE seule accusait cette ligne — elle
#    l'a fait, sur les deux editions, et c'est le contrôle qui avait tort. Sans cette borne,
#    rien n'empeche d'y revenir demain.
o16, l16, _ = sig(["M6 · 12c/12c · 16 Go · 512 Go · 4 ports USB", "2 219 €"])
borne("⑯ 512 Go à 2 219 € en verre standard n'est PAS accusé (ACCEPTÉE)",
      o16 == [] and l16 == 1, "o=%r l=%d" % (o16, l16))
# ⑰ ACCEPTEE : l'autre variante du meme prix, 256 Go a verre nano-texture.
o17, l17, _ = sig(["M6 · 12c/12c · 16 Go · 256 Go · 4 ports USB · verre nano-texturé", "2 219 €"])
borne("⑰ 256 Go à 2 219 € en nano-texturé n'est PAS accusé (ACCEPTÉE)",
      o17 == [] and l17 == 1, "o=%r l=%d" % (o17, l17))
# ⑱ ET LA REGLE MORD DANS L'AUTRE SENS : 256 Go en verre STANDARD vaut 1 999 €, pas 2 219 €.
o18, _, _ = sig(["M6 · 12c/12c · 16 Go · 256 Go · 4 ports USB", "2 219 €"])
borne("⑱ 256 Go à 2 219 € en verre standard → signalé",
      len(o18) == 1 and "verre standard" in o18[0], "o=%r" % (o18,))
# ⑲ ACCEPTEE : une ligne de PUCES porte SON prix, et n'est pas confrontee a celui des deux
#    suivantes. Forme reelle de la note controle-livrables du 08/11, deux faux positifs mesures.
o19, l19, _ = sig(["• M6 10c CPU/GPU · 16 Go · 256 Go : 1 799,00 € ✅ (concordance)",
                   "• M6 12c CPU/GPU · 16 Go · 256 Go : 1 999,00 € ✅ (concordance)",
                   "• M6 12c CPU/GPU · 24 Go · 512 Go : 2 439,00 € ✅ (concordance)"])
borne("⑲ trois lignes de puces, chacune avec SON prix → 0 accusation (ACCEPTÉE)",
      o19 == [] and l19 == 3, "o=%r l=%d" % (o19, l19))
# ⑳ ACCEPTEE : une PROSE qui nomme M6 et un stockage n'emprunte pas le prix du paragraphe
#    SUIVANT. Forme reelle de la veille du 18/10, faux positif mesure.
o20, l20, _ = sig(["⚠️ Contexte : les configurations M6 16 Go et 256 Go n'offrent aucune remise",
                   "Autres remises : iMac 10c/10c · 512 Go Vert à 1 971 € (−11,2 % vs 2 219 €)"])
borne("⑳ prose : le prix du paragraphe suivant n'est pas emprunté (ACCEPTÉE)",
      o20 == [] and l20 == 0, "o=%r l=%d" % (o20, l20))
# ㉑ ACCEPTEE : un MARQUEUR qui cite le libelle fautif ne rouvre pas le motif qu'on vient de
#    fermer (leçons des 23 et 25/10). corps_runs est joue, pas suppose.
cr21 = corps_runs(["   [Corrigé le 22/11/2026 : « M6 · 12c CPU/GPU · 16 Go · 512 Go + "
                   "nano-texturé » cumulait deux options, et 1 999 € en est la base]", "2 219 €"])
o21, l21, _ = sig(cr21)
borne("㉑ marqueur citant le libellé fautif → aucune accusation (ACCEPTÉE)",
      o21 == [] and l21 == 0, "o=%r l=%d" % (o21, l21))
# ㉒ tout ce qui suit le TITRE du journal est hors du corps : ses chiffres ne sont pas ceux
#    d'une ligne de grille — 4 accusations portees par mes propres journaux le 22/11 au soir.
cr22 = corps_runs(["📝 Journal des corrections — 22 novembre 2026",
                   "M6 · 12c/12c · 16 Go · 512 Go + nano-texturé était faux", "2 219 €"])
borne("㉒ rien n'est lu à partir du titre du journal", cr22 == [], "corps=%r" % (cr22,))
# ㉓ ACCEPTEE, ET DECISIVE : la sentinelle est le TITRE, jamais la phrase nue. Une note qui
#    PARLE du journal d'un autre document ne doit pas etre tronquee — forme reelle de la note
#    controle-livrables du 08/11, ou tronquer sur la phrase nue coupait au run 76 sur 99.
cr23 = corps_runs(["4. HAS — 2 citations du Journal des corrections non confirmables",
                   "• M6 12c CPU/GPU · 24 Go · 512 Go : 2 439,00 € ✅ (concordance)"])
o23, l23, _ = sig(cr23)
borne("㉓ la phrase « Journal des corrections » SANS son titre ne tronque pas (ACCEPTÉE)",
      len(cr23) == 2 and o23 == [] and l23 == 1, "corps=%d o=%r l=%d" % (len(cr23), o23, l23))
# ㉔ ACCEPTEE, FABRIQUEE ET DITE TELLE : un dollar dans un run qui dit « lancement » mais ne
#    nomme PAS la machine n'est pas un prix US d'iMac. Le corpus n'en porte qu'un cas, dans une
#    leçon revenus-passifs, et les deux resserrements possibles y sont EQUIVALENTS : c'est donc
#    cette borne, et non la mesure, qui fixe le choix de la conjonction.
o24, _, d24 = sig(["Taille de marché ($15,7B → $59,6B), données de lancement : 70 % <1 000 $/mois"])
borne("㉔ « lancement » sans la machine → ni accusé ni compté (ACCEPTÉE)",
      o24 == [] and d24 == 0, "o=%r d=%d" % (o24, d24))

# ㉕ CONCORDANCE AVEC LE PROMPT, dans les DEUX SENS, et sans recopier ni l'un ni l'autre : la
#    grille du controle et les faits verses au prompt doivent dire la MEME chose. Sans cette
#    borne, mettre a jour l'un et pas l'autre deriverait en SILENCE — aucun des deux fichiers
#    n'importe les constantes de l'autre (meme classe que le plancher de 3 000 porte par cinq
#    fichiers). Si le prompt n'est pas lisible, la borne REFUSE : elle ne s'excuse pas.
ecarts = []
try:
    d = json.load(io.open(os.path.normpath(CONFIG), encoding="utf-8"))
    pr = [j for j in d["jobs"] if j["id"] == "imac-veille"][0]["prompt"]
    a = pr.find("## ⚠️ FAITS ACQUIS")
    m = re.search(r"\n## ", pr[a:]) if a != -1 else None
    fen = pr[a:a + m.start()] if (a != -1 and m) else ""
    if not fen:
        ecarts.append("aucune section « FAITS ACQUIS » dans le prompt imac")
    MOT_VERRE = {"nano": "nano-texturé", "standard": "verre standard"}
    for p in ("1 799", "2 219"):
        i = fen.find(p)
        if i == -1:
            ecarts.append("%s absent du prompt" % p)
            continue
        # FENETRE STRUCTURELLE — la puce qui porte ce prix, jusqu'a la suivante — et JAMAIS un
        # nombre de caracteres en dur : une fenetre de 200 caracteres est tombee le 17/11 sur
        # deux lignes de commentaire ajoutees, et celle-ci faisait 170.
        f = fen.find("\n- ", i)
        puce = fen[i:f if f != -1 else len(fen)]
        for sto, verre in GRILLE_M6[p]:
            if sto + " Go" not in puce:
                ecarts.append("le prompt n'apparie pas %s à %s Go" % (p, sto))
            # le verre n'est EXIGE que la ou il DISCRIMINE, c'est-a-dire la ou un meme prix
            # porte plusieurs variantes : ailleurs le prompt n'a pas a le nommer.
            if len(GRILLE_M6[p]) > 1 and MOT_VERRE[verre] not in puce:
                ecarts.append("le prompt n'apparie pas %s au verre %s" % (p, verre))
    for p in PRIX_US:
        if p.replace(" ", ",") not in fen:
            ecarts.append("$%s absent du prompt" % p.replace(" ", ","))
except Exception as e:                                        # noqa: BLE001
    ecarts.append("prompt illisible : %s" % e)
borne("㉕ la grille du contrôle et les faits du prompt disent la même chose", ecarts == [],
      "écarts=%r" % (ecarts,))

# ㉖ le garde du harnais lit-il la ligne que ce temoin imprime ? (defaut du 04/11, ancre ASCII)
m_sed = re.search(r'LU_FL=\$\(sed -n "([^"]+)"', io.open(NR_SH, encoding="utf-8").read())
lu = ""
if m_sed:
    lu = subprocess.run(["sed", "-n", m_sed.group(1)], input=LIGNE % (26, 27),
                        capture_output=True, text=True).stdout.strip()
borne("㉖ le motif du harnais, appliqué à la ligne que ce témoin imprime, rend le DÉNOMINATEUR",
      bool(m_sed) and lu == "27", "motif=%s · lu=%r (27 attendu)" % (bool(m_sed), lu))

for f in (FAUX, BON):
    os.unlink(f)
os.rmdir(tmp)
# ㉗ le temoin ne laisse RIEN derriere lui : 330 dossiers /tmp fuités par un temoin du 17/11.
borne("㉗ aucun dossier temporaire laissé", not os.path.isdir(tmp), "reste %s" % tmp)
print(LIGNE % (len(jouees) - len(ko), len(jouees)))
sys.exit(1 if ko else 0)
