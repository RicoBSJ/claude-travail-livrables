#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LES QUATRE FAITS ACQUIS DE LA SERIE iMac SONT-ILS VERSES AU PROMPT, ET BIEN APPARIES ? — 22/11/2026.

POURQUOI. Le 22/11/2026, deux faits JUSTES se sont defaits dans la meme journee, sur la meme serie.
① Le prix US de lancement : la fiche du 15/11 portait « $1,499 » au degre ① (MacRumors 06/11) ; le
document du creneau de 8h03 a ecrit « 1 299 $ », chiffre ABSENT des deux articles — mesure, `1,299`
a zero occurrence, et l'article 9to5Mac du 27/10 ne contient qu'UN SEUL « $ », qui est `1,499`.
② La reference a 2 219 € : le document de 8h03 l'avait JUSTE (« 256 Go · 4 ports + nano-texture ») ;
le rattrapage de 14h10 l'a republiee en « 512 Go », quand le comparateur ecrit 34 FOIS
`M6 12 coeurs, 16 Go, SSD 256 Go, 4 ports USB, Argent, Mat` a 2 219,00 €. Ce qui distingue cette
reference n'est pas le stockage, c'est le verre nano-texture.
③ Et la cause commune des « noms non retrouves » du matin est la RACINE DE SITE : l'edition du
15/11 citait les deux ARTICLES, celle du 22/11 a cite `macrumors.com` et `9to5mac.com` tout court —
une page d'accueil du 22/11 ne porte pas un fait publie le 27/10 ni le 06/11.

⛔ ET AUCUN CONTROLE DU DEPOT NE VOIT LA CLASSE : les trois axes de controle_edition_precedente.py
surveillent un defaut CORRIGE QUI REVIENT, jamais une justesse QUI SE DEFAIT. Une consigne ecrite
dans une fiche n'est pas un garde — lecon du 20/11, payee une seconde fois le 22/11 sur imac.

📊 LES FAITS SONT MESURES AU DEGRE ① LE 22/11/2026, pages aspirees et appariees litteralement :
MacRumors 06/11 ecrit `The iMac with M6 starts at $1,499 for the model with a 10-core CPU and
10-core GPU, while the version with a 12-core CPU and 12-core GPU starts at $1,699. Education
pricing starts at $1,449.` ; consomac.fr/comparateur/mac/imac-m6 ecrit `iMac 24" Retina 4,5K 2026,
M6 12 coeurs, 16 Go, SSD 256 Go, 4 ports USB, Argent, Mat … 2 219,00 €` et un revendeur detaille
`CPU 12 coeurs, GPU 12 coeurs, SSD de 256 Go, ecran Retina, Verre nano-texture`.

⛔ ON EXIGE LE LITTERAL, ET C'EST DIT : prouver l'EFFET demanderait de lancer le job — claude -p, du
reseau, et un plafond consomme a 99 %. Meme parti que le garde ② de l'assertion de tableau (18/10),
que desarmement_git.py (27/10) et que lettres_article5.py (21/11). Ce que ce temoin garde est que
les faits sont PRESENTS, dans la section lue en premier, correctement APPARIES, et qu'ils ne se
sont pas transformes en PROCEDURE.

⛔ LE PREDICAT EST STRUCTUREL, JAMAIS UN ID NI UN COMPTE EN DUR : « les prompts qui suivent l'iMac
ET les tout-en-un ». Un id fige perime a la premiere suppression de job, ce qui a bloque TOUS les
pushs les 15, 22 et 23/10. Mesure du jour : 1 prompt sur 6, et les deux chaines du predicat
PREEXISTAIENT au bloc verse (premiere phrase du prompt) — le predicat n'est pas satisfait par lui.

⛔ LES EXIGENCES SONT POSITIVES. On ne teste PAS l'absence de « 1 299 $ » ni celle de « 512 Go » :
ce temoin, le bloc du prompt et la consignation ecrivent tous les trois ces chaines pour en parler,
et un garde negatif se mord lui-meme — defaut du 17/10 sur « run: new TextRun ». Le garde du piege
512 Go est donc l'APPARIEMENT de 2 219 € a « nano-texture », pas l'absence de « 512 Go ».

