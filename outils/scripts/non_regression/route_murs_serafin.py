#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LA ROUTE D'ARCHIVE DES DEUX PAGES MUREES DE handicap.gouv.fr EST-ELLE VERSEE AU PROMPT, ET
BIEN APPARIEE ? — 28/11/2026.

POURQUOI. handicap.gouv.fr sert un gabarit anti-automate AVANT le routage sur ses pages de comite
strategique : `curl` et `aspirer.py` y rendent HTTP 200 · 93 caracteres utiles, texte « Please
enable javascript to view the page content. Your support ID is: … », et l'outil de recuperation de
page du job ne franchit pas davantage ce mur. L'etape 1 bis du prompt prescrit pourtant de
recuperer « la page de la reunion la plus recente » : le job y recolte donc 93 caracteres, sans
repli. Mesure du 20/11/2026 : un 404 de ce meme hote repond 200 derriere ce gabarit, donc un 200
de cet hote ne prouve NI que la page existe, NI qu'elle porte ce qu'on lui attribue.

⛔ ET AUCUNE CONSIGNE N'A TENU. La fiche du 11/11 avait trouve la route d'archive (5 761 car.
utiles) ; l'edition du 18/11 l'a reperdue et a refait le travail par une autre route ; la fiche du
18/11 a prescrit quatre verifications a l'edition suivante, et celle du 25/11 — ecrite A LA MAIN —
en a enfreint une : elle a marque le mur `✅` au lieu de `⚠`. C'est la regle du 21/11 (« une
consigne ecrite dans une fiche n'est pas un garde ») payee une troisieme fois, et le mecanisme est
nomme depuis le 09/11 : LE JOB RELIT LA NOTE, JAMAIS LA FICHE.

📊 LA ROUTE EST MESUREE LE 28/11/2026, et c'est ce qui la rend versable : les deux instantanes du
10/08/2026 rendent 5 861 et 7 332 caracteres utiles a `aspirer.py` — au-dessus du plancher de
3 000 du depot — et les 18 formulations lues au navigateur le 25/11 y reviennent TOUTES au degre ①
ou ②. Les deux ④ du premier essai venaient de la requete (un article de trop, une apostrophe
droite), troisieme occurrence de ce motif.

⛔ ON EXIGE LE LITTERAL, ET C'EST DIT : prouver l'EFFET demanderait de lancer le job — claude -p, du
reseau et un plafond a 5 $. Meme parti que le garde ② de l'assertion de tableau (18/10), que
desarmement_git.py (27/10), lettres_article5.py (21/11) et faits_imac.py (22/11). Ce que ce temoin
garde est que la route est PRESENTE, dans la section lue en premier, correctement APPARIEE, et
qu'elle ne s'est pas transformee en PROCEDURE.

