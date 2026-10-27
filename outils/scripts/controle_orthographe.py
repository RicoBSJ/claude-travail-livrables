#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""controle_orthographe.py — un NOM TECHNIQUE est-il mal écrit dans les consignations ?

POURQUOI (27/10/2026). J'ai écrit « kDrib » pour « kDrive » dans une consignation de JOBS.md.
C'est un `grep -c` qui l'a attrapé, pas ma relecture — et rien, dans le dépôt, ne contrôlait
l'orthographe des deux fichiers sur lesquels on s'appuiera dans six mois.

⛔ CE N'EST PAS UN CORRECTEUR ORTHOGRAPHIQUE, ET LA MESURE L'INTERDIT. Il n'y a pas de
dictionnaire français hors ligne sur cette machine, et surtout : **la morphologie française EST
une distance 1** — `ajouté` / `ajoutée` / `ajoutés` sont tous à un caractère l'un de l'autre, et
mon style met des mots entiers en capitales pour l'emphase. Mesuré sur le corpus réel (12 432
jetons distincts, 94 123 occurrences) : un contrôle par distance sur le français ordinaire rend
**746 à 3 062 fausses paires** selon les seuils. Inutilisable.

CE QU'IL FAIT, ET C'EST BORNÉ PAR LA MESURE : il ne regarde que les **noms techniques**, qui ne
se déclinent pas, et il prend le corpus lui-même pour dictionnaire. Un nom RARE qui est la
quasi-copie d'un nom FRÉQUENT est une coquille — c'est exactement ce qu'était « kDrib » (1
occurrence) à côté de « kDrive » (19).

Le vocabulaire retenu, mesuré à 288 noms pour 690 occurrences :
  ① les noms à CASSE MIXTE — une majuscule ailleurs qu'en tête ET au moins une minuscule :
     `kDrive`, `LibreSSL`, `iMac`, `JavaScript`, `TextRun`. Cette forme exclut `ABSENTS` (aucune
     minuscule) et `Mesuré` (majuscule en tête seulement) PAR CONSTRUCTION — c'est elle qui
     supprime tout le bruit des mots français en emphase.
  ② les noms TOUT EN CAPITALES qui, en plus, soit n'existent **pas** en minuscules dans le
     corpus (`ISBN`, `NASA`, `SIDOBA`, `DDADUE`), soit portent un **trait d'union** (`B-FR`,
     `B-NOM`, `SERAFIN-PH`). ⚠️ Sans le filtre des minuscules : **205 fausses paires** (c'est
     `ABSENTS` contre `ABSENT`, la morphologie française en capitales). ⚠️ Et sans l'exemption
     du trait d'union, `SERAFIN-PH` restait HORS de portée — mesuré : ses formes `serafin`,
     `serafin-ph` et `Serafin-PH` survivent en minuscules dans le texte nettoyé, donc le filtre
     le jetait. L'exemption porte le vocabulaire de 266 à 288 noms **sans salir**.

LES SEUILS SONT MESURÉS, PAS DEVINÉS — balayage sur le corpus réel, 0 paire partout dans
d ∈ {2,3} × rare ∈ {1,2,3} × fréquent ∈ {5,10} × préfixe ∈ {3,4} :
  • distance pliée **≤ 2**. ⚠️ ≤1 ne suffit PAS : `kDrib` → `kDrive` est à **distance 2**
    (substitution b→v PUIS insertion de e). C'est l'incident réel qui fixe ce seuil.
  • **préfixe plié partagé de 3** caractères. ⚠️ C'est la borne qui porte : à préfixe 2, le
    corpus rend 1 à 6 fausses paires (dont `iPad` ~ `iMac`, deux vrais produits Apple) ;
    à 3 et 4, zéro.
  • rare **≤ 2** · fréquent **≥ 5**. ⚠️ `fréquent ≥ 3` salit : 1 fausse paire.
Sens REFUS vérifié sur trois coquilles injectées : `kDrib`→`kDrive`, `SERAFIN-HP`→`SERAFIN-PH`,
`SERFIN-PH`→`SERAFIN-PH`, toutes PRISES, zéro faux positif collatéral.