Aucun reseau. Aucun fichier du depot dans le verdict des bornes : les prompts sont FABRIQUES.
"""
import json, os, re, subprocess, sys, tempfile

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # outils/scripts
# le bug de tolerance_page_morte.py (23/10) et de controle_integrite_livrables.py (11/11) :
# un dirname de trop ou de moins et tout ce qui suit mesure a cote. On l'assied sur un fait.
NR_SH = os.path.join(RACINE, "non_regression.sh")
assert os.path.isfile(NR_SH), "RACINE fausse : %s n'existe pas" % NR_SH

TITRE_FENETRE = "## ⚠️ FAITS ACQUIS"
ART_MR = "https://www.macrumors.com/2026/11/06/ipad-mini-oled-and-m6-imac-available-today/"
ART_95 = "https://9to5mac.com/2026/10/27/apple-launches-new-imac-with-powerful-m6-chip/"

# ── les faits mesures : la reference vit ICI, le prompt est la donnee verifiee ───────────────
# (designation, sujet) : le sujet doit vivre ENTRE sa designation et la SUIVANTE.
TABLE = [("**$1,499**",  "10 cœurs"),
         ("**$1,699**",  "12 cœurs"),
         ("**$1,449**",  "éducation"),
         ("**1 799 €**", "10c / 10c"),
         ("**2 219 €**", "nano-texturé"),
         (ART_MR,        "06/11/2026"),
         (ART_95,        "27/10/2026")]
PHRASES = ["La configuration d'entrée de gamme France est en 10 cœurs CPU et 10 cœurs GPU",
           "La référence à 2 219 € est la variante à VERRE NANO-TEXTURÉ, SSD 256 Go",
           "cite l'ARTICLE daté, jamais la racine du site"]
OUTILS = ["chercher.py", "aspirer.py", "lire_page.py", "WebSearch", "WebFetch", "curl ",
          "controle_"]


def predicat(p):
    """Les prompts qui suivent l'iMac ET les tout-en-un."""
    return "iMac" in p and "tout-en-un" in p


def fenetre(p):
    """La section lue en premier, bornee STRUCTURELLEMENT : du titre au prochain « ## »."""
    a = p.find(TITRE_FENETRE)
    if a == -1:
        return None
    m = re.search(r"\n## ", p[a + len(TITRE_FENETRE):])
    return p[a:a + len(TITRE_FENETRE) + m.start()] if m else p[a:]


def manques(f):
    """Ce qui manque dans la fenetre : appariements, phrases, et procedure interdite."""
    out, pos = [], {}
    for d, _ in TABLE:
        i = f.find(d)
        if i == -1:
            out.append("la désignation %s est absente de la section" % d)
        pos[d] = i
    # le sujet doit vivre ENTRE sa propre designation et la SUIVANTE : une simple presence des
    # deux chaines quelque part dans la section ne prouve AUCUN appariement (borne ④).
    for k, (d, sujet) in enumerate(TABLE):
        i = pos[d]
        if i == -1:
            continue
        suivantes = [pos[x] for x, _ in TABLE[k + 1:] if pos[x] > i]
        fin = min(suivantes) if suivantes else len(f)
        if sujet.lower() not in f[i:fin].lower():
            out.append("%s n'est pas apparié à « %s » (sujet absent entre %s et la désignation "
                       "suivante)" % (d, sujet, d))
    for ph in PHRASES:
        if ph not in f:
            out.append("la section ne porte pas « %s »" % ph)
    for t in OUTILS:
        if t in f:
            out.append("la section lue en premier appelle un outil (%s) : c'est un FAIT qu'elle "
                       "porte, pas une procédure — un tour de plus coûte ~1,5 %% sur ce job" % t)
    return out


