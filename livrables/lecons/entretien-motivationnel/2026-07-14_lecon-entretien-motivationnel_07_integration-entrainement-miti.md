---
type: fiche-document
source: 2026-07-14_lecon-entretien-motivationnel_07_integration-entrainement-miti.docx
date_creation: 2026-08-14
date_lecon: 2026-07-14
parcours: entretien-motivationnel
numero: 7
statut: parcours-archive
tags:
  - parcours/entretien-motivationnel
  - outil/miti
  - concept/fidelite
  - concept/supervision
  - theme/certificat-mutualise
  - theme/https-vers-http
  - correction/2026-10-25
---

# 2026-07-14_lecon-entretien-motivationnel_07_integration-entrainement-miti

Document source : [[2026-07-14_lecon-entretien-motivationnel_07_integration-entrainement-miti.docx]]

## Résumé

La leçon la plus honnête du parcours, et la plus dérangeante. Son objet : **connaître l'EM ne garantit pas de le pratiquer**. On peut poser des questions ouvertes tout en glissant des conseils non sollicités — le réflexe correcteur passe par la porte de service.

La « fidélité » désigne le degré auquel une pratique correspond réellement à l'EM. Elle s'évalue avec le **MITI** (version 4.2.1), système de codage appliqué à des entretiens enregistrés, combinant scores globaux (partenariat, empathie, cultiver le discours-changement) et comptages de comportements. Un indicateur simple et redoutable : **le ratio reflets/questions, à viser au moins à 1, idéalement à 2**.

Le constat rapporté des études de fidélité est le passage à retenir : malgré formation et supervision approfondies, **la plupart des praticiens n'atteignent pas d'emblée un bon niveau de compétence**. La fidélité s'acquiert par la pratique enregistrée et le feedback — pas par la lecture.

C'est un garde-fou contre l'illusion de compétence, applicable bien au-delà de l'EM.

**L'adresse de l'AFDEM n'était pas morte : son hôte mutualisé ne porte pas son nom. Corrigée le 25/10/2026**, l'hyperlien passant de `https://` à `http://`. Mesuré : `https://www.entretienmotivationnel.org/` rend HTTP 000 et `curl` **exit 60**, non parce que la page a disparu mais parce que le certificat présenté est celui de l'hébergement mutualisé OVH — `CN=cluster110.hosting.ovh.net`, **renouvelé le 19/10/2026**, donc vivant — sans aucun nom alternatif couvrant le domaine : *« no alternative certificate subject name matches target host name »*. Le site, lui, **répond** : en `http` il rend **HTTP 200 et 13 403 caractères utiles**, où `AFDEM` et son nom développé s'apparient au **degré ①**. L'archive était exclue d'office : le dernier instantané de l'hôte date du **12/12/2019**, sept ans avant la leçon.

**Ce que la correction coûte, et le marqueur le dit dans le document** : `http://` n'est pas chiffré, et un navigateur en HTTPS-first peut échouer là où `curl` réussit. Le lien reste donc utilisable mais dégradé — c'était le seul choix qui préserve l'accès à une ressource vivante, l'alternative étant de retirer un lien qui fonctionne.

**Requêtes passées** (ce qui n'y figure pas n'a pas été interrogé) : `curl -sS -o /dev/null -w "%{http_code} %{exitcode}"` avec **et** sans le faisceau du dépôt, sur `https://` et `http://`, forme nue et forme `www.` ; `openssl s_client -showcerts` pour la chaîne et les dates ; `aspirer.py` sur la forme `http` ; `chercher.py` sur `AFDEM` et *Association Francophone de Diffusion de l'Entretien Motivationnel* ; CDX Wayback sur `www.entretienmotivationnel.org` pour le dernier instantané à 200.

## Notes liées

- **⬅️ Précédente** · [[2026-07-13_lecon-entretien-motivationnel_06_discordance-situations-difficiles]]
  qui achevait l'exposé des compétences ; ici on demande si elles sont réellement acquises
- **➡️ Suivante** · [[2026-07-16_lecon-entretien-motivationnel_08_ecoute-reflective-approfondie]]
  premier module avancé, consacré au geste le plus central
