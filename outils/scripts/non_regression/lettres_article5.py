#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LES LETTRES DE L'ARTICLE 5 §1 SONT-ELLES VERSEES AU PROMPT, ET BIEN APPARIEES ? — 21/11/2026.

POURQUOI. Deux editions de la serie ai-act se sont trompees sur ces lettres. Le 13/11/2026
ecrivait « lit. h » et « lit. i », faux ET inverses sur le contenu. Le 15/11/2026 les avait
justes (« lit. ba/bb ») et sa fiche demandait noir sur blanc de les reconduire. Le 20/11/2026 a
produit un tableau de dix interdictions dont SEPT bases legales etaient fausses — une chaine
inventee « d · e · e bis · e ter · e quater » et « f » / « g » donnes aux deux interdictions du
2 decembre 2026, lettres que l'article attribue a la reconnaissance des emotions au travail et a
la classification biometrique. Le document a ete corrige le 21/11/2026 ; ce bloc versé au prompt
est ce qui evite la troisieme occurrence.

⛔ ET AUCUN CONTROLE DU DEPOT NE VOIT LA CLASSE : les trois axes de controle_edition_precedente.py
surveillent un defaut CORRIGE QUI REVIENT, jamais une formulation JUSTE REMPLACEE PAR UNE FAUSSE.
Une consigne ecrite dans une fiche n'est pas un garde — c'est la lecon du 20/11.

📊 LA TABLE EST MESUREE AU DEGRE ① LE 21/11/2026 sur artificialintelligenceact.eu/prohibited-ai-
practices/, qui numerote lui-meme sa liste : « 4) Prevision des infractions commises par des
individus (article 5, paragraphe 1, point d)) », « 5) Collecte non ciblee d'images faciales
(... point e)) », « 6) Reconnaissance des emotions au travail et dans l'enseignement (... point
f)) », « 7) Classification biometrique fondee sur des caracteristiques sensibles (... point g)) »,
« 8) Identification biometrique a distance en temps reel (... point h)) » ; puis « Le point (ba)
interdit les systemes » et « Le point (bb) interdit les systemes ».

⛔ ON EXIGE LE LITTERAL, ET C'EST DIT : prouver l'EFFET demanderait de lancer le job — claude -p,
du reseau, et un plafond deja a 97 %. Meme parti que le garde ② de l'assertion de tableau (18/10)
et que desarmement_git.py (27/10). Ce que ce temoin garde est que le FAIT est present, dans la
section lue en premier, correctement apparie, et qu'il ne s'est pas transforme en PROCEDURE.

⛔ LE PREDICAT EST STRUCTUREL, JAMAIS UN ID NI UN COMPTE EN DUR : « les prompts qui parlent de
l'AI Act ET de ses pratiques interdites ». Un id figé perime a la premiere suppression de job, ce
qui a bloque TOUS les pushs les 15, 22 et 23/10. Mesure du jour : 1 prompt sur 6, et les deux
chaines du predicat PREEXISTAIENT au bloc verse — le predicat n'est donc pas satisfait par lui.

⛔ LES EXIGENCES SONT POSITIVES. On ne teste PAS l'absence de « e bis » : ce temoin, le bloc du
prompt et la consignation ecrivent tous les trois cette chaine pour en parler, et un garde negatif
se mord lui-meme — c'est le defaut du 17/10 sur « run: new TextRun », corrige ce jour-la en
exigeant la PRESENCE de la bonne forme.

Aucun reseau. Aucun fichier du depot dans le verdict des bornes : les prompts sont FABRIQUES.
"""
import json, os, re, subprocess, sys, tempfile

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # outils/scripts
# le bug de tolerance_page_morte.py (23/10) et de controle_integrite_livrables.py (11/11) :
# un dirname de trop ou de moins et tout ce qui suit mesure a cote. On l'assied sur un fait.
NR_SH = os.path.join(RACINE, "non_regression.sh")
assert os.path.isfile(NR_SH), "RACINE fausse : %s n'existe pas" % NR_SH
DEPOT = os.path.dirname(os.path.dirname(RACINE))

TITRE_FENETRE = "## ⚠️ ÉTAT DU DOSSIER"
# ── la table mesuree : la reference vit ICI, le prompt est la donnee verifiee ────────────────
TABLE = [("a", "manipulation subliminale"),
         ("b", "exploitation de vulnérabilités"),
         ("c", "notation sociale"),
         ("d", "prévision des infractions"),
         ("e", "collecte non ciblée d'images faciales"),
         ("f", "reconnaissance des émotions"),
         ("g", "classification biométrique"),
         ("h", "identification biométrique à distance en temps réel")]
NOUVEAUX = [("ba", "hypertrucages sexuels non consentis"),
            ("bb", "contenus pédocriminels")]
PHRASES = ["Il n'existe aucun point e bis, e ter ni e quater",
           "(f) et (g) ne sont pas libres"]
OUTILS = ["chercher.py", "aspirer.py", "lire_page.py", "WebSearch", "WebFetch", "curl ",
          "controle_"]


def predicat(p):
    """Les prompts qui parlent de l'AI Act ET de ses pratiques interdites."""
    return "AI Act" in p and "pratiques interdites" in p