def verdict(config):
    d = json.load(open(config, encoding="utf-8"))
    vus = pb = 0
    for j in d["jobs"]:
        if not predicat(j["prompt"]):
            continue
        vus += 1
        f = fenetre(j["prompt"])
        if f is None:
            print("  ✗ %s : aucune section « %s » — les faits ne seraient pas lus en premier"
                  % (j["id"], TITRE_FENETRE))
            pb += 1
            continue
        for m in manques(f):
            print("  ✗ %s : %s" % (j["id"], m))
            pb += 1
    print("  FAITS ACQUIS DE LA SERIE IMAC : %d prompt(s) concerné(s) · %d écart(s)" % (vus, pb))
    if not vus:
        print("  ⓘ aucun prompt ne suit l'iMac et les tout-en-un : garde inerte, et il le dit")
    return 1 if pb else 0


# L'AIGUILLAGE EST ICI, AVANT LES BORNES : les bornes ⑬ et ⑭ relancent ce fichier en
# sous-processus pour jouer le VRAI verdict() de bout en bout. Place plus bas, il ferait jouer les
# bornes dans chaque sous-processus, donc une recursion sans fin.
if "--verdict" in sys.argv:
    sys.exit(verdict(sys.argv[sys.argv.index("--verdict") + 1]))

# ══════════════════════════════════ auto-test ═══════════════════════════════════════════════
LIGNE = "  %d/%d bornes des faits acquis de la serie imac"
jouees, ko = [], []
def borne(nom, cond, detail=""):
    jouees.append(nom)
    if not cond:
        ko.append(nom)
        print("  ✗ %s%s" % (nom, (" — " + detail) if detail else ""))


def bloc_juste():
    return (
        "\n\nCes quatre faits sont MESURÉS au degré ① le 22/11/2026. Ils ne sont pas à "
        "re-chercher : ils sont à RECOPIER.\n\n"
        "- Prix US de lancement de l'iMac M6 (MacRumors, 06/11/2026) : **$1,499** pour le modèle "
        "à 10 cœurs CPU et 10 cœurs GPU · **$1,699** pour celui à 12 cœurs CPU et 12 cœurs GPU · "
        "**$1,449** en tarif éducation.\n"
        "- **La configuration d'entrée de gamme France est en 10 cœurs CPU et 10 cœurs GPU** : "
        "**1 799 €** = M6 10c / 10c · 16 Go · 256 Go · 2 ports USB.\n"
        "- **La référence à 2 219 € est la variante à VERRE NANO-TEXTURÉ, SSD 256 Go** : "
        "**2 219 €** = M6 12c/12c · 16 Go · 256 Go · 4 ports USB · verre nano-texturé.\n"
        "- Pour les spécifications de la puce M6, cite l'ARTICLE daté, jamais la racine du site :\n"
        "  %s (06/11/2026)\n  %s (27/10/2026)\n" % (ART_MR, ART_95))


def prompt_fab(bloc, dans_fenetre=True, predicat_ok=True, titre=True):
    tete = ("Expert du marché des ordinateurs de bureau tout-en-un, iMac compris.\n\n"
            if predicat_ok else "Veille quelconque sur un sujet sans rapport.\n\n")
    if titre:
        tete += TITRE_FENETRE + " AU 22/11/2026 — À LIRE AVANT TOUT"
        if dans_fenetre:
            tete += bloc
    return tete + "\n\n## Étape 1 — Vérification des doublons\n\nTexte de l'étape." + (
        "" if (dans_fenetre and titre) else "\n" + bloc)


def config_fab(prompt):
    d = {"jobs": [{"id": "imac-veille", "prompt": prompt},
                  {"id": "autre-veille", "prompt": "Veille sans rapport."}]}
    f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
    json.dump(d, f, ensure_ascii=False)
    f.close()
    return f.name


def joue_verdict(cfg):
    r = subprocess.run([sys.executable, os.path.abspath(__file__), "--verdict", cfg],
                       capture_output=True, text=True)
    return r.returncode, r.stdout


JUSTE = prompt_fab(bloc_juste())

# ① le predicat selectionne, et il PREEXISTE au bloc : la tete seule le satisfait deja.
borne("① le prédicat tient sans le bloc", predicat(prompt_fab("", titre=False)) and
      predicat(JUSTE))
