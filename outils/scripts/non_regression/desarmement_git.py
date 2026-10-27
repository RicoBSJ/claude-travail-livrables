#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""desarmement_git.py — les trois scripts qui appellent `git` désarment-ils l'environnement
que `git push` leur transmet, et le font-ils AVANT leur premier appel à `git` ?

POURQUOI (27/10/2026). `git push` exporte GIT_DIR à ses hooks — et depuis que `.git` est un
fichier d'une ligne pointant hors de l'arbre, ce chemin est ABSOLU : un `cd` n'isole plus rien.
Mesuré pendant un push : le dépôt jetable du runner résolvait vers LE VRAI DÉPÔT, `git init
--bare` y a posé `core.bare = true` et `git config` l'identité de test, et le `reset --hard` /
`clean -qfdx` du témoin S14 visait l'arbre réel. Rien n'a été détruit par DEUX accidents.
Les trois fichiers portent depuis un `unset` des huit variables.

🔴 CE QUE CE TÉMOIN GARDE, ET POURQUOI IL A FALLU L'ÉCRIRE : **aucun témoin du dépôt ne peut
   exercer un désarmement dans le sens conforme.** Mesuré, pas raisonné : aucun script du dépôt
   ne POSE GIT_DIR (`grep "GIT_DIR=\\|export GIT_" non_regression.sh non_regression_runner.sh`
   → zéro, le `GIT_SSH_COMMAND` excepté), donc le harnais lance toujours ses témoins dans un
   environnement déjà propre, où retirer les trois `unset` ne change RIEN. Seul le lancement
   DEPUIS LE HOOK les exerce, et ce lancement n'est pas un témoin. D'où une borne de PRÉSENCE,
   du même type que le garde ② de l'assertion de tableau (18/10) : on ne peut pas prouver
   l'effet, on peut exiger la ligne — et exiger qu'elle soit au bon endroit.

⚠️ L'ORDRE EST LA MOITIÉ DE LA RÈGLE, et c'est un défaut mesuré, pas une précaution : le 27/10
   le `unset` du hook était posé APRÈS `ROOT="$(git rev-parse --show-toplevel)"`. Avec un GIT_DIR
   pointant ailleurs, `rev-parse` échouait, ROOT était vide, et le hook refusait le push en
   annonçant « un verdict a changé » — un motif FAUX. Une borne de présence seule l'aurait
   déclaré conforme. D'où ③ : le `unset` précède le PREMIER appel à `git` du fichier.

⚠️ CE QUE CETTE BORNE NE PEUT PAS VOIR, et il faut le dire :
   • elle est TEXTUELLE. Un `unset` placé dans un `if` qui ne se déclenche jamais, ou un `git`
     bâti dans une variable (`G=git; $G push`), y échapperaient. Les trois fichiers l'écrivent
     en littéral, c'est mesuré, et c'est la seule forme que le dépôt emploie.
   • elle exige CETTE forme : un `env -u GIT_DIR …` équivalent serait refusé. Coût assumé —
     une forme unique est ce qui rend la borne lisible.
   • elle ne prouve pas que le désarmement SERVE : elle prouve qu'il est là et qu'il est premier.

Les commentaires sont NEUTRALISÉS avant toute recherche (remplacés par des blancs de même
longueur, donc les positions restent celles du fichier) : les trois fichiers PARLENT de git
dans leurs commentaires d'en-tête — c'est l'état réel, et la borne ⑬ l'épingle.

