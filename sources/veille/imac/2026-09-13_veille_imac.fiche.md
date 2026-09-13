---
type: fiche-document
source: 2026-09-13_veille_imac.docx
date_creation: 2026-09-13
date_veille: 2026-09-13
veille: imac
statut: veille-active
tags:
  - veille/imac
  - theme/imac-m6
  - theme/mac-mini-m6
  - theme/gurman
  - theme/hausse-des-prix
  - theme/reconditionne
  - theme/decision
  - theme/attribution-croisee
  - theme/source-non-citee
  - theme/publication-retenue
  - alerte/a-corriger
---

# 2026-09-13_veille_imac

Document source : [[2026-09-13_veille_imac.docx]]

## Résumé

**Le relevé marchand est juste, ligne à ligne, et la décision proposée est honnête.** J'ai rouvert les huit pages qui répondent : le comparateur consomac daté du 13/09 à 08:09 porte bien **1 499 € (−17 %)**, **1 689 € (−6 %)**, **1 999 €** et **2 199 € (−10 %)** pour les trois configurations suivies ; LDLC porte l'HP OmniStudio 27-cy0044nf à **1 899,95 → 1 599,95 €, −15 % « jusqu'au 21/09 (inclus) »**, Core Ultra 7 355, 49 TOPS, 27" Full HD 100 Hz, Wi-Fi 7, Windows 11 Famille, et le MSI Modern AM273QP AI à **1 699,95 €**, Core Ultra 7 155H, WQHD 2560×1440, Windows 11 Pro, garantie 5 ans ; GeeksLands (6 septembre) écrit « attendu en octobre avec la puce M6 gravée en 2 nm » ; le roundup MacRumors du 28 août classe l'iMac **« Don't Buy — Updates Soon »**. La continuité avec le 06/09 tient : mêmes promos LDLC, même Boulanger à 2 199 €, Mac mini M6 le 22/09 à 1 049 € ; seul le meilleur prix d'entrée a changé de marchand (Carrefour → Joybuy), et la note prend soin de dire que Joybuy est une marketplace à conditions à vérifier. Le tableau des trois scénarios — acheter, attendre, basculer — met les contre-arguments à leur place, y compris le plus gênant pour un acheteur d'iMac : **le seul M6 observable, le Mac mini, a pris +50 %**. Décompte des sources cohérent (6 ✅ + 2 ⚠️ + 3 ⛔ = 11), vérifié par le contrôle, et Apple Refurb honnêtement déclaré non lu — il ne répond pas davantage à un navigateur ce soir.

**Le défaut est au cœur de la note : le calendrier de l'iMac M6 repose sur deux citations attribuées à la mauvaise personne et à la mauvaise page — et la conclusion contredit la source citée.** La section « état des informations » donne deux phrases entre guillemets, *« All signs point to the M6 models being close to launch »* et *« Before the end of the year »*, toutes deux « (Gurman/Bloomberg, selon consomac.fr du 26/08/2026) ». Ni l'une ni l'autre n'est sur la page consomac, qui est en français. Elles sont sur **9to5Mac** — et la première n'est pas de Gurman : c'est la phrase de l'auteur de 9to5Mac (*« if you've been holding out for a new iMac, your wait shouldn't be much longer. All signs point to… »*) ; seule la seconde y est rapportée comme parole de Gurman. Pire : la dépêche consomac du 26/08, réellement ouverte et citée, écrit *« Selon le journaliste Mark Gurman… la sortie de cette révision serait prévue vers la fin du mois d'octobre »*. Or la note conclut en gras : *« Gurman dit “avant fin 2026”, octobre est une déduction MacRumors — pas une date confirmée »*. **C'est l'inverse de ce que dit sa propre source** : consomac attribue « fin octobre » à Gurman lui-même. La prudence de la note est bonne — Apple n'a rien annoncé — mais elle est construite sur une attribution fausse, et le lecteur qui ouvrirait consomac y lirait le contraire de la conclusion.

