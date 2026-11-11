#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tout témoin du dépôt appartient-il à une catégorie du hook `pre-push` ?

POURQUOI — MESURÉ LE 11/11/2026, ET LE TROU ÉTAIT UN RÉPERTOIRE ENTIER.
NEUF des douze fichiers de `outils/scripts/non_regression/` n'appartenaient à AUCUNE
catégorie : bfr_journal, coherence_skill, corps_tronque, desarmement_git, etiquette_has,
faisceau_5bis, murs_lus, publication_run, tolerance_page_morte. Un push qui ne touchait
qu'eux ne déclenchait RIEN — le témoin pouvait être amputé ou saboté et partir sur le
dépôt sans qu'UNE SEULE de ses bornes soit jouée. Même défaut que `CLAUDE.md` sans
catégorie (27/10) et que `rattrapage_jobs.sh` (06/11), à l'échelle d'un répertoire.

⚠️ ET MA PROPRE DESCRIPTION DU TROU ÉTAIT FAUSSE LA VEILLE : j'avais écrit que
`publication_run.py` n'était pas câblé « alors que muter_docx.py et omission_axe2.py le
sont ». Deux éléments lus comme un recensement : il y en avait NEUF. « Un recensement
textuel n'est pas un recensement d'appels », par l'autre bout.

🔴 LE PRÉDICAT EST STRUCTUREL, JAMAIS UN COMPTE EN DUR. Un `12/12` figé se périme au
prochain témoin écrit, et une liste de fichiers dans le hook se périme de la même façon
— c'est le défaut que ce dépôt a payé TROIS fois (`setup_launchd.sh`,
`rattrapage_jobs.sh`, la table dossier → job de ㊳). On lit donc les catégories DANS le
hook, on énumère les témoins DEPUIS git, et la borne ⑤ exige qu'un nom de témoin
FABRIQUÉ, qui n'existe pas, soit déjà couvert : c'est elle, et elle seule, qui interdit
de revenir à une liste.

⛔ IL NE PEUT PAS SE PÉRIMER : aucun réseau, aucun tiers, aucune date. L'invariant ne
devient faux que si un témoin du dépôt cesse d'être déclenché par le hook.