def fenetre(p):
    """La section lue en premier, bornee STRUCTURELLEMENT : du titre au prochain « ## »."""
    a = p.find(TITRE_FENETRE)
    if a == -1:
        return None
    m = re.search(r"\n## ", p[a + len(TITRE_FENETRE):])
    return p[a:a + len(TITRE_FENETRE) + m.start()] if m else p[a:]


def designation(lettre):
    return "**(%s)**" % lettre if len(lettre) > 1 else "**%s)**" % lettre


def manques(f):
    """Ce qui manque dans la fenetre : appariements, phrases, et procedure interdite."""
    out = []
    paires = TABLE + NOUVEAUX
    pos = {}
    for lettre, _ in paires:
        d = designation(lettre)
        i = f.find(d)
        if i == -1:
            out.append("la désignation %s est absente de la section" % d)
        pos[lettre] = i
    # le sujet doit vivre ENTRE sa propre designation et la SUIVANTE : une simple presence des
    # deux chaines quelque part dans la section ne prouve AUCUN appariement (borne ⑦).
    for k, (lettre, sujet) in enumerate(paires):
        i = pos[lettre]
        if i == -1:
            continue
        suivantes = [pos[l] for l, _ in paires[k + 1:] if pos[l] > i]
        fin = min(suivantes) if suivantes else len(f)
        if sujet.lower() not in f[i:fin].lower():
            out.append("%s n'est pas apparié à « %s » (sujet absent entre %s et la désignation "
                       "suivante)" % (designation(lettre), sujet, designation(lettre)))
    for ph in PHRASES:
        if ph not in f:
            out.append("la section ne porte pas « %s »" % ph)
    for t in OUTILS:
        if t in f:
            out.append("la section lue en premier appelle un outil (%s) : c'est un FAIT qu'elle "
                       "porte, pas une procédure — un tour de plus coûte ~3,3 %% sur ce job" % t)
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
            print("  ✗ %s : aucune section « %s » — le fait ne serait pas lu en premier"
                  % (j["id"], TITRE_FENETRE))
            pb += 1
            continue
        for m in manques(f):
            print("  ✗ %s : %s" % (j["id"], m))
            pb += 1
    print("  LETTRES DE L ARTICLE 5 : %d prompt(s) concerné(s) · %d écart(s)" % (vus, pb))
    if not vus:
        print("  ⓘ aucun prompt ne parle de l'AI Act et de ses pratiques interdites : garde inerte,"
              " et il le dit")
    return 1 if pb else 0


# L'AIGUILLAGE EST ICI, AVANT LES BORNES : les bornes ⑬ et ⑭ relancent ce fichier en
# sous-processus pour jouer le VRAI verdict() de bout en bout. Place plus bas, il ferait jouer les
# bornes dans chaque sous-processus, donc une recursion sans fin.
if "--verdict" in sys.argv:
    sys.exit(verdict(sys.argv[sys.argv.index("--verdict") + 1]))

# ══════════════════════════════════ auto-test ═══════════════════════════════════════════════
LIGNE = "  %d/%d bornes des lettres de l article 5"
jouees, ko = [], []
def borne(nom, cond, detail=""):
    jouees.append(nom)
    if not cond:
        ko.append(nom)
        print("  ✗ %s%s" % (nom, (" — " + detail) if detail else ""))


