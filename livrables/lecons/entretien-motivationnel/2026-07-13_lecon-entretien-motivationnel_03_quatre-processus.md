---
type: fiche-document
source: 2026-07-13_lecon-entretien-motivationnel_03_quatre-processus.docx
date_creation: 2026-08-14
date_lecon: 2026-07-13
parcours: entretien-motivationnel
numero: 3
statut: parcours-archive
tags:
  - parcours/entretien-motivationnel
  - processus/engager
  - processus/focaliser
  - processus/evoquer
  - processus/planifier
  - theme/certificat-mutualise
  - theme/https-vers-http
  - correction/2026-10-25
---

# 2026-07-13_lecon-entretien-motivationnel_03_quatre-processus

Document source : [[2026-07-13_lecon-entretien-motivationnel_03_quatre-processus.docx]]

## Résumé

Quatre processus — engager, focaliser, évoquer, planifier — et une mise en garde qui fait tout l'intérêt de la leçon : **ce ne sont pas quatre étapes**. Ils s'imbriquent, se superposent, et l'on y revient sans cesse. Ce n'est pas une check-list.

*Engager* établit la relation de confiance ; sans lien, rien ne suit. *Focaliser* clarifie ensemble un cap. *Évoquer* fait émerger les motivations propres de la personne — c'est le cœur de la méthode. *Planifier* co-construit des pas concrets, quand la personne est prête.

L'exercice d'auto-observation est le plus instructif du parcours : repérer par où l'on commence habituellement. **Beaucoup sautent directement à « planifier »** — donner le plan — sans avoir engagé ni évoqué. C'est le défaut professionnel le plus courant, et il explique la plupart des échecs attribués à la « mauvaise volonté » de la personne.

**L'adresse de l'AFDEM n'était pas morte : son hôte mutualisé ne porte pas son nom. Corrigée le 25/10/2026**, l'hyperlien passant de `https://` à `http://`. Mesuré : `https://www.entretienmotivationnel.org/` rend HTTP 000 et `curl` **exit 60**, non parce que la page a disparu mais parce que le certificat présenté est celui de l'hébergement mutualisé OVH — `CN=cluster110.hosting.ovh.net`, **renouvelé le 19/10/2026**, donc vivant — sans aucun nom alternatif couvrant le domaine : *« no alternative certificate subject name matches target host name »*. Le site, lui, **répond** : en `http` il rend **HTTP 200 et 13 403 caractères utiles**, où `AFDEM` et son nom développé s'apparient au **degré ①**. L'archive était exclue d'office : le dernier instantané de l'hôte date du **12/12/2019**, sept ans avant la leçon.

**Ce que la correction coûte, et le marqueur le dit dans le document** : `http://` n'est pas chiffré, et un navigateur en HTTPS-first peut échouer là où `curl` réussit. Le lien reste donc utilisable mais dégradé — c'était le seul choix qui préserve l'accès à une ressource vivante, l'alternative étant de retirer un lien qui fonctionne.

**Requêtes passées** (ce qui n'y figure pas n'a pas été interrogé) : `curl -sS -o /dev/null -w "%{http_code} %{exitcode}"` avec **et** sans le faisceau du dépôt, sur `https://` et `http://`, forme nue et forme `www.` ; `openssl s_client -showcerts` pour la chaîne et les dates ; `aspirer.py` sur la forme `http` ; `chercher.py` sur `AFDEM` et *Association Francophone de Diffusion de l'Entretien Motivationnel* ; CDX Wayback sur `www.entretienmotivationnel.org` pour le dernier instantané à 200.

## Notes liées

- **⬅️ Précédente** · [[2026-07-11_lecon-entretien-motivationnel_02_ambivalence-reflexe-correcteur]]
  dont le réflexe correcteur est précisément ce qui fait sauter les deux premiers processus
- **➡️ Suivante** · [[2026-07-13_lecon-entretien-motivationnel_04_oars-ouver]]
  les micro-compétences qui font vivre ces processus
