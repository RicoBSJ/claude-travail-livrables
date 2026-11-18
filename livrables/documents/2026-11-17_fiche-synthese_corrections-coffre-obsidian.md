---
type: note-correction
date_creation: 2026-11-18
date_corrections: 2026-11-17
portee: coffre Obsidian · audit_vault.py · harnais de non-régression
commits:
  - 0bdf0c0
  - 4ba999c
  - 3c036a1
tags:
  - registre/pro
  - coffre/obsidian
  - outil/audit-vault
  - outil/harnais
  - theme/un-detecteur-qui-voit-sans-pouvoir-refuser
  - theme/declenchement-n-est-pas-couverture
  - theme/vert-sur-une-question-non-posee
  - theme/garde-par-soustraction
  - theme/specimen-vivant-qui-perime
  - theme/avertissement-plutot-que-refus
---

# 2026-11-17_fiche-synthese_corrections-coffre-obsidian

Documents source : [[2026-11-16_veille_has-actualite.fiche]] · `outils/scripts/audit_vault.py` · `outils/scripts/non_regression.sh`

## Résumé

**Les deux corrections du 17/11 sont les deux moitiés d'une seule phrase, et c'est le message du premier commit qui l'écrit : « les 4 wikiliens suffixés `.md`, ET l'audit qui le disait sans pouvoir refuser ».** La première corrige un **livrable** — quatre liens morts dans une fiche de veille. La seconde corrige l'**outil** qui les avait nommés exactement, douze heures trop tard, dans un log qui annonce lui-même qu'il n'interrompt rien. Prises séparément, la première est une faute de frappe et la seconde un détail de câblage ; prises ensemble, elles disent qu'un défaut a vécu une journée entière alors qu'un script du dépôt l'avait vu.

### ① La fiche du 16/11 — quatre wikiliens suffixés `.md` (`0bdf0c0`)

**Le défaut est le suffixe, pas la cible.** Les quatre relations de la fiche écrivaient `[[…fiche.md]]` là où la règle Obsidian du coffre veut `[[…fiche]]` : quatre liens morts pour quatre cibles **qui existent sur le disque**. `audit_vault.py` le rendait en une ligne — `✗ Liens wiki résolus (règle Obsidian) — 4 problème(s)`, exit 1 — et nommait les quatre.

**La classe est bornée, et c'est mesuré, pas supposé** : un seul fichier, quatre occurrences sur les **1 475** liens du coffre, et les deux fiches voisines de la série (09/11, 02/11) écrivent **toutes** leurs relations sans `.md`. Faute de ma main, pas une dérive de convention. Remesuré le 18/11 : **0 wikilien suffixé `.md`** dans tout le coffre.

**Garde par soustraction** (règle du 26/10) : remettre `.md` rend le fichier d'avant au **sha256 identique**, le diff ne touche que les lignes **107 · 111 · 113 · 115**, et le delta est de **−12 octets exactement** (24 139 → 24 127 octets, remesuré). ⚠️ Et la ligne 27 — `[[2026-11-16_veille_has-actualite.docx]]` — est **intacte**, le motif étant ancré sur `.fiche.md]]` : un lien vers un `.docx` se résout par le **CHEMIN** et non par l'index des notes, ce sont **311** liens du coffre qui sont dans ce cas, et les écraser aurait cassé la ligne `Document source :` de chaque fiche.

**Validé dans les deux sens** : avant → 4 problèmes, exit 1 ; après → les 9 contrôles au vert, exit 0, et le contrôle `c9` passe de **2 à 0** fichier(s) en attente de publication. Un lien recassé → `✗ 1 problème(s)`, exit 1, l'audit **le nomme** ; fichier restauré au sha256 identique.

⛔ **Ni marqueur ni Journal des corrections, et c'est une décision explicite** : aucune affirmation ne change — ce qui bouge est le suffixe d'une étiquette de lien, que le lecteur voit identique avant et après. Précédent du **26/10** sur les `rels` orphelins, où le nettoyage ne laissait rien de visible non plus. **Si la trace est voulue, elle est à ajouter** : c'est une décision du propriétaire, pas un oubli.

### ② L'outil qui voyait sans pouvoir refuser (`4ba999c`, `3c036a1`)