def bloc_juste():
    lignes = ["- Les huit interdictions applicables depuis le 2 février 2025 sont les points "]
    lignes += ["%s %s · " % (designation(l), s) for l, s in TABLE]
    lignes += ["\n- Les deux interdictions du 2 décembre 2026 sont les points "]
    lignes += ["%s — %s — " % (designation(l), s) for l, s in NOUVEAUX]
    lignes += ["\n- ⛔ **%s, et %s**\n" % (PHRASES[0], PHRASES[1])]
    return "".join(lignes)


def prompt_fab(bloc, dans_fenetre=True, predicat_ok=True):
    tete = "AI Act — veille.\n\n" if predicat_ok else "Veille quelconque.\n\n"
    tete += TITRE_FENETRE + " AU 30/08/2026\n\n- sanctions : 35 M€ ou 7 % pour les "
    tete += ("pratiques interdites" if predicat_ok else "amendes") + ".\n"
    if dans_fenetre:
        tete += bloc
    return tete + "\n## Étape 1 — doublons\n\nTexte de l'étape." + ("" if dans_fenetre else
                                                                    "\n" + bloc)


# ① la table elle-meme
lettres = [l for l, _ in TABLE + NOUVEAUX]
borne("① la table mesurée porte 10 désignations, a à h puis ba et bb, chacune une seule fois",
      lettres == ["a", "b", "c", "d", "e", "f", "g", "h", "ba", "bb"]
      and len(set(lettres)) == 10, "lettres=%r" % lettres)

# ② la fenetre est bornee STRUCTURELLEMENT
p2 = prompt_fab(bloc_juste())
f2 = fenetre(p2)
borne("② la section est bornée au prochain « ## », pas à un nombre de caractères",
      f2 is not None and "Étape 1" not in f2 and "classification biométrique" in f2,
      "fenetre=%r" % (f2 or "")[-40:])

# ③ ACCEPTEE : le bloc juste ne declenche rien
borne("③ ACCEPTÉE : la section qui porte la table juste n'a AUCUN écart",
      manques(fenetre(prompt_fab(bloc_juste()))) == [],
      "manques=%r" % manques(fenetre(prompt_fab(bloc_juste()))))

# ④ d et h echanges — l'incident du 20/11
ech = bloc_juste().replace("**d)** prévision des infractions",
                           "**d)** identification biométrique à distance en temps réel") \
                  .replace("**h)** identification biométrique à distance en temps réel",
                           "**h)** prévision des infractions")
m4 = manques(fenetre(prompt_fab(ech)))
borne("④ d et h échangés — l'incident du 20/11 — sont REFUSÉS, et le message nomme la lettre",
      any("**d)**" in x for x in m4) and any("**h)**" in x for x in m4), "manques=%r" % m4)

# ⑤ la chaine inventee « e bis »
ebis = bloc_juste().replace("**e)** collecte non ciblée d'images faciales",
                            "**e bis)** collecte non ciblée d'images faciales")
m5 = manques(fenetre(prompt_fab(ebis)))
borne("⑤ la chaîne inventée e bis est REFUSÉE (la désignation **e)** disparaît)",
      any("**e)**" in x for x in m5), "manques=%r" % m5)

# ⑥ (f) et (g) donnes aux deux nouvelles interdictions
fg = bloc_juste().replace("**(ba)** — hypertrucages", "**(f)** — hypertrucages") \
                 .replace("**(bb)** — contenus pédocriminels", "**(g)** — contenus pédocriminels")
m6 = manques(fenetre(prompt_fab(fg)))
borne("⑥ (f) et (g) donnés aux deux interdictions du 2 décembre sont REFUSÉS, ba et bb nommés",
      any("(ba)" in x for x in m6) and any("(bb)" in x for x in m6), "manques=%r" % m6)

# ⑦ LA BORNE DECISIVE : le sujet apres la designation SUIVANTE ne vaut pas appariement
# le sujet de d) est deplace APRES la designation **e)**, donc hors de sa propre plage :
# les deux chaines sont bien dans la section, et pourtant rien n'apparie d) a son sujet.
dep = bloc_juste().replace("**d)** prévision des infractions", "**d)**") \
                  .replace("**f)** reconnaissance", "prévision des infractions **f)** reconnaissance")
m7 = manques(fenetre(prompt_fab(dep)))
borne("⑦ un sujet déplacé APRÈS la désignation suivante est REFUSÉ : la présence des deux "
      "chaînes quelque part ne prouve aucun appariement",
      any("**d)**" in x for x in m7), "manques=%r" % m7)

