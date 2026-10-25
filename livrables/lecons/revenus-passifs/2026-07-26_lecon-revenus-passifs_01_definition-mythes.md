---
type: fiche-document
source: 2026-07-26_lecon-revenus-passifs_01_definition-mythes.docx
date_creation: 2026-08-14
date_lecon: 2026-07-26
parcours: revenus-passifs
numero: 1
statut: parcours-actif
tags:
  - parcours/revenus-passifs
  - notion/continuum-actif-passif
  - notion/mythes
  - notion/signaux-alerte
  - theme/domaine-parke
  - theme/code-200-trompeur
  - correction/2026-10-25
---

# 2026-07-26_lecon-revenus-passifs_01_definition-mythes

Document source : [[2026-07-26_lecon-revenus-passifs_01_definition-mythes.docx]]

## Résumé

Leçon d'ouverture, et **la plus défensive du corpus** — à raison. Elle s'ouvre sur un constat que peu de contenus du secteur assument : *le domaine des revenus passifs est saturé de promesses trompeuses et d'arnaques*.

Le travail principal est de démonter les mythes fondateurs : **passif ne signifie ni sans effort, ni sans capital, ni sans risque**. La leçon propose de situer tout modèle sur un **continuum actif/passif** à l'aide de trois critères, plutôt que de raisonner en catégories binaires.

Elle donne aussi les **signaux d'alerte** permettant de reconnaître une arnaque avant d'y avoir engagé un euro — la contribution la plus immédiatement utile.

Le cadre déontologique est explicite et rappelé à chaque leçon : contenu éducatif, jamais de conseil ; le conseil en investissement est en France une activité réglementée (statut CIF, registre ORIAS).

**Source nommée sans adresse, corrigée le 12/09/2026.** Relevée par la passe A du contrôle d'attribution (règle ⑭ : un site cité comme source sans aucune page listée bloque comme une page) : la section Mythes attribuait un ordre de grandeur aux « retours d'expérience de la communauté Indie Hackers (indiehackers.com) » sans aucune adresse : lien posé, ressource n°8 ajoutée, affirmation inchangée. Formulation d'origine dans le journal des corrections du document.

**Le domaine Observalys est parké, et c'est un `200` qui le cachait. Corrigée le 25/10/2026**, hyperlien **retiré**, adresse conservée en clair. Le diagnostic a demandé trois étapes, parce qu'un « 000 » ne dit rien par lui-même. ① En `https`, le serveur émet lui-même une **alerte TLS 80** (*« tlsv1 alert internal error »*) : HTTP 000, `curl` **exit 35**, **six essais sur six**, en IPv4 **et** en IPv6, avec `curl` comme avec `openssl 3.6.2` — ce n'est donc ni une intermittence, ni notre pile TLS. ② En `http`, l'adresse rend **HTTP 200** : un code qui ne prouve rien, car la page servie est le gabarit **« Parked Domain name »** de Hostinger, **927 caractères utiles**, où `Observalys`, `Revenu passif` et `mythe ou réalité` sont tous **④ ABSENT**. ③ Wayback n'a **aucun** instantané de cette adresse, donc aucune archive ne peut la remplacer.

**Et c'est un angle mort mesuré de `balayer_adresses.py`** : citée en `http`, cette adresse aurait été classée « vivante » — le balayage lit un code, pas un contenu. Le gabarit de parking est exactement le cas où les deux divergent.

**Requêtes passées** : `curl` avec et sans faisceau, `https` et `http`, IPv4 et IPv6, trois essais par combinaison ; `openssl s_client` ; `aspirer.py` sur la forme `http` (927 caractères utiles, sous le plancher de 3 000) ; `chercher.py` sur `Observalys`, `Revenu passif`, `mythe ou réalité` ; CDX Wayback sur l'adresse et sur le domaine nu.

## Notes liées

- **➡️ Suivante** · [[2026-08-02_lecon-revenus-passifs_02_grandes-familles-panorama]]
  de la déconstruction à la cartographie
- **🔗 Pont** · [[2026-06-20_lecon-placement-financier_02_rendement-risque-diversification]]
  le meilleur antidote aux promesses du secteur tient en une phrase de cette leçon : rendement élevé et sécurité totale ne coexistent pas
