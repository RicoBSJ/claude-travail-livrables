---
type: fiche-document
source: 2026-07-13_lecon-entretien-motivationnel_05_discours-changement-darn-cat.docx
date_creation: 2026-08-14
date_lecon: 2026-07-13
parcours: entretien-motivationnel
numero: 5
statut: parcours-archive
tags:
  - parcours/entretien-motivationnel
  - outil/darn-cat
  - concept/discours-maintien
  - concept/evocation
  - theme/certificat-mutualise
  - theme/https-vers-http
  - correction/2026-10-25
---

# 2026-07-13_lecon-entretien-motivationnel_05_discours-changement-darn-cat

Document source : [[2026-07-13_lecon-entretien-motivationnel_05_discours-changement-darn-cat.docx]]

## Résumé

La grille qui permet d'entendre finement où en est la personne. Le discours-changement se décline en deux temps : **DARN**, préparatoire — Désir (« j'aimerais »), Aptitude (« je pourrais »), Raisons (« ça m'éviterait »), Nécessité (« il faut que ») — puis **CAT**, mobilisation, plus proche du passage à l'acte : engagement (« je vais »), activation (« je suis prêt »), premiers pas (« j'ai déjà commencé »).

La distinction est opératoire : **entendre du DARN sans CAT signale qu'il est trop tôt pour planifier**. C'est le repère qui manque le plus souvent.

La règle centrale est reprise de la leçon 01 : on ne fabrique pas le discours-changement, on l'évoque. Poser la question ouverte, puis refléter et résumer ce qui va dans son sens.

Face au discours-maintien, la consigne est explicite — **ne pas argumenter contre, cela le renforce**. On l'accueille par un reflet, on explore l'ambivalence, on ré-ouvre sans forcer.

**L'adresse de l'AFDEM n'était pas morte : son hôte mutualisé ne porte pas son nom. Corrigée le 25/10/2026**, l'hyperlien passant de `https://` à `http://`. Mesuré : `https://www.entretienmotivationnel.org/` rend HTTP 000 et `curl` **exit 60**, non parce que la page a disparu mais parce que le certificat présenté est celui de l'hébergement mutualisé OVH — `CN=cluster110.hosting.ovh.net`, **renouvelé le 19/10/2026**, donc vivant — sans aucun nom alternatif couvrant le domaine : *« no alternative certificate subject name matches target host name »*. Le site, lui, **répond** : en `http` il rend **HTTP 200 et 13 403 caractères utiles**, où `AFDEM` et son nom développé s'apparient au **degré ①**. L'archive était exclue d'office : le dernier instantané de l'hôte date du **12/12/2019**, sept ans avant la leçon.

**Ce que la correction coûte, et le marqueur le dit dans le document** : `http://` n'est pas chiffré, et un navigateur en HTTPS-first peut échouer là où `curl` réussit. Le lien reste donc utilisable mais dégradé — c'était le seul choix qui préserve l'accès à une ressource vivante, l'alternative étant de retirer un lien qui fonctionne.

**Requêtes passées** (ce qui n'y figure pas n'a pas été interrogé) : `curl -sS -o /dev/null -w "%{http_code} %{exitcode}"` avec **et** sans le faisceau du dépôt, sur `https://` et `http://`, forme nue et forme `www.` ; `openssl s_client -showcerts` pour la chaîne et les dates ; `aspirer.py` sur la forme `http` ; `chercher.py` sur `AFDEM` et *Association Francophone de Diffusion de l'Entretien Motivationnel* ; CDX Wayback sur `www.entretienmotivationnel.org` pour le dernier instantané à 200.

## Notes liées

- **⬅️ Précédente** · [[2026-07-13_lecon-entretien-motivationnel_04_oars-ouver]]
  dont les outils sont ici orientés
- **➡️ Suivante** · [[2026-07-13_lecon-entretien-motivationnel_06_discordance-situations-difficiles]]
  ce qui se passe quand la relation, et non le discours, se grippe
- **🔗 Pont** · [[2026-07-23_lecon-entretien-motivationnel_09_planification-engagement]]
  où le passage du DARN au CAT devient le signal d'entrée en planification