⛔ LE PREDICAT EST STRUCTUREL, JAMAIS UN ID NI UN COMPTE EN DUR : « les prompts qui suivent
SERAFIN-PH ET les comites strategiques ». Un id fige perime a la premiere suppression de job, ce
qui a bloque TOUS les pushs les 15, 22 et 23/10. Mesure du jour : 1 prompt sur 6 — et les deux
chaines du predicat PREEXISTAIENT au bloc verse (premiere phrase du prompt pour l'une, etape 1 bis
pour l'autre), donc le predicat n'est pas satisfait par lui. La conjonction est mesuree NECESSAIRE :
`controle-livrables` porte « SERAFIN-PH » sans porter « comite strategique » (borne ②).

⛔ LES EXIGENCES SONT POSITIVES. On ne teste PAS l'absence de « 93 caracteres » ni celle d'un `✅` :
ce temoin, le bloc du prompt et la consignation ecrivent tous les trois ces chaines pour en parler,
et un garde negatif se mord lui-meme — defaut du 17/10 sur « run: new TextRun ». Le garde du piege
est donc l'APPARIEMENT de chaque compte a la page qui le rend.

⚠️ ET LA LISTE DES OUTILS INTERDITS DANS LA SECTION EXCLUT VOLONTAIREMENT `WebFetch` ET
`aspirer.py`, parce que le bloc les nomme comme CE QUI NE MARCHE PAS — c'est un fait, pas une
instruction. Les interdire ferait refuser le bloc qu'on protege : meme piege que la coquille citee
qui s'immunise elle-meme (27/10), pris par l'autre bout. Ce qui est interdit est ce qui
signalerait une derive vers la procedure et qui est ABSENT aujourd'hui, donc une borne qui PEUT
echouer (borne ⑩).

Aucun reseau. Aucun fichier du depot dans le verdict des bornes : les prompts sont FABRIQUES.
"""
import json, os, re, subprocess, sys, tempfile

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # outils/scripts
# le bug de tolerance_page_morte.py (23/10), coherence_skill.py (27/10) et
# controle_integrite_livrables.py (11/11) : un dirname de trop ou de moins et tout ce qui suit
# mesure a cote, en rendant un VERT. On l'assied sur un fait.
NR_SH = os.path.join(RACINE, "non_regression.sh")
assert os.path.isfile(NR_SH), "RACINE fausse : %s n'existe pas" % NR_SH

TITRE_FENETRE = "## ⚠️ FAIT ACQUIS — LES DEUX PAGES DE COMITÉ"
ARCH_14 = ("https://web.archive.org/web/20260810045044/https://handicap.gouv.fr/"
           "reforme-tarifaire-des-esms-serafin-ph-14e-reunion-du-comite-strategique")
ARCH_13 = ("https://web.archive.org/web/20260810043921/https://handicap.gouv.fr/"
           "reforme-tarifaire-des-esms-serafin-ph-reunion-du-comite-strategique")

# ── la reference vit ICI, le prompt est la donnee verifiee ───────────────────────────────────
# (designation, sujet) DANS L'ORDRE DU DOCUMENT : le sujet doit vivre ENTRE sa designation et la
# SUIVANTE. « les deux chaines sont quelque part dans la section » est satisfait par l'incident
# lui-meme — c'est l'appariement qui porte tout (borne ⑤).
# ⚠️ UN SUJET NE PEUT PAS ETRE LA DESIGNATION SUIVANTE : la fenetre d'appariement s'arrete a
#    celle-ci, donc apparier une URL a « 5 861 » quand « **5 861 caracteres utiles.** » EST la
#    designation suivante accuse un bloc JUSTE. Defaut de mon premier jet, dit par la borne ⑤ —
#    qui doit etre ACCEPTEE — et non par la relecture. L'appariement porte donc sur
#    TITRE → HORODATAGE puis COMPTE → NOM, et les deux URL completes sont exigees au LITTERAL.
TABLE = [("**HTTP 200 · 93 caractères utiles**",                        "Please enable JavaScript"),
         ("### ① 14e réunion du comité stratégique",                    "20260810045044"),
         ("**5 861 caractères utiles.**",                               "Camille Galliard-Minier"),
         ("### ② Réunion du comité stratégique du 18 novembre 2025",    "20260810043921"),
         ("**7 332 caractères utiles.**",                               "Charlotte Parmentier-Lecocq"),
         ("**six critères**",                                           "usage du numérique")]
# presence au LITTERAL, pas appariement : un horodatage echange rend ces deux chaines absentes.
LITTERAUX = [ARCH_14, ARCH_13]
PHRASES = ["UN 200 DE CET HÔTE NE PROUVE DONC RIEN",
           "CITE L'ADRESSE VIVANTE, PAS CELLE DE L'ARCHIVE",
           "MARQUE CES DEUX LIGNES `⚠️`, JAMAIS `✅`",
           "La date du **23 mars 2026** est une DÉDUCTION"]
# absents du bloc aujourd'hui, et chacun signalerait une derive vers la procedure (cf. docstring)
OUTILS = ["WebSearch", "chercher.py", "lire_page.py", "--dossier", "allowed_domains"]


def predicat(p):
    """Les prompts qui suivent SERAFIN-PH ET les comités stratégiques."""
    return "SERAFIN-PH" in p and bool(re.search(r"comit[ée]\s+strat[ée]gique", p, re.I))


def fenetre(p):
    """La section lue en premier, bornée STRUCTURELLEMENT : du titre au prochain « ## »."""
    a = p.find(TITRE_FENETRE)
    if a == -1:
        return None
    m = re.search(r"\n## ", p[a + len(TITRE_FENETRE):])
    return p[a:a + len(TITRE_FENETRE) + m.start()] if m else p[a:]


def avant_etapes(p):
    """« Lue en premier » se VERIFIE : le titre doit precéder la première « ## Étape ».

    🔴 TROUVE PAR LE SABOTAGE S3, PAS PAR LA RELECTURE : deplacer la section ENTIERE — titre
    compris — apres l'etape 1 laissait le garde vert, parce que fenetre() trouve son titre ou
    qu'il soit et que la fenetre court alors jusqu'a la fin du prompt. Le bloc etait complet et
    appariE, mais lu en DERNIER. Le garde revendiquait « la section lue en premier » sans jamais
    le mesurer — meme classe que « un recensement textuel n'est pas un recensement d'appels »
    (27/10) : une revendication n'est pas une verification.
    """
    a = p.find(TITRE_FENETRE)
    m = re.search(r"\n## Étape", p)
    return a != -1 and (m is None or a < m.start())


def manques(f):
    """Ce qui manque dans la fenêtre : appariements, phrases, et procédure interdite."""
    out, pos = [], {}
    for d, _ in TABLE:
        i = f.find(d)
        if i == -1:
            out.append("la désignation %s est absente de la section" % d[:70])
        pos[d] = i
    for k, (d, sujet) in enumerate(TABLE):
        i = pos[d]
        if i == -1:
            continue
        suivantes = [pos[x] for x, _ in TABLE[k + 1:] if pos[x] > i]
        fin = min(suivantes) if suivantes else len(f)
        if sujet.lower() not in f[i:fin].lower():
            out.append("%s n'est pas apparié à « %s » (sujet absent entre cette désignation et "
                       "la suivante)" % (d[:70], sujet))
    for u in LITTERAUX:
        if u not in f:
            out.append("l'URL d'archive %s est absente de la section au littéral" % u)
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
            print("  ✗ %s : aucune section « %s » — la route ne serait pas lue en premier"
                  % (j["id"], TITRE_FENETRE))
            pb += 1
            continue
        if not avant_etapes(j["prompt"]):
            print("  ✗ %s : la section existe mais vient APRÈS la première « ## Étape » — elle "
                  "n'est donc PAS lue en premier" % j["id"])
            pb += 1
        for m in manques(f):
            print("  ✗ %s : %s" % (j["id"], m))
            pb += 1
    print("  ROUTE D ARCHIVE DES MURS SERAFIN : %d prompt(s) concerné(s) · %d écart(s)" % (vus, pb))
    if not vus:
        print("  ⓘ aucun prompt ne suit SERAFIN-PH et les comités : garde inerte, et il le dit")
    return 1 if pb else 0


# L'AIGUILLAGE EST ICI, AVANT LES BORNES : les bornes ⑬ et ⑭ relancent ce fichier en
# sous-processus pour jouer le VRAI verdict() de bout en bout. Place plus bas, il ferait jouer les
# bornes dans chaque sous-processus, donc une recursion sans fin.
if "--verdict" in sys.argv:
    sys.exit(verdict(sys.argv[sys.argv.index("--verdict") + 1]))

# ══════════════════════════════════ auto-test ═══════════════════════════════════════════════
LIGNE = "  %d/%d bornes de la route d archive des murs serafin"
jouees, ko = [], []


def borne(nom, cond, detail=""):
    jouees.append(nom)
    if not cond:
        ko.append(nom)
        print("  ✗ %s%s" % (nom, (" — " + detail) if detail else ""))


def bloc_juste():
    return (
        "\n\n⛔ **CECI EST UN FAIT À RECOPIER, PAS UNE PROCÉDURE.**\n\n"
        "🔴 **LE PROBLÈME, MESURÉ** : `handicap.gouv.fr` sert un gabarit anti-automate AVANT le "
        "routage. Les outils de lecture y rendent **HTTP 200 · 93 caractères utiles**, avec le "
        "texte « Please enable JavaScript to view the page content. Your support ID is: … ». "
        "⚠️ **UN 200 DE CET HÔTE NE PROUVE DONC RIEN** — le 20/11/2026, un 404 de ce même hôte a "
        "répondu 200 derrière ce gabarit.\n\n"
        "### ① 14e réunion du comité stratégique — réunion du 23 mars 2026\n\n%s\n\n"
        "**5 861 caractères utiles.** Elle porte, au littéral : « Camille Galliard-Minier » · "
        "« financement des transports dans la dotation globale ». ⚠️ La date du **23 mars 2026** "
        "est une DÉDUCTION : la page écrit « Ce lundi ».\n\n"
        "### ② Réunion du comité stratégique du 18 novembre 2025\n\n%s\n\n"
        "**7 332 caractères utiles.** Elle porte, au littéral : « Charlotte Parmentier-Lecocq » · "
        "« les ESMS connaîtront leur dotation théorique » · et les **six critères** de la dotation "
        "complémentaire, nommés : « complexité des situations », « usage du numérique ».\n\n"
        "⛔ **DANS LA NOTE, CITE L'ADRESSE VIVANTE, PAS CELLE DE L'ARCHIVE.**\n\n"
        "⛔ **ET MARQUE CES DEUX LIGNES `⚠️`, JAMAIS `✅`, EN DONNANT LE COMPTE.**\n\n"
        % (ARCH_14, ARCH_13))


def prompt_fab(bloc, dans_fenetre=True, predicat_ok=True, titre=True):
    tete = ("Veille hebdomadaire SERAFIN-PH.\n\nCherche le comité stratégique le plus récent.\n\n"
            if predicat_ok else "Veille quelconque sur un sujet sans rapport.\n\n")
    if titre:
        tete += TITRE_FENETRE + " DE handicap.gouv.fr SONT MURÉES (28/11/2026)"
        if dans_fenetre:
            tete += bloc
    return tete + "\n\n## Étape 1 — Vérification des doublons\n\nTexte de l'étape." + (
        "" if (dans_fenetre and titre) else "\n" + bloc)


def config_fab(prompt):
    d = {"jobs": [{"id": "serafin-ph-veille", "prompt": prompt},
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

# ① le predicat tient SANS le bloc : les deux chaines preexistent, il n'est pas satisfait par lui.
borne("① le prédicat tient sans le bloc", predicat(prompt_fab("", titre=False)) and
      predicat(JUSTE))
# ② ACCEPTEE : la CONJONCTION discrimine. Un prompt qui porte « SERAFIN-PH » sans porter
#    « comité stratégique » est ignoré — c'est le cas mesuré de controle-livrables.
borne("② SERAFIN-PH seul ne suffit pas (ACCEPTÉE)",
      not predicat("Relis les livrables de la semaine, veille SERAFIN-PH comprise."))
# ③ ACCEPTEE : un prompt hors predicat est ignore, bloc ou pas.
borne("③ hors prédicat, le garde se taît (ACCEPTÉE)",
      not predicat(prompt_fab("", predicat_ok=False, titre=False)))
# ④ la fenetre est STRUCTURELLE : du titre au prochain « ## », jamais un nombre de caracteres —
#    une fenetre en dur est tombee le 17/11 sur deux lignes de commentaire ajoutees.
f = fenetre(JUSTE)
borne("④ fenêtre structurelle", f is not None and "Étape 1" not in f and ARCH_14 in f,
      "fenêtre=%r" % (f[:40] if f else None))
# ⑤ ACCEPTEE : le bloc juste ne manque de rien.
borne("⑤ le bloc juste passe (ACCEPTÉE)", manques(f) == [], "manques=%r" % (manques(f),))
# ⑥ APPARIEMENT, pas presence : les DEUX MINISTRES echanges, les quatre chaines toujours la.
#    C'est l'erreur reelle a redouter — les deux intitules de portefeuille DIFFERENT.
ech = bloc_juste().replace("« Camille Galliard-Minier »", "« Charlotte Parmentier-Lecocq »", 1)
ech = ech.replace("**7 332 caractères utiles.** Elle porte, au littéral : "
                  "« Charlotte Parmentier-Lecocq »",
                  "**7 332 caractères utiles.** Elle porte, au littéral : "
                  "« Camille Galliard-Minier »")
m6 = manques(fenetre(prompt_fab(ech)))
borne("⑥ ministres échangés → refus par appariement",
      any("5 861" in x and "Camille" in x and "apparié" in x for x in m6), "manques=%r" % (m6,))
# ⑦ les deux HORODATAGES d'archive echanges : les URL completes ne s'apparient plus au littéral,
#    et la borne NOMME les deux. C'est l'erreur de copier-coller la plus probable.
inv = bloc_juste().replace("20260810045044", "@A@").replace("20260810043921", "20260810045044")
inv = inv.replace("@A@", "20260810043921")
m7 = manques(fenetre(prompt_fab(inv)))
borne("⑦ horodatages d'archive échangés → refus nommant les deux URL",
      sum(1 for x in m7 if "web.archive.org" in x and "absente" in x) == 2 and
      any("20260810045044" in x and "apparié" in x for x in m7), "manques=%r" % (m7,))
# ⑧ un compte altere est NOMME : 5 861 remplace par le compte de l'autre page.
m8 = manques(fenetre(prompt_fab(bloc_juste().replace("**5 861 caractères utiles.**",
                                                     "**7 332 caractères utiles.**"))))
borne("⑧ compte altéré nommé", any("5 861" in x for x in m8), "manques=%r" % (m8,))
# ⑨ ACCEPTEE : de la prose entre la designation et son sujet ne gene pas.
pr = bloc_juste().replace("**5 861 caractères utiles.** Elle porte",
                          "**5 861 caractères utiles.** Instantané du 10/08/2026. Elle porte")
borne("⑨ prose intercalaire acceptée (ACCEPTÉE)", manques(fenetre(prompt_fab(pr))) == [],
      "manques=%r" % (manques(fenetre(prompt_fab(pr))),))
# ⑩ une derive vers la PROCEDURE est refusee : un fait se recopie, une procedure se paie — et
#    chaque tour coute ~3,3 % sur ce job (mesure du 31/10). ⚠️ `WebFetch` et `aspirer.py` ne sont
#    PAS dans la liste : le bloc les nomme comme ce qui NE MARCHE PAS (cf. docstring).
m10 = manques(fenetre(prompt_fab(
    bloc_juste() + "\n- Relance une WebSearch avec allowed_domains avant d'écrire.\n")))
borne("⑩ dérive vers la procédure → refus", any("appelle un outil" in x for x in m10),
      "manques=%r" % (m10,))
# ⑪ ACCEPTEE : nommer l'outil qui NE franchit pas le mur reste un FAIT, et passe.
ok = bloc_juste().replace("Les outils de lecture y rendent",
                          "`curl`, `aspirer.py` et `WebFetch` y rendent")
borne("⑪ nommer l'outil qui échoue reste un fait (ACCEPTÉE)",
      manques(fenetre(prompt_fab(ok))) == [], "manques=%r" % (manques(fenetre(prompt_fab(ok))),))
# ⑫ une PHRASE manquante est nommee : celle du marquage ⚠, c'est-a-dire la consigne du 18/11 que
#    l'edition du 25/11 a enfreinte.
m12 = manques(fenetre(prompt_fab(bloc_juste().replace(
    "ET MARQUE CES DEUX LIGNES `⚠️`, JAMAIS `✅`, EN DONNANT LE COMPTE.",
    "ET MARQUE CES DEUX LIGNES COMME IL CONVIENT."))))
borne("⑫ phrase du marquage manquante nommée",
      any("JAMAIS `✅`" in x for x in m12), "manques=%r" % (m12,))
# ⑬ le bloc pose APRES « ## Étape 1 » n'est pas dans la fenetre : l'emplacement compte.
m13 = manques(fenetre(prompt_fab(bloc_juste(), dans_fenetre=False)))
borne("⑬ bloc hors fenêtre → refus", len(m13) >= 10, "manques=%d" % len(m13))
# ⑭ pas de section du tout : message propre, et pas un plantage.
borne("⑭ aucune section → fenetre None", fenetre(prompt_fab(bloc_juste(), titre=False)) is None)
# ⑮ ACCEPTEE : le VRAI verdict() de bout en bout sur une config fabriquee juste.
cfg = config_fab(JUSTE)
rc, out = joue_verdict(cfg)
borne("⑮ verdict réel sur config juste → 0 (ACCEPTÉE)",
      rc == 0 and "1 prompt(s) concerné(s) · 0 écart(s)" in out, "rc=%d out=%r" % (rc, out[-200:]))
# ⑯ le VRAI verdict() sur une config cassee → 1, et il NOMME le job.
cfg2 = config_fab(prompt_fab(bloc_juste().replace(ARCH_13, "https://handicap.gouv.fr/x")))
rc2, out2 = joue_verdict(cfg2)
borne("⑯ verdict réel sur config cassée → 1 et nomme le job",
      rc2 == 1 and "serafin-ph-veille" in out2 and "web.archive.org" in out2,
      "rc=%d out=%r" % (rc2, out2[-200:]))
# ⑰ le garde du harnais lit-il vraiment la ligne que ce temoin imprime ? (defaut du 04/11)
#    L'ancre est ASCII SANS ACCENT, et on applique le sed DU HARNAIS, LU dans le fichier, jamais
#    recopie : une derive de libelle dans les DEUX cotes laisserait le lot vert (regle du 15/10).
m_sed = re.search(r'LU_RM=\$\(sed -n "([^"]+)"', open(NR_SH, encoding="utf-8").read())
lu = ""
if m_sed:
    lu = subprocess.run(["sed", "-n", m_sed.group(1)], input=LIGNE % (20, 21),
                        capture_output=True, text=True).stdout.strip()
borne("⑰ le motif du harnais, appliqué à la ligne que ce témoin imprime, rend le DÉNOMINATEUR",
      bool(m_sed) and lu == "21", "motif=%s · lu=%r (21 attendu)" % (bool(m_sed), lu))
# ⑲ « lue en premier » est VERIFIE : la section deplacee APRES l'etape 1 est refusee, et la
#    ⑲bis — ACCEPTEE — exige que l'ordre normal passe. Borne nee du sabotage S3 (28/11).
def deplace(p):
    i, j = p.find(TITRE_FENETRE), p.find("## Étape 1 — Vérification des doublons")
    return p[:i] + p[j:] + "\n\n" + p[i:j]
borne("⑲ section déplacée après l'étape 1 → refus", not avant_etapes(deplace(JUSTE)))
borne("⑲bis l'ordre normal passe (ACCEPTÉE)", avant_etapes(JUSTE))
# ⑳ le VRAI verdict() de bout en bout sur une config dont la section est deplacee.
cfg4 = config_fab(deplace(JUSTE))
rc4, out4 = joue_verdict(cfg4)
borne("⑳ verdict réel sur section déplacée → 1 et le dit",
      rc4 == 1 and "lue en premier" in out4, "rc=%d out=%r" % (rc4, out4[-200:]))
# ⑱ ACCEPTEE : la config sans aucun prompt concerne le DIT, au lieu de rendre un vert muet.
cfg3 = config_fab("Veille sans rapport avec le financement médico-social.")
rc3, out3 = joue_verdict(cfg3)
borne("⑱ aucun prompt concerné : le garde le dit (ACCEPTÉE)",
      rc3 == 0 and "garde inerte" in out3, "rc=%d out=%r" % (rc3, out3[-160:]))

for c in (cfg, cfg2, cfg3, cfg4):
    os.unlink(c)
print(LIGNE % (len(jouees) - len(ko), len(jouees)))
sys.exit(1 if ko else 0)