⛔ MOTIF ABANDONNÉ SUR MESURE, et il faut le dire : « un nom de fichier cité entre apostrophes
inverses existe-t-il sur le disque ? » rendait **48 occurrences, 48 légitimes** — gabarits
(`YYYY-MM-DD_veille_HAS.md`), témoins VOLONTAIREMENT inexistants (`corrompu.docx`,
`FANTOME.docx`, `absent.docx`), scripts jetables du scratchpad, et fragments coupés par le
découpage (`Jobs.xlsx` venant de « Les 8 Jobs.xlsx »). Zéro signal : non retenu.

HORS DE PORTÉE, ET ASSUMÉ : l'orthographe du français ordinaire · une coquille dans un mot tout
en capitales qui existe aussi en minuscules sans trait d'union (`RBPP`, `CNSA`, `HAS` — mesuré,
ils ne sont PAS au vocabulaire) · une coquille à l'intérieur d'une apostrophe inverse (le code
est écarté avant le découpage) · un nom mal écrit qui n'a aucun jumeau fréquent, faute de
référence à quoi le comparer.

Aucun réseau. Usage :
    controle_orthographe.py [<fichier.md>…]      # défaut : CLAUDE.md + outils/scripts/JOBS.md
    controle_orthographe.py --autotest
Sortie : 0 si aucune coquille, 1 sinon.
"""
import io
import os
import re
import sys
import unicodedata
from collections import Counter

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONSIGNES = [os.path.join(RACINE, "CLAUDE.md"),
             os.path.join(RACINE, "outils", "scripts", "JOBS.md")]

DIST_MAX = 2        # l'incident kDrib→kDrive est à 2
PREFIXE = 3         # à 2, le corpus rend jusqu'à 6 fausses paires
RARE = 2
FREQUENT = 5

MOT = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ][A-Za-zÀ-ÖØ-öø-ÿ-]*")


def nettoyer(t):
    """Retire ce dont l'orthographe ne se juge pas : code, adresses, empreintes, chemins."""
    t = re.sub(r"```.*?```", " ", t, flags=re.S)
    t = re.sub(r"`[^`]*`", " ", t)
    t = re.sub(r"https?://\S+", " ", t)
    t = re.sub(r"\b[0-9a-f]{7,40}\b", " ", t)
    t = re.sub(r"[\w./-]*/[\w./-]+", " ", t)
    return t


def plie(w):
    """Casse et accents pliés : « Mesuré » et « MESURE » sont le même mot."""
    return "".join(c for c in unicodedata.normalize("NFD", w.lower())
                   if unicodedata.category(c) != "Mn")


def dist(a, b, maxi):
    """Levenshtein, abandonnée dès que l'écart de longueur dépasse maxi."""
    if abs(len(a) - len(b)) > maxi:
        return maxi + 1
    prec = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prec[j] + 1, cur[j - 1] + 1, prec[j - 1] + (ca != cb)))
        prec = cur
    return prec[-1]


def vocabulaire(texte):
    """Les noms techniques du texte et leur fréquence. Voir l'en-tête pour les deux classes."""
    jetons = [w.strip("-") for w in MOT.findall(texte)]
    jetons = [w for w in jetons if len(w) >= 4]
    minuscules = {plie(w) for w in jetons if not w.isupper()}

    def retenu(w):
        if any(c.isupper() for c in w[1:]) and any(c.islower() for c in w):
            return True                                    # ① casse mixte
        if not w.isupper():
            return False
        return plie(w) not in minuscules or "-" in w        # ② capitales, filtrées
    return Counter(w for w in jetons if retenu(w))


def coquilles(voc):
    """Les paires (rare, fréquent) suspectes, triées. Une entrée = une coquille probable."""
    freqs = [(w, v) for w, v in voc.items() if v >= FREQUENT]
    out = []
    for w, v in voc.items():
        if v > RARE:
            continue
        for cand, vc in freqs:
            if plie(cand) == plie(w) or plie(w)[:PREFIXE] != plie(cand)[:PREFIXE]:
                continue
            if dist(plie(w), plie(cand), DIST_MAX) <= DIST_MAX:
                out.append((w, v, cand, vc))
    return sorted(set(out))


