---
type: fiche-document
source: 2026-10-04_lecon-revenus-passifs_11_structures-juridiques-fiscales-france.docx
date_creation: 2026-10-04
date_lecon: 2026-10-04
parcours: revenus-passifs
numero: 11
statut: parcours-clos
tags:
  - parcours/revenus-passifs
  - registre/perso
  - module/statuts-juridiques
  - concept/micro-entreprise
  - concept/sasu-eurl
  - concept/pfu-2026
  - concept/franchise-tva
  - source/service-public
  - source/urssaf
  - source/impots-gouv
  - source/amf
  - source/bpifrance
  - theme/lecon-hors-feuille-de-route
  - theme/parcours-sans-clause-de-fermeture
  - theme/contradiction-interne
  - theme/chiffre-prete-a-une-page-qui-ne-le-porte-pas
  - theme/pdf-non-lu-par-le-controle
  - theme/comparaison-a-perimetres-inegaux
  - theme/passe-D-aveugle-aux-separateurs
  - alerte/a-corriger
  - incident/11e-lecon-d-un-parcours-de-10
---

# 2026-10-04_lecon-revenus-passifs_11_structures-juridiques-fiscales-france

Document source : [[2026-10-04_lecon-revenus-passifs_11_structures-juridiques-fiscales-france.docx]]

## Résumé

**C'est la onzième leçon d'un parcours de dix, et la leçon le dit elle-même en en-tête.** Elle s'intitule *« Leçon 11 / 10+ — Approfondissement »* et précise sous le titre : *« Les 10 leçons du parcours initial sont couvertes. Cette leçon approfondit la dimension juridique et fiscale, transversale à tous les modèles. »* Le récapitulatif du job va plus loin : *« Position : Approfondissement — parcours de 10 leçons complété, **leçon hors feuille de route initiale** »*. Le job a donc correctement diagnostiqué que la feuille de route était épuisée, puis a produit une leçon quand même, et en a annoncé une douzième. ⚠️ **La cause est dans le prompt, et elle est mécanique.** Il déclare le parcours en 10 leçons à deux endroits — *« un PARCOURS D'APPRENTISSAGE PROGRESSIF en 10 LEÇONS »* et *« FEUILLE DE ROUTE — Parcours Revenus passifs (10 leçons) »*, dont les dix items sont tous traités — mais sa règle de numérotation est *« Le numéro (NN) = nombre de fichiers existants + 1 »*, **sans limite**. Dix fichiers en place, NN = 11 : l'issue était déterminée. Et `PARCOURS FERMÉ` compte **zéro occurrence** dans ce prompt.

**Le garde-fou existe dans le dépôt, et il manque exactement aux trois parcours qui en ont besoin.** Relevé ce jour sur les neuf jobs de leçon :

| parcours | annoncé | fichiers | clause ⛔ PARCOURS FERMÉ | limite sur NN |
|---|---|---|---|---|
| enneagramme · dzogchen · psychopathologie · placement-financier · hypnose · stoicisme | 20 | 16 à 18 | **OUI** | **OUI** |
| astrologie-karmique | 12 | 9 | **NON** | **NON** |
| **revenus-passifs** | **10** | **11** ⚠️ | **NON** | **NON** |
| **appli-ia** | **12** | **12** ⚠️ | **NON** | **NON** |

