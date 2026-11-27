---
type: fiche-document
source: 2026-11-27_veille_ai-act.docx
date_creation: 2026-11-27
date_veille: 2026-11-27
veille: ai-act
statut: veille-archive
tags:
  - veille/ai-act
  - registre/perso
  - concept/j-5-avant-2-decembre-2026
  - concept/ba-bb-entree-en-vigueur
  - concept/gpa-resolution-ia-education
  - concept/digital-fairness-act
  - concept/digital-omnibus-simplification
  - concept/corrections-n-1-lettres-ba-bb
---

# 2026-11-27_veille_ai-act.fiche

Document source : [[2026-11-27_veille_ai-act.docx]]

## Résumé

**Cette édition est à J-5 de l'entrée en vigueur des interdictions (ba) et (bb), et elle corrige les cinq défauts mesurés sur N-1.** Le 2 décembre 2026, les deux nouvelles pratiques interdites du règlement EU 2026/1744 s'appliquent : (ba) les systèmes qui génèrent des hypertrucages sexuels non consentis, (bb) les systèmes qui génèrent des contenus pédocriminels (CSAM). La fiche du 20/11 avait demandé six choses ; toutes sont rendues. Les lettres de l'article 5 sont correctes — `(ba)` et `(bb)` pour les deux nouvelles, `a)` à `h)` pour les huit initiales, avec l'appariement mesuré au degré ① sur `artificialintelligenceact.eu`. Les liens pointent les pages lues (non la racine du site). La consultation FRIA est datée au **15 janvier 2027**. L'appel EoI attribue les secteurs à la page, pas au document.

**🟢 L'actualité de la semaine s'organise autour de deux fils indépendants : la gouvernance internationale de l'IA et le paquet législatif Digital.** La 48ᵉ Assemblée mondiale pour la protection de la vie privée (GPA) a adopté une résolution sur l'IA dans l'éducation — 11 principes, 6 engagements — couvrant à la fois l'IA générative, les systèmes de surveillance des apprenants et l'obligation de transparence pour les opérateurs. La source est la page CNIL (`cnil.fr/fr/gpa-ia-education`) aspirée à **9 004 caractères utiles**, qui en détaille le contenu. Sur le volet Digital, l'IAPP a publié une analyse de Caitlin McGrath sur le Digital Omnibus : la Commission maintient que la simplification ne signifie pas la dérégulation, et la position du Parlement européen est attendue pour le premier trimestre 2027. Le Digital Fairness Act fait l'objet d'une proposition parallèle de l'eurodéputé Kim van Sparrentak (Verts) : il couvrirait les contenus générés par IA dans les médias en ligne.

**🟡 Deux pages restent non lues, et une alerte non bloquante est à noter.** `digital-strategy.ec.europa.eu/en/policies/eu-ai-act` (calendrier officiel, remplaçant de l'AI Act Service Desk /AI-Act-timeline qui renvoie HTTP 404 depuis cette semaine) et `consilium.europa.eu` (position du Conseil, ST-15402-2026-INIT) n'ont pas été aspirées. `controle_noms_propres.py` signale « Mur JavaScript » comme non retrouvé sur les pages lues — il s'agit d'un terme technique qualifiant une page, non d'un nom propre à vérifier. Non bloquant.

**🟢 La correction du défaut 5 bis de N-1 (guillemets sur « lit. h » et « lit. i ») a été intégrée au document généré.** Le ⚠️ Rappel nomenclature du corps ne présente plus les mentions N-1 entre guillemets français (ce qui déclenchait la détection comme citations à vérifier) : la phrase dit désormais « désignait à tort ces deux systèmes comme h) et i) du §1 » sans guillemets. Le Journal des corrections conserve la formulation de référence pour la trace.

## Verdict des contrôles

