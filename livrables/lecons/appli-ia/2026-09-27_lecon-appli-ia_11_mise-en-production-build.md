---
type: fiche-document
source: 2026-09-27_lecon-appli-ia_11_mise-en-production-build.docx
date_creation: 2026-09-27
date_lecon: 2026-09-27
parcours: appli-ia
numero: 11
statut: parcours-actif
tags:
  - parcours/appli-ia
  - registre/perso
  - module/mise-en-production
  - outil/vite
  - outil/node
  - outil/git
  - concept/build-production
  - concept/empreinte-de-contenu
  - concept/path-traversal
  - concept/sauvegarde
  - concept/defense-en-profondeur
  - alerte/memoire-contredit-lecon
  - alerte/garde-fou-outrepasse
  - alerte/ressource-non-exploitee
  - alerte/test-inerte
---

# 2026-09-27_lecon-appli-ia_11_mise-en-production-build

Document source : [[2026-09-27_lecon-appli-ia_11_mise-en-production-build.docx]]

## Résumé

**C'est l'exécution la mieux mesurée du parcours, et la première dont on connaisse le coût complet.** **4,2646 $ / 5,00 $ (85 %)**, **90 tours**, 32 min 44 s, **une seule tentative**, `[audit] vault conforme`, push OK. Le relèvement du plafond de 3 à 5 $, décidé deux heures plus tôt, était juste : **à 3 $ ce job aurait été tué**, et depuis le correctif du matin un dépassement ne publie plus rien. Jusqu'ici aucune exécution complète de ce job n'avait jamais abouti — celle du 26/09 est morte *à* 3,0689 $ sans faire l'étape 6. Tout a été rejoué : les **quatre décomptes de lignes sont exacts** (`serveur.js` 316, `sauvegarder.js` 132, `utils.js` 126, et `audit-securite.js` **151** — c'est-à-dire compté **après** ma correction du même matin, preuve que le job a lu le fichier corrigé et non sa version publiée) ; **vite 8.2.2** est réellement installé ; la sortie de `vite build` est reproduite **au caractère près, empreintes de contenu comprises** — `index-CY5p-_Kr.css` 3,21 kB / gzip 1,01 kB, `index-BrbzaqXI.js` 196,20 kB / gzip 61,95 kB, `index.html` 0,40 kB / gzip 0,27 kB, « ✓ 20 modules transformed » — seule la durée bouge (329 ms annoncés, 311 ms au rejeu), ce que la leçon présente bien comme une mesure. `npm test` rend **17 + 16 = 33 tests, 0 fail** ; la sauvegarde affiche mot pour mot **« ✓ Sauvegarde terminée : 12 élément(s) — 11 Ko copiés »** ; les quatre lignes de démarrage du serveur sont exactes ; **la page servie EST le build** (les deux mêmes empreintes dans le `<head>`) ; `sauvegardes/` est bien ignoré par git (`git status --short` vide). Quatre URL en **200**. **Étape 5 bis : les quinze motifs au vert** ; `controle_attributions` **0 bloquant**. `PROJET.md` a bougé (md5 `e41baf3e…` → `9f144841…`), compteur du tableau de bord à **11**.

**Les trois règles écrites ce matin ont passé leur première leçon — et l'une des trois était inerte.** (p) PROJET.md porte la leçon 11 et nomme tous ses fichiers source ✓ · (q) chaque engagement dû à la leçon 11 est nommé ou daté ✓ · (r) aucune sortie ne montre un repli à la place d'une valeur ✓. Mais l'acquittement de **(q) était gratuit**, et c'est vérifiable : rejoué avec le `PROJET.md` d'**hier** — celui où j'avais écrit « Reporté le 27/09/2026 à la leçon 11 » — et le `.docx` d'aujourd'hui, le test rend **exit 0**. Un report **daté par la leçon précédente** contient à la fois « leçon 11 » et une date : il satisfait le test pour toujours. La leçon a soldé ses deux dettes parce que le **texte** de la règle 26 le demandait, pas parce que son **test** pouvait la prendre en défaut. Correctif en une ligne : exiger que la date soit **celle de la leçon en cours**, ou que le report nomme une leçon **autre** que celle du jour. *Une règle dont la prose fonctionne et dont le test acquitte est la plus dangereuse : elle se croit tenue.*

**La plus belle preuve de la leçon est celle qu'elle ne pouvait pas truquer : elle affirme que son garde-fou 403 est inatteignable, et la mesure le confirme.** La théorie explique pourquoi — `new URL(req.url, …)` normalise d'abord la séquence (*« les .. au-delà de la racine sont ignorés — RFC 3986 §5.2.4 »*), puis `path.resolve` ramène dans l'arborescence autorisée. Vérifié en lançant le serveur : `GET /../../../etc/passwd` rend **404, pas 403** — la branche ne se déclenche jamais, exactement comme annoncé. La leçon garde le contrôle comme **défense en profondeur**, et l'argument est explicite : si l'un des deux maillons tombait, l'autre arrêterait la traversée. C'est ce raisonnement qui solde la dette **« Branche 403 inatteignable »** ouverte depuis le **21/08/2026**, et que j'avais reportée hier à cette leçon. L'autre dette reportée, le LIKE accentué, est soldée aussi — les deux avec un motif écrit, pas balayées.

