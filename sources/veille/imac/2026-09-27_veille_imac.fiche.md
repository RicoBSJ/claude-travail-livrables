---
type: fiche-document
source: 2026-09-27_veille_imac.docx
date_creation: 2026-09-27
date_veille: 2026-09-27
veille: imac
statut: veille-active
tags:
  - veille/imac
  - registre/perso
  - concept/comparateur-prix
  - concept/reconditionne-apple
  - concept/tout-en-un-windows
  - concept/calendrier-m6
  - source/consomac
  - source/apple
  - source/macrumors
  - source/iphonote
  - source/appsystem
  - source/ldlc
  - theme/fiche-ecrite-quarante-jours-apres
  - theme/convention-d-heritage-appliquee-a-un-chiffre-sur-deux
  - theme/fait-attribue-a-une-page-declaree-sans-element
  - theme/trente-huitieme-muet-log-purge-a-trente-jours
  - theme/mur-anti-automate-reel-les-deux-agents
  - theme/page-dix-fois-au-dessus-du-plancher-et-inutilisable
  - theme/faux-positif-du-controle-des-noms-propres
  - theme/page-vivante-non-verifiable-retrospectivement
---

# 2026-09-27_veille_imac

Document source : [[2026-09-27_veille_imac.docx]]

## Résumé

**Cette fiche est écrite quarante jours après la note, et ce retard est lui-même le premier fait à consigner.** Le squelette de 294 octets a été posé par le job le 27/09 à 08:15, deux minutes après le `.docx`, et n'a jamais été ni complété ni commité — il est resté **non suivi par git** jusqu'à aujourd'hui. La fiche du 04/10 l'avait pourtant nommé, dès la semaine suivante : *« fiche jamais écrite — stub de 294 octets posé le 27/09 et resté tel quel »*. Sept jours plus tard la fiche du 11/10 relisait la 04/10, et ainsi de suite : **la chaîne ⬅️/➡️ a continué de se construire par-dessus un trou**, et aucun contrôle ne pouvait le dire — `audit_vault.py` compte les squelettes mais ne les date pas, et son seul détecteur est l'étiquette de classement que le job pose dans le frontmatter — une chaîne que cette fiche se garde de reproduire, parce que la citer la ferait compter elle-même parmi les squelettes (mesuré : `○ Fiches restant à renseigner — 1`, au premier essai).

**Les faits de la note sont justes, et les deux attributions du calendrier M6 sont exactes au caractère.** Les dix-huit requêtes passées sur les quatre pages lisibles rendent **① LITTÉRAL sans une absence** : la citation de Gurman via iphonote — *« au cours des derniers mois de 2026 »* — est littérale, sa date du **23 août 2026** est littérale sur la page, et les deux références internes **J833** et **J834** sont littérales chez appsystem *et* chez consomac. Les dix contrôles arithmétiques tombent juste : +240 € de remise disparue (2 439 − 2 199), −170 € du reconditionné (1 689 − 1 519), −280 € et −310 € contre l'Apple Store, −6 % et −5 % d'écart marché, et les quatre comparaisons Mac/Windows au centime (+11 €, 211 €, 199 €, −1 €). `controle_decompte.py` rend **COHÉRENT** sur 7 ✅ · 2 ⚠ · 4 ⛔ · 13 tentées, et le décompte du reconditionné — *« 11 lignes vs 13 le 20/09 »* — se vérifie sur l'édition N-1, qui écrit bien **« 13 iMac M4 reconditionnés listés »**.