# ⑧ ACCEPTEE : de la prose intercalaire ne gene pas
pro = bloc_juste().replace("**d)** prévision",
                           "**d)** (lire les lignes directrices) prévision")
borne("⑧ ACCEPTÉE : de la prose entre la désignation et son sujet n'est PAS un écart",
      manques(fenetre(prompt_fab(pro))) == [],
      "manques=%r" % manques(fenetre(prompt_fab(pro))))

# ⑨ le bloc hors de la section lue en premier
m9 = manques(fenetre(prompt_fab(bloc_juste(), dans_fenetre=False)))
borne("⑨ la table posée HORS de la section lue en premier est REFUSÉE",
      len(m9) >= 10, "%d manque(s)" % len(m9))

# ⑩ ACCEPTEE : un prompt hors predicat n'est pas accuse
borne("⑩ ACCEPTÉE : un prompt qui ne parle pas de l'AI Act et de ses pratiques interdites "
      "n'est pas concerné",
      not predicat(prompt_fab(bloc_juste(), predicat_ok=False))
      and predicat(prompt_fab(bloc_juste())), "")

# ⑪ la section ne doit pas devenir une PROCEDURE (preventif, et c'est dit)
m11 = manques(fenetre(prompt_fab(bloc_juste() + "- vérifie-les par chercher.py avant d'écrire.\n")))
borne("⑪ un appel d'outil dans la section lue en premier est REFUSÉ (préventif : 0 occurrence "
      "aujourd'hui)", any("chercher.py" in x for x in m11), "manques=%r" % m11)

# ⑫ les deux phrases d'interdiction
m12 = manques(fenetre(prompt_fab(bloc_juste().replace(PHRASES[0], "Les lettres sont celles-là"))))
borne("⑫ la phrase qui dit qu'aucun point e bis n'existe est EXIGÉE au littéral",
      any(PHRASES[0] in x for x in m12), "manques=%r" % m12)

# ⑬ et ⑭ : le VRAI verdict(), de bout en bout, sur des configs FABRIQUEES
def lance(bloc):
    cfg = {"jobs": [{"id": "temoin", "prompt": prompt_fab(bloc)},
                    {"id": "hors-sujet", "prompt": "Veille matériel, rien sur le règlement."}]}
    fd, path = tempfile.mkstemp(suffix=".json"); os.close(fd)
    json.dump(cfg, open(path, "w", encoding="utf-8"), ensure_ascii=False)
    r = subprocess.run([sys.executable, os.path.abspath(__file__), "--verdict", path],
                       capture_output=True, text=True)
    os.unlink(path)
    return r.returncode, r.stdout


c_ok, s_ok = lance(bloc_juste())
borne("⑬ bout en bout : le VRAI verdict() ACCEPTE la config juste, exit 0, et compte 1 prompt",
      c_ok == 0 and "1 prompt(s) concerné(s) · 0 écart(s)" in s_ok,
      "exit=%d · sortie=%r" % (c_ok, s_ok.strip()[-90:]))
c_ko, s_ko = lance(ech)
borne("⑭ bout en bout : le VRAI verdict() REFUSE la config fautive, exit 1, en nommant la lettre",
      c_ko == 1 and "**d)**" in s_ko, "exit=%d · sortie=%r" % (c_ko, s_ko.strip()[-90:]))

# ⑮ le garde du harnais lit-il vraiment la ligne que ce temoin imprime ? (defaut du 04/11)
#    L'ancre est ASCII SANS ACCENT : la derive d'un libelle accentue a fait refuser tous les
#    pushs le 04/11. On applique le sed DU HARNAIS, lu dans le fichier, jamais recopie.
m_sed = re.search(r'LU_A5=\$\(sed -n "([^"]+)"', open(NR_SH, encoding="utf-8").read())
lu = ""
if m_sed:
    lu = subprocess.run(["sed", "-n", m_sed.group(1)], input=LIGNE % (14, 15),
                        capture_output=True, text=True).stdout.strip()
borne("⑮ le motif du harnais, appliqué à la ligne que ce témoin imprime, rend le DÉNOMINATEUR",
      bool(m_sed) and lu == "15", "motif=%s · lu=%r (15 attendu)" % (bool(m_sed), lu))

print(LIGNE % (len(jouees) - len(ko), len(jouees)))
sys.exit(1 if ko else 0)
