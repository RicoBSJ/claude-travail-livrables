---
type: fiche-document
source: 2026-10-26_veille_has-actualite.docx
date_creation: 2026-10-26
date_veille: 2026-10-26
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
  - theme/attribution-perdue-sans-erreur-de-fait
  - theme/marqueur-de-provenance-retire
  - theme/document-qui-enfreint-sa-propre-convention
  - theme/contradiction-resolue-par-la-taille-de-la-page
  - theme/graphie-numerique-contre-graphie-en-mots
  - theme/passe-D-inerte-sur-un-document-de-dates
  - theme/absence-recopiee-revalidee
  - theme/inaccessibilite-heritee-sans-adresse
  - theme/plafond-retombe-a-42-pour-cent
  - alerte/attribution-non-sourcee
---

# 2026-10-26_veille_has-actualite.fiche

Document source : [[2026-10-26_veille_has-actualite.docx]]

## Résumé

**Le seul défaut de cette note n'est pas une erreur de fait : c'est une attribution perdue, et l'édition précédente faisait mieux.** La note écrit deux fois *« Note de cadrage validée 29/09/2026, mise en ligne 08/10/2026 »* (SAAD Familles) et *« … mise en ligne 07/10/2026 »* (Surdicécité), en ne citant que les pages d'appel à candidatures. Mesuré : sur ces deux pages, `08/10/2026` et `07/10/2026` sont **① LITTÉRAL** — la page SAAD écrit mot pour mot *« Clôture de l'appel le 02/11/2026 Appel à candidature - Mis en ligne le 08 oct. 2026 »* —, mais **`29/09/2026` est ④ ABSENT dans les deux graphies**, et l'unique occurrence de « validation » sur la page SAAD désigne la **future** validation des recommandations par la CSMS, pas une date de validation de la note de cadrage. 🟢 **Le fait reste vrai, et je l'ai vérifié à sa source** : la note de cadrage SAAD (`p_4559627`, non citée par cette édition, 200 pour 6 709 caractères) porte **`Date de validation : 29 septembre 2026` en ① LITTÉRAL**. 🔴 **Ce qui a été perdu est le marqueur de provenance.** L'édition du 12/10 avait établi le fait en lisant les notes de cadrage — *« toutes portant la mention "Date de validation : 29 septembre 2026" »* — après une correction qui avait justement retiré l'attribution à la CSMS ; celle du 19/10 écrivait *« validée 29/09/2026, mise en ligne 08/10/2026 **(d'après l'édition du 12/10/2026 de cette veille)** »*. Le 26/10 a laissé tomber la parenthèse. ⚠️ **Et le document enfreint ainsi sa propre convention**, qu'il énonce en toutes lettres — *« les informations héritées des éditions précédentes sont identifiées par la mention "d'après l'édition du JJ/MM/AAAA de cette veille" »* — et qu'il applique correctement à Autodétermination et à Pair-aidance, deux lignes plus bas. Le défaut est donc **interne et vérifiable sans réseau** : deux énoncés sur six portent le marqueur, deux ne le portent pas, et rien ne distingue les deux cas.

**Aucun contrôle du dépôt ne peut voir cette classe, et c'est mesuré ce jour, pas supposé.** La passe D de `controle_attributions.py` est **entièrement inerte sur ce document — 0 valeur chiffrée en contexte d'attribution** —, exactement comme la fiche du 19/10 l'avait déjà relevé : une note faite de dates échappe à la seule passe qui vérifie les valeurs chiffrées attribuées. Le motif ③ de `controle_edition_precedente.py`, lui, voit les **phrases d'absence** recopiées sans mention d'héritage, et il en signale deux — mais une date héritée n'est pas une phrase d'absence, donc il passe à côté. ㊲ a écarté le « 200 » comme instrumentation, à juste titre. **Le trou est structurel : le dépôt sait vérifier qu'un fait est sur une page, il ne sait pas vérifier qu'un fait est attribué à la page qui le porte.**