**La convention d'héritage est appliquée à un chiffre et pas à son voisin, dans la même phrase.** Le paragraphe d'impact écrit *« le Mac mini M4 au tarif courant (949 € depuis juin 2026, **selon la veille du 20/09/2026 — non re-vérifié aujourd'hui**) »* — la convention dans sa forme exacte — et, trois mots avant, *« le Mac mini M6 (1 049 €) »* **sans aucune réserve**. La passe D le voit et le dit : `A VERIFIER 1 049 → absente des pages citées`. Le chiffre est pourtant **juste** : l'édition du 20/09 le portait avec sa source (*« 1 049 € (16 Go/256 Go) — +100 € sur le Mac mini M4 au tarif courant : consomac »*). Ce n'est donc pas un chiffre faux, c'est un chiffre **dont la provenance a été perdue en une semaine** alors que la phrase d'à côté montrait comment la garder.

**Et un fait est attribué à une page que la note elle-même déclare sans élément.** La hausse de juin 2026 — *« de 1 499 € à 1 799 € (entrée de gamme, **source consomac bons plans**, consultée sans élément dans la fenêtre) »* — crédite `consomac.fr/bonsplans-imac.html`, que la rubrique Sources range en **⚠️** avec le motif *« consultée, sans élément dans la fenêtre : dernières offres datées mai et juillet 2026 »*. Mesuré dans les deux sens : la passe D retrouve **1 499 et 1 799 sur cette page même** (`OK → consomac.fr/bonsplans-imac.html (texte)`), donc les valeurs y sont. Le défaut n'est pas le fait, c'est la **contradiction interne** — une page ne peut pas être la source d'un chiffre et n'avoir rien livré, et c'est la deuxième phrase du même document qui tranche contre la première.

**Le mur anti-automate de la Fnac et de Darty est réel, mesuré avec les deux agents, et c'est une réfutation de ce que j'aurais pu écrire.** Les trois ⛔ en 403 sont la tentation évidente du moment : la série a mesuré le 04/10 que la commande prescrite par les neuf prompts envoie un `-A "Mozilla/5.0"` **tronqué** et qu'un agent Chrome complet ouvre des pages qu'il ferme. Rejoué aujourd'hui, seul et espacé, faisceau compris : `fnac.com/informatique/imac-m4/q` rend **403 avec l'agent tronqué et 403 avec l'agent complet**, et `darty.com` rend **403** avec l'agent complet. La fiche du 04/10 l'avait déjà borné dans ces termes — *« Fnac rend 403 dans les deux cas : ce mur-là est réel »* — et ma mesure la **reproduit**. Les quatre ⛔ de la note sont donc correctement diagnostiqués, et la généralisation séduisante était fausse.

**La seule affirmation d'outillage de la note est vraie, et sa vérification borne un motif que j'ai livré hier.** La note écrit deux fois *« Apple Store officiel : prix rendus en JavaScript — non lisibles en headless »*. Mesuré aujourd'hui par `aspirer.py` sur `apple.com/fr/shop/buy-mac/imac` : **HTTP 200 · 424 450 octets bruts · 31 598 caractères utiles**, soit **dix fois le plancher de 3 000**, donc très loin d'une façade — et pourtant les **20 occurrences de `€`** de la page sont **toutes** des exemples de simulation de crédit Cetelem (*« Prix d'achat 1 500,00 € · TAEG fixe 14,95 % »*), **zéro prix de produit**, alors que la liste des configurations est bien servie (*« iMac, 24 pouces, M6 Puce, CPU 10 cœurs… »*). Le plancher de lisibilité détecte un **mur**, pas un **rendu partiel** : une page peut être dix fois au-dessus et rester inutilisable pour la donnée cherchée. C'est la deuxième borne mesurée du motif `FAÇADE ?` en deux jours, et elle vient du côté opposé à la première.

**Trois contrôles sortent en 0 et un quatrième est structurellement muet.** `controle_attributions.py` rend **0 problème bloquant** avec **quatre passes inertes** (B, B-NOM, C, C2) et trois pages non lues — les deux Fnac et Darty, celles-là mêmes que la note déclare. `controle_edition_precedente.py` rend **OK** sur ses trois axes : 25 citations d'origine dans le journal de N-1, 4 retenues, 3 jetons distinctifs, **aucun rejoué**. `controle_decompte.py` rend COHÉRENT. Mais **㊳ n'imprime rien du tout, exit 0** : `run_job.sh:494` purge les logs à **30 jours**, le log du 27/09 n'existe plus, et le contrôle qui vérifie qu'un livrable vient d'une exécution réussie n'a donc **aucune trace à lire**. C'est la portée mesurée le 24/10 — 51 documents sur 294 — observée en acte : ni le coût, ni les tours, ni le code de sortie de ce créneau ne sont récupérables, et aucun décompte de liens 🔗 n'existe pour cette édition.

**Un faux positif du contrôle des noms propres, et c'est la cinquième fois que l'aplatissement du `.docx` coûte une accusation.** `controle_noms_propres.py` rend *« NOM NON RETROUVÉ : « Côté Windows » ne figure sur AUCUNE des 9 pages LUE(s) »*. Ce n'est pas un nom propre : c'est l'ouverture de phrase *« Côté Windows, pas de bon plan notable repéré cette semaine »*, où « Côté » est capitalisé par sa position et « Windows » est le seul vrai nom de la paire. Le discriminant du 31/10 — le corpus pour dictionnaire, un jeton écrit aussi en minuscules n'est pas un nom propre — ne peut pas mordre ici : « côté » n'apparaît en minuscules ni dans ce document ni dans ses neuf pages lues. Le contrôle dit par ailleurs exactement ce qu'il faut (**3/12 pages non lues**, nommées), et il est **non bloquant** par construction. Deuxième bruit du même lot : la passe D liste `A VERIFIER 404` pour le *« ⛔ macg.co — 404 (page non trouvée) »* de la rubrique Sources — l'exemption ㊲ demande le nombre collé à `HTTP` ou à `curl`, et un tiret ne suffit pas.

**Ce qui n'est pas vérifiable retrospectivement doit être dit comme tel, pas accusé.** Les trois spécifications M6 de la note — *« Architecture 2 nm »*, *« 12 cœurs CPU, 12 cœurs GPU »*, *« Double Neural Engine 16 cœurs »* — sont attribuées à `macrumors.com/roundup/imac/`, une **page vivante** qui décrit aujourd'hui un iMac M6 commercialisé depuis le 6 novembre. La relire aujourd'hui ne dit rien de son état du 27 septembre : c'est la règle du 15/10 sur les propriétés volatiles, appliquée à un article entier. Ce qui est mesurable, et qui corrobore, est ailleurs : consomac écrit *« La puce gagne ainsi deux cœurs de CPU et de GPU, et second Neural Engine permettant de doubler les performances »*, ce qui donne bien 12c/12c depuis les 10c/10c du M4, et l'édition du 01/11 confirme *« jusqu'à 12 cœurs CPU et GPU »*. Les **16 cœurs** du Neural Engine, en revanche, ne sont portés par aucune page que j'aie pu lire.

### Requêtes passées

Quatre pages aspirées sur disque (`aspirer.py`), **aucune n'est entrée en contexte** ; appariement par `chercher.py`, degré ① exigé pour tout ce qui est entre guillemets ; fenêtres lues par `lire_page.py --autour`. Trois sondes `curl` de diagnostic, seules et espacées de 16 s, faisceau de certificats compris.

| Source (car. utiles mesurés) | Requêtes | Degré |
|---|---|---|
| `iphonote.com` — 387222 (6 173) | `au cours des derniers mois de 2026` · `Gurman` · `Bloomberg` · `23 août 2026` · `derniers mois` · `sept couleurs` | **① ×6, 0 absente** |
| `appsystem.fr` — 257168 (8 901) | `J833` · `J834` · `automne` · `Gurman` · `couleurs` | **① ×5, 0 absente** |
| `consomac.fr` — news-24460 (7 924) | `TSMC` · `première puce Apple Silicon` · `palette de couleurs inédite` · `couleur` | **① ×4** |
| `consomac.fr` — news-24460 | `2 nm` | ④ → fenêtre lue : *« gravée en 2 nanomètres par TSMC »* — **variante de graphie, pas une absence** |
| `consomac.fr` — news-24460 | `3 nanomètres` | **④ ABSENT** — le « M4 est en 3 nm » du 25/10 n'est pas sur cette page |
| `apple.com/fr/shop/buy-mac/imac` (31 598) | `1 799,00 €` · `1 999,00 €` · `1 799 €` · `À partir de` · fenêtre `€` ×20 | **③ confirmé** : aucun prix produit, 20 € de simulation de crédit |
| `fnac.com/informatique/imac-m4/q` | `curl` UA tronqué · UA complet | **403 / 403** — mur réel |
| `darty.com` — filtre 27 pouces | `curl` UA complet | **403** — mur réel |
| N-1 `2026-09-20_veille_imac.docx` | `13 iMac M4 reconditionnés` · `1 049 €` · `949 €` | **① ×3**, continuité exacte |
| `2026-10-04_veille_imac.fiche.md` | passage `Mozilla/5.0` | **①** — *« Fnac rend 403 dans les deux cas »* |

**Ce qui n'a PAS été interrogé, et il faut le dire.** `macrumors.com/roundup/imac/` n'a pas été relu : page vivante, son état du 27/09 est hors d'atteinte, et l'interroger aujourd'hui produirait un verdict sur un autre document. Les **deux pages LDLC** des modèles Windows n'ont pas été rouvertes : une fiche produit porte un prix et un stock qui dérivent, et les 1 699,95 € / 1 899,95 € du 27 septembre ne sont pas réfutables par la page du 6 novembre. `9to5mac.com/2026/09/` est une archive mensuelle, donc une page d'index : elle est exemptée de ⑩ par règle du 15/10 et ne prouve pas une absence. Les trois ⛔ en 403 n'ont pas été contournés — jamais `-k`, jamais `--insecure`. Et aucune mesure n'a été faite sur le **coût du créneau** : le log est purgé.

## Notes liées

- **⬅️ Précédente** · [[2026-09-20_veille_imac.fiche]]
  **elle a produit le garde-fou que cette note applique à moitié.** C'est l'édition qui a imposé de comparer le Mac mini M6 au **tarif courant** du M4 (949 €) et non à son prix de lancement (699 €), et elle portait ses deux chiffres avec leur source. Sept jours plus tard, le **949 € a gardé sa mention d'héritage et le 1 049 € l'a perdue** — dans la même phrase. Le garde-fou s'est transmis ; la provenance, non.
- **➡️ Suivante** · [[2026-10-04_veille_imac.fiche]]
  **elle a nommé ce squelette dès la semaine suivante, et il est resté vide trente-trois jours de plus.** Elle écrit *« fiche jamais écrite — stub de 294 octets posé le 27/09 et resté tel quel »* et mesure même l'écart de volume entre les deux notes. Une fiche peut donc diagnostiquer l'absence de sa voisine sans que rien ne la comble : **un constat dans une fiche n'est pas une tâche.** C'est aussi elle qui a mesuré le défaut d'agent tronqué, le **04/10**, avec sa borne.
- **🔗 Pont** · [[2026-10-25_veille_imac.fiche]]
  **l'autre squelette du même dossier, écrit le même jour que celui-ci, et le seul des deux dont le créneau a perdu sa publication.** Les deux éditions partagent la même phrase sur l'Apple Store rendu en JavaScript — vraie, et vérifiée ici pour les deux —, mais la note du 25/10 est celle où les spécifications M6 trouvent enfin une page qui les porte. Lues ensemble, les deux fiches montrent la même attribution se déplacer de source en source pendant cinq semaines.
- **🔗 Pont** · [[2026-11-06_veille_ai-act.fiche]]
  **écrite ce matin, et elle datait mal le défaut d'agent tronqué.** Elle annonce une *« récidive à sept jours »* en se référant à la fiche ai-act du 30/10. Or la mesure est **dans la série imac, au 04/10** — `dell.com` à 403 avec l'agent tronqué, **200 et 28 134 caractères** avec un agent complet. L'écart réel est de **trente-trois jours sur deux séries**, et le 06/11 est la **troisième** occurrence, pas la seconde. La leçon est plus dure que ce que j'avais écrit.
- **🗂️ Dossier** · [[iMac_dossier.fiche]]
  **le plancher de lisibilité du dépôt sort indemne de cette fiche, et élargi.** Ni les 31 598 caractères de l'Apple Store ni les 403 de la Fnac ne relèvent d'un mur au sens du motif livré le 05/11 : la première est riche et muette sur le seul chiffre utile, les seconds ne renvoient aucun corps. 📌 Piste bornée, non faite, non ordonnée : un verdict `PARTIEL ?` pour une page largement au-dessus du plancher dont la **classe de donnée cherchée** est absente — mais il faudrait savoir ce qu'on cherche, ce qu'un balayage d'adresses ne sait pas.