**Le vrai défaut n'était pas les quatre liens : aucun push ne pouvait les refuser.** Recensement d'**appels** et non textuel, lignes commentées retirées : `audit_vault.py` est lancé **0 fois** par `non_regression.sh` (sa seule mention y est un commentaire, ligne 2436), **0 fois** par le hook (commentaire ligne 57), et **3 fois** par `run_job.sh:433` — **après `EXIT=0`**, dans une branche qui imprime d'elle-même *« le livrable a bien été produit ; l'audit n'interrompt rien »*. Il **est** dans `SURVEILLES`, mais c'est un **déclenchement**, pas une **couverture** — la distinction écrite le 11/11. Ma faute a vécu du 16 au 17/11, et la seule chose qui l'a dite est une ligne de log qui annonce qu'elle n'arrête rien.

**Deux changements bornés à l'outil** (9 333 → 10 849 octets, `fe4f79389df6617f` → `eaf42dc8f262952b`) :

- **`--racine <chemin>`, que la production ne passe JAMAIS** (mesuré sur `run_job.sh:434`). Il n'existe que pour qu'un témoin figé joue le **VRAI** `Audit` sur un coffre **fabriqué en `tempfile`** au lieu d'en recopier la logique — *un test qui teste une COPIE de la logique ne garde rien* (15/10). C'est la piste bornée du **23/10**, payée pour `controle_livrable_du_job.py` le 16/11 et reprise ici le lendemain. Sortie sur le coffre réel **identique à l'octet** avant et après, sha256 `47b606afa4048cb7` des deux côtés.
- **`c9` lit le CODE DE SORTIE de `git`.** Rejoué le 18/11 sur un dossier qui n'est pas un dépôt : la version d'avant imprime `✓ Aucune fiche ne partirait à l'auto-push (0 fichier(s) en attente de publication)` là où `git` répond **128** et `stdout` est **vide** — **un vert sur une question qu'elle n'avait pas pu poser**. Classe exacte du témoin de `supprimer_job.sh` (27/10, « les deux photos sont vides, donc égales ») et du garde `$SEMENCE non vide` du runner : *un garde satisfait par un état cassé*. Elle imprime désormais `○ Portée de l'auto-push — non vérifiable (git a répondu 128)`, **non bloquant** comme la branche d'exception au-dessus — on le **dit**, on ne tranche pas.

**Et le câblage : le mode `--coffre`, en avertissement.** `bloc_coffre` = un témoin figé (**bloquant**, 23 bornes, `ATTENDU_CF=23` lisant le **dénominateur**) + le verdict **réel** de `audit_vault.py` **en avertissement**, remonté avec la ligne qui **nomme** le lien fautif. Mesuré le 18/11 : `23/23`, `✓ 1475 liens`, **2,02 s et 2,34 s** (hier 1,73 · 1,74 · 2,00 s).

⛔ **Deux choses restent bloquantes et ne jugent AUCUN contenu** : le témoin, et le fait que l'audit **ait parlé** des liens — un détecteur muet rend indiscernables *« le coffre va bien »* et *« personne n'a regardé »*, même famille que le bloc `0 nonies` (26/10) et `corps_tronque.py` (04/11). Le verdict sur le coffre, lui, est un **avertissement** : un lien cassé dans une fiche n'est pas une régression du dépôt, et refuser le push punirait le livrable qui passe (14/10).

🔴 **Et la mesure a démenti ma propre piste, écrite une heure plus tôt.** J'avais annoncé « câblé sur une catégorie du hook ». Recensement : les **651** fichiers du coffre sont **déjà tous** dans `LIVRABLES` — **651/651**, 312 aussi dans `DOCS`, **0 dehors**. Une catégorie `COFFRE` dédiée aurait été **du code mort**, et une branche de hook morte se lit comme une couverture. La couverture est donc portée par les deux appels de `bloc_coffre` — le **chemin commun** et le mode **`--integrite`**, le seul qu'un push de fiche déclenche — et gardée par deux bornes qui **lisent `LIVRABLES` dans le hook** et exigent qu'un nom de fiche **FABRIQUÉ** y soit couvert : resserrer le motif, ou en faire une liste de séries, refuse.

### Ce que les deux corrections ont en commun

**Les deux sont des vérités que le dépôt possédait déjà et que personne ne lisait** — et c'est la troisième fois en huit jours. Le 11/11, `git status` montrait trois livrables abîmés par kDrive depuis cinq jours. Le 17/11, un log nommait quatre liens cassés en annonçant qu'il n'interrompt rien. **Ce qui manque n'est jamais le détecteur : c'est le moment où il parle, et le fait que quelqu'un soit tenu de répondre.**

