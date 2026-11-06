#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Témoin : `rattrapage_jobs.sh --manques` distingue-t-il un run PUBLIÉ d'un run qui ne l'est pas ?

    python3 outils/scripts/non_regression/publication_run.py

POURQUOI (06/11/2026). Le créneau `imac-veille` du 25/10 est allé au bout — épilogue
`(code de sortie : 0, tentatives : 1)` —, a produit son livrable, l'a committé, et son push a
été refusé TROIS fois. `--manques` répondait « ✓ tracé » : il lisait la PRÉSENCE de l'épilogue
sans jamais lire ce que `run_job.sh` écrit APRÈS lui. ㊳ ne pouvait rien dire non plus, puisqu'il
juge l'EXÉCUTION — et l'exécution avait réussi. Entre « créneau perdu » et « job en échec », il
existait un troisième état que personne ne regardait : **run réussi, publication échouée**.
📊 Mesuré sur les 39 logs présents : 19 `✅ push OK`, 5 `Rien de nouveau à committer`,
2 `Job en erreur`, 0 `PAS DE PUBLICATION`, et **12 — 31 % — portent la ligne d'échec**, tous
avec un code de sortie 0, sur SEPT jobs du 07/10 au 04/11. Les douze portent trois fois
`pre-push : ✗ PUSH REFUSÉ` : la cause dominante est le HOOK, pas le transport.

CE QUE CE TÉMOIN GARDE, ET COMMENT.
  · Les quatre motifs et la fonction `publication()` sont EXTRAITS de `rattrapage_jobs.sh` et
    exécutés — jamais recopiés. Un test qui teste une COPIE de la logique ne garde rien (15/10).
  · Tous les logs sont FABRIQUÉS en `tempfile` : rien de vivant n'entre dans le verdict, donc
    ce lot ne peut pas se périmer sur un log purgé à 30 jours ni sur la panne d'un tiers —
    contrairement aux trois témoins qui ont bloqué TOUS les pushs les 15, 22 et 23/10.
  · SIX bornes doivent être ACCEPTÉES : les quatre autres états terminaux de `run_job.sh`, le
    rattrapage qui publie, et le log vide. Sans elles, rien n'empêche d'élargir le motif demain.
  · Aucun réseau, aucun appel à git, aucun tiers.
