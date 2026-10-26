#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""faisceau_5bis.py — les trois étapes 5 bis sondent-elles AVEC le faisceau de certificats ?

POURQUOI (26/10/2026). Les trois contrôles 5 bis appelaient `curl` SANS `--cacert`, alors que
`aspirer.py`, `controle_attributions.py`, `balayer_adresses.py` et les huit prompts de job le
passent depuis le 18/10. Mesuré sur l'hôte même que `controle_psychopathologie.py` sonde —
deux URL `has-sante.fr/jcms/` citées par ses leçons : **000 · exit 60 sans le faisceau,
200 · exit 0 avec**. Conséquence, et elle était silencieuse : son motif (1) s'écrit
`if pdfs and not any(…)`, donc une page vide le rend INERTE. Le portage a rendu quatre refus
exacts sur treize leçons, et la mesure à la main l'a confirmé — 1 à 12 PDF liés sur la page
jcms, zéro dans les ressources des documents.

CE QUE CE TÉMOIN GARDE, et ce qu'il ne garde pas :
  • ① ② ③  chaque `subprocess.run(["curl"…])` des trois porte le faisceau — comptage, donc un
    site ajouté sans faisceau fait crier. ⚠️ BORNE TEXTUELLE : un curl bâti dans une variable
    y échapperait. Les trois l'écrivent en littéral, c'est mesuré, et c'est la seule forme
    que le dépôt emploie.
  • ④  le bloc d'import est EXTRAIT DES FICHIERS puis exécuté — pas une copie de sa logique —
    avec `ca_bundle` rendu inimportable : `CA` doit retomber à `[]`. C'est le principe du
    18/10 enfin prouvé : sur une machine sans brew, les contrôles repassent au magasin système
    au lieu de mourir.
  • ⑤  et avec `ca_bundle` importable, `CA` doit ÉGALER `ca_bundle.args_curl()` — sans quoi
    un chemin en dur passerait ④ comme ① ② ③ (c'est le défaut que `ca_bundle.py` portait
    lui-même jusqu'au 26/10 pour ses intermédiaires).
  • ⑥  aucun `-k`, aucun `--insecure` : la chaîne est validée entièrement, rien n'est désactivé.
  • ⑦  RACINE est RENDUE. Le piège du 23/10 : ce script vit un cran plus bas que les contrôles,
    donc QUATRE dirname. Avec trois, les chemins pointeraient à côté et toutes les bornes
    seraient vertes sur des fichiers absents.

Aucun réseau. Usage : python3 outils/scripts/non_regression/faisceau_5bis.py [--autotest]
Sortie : 0 si les sept bornes tiennent, 1 sinon.
"""
import os, re, sys

# ⚠️ QUATRE dirname — voir ⑦ et la note de tolerance_page_morte.py (25/10/2026).
RACINE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
SCRIPTS = os.path.join(RACINE, "outils", "scripts")
CTL = ("controle_astrologie_karmique.py", "controle_psychopathologie.py",
       "controle_ai_act.py")
DEBUT, FIN = "try:\n    import ca_bundle", "    CA = []\n"


class _Bloqueur:
    """Rend `import ca_bundle` impossible, pour exercer l'except des contrôles."""

    def find_spec(self, nom, chemin=None, cible=None):
        if nom == "ca_bundle":
            raise ImportError("ca_bundle rendu inimportable par le témoin")
        return None


def bloc_import(src):
    """Le bloc try/except DU FICHIER, tel quel. None s'il n'y est pas."""
    i = src.find(DEBUT)
    if i < 0:
        return None
    j = src.find(FIN, i)
    return src[i:j + len(FIN)] if j >= 0 else None


def _exec(bloc, bloquer):
    g = {}
    sauve_modules = sys.modules.pop("ca_bundle", None)
    sauve_path = list(sys.path)
    try:
        if bloquer:
            sys.meta_path.insert(0, _Bloqueur())
        else:
            sys.path.insert(0, SCRIPTS)
        exec(compile(bloc, "<bloc extrait>", "exec"), g)
    finally:
        if bloquer:
            sys.meta_path[:] = [m for m in sys.meta_path if not isinstance(m, _Bloqueur)]
        sys.path[:] = sauve_path
        sys.modules.pop("ca_bundle", None)
        if sauve_modules is not None:
            sys.modules["ca_bundle"] = sauve_modules
    return g.get("CA", "ABSENT")


def controler():
    # ⚠️ 26/10/2026 — `jouees` N'EST PAS DECORATIF, IL EST NÉ D'UN SABOTAGE QUI N'A PAS MORDU.
    #    La premiere version imprimait un denominateur EN DUR et un numerateur « bornes moins
    #    echecs » : retirer une borne du lot laissait donc « 7/7 » et le harnais sortait en 0.
    #    C'est la regle du 15/10 (« un garde qui ne fait pas sortir en 1 est decoratif ») prise
    #    par l'autre bout — le garde existait, c'est le NOMBRE qu'il lisait qui ne bougeait pas.
    #    Le denominateur est desormais le nombre de bornes REELLEMENT jouees, et c'est LUI que
    #    le harnais lit (ATTENDU_CB5).
    ko, jouees = [], []

    def borne(nom, ok, detail=""):
        print("  %s %s%s" % ("✓" if ok else "✗", nom, (" — " + detail) if detail else ""))
        jouees.append(nom)
        if not ok:
            ko.append(nom)

    # ⑦ d'abord : si RACINE est fausse, tout le reste est vert sur du vide.
    presents = [c for c in CTL if os.path.isfile(os.path.join(SCRIPTS, c))]
    borne("⑦ RACINE est rendue — les trois contrôles sont là où ce script les cherche",
          len(presents) == len(CTL),
          "%d/%d sous %s" % (len(presents), len(CTL), SCRIPTS))
    if len(presents) != len(CTL):
        print("  %d/%d bornes du faisceau des étapes 5 bis"
              % (len(jouees) - len(ko), len(jouees)))
        return 1

    srcs, blocs = {}, {}
    for i, c in enumerate(CTL, 1):
        src = open(os.path.join(SCRIPTS, c), encoding="utf-8").read()
        srcs[c] = src
        blocs[c] = bloc_import(src)
        n_curl = len(re.findall(r'subprocess\.run\(\["curl"', src))
        n_ca = src.count("+ CA +")
        borne("%s %-32s chaque curl porte le faisceau"
              % ("①②③"[i - 1], c), n_curl >= 1 and n_curl == n_ca,
              "%d curl, %d porteur(s)" % (n_curl, n_ca))

    manque = [c for c in CTL if blocs[c] is None]
    if manque:
        borne("④ le repli sans ca_bundle rend CA = []", False,
              "bloc try/except introuvable dans : %s" % ", ".join(manque))
        borne("⑤ CA vaut ca_bundle.args_curl(), pas un chemin en dur", False, "idem")
    else:
        sans = {c: _exec(blocs[c], True) for c in CTL}
        borne("④ sans ca_bundle importable, CA retombe à [] (repli d'avant le faisceau)",
              all(v == [] for v in sans.values()),
              ", ".join("%s=%r" % (c.split("_")[1][:5], v) for c, v in sans.items()))
        sys.path.insert(0, SCRIPTS)
        try:
            import ca_bundle
            attendu = ca_bundle.args_curl()
        finally:
            sys.path.pop(0)
        avec = {c: _exec(blocs[c], False) for c in CTL}
        borne("⑤ CA vaut ca_bundle.args_curl(), pas un chemin en dur",
              all(v == attendu for v in avec.values()),
              "attendu %r" % (attendu[:1] + ["…"] if attendu else []))

    nus = [c for c in CTL if re.search(r'"-k"|--insecure', srcs[c])]
    borne("⑥ aucun -k ni --insecure — la chaîne est validée entièrement", not nus,
          "en faute : %s" % ", ".join(nus) if nus else "les trois sont propres")

    print("  %d/%d bornes du faisceau des étapes 5 bis"
          % (len(jouees) - len(ko), len(jouees)))
    return 1 if ko else 0


if __name__ == "__main__":
    raise SystemExit(controler())