# ② ACCEPTEE : un prompt hors predicat est ignore, bloc ou pas.
borne("② hors prédicat, le garde se taît (ACCEPTÉE)",
      not predicat(prompt_fab("", predicat_ok=False, titre=False)))
# ③ la fenetre est STRUCTURELLE : elle s'arrete au prochain « ## », jamais a un nombre de
#    caracteres — une fenetre en dur est tombee le 17/11 sur deux lignes de commentaire ajoutees.
f = fenetre(JUSTE)
borne("③ fenêtre structurelle", f is not None and "Étape 1" not in f and "$1,499" in f,
      "fenêtre=%r" % (f[:40] if f else None))
# ④ ACCEPTEE : le bloc juste ne manque de rien.
borne("④ le bloc juste passe (ACCEPTÉE)", manques(f) == [], "manques=%r" % (manques(f),))
# ⑤ APPARIEMENT, pas presence : les deux sujets echanges, les quatre chaines toujours la.
ech = bloc_juste().replace("10 cœurs CPU et 10 cœurs GPU · **$1,699** pour celui à 12 cœurs",
                           "12 cœurs CPU et 12 cœurs GPU · **$1,699** pour celui à 10 cœurs")
m5 = manques(fenetre(prompt_fab(ech)))
borne("⑤ sujets échangés → refus", any("$1,499" in x and "apparié" in x for x in m5),
      "manques=%r" % (m5,))
# ⑥ une designation absente est NOMMEE.
m6 = manques(fenetre(prompt_fab(bloc_juste().replace("**$1,449**", "en tarif réduit"))))
borne("⑥ désignation absente nommée", any("$1,449" in x and "absente" in x for x in m6),
      "manques=%r" % (m6,))
# ⑦ le sujet deplace APRES la designation suivante ne compte pas.
dep = bloc_juste().replace("**1 799 €** = M6 10c / 10c · 16 Go", "**1 799 €** = M6 · 16 Go")
dep = dep.replace("verre nano-texturé.", "verre nano-texturé, à comparer au 10c / 10c.")
m7 = manques(fenetre(prompt_fab(dep)))
borne("⑦ sujet déplacé après la désignation suivante → refus",
      any("1 799 €" in x and "apparié" in x for x in m7), "manques=%r" % (m7,))
# ⑧ ACCEPTEE : de la prose entre la designation et son sujet ne gene pas.
pr = bloc_juste().replace("**1 799 €** = M6 10c / 10c",
                          "**1 799 €**, prix conseillé inchangé depuis le M4, = M6 10c / 10c")
borne("⑧ prose intercalaire acceptée (ACCEPTÉE)", manques(fenetre(prompt_fab(pr))) == [],
      "manques=%r" % (manques(fenetre(prompt_fab(pr))),))
# ⑨ une PHRASE manquante est nommee.
m9 = manques(fenetre(prompt_fab(bloc_juste().replace(
    "cite l'ARTICLE daté, jamais la racine du site", "cite une source"))))
borne("⑨ phrase manquante nommée", any("racine du site" in x for x in m9), "manques=%r" % (m9,))
# ⑩ un appel d'outil dans la section lue en premier est refuse : un fait se recopie, une
#    procedure se paie — et ce job vient de consommer 99 % de son plafond.
m10 = manques(fenetre(prompt_fab(bloc_juste() + "\n- Vérifie avec `chercher.py` avant d'écrire.\n")))
borne("⑩ outil dans la section → refus", any("appelle un outil" in x for x in m10),
      "manques=%r" % (m10,))
