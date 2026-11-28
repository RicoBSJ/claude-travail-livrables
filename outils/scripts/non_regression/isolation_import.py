#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""isolation_import.py — `aspirer.py` sonde-t-il AVEC le faisceau même sous `python3 -I` ?

POURQUOI (28/11/2026). `-I` implique `-P` : le dossier du script quitte `sys.path`, donc
`import ca_bundle` lève `ModuleNotFoundError`, l'`except Exception` l'avale, et `curl` part
SANS `--cacert`. Mesuré de bout en bout sur `https://www.has-sante.fr/`, les deux sondes
sous `-I` et espacées de 15 s : la version d'avant rend **HTTP 000 · curl 60 · NON LUE**,
la corrigée **200**. C'est le défaut du 18/10 par une autre porte — une source valide
écartée en silence —, et il est ATTEIGNABLE À LA MAIN : la consigne d'isolation de cette
session prescrit `-I` pour tout Python qui lit un fichier non fiable.

⛔ CE N'EST PAS UN DÉFAUT DE PRODUCTION, et il faut le dire : `0` occurrence de
`python3 -I` dans le hook, le harnais et `run_job.sh`, contre 50 `python3` nus.

🔴 ET LE FOND N'ÉTAIT PAS LE REPLI, C'ÉTAIT QU'IL ÉTAIT INDISCERNABLE. `args_curl()` NE
LÈVE PAS — `chemin()` rattrape `OSError` et rend `None`, d'où `[]` ; mesuré en masquant
brew ET `ca/`. Donc cet `except` n'attrape QUE l'import, c'est-à-dire un `ca_bundle` absent
du disque ou un `sys.path` perdu, et muet il rendait ces deux états cassés indiscernables
du repli légitime d'une machine sans brew. Un garde satisfait par un état cassé : le défaut
qui revient le plus souvent ici (`$SEMENCE` non vide, les deux photos vides, le `git` à 128).
⚠️ La docstring de `faisceau_5bis.py` attribue ce repli à « une machine sans brew » : c'est
le MÉCANISME qui est mal nommé, pas sa borne ④ — sur une telle machine l'import réussit et
c'est `args_curl()` qui rend `[]`, sans jamais passer par l'`except`.

CE QUE CE TÉMOIN GARDE, et ce qu'il ne garde pas :
  • ①  les chemins sont rendus — QUATRE dirname, ce script vivant un cran plus bas. Le bug
    à cinq occurrences (23/10, 27/10, 11/11 deux fois, 28/11) : avec trois, tout serait vert
    sur des fichiers absents.
  • ②  `aspirer.py` répare `sys.path` ET le fait AVANT son `import ca_bundle`. L'ORDRE est la
    moitié de la règle, comme pour le désarmement git du 27/10 : une borne de présence seule
    déclarerait conforme un fichier où la réparation vient après l'import.
  • ③ ④  la tête du fichier est EXTRAITE puis exécutée dans un sous-processus RÉEL, avec `-I`
    et sans — `CA` doit être non vide des deux côtés. Pas une copie de sa logique (15/10).
  • ⑤ ⑥  `ca_bundle` rendu inimportable : `CA` retombe à `[]` ET une ligne le DIT sur stderr.
    Les deux ne sont pas redondantes — c'est le silence qui était le défaut, pas le repli.
  • ⑦  ACCEPTÉE : `args_curl()` ne lève pas, brew et `ca/` masqués. C'est la PRÉMISSE de ⑥ —
    si elle devenait fausse, l'`except` attraperait aussi le repli légitime et la ligne de
    stderr accuserait une machine saine.
  • ⑧  aucun `.py` de `outils/scripts/` ne collide avec un module standard. C'est le risque
    que l'insert en position 0 CRÉE, et c'est exactement le danger du `json.py` planté que la
    consigne d'isolation veut écarter : on le mesure au lieu de le supposer.
  • ⑨  aucun `-k`, aucun `--insecure` : la chaîne reste validée entièrement.
  ⛔ CE QU'IL NE GARDE PAS : les QUATRE autres scripts qui importent un voisin sans réparer
    `sys.path` (`controle_ai_act.py`, `controle_astrologie_karmique.py`,
    `controle_attributions.py`, `controle_psychopathologie.py`). Ils sont RECENSÉS et
    imprimés, non bloquants : l'ordre ne nommait qu'`aspirer.py`, et les corriger demanderait
    de reprendre l'extraction de `faisceau_5bis.py`, ancrée sur `try:\n    import ca_bundle`.

