---
type: fiche-document
source: 2026-07-13_lecon-entretien-motivationnel_04_oars-ouver.docx
date_creation: 2026-08-14
date_lecon: 2026-07-13
parcours: entretien-motivationnel
numero: 4
statut: parcours-archive
tags:
  - parcours/entretien-motivationnel
  - outil/oars
  - outil/reflets
  - outil/questions-ouvertes
  - outil/resumes
  - theme/certificat-mutualise
  - theme/https-vers-http
  - correction/2026-10-25
---

# 2026-07-13_lecon-entretien-motivationnel_04_oars-ouver

Document source : [[2026-07-13_lecon-entretien-motivationnel_04_oars-ouver.docx]]

## Résumé

La boîte à outils concrète, résumée par **OARS** — questions Ouvertes, Affirmation, Reflets, Synthèses — rendue en français par **OuVER** (Ouvertes, Valoriser, Écoute réflective, Résumer).

Les questions ouvertes invitent à développer plutôt qu'à répondre par oui ou non. L'affirmation souligne sincèrement une force ou un effort, et nourrit le sentiment d'auto-efficacité. Les synthèses rassemblent les propos, en privilégiant le discours-changement.

Le cœur de la leçon est le **reflet**, décrit comme **l'outil le plus puissant et le plus sous-utilisé**. Reflet simple (paraphrase) ou complexe (on ajoute le sens ou l'émotion sous-jacente). La formule à retenir : *le reflet n'est pas une question déguisée — c'est une hypothèse sur le sens, offerte à la personne, qu'elle peut confirmer ou corriger*.

L'exercice de transformation des questions fermées en questions ouvertes est le plus immédiatement transférable en réunion d'équipe.

**L'adresse de l'AFDEM n'était pas morte : son hôte mutualisé ne porte pas son nom. Corrigée le 25/10/2026**, l'hyperlien passant de `https://` à `http://`. Mesuré : `https://www.entretienmotivationnel.org/` rend HTTP 000 et `curl` **exit 60**, non parce que la page a disparu mais parce que le certificat présenté est celui de l'hébergement mutualisé OVH — `CN=cluster110.hosting.ovh.net`, **renouvelé le 19/10/2026**, donc vivant — sans aucun nom alternatif couvrant le domaine : *« no alternative certificate subject name matches target host name »*. Le site, lui, **répond** : en `http` il rend **HTTP 200 et 13 403 caractères utiles**, où `AFDEM` et son nom développé s'apparient au **degré ①**. L'archive était exclue d'office : le dernier instantané de l'hôte date du **12/12/2019**, sept ans avant la leçon.

**Ce que la correction coûte, et le marqueur le dit dans le document** : `http://` n'est pas chiffré, et un navigateur en HTTPS-first peut échouer là où `curl` réussit. Le lien reste donc utilisable mais dégradé — c'était le seul choix qui préserve l'accès à une ressource vivante, l'alternative étant de retirer un lien qui fonctionne.

**Requêtes passées** (ce qui n'y figure pas n'a pas été interrogé) : `curl -sS -o /dev/null -w "%{http_code} %{exitcode}"` avec **et** sans le faisceau du dépôt, sur `https://` et `http://`, forme nue et forme `www.` ; `openssl s_client -showcerts` pour la chaîne et les dates ; `aspirer.py` sur la forme `http` ; `chercher.py` sur `AFDEM` et *Association Francophone de Diffusion de l'Entretien Motivationnel* ; CDX Wayback sur `www.entretienmotivationnel.org` pour le dernier instantané à 200.

## Notes liées

- **⬅️ Précédente** · [[2026-07-13_lecon-entretien-motivationnel_03_quatre-processus]]
  dont OARS est la mise en œuvre
- **➡️ Suivante** · [[2026-07-13_lecon-entretien-motivationnel_05_discours-changement-darn-cat]]
  ces outils y sont mis au service d'un objectif précis
- **🔗 Pont** · [[2026-07-16_lecon-entretien-motivationnel_08_ecoute-reflective-approfondie]]
  où le reflet, esquissé ici, est décomposé en cinq niveaux
