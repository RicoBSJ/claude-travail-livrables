#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""isolation_import.py — les CINQ scripts qui importent `ca_bundle` sondent-ils AVEC le
faisceau, même sous `python3 -I` ? Et leur repli se dit-il ?

POURQUOI (28/11/2026). `-I` implique `-P` : le dossier du script quitte `sys.path`, donc
`import ca_bundle` lève `ModuleNotFoundError`, l'`except Exception` l'avale, et `curl` part
SANS `--cacert`. Mesuré de bout en bout sur `https://www.has-sante.fr/`, les deux sondes
sous `-I` et rejouées seules : la version d'avant rend **HTTP 000 · curl 60 · NON LUE**, la
corrigée **HTTP 200 · 7 253 car. utiles**. C'est le défaut du 18/10 par une autre porte — une
source valide écartée en silence —, et il est ATTEIGNABLE À LA MAIN : la consigne d'isolation
prescrit `-I` pour tout Python qui lit un fichier non fiable.

⛔ CE N'ÉTAIT PAS UN DÉFAUT DE PRODUCTION, et il faut le dire : `0` occurrence de
`python3 -I` dans le hook, le harnais et `run_job.sh`, contre 50 `python3` nus. Et lancés
comme scripts, les cinq avaient déjà leur dossier en `sys.path[0]` : l'insert y est un
DOUBLON inoffensif et le `print` ne part jamais. Le correctif ne mord que sous `-I` et dans
la tranche que le harnais exécute.

🔴 ET LE FOND N'ÉTAIT PAS LE REPLI, C'ÉTAIT QU'IL ÉTAIT INDISCERNABLE. `args_curl()` NE
LÈVE PAS — `chemin()` rattrape `OSError` et rend `None`, d'où `[]` ; mesuré en masquant
brew ET `ca/`. Donc cet `except` n'attrape QUE l'import, c'est-à-dire un `ca_bundle` absent
du disque ou un `sys.path` perdu, et muet il rendait ces deux états cassés indiscernables du
repli légitime d'une machine sans brew. Un garde satisfait par un état cassé.
⚠️ La docstring de `faisceau_5bis.py` attribue ce repli à « une machine sans brew » : c'est le
MÉCANISME qui est mal nommé, pas sa borne ④ — sur une telle machine l'import réussit et c'est
`args_curl()` qui rend `[]`, sans jamais passer par l'`except`.