**Trois défauts, et le plus gênant est dans la mémoire, pas dans la leçon.** ① **`PROJET.md` contredit la leçon sur `/api/db/search`, et solde une dette sur cette phrase fausse.** La mémoire écrit *« la route `/api/db/search` reste sur `nom LIKE`, ce qui est acceptable »* et s'en sert pour justifier un **« soldé le 27/09/2026 »**. Or `serveur.js` ligne 223 porte `WHERE slug_normalise LIKE @motif`, et la mesure tranche : `lecon` → **50** résultats, `leçon` → **50**, `evaluation` → **2**, `évaluation` → **2**. **La leçon a raison, la mémoire a tort**, et la dette est close sur un constat erroné — la réalité étant *meilleure* que ce que la mémoire prétend. Les deux textes ont été écrits par la même exécution, à une heure d'intervalle. ② **Le contrôle de l'étape 6 a refusé, et il a été outrepassé** : **42 lignes supprimées** dans `PROJET.md` pour un plafond de **40**. Le job l'a dit dans son récapitulatif — *« 2 au-dessus du garde-fou de 40, toutes sont des remplacements intentionnels »* — et l'inspection lui donne raison sur le fond (état de l'application, table des fichiers, « Reste à faire » : les trois sections que la règle autorise à remplacer). Mais **un contrôle mécanique écarté par le jugement de l'exécutant n'est pas un contrôle qui a tenu**, et sa transparence ne change pas cela : le plafond ne distingue pas le journal, où l'on ajoute, des trois sections qui décrivent un présent. ③ **« Git — Tagging » est listé deux fois en ressource et jamais exploité** : `git tag` **zéro** occurrence, « versionnage » **zéro**, « déploiement » **zéro**. La feuille de route annonce pour la leçon 11 *« build, versionnage Git, déploiement, sauvegardes »* — **deux des quatre** sont livrés, le `v1.0.0` de `package.json` étant le seul geste de versionnage, sans étiquette git.

**À corriger, à durcir, et l'avocat du diable.** **À corriger** : la phrase de `PROJET.md` sur `/api/db/search` (et la justification du soldé qui en dépend) ; la ressource Git Tagging, à exploiter ou à retirer. **À durcir** : (q) doit exiger une date **de la leçon en cours** ; le plafond de 40 lignes de l'étape 6 doit distinguer les trois sections remplaçables du journal, distinction que la règle fait déjà en prose et que son test ignore ; et **rien ne vérifie qu'une ressource listée est utilisée** — quatre URL testées en 200, dont une pour un thème absent. **Avocat du diable** : les thèmes de la feuille de route ne sont surveillés par aucun test dans ce parcours, alors que `placement-financier` a son motif ⑥ exactement pour ça — je l'ai signalé le 27/09 au matin et ne l'ai pas porté. Le coût complet étant désormais connu (**4,26 $**), le plafond à 5 $ ne laisse que **15 %** de marge sur un prompt qui a grossi de 84 % en un mois (64 372 → 118 352 octets). Et sur onze leçons, c'est la première fois que la leçon, le code, la mémoire et les mesures concordent presque entièrement — ce qui rend l'unique contradiction d'autant plus visible : **la seule phrase fausse de la journée est celle qui sert à clore un dossier.**

## Notes liées

- **⬅️ Précédente** · [[2026-09-26_lecon-appli-ia_10_securite-donnees]]
  la n°10 avait tout mesuré et rien retenu : plafond dépassé à 102 %, `PROJET.md` non mis à jour, un champ npm inexistant publié comme résultat. **Les trois règles nées d'elle ce matin (25, 26, 27) sont passées ici dès la première exécution** — et cette leçon compte `audit-securite.js` à 151 lignes, c'est-à-dire après la correction, preuve qu'elle a lu le fichier réparé
- **➡️ Suivante** · [[2026-10-02_lecon-appli-ia_12_maintenance-evolution-bilan]]
  **la dernière du parcours, et la mieux mesurée de la semaine** : les six numéros de version justes contre le registre npm, `maintenance.js` à 144 lignes comptées, et `npm run maintenance` qui reproduit son bloc de sortie mot pour mot — un seul « s » manquant. La ligne de « Reste à faire » que la 11 annonçait est barrée. Son seul défaut de fond est hors de portée des treize motifs : le Challenge fait appeler `npm build`, qui n'existe pas
- **🔗 Pont** · [[2026-09-18_lecon-appli-ia_08_api-architecture-contrats]]
  la leçon qui a motivé la règle de l'étape 6 — elle avait réécrit `PROJET.md` « en plus court », −122 lignes pour +80. Le plafond de 40 lignes vient de là ; aujourd'hui il refuse 42 suppressions **légitimes**, et il est outrepassé. *Un seuil posé contre un abus finit par gêner l'usage normal*
- **🔗 Pont** · [[2026-09-26_lecon-placement-financier_16_transmission-succession-demembrement]]
  son **motif ⑥** vérifie que les thèmes annoncés par la leçon précédente sont nommés. `appli-ia` ne l'a pas : c'est pourquoi « versionnage Git » et « déploiement » manquent sans que rien ne bronche, ressource Git Tagging listée à l'appui
- **🔗 Pont** · [[2026-09-27_lecon-revenus-passifs_10_esperance-de-vie-modeles]]
  l'autre leçon du jour, et le miroir : là-bas une SCPI réelle recevait des chiffres inventés, ici c'est la **mémoire du projet** qui affirme faux sur son propre code. Dans les deux cas le texte qui se trompe est celui qui sert à conclure — un « Maintenir + surveiller » d'un côté, un « soldé » de l'autre
- **🗂️ Dossier** · `livrables/projets/appli-ia/PROJET.md` (hors vault Obsidian)
