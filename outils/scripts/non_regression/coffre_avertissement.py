#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Le coffre Obsidian est-il relu AU MOMENT DU PUSH ? — aucun réseau, aucun tiers, 1,2 s.

🔴 17/11/2026 — POURQUOI CE TÉMOIN EXISTE. La fiche has-actualite du 16/11 portait QUATRE
   wikiliens écrits `[[…fiche.md]]` là où la règle du coffre veut `[[…fiche]]`. Les quatre
   cibles existaient sur le disque : le défaut était le SUFFIXE, pas la cible. `audit_vault.py`
   l'a dit, exactement, le 17/11 à 08:11, en nommant les quatre liens — et personne n'a pu
   refuser quoi que ce soit, parce que ce script est lancé 0 fois par le harnais, 0 fois par le
   hook, et 3 fois par `run_job.sh:433`, APRÈS `EXIT=0`, dans une branche qui imprime
   d'elle-même « l'audit n'interrompt rien ». Il EST dans `SURVEILLES` du hook, mais c'est un
   DÉCLENCHEMENT, pas une couverture — la distinction du 11/11, et lire « 0 orphelin » comme
   « tout est testé » en est la pire lecture. La faute a donc vécu du 16 au 17/11.

⛔ CE QUI EST BLOQUANT ET CE QUI NE L'EST PAS, ET LA FRONTIÈRE N'EST PAS UNE PRUDENCE VAGUE :
   · le VERDICT sur le coffre est un AVERTISSEMENT. Un lien cassé dans une fiche n'est pas une
     régression du dépôt, et refuser le push punirait le livrable qui passe — règle du 14/10,
     et un balayage rétrospectif ne valide pas un motif bloquant. En production, un faux refus
     coûte un livrable non publié ; un vrai manqué coûte une relecture.
   · ce TÉMOIN-CI est bloquant, comme tous les autres : si le détecteur cesse de mordre, ou si
     le bloc du harnais cesse de REMONTER ce qu'il dit, c'est bien le dépôt qui régresse.

⛔ Il ne peut pas se périmer comme les témoins qui ont bloqué TOUS les pushs les 15, 22 et
   23/10 : aucun tiers, aucune date, aucun fichier vivant dans ses neuf premières bornes — le
   coffre est FABRIQUÉ en tempfile (leçon du 22/10). Les bornes de structure lisent le harnais
   et le hook, jamais une copie de leurs motifs (règle du 15/10).