**La contradiction apparente entre deux éditions se résout par la taille de la page, et les deux avaient raison.** L'édition du 19/10 écrivait *« Semaine 26 oct. – 1er nov. : aucun événement HAS annoncé »* ; celle du 26/10 écrit *« Semaine 26 oct. – 1er nov. : Journées de sensibilisation au CRM Santé (21/10/2026 – 31/03/2027, hors secteur ESSMS stricto sensu) »*. Même semaine, même page. Mesure décisive : le calendrier détaillé est passé de **9 506 caractères utiles le 19/10 à 12 402 le 26/10, soit +2 896**, pendant que **cinq des huit autres pages rendent un compte de caractères identique à l'unité** (flux Recommandations 47 698, réunion CSMS 3 711, GT Mineurs 14 107, SAAD 13 737, CVS 11 437). Le calendrier a été alimenté dans l'intervalle, et il porte aujourd'hui littéralement *« Du 26 octobre au 1 novembre 21/10/2026 - 31/03/2027 Journées de sensibilisation au CRM Santé icone hours 10h - 17h »*. `CRM Santé`, `31/03/2027` et `21/10/2026` sont tous trois **① LITTÉRAL**. **Ce n'est donc pas une édition qui se trompe : c'est une page qui a changé, et la fiche du 19/10 reste exacte à sa date.**

**Le « 🟢 calme » du bandeau est mesuré, pas affirmé.** Le flux « Recommandations et guides » porte **0 entrée depuis le 19/10/2026 sur ses 50 items** — la note écrit « aucune nouvelle RBPP publiée … entre le 19 et le 26 octobre 2026 », et c'est exact. Le flux HAS-Actualité porte **exactement une entrée** dans la fenêtre : `21/10/2026 · Chef de projet SI évaluation des ESSMS - Service évaluation (H/F) CDI`. La note écrit « 1 publication HAS dans la fenêtre, hors RBPP : offre d'emploi "Chef de projet SI évaluation des ESSMS" (21/10/2026) » — titre tronqué au bon endroit, date juste, et le libellé est **① LITTÉRAL** sur le flux. Le compte de trois appels actifs se recompte à la main : SAAD 02/11, CVS 08/11, Surdicécité 13/11, le GT Mineurs clôturant le jour même.

**Tout le reste se vérifie à la ligne, et la leçon de graphie du 19/10 a été appliquée d'emblée.** Les quatre dates de clôture sont littérales sur les pages que la note nomme : `26/10/2026` **et** `26 octobre 2026` tous deux ① sur la page du GT Mineurs ; `02/11/2026` et `2 novembre 2026` tous deux ① sur SAAD ; `13/11/2026` et `13 novembre 2026` tous deux ① sur Surdicécité. ⚠️ **Le cas miroir est de retour sur la page CVS, et c'est pourquoi il fallait chercher les deux graphies** : `08/11/2026` et `08/12/2026` sont **④ ABSENT** en chiffres, tandis que `8 novembre 2026` et `8 décembre 2026` sont **① LITTÉRAL** en mots — la note convertit, ce qu'elle a le droit de faire. `Saint-Denis` est ① sur la même page. **Conclure de la seule graphie numérique aurait produit deux fausses accusations**, ce qui est exactement l'erreur que la fiche du 19/10 avait payée.

**L'absence de compte-rendu CSMS est établie par un argument de contraste, pas par un simple « je n'ai rien trouvé ».** La page de la réunion du 29/09/2026 répond 200 pour 3 711 caractères et ne porte que ses métadonnées d'événement — *« 29/09/2026 CSMS - Réunion du mardi 29 septembre 2026 … Evénement de Calendrier - Mis en ligne le 04 févr. 2026 … 09h30 - 17h »*. `ordre du jour` et `Télécharger` y sont **④ ABSENT**. Or le calendrier montre que d'autres entrées de la même nature **portent un bloc « Documents »** (`Documents ODJ CD 01 10 2026`, `Documents ORDRE DU JOUR CT 21 10 2026`) : l'absence sur la page CSMS est donc **significative**, et le « toujours non publié au 26/10/2026 » tient. Et `CSMS` compte **2 occurrences sur le calendrier, les deux pour cette même réunion passée** — le calendrier rend sa liste deux fois, ce qui explique l'écart avec la seule occurrence relevée le 19/10 ; dans les deux cas, **aucune réunion CSMS à venir**, donc la phrase de la note est juste.

**Les deux absences recopiées que le contrôle signale sont vraies, et les revérifier était justifié.** Le motif ③ relève *« Bascule SERAFIN-PH 2027 — aucune publication HAS spécifique cette semaine »* et *« Pas de réunion CSMS dans les prochaines semaines »*, recopiées mot pour mot sans mention d'héritage. Vérifié : **`SERAFIN` et `SERAFIN-PH` comptent 0 occurrence** sur les deux flux et sur le calendrier, et la question CSMS est tranchée ci-dessus. Les deux absences sont exactes — mais le motif a eu raison de les faire revérifier plutôt que de les laisser passer, puisque c'est précisément la classe de phrase qui se périme en silence.

