---
type: fiche-document
source: 2026-07-08_lecon-entretien-motivationnel_01_esprit-em-pace.docx
date_creation: 2026-08-14
date_lecon: 2026-07-08
parcours: entretien-motivationnel
numero: 1
statut: parcours-archive
tags:
  - parcours/entretien-motivationnel
  - auteur/miller
  - auteur/rollnick
  - concept/pace
  - concept/evocation
  - theme/certificat-mutualise
  - theme/https-vers-http
  - correction/2026-10-25
---

# 2026-07-08_lecon-entretien-motivationnel_01_esprit-em-pace

Document source : [[2026-07-08_lecon-entretien-motivationnel_01_esprit-em-pace.docx]]

## Résumé

Leçon d'ouverture, et la seule qui compte vraiment si l'on ne devait en retenir qu'une : **l'EM n'est pas une boîte à outils qu'on applique à quelqu'un, c'est une manière d'être avec lui**.

Formalisé par William Miller dans les années 1980 à partir du champ des addictions, puis développé avec Stephen Rollnick, l'EM est défini comme un style de conversation collaboratif visant à renforcer la motivation propre d'une personne et son engagement vers le changement.

L'intuition fondatrice est contre-intuitive et vérifiable au quotidien : **face à quelqu'un d'ambivalent, lui expliquer pourquoi il devrait changer le pousse à défendre le statu quo**. Les arguments en faveur du changement n'ont d'effet que s'ils sortent de sa bouche à elle. Tout le dispositif de l'EM organise la conversation pour que ce soit le cas.

D'où l'esprit **PACE** — Partenariat, Acceptation, Compassion, Évocation — posé avant toute technique. La leçon le dit sans détour : sans cet état d'esprit, les techniques deviennent des ficelles de manipulation.

**L'adresse de l'AFDEM n'était pas morte : son hôte mutualisé ne porte pas son nom. Corrigée le 25/10/2026**, l'hyperlien passant de `https://` à `http://`. Mesuré : `https://www.entretienmotivationnel.org/` rend HTTP 000 et `curl` **exit 60**, non parce que la page a disparu mais parce que le certificat présenté est celui de l'hébergement mutualisé OVH — `CN=cluster110.hosting.ovh.net`, **renouvelé le 19/10/2026**, donc vivant — sans aucun nom alternatif couvrant le domaine : *« no alternative certificate subject name matches target host name »*. Le site, lui, **répond** : en `http` il rend **HTTP 200 et 13 403 caractères utiles**, où `AFDEM` et son nom développé s'apparient au **degré ①**. L'archive était exclue d'office : le dernier instantané de l'hôte date du **12/12/2019**, sept ans avant la leçon.

**Ce que la correction coûte, et le marqueur le dit dans le document** : `http://` n'est pas chiffré, et un navigateur en HTTPS-first peut échouer là où `curl` réussit. Le lien reste donc utilisable mais dégradé — c'était le seul choix qui préserve l'accès à une ressource vivante, l'alternative étant de retirer un lien qui fonctionne.

**Requêtes passées** (ce qui n'y figure pas n'a pas été interrogé) : `curl -sS -o /dev/null -w "%{http_code} %{exitcode}"` avec **et** sans le faisceau du dépôt, sur `https://` et `http://`, forme nue et forme `www.` ; `openssl s_client -showcerts` pour la chaîne et les dates ; `aspirer.py` sur la forme `http` ; `chercher.py` sur `AFDEM` et *Association Francophone de Diffusion de l'Entretien Motivationnel* ; CDX Wayback sur `www.entretienmotivationnel.org` pour le dernier instantané à 200.

## Notes liées

- **➡️ Suivante** · [[2026-07-11_lecon-entretien-motivationnel_02_ambivalence-reflexe-correcteur]]
  qui explique pourquoi cet esprit est nécessaire, et non seulement souhaitable
- **🔗 Pont** · [[2026-07-06_lecon-psychopathologie_04_entretien-clinique-examen-etat-mental]]
  **pont majeur.** L'alliance thérapeutique de Bordin et l'esprit PACE décrivent la même réalité depuis deux traditions. La différence tient au statut de la relation : condition du recueil chez le clinicien, levier du changement lui-même dans l'EM
- **🔗 Pont** · [[2026-06-05_lecon-stoicisme_01_dichotomie-controle]]
  le refus d'un usager : « ce qui ne dépend pas de moi » pour le stoïcien, autonomie de la personne pour l'EM. Deux façons d'éviter l'épuisement, mais l'EM ajoute comment continuer à travailler avec ce refus