# ⑪ le bloc pose APRES « ## Étape 1 » n'est pas dans la fenetre.
m11 = manques(fenetre(prompt_fab(bloc_juste(), dans_fenetre=False)))
borne("⑪ bloc hors fenêtre → refus", len(m11) >= 7, "manques=%d" % len(m11))
# ⑫ pas de section du tout : message propre, et pas un plantage.
borne("⑫ aucune section → fenetre None", fenetre(prompt_fab(bloc_juste(), titre=False)) is None)
# ⑬ ACCEPTEE : le VRAI verdict() de bout en bout sur une config fabriquee juste.
cfg = config_fab(JUSTE)
rc, out = joue_verdict(cfg)
borne("⑬ verdict réel sur config juste → 0 (ACCEPTÉE)",
      rc == 0 and "1 prompt(s) concerné(s) · 0 écart(s)" in out, "rc=%d out=%r" % (rc, out[-200:]))
# ⑭ le VRAI verdict() sur une config cassee → 1, et il NOMME le job.
cfg2 = config_fab(prompt_fab(bloc_juste().replace("**2 219 €**", "2 219 euros")))
rc2, out2 = joue_verdict(cfg2)
borne("⑭ verdict réel sur config cassée → 1 et nomme le job",
      rc2 == 1 and "imac-veille" in out2 and "2 219 €" in out2, "rc=%d out=%r" % (rc2, out2[-200:]))
# ⑮ LE PIEGE DU 22/11 : 2 219 € apparie a « 512 Go » au lieu du verre nano-texture.
#    C'est l'APPARIEMENT qui l'attrape, pas l'absence de « 512 Go » (exigence POSITIVE).
p512 = bloc_juste().replace("**2 219 €** = M6 12c/12c · 16 Go · 256 Go · 4 ports USB · verre "
                            "nano-texturé.", "**2 219 €** = M6 12c/12c · 16 Go · 512 Go · "
                            "4 ports USB.")
m15 = manques(fenetre(prompt_fab(p512)))
borne("⑮ piège 512 Go → refus par appariement",
      any("2 219 €" in x and "nano-texturé" in x and "apparié" in x for x in m15),
      "manques=%r" % (m15,))
# ⑯ LE PIEGE DES RACINES : citer macrumors.com et 9to5mac.com tout court est refuse, et le
#    message nomme l'ARTICLE attendu.
rac = bloc_juste().replace(ART_MR, "https://www.macrumors.com").replace(
    ART_95, "https://9to5mac.com")
m16 = manques(fenetre(prompt_fab(rac)))
borne("⑯ racines de site → refus nommant l'article",
      any(ART_MR in x and "absente" in x for x in m16) and
      any(ART_95 in x and "absente" in x for x in m16), "manques=%r" % (m16,))
# ⑰ le garde du harnais lit-il vraiment la ligne que ce temoin imprime ? (defaut du 04/11)
#    L'ancre est ASCII SANS ACCENT, et on applique le sed DU HARNAIS, lu dans le fichier, jamais
#    recopie : une derive de libelle dans les DEUX cotes laisserait le lot vert (regle du 15/10,
#    repayee le 11/11 sur ma borne ⑩ de categories_hook.py).
m_sed = re.search(r'LU_FI=\$\(sed -n "([^"]+)"', open(NR_SH, encoding="utf-8").read())
lu = ""
if m_sed:
    lu = subprocess.run(["sed", "-n", m_sed.group(1)], input=LIGNE % (17, 18),
                        capture_output=True, text=True).stdout.strip()
borne("⑰ le motif du harnais, appliqué à la ligne que ce témoin imprime, rend le DÉNOMINATEUR",
      bool(m_sed) and lu == "18", "motif=%s · lu=%r (18 attendu)" % (bool(m_sed), lu))
# ⑱ ACCEPTEE : la config sans aucun prompt concerne le DIT, au lieu de rendre un vert muet.
cfg3 = config_fab("Veille sans rapport avec le matériel.")
rc3, out3 = joue_verdict(cfg3)
borne("⑱ aucun prompt concerné : le garde le dit (ACCEPTÉE)",
      rc3 == 0 and "garde inerte" in out3, "rc=%d out=%r" % (rc3, out3[-160:]))

for c in (cfg, cfg2, cfg3):
    os.unlink(c)
print(LIGNE % (len(jouees) - len(ko), len(jouees)))
sys.exit(1 if ko else 0)