**Le défaut structurel des trois ⛔ sans adresse en est à sa cinquième édition.** Vie quotidienne des enfants 3-11 ans, Habitat volet 3, Prévention spécialisée : portés d'édition en édition avec la mention *« ⛔ Page inaccessible »* et **aucune URL**. Ni un contrôle ni un lecteur ne peut les tester, la passe A ne voyant pas de page citée. La fiche du 19/10 l'avait signalé, celle du 12/10 avant elle ; rien n'a bougé. ⚠️ Et la consigne du prompt — « jamais un ⛔ page inaccessible sans avoir essayé `aspirer.py` » — ne les atteint toujours pas : ce sont des énoncés hérités, pas des tentatives de lecture de l'exécution courante.

**Mesures du job, et le chiffre qui dédramatise la semaine passée. 2,0892 $ pour un plafond de 5,00 $ — 42 %**, **49 tours**, 8 min 09 s, 27 861 tokens en sortie, 3 932 925 de cache lu, **une seule tentative**, `exit 0`, prompt à **56 313 octets**. 🟢 **Trajectoire sur six semaines : 71 · 61 · 60 · 59 · 93 · 42 %.** Les 93 % du 19/10 avaient fait relever le plafond de 4 à 5 $ ; cette semaine le coût **absolu** baisse aussi — 3,7351 $ → 2,0892 $ — et les tours passent de 72 à 49. ⚠️ **Il faut dire ce que cette mesure ne prouve pas** : les six créneaux ont tous pris l'**Étape 7**, le chemin le moins cher, et la dernière note RBPP complète date du 09/07/2026. Le 42 % ne dit rien du chemin qui ajoute PDF, note Word, quiz de 100 questions et infographie. Document de **13 808 octets** pour **6 653 caractères**, 8 adresses, 15 liens, **1 tableau** (les trois appels actifs), 0 ⛔ de source. Contrôles rejoués **verbatim sous `env -i`** : `controle_decompte` **COHÉRENT** (5 ✅ + 3 ⚠ + 0 ⛔ = 8 annoncés, 8 listés) ; `controle_attributions` **exit 0, 0 bloquant**, une seule réserve B-FR et elle porte sur la phrase-gabarit *« d'après l'édition du JJ/MM/AAAA de cette veille »* de la note méthodologique — artefact déjà connu du 19/10 ; `controle_edition_precedente` **exit 0**, aucune correction de N-1 rejouée, deux ③ non bloquants tous deux revérifiés vrais ; `controle_livrable_du_job` **accepte**, avec le décompte des liens relevé — **8 testés · 8 retenus · 0 écarté, aucun rejet, tous HTTP 200** —, ce qui confirme au passage que la table `has-actualite → rbpp-pipeline` corrigée le 20/10 fonctionne.

### Requêtes passées

Neuf pages aspirées sur disque (`aspirer.py`), **aucune n'est entrée en contexte** ; appariement par `chercher.py`, degré ① exigé pour tout ce qui est entre guillemets, chaque date interrogée dans ses **deux graphies**. Les huit adresses de la note, plus la note de cadrage SAAD pour éprouver l'attribution du `29/09/2026`.

| Requête | Verdict |
|---|---|
| `26/10/2026` · `26 octobre 2026` | **① LITTÉRAL** tous deux — page du GT Mineurs prostitution |
| `02/11/2026` · `2 novembre 2026` · `08/10/2026` | **①** tous trois — page SAAD Familles |
| `29/09/2026` · `29 septembre 2026` | **④ ABSENT** sur SAAD **et** sur Surdicécité — **le défaut de la note** |
| `Date de validation` · `29 septembre 2026` | **① LITTÉRAL** sur la **note de cadrage** `p_4559627` — le fait est vrai, la source n'est pas citée |
| `validation` (page SAAD) | **1 seule occurrence**, et elle porte sur la *future* validation par la CSMS |
| `13/11/2026` · `13 novembre 2026` · `07/10/2026` | **①** tous trois — page Surdicécité |
| `08/11/2026` · `08/12/2026` | **④ ABSENT** en chiffres — le cas miroir |
| `8 novembre 2026` · `8 décembre 2026` · `Saint-Denis` | **① LITTÉRAL** en mots — page CVS |
| items du flux « Recommandations et guides » depuis le 19/10 | **0 entrée sur 50** — « aucune nouvelle RBPP » est exact |
| items du flux HAS-Actualité depuis le 19/10 | **1 entrée** : `21/10/2026 · Chef de projet SI évaluation des ESSMS` |
| `CRM Santé` · `31/03/2027` · `21/10/2026` | **①** calendrier — sous la semaine « Du 26 octobre au 1 novembre » |
| `CSMS` (calendrier) | **2 occurrences, les deux pour la réunion passée du 29/09** |
| `ordre du jour` · `Télécharger` (page CSMS) | **④ ABSENT** — et les autres entrées du calendrier ont un bloc « Documents » |
| `SERAFIN` · `SERAFIN-PH` | **0 occurrence** sur les deux flux et le calendrier — l'absence recopiée est vraie |
| taille des 9 pages | 47 698 · 45 832 · **12 402** · 3 711 · 14 107 · 13 737 · 11 437 · 14 792 · 6 709 car. utiles, **8/8 à HTTP 200** |

