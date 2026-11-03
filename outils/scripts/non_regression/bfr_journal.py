#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bfr_journal.py — B-FR lit-elle le 📝 Journal des corrections, et seulement ce qu'il AFFIRME ?

POURQUOI (03/11/2026). Le journal de la veille has-actualite du 02/11 citait
« entre décembre 2026 et début de l'année 2028 » avec l'apostrophe DROITE là où la page
archivée porte l'apostrophe typographique — ① LITTÉRAL contre ④ ABSENT. Mesure du jour sur ce
document : 3 spans entre guillemets dans le CORPS, 11 dans les JOURNAUX, et B-FR en examinait
2. Le journal était donc À LA FOIS le seul endroit sûr pour poser un littéral — il est exempté
de B, B-FR, B-NOM et D — ET le seul endroit où un littéral FAUTIF est invisible. Les deux
moitiés sont le même fait.

LA BORNE EST MESURÉE, PAS CHOISIE. La reprise NAÏVE du journal fait entrer 1 006 citations
neuves dans 161 documents, dont 183 capables de BLOQUER : ce sont les formulations d'origine
que le journal conserve par doctrine. Avec le verbe de portage AU PRÉSENT : 30 neuves dans
22 documents, 19 à source nommée, et sur ces 22 documents — relancés un par un, séquentiellement,
avec le réseau — **0 bloquant changé, 0 compteur du corps changé, 0 ligne perdue**, pour
17 « JOURNAL OK », 9 « JOURNAL A RELIRE » et 326 spans écartés.

LE DISCRIMINANT EST LE TEMPS DU VERBE, et il colle au sens : le PRÉSENT dit ce que la page
porte (« la page AMF écrit « … » »), l'IMPARFAIT ce que le document portait (« cette rubrique
portait « … » », « la note écrivait « … » »). L'imparfait est le temps de la conservation.

⛔ ET ELLES NE SONT JAMAIS BLOQUANTES. Un balayage rétrospectif ne valide pas un motif
bloquant (règle du 14/10) et le journal est, par construction, l'endroit où vivent les
libellés fautifs : une citation du journal est vérifiée et RAPPORTÉE, jamais refusée.

⚠️ CE N'EST PAS UNE COPIE DE LA LOGIQUE : le bloc `PORTE_JRN … porte_jrn` est EXTRAIT de
`controle_attributions.py` puis exécuté. Si l'un de ses morceaux disparaît du contrôle, la
borne ② le dit — sans elle, ce témoin resterait vert sur du vide.

⚠️ RÉSIDU DIT : « M. X présente une fuite des idées » (psychopathologie n°04) reste accusée à
tort — son porteur, « le second exercice », tombe hors de la fenêtre de 90 caractères. Non
bloquant, donc le prix est du bruit, pas un refus. Et la direction d'erreur de chaque exemption
est un vrai défaut manqué, qui coûte une relecture humaine, jamais un livrable non publié.