⚠️ CE QU'IL NE FAIT PAS, ET C'EST DIT : les scripts de PREMIER niveau
(`outils/scripts/*.py|sh`) ne sont pas exigés — leur rattachement est une décision par
script, pas un invariant. Ils sont RECENSÉS et IMPRIMÉS, non bloquants, pour que ce
reste soit visible au lieu d'être silencieux (même parti que `--table` de
`controle_livrable_du_job.py`). Mesure du 11/11 : 8 orphelins de premier niveau.
"""
import pathlib, re, subprocess, sys

RACINE = pathlib.Path(__file__).resolve().parent.parent.parent.parent
# ⚠️ QUATRE parent : ce témoin vit dans outils/scripts/non_regression/. Trois donnaient
# outils/ — bug de tolerance_page_morte.py (23/10), coherence_skill.py (27/10) et
# integrite_livrables.py (11/11, le jour même).
assert (RACINE / "jobs_config.json").exists(), "RACINE ne pointe pas sur la racine : %s" % RACINE
HOOK = RACINE / "outils" / "scripts" / "hooks" / "pre-push"

KO, JOUEES = [], []
def borne(nom, condition):
    JOUEES.append(nom)
    if not condition:
        KO.append(nom)

# ── les catégories sont LUES dans le hook, par motif de déclaration et non par une liste
#    de noms : renommer une catégorie ne doit pas la faire disparaître du recensement.
src = HOOK.read_text()
CATS = {}
for m in re.finditer(r"^([A-Z][A-Z0-9_]*)='(\^[^']+)'$", src, re.M):
    CATS[m.group(1)] = m.group(2)
borne("① les catégories sont lues DANS le hook (au moins six déclarations)", len(CATS) >= 6)

def categories(chemin):
    return [n for n, r in CATS.items() if re.match(r, chemin)]

suivis = [p.decode() for p in
          subprocess.run(["git", "ls-files", "-z"], cwd=str(RACINE), capture_output=True).stdout.split(b"\0") if p]
temoins = sorted(p for p in suivis
                 if p.startswith("outils/scripts/non_regression/") and p.endswith(".py"))
orphelins = [p for p in temoins if not categories(p)]

borne("② le dépôt a bien des témoins à vérifier (un périmètre VIDE n'est pas un dépôt sain)",
      len(temoins) >= 10)
borne("③ AUCUN témoin n'est orphelin de catégorie", not orphelins)
borne("④ le hook se surveille lui-même — sinon l'éditer ne déclenche rien",
      bool(categories("outils/scripts/hooks/pre-push")))
# ⑤ LA BORNE QUI INTERDIT DE REVENIR À UNE LISTE : un nom FABRIQUÉ, absent du dépôt,
#    doit déjà être couvert. Avec une liste de fichiers en dur, elle tombe.
FABRIQUE = "outils/scripts/non_regression/temoin_fabrique_qui_nexiste_pas.py"
assert FABRIQUE not in suivis, "le nom fabriqué existe pour de vrai : en changer"
borne("⑤ un témoin FUTUR est déjà couvert — donc c'est un MOTIF, pas une liste (ACCEPTEE)",
      bool(categories(FABRIQUE)))
# ⚠️ MA PREMIÈRE ⑥ S'ÉCRIVAIT `True if X == [] else X != []` : elle ne pouvait PAS échouer,
#    donc ce n'était pas une borne (règle du 26/10). Forme juste : le motif de répertoire est
#    ANCRÉ, donc un .py quelconque hors de ce répertoire n'est PAS attrapé par lui. Un motif
#    élargi en `.*\.py` ferait tomber cette borne — c'est ce qu'elle garde.
borne("⑥ le motif est ANCRÉ au répertoire : un .py jetable n'est pas attrapé (ACCEPTEE)",
      "SURVEILLES" not in categories("en_cours/jetable.py")
      and "SURVEILLES" not in categories("outils/scripts/non_regression/sous/profond.py"))
borne("⑦ les catégories spécifiques SURVIVENT au motif de répertoire — muter_docx garde CINQBIS",
      "CINQBIS" in categories("outils/scripts/non_regression/muter_docx.py")
      and "EDPREC" in categories("outils/scripts/non_regression/omission_axe2.py"))
borne("⑧ le motif de répertoire est dans SURVEILLES, la catégorie qui lance le mode normal",
      "SURVEILLES" in categories("outils/scripts/non_regression/publication_run.py"))

# ──────── ⑫ LE PRÉDICAT QUI COMPTE : TOUT SCRIPT QUE LE HARNAIS EXÉCUTE EST-IL SURVEILLÉ ?
#    Mesuré le 11/11/2026 : des 27 scripts que non_regression.sh référence par chemin, DEUX
#    n'appartenaient à aucune catégorie — `balayer_adresses.py` (ATTENDU_BAL=72) et
#    `ca_bundle.py` (ATTENDU_CA=6). Leurs bornes vivent DANS le harnais, donc les toucher
#    aurait dû le lancer : il ne se lançait pas. C'est le même invariant que ③ d'un cran plus
#    large, et il est LU DANS LE HARNAIS — aucune liste, aucun compte en dur, donc le prochain
#    script que le harnais apprendra à exécuter sera exigé tout seul.
#    ⚠️ LES LIGNES ENTIÈREMENT COMMENTÉES SONT RETIRÉES AVANT LE BALAYAGE. Mon premier jet
#    lisait le texte brut, et un sabotage qui ajoutait une référence EN COMMENTAIRE le faisait
#    mordre : c'est « un recensement textuel n'est pas un recensement d'appels » (27/10), qui
#    m'avait déjà fait presque durcir trois fichiers qui ne font rien. L'erreur allait dans le
#    sens sûr — une exigence de trop — mais une fausse exigence se « corrige » en câblant un
#    script que le harnais n'exécute pas. On retire donc les lignes de commentaire ENTIÈRES,
#    et pas les « # » en ligne, qui vivent dans des chaînes et des motifs.
HARNAIS = (RACINE / "outils" / "scripts" / "non_regression.sh").read_text()

# ─────────────────────────────────────────────────────────────────────────────────────────────
# MODE --journal : LE RECENSEMENT D'EXÉCUTION, celui que le prédicat textuel ne pouvait pas
# faire. L'épilogue du harnais appelle ce mode avec le journal que le shim nr_trace.sh vient
# d'écrire, donc on confronte les catégories du hook à ce qui a RÉELLEMENT été lancé, et non
# à ce que le texte du harnais a l'air de lancer. Appelé, jamais recopié (règle du 15/10) :
# `categories()` et `CATS` sont les mêmes ici et dans les bornes.
# ⛔ Un journal ABSENT ou VIDE n'accuse personne : l'absence de mesure n'est pas une mesure
#    (c'est la borne ④ de balayer_adresses.py, « None n'est jamais une façade »). Il le DIT.
# ─────────────────────────────────────────────────────────────────────────────────────────────
if len(sys.argv) > 2 and sys.argv[1] == "--journal":
    jr = pathlib.Path(sys.argv[2])
    if not jr.exists():
        print("  ⓘ JOURNAL D'EXÉCUTION ABSENT : %s — rien n'est mesuré, rien n'est accusé" % jr)
        sys.exit(0)
    lances = sorted({l.strip() for l in jr.read_text().split("\n") if l.strip()})
    if not lances:
        print("  ⓘ JOURNAL D'EXÉCUTION VIDE — rien n'est mesuré, rien n'est accusé")
        sys.exit(0)
    orph = [c for c in lances if c in set(suivis) and not categories(c)]
    hors = [c for c in lances if c not in set(suivis)]
    print("  JOURNAL D'EXÉCUTION : %d script(s) RÉELLEMENT lancé(s) · %d orphelin(s) de catégorie"
          "%s" % (len(lances), len(orph), " · %d non suivi(s) par git" % len(hors) if hors else ""))
    for c in orph:
        print("  ⛔ LANCÉ PAR LE HARNAIS, NON SURVEILLÉ : %s — un push qui ne touche que lui ne "
              "déclenche rien" % c)
    sys.exit(1 if orph else 0)


def code_seul(texte):
    """Le texte privé de ses lignes ENTIÈREMENT commentées. UNE seule définition : la borne ⑭
    l'appelle, elle ne la recopie pas — sans quoi l'élargir laisserait la borne verte (défaut
    mesuré au sabotage S12, troisième occurrence de la règle du 15/10 dans la même séance)."""
    return "\n".join(l for l in texte.split("\n") if not l.lstrip().startswith("#"))

# 🔴 11/11/2026 — ET MON MOTIF NE CONNAISSAIT QU'UNE SEULE FORME D'APPEL, DONC IL RATAIT UN
#    SCRIPT RÉELLEMENT EXÉCUTÉ. `controle_clauses_parcours.py` est lancé par le témoin de
#    `supprimer_job.sh` sous la forme PYTHON — `racine + "/outils/scripts/…"`, dans un heredoc —
#    et non `$ROOT/…` : il n'était NI compté parmi les exécutés, NI accusé. Un prédicat qui ne
#    reconnaît qu'une forme de ce qu'il cherche rend un vert sur ce qu'il n'a pas vu ; c'est
#    « un recensement textuel n'est pas un recensement d'appels » (27/10) d'un cran plus loin.
# ⛔ ET LE PRÉFIXE EST LE DISCRIMINANT, PAS UN DÉTAIL : `setup_launchd.sh` apparaît NU dans le
#    harnais, comme ARGUMENT d'un `git status --porcelain` — ce n'est pas une exécution, et la
#    borne ⑰ l'épingle. Exiger un préfixe (`$ROOT/` ou `<var> + "/`) sépare les deux.
FORMES = r'(?:\$\{?ROOT\}?|[A-Za-z_][A-Za-z0-9_]* \+ ")/(outils/scripts/[A-Za-z0-9_./-]+\.(?:py|sh))'

# 🔴 11/11/2026, TROISIÈME ANGLE MORT, ET C'EST LE RECENSEMENT D'EXÉCUTION QUI L'A TROUVÉ, PAS
#    LA RELECTURE : `tolerance_page_morte.py` est lancé par `$NR/…` — une variable AUTRE que
#    `$ROOT` — donc aucun motif ancré sur `$ROOT` ne pouvait l'apparier. Mesuré : 2 scripts
#    (`tolerance_page_morte.py` ×3, `muter_docx.py` ×1), tous deux déjà câblés, donc zéro trou
#    de câblage — mais le garde ne les aurait PAS accusés s'ils avaient été orphelins.
# 🟢 La table des variables est DÉRIVÉE du harnais, jamais écrite en dur : une variable de
#    chemin ajoutée demain est prise d'elle-même (« un motif, jamais une liste »).
def prefixes(texte):
    """{nom de variable : prefixe relatif} pour toute variable du harnais valant $ROOT/…"""
    return {m.group(1): m.group(2).rstrip("/") for m in
            re.finditer(r'(?m)^([A-Z][A-Z0-9_]*)="?\$\{?ROOT\}?/(outils/scripts[^"\s]*)"?\s*$',
                        texte)}

def scripts_executes(texte):
    c = code_seul(texte)
    trouves = set(re.findall(FORMES, c))
    for nom, pref in prefixes(texte).items():
        for rel in re.findall(r'\$\{?%s\}?/([A-Za-z0-9_./-]+\.(?:py|sh))' % nom, c):
            trouves.add("%s/%s" % (pref, rel))
    return sorted(trouves)

executes = scripts_executes(HARNAIS)
suivis_set = set(suivis)
orph_exec = [p for p in executes if p in suivis_set and not categories(p)]
borne("⑫ le harnais exécute bien des scripts (un périmètre VIDE n'est pas un dépôt sain)",
      len(executes) >= 20)
borne("⑬ TOUT script que le harnais exécute est déclenché par le hook", not orph_exec)
# ⑭ LA BORNE QUI DOIT ÊTRE ACCEPTÉE : une référence posée EN COMMENTAIRE n'est pas une
#    exécution, donc elle n'exige rien. Sans elle, rien n'empêche de réélargir demain et de
#    faire câbler un script que le harnais ne lance pas (leçon du 27/10).
borne("⑭ une reference EN COMMENTAIRE n'exige rien — recensement d'APPELS, pas textuel (ACCEPTEE)",
      "outils/scripts/audit_vault.py" not in
      scripts_executes(HARNAIS + '\n#   "$ROOT/outils/scripts/audit_vault.py"\n'))
borne("⑮ et une reference RÉELLE, elle, est bien recensée (sans quoi ⑭ passerait sur du vide)",
      "outils/scripts/audit_vault.py" in
      scripts_executes(HARNAIS + '\nenv -i $PY "$ROOT/outils/scripts/audit_vault.py"\n'))
# ⑯ la forme PYTHON d'un appel est reconnue : c'est le faux négatif mesuré le 11/11, et la
#    borne nomme le script qui le révélait, pas un fabriqué — il est dans le harnais pour de bon.
borne("⑯ la forme PYTHON « racine + \"/outils/… » est reconnue comme un appel",
      "outils/scripts/controle_clauses_parcours.py" in executes)
# ⑰ LA BORNE QUI DOIT ÊTRE ACCEPTÉE : un script passé en ARGUMENT n'est pas exécuté. Sans elle,
#    retirer l'exigence de préfixe laisserait le lot vert et ferait compter des arguments.
borne("⑰ un script passé en ARGUMENT n'est pas un appel (ACCEPTEE)",
      "outils/scripts/setup_launchd.sh" not in
      scripts_executes('  SJ=$(git status --porcelain outils/scripts/setup_launchd.sh)\n'))

# ── recensement NON BLOQUANT des scripts de premier niveau, pour qu'il ne soit pas silencieux
niv1 = sorted(p for p in suivis if re.match(r"outils/scripts/[^/]+\.(py|sh)$", p))
orph1 = [p for p in niv1 if not categories(p)]
borne("⑨ le recensement de premier niveau est fait (un périmètre VIDE n'est pas un dépôt sain)",
      len(niv1) >= 20)
# 🆕 11/11/2026 — LE RECENSEMENT DE PREMIER NIVEAU DEVIENT UNE BORNE, les six derniers orphelins
#    ayant été câblés. ⛔ Cela déroge à la règle du 14/10 (« avertir avant de bloquer ») de la
#    même façon que `corps_tronque.py` : le motif ne juge aucun CONTENU, il juge si le câblage du
#    dépôt est complet — un fait structurel entièrement de notre main, dont le remède est UNE
#    ligne dans `SURVEILLES`. ⚠️ Le coût est dit : un script neuf de premier niveau doit être
#    rattaché à une catégorie AVANT son premier push, sans quoi le hook refuse.
borne("⑱ AUCUN script de premier niveau n'est orphelin de categorie", not orph1)

# ─────────────────────────────────────────────────────────────────────────────────────────────
# L'INSTRUMENTATION ELLE-MÊME (11/11/2026). Les bornes ci-dessus gardent le CÂBLAGE ; celles-ci
# gardent le MÉCANISME qui le mesure. Sans elles, remettre `PY=/usr/bin/python3` rendrait
# l'épilogue aveugle et muet — un journal vide n'accuse personne, par conception.
# ⛔ Le shim est exercé POUR DE VRAI, sur une arborescence FABRIQUÉE en tempfile : rien de
#    vivant n'entre dans le verdict (leçon du 22/10), et ce lot ne peut donc pas périmer.
# ─────────────────────────────────────────────────────────────────────────────────────────────
SHIM = RACINE / "outils" / "scripts" / "nr_trace.sh"
borne("⑲ le harnais definit PY sur le SHIM, au litteral (sinon l'epilogue est aveugle)",
      'PY="$ROOT/outils/scripts/nr_trace.sh"' in HARNAIS
      and not re.search(r'(?m)^PY=/usr/bin/python3\s*$', HARNAIS))

import tempfile, os, shutil, stat
with tempfile.TemporaryDirectory() as _t:
    _sc = pathlib.Path(_t) / "outils" / "scripts"
    (_sc / "logs").mkdir(parents=True)
    _sh = _sc / "nr_trace.sh"
    shutil.copy(SHIM, _sh); os.chmod(_sh, 0o755)
    _jr = _sc / "logs" / ".nr_journal"
    (_sc / "bidon.py").write_text("import sys\nsys.exit(7)\n")

    def _lance(*args):
        r = subprocess.run([str(_sh), *args], capture_output=True, text=True, env={})
        return r.returncode, (_jr.read_text() if _jr.exists() else "")

    _rc, _j = _lance(str(_sc / "bidon.py"))
    borne("⑳ le shim JOURNALISE le script lance, en chemin relatif a la racine",
          "outils/scripts/bidon.py" in _j)
    borne("㉑ et il TRANSMET le code de sortie du vrai interprete (7, pas 0)", _rc == 7)
    _jr.unlink(missing_ok=True)   # S18 produit un journal ABSENT : un plantage ici
                                 # n'imprimerait AUCUN ✗ (diagnostic vide, 11/11)
    # ㉒ LA BORNE QUI DOIT ÊTRE ACCEPTÉE : un `-c` inline ne lance aucun script du dépôt, donc il
    #    ne journalise RIEN. Sans elle, un élargissement remplirait le journal de bruit et
    #    l'épilogue accuserait des chaînes qui ne sont pas des scripts.
    _rc2, _j2 = _lance("-c", "print(1)")
    borne("㉒ un `-c` inline ne journalise RIEN (ACCEPTEE)", _rc2 == 0 and _j2.strip() == "")
    # ㉓ tout cela a tourné avec env={} — donc sans NR_JOURNAL, sans PATH, sans HOME : c'est la
    #    contrainte qui dicte la forme du shim, le harnais lançant presque tout sous `env -i`.
    borne("㉓ le shim fonctionne sous un environnement VIDE (le harnais lance sous env -i)",
          "outils/scripts/bidon.py" in _lance(str(_sc / "bidon.py"))[1])

borne("㉔ l'epilogue du harnais APPELLE le mode --journal et pose STATUT=1 — une alerte que "
       "personne ne lit n'existe pas (27/10)",
      '--journal "$NR_JOURNAL"' in code_seul(HARNAIS)
      and "Recensement d'exécution" in HARNAIS
      and re.search(r"--journal \"\$NR_JOURNAL\"[\s\S]{0,260}?STATUT=1", code_seul(HARNAIS)))
borne("㉕ les trois lancements de .sh se DECLARENT par nr_lance (ils ne passent pas par $PY)",
      all(("nr_lance %s" % c) in code_seul(HARNAIS) for c in
          ("outils/scripts/non_regression.sh", "outils/scripts/supprimer_job.sh",
           "outils/scripts/non_regression_runner.sh")))
# ㉖ `sys.executable` CONTOURNAIT le shim : c'est la forme d'appel qui avait échappé au
#    recensement textuel, et elle ne doit pas revenir sur ce site.
# ㉗ et ㉘ exercent le mode --journal LUI-MÊME, en relançant ce script : c'est lui que
#    l'épilogue appelle, donc c'est lui qu'il faut éprouver, pas une réimplémentation (15/10).
MOI = str(pathlib.Path(__file__).resolve())
with tempfile.TemporaryDirectory() as _t:
    _j = pathlib.Path(_t) / "j"
    # un script SUIVI par git et DÉPOURVU de catégorie doit faire sortir en 1. On en fabrique un
    # en retirant sa catégorie du hook dans une COPIE, jamais dans le fichier du dépôt.
    _j.write_text("outils/scripts/nr_trace.sh\n")
    _r = subprocess.run([sys.executable, MOI, "--journal", str(_j)],
                        capture_output=True, text=True)
    borne("㉗ un script LANCE et surveille ne fait PAS sortir en 1 (ACCEPTEE)",
          _r.returncode == 0 and "RÉELLEMENT lancé" in _r.stdout)
    _j.write_text("")
    _r2 = subprocess.run([sys.executable, MOI, "--journal", str(_j)],
                         capture_output=True, text=True)
    borne("㉘ un journal VIDE n'accuse personne et le DIT (ACCEPTEE) — l'absence de mesure "
          "n'est pas une mesure",
          _r2.returncode == 0 and "VIDE" in _r2.stdout)
    _r3 = subprocess.run([sys.executable, MOI, "--journal", str(_j) + ".absent"],
                         capture_output=True, text=True)
    borne("㉙ un journal ABSENT n'accuse personne et le DIT (ACCEPTEE)",
          _r3.returncode == 0 and "ABSENT" in _r3.stdout)
    # ㉜ LE CAS REFUSANT du mode --journal, et c'est lui le garde : ㉗ ㉘ ㉙ ne prouvent que
    #    les cas où il se TAIT. On y met un chemin SUIVI par git et dépourvu de catégorie —
    #    il n'a pas besoin d'être un script, le mode ne juge que « suivi ET sans catégorie ».
    _hors = next((c for c in suivis if c.startswith("outils/templates/")
                  and not categories(c)), None)
    assert _hors, "aucun chemin suivi sans catégorie : la borne ㉜ passerait sur du vide"
    _j.write_text(_hors + "\n")
    _r4 = subprocess.run([sys.executable, MOI, "--journal", str(_j)],
                         capture_output=True, text=True)
    borne("㉜ un chemin LANCE et SANS categorie fait sortir en 1, et il est NOMME",
          _r4.returncode == 1 and _hors in _r4.stdout and "NON SURVEILLÉ" in _r4.stdout)

# ㉚ la table des préfixes est DÉRIVÉE : un lancement via une variable autre que $ROOT est vu.
borne("㉚ un lancement via une AUTRE variable de chemin ($NR/…) est recense",
      "outils/scripts/non_regression/tolerance_page_morte.py" in executes
      and "NR" in prefixes(HARNAIS))
# ㉛ LA BORNE QUI DOIT ÊTRE ACCEPTÉE : une variable qui ne vaut PAS $ROOT/outils/scripts n'entre
#    pas dans la table — sinon n'importe quel $VAR/x.py deviendrait un lancement de script du dépôt.
borne("㉛ une variable etrangere a outils/scripts n'entre pas dans la table (ACCEPTEE)",
      "HOME" not in prefixes('HOME="$ROOT/livrables"\nNR="$ROOT/outils/scripts/non_regression"\n')
      and "NR" in prefixes('HOME="$ROOT/livrables"\nNR="$ROOT/outils/scripts/non_regression"\n'))

borne("㉖ l'appel Python interne passe par le shim, PAS par sys.executable",
      "sys.executable, racine" not in HARNAIS
      and 'racine + "/outils/scripts/nr_trace.sh"' in HARNAIS)
print("")


print("CATÉGORIES DU HOOK : %d · témoins : %d dont %d orphelin(s) · exécutés par le harnais : "
      "%d dont %d non surveillé(s) · premier niveau : %d dont %d sans catégorie"
      % (len(CATS), len(temoins), len(orphelins), len(executes), len(orph_exec), len(niv1), len(orph1)))
for p in orphelins:
    print("  ⛔ TÉMOIN ORPHELIN : %s — un push qui ne touche que lui ne déclenche RIEN" % p)
for p in orph_exec:
    print("  ⛔ EXÉCUTÉ PAR LE HARNAIS, NON SURVEILLÉ : %s — ses bornes vivent dans le harnais,"
          " et le toucher ne le lance pas" % p)
for p in orph1:
    print("  ⓘ  premier niveau sans catégorie : %s" % p)

# ⑩ LE sed DU HARNAIS, APPLIQUÉ À LA LIGNE RÉELLEMENT IMPRIMÉE. L'ancre est ASCII sans
#    accent : la dérive d'un libellé accentué a déjà fait lire un dénominateur VIDE et
#    refuser TOUS les pushs (04/11). Un garde de compte doit être essayé sur la ligne
#    qu'il va vraiment lire — faux, il bloque tout ; inversé, il accepte tout.
# 🔴 LE sed EST LU DANS LE HARNAIS, PAS RECOPIÉ ICI. Mon premier jet le recopiait : un
#    sabotage qui faisait dériver le libellé dans les DEUX fichiers du témoin laissait la
#    borne verte, puisque la copie dérivait avec. « Un test qui teste une COPIE de la
#    logique ne garde rien » (15/10) — c'est le sabotage qui l'a dit, pas la relecture.
_h = (RACINE / "outils" / "scripts" / "non_regression.sh").read_text()
_seds = re.findall(r"sed -n '([^']*categories hook[^']*)'", _h)
borne("⑩ le harnais porte UN seul sed pour cette ligne", len(_seds) == 1)
_sed = _seds[0] if _seds else "s/ZZZ/\\1/p"
_ligne = ("%d/%d bornes categories hook — tout temoin du depot est declenche par le hook"
          % (len(JOUEES) + 1 - len(KO), len(JOUEES) + 1))
_lu = subprocess.run(["sed", "-n", _sed], input=_ligne, capture_output=True, text=True).stdout.strip()
borne("⑪ le sed DU HARNAIS lit le DENOMINATEUR sur la ligne reellement imprimee",
      _lu == str(len(JOUEES) + 1))

print("%d/%d bornes categories hook — tout temoin du depot est declenche par le hook"
      % (len(JOUEES) - len(KO), len(JOUEES)))
for n in KO:
    print("  ✗ %s" % n)
sys.exit(1 if KO else 0)