Aucun réseau, aucun tiers — ce lot ne peut pas périmer sur la panne d'un site, contrairement
aux témoins qui ont bloqué TOUS les pushs les 15, 22 et 23/10.
Usage : python3 outils/scripts/non_regression/isolation_import.py [--autotest]
Sortie : 0 si les bornes tiennent, 1 sinon.
"""
import os, re, subprocess, sys

# ⚠️ QUATRE dirname — voir ① et la note de faisceau_5bis.py.
RACINE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
SCRIPTS = os.path.join(RACINE, "outils", "scripts")
ASPIRER = os.path.join(SCRIPTS, "aspirer.py")
CABUNDLE = os.path.join(SCRIPTS, "ca_bundle.py")
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


def voisins_non_repares():
    """Recensement : les scripts de outils/scripts/ qui importent un voisin SANS reparer
    sys.path. Non bloquant — l'ordre ne nommait qu'aspirer.py."""
    voisins = {f[:-3] for f in os.listdir(SCRIPTS) if f.endswith(".py")}
    out = []
    for f in sorted(os.listdir(SCRIPTS)):
        if not f.endswith(".py"):
            continue
        src = code_seul(open(os.path.join(SCRIPTS, f), encoding="utf-8").read())
        imp = sorted({m for m in re.findall(r"^\s*(?:import|from) ([a-z_][\w]*)", src, re.M)
                      if m in voisins and m != f[:-3]})
        if imp and "sys.path.insert" not in src:
            out.append((f, imp))
    return out


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
    presents = [p for p in (ASPIRER, CABUNDLE) if os.path.isfile(p)]
    borne("① les chemins sont rendus — aspirer.py et ca_bundle.py sont la ou on les cherche",
          len(presents) == 2, "%d/2 sous %s" % (len(presents), SCRIPTS))
    if len(presents) != 2:
        return fin()

    src = open(ASPIRER, encoding="utf-8").read()
    nu = code_seul(src)
    i_rep = nu.find("sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))")
    i_imp = next((m.start() for m in re.finditer(r"^\s*import ca_bundle\s*$", nu, re.M)), -1)
    borne("② aspirer.py repare sys.path AVANT son import ca_bundle",
          i_rep >= 0 and i_imp >= 0 and i_rep < i_imp,
          "reparation @%d, import @%d" % (i_rep, i_imp))

    n_iso, _ = sonde(True)
    borne("③ sous un VRAI -I, la tete extraite rend CA NON VIDE",
          n_iso is not None and n_iso > 0, "len(CA) = %r" % (n_iso,))
    n_nu, _ = sonde(False)
    borne("④ sans -I, CA est non vide aussi (non-regression)",
          n_nu is not None and n_nu > 0, "len(CA) = %r" % (n_nu,))

    n_bl, err = sonde(False, bloquer=True)
    borne("⑤ ca_bundle inimportable : CA retombe a [] (le repli tient)",
          n_bl == 0, "len(CA) = %r" % (n_bl,))
    dit = "ca_bundle non import" in err and "faisceau" in err
    borne("⑥ ... et le repli SE DIT sur stderr, en nommant la cause",
          dit, (err.strip().splitlines() or ["(rien sur stderr)"])[0][:72])

    # ⑦ ACCEPTÉE — la premisse de ⑥ : args_curl() ne leve pas, donc l'except n'attrape que
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
    borne("⑦ ACCEPTEE : args_curl() ne leve pas, brew et ca/ masques -> []",
          leve is None and val == [], "leve=%r val=%r" % (leve, val))

    std = modules_standard()
    noms = sorted(f[:-3] for f in os.listdir(SCRIPTS) if f.endswith(".py"))
    coll = [n for n in noms if n in std]
    borne("⑧ aucun .py de outils/scripts/ ne masque un module standard",
          not coll, "%d .py contre %d modules%s"
          % (len(noms), len(std), (" — EN FAUTE : " + ", ".join(coll)) if coll else ""))

    borne("⑨ aucun -k ni --insecure dans aspirer.py",
          not re.search(r'"-k"|--insecure', src), "la chaine reste validee entierement")

    reste = voisins_non_repares()
    print("  ○ scripts important un voisin SANS reparer sys.path : %d (NON bloquant) — %s"
          % (len(reste), ", ".join(f for f, _ in reste) if reste else "aucun"))
    return fin()


if __name__ == "__main__":
    raise SystemExit(controler())