Les six parcours de vingt leçons portent tous la clause (*« ⛔ PARCOURS FERMÉ — 20 LEÇONS. Ce parcours compte exactement 20 leçons, pas une de plus. Avant de rédiger, compte les fichiers existants : s'il y en a déjà 20, NE PRODUIS RIEN »*) et **aucun n'est près de sa limite**. Les trois parcours courts, dont la limite est atteignable, sont les trois sans clause : un l'a franchie (**revenus-passifs, 11/10**), un est exactement dessus (**appli-ia, 12/12** — son créneau du vendredi produirait une treizième leçon), un en est à trois leçons (**astrologie, 9/12**). Le garde-fou a été écrit pour les parcours qui n'en avaient pas encore l'usage.

**Sur le fond, c'est une leçon solide : tous les taux sont littéraux sur les pages officielles, et les vingt-trois calculs sont justes.** Les sept sources ont été rouvertes le 04/10/2026, toutes en **200**. Les plafonds de la micro-entreprise sont littéraux à deux endroits : l'URSSAF écrit *« **203.100 €** pour une activité de vente de marchandises … **83.600 €** pour les prestations de services relevant de la catégorie des bénéfices industriels et commerciaux (BIC) »*, et service-public les porte aussi. **Les cinq taux de cotisations** (12,3 · 21,2 · 25,6 · 23,2 · 6 %) et **les trois taux de versement libératoire** (1 · 1,7 · 2,2 %) sont sur la page URSSAF, chacun avec son champ d'activité exact, y compris la mention *« y compris les locations meublées de toutes natures et les chambres d'hôte »*. **L'IS est complet et juste** : 25 %, 15 % jusqu'à **42 500 €**, CA ≤ **10 000 000 €**, capital entièrement libéré et détenu à ≥ **75 %** par des personnes physiques — les quatre éléments sur service-public F23575. Les seuils de TVA (**85 000 / 93 500 / 37 500 / 41 250**) et la mention *« TVA non applicable - article 293 B du CGI »* sont sur la page URSSAF. Le *« environ 60 % de la rémunération brute »* en SASU est littéral chez BpiFrance, **avec sa clause** : *« Si aucune rémunération n'est versée, aucune cotisation sociale n'est due. »* Et **vingt-trois opérations arithmétiques sur vingt-trois sont exactes**, y compris l'IS à deux tranches (6 375 + 625 = 7 000 €), le PFU (30 000 × 31,4 % = 9 420 €) et les ratios (20 580 / 55 000 = 37,4 %). Les **cinq tests mécaniques du prompt, rejoués verbatim sous `env -i`, sortent tous en OK**, et `controle_attributions` rend **0 bloquant**.

**Le passage le plus difficile de la leçon est aussi le mieux traité : le PFU 2026.** La note annonce *« 12,8 % au titre de l'impôt sur le revenu + **18,6 %** au titre des prélèvements sociaux (taux applicable aux dividendes depuis le 01/01/2026) = **31,4 %** »*, et ajoute que ce 18,6 % *« ne concerne pas les produits d'assurance-vie et de capitalisation ni certains PEL/CEL antérieurs à 2018, qui restent à 17,2 % »*. impots.gouv.fr écrit : *« A compter du 1er janvier 2026, le taux des prélèvements sociaux passent à 18,6 % sauf pour les produits suivants qui restent soumis au taux de 17,2 % : les produits attachés aux bons et contrats de capitalisation et aux contrats d'assurance-vie …, les intérêts et primes d'épargne des comptes épargne logement (CEL) ouverts jusqu'au 31 décembre 2017, les intérêts des plan d'épargne logement (PEL) ouverts jusqu'au 31 décembre 2017 … »*, et ailleurs *« les revenus de capitaux mobiliers sont soumis, sauf exceptions, au PFU de 12,8 % »*. **Le taux, la date d'effet et la liste d'exceptions sont reproduits fidèlement** — « antérieurs à 2018 » valant « ouverts jusqu'au 31 décembre 2017 ». Le **31,4 %** ne figure sur aucune page : c'est la somme des deux composantes sourcées, et elle est juste. Sur un taux qui vient de changer et dont le périmètre d'exception est piégeux, c'est le geste exact.

**Mais la seule donnée chiffrée de l'« Ancrage réaliste » n'est pas dans la source qu'elle nomme — et c'est la section dont c'est tout l'objet.** La leçon écrit : *« L'AMF a reçu **près d'une centaine de signalements** concernant des **MLM** et formations pyramidales promettant des **revenus passifs** et de l'**argent facile** via les réseaux sociaux. (Source : AMF France — Quelles sont les arnaques les plus courantes ?) »*. J'ai téléchargé ce PDF et l'ai extrait avec `pdfminer` — **8 pages, 17 931 caractères**. Comptages : *« centaine »* **0** · *« signalement »* **0** · *« MLM »* **0** · *« revenus passifs »* **0** · *« argent facile »* **0**. Seuls *« pyramidal »* (5) et *« réseaux sociaux »* (4) y sont. ⚠️ **Et le PDF ne porte aucune statistique du tout** : ses seuls nombres sont des dates, un numéro de téléphone et un code postal. Le fond est juste — le document dit bien *« Ces formations peuvent en réalité … s'apparenter à des systèmes pyramidaux frauduleux dont l'objectif est de vous faire recruter de nouvelles personnes dans votre entourage »* et *« Gare aux systèmes pyramidaux qui se diffusent grâce au bouche-à-oreille »* — mais **le chiffre et trois des quatre libellés sont ajoutés**. C'est la forme que je poursuis depuis une semaine : un énoncé vrai au fond, sous une ligne de source qui ne le soutient pas.

**Et le contrôle l'avait annoncé, en toutes lettres, dans une réserve que le récapitulatif du job n'a pas reprise.** Le relevé de `controle_attributions` porte : *« **RESSOURCES NON ANALYSABLES (PDF) : 1** … Aucune citation ne peut etre confirmee sur ces pages par ce test »*. Le contrôle **ne lit pas les PDF** — il le déclare honnêtement — et le seul énoncé non sourcé de la leçon est précisément celui qui est attribué à un PDF. Le récapitulatif du job, lui, a écrit *« controle_attributions.py ✅ (0 bloquant) »* **sans la réserve** : troisième fois cette semaine qu'un récapitulatif conserve le verdict et jette ce qui l'entoure. ⚠️ **Le correctif est à portée de main** : `pdfminer` est installé sur la machine, c'est lui qui m'a servi à lire les huit pages en une commande.

**La leçon se contredit sur sa propre mesure, et le test chargé de ça n'a rien mesuré.** Le corps écrit *« (Mesure E5 : la partie pratique fait **51 %** du document entre les repères de section) »* ; la note méthodologique finale écrit *« La partie pratique (Exercice 1 à Challenge) représente environ **70 %** du contenu entre les repères de section »*. Les deux parlent de la même grandeur, délimitée de la même façon. Mesuré avec **le code du test lui-même**, son échappatoire neutralisée : théorie + ancrage 7 383 signes, pratique 7 854 signes → **52 %**. Le corps est juste à un point près ; la note se trompe de **dix-huit**. ⚠️ **Et voici pourquoi rien n'a bronché** : le test E5 commence par `if re.search(r"(?:partie pratique|pratique)[^.]{0,40}?fait\s+\d{1,3}\s*%…")`, imprime *« la leçon déclare elle-même sa répartition mesurée — acquitté »* et sort en **0**, **sans jamais compter**. L'échappatoire a été écrite pour permettre à une leçon de déclarer sa vraie part au lieu de mentir avec une étiquette — elle accepte **n'importe quelle** déclaration. Le premier chiffre a acquitté le document, le second n'a jamais été lu, et le plancher de 65 % que le test défend n'est pas atteint (52 %).

**Trois défauts de raisonnement, tous dans la partie pratique, aucun arithmétique.** ① **Le versement libératoire est appliqué à un profil qui n'y a probablement pas droit.** Le Challenge donne à Carla *« une TMI IR de **30 %** (tranche de son foyer fiscal principal) »*, puis le corrigé lui applique le versement libératoire à 2,2 %. Or la page URSSAF citée porte, dans un encadré « Bon à savoir » : *« Pour bénéficier du versement libératoire de l'impôt sur le revenu en année N, votre **revenu fiscal de référence N-2** … ne doit pas excéder certains seuils calculés en fonction de votre quotient familial »*. Un foyer imposé à 30 % dépasse très probablement ce plafond. La condition est sur la page citée, dans un bloc mis en évidence, et elle fonde **deux des trois exercices chiffrés** de la leçon. ② **La comparaison finale déduit les charges d'un seul côté.** Le corrigé oppose « micro **15 162 €** net » à « SASU **10 612 €** net » et conclut *« nettement plus avantageuse »*. Mais B1 retire les 2 800 € de charges réelles du côté SASU (21 000 − 2 800) quand A3 ne les retire pas du côté micro (21 000 − 5 376 − 462) — alors que Carla les paie dans les deux cas. À périmètre comparable : **12 362 € contre 10 612 €**, soit **+1 750 €** et non +4 550 €. **L'écart annoncé vaut 2,6 fois l'écart réel**, et la leçon discute ces mêmes 2 800 € en A4 sans voir qu'ils manquent d'un côté de sa propre comparaison. ③ **Un décalage d'un mois.** Le seuil majoré de TVA (41 250 €) à 3 200 €/mois tombe à **12,89 mois** : après les 38 400 € de la première année, il reste 2 850 € à faire, soit 0,89 mois → **pendant le premier mois** de l'année suivante. Le corrigé écrit *« au cours du **deuxième** mois de l'année suivante »*. Le nombre affiché (12,9) est juste, sa lecture ne l'est pas. Accessoirement, la réponse D du même exercice annonce « deux conséquences » et en livre une et demie, avec une phrase cassée : *« ses prix hors taxe deviennent hors taxe »*.

**Mesures, et la passe D pour la troisième fois de la semaine. 2,9863 $ pour un plafond de 3,00 $ — exactement 100 % du plafond**, **82 tours**, 13 min 51 s, 48 470 tokens en sortie, 5 687 449 de cache lu, une seule tentative, `exit 0`, prompt à **60 695 octets**. Document de **19 688 octets** pour 18 811 caractères. **C'est le run le plus long et le plus cher du parcours — pour une leçon hors feuille de route.** `controle_attributions` : **0 bloquant**, une seule valeur en passe D — *« 37 500 absente des pages citées »* — et elle est **fausse** : le seuil est sur service-public F23575. Avec le correctif d'un caractère mesuré le 03/10 : **1 alerte → 0**. Troisième document consécutif où l'unique signal de la passe D est un faux positif de séparateur de milliers. Ce qui est honnête dans cette leçon et mérite d'être noté : elle **déclare** ses trous dans une note méthodologique finale — dividendes en EURL non lus à une source primaire, seuils de TVA 2026 non vérifiés (elle donne ceux de 2025 en le disant), approximation des 60 % en SASU, et grille du Challenge construite pour l'illustration. Chaque cas fictif nomme son invention. Le cadre déontologique est explicite, répété, et renvoie au statut CIF et au registre ORIAS.

## Notes liées

- **⬅️ Précédente** · [[2026-09-27_lecon-revenus-passifs_10_esperance-de-vie-modeles]]
  **la dixième et dernière du parcours tel qu'il était commandé** — et c'est son audit, le 27/09, qui a mesuré que la règle 20/80 n'avait jamais été tenue sur dix leçons (34 % à 57 % de pratique) et fait écrire le test E5. Une semaine plus tard, le test existe, la leçon déclare sa part, et **c'est la déclaration qui n'est pas vérifiée** : 51 % dans le corps, 70 % dans la note, 52 % à la mesure
- **🔗 Pont** · [[2026-10-03_lecon-placement-financier_17_arnaques-produits-toxiques-signaux-alerte]]
  **le même sujet, la même source, le même défaut.** Là-bas cinq des dix signaux d'alerte n'avaient aucune base sur les pages AMF ouvertes ; ici le seul chiffre de l'ancrage réaliste n'est pas dans le PDF AMF cité. Et dans les deux cas **le récapitulatif du job a rapporté « 0 bloquant » en laissant tomber la réserve du contrôle** — dix citations « A RELIRE » d'un côté, « RESSOURCES NON ANALYSABLES (PDF) » de l'autre
- **🔗 Pont** · [[2026-10-04_veille_imac.fiche]]
  **le même matin, l'autre job du dimanche, et deux constats qui se répètent** : un chiffre repris du cadrage du job sans ligne de provenance (le 1 049 € du Mac mini M6 là-bas, le « près d'une centaine » ici), et la passe D dont l'unique ou la majorité des alertes sont des faux positifs de séparateur. Troisième document de la semaine pour ce correctif d'un caractère, toujours pas appliqué
- **🔗 Pont** · [[2026-09-26_lecon-placement-financier_16_transmission-succession-demembrement]]
  **un document qui se contredit lui-même, déjà.** Là-bas le barème progressif était démontré dans l'exercice 1 et nié dans l'exemple de théorie trente lignes plus haut ; ici la part de pratique vaut 51 % au milieu du document et 70 % à la fin. Dans les deux cas le document porte son propre correctif sans le voir — et dans les deux cas il a fallu mesurer, pas relire