**Ce que « standard » n'a pas interrogé, et il faut le dire** : la note de cadrage **Surdicécité** n'a pas été aspirée — seule celle de SAAD l'a été, et la conclusion sur le `29/09/2026` de Surdicécité est donc une **inférence par symétrie**, pas une mesure ; les trois ⛔ hérités n'ont pas pu être testés, faute d'adresse dans le document ; les six RBPP « en cours d'élaboration » n'ont été vérifiées sur aucune page, la note les donnant toutes pour héritées ; et le contenu des trois pages d'appel au-delà de leurs dates de clôture et de mise en ligne n'a pas été relu, ce que la note déclare elle-même en les marquant « contenu non relu ».

## Notes liées

- **⬅️ Précédente** · [[2026-10-19_veille_has-actualite.fiche]]
  **elle faisait mieux sur le point exact où celle-ci faiblit.** Le 19/10 écrivait « validée 29/09/2026 … **(d'après l'édition du 12/10/2026 de cette veille)** » ; le 26/10 a laissé tomber la parenthèse et ne cite qu'une page qui ne porte pas la date. Et sa leçon de graphie a servi dès la première requête : sans elle, `08/11/2026` et `08/12/2026` en ④ auraient produit **deux fausses accusations** sur la page CVS. C'est aussi elle qui avait relevé que **la passe D est inerte sur ce document** — c'est encore vrai, et c'est pourquoi le défaut du jour n'est vu par aucun contrôle
- **🔗 Pont** · [[2026-10-12_veille_has-actualite.fiche]]
  **c'est son travail qui est aujourd'hui mal attribué, pas démenti.** Le 12/10 avait retiré l'attribution des validations à la CSMS et établi, pages en main, que les notes de cadrage portent « Date de validation : 29 septembre 2026 ». La vérification du jour le confirme en **① LITTÉRAL** sur `p_4559627`. **Le fait qu'elle a établi survit ; c'est le chemin qui y mène qui a disparu du document** — et c'est une régression plus discrète qu'une erreur, donc plus durable
- **🔗 Pont** · [[2026-10-21_veille_SERAFIN-PH.fiche]]
  **les huit adresses HAS de cette série répondent 200, et le même jour celles de la CNSA sont tombées.** Le balayage du 26/10 classe **5 adresses `cnsa.fr` en défaut TLS** (`exit 60`, 3/3 essais, avec **et** sans notre faisceau), dans **38 documents** de la série SERAFIN-PH. Le serveur ne présente que son certificat feuille — émetteur `Sectigo Qualified Website Authentication CA R39`, absent du faisceau —, verdict `21 unable to verify the first certificate`. **C'est le mécanisme de `has-sante.fr` au 18/10**, et il concerne la source principale d'une veille dont le créneau tombe le mercredi
- **🗂️ Dossier** · [[HAS-actualite_dossier.fiche]]
  à mettre à jour sur trois points mesurés : **le calendrier détaillé HAS est une page VOLATILE** — 9 506 → 12 402 caractères en sept jours — donc une absence d'événement n'y vaut qu'à sa date, et deux éditions peuvent se contredire en ayant toutes deux raison ; **la convention « d'après l'édition du JJ/MM/AAAA » n'est appliquée qu'à une partie des énoncés hérités**, deux sur six dans cette édition, et aucun contrôle ne la fait respecter ; et **les trois ⛔ sans adresse en sont à leur cinquième reconduction** — à ré-ancrer sur des URL avant d'être reconduits une sixième fois