Aucun réseau, aucun tiers : ce témoin ne peut donc pas périmer sur la panne d'un site, la
leçon des 15, 22 et 23/10.
Usage : python3 outils/scripts/non_regression/desarmement_git.py
Sortie : 0 si les treize bornes tiennent, 1 sinon.
"""
import os, re, sys, tempfile

# ⚠️ QUATRE dirname — ce script vit un cran plus bas que les contrôles (piège du 23/10, où
#    trois dirname rendaient toutes les bornes vertes sur des fichiers absents). La borne ①
#    le vérifie AVANT tout le reste.
RACINE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))

# ⛔ `non_regression.sh` N'EST PAS DANS CETTE LISTE, ET C'EST VOULU : ses deux appels à git
#    (le `git status` du témoin de supprimer_job.sh, le `git diff` des documents) VISENT le vrai
#    dépôt à dessein. On désarme là où l'isolation est requise — le runner, le push de run_job.sh,
#    le hook qui lance les deux — et on garde là où une réponse du vrai dépôt est attendue. Un
#    `unset` posé dans le harnais y aurait masqué son propre détecteur : c'est lui qui a prouvé,
#    le 27/10, que le hook désarme bien (sans GIT_DIR il imprime 5/5, avec il crie « codes 128 »).
FICHIERS = ("outils/scripts/run_job.sh",
            "outils/scripts/non_regression_runner.sh",
            "outils/scripts/hooks/pre-push")

# Les huit que `git` exporte à ses hooks (GIT_PREFIX et GIT_QUARANTINE_PATH compris : le
# premier décale les chemins relatifs, le second détourne la base d'objets d'un pre-receive).
VARS = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
        "GIT_COMMON_DIR", "GIT_QUARANTINE_PATH", "GIT_ALTERNATE_OBJECT_DIRECTORIES",
        "GIT_PREFIX")

# `unset` en tête de ligne, continuations « \ » comprises : le hook l'écrit sur DEUX lignes.
# 🔴 ET LA PREMIÈRE FORME DE CE MOTIF A ÉTÉ PRISE PAR SA PROPRE BORNE ⑦ : écrit
# `[^\n]*(?:\\\n[^\n]*)*`, il s'arrêtait à la fin de la PREMIÈRE ligne — le groupe de
# continuation pouvant matcher ZÉRO fois, rien ne forçait le retour arrière qui aurait rendu
# le « \ » final. Il lisait donc 5 variables sur 8 dans le hook RÉEL, et déclarait son
# désarmement incomplet. D'où la forme ci-dessous : une suite de caractères qui ne sont PAS
# un « \ », ou de paires « \ + saut de ligne ». Un groupe optionnel ne provoque aucun retour
# arrière : c'est la borne qui doit être ACCEPTÉE qui l'a dit, pas la relecture.
RE_UNSET = re.compile(r"^[ \t]*unset[ \t](?:[^\n\\]|\\\n)*", re.M)
# Un appel à git en position de commande : ni `--git-dir`, ni `GIT_SSH_COMMAND`, ni `.git`.
RE_GIT = re.compile(r"(?<![\w./-])git(?=[ \t])")
# Un réarmement : une AFFECTATION de l'une des huit, après le désarmement.
RE_REARME = re.compile(r"(?<![\w])(?:export[ \t]+)?(GIT_(?:DIR|WORK_TREE|INDEX_FILE|"
                       r"OBJECT_DIRECTORY|COMMON_DIR|QUARANTINE_PATH|"
                       r"ALTERNATE_OBJECT_DIRECTORIES|PREFIX))=")


def sans_commentaires(src):
    """Les lignes de commentaire deviennent des blancs DE MÊME LONGUEUR : les positions
    rendues restent celles du fichier, donc comparables entre elles."""
    return "\n".join(" " * len(l) if l.lstrip().startswith("#") else l
                     for l in src.split("\n"))


def lire(racine, rel):
    """Le dossier de l'état d'un fichier. `present=False` si on n'a rien pu lire : un verdict
    vert sur un fichier qu'on n'a pas ouvert est le défaut du 26/10, on ne le refait pas."""
    etat = {"rel": rel, "present": False, "unset": None, "manquantes": list(VARS),
            "pos_unset": None, "pos_git": None, "rearme": []}
    try:
        with open(os.path.join(racine, rel), encoding="utf-8") as f:
            src = f.read()
    except OSError:
        return etat
    etat["present"] = True
    code = sans_commentaires(src)
    # Le `unset` retenu est le PREMIER qui nomme au moins une des huit : un `unset FOO`
    # quelconque ailleurs dans le script ne doit pas être pris pour le désarmement.
    for m in RE_UNSET.finditer(code):
        noms = set(re.findall(r"GIT_[A-Z_]+", m.group(0)))
        if noms & set(VARS):
            etat["unset"] = m.group(0)
            etat["manquantes"] = [v for v in VARS if v not in noms]
            etat["pos_unset"] = m.start()
            break
    g = RE_GIT.search(code)
    etat["pos_git"] = g.start() if g else None
    if etat["pos_unset"] is not None:
        etat["rearme"] = [m.group(1) for m in RE_REARME.finditer(code[etat["pos_unset"]:])]
    return etat


def verifier(racine):
    """Rend la liste des (fichier, motif). Vide = les trois sont conformes."""
    pb = []
    for rel in FICHIERS:
        e = lire(racine, rel)
        if not e["present"]:
            pb.append((rel, "ILLISIBLE — rien n'a été lu, donc rien n'est prouvé"))
            continue
        if e["pos_unset"] is None:
            pb.append((rel, "AUCUN désarmement : pas de `unset` nommant les variables de git"))
            continue
        if e["manquantes"]:
            pb.append((rel, "désarmement INCOMPLET — manque : %s" % ", ".join(e["manquantes"])))
        if e["pos_git"] is None:
            pb.append((rel, "AUCUN appel à `git` hors commentaire — l'ordre serait vrai sur du "
                            "vide ; si ce script n'appelle plus git, retire-le de FICHIERS"))
        elif e["pos_unset"] > e["pos_git"]:
            pb.append((rel, "désarmement posé APRÈS le premier `git` (offsets %d > %d) — c'est "
                            "le défaut du hook du 27/10, et il refusait le push sur un motif faux"
                            % (e["pos_unset"], e["pos_git"])))
        if e["rearme"]:
            pb.append((rel, "RÉARMEMENT après le désarmement : %s" % ", ".join(e["rearme"])))
    return pb


# ─────────────────────────── le lot de bornes ───────────────────────────
CONFORME = """#!/bin/sh
# en-tête qui PARLE de git push et de GIT_DIR, comme les trois vrais fichiers
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_OBJECT_DIRECTORY GIT_COMMON_DIR GIT_QUARANTINE_PATH GIT_ALTERNATE_OBJECT_DIRECTORIES GIT_PREFIX
git status
"""


def _arbre(variantes):
    """Une arborescence FABRIQUÉE portant les trois chemins — rien de vivant dans le verdict
    (leçon du 22/10 : un compte pris sur le dépôt réel périme tout seul). `variantes` remplace
    le contenu d'un ou plusieurs fichiers ; les autres sont conformes."""
    d = tempfile.mkdtemp(prefix="desarm")
    for rel in FICHIERS:
        chemin = os.path.join(d, rel)
        os.makedirs(os.path.dirname(chemin), exist_ok=True)
        contenu = variantes.get(rel, CONFORME)
        if contenu is None:          # fichier volontairement ABSENT
            continue
        with open(chemin, "w", encoding="utf-8") as f:
            f.write(contenu)
    return d