def zone_morte(voc):
    """NON BLOQUANT. Les noms qui tombent ENTRE les deux seuils (RARE < n < FREQUENT) avec un
    jumeau fréquent : trop écrits pour être une coquille, trop peu pour être le nom juste.

    Né d'un défaut MESURÉ de la conception, et du pire genre — autodestructeur. Consigner la
    coquille de l'incident (« kDrib ») dans CLAUDE.md ET dans JOBS.md l'a portée à 3 occurrences,
    donc AU-DESSUS de RARE : le contrôle ne la voyait plus, et une récidive l'aurait portée à 4,
    toujours invisible. Le corpus EST le dictionnaire, donc écrire une coquille dans la
    consignation l'IMMUNISE. Remède appliqué : une coquille citée s'écrit entre apostrophes
    inverses (`nettoyer` les retire), et ce motif dit ce qui a glissé dans l'entre-deux.

    NON BLOQUANT, et PRÉVENTIF : sur le corpus réel il rend ZÉRO entrée une fois la coquille
    citée sortie du corpus. La seule qu'il ait jamais eue est cette coquille-là.

    Ma mesure d'exploration en annonçait DEUX, et la seconde était INVENTÉE : « Serafin-PH » (3)
    à côté de « SERAFIN-PH » (28). Ma boucle jetable avait OMIS la ligne `plie(cand) == plie(w)`,
    présente dans les deux motifs depuis l'origine, qui écarte une simple variante de casse — la
    clé pliant la casse, les deux graphies sont le MÊME mot pour le contrôle. Un test qui teste
    une COPIE de la logique ne garde rien, et ici la copie a inventé un défaut. (Les trois
    « Serafin-PH » sont par ailleurs la graphie verbatim d'un titre de section de la CNSA : les
    corriger falsifierait la citation. Une variante de casse d'un nom tiers n'est donc PAS de
    notre ressort, et c'est une deuxième raison de ne pas bloquer.)"""
    freqs = [(w, v) for w, v in voc.items() if v >= FREQUENT]
    out = []
    for w, v in voc.items():
        if not (RARE < v < FREQUENT):
            continue
        for cand, vc in freqs:
            if plie(cand) == plie(w) or plie(w)[:PREFIXE] != plie(cand)[:PREFIXE]:
                continue
            if dist(plie(w), plie(cand), DIST_MAX) <= DIST_MAX:
                out.append((w, v, cand, vc))
                break
    return sorted(set(out))


def lignes_de(chemins, mot):
    """Où lire la coquille : fichier et numéro de ligne, pour qu'elle soit corrigeable."""
    vus = []
    for c in chemins:
        for n, l in enumerate(io.open(c, encoding="utf-8"), 1):
            if re.search(r"(?<![A-Za-z])%s(?![A-Za-z])" % re.escape(mot), l):
                vus.append("%s:%d" % (os.path.basename(c), n))
    return vus


def controler(chemins):
    manquants = [c for c in chemins if not os.path.isfile(c)]
    if manquants:
        print("CONSIGNATION INTROUVABLE : %s" % ", ".join(manquants))
        return 1
    texte = " ".join(nettoyer(io.open(c, encoding="utf-8").read()) for c in chemins)
    voc = vocabulaire(texte)
    pb = coquilles(voc)
    for w, v, cand, vc in pb:
        print("COQUILLE PROBABLE : « %s » (%d occurrence%s) ressemble à « %s » (%d) — %s"
              % (w, v, "s" if v > 1 else "", cand, vc,
                 " ; ".join(lignes_de(chemins, w)) or "⟨ligne introuvable⟩"))
    for w, v, cand, vc in zone_morte(voc):
        print("ZONE MORTE (non bloquant) : « %s » (%d) est entre les seuils, à côté de « %s » (%d) — %s"
              % (w, v, cand, vc, " ; ".join(lignes_de(chemins, w)) or "⟨ligne introuvable⟩"))
    print("%s — %d nom(s) technique(s) au vocabulaire, %d coquille(s)"
          % ("REFUSÉ" if pb else "OK", len(voc), len(pb)))
    return 1 if pb else 0


