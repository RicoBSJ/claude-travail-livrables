---
type: fiche-document
source: 2026-07-11_lecon-entretien-motivationnel_02_ambivalence-reflexe-correcteur.docx
date_creation: 2026-08-14
date_lecon: 2026-07-11
parcours: entretien-motivationnel
numero: 2
statut: parcours-archive
tags:
  - parcours/entretien-motivationnel
  - concept/ambivalence
  - concept/reflexe-correcteur
  - concept/discours-changement
  - theme/certificat-mutualise
  - theme/https-vers-http
  - correction/2026-10-25
---

# 2026-07-11_lecon-entretien-motivationnel_02_ambivalence-reflexe-correcteur

Document source : [[2026-07-11_lecon-entretien-motivationnel_02_ambivalence-reflexe-correcteur.docx]]

## Résumé

Trois notions qui font basculer l'EM de l'intuition à la méthode.

**L'ambivalence n'est pas une résistance** : c'est la présence simultanée de motivations contradictoires, et l'antichambre normale du changement. La personne qui semble bloquée délibère. Cette relecture change entièrement la posture — on cesse de vouloir vaincre une opposition.

**Le réflexe correcteur** (*fixing reflex*, renommé ainsi dans la 4ᵉ édition, auparavant *righting reflex*) est notre pulsion naturelle de réparer l'autre : aligner les bons arguments, convaincre. Le piège est mécanique — plus j'argumente pour le changement, plus j'assigne à la personne le rôle inverse, celui de défendre le statu quo. **C'est moi qui produis la résistance que je constate ensuite.**

Enfin la distinction à entraîner à l'oreille : discours-changement contre discours-maintien. Tout ce que dit la personne penche d'un côté ou de l'autre, et l'intervenant influe sur la proportion sans s'en rendre compte.

**L'adresse de l'AFDEM n'était pas morte : son hôte mutualisé ne porte pas son nom. Corrigée le 25/10/2026**, l'hyperlien passant de `https://` à `http://`. Mesuré : `https://www.entretienmotivationnel.org/` rend HTTP 000 et `curl` **exit 60**, non parce que la page a disparu mais parce que le certificat présenté est celui de l'hébergement mutualisé OVH — `CN=cluster110.hosting.ovh.net`, **renouvelé le 19/10/2026**, donc vivant — sans aucun nom alternatif couvrant le domaine : *« no alternative certificate subject name matches target host name »*. Le site, lui, **répond** : en `http` il rend **HTTP 200 et 13 403 caractères utiles**, où `AFDEM` et son nom développé s'apparient au **degré ①**. L'archive était exclue d'office : le dernier instantané de l'hôte date du **12/12/2019**, sept ans avant la leçon.

**Ce que la correction coûte, et le marqueur le dit dans le document** : `http://` n'est pas chiffré, et un navigateur en HTTPS-first peut échouer là où `curl` réussit. Le lien reste donc utilisable mais dégradé — c'était le seul choix qui préserve l'accès à une ressource vivante, l'alternative étant de retirer un lien qui fonctionne.

**Requêtes passées** (ce qui n'y figure pas n'a pas été interrogé) : `curl -sS -o /dev/null -w "%{http_code} %{exitcode}"` avec **et** sans le faisceau du dépôt, sur `https://` et `http://`, forme nue et forme `www.` ; `openssl s_client -showcerts` pour la chaîne et les dates ; `aspirer.py` sur la forme `http` ; `chercher.py` sur `AFDEM` et *Association Francophone de Diffusion de l'Entretien Motivationnel* ; CDX Wayback sur `www.entretienmotivationnel.org` pour le dernier instantané à 200.

## Notes liées

- **⬅️ Précédente** · [[2026-07-08_lecon-entretien-motivationnel_01_esprit-em-pace]]
  dont elle justifie l'exigence
- **➡️ Suivante** · [[2026-07-13_lecon-entretien-motivationnel_03_quatre-processus]]
  la structure qui permet d'accompagner l'ambivalence au lieu de la heurter
- **🔗 Pont** · [[2026-08-03_lecon-psychopathologie_08_troubles-personnalite-clusters-borderline]]
  l'instabilité relationnelle du borderline est la configuration où le réflexe correcteur se déclenche le plus fort — et donc celle où l'EM est le plus difficile à tenir et le plus utile
- **🔗 Pont** · [[2026-08-13_lecon-stoicisme_10_progres-moral-prokopton-sage]]
  deux modèles du changement comme processus continu plutôt que comme bascule
