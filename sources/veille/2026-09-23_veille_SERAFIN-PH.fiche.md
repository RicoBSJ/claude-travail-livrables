---
type: fiche-document
source: 2026-09-23_veille_SERAFIN-PH.docx
date_creation: 2026-09-23
date_veille: 2026-09-23
veille: serafin-ph
statut: veille-active
tags:
  - veille/serafin-ph
  - registre/pro
  - theme/reforme-tarifaire
  - theme/dotation-complementaire
  - theme/sidoba
  - theme/semaine-creuse
  - source/cnsa
  - source/handicap-gouv
  - source/atih
  - theme/decompte-ambigu
  - theme/liste-de-memoire
  - alerte/corrige
  - correction/2026-09-23
---

# 2026-09-23_veille_SERAFIN-PH

Document source : [[2026-09-23_veille_SERAFIN-PH.docx]]

## Résumé

**Une semaine creuse honnêtement déclarée, un push refusé pour une virgule de décompte, et une liste de six critères qui ne vient de nulle part.** La note dit franchement qu'aucune publication SERAFIN-PH n'a paru entre le 16 et le 23/09 et range tout le reste en « Rappel / Contexte » daté — c'est la règle 7 appliquée. Les quatre pages institutionnelles répondent 200 et portent ce qu'elle leur prête : le communiqué de handicap.gouv.fr confirme *« une mise en œuvre opérationnelle de la réforme tarifaire au 1er janvier 2027 pour les ESMS handicap du secteur "enfant" »*, *« Camille Galliard-Minier, ministre chargée de l'Autonomie et des Personnes handicapées, a présidé le 14ᵉ comité stratégique »*, le recueil *« lancé à partir du 30 mars 2026 »* ; la CNSA porte la *« période de convergence prévue sur 8 ans »* à compter du 1er janvier 2027, les deux phases du recueil PH 2026 (mars : caractéristiques des places ; mai : *« une dizaine de variables »* d'activité et *« six variables »* de dotation complémentaire), l'année blanche, et *« le décret du 13 mai 2026 précise les modalités de transmission »* ; l'ATIH porte RAMSECE-PH et la trajectoire de convergence. Le périmètre enfance et l'exclusion des ESMS adultes sont justes. Légifrance est en 403 pour tout le monde, y compris avec un agent de navigateur.

**Corrigé le 23/09/2026, journal de six entrées.** ① Le **décompte** annonçait *« 3 ✅ | 1 source ⚠️ HTTP 200 | 1 source ⚠️ 403 »* — deux ⚠️ comptées une par une, sans total, quand le pied de note en annonçait 2 : `controle_decompte` a lu « 1 annoncé pour ⚠, liste 2 » et **le hook a refusé le push trois fois**, retenant avec cette note la leçon ennéagramme du même matin, conforme. Réécrit en **4 ✅ | 1 ⚠️ — 5 tentées**, COHÉRENT. ② La page CNSA *« préparation recueil PH 2026 »* était marquée *« non ouverte directement, fond documentaire »* alors que son contenu irrigue le corps (les deux phases, les 10 et 6 variables) : passée en ✅, ce qui est la règle 3 (*✅ = ouverte ET reprise*). ③ **Les six critères de la dotation complémentaire** — *« complexité de situation, scolarisation en milieu ordinaire, coopération, soutien en environnement ordinaire, autodétermination, usage du numérique »*, avec la consigne *« vérifier comment l'ESMS se positionne sur chaque critère »* — ne figurent sur **aucune** des cinq sources : la CNSA n'écrit que *« six variables »*. Un fait de mémoire, prescriptif, dans un tableau de vigilance adressé à une direction ; remplacé par ce que la source dit et par la consigne de poser la question à l'ARS. ④ Le **décret** : Légifrance en 403, et ni le numéro *2026-376* ni *l'art. 90 de la LFSS 2026* ne sont sur les quatre autres pages — seule la date du 13 mai est sourcée, par la CNSA ; les deux références sont désormais données comme à confirmer. ⑤ Les **simulations** étaient placées à l'automne 2026 ; la source écrit que la fiabilisation des données court *« jusqu'à l'automne 2026 »* et que les simulations sont transmises *« ensuite »*. ⑥ La date du **23 mars 2026** n'est pas sur la page : elle se déduit de *« Ce lundi »* et du *« Publié le 27/03/2026 »* — c'est écrit maintenant. `controle_attributions` **exit 0**, décompte COHÉRENT.

**Ce que cette note apprend sur l'outillage.** Le prompt `serafin-ph-veille` (24 656 octets) porte la règle 3 — *décompte exact, recompte avant d'écrire* — **sans aucun test mécanique** : ni `controle_decompte.py`, ni `controle_attributions.py` n'y sont appelés, alors qu'`ai-act` et `rbpp-pipeline` les lancent depuis le 12/09. La note est donc partie avec son ambiguïté, et c'est le **hook pre-push** qui l'a arrêtée — en bloquant du même coup un livrable conforme produit une heure plus tard. Le garde-fou a fonctionné, au prix le plus élevé : deux jobs retenus, trois commits en attente, et une leçon publiée avec un jour de retard. Les six critères, eux, ne sont vus par aucun contrôle : aucune passe ne cherche une liste sans nom de source.

## Notes liées

- **⬅️ Précédente** · [[2026-09-16_veille_SERAFIN-PH.fiche]]
  même format, même semaine creuse assumée ; la nouveauté de celle-ci est d'avoir été arrêtée par le hook — la première note du dépôt refusée à la publication pour un décompte
- **🔗 Pont** · [[2026-09-23_lecon-enneagramme_17_relations-couple-famille-conflits]]
  **le livrable retenu avec elle** : conforme, 0 bloquant, non publié pendant une journée parce que les deux jobs poussent sur la même branche
- **🔗 Pont** · [[2026-09-21_veille_has-actualite.fiche]]
  l'autre veille du dépôt qui a reçu, le même week-end, un contrôle de note (étape 7.6 bis) ; `serafin-ph-veille` n'appelle toujours aucun des deux contrôles communs
- **🗂️ Dossier** · [[SERAFIN-PH_dossier.fiche]]
  à compléter du calendrier confirmé — 1er janvier 2027 secteur enfance, convergence sur 8 ans — et de la question ouverte : quelles sont les six variables de la dotation complémentaire ?

