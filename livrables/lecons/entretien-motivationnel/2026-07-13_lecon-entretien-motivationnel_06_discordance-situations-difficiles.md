---
type: fiche-document
source: 2026-07-13_lecon-entretien-motivationnel_06_discordance-situations-difficiles.docx
date_creation: 2026-08-14
date_lecon: 2026-07-13
parcours: entretien-motivationnel
numero: 6
statut: parcours-archive
tags:
  - parcours/entretien-motivationnel
  - concept/discordance
  - concept/ethique
  - concept/autonomie
  - theme/certificat-mutualise
  - theme/https-vers-http
  - correction/2026-10-25
---

# 2026-07-13_lecon-entretien-motivationnel_06_discordance-situations-difficiles

Document source : [[2026-07-13_lecon-entretien-motivationnel_06_discordance-situations-difficiles.docx]]

## Résumé

Leçon qui clôt le socle fondamental par les moments de friction et la déontologie.

Le déplacement terminologique est significatif : **l'EM moderne abandonne la « résistance », qui blâme la personne, au profit de la « discordance »**, qui décrit un état de la relation. Interruption, argumentation, désengagement, minimisation ne sont pas des affronts : ce sont des informations, généralement sur un excès de réflexe correcteur ou un cap fixé trop vite.

La réponse est contre-intuitive et centrale : **quand la friction monte, ce n'est pas le moment de pousser plus fort** — c'est le signe qu'il faut revenir à l'engagement. Refléter, souligner l'autonomie, changer d'orientation. Jamais forcer.

La section éthique tranche une question qu'on pose souvent à l'EM : **est-ce de la manipulation ?** La réponse tient à la direction — l'EM fait émerger les motivations propres de la personne au service de ses objectifs à elle. Employer ces techniques pour l'amener où elle ne veut pas aller trahit PACE et devient effectivement de la manipulation. L'intention et la transparence font la différence.

**L'adresse de l'AFDEM n'était pas morte : son hôte mutualisé ne porte pas son nom. Corrigée le 25/10/2026**, l'hyperlien passant de `https://` à `http://`. Mesuré : `https://www.entretienmotivationnel.org/` rend HTTP 000 et `curl` **exit 60**, non parce que la page a disparu mais parce que le certificat présenté est celui de l'hébergement mutualisé OVH — `CN=cluster110.hosting.ovh.net`, **renouvelé le 19/10/2026**, donc vivant — sans aucun nom alternatif couvrant le domaine : *« no alternative certificate subject name matches target host name »*. Le site, lui, **répond** : en `http` il rend **HTTP 200 et 13 403 caractères utiles**, où `AFDEM` et son nom développé s'apparient au **degré ①**. L'archive était exclue d'office : le dernier instantané de l'hôte date du **12/12/2019**, sept ans avant la leçon.

**Ce que la correction coûte, et le marqueur le dit dans le document** : `http://` n'est pas chiffré, et un navigateur en HTTPS-first peut échouer là où `curl` réussit. Le lien reste donc utilisable mais dégradé — c'était le seul choix qui préserve l'accès à une ressource vivante, l'alternative étant de retirer un lien qui fonctionne.

**Requêtes passées** (ce qui n'y figure pas n'a pas été interrogé) : `curl -sS -o /dev/null -w "%{http_code} %{exitcode}"` avec **et** sans le faisceau du dépôt, sur `https://` et `http://`, forme nue et forme `www.` ; `openssl s_client -showcerts` pour la chaîne et les dates ; `aspirer.py` sur la forme `http` ; `chercher.py` sur `AFDEM` et *Association Francophone de Diffusion de l'Entretien Motivationnel* ; CDX Wayback sur `www.entretienmotivationnel.org` pour le dernier instantané à 200.

## Notes liées

- **⬅️ Précédente** · [[2026-07-13_lecon-entretien-motivationnel_05_discours-changement-darn-cat]]
  dont le discours-maintien est le versant verbal de ce qui se joue ici dans la relation
- **➡️ Suivante** · [[2026-07-14_lecon-entretien-motivationnel_07_integration-entrainement-miti]]
  qui clôt le module par la question de la fidélité réelle à la méthode