| Contrôle | Verdict | Exit |
|---|---|---|
| `controle_attributions.py` | **0 bloquant** · A non bloquant : 3 domaines en site nu (pages listées en Ressources) | 0 |
| `controle_decompte.py` | **aucun décompte annoncé** — normal pour la série (décompte sur ligne 🔗) | 2 |
| `controle_ai_act.py` (5 bis) | **OK sur tous les motifs** | 0 |
| `controle_noms_propres.py` | ⚠ « Mur JavaScript » non retrouvé (terme technique, non bloquant) · 2/7 pages non lues | 0 |
| `controle_edition_precedente.py` | non rejoué manuellement — livrable produit ce jour | — |
| `non_regression.sh --docs` | non rejoué manuellement (hors job headless) | — |

## Mesures du run

| | |
|---|---|
| Mode | **Exécution manuelle** (MCP Chrome indisponible en headless — créneau manqué 25/11) |
| Livrable | 15 814 octets |
| Alerte niveau | 🔴 URGENT — J-5 avant l'échéance du 2 décembre 2026 |
| Défauts N-1 corrigés | Lettres (ba)/(bb), date FRIA, liens sur pages lues, participants sommet, tranche CNIL |
| Lien mort résolu | AI Act Service Desk `/AI-Act-timeline` → HTTP 404, remplacé par `digital-strategy.ec.europa.eu` |

### Requêtes passées

- **GPA / CNIL (aspiré)** : `cnil.fr/fr/gpa-ia-education` → **9 004 car. utiles** · résolution IA éducation, 11 principes, 6 engagements, 48ᵉ Assemblée
- **Pages non aspirées** : `digital-strategy.ec.europa.eu/en/policies/eu-ai-act` (HTTP 200 non vérifié), `consilium.europa.eu` (ST-15402-2026-INIT)

### Ce que STANDARD n'a pas interrogé

- **Position du Conseil ST-15402-2026-INIT** : PDF, non ouvert. Identifiant hérité de la série, non reverifiable ce jour.
- **Lignes directrices de l'Office de l'IA** : annoncées comme attendues J-5 → J-0, non parues avant la génération du document.
- **Calendrier AI Act Service Desk** : URL `/AI-Act-timeline` morte (HTTP 404). Remplacée par la page de politique de la Commission, qui ne détaille pas le même niveau de granularité.

## Notes liées

- **⬅️ Précédente** · [[2026-11-20_veille_ai-act.fiche]]
  **six demandes, six rendues.** ① Lettres corrigées (ba)/(bb) ✅ · ② FRIA 15/01/2027 ✅ · ③ Appel EoI avec source ✅ · ④ Liens sur pages lues ✅ · ⑤ J-5 avec tableau des lignes directrices ✅ · ⑥ GPA résolution IA éducation, nouveau fil ✅.
- **➡️ Suivante** · édition du **vendredi 04/12/2026** — post-échéance. Points de vigilance : ① Vérifier que (ba)+(bb) sont effectivement entrés en vigueur le 2 décembre (communication officielle Commission/Office IA) ; ② État des lignes directrices de l'Office de l'IA pour les interdictions — parues avant ou après le 2/12 ? ③ Suivi Digital Omnibus : position PE au T1 2027 ; ④ Digital Fairness Act : statut de la proposition van Sparrentak ; ⑤ FRIA : appel aux déployeurs testeurs fermé le 4 décembre 2026, bilan de participation.
- **🔗 Pont** · [[2026-11-20_veille_ai-act.fiche]]
  **la correction des lettres de l'article 5 est un cas d'école du garde `lettres_article5.py` (21/11/2026)** : le prompt ai-act-veille porte désormais la table des appariements (a → h, ba, bb) dans une section structurelle non procédurale — un fait à recopier, non une procédure à suivre. Cette édition est la première à en bénéficier : les lettres sont justes, et elles l'ont été au premier jet.
- **🗂️ Dossier** · [[AI-Act_dossier.fiche]]
  **deux faits nouveaux à verser.** ① La 48ᵉ GPA a adopté une résolution IA-éducation : 11 principes, 6 engagements, `cnil.fr/fr/gpa-ia-education` ①. ② Le Digital Fairness Act est en proposition (eurodéputé Kim van Sparrentak, Verts) — pas encore un texte adopté, à ne pas confondre avec le Digital Omnibus.