**Deux sources nommées sans lien, dont une que la note précédente liait.** *« Source : MacGeneration, communiqué Apple »* pour le prix et la date du Mac mini M6 — la veille du 06/09 liait l'article de macg.co du 25/08 ; celle-ci le nomme et ne le lie pas (le chiffre est par ailleurs sur GeeksLands, ce qui a suffi au contrôle). Et le titre MacRumors du 25/08, *« M6 MacBook Pro and M6 iMacs Likely Coming in October »*, cité pour dire qu'octobre est une estimation du site, renvoie au **roundup** et non à l'article — le titre n'y est pas, le contrôle l'a déclaré non vérifiable. Les specs M6 (+40-44 % CPU, 170 Go/s) sont annoncées « issues d'extraits, non vérifiées mot pour mot » : c'est écrit, c'est le bon geste, et c'est aussi la raison de ne pas s'en servir dans un tableau de décision.

**Une note conforme retenue trois heures par un défaut qui n'était pas le sien.** Le hook pre-push l'a contrôlée trois fois — 0 bloquant aux passes A, décompte cohérent — et l'a refusée trois fois, parce que la leçon revenus-passifs 08 du même matin, sur la même branche, nommait une page sans la lier. Publiée à 12h, avec la correction de l'autre. C'est le fonctionnement voulu, et c'est son prix : **un push porte la branche, pas un document**. Le contrôle complet, lui, n'avait pas tourné — le hook ne lance que les passes sans aspiration ; c'est lui, ce soir, qui a mis 9to5Mac sous *« All signs point »* et déclaré l'autre titre non vérifiable. Coût du job : **1,14 $** (29 % du plafond), 31 tours, 347 secondes.

**Ce qu'il faudrait corriger, dans l'ordre.** ① Réattribuer les deux citations : la première à 9to5Mac (auteur), la seconde à Gurman via 9to5Mac ; ② réécrire le résumé du calendrier : *consomac (26/08) rapporte que Gurman vise la fin octobre ; 9to5Mac (23/08) rapporte « before the end of the year » ; MacRumors (25/08) estime octobre* — trois sources, deux formulations, aucune date Apple ; ③ lier MacGeneration et l'article MacRumors du 25/08 au lieu du roundup. Rien à changer aux prix ni aux scénarios.

## Notes liées

- **⬅️ Précédente** · [[2026-09-06_veille_imac.fiche]]
  la continuité tient sur tout le relevé — LDLC, Boulanger, Mac mini M6 — et la note du 06/09 avait déjà le défaut miroir : elle liait MacGeneration mais n'en rapportait pas le chiffre décisif ; celle-ci rapporte le chiffre et ne lie plus la page
- **🔗 Pont** · [[2026-09-13_lecon-revenus-passifs_08_outils-creation-hebergement-paiement]]
  la leçon qui a retenu cette veille à la porte : un lien manquant là-bas, trois heures de retard ici. Premier cas concret du coût d'une branche unique pour quatorze jobs
- **🔗 Pont** · [[2026-09-11_veille_ai-act.fiche]]
  même famille de défaut, deux jours plus tôt : une citation exacte prêtée à la mauvaise page. Ici s'y ajoute la mauvaise personne — la phrase d'un rédacteur de 9to5Mac mise dans la bouche de Gurman — et une conclusion qui contredit la dépêche qu'elle cite. La règle 10 d'ai-act (un constat fait avec le même outil se répète, il ne se confirme pas) a une cousine ici : **un extrait de recherche ne dit pas qui parle**
- **🔗 Pont** · [[2026-06-09_veille_ai-act.fiche]]
  la prudence du 13/09 sur le calendrier M6 est du même type que celle de juin sur l'AI Omnibus : la note refuse de dater ce qu'Apple ou la Commission n'a pas daté. Bon réflexe — à condition que l'attribution des dates aux rumeurs soit juste, ce qui manque ici
