---
type: fiche-document
source: 2026-09-14_veille_has-actualite.docx
date_creation: 2026-09-14
date_veille: 2026-09-14
veille: has-actualite
statut: veille-active
tags:
  - veille/has-actualite
  - registre/pro
  - theme/semaine-securite-patients
  - theme/csms
  - theme/rbpp-en-cours
  - theme/protection-enfance
  - theme/habitat
  - theme/citation-inexacte
  - theme/source-non-listee
  - theme/regression-edition
  - theme/adresse-perimee
  - alerte/corrige
  - correction/2026-09-14
  - correction/2026-09-21
---

# 2026-09-14_veille_has-actualite

Document source : [[2026-09-14_veille_has-actualite.docx]]

## Résumé

**L'actualité de la semaine est juste, et c'est la bonne.** L'article HAS du 11 septembre existe, il dit ce que la note lui fait dire : Semaine de la sécurité des patients du **14 au 18 septembre**, consacrée aux *personnes atteintes de pathologies chroniques*, un « défi collectif : mieux articuler les interventions, **décloisonner** les secteurs sanitaire, social et médico-social », et trois leviers dont les intitulés sont ceux de la page — *coordonner et fluidifier les parcours*, *connaître et prévenir les risques liés aux soins*, *renforcer l'engagement des patients et la participation des personnes*. Pas de RBPP publiée dans la fenêtre : exact. Le calendrier HAS porte bien la réunion **CSMS du mardi 29 septembre, 9h30-17h**, et le webinaire du 23 à 12h30-14h. La consultation d'usagers sur les actes esthétiques est réelle : appel mis en ligne le **8 septembre**, clôture le **30 septembre**, 6 à 8 usagers ayant eu recours à des actes non chirurgicaux — et la note a raison de la classer hors périmètre. Décompte **2 ✅ | 1 consultée | 2 ⛔ — 5 tentées**, cohérent au contrôle ; les trois liens répondent 200 ; la note nomme ses deux pages ⛔ et pourquoi. Coût **1,85 $** (46 % du plafond), 47 tours, 11 minutes ; hook `--docs` passé.

**Un titre entre guillemets qui n'est pas celui de la page — attrapé par le contrôle né ce matin.** *« 6e cycle de certification : premiers résultats et perspectives vers 2030 »* : le calendrier HAS écrit **« premiers résultats et cap sur 2030 »**. Trois mots changés dans une citation de neuf, sous une source nommée (« Source : calendrier HAS »). La passe B-FR (㉖), écrite quelques heures plus tôt pour la leçon psychopathologie 16, rend sur cette note **exit 1 — « ABSENTE DE LA SOURCE NOMMEE … prêtée à has-sante.fr (3 pages françaises lues, aucune ne la porte) »** ; le job, lui, a tourné avant ㉖ et a déclaré « 0 bloquant ». Il a fallu au passage lever un filtre du contrôle : une citation commençant par un chiffre (« 6e cycle… ») n'était pas lue. C'est le premier document du dépôt où B-FR mord sans qu'on l'ait cherché.

**Deux régressions par rapport à l'édition du 02/09, sur les mêmes travaux.** Le 02/09, la même veille écrivait : *« Accompagner dans et vers l'habitat – volet 3 – appel à candidatures précédemment ouvert (clôture 03/04/2026) »* et *« l'appel à candidatures [vie quotidienne 3-11 ans] se clôt le 4 septembre 2026 »*, pages ouvertes à 200. Le 14/09, les deux pages renvoient une page d'**identification** (HTTP 200, formulaire de connexion — les appels clos passent derrière un login ; vérifié avec deux agents et par WebFetch), et la note écrit pour l'habitat : *« Appel à candidatures en cours, statut non confirmé au 14/09/2026 »*. Un appel clos depuis cinq mois, que la note précédente datait, redevient « en cours ». Pour la protection de l'enfance, la note garde « clôturé début septembre » (juste) mais ajoute *« publication estimée : 2027 (délai habituel 18-24 mois après constitution du groupe) »* : un « délai habituel » de mémoire, alors que la **note de cadrage adoptée le 7 juillet 2026** — dans le dépôt depuis le 09/07, ouverte pour cette fiche — donne le calendrier : composition des groupes 09-10/2026, travaux 11/2026-10/2027, relecture 07-09/2027, **passage en commission 4e trimestre 2027**. La source de rang 1 existait, publique, et la note a préféré une règle de pouce sous une page ⛔.

**Une source utilisée sans être listée, et une adresse qui ment sur ce qu'elle ouvre.** La consultation esthétique (8 → 30 septembre, profil des usagers) est exacte — mais aucune des cinq sources listées ne la porte : ni le calendrier, ni la page des publications SMS, ni l'article SSP. Elle vient de la page d'appel `p_4391619`, que la note n'a ni liée ni comptée : le décompte est cohérent avec la liste, la liste n'est pas cohérente avec le corps (règle 3, deuxième tiret). Et l'article SSP est lié par `…/p_3644382/fr/semaine-de-la-securite-des-patients-**2025**-la-has-aussi-engagee-dans-la-securite-des-soins-**pediatriques**` : la HAS a réutilisé l'identifiant de l'article 2025, le serveur ignore le slug et sert bien la page 2026 — mais le lecteur qui lit le lien croit ouvrir l'article de l'an dernier sur les soins pédiatriques. Le canonique de la page est `…/semaine-de-la-securite-des-patients-2026-la-has-engagee-pour-des-parcours-plus-surs`. Plus petit : la note de méthode du job annonce que le format de ses liens a été « corrigé » pour le contrôle du décompte — c'est le job qui s'adapte au test, dans le bon sens.