"""
import os
import re
import sys
import tempfile

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# ⚠️ 23/10/2026 — ce fichier vit UN CRAN PLUS BAS que les contrôles : QUATRE dirname, pas trois.
#    Et l'assertion ci-dessous a mordu au premier essai, sur MON compte de dirname : c'est
#    exactement le bug de tolerance_page_morte.py du 23/10, reproduit dans le commentaire qui
#    en avertissait. Un commentaire ne mesure rien ; l'assertion, si.
#    Copier l'arithmétique d'un autre contrôle a déjà fait partir des sondes sans faisceau, en
#    silence. L'assertion vaut mieux qu'un commentaire.
assert os.path.isdir(os.path.join(RACINE, "outils", "scripts")), RACINE
SCRIPT = os.path.join(RACINE, "outils", "scripts", "rattrapage_jobs.sh")
HOOK = os.path.join(RACINE, "outils", "scripts", "hooks", "pre-push")

src = open(SCRIPT, encoding="utf-8").read()
ko, jouees = [], []


def borne(num, libelle, ok):
    jouees.append(num)
    if not ok:
        ko.append("%s %s" % (num, libelle))


# ---- extraction ------------------------------------------------------------
motifs = {}
for nom in ("PUB_OK", "PUB_ECHEC", "PUB_HOOK", "PUB_RESEAU"):
    m = re.search(r"^%s = re\.compile\(.*$" % nom, src, re.M)
    if m:
        motifs[nom] = m.group(0)

m = re.search(r"^def publication\(logs\):\n(?:.*\n)*?(?=^\S)", src, re.M)
corps_pub = m.group(0) if m else ""

ns = {"re": re}
extrait = False
if len(motifs) == 4 and corps_pub.strip():
    try:
        exec("\n".join(motifs.values()) + "\n" + corps_pub, ns)
        extrait = "publication" in ns
    except SyntaxError as e:
        print("  ⚠️ le bloc extrait ne compile pas : %s" % e)

borne("①", "les quatre motifs PUB_* sont dans rattrapage_jobs.sh", len(motifs) == 4)
# ⚠️ Une extraction qui rend du VIDE ne lève aucune erreur (leçon du 24/10) : on exige que le
#    corps extrait mentionne PUB_ECHEC, sinon on aurait extrait une autre fonction, ou rien.
borne("②", "publication() est extraite, compile, et s'appuie sur PUB_ECHEC",
      extrait and "PUB_ECHEC" in corps_pub)
if not extrait:
    print("\n✗ extraction impossible — les bornes ③ à ⑭ ne peuvent pas être jouées.")
    print("  %d/%d borne(s) jouée(s)" % (len(jouees) - len(ko), len(jouees)))
    sys.exit(1)
publication = ns["publication"]

LIGNE_FIN = ("\n  %d/%d borne(s) jouée(s) — un run réussi dont le push échoue est NON PUBLIÉ, "
             "et les quatre autres états terminaux de run_job.sh sont des silences")

# ---- fabrication des logs --------------------------------------------------
EPILOGUE = "<<< 2026-10-25 08:15:11 — Fin du job imac-veille (code de sortie : 0, tentatives : 1)\n"
ECHEC = ("[git] ⛔ push ÉCHEC après 3 tentatives — 2 commit(s) en avance sur origin/main, "
         "à pousser manuellement (git push origin main).\n")
REFUS = "pre-push : ✗ PUSH REFUSÉ — un verdict a changé, un témoin ne sort plus en 1, ou (mode\n"
RESEAU = "Connection to github.com closed by remote host.\n"

tmp = tempfile.mkdtemp(prefix="temoin_publication_")


def log(nom, corps):
    chemin = os.path.join(tmp, nom)
    open(chemin, "w", encoding="utf-8").write(corps)
    return chemin


cas = {
    "pousse":     log("a_20261101_080300.log", EPILOGUE + "[git] ✅ push OK (tentative 1)\n"),
    "rien":       log("b_20261101_080300.log", EPILOGUE + "[git] Rien de nouveau à committer.\n"),
    "erreur":     log("c_20261101_080300.log", EPILOGUE + "[git] Job en erreur (exit 1) — pas de commit.\n"),
    "exit7":      log("d_20261101_080300.log", EPILOGUE + "[git] ⛔ PAS DE PUBLICATION — exit 0 non prouvé après un échec (voir [retry] ci-dessus).\n"),
    "hook":       log("e_20261101_080300.log", EPILOGUE + REFUS + REFUS + REFUS + ECHEC),
    "transport":  log("f_20261101_080300.log", EPILOGUE + RESEAU + ECHEC),
    "les_deux":   log("g_20261101_080300.log", EPILOGUE + REFUS + RESEAU + REFUS + ECHEC),
    "nu":         log("h_20261101_080300.log", EPILOGUE + ECHEC),
    "vide":       log("i_20261101_080300.log", ""),
    "cite":       log("j_20261101_080300.log", EPILOGUE + "   la note dit « [git] ⛔ push ÉCHEC après 3 tentatives — 9 commit(s) en avance » et c'est faux\n"),
    "inconnu":    log("k_20261101_080300.log", EPILOGUE + "[git] ⛔ push ÉCHEC après 3 tentatives — ? commit(s) en avance sur origin/main.\n"),
}

# ---- les six bornes qui doivent être ACCEPTÉES -----------------------------
for num, cle, quoi in (("③", "pousse", "`✅ push OK`"),
                       ("④", "rien", "`Rien de nouveau à committer`"),
                       ("⑤", "erreur", "`Job en erreur`"),
                       ("⑥", "exit7", "`PAS DE PUBLICATION` (exit 7 — borne du 23/10)")):
    suffixe, motif = publication([cas[cle]])
    borne(num, "ACCEPTÉE : %s n'est PAS accusé" % quoi, motif is None and suffixe == "")

# ⚠️ Détection POSITIVE : pas de ligne = pas d'accusation. Un garde satisfait par un état cassé
#    est le défaut qui revient le plus dans ce dépôt (`$SEMENCE` non vide, les deux photos vides).
suffixe, motif = publication([cas["vide"]])
borne("⑦", "ACCEPTÉE : un log VIDE n'est pas accusé (détection positive)",
      motif is None and suffixe == "")

# Même règle de jour que juge() : un rattrapage qui publie efface l'échec du matin.
suffixe, motif = publication([cas["hook"], cas["pousse"]])
borne("⑧", "ACCEPTÉE : échec + rattrapage qui publie le même jour → silence",
      motif is None and suffixe == "")

# ---- les bornes qui doivent MORDRE ----------------------------------------
suffixe, motif = publication([cas["nu"]])
borne("⑨", "la ligne d'échec seule est accusée, et le compte de commits est rendu",
      motif == "nonpublie" and "NON PUBLIÉ" in suffixe and "2 commit(s)" in suffixe)

suffixe, motif = publication([cas["hook"]])
borne("⑩", "cause « hook » nommée quand pre-push a refusé",
      motif == "nonpublie" and "hook" in suffixe and "transport" not in suffixe)

suffixe, motif = publication([cas["transport"]])
borne("⑪", "cause « transport » nommée quand la connexion a été coupée",
      motif == "nonpublie" and "transport" in suffixe and "hook" not in suffixe)

# La forme RÉELLE du log du 25/10 : le hook refuse ET la connexion tombe. Les deux gestes sont
# opposés, donc les deux doivent être nommés — en taire un ferait relancer un push qui sera refusé.
suffixe, motif = publication([cas["les_deux"]])
borne("⑫", "les DEUX causes sont nommées (forme réelle du log du 25/10)",
      motif == "nonpublie" and "hook" in suffixe and "transport" in suffixe)

# L'ancrage en début de ligne n'est pas cosmétique : une consignation qui CITE la ligne d'échec
# ne doit pas accuser le run qui la cite. C'est la leçon du 27/10 sur le corpus-dictionnaire.
suffixe, motif = publication([cas["cite"]])
borne("⑬", "ACCEPTÉE : la ligne d'échec CITÉE en milieu de ligne n'accuse pas",
      motif is None and suffixe == "")

# run_job.sh écrit '?' quand `git rev-list` échoue : le compte est inconnu, l'échec ne l'est pas.
suffixe, motif = publication([cas["inconnu"]])
borne("⑭", "un compte de commits « ? » est quand même accusé",
      motif == "nonpublie" and "? commit(s)" in suffixe)

# ---- le câblage : une fonction juste jamais appelée n'écrit dans aucun log ----
# Leçon du 27/10 : la borne doit NOMMER celle des trois exigences qui manque, sans quoi deux
# sabotages différents rendraient le même message.
manque = []
# 🔴 06/11/2026 — AU PREMIER JET CETTE BORNE APPARIAIT LA DÉFINITION, PAS L'APPEL : le motif
#    `publication\(logs\)` est satisfait par `def publication(logs):`, donc remplacer l'appel par
#    une valeur constante laissait le lot VERT, harnais en exit 0. C'est le sabotage S4 qui l'a dit,
#    pas la relecture — et c'est la borne qui garde la leçon du 27/10 (« une fonction juste jamais
#    appelée n'écrit dans aucun log ») qui ne pouvait pas échouer. On exige la forme ASSIGNÉE.
if not re.search(r"=\s*publication\(logs\)", src):
    manque.append("publication(logs) n'est pas APPELÉE (seule sa définition est là)")
if not re.search(r"nonpublies\.append\(jid\)", src):
    manque.append("jid n'est pas ajouté à nonpublies")
if not re.search(r"if manques or interrompus or nonpublies:", src):
    manque.append("nonpublies n'est pas dans la condition de sortie")
if not re.search(r"✗ %d run\(s\) NON PUBLIÉ\(S\)", src):
    manque.append("le message de synthèse n'est pas imprimé")
borne("⑮", "câblage complet dans --manques" + ((" — MANQUE : " + " ; ".join(manque)) if manque else ""),
      not manque)

# ⚠️ 27/10/2026 — un script qui n'appartient à AUCUNE catégorie du hook ne déclenche RIEN :
#    un push qui ne touche que lui passe sans contrôle. C'était le cas de CLAUDE.md, et c'était
#    le cas de rattrapage_jobs.sh jusqu'à aujourd'hui.
hook_src = open(HOOK, encoding="utf-8").read() if os.path.exists(HOOK) else ""
borne("⑯", "rattrapage_jobs.sh est dans SURVEILLES du hook",
      bool(re.search(r"rattrapage_jobs\\\.sh", hook_src)))

# ⚠️ 04/11/2026 — UN GARDE DE COMPTE DOIT ÊTRE ESSAYÉ SUR LA LIGNE QU'IL VA VRAIMENT LIRE.
#    Ce jour-là mon `sed` exigeait « un caractère PUIS une espace » avant le numérateur, or la
#    ligne du témoin commençait en colonne 1 : LU était VIDE, et --docs refusait tous les pushs
#    d'un dépôt sain. Faux dans l'autre sens, un tel garde accepterait tout. On applique donc le
#    `sed` DU HARNAIS à la ligne que ce témoin imprime, et on exige ATTENDU_PUB = bornes jouées.
import subprocess
h_src = open(os.path.join(RACINE, "outils", "scripts", "non_regression.sh"), encoding="utf-8").read()
m_bloc = re.search(r"bloc_publication \(\) \{(?:.*\n)*?^\}", h_src, re.M)
bloc_h = m_bloc.group(0) if m_bloc else ""
m_att = re.search(r"ATTENDU_PUB=(\d+)", bloc_h)
m_sed = re.search(r"sed -n '([^']+)'", bloc_h)
detail = []
lu = None
if not m_att:
    detail.append("ATTENDU_PUB introuvable dans bloc_publication")
if not m_sed:
    detail.append("le sed du harnais est introuvable")
if m_att and m_sed:
    attendu = int(m_att.group(1))
    rendu = LIGNE_FIN % (attendu, attendu)
    lu = subprocess.run(["sed", "-n", m_sed.group(1)], input=rendu,
                        capture_output=True, text=True).stdout.strip()
    if lu != str(attendu):
        detail.append("le sed du harnais rend %r sur la ligne réelle, pas %d" % (lu, attendu))
    if attendu != len(jouees) + 1:
        detail.append("ATTENDU_PUB=%d mais %d bornes sont jouées" % (attendu, len(jouees) + 1))
borne("⑰", "le sed du harnais lit le DÉNOMINATEUR de la ligne réelle"
      + ((" — " + " ; ".join(detail)) if detail else ""), not detail)

for f in cas.values():
    os.unlink(f)
os.rmdir(tmp)

if ko:
    # ⚠️ 06/11/2026 — CHAQUE LIGNE DE DÉTAIL PORTE SON ✗, et ce n'est pas cosmétique : la branche
    #    d'échec du harnais fait `grep '✗' "$OUT"`, donc un détail sans ✗ est AVALÉ et les sept
    #    sabotages rendent le même message générique — on ne sait plus laquelle des bornes a mordu.
    #    Mesuré au premier jet : les sept imprimaient « NE DISTINGUE PLUS… » et rien d'autre.
    print("\n✗ %d borne(s) en défaut :" % len(ko))
    for x in ko:
        print("    ✗ " + x)
print(LIGNE_FIN % (len(jouees) - len(ko), len(jouees)))
sys.exit(1 if ko else 0)