🔴 ET LE PORTAGE AUX QUATRE AUTRES A CASSÉ DEUX CHOSES, MESURÉES AVANT D'ÊTRE CORRIGÉES :
  • `faisceau_5bis._exec` exécutait la tranche extraite avec `g = {}` ; le repli qui parle a
    besoin du `sys` du module, que la tranche n'emporte pas (elle commence à `try:`) →
    `NameError`, et le témoin PLANTAIT, donc ni ④ ni ⑤ ne se voyaient mordre. `sys` est
    désormais fourni : on donne au fragment le contexte qu'il attend, plutôt que de
    contorsionner le code de production pour arranger un test.
  • les TROIS sites du harnais qui exécutent la tranche de `controle_attributions.py`
    passaient `g = {"__name__": "__main__"}` SANS `__file__` → `NameError`, non rattrapé
    (seul `SystemExit` l'est), et le gate QUI ALIMENTE LA RÉFÉRENCE mourait. La borne ⑭ garde
    que les trois le fournissent, une dérive d'un seul suffisant.

CE QUE CE TÉMOIN GARDE, et ce qu'il ne garde pas :
  • ①  les chemins sont rendus — QUATRE dirname, ce script vivant un cran plus bas. Le bug à
    cinq occurrences : avec trois, tout serait vert sur des fichiers absents.
  • ② ③ ④  PRÉDICAT STRUCTUREL, jamais une liste : tout `.py` de `outils/scripts/` qui importe
    un VOISIN doit réparer `sys.path`, et AVANT ce premier import. ② exige un ensemble NON
    VIDE (7 scripts aujourd'hui), ③ et ④ sont BLOQUANTES. À 0 orphelin, les laisser non
    bloquantes garantissait qu'elles repourrissent au prochain script écrit (règle du 11/11).
  • ⑤  FABRIQUÉE, et DÉCISIVE : un script qui importe un voisin sans réparer doit être
    DÉTECTÉ, et un qui répare trop tard aussi. Sans elle, ③ et ④ seraient vertes sur un
    détecteur inerte.
  • ⑥ ⑦ ⑧ ⑨  la tête d'`aspirer.py` est EXTRAITE puis exécutée dans de VRAIS sous-processus,
    avec `-I` et sans — pas une copie de sa logique (15/10). Les sous-processus partent de la
    RACINE du dépôt, pour que le sens non isolé réussisse par la ligne de réparation et non
    par le cwd. ⑧ et ⑨ ne sont pas redondantes : c'est le SILENCE qui était le défaut.
  • ⑩  TEXTUELLE, et sa limite est dite : seul `aspirer.py` a une tête exécutable hors
    contexte — les trois 5 bis sortent sur un `sys.exit` d'usage, `controle_attributions.py`
    pèse 1 626 lignes. Pour les quatre autres on exige donc le LITTÉRAL, même parti que le
    garde ② de l'assertion de tableau (18/10) et que `desarmement_git.py` (27/10).
  • ⑪  ACCEPTÉE : `args_curl()` ne lève pas. C'est la PRÉMISSE de ⑨ — si elle devenait fausse,
    l'`except` attraperait aussi le repli légitime et la ligne de stderr accuserait une
    machine saine.
  • ⑫  aucun `.py` de `outils/scripts/` ne masque un module standard. C'est le risque que
    l'insert en position 0 CRÉE, et c'est exactement le danger du `json.py` planté que la
    consigne d'isolation veut écarter : on le mesure au lieu de le supposer.
  • ⑬  aucun `-k`, aucun `--insecure` dans les cinq : la chaîne reste validée entièrement.
  ⛔ CE QU'IL NE GARDE PAS : l'EFFET du correctif sur les quatre autres scripts — le prouver
    demanderait du réseau et, pour les 5 bis, un `.docx` et des pages tierces. On exige le
    littéral là, et l'exécution sur `aspirer.py`.

Aucun réseau, aucun tiers — ce lot ne peut pas périmer sur la panne d'un site, contrairement
aux témoins qui ont bloqué TOUS les pushs les 15, 22 et 23/10.
Usage : python3 outils/scripts/non_regression/isolation_import.py [--autotest]
Sortie : 0 si les bornes tiennent, 1 sinon.
"""
import os, re, subprocess, sys, tempfile

# ⚠️ QUATRE dirname — voir ① et la note de faisceau_5bis.py.
RACINE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
SCRIPTS = os.path.join(RACINE, "outils", "scripts")
ASPIRER = os.path.join(SCRIPTS, "aspirer.py")
CABUNDLE = os.path.join(SCRIPTS, "ca_bundle.py")
NR_SH = os.path.join(SCRIPTS, "non_regression.sh")
# ⛔ CIBLES n'est PAS le prédicat : c'est la liste des scripts dont on exige en plus que le repli
#    PARLE (borne ⑩) et qu'ils n'aient aucun -k (⑬). Le prédicat de ③ ④, lui, est STRUCTUREL —
#    « tout .py de outils/scripts/ qui importe un voisin » — et il couvrira un script neuf
#    sans qu'on y touche. Une liste se périme ; un motif, non (11/11).
CIBLES = tuple(os.path.join(SCRIPTS, f) for f in (
    "aspirer.py", "controle_ai_act.py", "controle_astrologie_karmique.py",
    "controle_attributions.py", "controle_psychopathologie.py"))
FIN_TETE = "    CA = []\n"

# Le sous-processus de ③ ④ : il EXTRAIT la tête du fichier et l'exécute. `__file__` doit être
# fourni, sans quoi la ligne de réparation lève NameError — ma première mesure du 28/11 l'a
# oublié et affichait `['A', '…']`, soit la première lettre de la chaîne « ABSENT ».
SONDE = r'''
import os, sys
src = open(%r, encoding="utf-8").read()
F = "    CA = []\n"
tete = src[:src.find(F) + len(F)]
g = {"__file__": %r, "__name__": "tete"}
%s
try:
    exec(compile(tete, "<tete>", "exec"), g)
except Exception as e:
    print("LEVE %%s" %% type(e).__name__)
v = g.get("CA", "ABSENT")
print("CA %%d" %% (len(v) if isinstance(v, list) else -1))
'''
BLOQUEUR = '''
class _B:
    def find_spec(self, n, p=None, c=None):
        if n == "ca_bundle":
            raise ImportError("rendu inimportable par le temoin")
        return None
sys.meta_path.insert(0, _B())
'''


def sonde(isole, bloquer=False):
    """Lance la tete d'aspirer.py dans un sous-processus reel. Rend (len(CA), stderr)."""
    code = SONDE % (ASPIRER, ASPIRER, BLOQUEUR if bloquer else "")
    cmd = [sys.executable] + (["-I"] if isole else []) + ["-c", code]
    # ⛔ cwd hors de outils/scripts/ : `-P` retire le cwd pour un `-c`, mais on ne veut pas
    #    que le sens NON isole reussisse par le cwd plutot que par la ligne de reparation.
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=RACINE, timeout=60)
    m = re.search(r"^CA (-?\d+)$", r.stdout, re.M)
    return (int(m.group(1)) if m else None), (r.stderr or "")


def modules_standard():
    """Les noms de modules de la bibliotheque standard de CE python (3.9 : pas de
    sys.stdlib_module_names)."""
    import sysconfig
    lib = sysconfig.get_paths()["stdlib"]
    noms = set(sys.builtin_module_names)
    try:
        for f in os.listdir(lib):
            if f.endswith(".py"):
                noms.add(f[:-3])
            elif os.path.isdir(os.path.join(lib, f)) and \
                    os.path.exists(os.path.join(lib, f, "__init__.py")):
                noms.add(f)
    except OSError:
        pass
    return noms


def code_seul(src):
    """La source sans ses commentaires — l'en-tete d'aspirer.py NOMME `import ca_bundle`
    dans le commentaire meme qui explique le defaut : un test textuel naif accuserait sa
    propre documentation (le piege de la coquille citee, 27/10)."""
    return "\n".join(l.split("#")[0] for l in src.splitlines())


def importe_voisin(src_nu, voisins, soi):
    """Les voisins que CE source importe, par ordre d'apparition. `src_nu` est le code SANS
    ses commentaires : l'en-tete des cinq scripts NOMME `import ca_bundle` dans le commentaire
    meme qui explique le defaut, et un test textuel naif accuserait sa propre documentation
    (le piege de la coquille citee, 27/10)."""
    out = []
    for m in re.finditer(r"^[ \t]*(?:import|from) ([a-z_][\w]*)", src_nu, re.M):
        if m.group(1) in voisins and m.group(1) != soi:
            out.append((m.start(), m.group(1)))
    return out


def etat_reparation(src_nu):
    """(repare, position de la reparation). -1 si absente."""
    i = src_nu.find("sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))")
    if i < 0:
        i = src_nu.find("sys.path.insert(0, os.path.join(RACINE,")
    return i


def recense(dossier=None):
    """PREDICAT STRUCTUREL, jamais une liste : tout .py de outils/scripts/ qui importe un
    VOISIN doit reparer sys.path, et le faire AVANT ce premier import. Une liste de cinq noms
    se perimerait au prochain script ecrit — defaut deja paye trois fois ici (setup_launchd.sh,
    rattrapage_jobs.sh, la table dossier -> job de ㊳)."""
    d = dossier or SCRIPTS
    voisins = {f[:-3] for f in os.listdir(d) if f.endswith(".py")}
    concernes, sans, apres = [], [], []
    for f in sorted(os.listdir(d)):
        if not f.endswith(".py"):
            continue
        nu = code_seul(open(os.path.join(d, f), encoding="utf-8").read())
        imp = importe_voisin(nu, voisins, f[:-3])
        if not imp:
            continue
        concernes.append(f)
        rep = etat_reparation(nu)
        if rep < 0:
            sans.append((f, [n for _, n in imp]))
        elif rep > imp[0][0]:
            apres.append((f, imp[0][1]))
    return concernes, sans, apres


def controler():
    ko, jouees = [], []

    def borne(nom, ok, detail=""):
        print("  %s %s%s" % ("✓" if ok else "✗", nom, (" — " + detail) if detail else ""))
        jouees.append(nom)
        if not ok:
            ko.append(nom)

    def fin():
        print("  %d/%d bornes de l'isolation des imports"
              % (len(jouees) - len(ko), len(jouees)))
        return 1 if ko else 0

    # ① d'abord : si les chemins sont faux, tout le reste est vert sur du vide.
    presents = [p for p in CIBLES + (CABUNDLE,) if os.path.isfile(p)]
    borne("① les chemins sont rendus — les cinq scripts et ca_bundle.py sont la",
          len(presents) == len(CIBLES) + 1,
          "%d/%d sous %s" % (len(presents), len(CIBLES) + 1, SCRIPTS))
    if len(presents) != len(CIBLES) + 1:
        return fin()

    concernes, sans, apres = recense()
    borne("② le predicat trouve un ensemble NON VIDE (sinon : vert sur rien)",
          len(concernes) >= 5, "%d script(s) importent un voisin" % len(concernes))
    borne("③ tout script important un voisin REPARE sys.path",
          not sans, "%d sans reparation%s"
          % (len(sans), (" — EN FAUTE : " + ", ".join(f for f, _ in sans)) if sans else ""))
    borne("④ ... et le fait AVANT son premier import de voisin (l'ORDRE)",
          not apres, "%d apres l'import%s"
          % (len(apres), (" — EN FAUTE : " + ", ".join(f for f, _ in apres)) if apres else ""))

    # ⑤ FABRIQUEE, et c'est la borne DECISIVE : sans elle, le predicat pourrait etre inerte et
    #    ③ ④ seraient vertes sur un detecteur qui ne detecte rien.
    with tempfile.TemporaryDirectory() as d:
        open(os.path.join(d, "ca_bundle.py"), "w").write("def args_curl(): return []\n")
        open(os.path.join(d, "fautif.py"), "w").write("import ca_bundle\nCA = []\n")
        open(os.path.join(d, "tardif.py"), "w").write(
            "import os, sys\nimport ca_bundle\n"
            "sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\n")
        c2, s2, a2 = recense(d)
        borne("⑤ FABRIQUEE : un script qui importe un voisin SANS reparer est DETECTE",
              [f for f, _ in s2] == ["fautif.py"] and [f for f, _ in a2] == ["tardif.py"],
              "concernes=%r sans=%r apres=%r" % (sorted(c2), [f for f, _ in s2], [f for f, _ in a2]))

    n_iso, _ = sonde(True)
    borne("⑥ sous un VRAI -I, la tete d'aspirer.py extraite rend CA NON VIDE",
          n_iso is not None and n_iso > 0, "len(CA) = %r" % (n_iso,))
    n_nu, _ = sonde(False)
    borne("⑦ sans -I, CA est non vide aussi (non-regression)",
          n_nu is not None and n_nu > 0, "len(CA) = %r" % (n_nu,))
    n_bl, err = sonde(False, bloquer=True)
    borne("⑧ ca_bundle inimportable : CA retombe a [] (le repli tient)",
          n_bl == 0, "len(CA) = %r" % (n_bl,))
    borne("⑨ ... et le repli SE DIT sur stderr, en nommant la cause",
          "ca_bundle non import" in err and "faisceau" in err,
          (err.strip().splitlines() or ["(rien sur stderr)"])[0][:72])

    # ⑩ TEXTUELLE, et sa limite est dite : seul aspirer.py a une tete executable hors contexte
    #    (les trois 5 bis sortent sur un sys.exit d'usage, controle_attributions.py pese 1 626
    #    lignes). Pour les quatre autres on exige donc le LITTERAL, comme le garde ② de
    #    l'assertion de tableau (18/10) et desarmement_git.py (27/10).
    muets = []
    for p in CIBLES:
        s = open(p, encoding="utf-8").read()
        if not re.search(r"except Exception as _e:(?:\n(?:\s*#[^\n]*|\s*)\n?)*?\s*print\(", s) \
                or "file=sys.stderr" not in s:
            muets.append(os.path.basename(p))
    borne("⑩ le repli PARLE dans les CINQ (exigence LITTERALE)", not muets,
          "muet(s) : %s" % ", ".join(muets) if muets else "les cinq parlent")

    # ⑪ ACCEPTEE — la premisse de ⑨ : args_curl() ne leve pas, donc l'except n'attrape que
    #    l'import. Aucun effet de bord : chemin() rend None avant de toucher au cache.
    sauve = list(sys.path)
    sys.path.insert(0, SCRIPTS)
    try:
        import ca_bundle as _cb
        _b, _d = _cb.BREW, _cb.CA_DIR
        try:
            _cb.BREW, _cb.CA_DIR = ("/nexistepas/cert.pem",), "/nexistepas"
            leve, val = None, _cb.args_curl()
        except Exception as e:                       # pragma: no cover
            leve, val = type(e).__name__, None
        finally:
            _cb.BREW, _cb.CA_DIR = _b, _d
    finally:
        sys.path[:] = sauve
    borne("⑪ ACCEPTEE : args_curl() ne leve pas, brew et ca/ masques -> []",
          leve is None and val == [], "leve=%r val=%r" % (leve, val))

    std = modules_standard()
    noms = sorted(f[:-3] for f in os.listdir(SCRIPTS) if f.endswith(".py"))
    coll = [n for n in noms if n in std]
    borne("⑫ aucun .py de outils/scripts/ ne masque un module standard",
          not coll, "%d .py contre %d modules%s"
          % (len(noms), len(std), (" — EN FAUTE : " + ", ".join(coll)) if coll else ""))

    nus = [os.path.basename(p) for p in CIBLES
           if re.search(r'"-k"|--insecure', open(p, encoding="utf-8").read())]
    borne("⑬ aucun -k ni --insecure dans les cinq", not nus,
          "en faute : %s" % ", ".join(nus) if nus else "les cinq sont propres")

    # ⑭ LES TROIS SITES DU HARNAIS. La tranche de controle_attributions.py est executee COMME SI
    #    elle etait le controle : sans `__file__` dans ses globals, la reparation leve NameError,
    #    non rattrape (seul SystemExit l'est), et le gate QUI ALIMENTE LA REFERENCE mourait.
    #    Les trois sites sont octet pour octet identiques (26/10) : une derive d'un seul suffit.
    hs = open(NR_SH, encoding="utf-8").read()
    n_site = hs.count('code = src[src.index("import sys, re, html, subprocess")')
    n_file = hs.count('"__file__": CTRL')
    n_ctrl = hs.count("CTRL = sys.argv[1]")
    borne("⑭ les sites du harnais qui executent la tranche fournissent __file__",
          n_site >= 1 and n_site == n_file == n_ctrl,
          "%d site(s), %d __file__, %d CTRL" % (n_site, n_file, n_ctrl))

    print("  ○ %d script(s) importent un voisin · 0 attendu sans reparation (BLOQUANT depuis"
          " le 28/11 : a 0 orphelin, le laisser non bloquant garantissait qu'il repourrisse)"
          % len(concernes))
    return fin()


if __name__ == "__main__":
    raise SystemExit(controler())