### Avocat du diable

**Le gain est conditionnel à ce que quelqu'un lise la sortie du push.** Un avertissement noyé dans trente lignes de vert a exactement la forme qu'avait déjà la ligne du log du job — et elle n'a pas été lue le 16/11. Ce qui change n'est pas la visibilité, c'est **le moment** : au push la correction coûte une seconde, douze heures plus tard un commit, un cycle complet et une fiche. S'il est ignoré deux fois, la bonne réponse ne sera pas de crier plus fort mais de rendre bloquante **la seule classe mesurée sans faux positif** — un suffixe `.md` sur un lien dont la cible existe, qui est un défaut d'écriture et jamais un jugement de contenu. ⚠️ Et un second angle mort reste entier : `audit_vault.py` ne tourne dans `run_job.sh` qu'**après `EXIT=0`**, donc **un run en échec ne voit jamais son coffre** — exactement le cas où un livrable à moitié écrit peut y laisser une fiche incohérente.

### Mes propres défauts, quatre, aucun trouvé par la relecture

| | Défaut | Ce qui l'a dit |
|---|---|---|
| ① | Le bloc imprimait `1 problème(s)` **sans le lien fautif** — motif ancré aux lignes à deux espaces, le détail est à six | la lecture de la sortie du sens cassé — c'est le reproche exact que ma propre borne ④ fait au contrôle |
| ② | Ma borne ⑯ était un **compte global**, donc elle tombait avec ⑰ : deux bornes qui tombent ensemble n'en font qu'une (26/10) | le sabotage, pas la relecture |
| ③ | **Trois durées étaient estimées** et non mesurées | une relecture de mes propres chiffres |
| ④ | Le témoin **fuyait 330 dossiers `/tmp/coffre_*` (2,86 Mo)**, neuf par passage, sur un témoin que tout push touchant un contrôle exécute | mesuré **après** le premier push, c'est-à-dire après que je l'avais annoncé propre |

🟢 Le ④ est fermé par la **borne ㉓**, qui nettoie **puis** exige qu'il ne reste rien : une borne posée avant le nettoyage ne garde que l'intention. `ATTENDU_CF` 22 → 23.

🔴 **Et trois bornes de `categories_hook.py` sont tombées sur un dépôt JUSTE — aucune pour un invariant faux.** La ⑭ prenait pour spécimen `audit_vault.py` lui-même, choisi le 11/11 **précisément parce que** le harnais ne le mentionnait qu'en commentaire : le jour où il est vraiment lancé, elle est **satisfaite par la mauvaise chose**. La ㊼ cherchait sa fenêtre dans le **texte brut** du hook, qu'un commentaire nommant `--integrite` suffisait à déplacer. La ㊽ portait une fenêtre de **200 caractères en dur**. **La leçon de forme n'est pas « il fallait les durcir »** : une borne doit prendre un spécimen **FABRIQUÉ** quand elle teste une absence, et une fenêtre **STRUCTURELLE** quand elle teste un contenu — un spécimen réel qui dit aujourd'hui ce qu'on veut vérifier est un piège **à retardement, et il se referme le jour où le dépôt progresse**.

### Mesures passées (rejouées le 18/11, aucune réseau)

| Mesure | Verdict |
|---|---|
| `audit_vault.py` sur le coffre réel | `✓ Liens wiki résolus (1475 liens)` · `✓ auto-push (0 fichier)` · **les 9 contrôles au vert** |
| wikiliens suffixés `.md` dans le coffre | **0** |
| wikiliens `.docx` (résolus par chemin) | **311** |
| delta d'octets du commit `0bdf0c0` | 24 139 → 24 127, soit **−12** |
| version d'avant de `c9`, hors dépôt git | `✓ … (0 fichier(s))` pour un `git` à **128** — défaut reproduit |
| version d'après, même dossier | `○ … non vérifiable (git a répondu 128)` |
| sortie sur le coffre réel, avant vs après | **identique à l'octet**, sha256 `47b606afa4048cb7` |
| `non_regression.sh --coffre` | `23/23`, exit 0, **2,02 s** et **2,34 s** |
| chemins candidats contre `LIVRABLES` du hook | `livrables/documents/*.md` **couvert** — donc 0 orphelin au recensement |

Non rejoué aujourd'hui, mesuré hier : **16 sabotages, 16 refus**, chacun nommant **sa** borne, prouvant d'abord qu'il a modifié le fichier (sha256 avant → après) et restauré au sha256 identique ; harnais en mode défaut **exit 0, zéro `✗`**, deux fois (3 min 09 s et 3 min 12 s).