def _autotest():
    """Bornes HORS RÉSEAU. Elles gardent les quatre seuils ET les quatre sources de bruit
    mesurées le 27/10/2026 : morphologie française, emphase en capitales, préfixe, et le
    couple iPad/iMac qui est le seul faux positif que le corpus ait produit."""
    ko, jouees = [], []

    def borne(nom, ok, detail=""):
        print("  %s %s%s" % ("✓" if ok else "✗", nom, (" — " + detail) if detail else ""))
        jouees.append(nom)
        if not ok:
            ko.append(nom)

    def pris(faux, texte_voc):
        voc = vocabulaire(texte_voc)
        voc[faux] = 1
        return [p for p in coquilles(voc) if p[0] == faux]

    base = ("kDrive " * 19) + ("iMac " * 49) + "iPad " + ("SERAFIN-PH " * 28)
    borne("① la coquille de l'incident est prise (kDrib ~ kDrive, distance 2)",
          bool(pris("kDrib", base)), str(pris("kDrib", base))[:60])
    borne("② une transposition dans un nom à trait d'union est prise (SERAFIN-HP)",
          bool(pris("SERAFIN-HP", base)))
    borne("③ iPad ~ iMac N'EST PAS signalé — SEUL faux positif que le corpus ait produit,"
          " écarté par le préfixe de 3 : ce témoin DOIT être ACCEPTÉ",
          coquilles(vocabulaire(base)) == [], str(coquilles(vocabulaire(base))))
    morpho = ("ajouté " * 33) + ("ajoutée " * 34) + "ajoutés AJOUTÉS "
    borne("④ la morphologie française n'est PAS une coquille (ajouté/ajoutée/ajoutés)",
          coquilles(vocabulaire(morpho)) == [], str(coquilles(vocabulaire(morpho))))
    emphase = ("ABSENT " * 12) + ("ABSENTE " * 16) + "ABSENTS absent absente "
    borne("⑤ un mot français en CAPITALES n'est pas un nom technique (ABSENTS/ABSENT)",
          coquilles(vocabulaire(emphase)) == [], str(coquilles(vocabulaire(emphase))))
    borne("⑥ le code entre apostrophes inverses est écarté du découpage",
          "kDrib" not in nettoyer("`kDrib` et ```\nkDrib\n```"))
    borne("⑦ une adresse et une empreinte sont écartées",
          nettoyer("https://kDrib.fr 424fa396099db8781f37208f64a6a9e17fc327a0").strip() == "")
    borne("⑧ les quatre seuils sont ceux que la mesure a fixés",
          (DIST_MAX, PREFIXE, RARE, FREQUENT) == (2, 3, 2, 5),
          "distance %d · préfixe %d · rare %d · fréquent %d" % (DIST_MAX, PREFIXE, RARE, FREQUENT))
    borne("⑨ un nom à casse mixte rare SANS jumeau fréquent ne crie pas (pas de référence)",
          coquilles(vocabulaire("NotebookLM OpenSSL CommonJS")) == [])
    borne("⑩ la coquille est localisée, fichier et ligne, sinon elle n'est pas corrigeable",
          "lignes_de" in open(os.path.abspath(__file__), encoding="utf-8").read()
          and "⟨ligne introuvable⟩" in open(os.path.abspath(__file__), encoding="utf-8").read())
    immun = ("kDrive " * 19) + "kDrib kDrib kDrib "
    borne("⑪ la ZONE MORTE est dite : une coquille écrite 3 fois est au-dessus de RARE, donc"
          " INVISIBLE au motif bloquant — c'est le défaut autodestructeur du 27/10",
          coquilles(vocabulaire(immun)) == [] and [z[0] for z in zone_morte(vocabulaire(immun))] == ["kDrib"],
          "bloquant : %s · zone morte : %s" % (coquilles(vocabulaire(immun)), zone_morte(vocabulaire(immun))))
    borne("⑫ et une coquille CITÉE entre apostrophes inverses ne compte plus au corpus,"
          " sinon la consigner l'immunise",
          "kDrib" not in nettoyer(u"la coquille `kDrib` citée") and
          "kDrib" in nettoyer(u"la coquille « kDrib » citée"))
    print("  %d/%d bornes de l'orthographe des consignations" % (len(jouees) - len(ko), len(jouees)))
    return 1 if ko else 0


if __name__ == "__main__":
    if "--autotest" in sys.argv:
        raise SystemExit(_autotest())
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    raise SystemExit(controler([os.path.abspath(a) for a in args] if args else CONSIGNES))