"""
import os
import re
import subprocess
import sys
import tempfile

# ⚠️ QUATRE `dirname` : ce script vit dans `outils/scripts/non_regression/`, un cran plus bas
#    que les contrôles. Copier l'arithmétique des TROIS `dirname` d'un contrôle est le bug de
#    tolerance_page_morte.py (23/10), de coherence_skill.py (27/10) et de
#    controle_integrite_livrables.py (11/11) — trois fois payé. L'assertion le dit tout de suite.
RACINE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
assert os.path.isdir(os.path.join(RACINE, "outils", "scripts")), \
    "RACINE mal calculée : %s" % RACINE

AUDIT = os.path.join(RACINE, "outils", "scripts", "audit_vault.py")
HARNAIS = os.path.join(RACINE, "outils", "scripts", "non_regression.sh")
HOOK = os.path.join(RACINE, "outils", "scripts", "hooks", "pre-push")

RE_C7 = re.compile(r"^  (?P<etat>[✓✗]) Liens wiki résolus \(règle Obsidian\)"
                   r"(?: \((?P<n>\d+) liens\)| — (?P<pb>\d+) problème\(s\))", re.M)


def code_seul(src):
    """Le texte d'un script SANS ses lignes entièrement commentées. Un recensement textuel
    qui compte une référence en commentaire n'est pas un recensement d'appels — leçon du
    27/10, et c'est le sabotage S10 du 11/11 qui l'a prouvée dans categories_hook.py."""
    return "\n".join(l for l in src.splitlines() if not l.lstrip().startswith("#"))


def joue(racine):
    """Le VRAI audit_vault.py sur un coffre fabriqué, par son VRAI point d'entrée (`--racine`).
    Aucune logique recopiée : on lance le script, on lit sa sortie et son code de sortie."""
    r = subprocess.run([sys.executable, AUDIT, "--racine", racine, "--sans-couleur"],
                       capture_output=True, text=True, timeout=60)
    return r.returncode, r.stdout + r.stderr


def coffre(liens_a, extras=None, source_a="a.docx", controles=None):
    """Un coffre minimal : deux fiches de leçon, leurs deux .docx, et les liens demandés."""
    d = tempfile.mkdtemp(prefix="coffre_")
    lec = os.path.join(d, "livrables", "lecons", "essai")
    os.makedirs(lec)
    os.makedirs(os.path.join(d, "sources", "veille", "serie"))
    os.makedirs(os.path.join(d, "livrables", "controles"))
    for nom in ("a.docx", "b.docx"):
        open(os.path.join(lec, nom), "w").close()
    open(os.path.join(lec, "a.md"), "w", encoding="utf-8").write(
        "---\ntype: fiche-document\nsource: %s\n---\n# a\n%s\n" % (source_a, "\n".join(liens_a)))
    open(os.path.join(lec, "b.md"), "w", encoding="utf-8").write(
        "---\ntype: fiche-document\nsource: b.docx\n---\n# b\n")
    for nom, txt in (controles or {}).items():
        open(os.path.join(d, "livrables", "controles", nom), "w", encoding="utf-8").write(txt)
    for chemin, txt in (extras or {}).items():
        open(os.path.join(d, chemin), "w", encoding="utf-8").write(txt)
    return d


def ligne_c7(out):
    """La ligne du contrôle des liens, telle que l'audit l'imprime — un détail d'alerte doit
    être lisible : 200 caractères coupés au milieu d'un mot ne le sont pas (leçon du 06/11)."""
    m = RE_C7.search(out)
    return m.group(0).strip() if m else "AUCUNE ligne « Liens wiki résolus » dans la sortie"