### Ce que STANDARD n'a pas interrogé

- **Le contenu des deux fiches du 17/11.** Leurs citations, leurs degrés d'appariement et leurs chiffres ne sont gardés par **aucun** contrôle du dépôt — `--coffre` vérifie que les liens **résolvent**, jamais que la fiche **dit vrai**.
- **Le push refusé une fois, pour une cause que je ne sais pas nommer.** Le run `--docs` imbriqué du témoin `0 nonies` est mort **dans le bloc du balayage d'adresses**, sortie tronquée à **2 018 octets**, sans aucun message d'échec, bien avant le coffre. Non reproductible : le même mode rejoué deux fois donne exit 0 et une sortie imbriquée complète (6 297 octets). `--no-verify` **n'a pas** été utilisé ; le push a simplement été relancé et le hook est passé. **Un enfant tué, pas un verdict changé — mais la cause reste inconnue.**
- **Les wikiliens de CETTE note ne sont vérifiés par aucun contrôle** : `c7` ne lit que `livrables/lecons/` et `sources/veille/`, et cette note vit dans `livrables/documents/`. Les **cinq** liens réels ont été vérifiés contre l'**index RÉEL** de `audit_vault.py`, importé et non recopié (règle du 15/10) : **5 sur 5 résolus** sur ses 323 noms. 🔴 **Et la mesure a trouvé autre chose, qui décide de l'emplacement de cette note** : elle cite **trois** formes de lien à titre d'exemple — la forme fautive, la forme juste et le lien `.docx` de la ligne 27 — et `c7` apparie `[[…]]` sur le **texte brut, sans égard pour les accents graves**. Déposée dans `livrables/lecons/` ou `sources/veille/`, cette note aurait donc fait **refuser trois liens qui n'en sont pas**, c'est-à-dire accusé sa propre documentation — le piège du **27/10**, où une coquille citée s'immunisait elle-même, pris par l'autre bout. Même remarque pour son `type: note-correction`, valeur que l'audit ne lit jamais ici — `c1` et `c2` ne contrôlent le type que dans les deux arbres qu'ils scannent.
- **Rien n'a été vérifié du côté d'Obsidian lui-même** : la règle « un wikilien ne porte pas l'extension » est celle que `audit_vault.py` implémente, et c'est elle qui a été rejouée, pas le comportement de l'application.

## Notes liées

- ⬅️ **Corrigée** — [[2026-11-16_veille_has-actualite.fiche]]
  **la fiche porteuse des quatre liens, et elle avait par ailleurs raison sur tout le reste.** Ses quatre relations pointaient vers des cibles existantes : le défaut n'a jamais touché une seule de ses affirmations. ⚠️ Et elle garde une dette indépendante de cette correction — son `➡️ Suivante` prescrit quatre vérifications pour l'édition du 23/11, dont la forme du récapitulatif des liens, déjà à son troisième report
- 🔗 **Pont** — [[2026-11-13_veille_ai-act.fiche]]
  **la même classe au même endroit du raisonnement, et c'est elle qui donne son nom à l'incident de `c9`.** Là-bas, une déclaration ㊳ annonçait « 0 bloquant » pour trois contrôles qui n'avaient **rien à examiner** — *une passe inerte n'est PAS une passe réussie*. Ici, `c9` annonçait « 0 fichier en attente » pour un `git` qui avait répondu **128**. Dans les deux cas, **un verdict vide est lu comme un verdict favorable**, et le dépôt sait compter des bloquants sans savoir compter des silences
- 🔗 **Pont** — [[2026-11-09_veille_has-actualite.fiche]]
  **elle avait déjà mesuré, huit jours plus tôt, que le job relit la note et jamais la fiche.** C'est le mécanisme général dont la correction ① est un cas particulier : une fiche peut porter la bonne prescription, ou la mauvaise étiquette de lien, sans qu'aucun chemin d'exécution ne la lise. `--coffre` ouvre exactement **un** de ces chemins, au moment du push, et seulement pour les liens
- 🗂️ **Dossier** — [[HAS-actualite_dossier.fiche]]
  à mettre à jour d'un point : la série a eu, le 16/11, un défaut **de fiche** et non de note — le premier de la série —, et il a été vu par un outil que le pipeline ne lançait nulle part où son avis comptait
