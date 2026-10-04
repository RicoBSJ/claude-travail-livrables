#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""controle_clauses_parcours.py — un parcours fermé s'arrête-t-il tout seul ?

Usage : /usr/bin/python3 outils/scripts/controle_clauses_parcours.py [config.json]
        (l'argument sert à VALIDER LE TEST sur une config mutée, sans toucher au dépôt)
Sort en 0 si chaque job de leçon peut s'arrêter à la fin de son parcours,
en 1 si l'un d'eux produirait une leçon de trop.

NÉ D'UN INCIDENT (04/10/2026). revenus-passifs-lecon a produit une ONZIÈME leçon
d'un parcours commandé en DIX. Son prompt déclarait les 10 leçons à deux endroits
— préambule et feuille de route, dont les dix items étaient tous traités — mais
numérotait par « NN = nombre de fichiers existants + 1 » SANS LIMITE, et
« PARCOURS FERMÉ » y comptait zéro occurrence. Le job avait pourtant posé le bon
diagnostic dans son récapitulatif (« parcours de 10 leçons complété, leçon hors
feuille de route initiale ») : diagnostiquer la fin d'un parcours sans pouvoir
s'arrêter ne sert à rien.

Le relevé du même jour sur les neuf jobs de leçon a montré la vraie forme du trou :
les SIX parcours de 20 leçons portaient tous la clause et AUCUN n'était près de sa
limite ; les TROIS parcours courts, dont la limite était atteignable, étaient les
trois qui en étaient dépourvus (revenus-passifs 11/10, appli-ia 12/12,
astrologie-karmique 9/12). La clause avait été écrite pour les parcours qui n'en
avaient pas encore l'usage. C'est ce test qui rend le constat rejouable.

Ce que le test LIT, pour chaque job dont l'id finit par « -lecon » :
  — le nombre de leçons ANNONCÉ par le prompt (« en N LEÇONS », « (N leçons) ») ;
  — la présence d'une clause « ⛔ PARCOURS FERMÉ » ;
  — la présence d'une limite sur la numérotation (« dans la limite de N ») ;
  — le nombre réel de fichiers .docx du dossier du parcours.
    ⚠️ SEULS LES .docx. Le dossier porte aussi une fiche .md par leçon : sans le
    filtre, le compte est doublé et la clause paraîtrait se déclencher partout.
Ce que le test REFUSE : un parcours à N-1 fichiers ou plus, dont le prompt n'a pas
de clause de fermeture. À N-1, la prochaine exécution produit la dernière leçon ;
à N, elle en produit une de trop. Un job dont le statut est « arrete » est signalé
mais ne bloque pas.
"""
import json, os, re, sys, glob

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONF = sys.argv[1] if len(sys.argv) > 1 else os.path.join(RACINE, "jobs_config.json")

def annonce(p):
    for pat in (r"en\s+(\d+)\s+LEÇONS", r"\((\d+)\s+leçons\)", r"—\s*(\d+)\s+leçons\s*:"):
        m = re.search(pat, p, re.I)
        if m:
            return int(m.group(1))
    return None

def main():
    with open(CONF, encoding="utf-8") as f:
        jobs = [j for j in json.load(f)["jobs"] if j["id"].endswith("-lecon")]
    pb, avert, lignes = [], [], []
    for j in sorted(jobs, key=lambda x: x["id"]):
        p = j["prompt"]
        slug = j["id"][:-len("-lecon")]
        n = annonce(p)
        dossier = os.path.join(RACINE, "livrables", "lecons", slug)
        reels = len(glob.glob(os.path.join(dossier, "*.docx")))
        # ⚠️ NE PAS CHERCHER « ⛔ PARCOURS FERMÉ » : revenus-passifs écrit « ⛔ JOB ARRÊTÉ LE
        #    04/10/2026 — PARCOURS FERMÉ, 10 LEÇONS », et les prompts qui RACONTENT l'incident
        #    citent la phrase sans porter la clause. On cherche l'INSTRUCTION OPÉRANTE : le mot
        #    d'ordre « NE PRODUIS RIEN » à proximité de « PARCOURS FERMÉ » (04/10/2026).
        clause = bool(re.search(r"PARCOURS FERMÉ.{0,400}?NE PRODUIS RIEN", p, re.S))
        limite = bool(re.search(r"dans la limite de \d+", p))
        arrete = j.get("statut") == "arrete"
        etat = "arrêté" if arrete else "actif"
        lignes.append("  %-28s annoncé %-4s réels %-4s clause %-4s limite %-4s %s"
                      % (j["id"], n if n else "?", reels,
                         "oui" if clause else "NON", "oui" if limite else "NON", etat))
        if n is None:
            pb.append("%s : nombre de leçons non déclaré dans le prompt" % j["id"])
            continue
        if reels > n:
            # ⚠️ UN DÉBORDEMENT DÉJÀ TRAITÉ NE DOIT PAS BLOQUER POUR TOUJOURS. Le dépassement de
            #    revenus-passifs (11/10) est un fait historique : le job est arrêté, la leçon de
            #    trop est conservée et fichée. Un contrôle qui crie à chaque exécution sur un
            #    incident clos finit par ne plus être lu — c'est le défaut mesuré sur la passe D
            #    de controle_attributions le 04/10/2026. On le signale, on ne le refuse pas.
            if arrete and clause:
                avert.append("%s : %d leçons pour %d annoncées — débordement du 04/10/2026, "
                             "job arrêté et clause posée : incident clos, signalé pour mémoire"
                             % (j["id"], reels, n))
            else:
                pb.append("%s : %d leçons produites pour %d annoncées — le parcours a DÉBORDÉ "
                          "et le job tourne encore" % (j["id"], reels, n))
        elif reels == n and not clause and not arrete:
            pb.append("%s : %d/%d et AUCUNE clause de fermeture — la PROCHAINE exécution "
                      "produira une leçon de trop" % (j["id"], reels, n))
        elif reels == n - 1 and not clause and not arrete:
            pb.append("%s : %d/%d et AUCUNE clause de fermeture — la prochaine exécution "
                      "produira la dernière leçon, celle d'après une leçon de trop"
                      % (j["id"], reels, n))
        elif not clause and not arrete:
            pb.append("%s : %d/%d, pas de clause de fermeture (pas urgent, mais le trou est là)"
                      % (j["id"], reels, n))
        if clause and not limite and not arrete:
            pb.append("%s : clause présente mais la numérotation n'est pas bornée "
                      "(« dans la limite de N » absent)" % j["id"])
    print("Clauses de fermeture des parcours de leçons\n")
    print("\n".join(lignes))
    print()
    for x in avert:
        print("⚠️ " + x)
    if avert and not pb:
        print()
    if pb:
        for x in pb:
            print("⛔ " + x)
        sys.exit("%d parcours sans arrêt possible" % len(pb))
    print("✓ chaque parcours de leçons peut s'arrêter tout seul")

if __name__ == "__main__":
    main()
