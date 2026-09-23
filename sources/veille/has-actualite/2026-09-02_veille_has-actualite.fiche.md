---
type: fiche-document
source: 2026-09-02_veille_has-actualite.docx
date_creation: 2026-09-02
date_veille: 2026-09-02
veille: has-actualite
statut: veille-active
tags:
  - veille/has-actualite
  - theme/semaine-creuse
  - theme/vie-intime
  - theme/protection-enfance
  - theme/prevention-specialisee
  - controle/liens
  - alerte/dates
  - alerte/corrige
  - correction/2026-09-21
---

# 2026-09-02_veille_has-actualite

Document source : [[2026-09-02_veille_has-actualite.docx]]

## Résumé

**Première note produite après le durcissement du prompt sur les liens, et le contrôle tient.** J'ai recompté indépendamment : **13 relations hypertexte** dans le document, **13 balises `<w:hyperlink>`** — aucun lien orphelin —, pour **7 cibles uniques**, toutes testées à la main et **toutes en 200**. Aucune adresse tronquée, aucune URL de rubrique générique : la note pointe des pages HAS précises, notes de cadrage et appels à candidatures compris. Le job a exécuté le nouveau contrôle et l'a cité dans son récapitulatif. Progression sur cinq semaines : 4 → 7 → 9 → 5 → **13**. Réserve honnête : cette note passe par l'étape 7 du pipeline ; l'instruction ajoutée à l'étape 4a — celle qui vise les veilles RBPP, à **zéro lien sur quatre notes d'affilée** — n'est toujours pas exercée, faute de nouvelle RBPP depuis le 27 juin.

**Le défaut de cette note est ailleurs : elle prend des dates de fichier pour des dates de publication.** Le bloc « Dernières RBPP publiées » liste 27/06 PPA-DUI, 22/06 vie intime volet 1, 15/06 habitat volet 2, 06/06 autisme. Ce sont les dates des **veilles du dépôt**, pas celles de la HAS. Vérifié sur deux d'entre elles : la RBPP Autisme a été **publiée le 12 février 2026** — la veille du 06/06 l'écrit elle-même en première page —, et le guide PPA-DUI a été **publié le 24 juin 2026**, après adoption par la CSMS le 12 mai. Pire, la « rectification » que la note s'applique à elle-même est **à moitié fausse** : « publication initiale 12/02/2025 » est juste (la page HAS affiche *« Mis en ligne le 12 févr. 2025 »*), mais « dernière actualisation 22/06/2026 » ne l'est pas — la HAS indique **14/11/2025**, et 22/06/2026 est, une fois encore, la date du fichier de veille. Corriger une erreur en en réintroduisant une autre, à partir de la même confusion.

**Sur le fond, semaine calme et tri pertinent.** Aucune RBPP opposable publiée dans la fenêtre, ce que la note dit franchement. Quatre travaux en cours sont suivis, et surtout **le tri enfance / adultes est fait et il est juste** : la RBPP protection de l'enfance vise foyers de l'enfance, MECS et pouponnières, « pas directement les foyers d'hébergement pour adultes handicapés » ; la prévention spécialisée vise le milieu ouvert, avec la nuance que **les recommandations sur la coordination territoriale seront transférables** aux pratiques partenariales. C'est exactement le travail qu'on attend d'une veille : ne pas tout déverser, mais dire ce qui touche l'établissement et ce qui ne le touche pas.

**Ce qui te concerne vraiment — et une échéance à ne pas attendre.** La note annonce un « fort impact attendu pour tous les ESSMS accueillant des adultes » pour le **volet 2** de la RBPP vie intime, affective et sexuelle, sans date de publication. Elle recommande de préparer les protocoles internes d'ici là. Mais elle ne redit pas ce que la fiche du 22/06 avait retenu et que j'ai revérifié sur la page HAS : **le volet 1 est déjà opposable et a été actualisé le 14 novembre 2025** pour intégrer la **loi n° 2025-1057 du 6 novembre 2025** modifiant la définition pénale du viol et des agressions sexuelles. Attendre le volet 2 pour agir serait une erreur de calendrier : le socle transversal existe, il est à jour du droit pénal, et il s'applique dès maintenant.

**Corrigé le 21/09/2026, journal de huit entrées dans le document — dix-neuf jours après la fiche, parce que la note du 21/09 en avait hérité les dates.** Le bloc « Dernières RBPP publiées » est refait aux dates du site HAS, pages ouvertes et liées : guide PPA-DUI *validé le 12 mai 2026, mis en ligne le 24 juin 2026* ; RBPP autisme *validée le 08 janvier 2026, mise en ligne le 12 févr. 2026* ; habitat volet 2 *validée le 04 novembre 2025, mise en ligne le 25 nov. 2025* ; vie intime volet 1 *12 févr. 2025*, *« Mise à jour 14/11/2025 »* — le 27/06, le 06/06, le 15/06 et le 22/06 étaient les dates des fichiers du dépôt, et la « rectification » de la note est nommée pour ce qu'elle était. Deux projections sortent : *« la prochaine vague de publications est attendue à l'automne 2026 »* et *« publication finale attendue fin 2027 »* devient le *« passage en commission : 4ème trimestre 2027 »* de la note de cadrage ; l'article des 22 ans est lié ; le flux RSS *Recommandations et guides*, lu le 21/09, confirme la semaine creuse du 26/08 au 02/09 et entre dans les sources. Douze ✅, `controle_attributions` exit 0 (deux A RELIRE, titres abrégés de la note elle-même), `controle_decompte` sans décompte à comparer (la note n'en annonçait pas), étape 7.6 bis du prompt → OK. Ce que cette correction ne répare pas : la note du 14/09, qui n'a jamais eu le bloc, et l'habitude — trois éditions sur quatre — de ne pas lier ce qu'on date.

## Notes liées

- **⬅️ Précédente** · [[2026-08-31_veille_has-actualite]]
  même format à deux jours d'écart, la seconde produite hors créneau pour tester le durcissement. Celle du 31/08 portait la loi sur l'aide à mourir et l'absence de clause de conscience pour les professionnels d'ESSMS — point autrement plus lourd que tout ce qui figure ici
- **🔗 Pont** · [[2026-06-22_veille_rbpp_vie-intime-affective-sexuelle-volet1.fiche]]
  **la fiche qui avait les bonnes dates** : validation 14/01/2025, mise à jour 14/11/2025 intégrant la loi n° 2025-1057. La note du 02/09 réintroduit une actualisation « 22/06/2026 » qui n'existe pas. Le corpus de fiches est ici plus fiable que la veille du jour
- **🔗 Pont** · [[2026-09-02_veille_SERAFIN-PH.fiche]]
  **deux notes du même jour, deux régimes de liens** : SERAFIN, produite avant le durcissement, n'en porte aucun et publie une adresse CNSA en 404 ; celle-ci en porte treize, tous testés. La différence tient à une instruction ajoutée entre les deux
- **🗂️ Dossier** · [[RBPP_dossier.fiche]]
  à corriger sur le même travers si le catalogue reprend les dates de fichier : les dates de veille du dépôt ne sont pas les dates de publication HAS, et l'écart atteint quatre mois sur la RBPP Autisme
