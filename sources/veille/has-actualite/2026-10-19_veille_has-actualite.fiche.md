---
type: fiche-document
source: 2026-10-19_veille_has-actualite.docx
date_creation: 2026-10-19
date_veille: 2026-10-19
veille: has-actualite
statut: veille-active
tags:
  - veille/has-actualite
  - registre/pro
  - concept/appels-a-candidatures
  - concept/csms
  - concept/calendrier-has
  - source/has
  - source/flux-rss
  - theme/faux-refus-du-controle
  - theme/jeton-commun-dans-un-sens-different
  - theme/correctif-tls-tenu-en-production
  - theme/exemption-de-chemin-verifiee
  - theme/quatre-corrections-qui-tiennent
  - theme/graphie-numerique-contre-graphie-en-mots
  - theme/inaccessibilite-heritee-sans-adresse
  - theme/passe-D-inerte-sur-un-document-de-dates
  - theme/plafond-a-93-pour-cent
  - alerte/push-refuse
  - correction/2026-10-19
  - alerte/faux-refus
---

# 2026-10-19_veille_has-actualite.fiche

Document source : [[2026-10-19_veille_has-actualite.docx]]

## Résumé

**Le document est juste, et c'est le contrôle qui refuse le push — pour la deuxième fois sur trois.** `controle_edition_precedente` a refusé trois tentatives sur un seul jeton : *« INTERDIT « Commission » — retiré du corps de 2026-10-12 par une correction, présent dans celui-ci »*, la formulation d'origine étant *« toutes validées le 29/09/2026 par la Commission en charge du social et du médico-social (CSMS) »*. Cette correction du 12/10 était juste : les trois pages ne portaient ni « CSMS » ni « Commission », et la note donnait pour lue une inférence. ⚠️ **Mais le « Commission » du 19/10 désigne un autre objet, et il est exact** : la note écrit *« Semaine 19-25 octobre : CNEDIMTS (20/10), CTV (20/10), Commission de la transparence (21/10) — hors secteur social & médico-social »*, et le calendrier HAS, aspiré ce jour, porte littéralement **`21/10/2026 Commission Commission de la transparence - Réunion du 21 octobre 2026`**, comme il porte `20/10/2026 Commission CNEDIMTS` et `20/10/2026 Commission CTV`. La page est listée dans les sources, elle répond 200 pour 9 506 caractères, et la note signale elle-même que l'item est hors secteur. 🔴 **Le resserrement du 14/10 ne sépare pas ce cas** : il exige que la citation d'origine soit suivie d'une dénonciation (elle l'est — « zéro occurrence ») et que le jeton ne soit pas en tête de citation (il ne l'est pas). **Bilan du motif ① en production : trois refus, deux faux** — serafin-ph le 14/10 (« Inaccessible », « Semaine »), la veille iMac le 18/10 (vrai : « 2031 » était faux), celle-ci aujourd'hui. 🔧 **CORRIGÉ LE 19/10/2026, et la piste que j'avais proposée ici était FAUSSE.** J'avais écrit qu'il suffirait d'exiger **deux mots consécutifs** de recouvrement avec la citation : mesuré, cela perd le vrai rejeu du 18/10, parce que *« oct. 2031 »* et *« octobre 2031 »* ne se recouvrent pas. Deux autres bornes ont été mesurées puis abandonnées — la fréquence du jeton dans la série (Commission 26 %, Microsoft 23 %, 2031 35 %, TSMC 17 % : entrelacées) et le nombre de jetons revenus (1 pour « TSMC », qui est le rejeu fondateur). **La borne retenue est l'ACCOMPAGNEMENT** : un jeton revenu ne bloque que si un autre mot de sa citation figure à moins de **80 caractères**, le vocabulaire de la série étant écarté (un mot présent 5 fois ou plus dans le corps de N-1). Mesures : « Microsoft » à **47** caractères de « 2031 » ; « CSMS », seul accompagnateur non calendaire de « Commission », à **128**. **Balayage : 108 veilles, un seul verdict change — celui-ci.** Deux témoins gelés de plus au harnais, dont celui-ci qui doit être **ACCEPTÉ** avec sa ligne « À RELIRE « Commission » ».

**Les deux correctifs de la veille ont tenu, et cela se mesure.** ① **TLS** : les **huit** adresses HAS de la note répondent **HTTP 200**, revérifiées ce jour une par une (47 698 · 45 883 · 3 711 · 9 506 · 14 107 · 14 788 · 13 737 · 11 437 caractères utiles), et le job s'est exécuté sans une seule erreur de certificat — dix-huit heures après que `WebFetch` rendait « unable to verify the first certificate » sur cette même machine et ce même domaine. La note déclare « HTTP 200 vérifié » sur chacune, et c'est vrai. ② **Assertion de tableau** : le contrôle d'intégrité du prompt, rejoué verbatim, imprime **`1 tableau(x) — hors note RBPP, assertion de tableau non applicable`**. L'**exemption de chemin** fonctionne exactement comme elle a été bornée hier : la note d'Étape 7 vit dans `has-actualite/`, l'assertion ne s'y applique pas. 🟢 **Et le correctif a un effet de bord dans le bon sens** : cette note porte **un tableau**, là où les **seize** éditions `has-actualite` du dépôt en portaient **zéro** — la ligne `require` importe `Table` depuis hier, et le récapitulatif des quatre appels est devenu un vrai tableau Word.

**Les quatre corrections du 12/10 ont toutes tenu, deux semaines de suite.** ① La phrase-gabarit fausse — *« aucune entrée du secteur datée de la fenêtre »* — est remplacée par un constat sourcé, et le flux le confirme : 50 items, **quatre d'octobre 2026**, le plus récent daté du **12 Oct 2026** et intitulé *« Réponse à la saisine de l'Assurance Maladie : Guide d'accompagnement pharmaceutique des patients… »* — hors secteur —, les trois notes de cadrage du secteur étant datées des **6, 7 et 8 octobre**, hors fenêtre. La fenêtre n'est donc pas vide : elle est vide **pour le secteur**, et c'est précisément ce que la note écrit. ② La date revient dans sa forme corrigée : *« note de cadrage validée 11/03/2025, mise en ligne 19/03/2025 »* — celle que ma fiche du 05/10 avait établie et que le 12/10 avait rejouée. ③ L'attribution des validations à la CSMS a disparu. ④ Le calendrier de la RBPP 3-11 ans porte sa provenance en toutes lettres : *« calendrier établi par l'édition du 28/09/2026, hérité du document téléchargeable de la note de cadrage »*. Quatre sur quatre — et le seul jeton qui revient est celui qui ne devait rien à ces corrections.

**Les dates qui portent tout le document sont littérales sur la source que la note nomme — et je me suis trompé une fois avant de le voir.** La note attribue trois dates de clôture au flux RSS « HAS-Actualité » : **26/10/2026, 02/11/2026 et 13/11/2026 sont ① LITTÉRAL sur ce flux**, en graphie numérique. ⚠️ **MON ERREUR, et c'est celle que le dépôt documente deux fois** : ma première interrogation portait sur « 26 octobre 2026 » et « 13 novembre 2026 », la graphie en mots ; `chercher.py` a rendu **④ ABSENT** sur deux des trois, et j'en ai conclu une attribution fautive — alors que le flux les écrit en chiffres. C'est la règle « chercher la variante de graphie AVANT de conclure à l'absence », que j'avais moi-même rappelée dans la fiche d'hier. Et le degré ④ ne m'a pas sauvé ici : son contexte imprimé était l'en-tête du flux, pas un quasi-appariement. Le cas miroir existe dans le même document : « 8 novembre 2026 » est **① en mots** sur le flux et **④ en chiffres**, et c'est la note qui le convertit en 08/11/2026. 📌 **Pour la série** : une date se cherche dans les **deux** graphies, et un « ABSENT » sur une seule ne vaut rien. Les pages des trois appels portent aussi ces dates, en mots — la note les déclare « contenu non lu », ce qui est prudent et non faux.

**Tout le reste se vérifie à la ligne.** L'appel CVS : la page écrit *« le groupe de travail se réunira dans les locaux de la HAS, 5 avenue du Stade-de-France à Saint-Denis (en Seine-Saint-Denis - 93), le 8 décembre 2026, de 10 h à 17 h environ »*, et la note en rend « 08/12/2026, 10h-17h, HAS, 5 avenue du Stade-de-France, Saint-Denis (93) » — exact, trait d'union compris. *« Semaine 26 oct. – 1er nov. : aucun événement HAS annoncé »* : la page écrit *« Du 26 octobre au 1 novembre Il n'y a pas d'événement prévu pour cette semaine-ci »*. *« Pas de réunion CSMS annoncée dans les prochaines semaines »* : « CSMS » compte **une seule occurrence** sur le calendrier, celle de la réunion du 29/09. Cette page de réunion répond **200 pour 3 711 caractères** et ne porte ni compte-rendu ni document attaché — le *« toujours non publié au 19/10/2026 »* tient. Et « dans 7 jours » tombe juste : du 19 au 26 octobre.

**Le motif ③ a sorti une réserve non bloquante, elle était légitime, et elle se solde favorablement.** Il signale *« Bascule SERAFIN-PH 2027 — aucune publication HAS spécifique cette semaine »* recopiée mot pour mot de l'édition précédente sans mention d'héritage — « une absence vraie la semaine passée peut être fausse celle-ci ». Vérifié : **« SERAFIN » compte zéro occurrence sur les deux flux** aspirés ce jour. L'absence est vraie, et le motif a eu raison de la faire revérifier plutôt que de la laisser passer.

**Le défaut qui reste est structurel : trois ⛔ « Page inaccessible » sans aucune adresse.** Vie quotidienne des enfants 3-11 ans, Habitat volet 3, Prévention spécialisée — portés d'édition en édition, et **aucune URL** ne les accompagne, ni dans ce document ni dans les trois précédents. Ni un contrôle ni un lecteur ne peut les tester : la passe A ne voit pas de page citée, donc elle ne dit rien. ⚠️ **Et cette semaine la question est plus lourde que d'habitude** : entre le 08 et le 18/10, un défaut de certificat a rendu **toutes** les pages HAS injoignables depuis cette machine — un ⛔ hérité est donc indiscernable d'un artefact TLS. La seule adresse voisine que la série listait encore, la note de cadrage des 3-11 ans, répond aujourd'hui **200 pour 9 026 caractères**. La consigne ajoutée hier au prompt — « jamais un ⛔ page inaccessible sans avoir essayé `aspirer.py` » — ne les atteint pas : ce sont des énoncés hérités, pas des tentatives de lecture de l'exécution.

**Mesures du job, et le chiffre qui doit décider quelque chose. 3,7351 $ pour un plafond de 4,00 $ — 93 %**, **72 tours**, 15 min 22 s, 59 056 tokens en sortie, 7 459 888 de cache lu, **une seule tentative**, `exit 0`, prompt à **52 550 octets**. 🔴 **Trajectoire sur cinq semaines : 71 % · 61 % · 60 % · 59 % · 93 %.** Le prompt est passé de **42 556 à 52 550 octets** entre le 12 et le 19/10, dont **4 262 octets de mon durcissement d'hier** ; les tours passent de 47 à 72 et le cache lu est multiplié par 2,4. **C'est exactement le risque que j'avais nommé la veille** — « si lundi dépasse 75 %, c'est cette lecture qu'il faudra resserrer » — et il s'est réalisé d'un coup, à 93 %. Les deux précédents du dépôt disent la suite : `astrologie-karmique` a fait 86 % puis **101 %**, `ai-act` a vu son prompt durci sans que le plafond suive puis **108 %**, et dans les deux cas le job est mort **en pleine vérification**, après avoir écrit un livrable complet qu'aucun contrôle n'a vu. Document de **14 591 octets** pour **7 582 caractères**, 81 paragraphes dont 68 porteurs, 17 liens, **1 tableau**. Contrôles rejoués **verbatim sous `env -i`** : intégrité **OK — 17 liens, 68 paragraphes, marge 51, 1 tableau** ; `controle_decompte` **COHÉRENT** (5 ✅ + 3 ⚠ + 0 ⛔ = 8 annoncés, 8 listés) ; `controle_attributions` **exit 0, 0 bloquant**, une seule réserve B-FR et elle porte sur la phrase-gabarit *« d'après l'édition du JJ/MM/AAAA de cette veille »* de la note méthodologique — un artefact, pas un défaut —, ㊲ ayant écarté le « 200 » comme instrumentation. ⚠️ **Et la passe D est ENTIÈREMENT INERTE sur ce document : zéro valeur chiffrée en contexte d'attribution**, alors que la note est faite de dates. Les quatre dates de clôture, qui sont son contenu même, ne sont examinées par **aucune** passe du dépôt — elles l'ont été à la main, ici.

### Requêtes passées

Neuf pages aspirées sur disque (`aspirer.py`), **aucune n'est entrée en contexte** ; appariement par `chercher.py`, degré ① exigé pour tout ce qui est entre guillemets. Les huit adresses de la note, plus la note de cadrage des 3-11 ans pour éprouver un ⛔ hérité.

| Requête | Verdict |
|---|---|
| `26/10/2026` · `02/11/2026` · `13/11/2026` | **① LITTÉRAL** sur le flux RSS HAS-Actualité — la source que la note nomme |
| `26 octobre 2026` · `13 novembre 2026` | **④** sur le flux, ① sur les pages des appels — **ma première mesure, et elle était trompeuse** |
| `8 novembre 2026` | ① en mots sur le flux et sur la page CVS ; `08/11/2026` → ④ |
| `8 décembre 2026` · `Saint-Denis` | ① page de l'appel CVS, avec l'horaire et l'adresse en clair |
| `CNEDIMTS` · `CTV` · `Commission de la transparence` | ① calendrier détaillé — et `21/10/2026` y est accolé à la troisième |
| `Du 26 octobre au 1 novembre` | la page écrit *« Il n'y a pas d'événement prévu pour cette semaine-ci »* |
| `CSMS` | **1 seule occurrence** sur le calendrier : la réunion du 29/09/2026 |
| `SERAFIN` | **0 occurrence** sur les deux flux — l'absence recopiée est vraie |
| `compte-rendu` · `document` · `ordre du jour` | **0** sur la page de la réunion CSMS du 29/09 (3 711 car.) |
| items du flux « Recommandations et guides » | 50 items · **4 d'octobre** · le plus récent du **12/10**, hors secteur |
| note de cadrage 3-11 ans (`p_4159155`) | **HTTP 200, 9 026 caractères** — lisible aujourd'hui |

**Ce que « standard » n'a pas interrogé, et il faut le dire** : les pages des trois ⛔ hérités n'ont pas pu être testées, faute d'adresse dans le document ; le document téléchargeable de la note de cadrage des 3-11 ans, d'où vient le calendrier 2026-2027, n'a pas été réouvert ; et les trois pages d'appel déclarées « contenu non lu » n'ont été interrogées que sur leurs dates de clôture, pas sur le reste de leur contenu.

## Notes liées

- **⬅️ Précédente** · [[2026-10-12_veille_has-actualite.fiche]]
  **ses quatre corrections tiennent toutes, et le seul jeton qui revient ne doit rien à aucune d'elles.** La phrase-gabarit fausse est remplacée par un constat sourcé et vérifiable, la date du 11/03 a sa forme corrigée, l'inférence CSMS a disparu, et le calendrier des 3-11 ans porte sa provenance. Ce qui revient, c'est « Commission » — dans « Commission de la transparence », un organisme réel, daté au jour près sur une page listée. **La correction du 12/10 était juste, et le contrôle qui la surveille a tort aujourd'hui**
- **🔗 Pont** · [[2026-10-18_veille_imac.fiche]]
  **le même contrôle, deux refus en vingt-quatre heures, un vrai et un faux.** Hier il bloquait « 2031 » et « Microsoft » sur un chiffre que quatre pages Microsoft démentent — refus juste, et le livrable était fautif. Aujourd'hui il bloque un nom commun de la série employé dans un sens sans rapport. **Ce qui sépare les deux cas n'est ni la dénonciation ni la position du jeton : c'est que le vrai rejeu ramène son jeton ACCOMPAGNÉ** — « Microsoft » à 47 caractères de « 2031 » là, rien à moins de 80 ici. Borne posée le 19/10, après trois autres mesurées et abandonnées. C'est aussi de là que vient l'assertion de tableau exemptée ici
- **🔗 Pont** · [[2026-10-05_veille_has-actualite.fiche]]
  **la date qu'elle avait établie tient deux éditions plus tard.** C'est elle qui avait démontré que « mise en ligne le 11/03/2025 » est faux — 11 mars = validation, 19 mars = mise en ligne —, démonstration que le 12/10 avait rejouée mot pour mot et qui avait fait écrire `controle_edition_precedente`. Le 19/10 écrit les deux dates à leur place. **La fiche qui a coûté un contrôle est celle dont la leçon a tenu**
- **🗂️ Dossier** · [[HAS-actualite_dossier.fiche]]
  à mettre à jour sur trois points mesurés : **les huit adresses HAS de la série sont lisibles** par `aspirer.py` et par `curl --cacert`, et **illisibles par `WebFetch`** tant que le serveur n'enverra pas sa chaîne intermédiaire ; le **flux RSS HAS-Actualité écrit ses dates de clôture en graphie numérique** (26/10/2026) et les pages d'appel en mots (26 octobre 2026) — une recherche de date doit essayer les deux ; et **trois items hérités portent un ⛔ sans adresse** depuis des semaines, à ré-ancrer sur des URL avant d'être reconduits une fois de plus