**Corrigé le 14/09/2026, journal dans le document — cinq corrections, toutes dans « À venir » et « Sources ».** ① Le titre du webinaire au mot près (« cap sur 2030 ») ; ② habitat volet 3 : appel clos le 3 avril 2026 d'après l'édition du 02/09, groupe de travail en cours, page désormais derrière une identification ; ③ protection de l'enfance : la **note de cadrage** (validée le 7 juillet, en ligne le 9) liée, avec son calendrier — groupes 09-10/2026, travaux 11/2026-10/2027, relecture 07-09/2027, passage en commission 4e trimestre 2027 — à la place du « délai habituel » ; ④ la page de la consultation esthétique liée dans le corps et ajoutée aux sources, décompte **3 ✅ | 1 | 2 ⛔ — 6**, cohérent ; ⑤ l'adresse canonique de l'article SSP. Le contrôle a mordu une seconde fois — sur ma propre correction : j'avais mis dans la liste des sources un titre *résumé* entre guillemets (« Consultation ciblée d'usagers — guide méthodologique actes à visée esthétique »), et B-FR l'a déclaré absent de la page ; le titre exact y est maintenant. Sauvegarde d'avant correction en `temoins_attributions_avant_correction/` (exit 1). **Le prompt `rbpp-pipeline`** (26 071 → 31 076) reçoit, à l'étape 7 : la relecture de l'édition précédente avant toute recherche (*une édition ne peut pas savoir moins que la précédente*, triée par nom et non par date de fichier — `ls -t` rendait le 10/08 corrigé avant le 02/09), *une page ⛔ n'autorise pas un fait de mémoire quand une source publique le porte* (la note de cadrage, le dépôt), *ce que tu utilises, tu le listes*, et l'appel à `controle_attributions.py` en 7.5 ; le garde-fou 4 reçoit l'incident du titre et le test B-FR ; le garde-fou 6, l'adresse canonique (`<link rel="canonical">`). Commandes ré-extraites du prompt et exécutées telles quelles : `ls | sort | tail -2` → 02/09 puis 14/09 ; attributions → exit 0 sur la note corrigée, exit 1 sur la sauvegarde ; décompte → COHÉRENT ; le grep canonique rend l'adresse 2026.

**Corrigé une seconde fois le 21/09/2026 — deux lignes, au passage du contrôle de note ajouté au prompt.** « RBPP en élaboration — *Horizon 2027 probable* » : une projection restée dans les Impacts après que la correction du 14/09 avait ramené le calendrier de la note de cadrage au § À venir ; elle devient *passage en commission prévu au 4e trimestre 2027 selon sa note de cadrage*. Et « Pas de nouvelle RBPP » reçoit sa source : le flux RSS *Recommandations et guides* de la HAS, lu le 21/09, aucune entrée du secteur du 7 au 14 septembre — décompte **4 ✅ | 1 | 2 ⛔ — 7**, COHÉRENT, exit 0, étape 7.6 bis → OK. Journal du 21/09 ajouté sous celui du 14/09.

## Notes liées

- **⬅️ Précédente** · [[2026-09-02_veille_has-actualite.fiche]]
  le 02/09 avait treize liens en 200, dont les deux appels à candidatures que le 14/09 déclare inaccessibles — les pages ont basculé derrière un login entre les deux éditions, et la note du 14/09 a perdu avec elles ce que celle du 02/09 savait : la clôture du 03/04/2026 pour l'habitat volet 3
- **🔗 Pont** · [[2026-07-09_veille_rbpp_vie-quotidienne-enfants-3-11-ans-pe.fiche]]
  la note de cadrage du 7 juillet 2026, lue page à page en juillet : composition des groupes 09-10/2026, passage en commission 4e trimestre 2027. C'est la source que la note du 14/09 remplace par « délai habituel 18-24 mois » — et le dépôt l'avait déjà relue en entier
- **🔗 Pont** · [[2026-09-14_lecon-psychopathologie_16_handicap-psychique-deficience-intellectuelle]]
  la passe B-FR est née le matin sur cette leçon (« contradictoires » prêté à l'INSERM) ; l'après-midi elle mord ici sur un titre de webinaire recopié de travers — deux documents, deux parcours, le même geste : une citation qui n'est pas sur la page de la source nommée
- **🔗 Pont** · [[2026-09-13_controle-livrables]]
  la note de contrôle d'hier lisait « exit 3 » là où le contrôle disait « page non lue » ; celle-ci lit « authentification requise » là où la page dit « Identification » — juste, cette fois, mais la même page était ouverte douze jours plus tôt, et rien dans la note ne le dit