Aucun réseau. Usage : python3 outils/scripts/non_regression/bfr_journal.py
Sortie : 0 si toutes les bornes tiennent, 1 sinon.
"""
import os, re, sys

# ⚠️ QUATRE dirname — ce script vit dans outils/scripts/non_regression/, un cran plus bas que
#    les contrôles. Le piège du 23/10, et la borne ① vérifie que RACINE est rendue.
RACINE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
CTL = os.path.join(RACINE, "outils", "scripts", "controle_attributions.py")

# Chaque cas est le CONTEXTE GAUCHE que le contrôle passe à porte_jrn(), c'est-à-dire les
# caractères du journal qui PRÉCÈDENT le guillemet ouvrant. Les six premiers viennent du
# corpus ; les formes « ACCEPTÉE » sont celles qui ne doivent RIEN faire entrer.
CAS = [
 ("③ RETENU — « la page AMF écrit « … » » : le cas nominal, 17 fois « JOURNAL OK » sur le corpus",
  "Citation entre guillemets attribuée nommément au régulateur, mais non conforme : la page AMF écrit ",
  True),
 ("④ RETENU — « porte littéralement » (astrologie n°07)",
  "la page Balguerie rend 39 794 caractères et 95 occurrences de « saturne », les deux annoncés,"
  " et porte littéralement ", True),
 ("⑤ RETENU — « n'écrit que » est RESTRICTIF, pas négatif (la CNSA, serafin 23/09)",
  "aucun de ces libellés n'est sur les sources consultées ; la CNSA n'écrit que ", True),
 ("⑥ RETENU — le 2e littéral d'une ÉNUMÉRATION (le cas même de l'incident du 02/11)",
  "est en revanche ouverte — 14 097 caractères utiles — et porte « Clôture de l'appel le 26/10/2026 », ",
  True),
 ("⑦ ACCEPTÉE — l'IMPARFAIT est le temps de la CONSERVATION : sans lui, 1 006 citations entrent",
  "Cette rubrique portait ", False),
 ("⑧ ACCEPTÉE — « la note écrivait « … » » : le document, pas la page",
  "Traduction qui perdait l'effet juridique. La note écrivait ", False),
 ("⑨ ACCEPTÉE — une NÉGATION est déjà un constat d'absence (placement-financier n°15)",
  "l'effet moutonnier lors des phases de marché extrêmes. » — la page IEFP ne dit ni la hiérarchie,"
  " ni les précisions, ni ", False),
 ("⑩ ACCEPTÉE — le porteur est le DOCUMENT (« le paragraphe … annonce »), astrologie n°02",
  "n'est pas corrigé ici. Le paragraphe sur la précession annonce ", False),
 ("⑪ ACCEPTÉE — l'objet est annoncé comme un EXEMPLE (psychopathologie n°04)",
  "il demande de traduire chaque domaine en observation légitime pour un éducateur,"
  " et donne le bon contre-exemple — ", False),
 ("⑫ ACCEPTÉE — « titre » est un NOM, pas un verbe de portage (psychopathologie n°14)",
  "la définition de l'insomnie est exacte MOT POUR MOT dans le PDF, que j'ai extrait et relu."
  " Le titre et la date de cette recommandation sont exacts — ", False),
]


def extrait():
    """Le bloc PORTE_JRN … porte_jrn, pris DANS le contrôle. None si absent."""
    s = open(CTL, encoding="utf-8").read()
    m = re.search(r"^PORTE_JRN = re\.compile\(.*?\n    return not NEG_JRN[^\n]*$", s, re.S | re.M)
    return m.group(0) if m else None


def controler():
    ko, jouees = [], []

    def borne(nom, ok, detail=""):
        print("  %s %s%s" % ("✓" if ok else "✗", nom, (" — " + detail) if detail else ""))
        jouees.append(nom)
        if not ok:
            ko.append(nom)

    def fin():
        # ⚠️ LE DÉNOMINATEUR EST LE NOMBRE DE BORNES JOUÉES, pas de réussies : avec le
        #    numérateur, retirer une borne laisse « N/N » et le garde du harnais est décoratif
        #    (défaut mesuré le 26/10 sur ATTENDU_CA et ATTENDU_CB5).
        print("  %d/%d bornes du journal en B-FR" % (len(jouees) - len(ko), len(jouees)))
        return 1 if ko else 0

    borne("① RACINE est rendue — le contrôle est là où ce script le cherche",
          os.path.isfile(CTL), CTL)
    if not os.path.isfile(CTL):
        return fin()

    bloc = extrait()
    borne("② le bloc PORTE_JRN … porte_jrn est bien DANS le contrôle (sinon ce témoin est vide)",
          bool(bloc), "%d caractères extraits" % len(bloc) if bloc else "ABSENT")
    if not bloc:
        return fin()

    ns = {"re": re}
    exec(compile(bloc, CTL, "exec"), ns)
    pj = ns["porte_jrn"]
    for nom, g, attendu in CAS:
        borne(nom, pj(g) is attendu,
              "porte_jrn rend %s, %s attendu" % (pj(g), attendu))

    src = open(CTL, encoding="utf-8").read()

    borne("⑬ le journal entre bien dans la COLLECTE : CIT_SRC = corps + journal, et la boucle"
          " itère sur CIT_SRC",
          "CIT_SRC = corps + journal" in src and "_CIT.finditer(CIT_SRC)" in src,
          "concat %s · boucle %s" % ("CIT_SRC = corps + journal" in src,
                                      "_CIT.finditer(CIT_SRC)" in src))

    # ⑭ L'ORDRE EST LA MOITIÉ DE LA RÈGLE (leçon du 27/10, desarmement_git) : la sortie de la
    #    branche anglaise doit PRÉCÉDER le premier filtre de cette branche, sinon la passe B
    #    chercherait sur les pages des messages d'erreur conservés au journal.
    i_sor = src.find("if m.start() >= _DEB_JRN:")
    i_sql = src.find("if SQL.match(c.strip()):")
    borne("⑭ la passe B (anglais) ne lit PAS le journal, et sa sortie est PREMIÈRE",
          0 < i_sor < i_sql, "sortie @%d · SQL @%d" % (i_sor, i_sql))

    # ⑮ LA BORNE QUI COMPTE LE PLUS : une citation du journal ne peut pas BLOQUER. On lit la
    #    branche entière et on exige qu'elle se termine par `continue` SANS toucher ko_b.
    i_br = src.find("if c in cits_jrn:")
    i_suite = src.find("\n    if not nommes:", i_br) if i_br > 0 else -1
    branche = src[i_br:i_suite] if 0 < i_br < i_suite else ""
    borne("⑮ les citations du JOURNAL ne peuvent pas bloquer : la branche sort par `continue`"
          " sans toucher ko_b",
          bool(branche) and "ko_b" not in branche and branche.rstrip().endswith("continue"),
          "branche de %d caractères, ko_b %s" % (len(branche), "PRÉSENT" if "ko_b" in branche else "absent"))

    borne("⑯ un libellé présent AUSSI dans le corps reste jugé comme tel (cits_jrn -= cits_corps)",
          "cits_jrn -= cits_corps" in src)

    borne("⑰ les autres passes ne voient PAS le journal : la coupe du corps est conservée",
          "corps = corps[:jrn]" in src and "journal = corps[jrn:]" in src)

    # ⑲ UNE FONCTION JUSTE MAIS JAMAIS APPELÉE LAISSE LE LOT VERT (leçon du 27/10). Sans cette
    #    borne, porte_jrn pourrait être parfaite et le contrôle reprendre le journal EN ENTIER :
    #    1 006 citations neuves, 183 capables de bloquer. Et l'appel doit PRÉCÉDER l'aiguillage
    #    FR / anglais, sinon la branche française a déjà enregistré la citation.
    i_app = src.find("and not porte_jrn(")
    i_fr = src.find("if FR.search(c) or not OUTILS.search(c):")
    borne("⑲ la collecte APPELLE porte_jrn, et l'appel précède l'aiguillage FR / anglais",
          0 < i_app < i_fr, "appel @%d · aiguillage @%d" % (i_app, i_fr))

    # ⑱ UN TRAVAIL QUI N'EST DANS AUCUN LOG N'EXISTE PAS (règle du 27/10, l'alerte d'étiquette).
    borne("⑱ le contrôle IMPRIME ce que la passe a retenu et écarté du journal",
          "B-FR a lu le corps ET le journal" in src and "span(s) du journal écarté" in src)

    return fin()


if __name__ == "__main__":
    raise SystemExit(controler())