def autotest():
    jouees, ko = [], []

    def borne(nom, cond, detail=""):
        jouees.append(nom)
        if not cond:
            ko.append("%s%s" % (nom, (" — " + detail) if detail else ""))

    # ── ①→⑨ : LE VRAI AUDIT, SUR DES COFFRES FABRIQUÉS ────────────────────────────────
    # ① ACCEPTÉE — la forme conforme du coffre ne doit RIEN produire. Sans elle, rien
    #    n'empêche de resserrer le motif demain jusqu'à accuser les 1 475 liens vivants.
    code, out = joue(coffre(["[[b]]"]))
    m = RE_C7.search(out)
    borne("① ACCEPTÉE : [[b]] sans suffixe → aucun problème",
          bool(m) and m.group("etat") == "✓" and m.group("n") == "1", ligne_c7(out))
    borne("② l'audit RÉEL sort en 0 sur un coffre conforme", code == 0, "code=%d" % code)

    # ③ LE DÉFAUT DU 16/11, à l'identique : la cible EXISTE, c'est le suffixe qui est faux.
    code, out = joue(coffre(["[[b.md]]"]))
    m = RE_C7.search(out)
    borne("③ le défaut du 16/11 : [[b.md]] dont b.md EXISTE → signalé",
          bool(m) and m.group("etat") == "✗" and m.group("pb") == "1", ligne_c7(out))
    borne("④ et le message NOMME le lien fautif", "→ [[b.md]]" in out,
          "un décompte sans le lien n'est pas actionnable")
    # ⑤ l'audit RÉEL refuse (exit 1). C'est la borne qui établit que le non-refus au push est
    #    une DÉCISION du harnais, et non une impuissance du détecteur.
    borne("⑤ l'audit RÉEL sort en 1 sur un lien cassé — le non-refus est une décision",
          code == 1, "code=%d" % code)

    # ⑥ ACCEPTÉE — un lien `[[x.docx]]` se résout par le CHEMIN, pas par l'index des notes :
    #    c'est la forme `Document source : [[…​.docx]]`, et c'est elle qui a imposé d'ancrer le
    #    motif de la correction du 17/11 sur `.fiche.md]]` et non sur `.md]]`.
    code, out = joue(coffre(["[[a.docx]]"]))
    m = RE_C7.search(out)
    borne("⑥ ACCEPTÉE : [[a.docx]] existant → non signalé (résolu par le chemin)",
          bool(m) and m.group("etat") == "✓", ligne_c7(out))

    # ⑦ et un .docx qui n'existe pas doit être signalé — sans quoi ⑥ exempterait tout.
    code, out = joue(coffre(["[[absent.docx]]"]))
    m = RE_C7.search(out)
    borne("⑦ [[absent.docx]] → signalé", bool(m) and m.group("etat") == "✗", ligne_c7(out))

    # ⑧ une cible qui n'existe nulle part : le contrôle ne juge pas que des suffixes.
    code, out = joue(coffre(["[[jamais-vu]]"]))
    m = RE_C7.search(out)
    borne("⑧ [[jamais-vu]] → signalé", bool(m) and m.group("etat") == "✗", ligne_c7(out))

    # ⑨ ACCEPTÉE — une note de `livrables/controles/` est une cible LÉGITIME (régression du
    #    15/09 : sans elle, [[2026-09-13_controle-livrables]] passait pour cassé).
    code, out = joue(coffre(["[[note-de-controle]]"],
                            controles={"note-de-controle.md": "# note\n"}))
    m = RE_C7.search(out)
    borne("⑨ ACCEPTÉE : une note de livrables/controles/ est une cible légitime (15/09)",
          bool(m) and m.group("etat") == "✓", ligne_c7(out))

    # ⑩ c9 ne rend plus un ✓ sur un `git` en échec. Mesuré le 17/11 : sur un coffre qui n'est
    #    pas un dépôt, git répond 128, stdout est VIDE, donc `pb` était vide et le contrôle
    #    imprimait « ✓ Aucune fiche ne partirait à l'auto-push (0 fichier(s)) » — un vert sur
    #    une question qu'il n'avait pas pu poser. Classe du témoin de supprimer_job.sh (27/10).
    borne("⑩ la portée de l'auto-push se DIT non vérifiable quand git échoue",
          "Portée de l'auto-push — non vérifiable" in out
          and "Aucune fiche ne partirait" not in out, ligne_c7(out))

    # ── ⑪→⑰ : LA STRUCTURE DU HARNAIS ET DU HOOK ───────────────────────────────────────
    #    Pourquoi du LITTÉRAL ici : l'effet « le push n'est pas refusé » ne s'exerce qu'en
    #    sabotant le coffre RÉEL pendant un push réel. On exige donc la forme, comme le garde
    #    ② de l'assertion de tableau (18/10) et desarmement_git.py (27/10) — et on le dit.
    src = open(HARNAIS, encoding="utf-8").read()
    mb = re.search(r"^bloc_coffre \(\) \{\n(.*?)^\}$", src, re.S | re.M)
    borne("⑪ bloc_coffre existe dans le harnais", bool(mb))
    corps = mb.group(1) if mb else ""
    nu = code_seul(corps)

    borne("⑫ bloc_coffre APPELLE audit_vault.py — une fonction jamais appelée n'écrit "
          "dans aucun log (27/10)", "outils/scripts/audit_vault.py" in nu)

    # ⑬ il REMONTE les lignes de l'audit. Le gate --docs a imprimé pendant huit jours un ✓/✗
    #    en laissant le détail dans un fichier temporaire (27/10 pour l'étiquette HAS, 05/11
    #    pour les murs lus) : une alerte que personne ne lit n'existe pas.
    borne("⑬ bloc_coffre REMONTE la sortie de l'audit, pas seulement un ✓/✗",
          bool(re.search(r"(grep|sed)[^\n]*\"\$VOUT\"", nu)))

    # ⑭ AVERTISSEMENT : la branche qui teste le code de sortie du verdict ne doit PAS poser le
    #    drapeau d'échec du bloc. C'est la borne qui porte l'ordre « en avertissement d'abord ».
    mv = re.search(r"if \[ \"\$VCODE\" != \"0\" \]; then\n(.*?)\n  fi", nu, re.S)
    borne("⑭ le code de sortie du VERDICT n'est pas reporté dans le KO du bloc "
          "(avertissement)", bool(mv) and "CF_KO=1" not in mv.group(1),
          "la branche du verdict pose un drapeau d'échec : le push serait REFUSÉ")

    # ⑮ mais un audit MUET refuse, lui : si le contrôle des liens n'imprime plus sa ligne, on
    #    ne sait plus rien du coffre, et ça n'est pas un contenu, c'est le détecteur.
    borne("⑮ une ligne du contrôle des liens ABSENTE fait échouer le bloc",
          bool(re.search(r"Liens wiki résolus", nu)) and nu.count("CF_KO=1") >= 1)

    # ⑯ le mode --coffre existe et APPELLE le bloc (il ne le recopie pas — 15/10), et le bloc
    #    est joué par le chemin COMMUN et par le mode --integrite. MESURÉ le 17/11 : les 651
    #    fichiers du coffre suivis par git sont TOUS dans la catégorie LIVRABLES du hook, donc
    #    une catégorie COFFRE dédiée serait du code mort — ce sont ces deux appels qui portent
    #    la couverture, et c'est eux qu'il faut garder.
    snu = code_seul(src)
    # 🔴 PORTÉE AU BLOC DU MODE, PAS À UN COMPTE GLOBAL : mon premier jet exigeait
    #    « au moins 4 occurrences de bloc_coffre », donc retirer un appel AILLEURS la faisait
    #    tomber avec ⑰ — deux bornes qui tombent ensemble n'en font qu'une (26/10). Les
    #    sabotages S1 et S2 l'ont dit ; ⑯ ne juge plus que SON mode.
    mc = re.search(r'if \[ "\$MODE" = "--coffre" \]; then\n(.*?)\nfi', snu, re.S)
    borne("⑯ le mode --coffre existe et APPELLE bloc_coffre (il ne le recopie pas)",
          bool(mc) and "bloc_coffre" in mc.group(1))
    mi = re.search(r'if \[ "\$MODE" = "--integrite" \]; then\n(.*?)\nfi', snu, re.S)
    borne("⑰ bloc_coffre est joué par le mode --integrite ET par le chemin commun",
          bool(mi) and "bloc_coffre" in mi.group(1)
          and bool(re.search(r"^bloc_coffre \|\| exit 1$", snu, re.M)),
          "le push d'une fiche ne déclencherait plus rien sur le coffre")

    # ⑱ ACCEPTÉE, ET C'EST ELLE QUI INTERDIT UNE LISTE : chaque fichier du coffre énuméré
    #    DEPUIS GIT, plus un nom FABRIQUÉ qui n'existe pas, doit être couvert par la catégorie
    #    LIVRABLES LUE DANS LE HOOK. Un motif, jamais une liste (11/11) — et sans le nom
    #    fabriqué, rien n'empêcherait de revenir à l'énumération des 651 chemins.
    ml = re.search(r"^LIVRABLES='([^']+)'", code_seul(open(HOOK, encoding="utf-8").read()), re.M)
    borne("⑱ la catégorie LIVRABLES est lue dans le hook", bool(ml))
    if ml:
        rx = re.compile(ml.group(1))
        fichiers = subprocess.run(
            ["git", "-C", RACINE, "ls-files", "livrables/lecons", "sources/veille",
             "livrables/controles"], capture_output=True, text=True, timeout=60).stdout.split()
        vault = [f for f in fichiers if f.endswith((".md", ".docx"))]
        nus = [f for f in vault if not rx.search(f)]
        borne("⑲ ACCEPTÉE : les %d fichiers du coffre sont couverts par LIVRABLES" % len(vault),
              bool(vault) and not nus, "non couverts : %s" % nus[:5])
        borne("⑳ ACCEPTÉE : un nom de fiche FABRIQUÉ est déjà couvert — un motif, pas une liste",
              bool(rx.search("sources/veille/serie-neuve/2099-01-01_veille_x.fiche.md")))

    # ㉑ LE `sed` DU HARNAIS, LU DANS LE HARNAIS, appliqué à la ligne que ce témoin imprime
    #    RÉELLEMENT. Le 04/11, un garde de compte dont le motif n'appariait pas la ligne qu'il
    #    allait vraiment lire a fait REFUSER TOUS LES PUSHS du dépôt sur un dépôt sain — et une
    #    comparaison inversée aurait tout accepté. L'ancre est ASCII SANS ACCENT (« bornes du
    #    coffre ») pour la même raison : une dérive de libellé accentué est passée par là.
    #    ⛔ On LIT le motif, on ne le recopie pas — ma borne ⑩ de categories_hook.py recopiait
    #    le sed du harnais le 11/11, et une dérive DANS LES DEUX la laissait verte (15/10).
    jouees.append("㉑ le sed du harnais apparie la ligne réellement imprimée")
    msed = re.search(r"^\s*LU=\$\(sed -n 's([^']+)' \"\$OUT\"\)", 
                     re.sub(r"(?m)^bloc_coffre \(\) \{", "bloc_coffre () {",
                            src[src.find("bloc_coffre () {"):]), re.M)
    ligne = "  %d/%d bornes du coffre en avertissement" % (len(jouees) - len(ko), len(jouees))
    lu = ""
    if msed:
        import subprocess as _sp
        lu = _sp.run(["sed", "-n", "s" + msed.group(1)], input=ligne + "\n",
                     capture_output=True, text=True).stdout.strip()
    if lu != str(len(jouees)):
        ko.append("㉑ le sed du harnais apparie la ligne réellement imprimée — lu=%r, "
                  "attendu %d : le garde de compte ne lirait pas le dénominateur" % (lu, len(jouees)))

    # ㉒ LE MOTIF DE REMONTÉE, LU DANS LE HARNAIS, appliqué à la ligne de DÉTAIL que l'audit
    #    imprime RÉELLEMENT — celle qui NOMME le lien fautif. C'est elle qui a attrapé mon
    #    premier jet : le motif n'appariait que les lignes à deux espaces, donc le bloc
    #    remontait « 1 problème(s) » sans dire lequel, exactement le reproche que la borne ④
    #    fait au contrôle. Même forme que ㉑ : on lit le motif du harnais, on ne le recopie pas.
    jouees.append("㉒ le motif de remontée apparie la ligne qui NOMME le lien")
    DETAIL = ("      2026-11-16_veille_has-actualite.fiche.md → "
              "[[2026-11-09_veille_has-actualite.fiche.md]]")
    mg = re.search(r"^\s*grep -E '([^']+)' \"\$VOUT\"", corps, re.M)
    vu = ""
    if mg:
        import subprocess as _sp
        vu = _sp.run(["grep", "-E", mg.group(1)], input=DETAIL + "\n",
                     capture_output=True, text=True).stdout.strip()
    if vu != DETAIL.strip():
        ko.append("㉒ le motif de remontée apparie la ligne qui NOMME le lien — vu=%r : le "
                  "bloc imprimerait un décompte sans dire QUEL lien est cassé" % vu[:60])

    for x in ko:
        print("  ✗ " + x)
    print("  %d/%d bornes du coffre en avertissement" % (len(jouees) - len(ko), len(jouees)))
    return 1 if ko else 0


if __name__ == "__main__":
    if "--racine" in sys.argv:
        print(RACINE)
        sys.exit(0)
    sys.exit(autotest())