def controler():
    ko, jouees = [], []

    def borne(nom, ok, detail=""):
        print("  %s %s%s" % ("✓" if ok else "✗", nom, (" — " + detail) if detail else ""))
        jouees.append(nom)
        if not ok:
            ko.append(nom)

    def fin():
        # ⚠️ Le DÉNOMINATEUR est le nombre de bornes réellement JOUÉES, et c'est lui que le
        #    harnais lit (ATTENDU_DES) : un « 13/13 » en dur laisserait passer un lot amputé.
        #    Deux gardes du dépôt sont tombés dans ce piège le 26/10 (ATTENDU_CB5, ATTENDU_CA).
        print("  %d/%d bornes du désarmement git" % (len(jouees) - len(ko), len(jouees)))
        return 1 if ko else 0

    # ① d'abord : si RACINE est fausse, tout le reste serait vert sur du vide.
    presents = [r for r in FICHIERS if os.path.isfile(os.path.join(RACINE, r))]
    borne("① RACINE est rendue — les trois fichiers sont là où ce témoin les cherche",
          len(presents) == len(FICHIERS),
          "%d/%d sous %s" % (len(presents), len(FICHIERS), RACINE))
    if len(presents) != len(FICHIERS):
        return fin()

    # ②③④⑤ — l'état RÉEL des trois fichiers du dépôt, aujourd'hui.
    etats = {r: lire(RACINE, r) for r in FICHIERS}
    inc = {r: e["manquantes"] for r, e in etats.items() if e["pos_unset"] is None or e["manquantes"]}
    borne("② les trois portent un `unset` nommant les HUIT variables de git",
          not inc,
          "; ".join("%s : %s" % (r.split("/")[-1], ", ".join(v) or "aucun unset")
                    for r, v in inc.items()) or "8/8 dans les trois")
    sans_git = [r for r, e in etats.items() if e["pos_git"] is None]
    borne("④ chacun appelle effectivement `git` hors commentaire (sinon ③ est vrai sur du vide)",
          not sans_git, ", ".join(sans_git) if sans_git else
          " · ".join("%s@%d" % (r.split("/")[-1], etats[r]["pos_git"]) for r in FICHIERS))
    tard = [r for r, e in etats.items()
            if e["pos_unset"] is not None and e["pos_git"] is not None
            and e["pos_unset"] > e["pos_git"]]
    borne("③ le désarmement PRÉCÈDE le premier `git` — le défaut du hook du 27/10",
          not tard, ", ".join(tard) if tard else
          " · ".join("%s : %d < %d" % (r.split("/")[-1], etats[r]["pos_unset"], etats[r]["pos_git"])
                     for r in FICHIERS))
    rearmes = {r: e["rearme"] for r, e in etats.items() if e["rearme"]}
    borne("⑤ aucun des trois ne RÉARME une des huit après le désarmement",
          not rearmes,
          "; ".join("%s : %s" % (r.split("/")[-1], ", ".join(v)) for r, v in rearmes.items())
          or "les trois sont propres")

    # ⑥→⑬ — le VRAI `verifier()` joué sur des arborescences fabriquées, les deux sens.
    def pbs(variantes, rel=None):
        d = _arbre(variantes)
        p = verifier(d)
        return [m for (f, m) in p if rel is None or f == rel]

    CIBLE = "outils/scripts/run_job.sh"
    borne("⑥ ACCEPTÉE : les trois conformes → aucun problème", pbs({}) == [],
          "; ".join(pbs({})) or "silence")

    # ⑦ la forme du hook RÉEL : `unset` sur deux lignes, continuation « \ ». Sans cette borne,
    #    un témoin plus strict refuserait le fichier qui est aujourd'hui dans le dépôt.
    deux = CONFORME.replace(
        "unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_OBJECT_DIRECTORY GIT_COMMON_DIR "
        "GIT_QUARANTINE_PATH",
        "unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_OBJECT_DIRECTORY GIT_COMMON_DIR \\\n"
        "      GIT_QUARANTINE_PATH")
    borne("⑦ ACCEPTÉE : `unset` coupé par une continuation « \\ » (la forme du hook réel)",
          "\\\n" in deux and pbs({CIBLE: deux}, CIBLE) == [],
          "; ".join(pbs({CIBLE: deux}, CIBLE)) or "silence")

    # ⑬ un `git` en COMMENTAIRE avant le `unset` ne doit pas refuser : c'est l'état réel des
    #    trois fichiers, dont les en-têtes racontent l'incident. C'est la borne qui sépare ce
    #    témoin d'une version naïve qui chercherait `git` sans neutraliser les commentaires.
    commente = "#!/bin/sh\n# git push exporte GIT_DIR, et git rev-parse échouerait\n" + \
               CONFORME.split("\n", 2)[2]
    borne("⑬ ACCEPTÉE : un `git` en commentaire AVANT le désarmement ne refuse pas",
          "# git push" in commente and pbs({CIBLE: commente}, CIBLE) == [],
          "; ".join(pbs({CIBLE: commente}, CIBLE)) or "silence")

    sans = pbs({CIBLE: CONFORME.replace(
        "unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_OBJECT_DIRECTORY GIT_COMMON_DIR "
        "GIT_QUARANTINE_PATH GIT_ALTERNATE_OBJECT_DIRECTORIES GIT_PREFIX\n", "")}, CIBLE)
    borne("⑧ `unset` RETIRÉ → refusé", any("AUCUN désarmement" in m for m in sans),
          "; ".join(sans) or "RIEN N'A ÉTÉ DIT")

    apres = CONFORME.replace("unset GIT_DIR", "#unset GIT_DIR") + \
            "unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_OBJECT_DIRECTORY " \
            "GIT_COMMON_DIR GIT_QUARANTINE_PATH GIT_ALTERNATE_OBJECT_DIRECTORIES GIT_PREFIX\n"
    tardif = pbs({CIBLE: apres}, CIBLE)
    borne("⑨ `unset` présent mais APRÈS le premier `git` → refusé (mon défaut du 27/10)",
          any("APRÈS le premier" in m for m in tardif),
          "; ".join(tardif) or "RIEN N'A ÉTÉ DIT")

    ampute = pbs({CIBLE: CONFORME.replace(" GIT_QUARANTINE_PATH", "")}, CIBLE)
    borne("⑩ une variable retirée de la liste → refusé, et la borne la NOMME",
          any("GIT_QUARANTINE_PATH" in m for m in ampute),
          "; ".join(ampute) or "RIEN N'A ÉTÉ DIT")

    muet = pbs({CIBLE: CONFORME.replace("git status", "echo rien")}, CIBLE)
    borne("⑪ plus aucun `git` hors commentaire → refusé (sinon ③ serait vrai sur du vide)",
          any("AUCUN appel" in m for m in muet), "; ".join(muet) or "RIEN N'A ÉTÉ DIT")

    absent = pbs({CIBLE: None}, CIBLE)
    borne("⑫ fichier ABSENT → refusé (le ✓ sur un fichier non lu, défaut du 26/10)",
          any("ILLISIBLE" in m for m in absent), "; ".join(absent) or "RIEN N'A ÉTÉ DIT")

    return fin()


if __name__ == "__main__":
    raise SystemExit(controler())
